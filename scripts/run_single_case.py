# run_single_case.py - the minimal decisive case, one process, no pool (2026-10-15)
# The pair's pool stalled. This is the simplest possible runner: drho=0.42
# (the super-threshold RETAINED candidate, the side that decides the 0.4143
# crossing), Nx=512, one process, progress printed to the log directly.
from dynamic_knot_HDF import run_case, summarize
import json, os

CASES = [dict(label="scan-0.414", Nx=1024, drho=0.414)]
OUT = "threshold_scan_results.json"

results = []
if os.path.exists(OUT):
    try:
        results = json.load(open(OUT))
    except Exception:
        results = []
    results = [r for r in results if r.get("drho") != 0.42]

for c in CASES:
    res = run_case(c["label"], c["Nx"], L=1.0, x0=0.5, w=0.06, drho_pulse=c["drho"], T_end=100.0)
    summarize(res)
    entry = dict(drho=c["drho"], peak_e_avail=float(res["peak_e_avail"]), E_lock=2.889795918367347,
                 final_t=float(res["final_t"]), E_drift_max=float(abs(res["hist"]["E_total"]-res["E0"]).max()/res["E0"]) if len(res["hist"]["t"]) else -1,
                 M_drift_max=float(abs(res["hist"]["M"]-res["M0"]).max()) if len(res["hist"]["t"]) else -1,
                 rhomax_reached=float(res["hist"]["rhomax"].max()) if len(res["hist"]["t"]) else -1,
                 Rknot_final=float(res["hist"]["Rknot"][-1]) if len(res["hist"]["t"]) else -1,
                 Rknot_max=float(res["hist"]["Rknot"].max()) if len(res["hist"]["t"]) else -1,
                 RETAINED=bool(res["hist"]["Rknot"][-1] > 0.0) if len(res["hist"]["t"]) else False)
    results.append(entry)
    json.dump(results, open(OUT, "w"), indent=2)
    print(f"[DONE] drho=0.414 RETAINED={entry['RETAINED']} -> {OUT}", flush=True)


