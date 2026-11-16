# full_run_everything.py - the whole stack, one command, the heat trail to follow
import subprocess, sys, os, time
ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, "..", ".venv-solar", "Scripts", "python.exe")
RUNS = [
    ("run_full_framework.py", None),
    ("anomaly_sweep_2026_10_21.py", None),
    ("run_all_rotation_catalogs.py", None),
    ("heat_tying_expansion_ledger.py", None),
    ("entropy_heat_drop_track.py", None),
    ("stellar_shell_size_law.py", None),
    ("galaxy_weather_report.py", None),
    ("forecast_pressure_drop_precursor.py", None),
    ("stage4_wall_void_y_contrast.py", None),
    ("merger_neck_yield.py", None),
    ("lepton_t7_unspool_closed.py", None),
    ("t6_lorentz_legs_closed.py", None),
    ("t27_cubic_tempo_closed.py", None),
    ("k_h0_bridge.py", None),
    ("neutron_fold_closed.py",
    "navier_stokes_bkm_regularity.py",
    "yang_mills_mass_gap_proof.py",
    "nuclear_force_bunny.py",
    "complete_electroweak_cavitation_closure.py", None),
]
out = open(os.path.join(ROOT, "full_run_2026-10-21.log"), "w", encoding="utf-8", errors="replace")
ok = fail = 0
for script, args in RUNS:
    p = os.path.join(ROOT, script)
    if not os.path.exists(p):
        out.write("===== %s MISSING =====\n" % script)
        fail += 1
        continue
    t0 = time.time()
    try:
        r = subprocess.run([PY, p] + ([args] if args else []), capture_output=True, text=True, timeout=1800)
        code = r.returncode
        out.write("===== %s | exit %d | %.0fs =====\n%s\n" % (script, code, time.time() - t0, (r.stdout or "")[-3000:]))
        out.flush()
        if code == 0:
            ok += 1
            print("[OK]   %s (%.0fs)" % (script, time.time() - t0), flush=True)
        else:
            fail += 1
            print("[FAIL] %s exit %d" % (script, code), flush=True)
    except subprocess.TimeoutExpired:
        fail += 1
        out.write("===== %s TIMEOUT =====\n" % script)
        print("[TIMEOUT] %s" % script, flush=True)
out.write("TALLY: %d ok, %d failed of %d\n" % (ok, fail, len(RUNS)))
out.close()
print("TALLY: %d ok, %d failed of %d" % (ok, fail, len(RUNS)), flush=True)
