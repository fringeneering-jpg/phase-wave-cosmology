# run_parallel_knots.py - Crash-proof incremental threshold scan around E_lock
import os
# CRITICAL: Stop NumPy/OpenBLAS from spawning 8 threads per worker (prevents 64-thread CPU thrashing)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import gc
import importlib.util
import json
import multiprocessing as mp
import time
import traceback
import numpy as np

RESULTS_FILE = "threshold_scan_results.json"
Nx, L, x0, w, T_end = 1024, 60.0, 15.0, 2.0, 100.0

# SUPER-THRESHOLD FORGE (2026-10-20): the pulse compresses BEYOND rho_max
# (Ruling #29's non-decompressing regime). Under the current EOS the
# crossing is at peak rho ~ 1.06 (drho ~ 0.76) and the cold weld (phi >
# 0.95) fires at e_avail >= 3.10 (drho ~ 0.79). Ordered to hit the weld
# FIRST (0.80, 0.85, 0.90), then the crossing band (0.75-0.78).
CASES = [0.80, 0.85, 0.90, 0.75, 0.76, 0.78, 0.95, 1.00]


def load_existing_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                data = json.load(f)
                # Keep only non-failed completed runs
                return {round(row["drho"], 2): row for row in data if not row.get("failed", False)}
        except Exception:
            return {}
    return {}


def save_results_dict(results_dict):
    ordered = [results_dict[k] for k in sorted(results_dict.keys())]
    tmp_file = RESULTS_FILE + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(ordered, f, indent=2)
    os.replace(tmp_file, RESULTS_FILE)


def worker(drho):
    t0 = time.time()
    try:
        spec = importlib.util.spec_from_file_location("dkh", "dynamic_knot_HDF.py")
        dkh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dkh)

        res = dkh.run_case(f"scan-{drho:.2f}", Nx, L, x0, w, drho, T_end)
        h = res["hist"]
        if len(h["t"]) == 0:
            return dict(drho=drho, failed=True, error="Empty history")

        retained = bool(h["Rknot"][-1] > 0.0)
        out = dict(
            drho=drho,
            peak_e_avail=float(res["peak_e_avail"]),
            E_lock=float(dkh.E_lock),
            final_t=float(h["t"][-1]),
            E_drift_max=float(np.abs(h["E_total"] - res["E0"]).max() / res["E0"]),
            M_drift_max=float(np.abs(h["M"] - res["M0"]).max() / res["M0"]),
            rhomax_reached=float(h["rhomax"].max()),
            Rknot_final=float(h["Rknot"][-1]),
            Rknot_max=float(h["Rknot"].max()),
            RETAINED=retained,
            wall_time_s=round(time.time() - t0, 2),
        )
        # Explicitly free massive history arrays before returning across IPC pipe
        del res, h
        gc.collect()
        return out

    except Exception as e:
        return dict(
            drho=drho,
            failed=True,
            error=str(e),
            traceback=traceback.format_exc(),
            wall_time_s=round(time.time() - t0, 2),
        )


if __name__ == "__main__":
    completed = load_existing_results()
    # If you already confirmed drho=0.40 earlier, this skips re-running any finished case
    pending = [c for c in CASES if round(c, 2) not in completed]

    print(f"Loaded {len(completed)} completed cases. {len(pending)} cases remaining: {pending}")

    # Use at most (CPU cores - 1) or 4 workers if RAM is tight, recycling each process after 1 task
    n_workers = min(len(pending), max(1, (os.cpu_count() or 4) - 1))

    if pending:
        with mp.Pool(processes=n_workers, maxtasksperchild=1) as pool:
            for row in pool.imap_unordered(worker, pending):
                drho_key = round(row["drho"], 2)
                completed[drho_key] = row
                save_results_dict(completed)

                flag = (
                    "RETAINED"
                    if row.get("RETAINED")
                    else ("FAILED" if row.get("failed") else "not retained")
                )
                print(
                    f"[SAVED] drho={row['drho']:.2f} | "
                    f"e_avail={row.get('peak_e_avail', float('nan')):.4f} | "
                    f"rho_max={row.get('rhomax_reached', float('nan')):.3f} | "
                    f"Rknot_final={row.get('Rknot_final', float('nan')):.4f} | "
                    f"time={row.get('wall_time_s', 0):.1f}s -> {flag}",
                    flush=True,
                )
                if row.get("failed"):
                    print(f"   Error detail: {row.get('error')}", flush=True)

    print("\n=== THRESHOLD SCAN SUMMARY ===")
    for k in sorted(completed.keys()):
        row = completed[k]
        flag = "RETAINED" if row.get("RETAINED") else ("FAILED" if row.get("failed") else "not retained")
        print(
            f"  drho={row['drho']:.2f}  e_avail={row.get('peak_e_avail', float('nan')):.4f} "
            f" rho_max={row.get('rhomax_reached', float('nan')):.3f}  "
            f"Rknot_final={row.get('Rknot_final', float('nan')):.4f}  -> {flag}"
        )