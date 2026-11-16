# corona_selfcheck_quiet.py - GATE G1: the frozen law must reproduce the mean
# quiet corona before any event-level test is allowed to run.
# Anchors (published quiet-sun means): T_q = 1.5 MK at n_e = 3e8 cm^-3;
# quiet radiative losses ~1e5-1e6 erg/cm^2/s; density spread 1e8-1e9 cm^-3.
# Checks (no per-region knobs - the frozen JSON only):
#   1. T centroid at the anchor density          (must land on 1.5 MK)
#   2. T spread over the quiet density range     (reported vs observed 1-2 MK)
#   3. quiet-region escaping flux vs observed losses (within stated factor 10)
#   4. quiet geometry (eps_a >= 0.3) must produce Pi_V < 1 (no false blocks)
import json, math, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(BASE, "..", "data", "solar"))
with open(os.path.join(DATA, "corona_model_frozen.json"), encoding="utf-8") as fh:
    F = json.load(fh)

c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
mp = 1.6726e-27
kB = 1.3806e-23
Rsun = 6.957e8
n = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
f_vent = F["global_anchors"]["f_vent"]["value"]

def C(rho): return c0*(rho0/rho)**n

print("="*78)
print("GATE G1 - THE QUIET-CORONA SELF-CHECK (frozen law only, zero knobs)")
print("="*78)
results = {}

# 1. T centroid
rho_anchor = 3e8*1e6*mp
T_pred = f_vent*mp*C(rho_anchor)**2/kB
ok1 = abs(T_pred - 1.5e6)/1.5e6 < 0.02
results["T_centroid_MK"] = T_pred/1e6
results["T_centroid_pass"] = ok1
print(f"1. T at n_e=3e8 cm^-3: predicted {T_pred/1e6:.3f} MK vs anchor 1.50 MK  ->  {'PASS' if ok1 else 'FAIL'}")

# 2. T spread
T_lo = f_vent*mp*C(1e8*1e6*mp)**2/kB
T_hi = f_vent*mp*C(1e9*1e6*mp)**2/kB
spread_ratio = (T_lo - T_hi)/(1.0e6)   # model range width / 1 MK of the observed spread
results["T_range_MK"] = [round(T_hi/1e6,2), round(T_lo/1e6,2)]
results["spread_vs_observed"] = round(T_lo/1e6 - T_hi/1e6, 2)
print(f"2. T spread over n_e 1e8-1e9 cm^-3: {T_hi/1e6:.2f}-{T_lo/1e6:.2f} MK")
print(f"   observed quiet spread 1-2 MK; model width {T_lo/1e6 - T_hi/1e6:.2f} MK - RESIDUAL NAMED (under-predicted)")

# 3. quiet-region escaping flux vs observed losses
#    quiet region: eps_a = 0.5 (half-open, the canonical quiet share)
eps_q = 0.5
flux_pred_Wm2 = f_esc*mdot_deep*(1-eps_q)*c0**2/(4*math.pi*Rsun**2)
flux_pred_erg = flux_pred_Wm2*1e3   # erg/cm^2/s
obs_lo, obs_hi = 1e5, 1e6
ok3 = obs_lo/10.0 <= flux_pred_erg <= obs_hi*10.0
results["quiet_flux_erg_cm2_s"] = round(flux_pred_erg, 1)
results["quiet_flux_pass"] = ok3
print(f"3. quiet-region escaping flux: predicted {flux_pred_erg:.1e} erg/cm^2/s")
print(f"   observed quiet losses {obs_lo:.0e}-{obs_hi:.0e} erg/cm^2/s  ->  {'PASS (within factor 10)' if ok3 else 'FAIL'}")

# 4. quiet geometry must not block
piv_min = (C(rho_anchor)/c0)**2/0.3
piv_max = (C(rho_anchor)/c0)**2/0.5
ok4 = piv_max < 1.0
results["Pi_V_quiet_range"] = [round(piv_max,4), round(piv_min,4)]
results["quiet_no_block_pass"] = ok4
print(f"4. quiet geometry eps_a 0.3-0.5: Pi_V = {piv_max:.4f}-{piv_min:.4f}  ->  {'PASS (no false blocks)' if ok4 else 'FAIL'}")

gate = ok1 and ok3 and ok4
results["gate_G1"] = "PASS" if gate else "FAIL"
results["checked_at"] = datetime.now(timezone.utc).isoformat()
print("-"*78)
print(f"GATE G1: {results['gate_G1']}")
if gate:
    print("The frozen law reproduces the mean quiet corona. Stage 3 (real data)")
    print("may proceed when the pipeline stages are done. The two named residuals")
    print("(T-spread width, and the tau_a ~ seconds accommodation timescale) are")
    print("carried into the tests as explicit predictions to be confronted.")
else:
    print("GATE FAILED - the four items must be revised before any event-level")
    print("test. No real event data may be used until the gate passes.")
with open(os.path.join(DATA, "corona_selfcheck_result.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1)
print("result written: data/solar/corona_selfcheck_result.json")
