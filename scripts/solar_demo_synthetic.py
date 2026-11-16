# solar_demo_synthetic.py - GATE G2: pipeline verification on a planted event
# A toy active region with truths known by construction. Verifies:
#   T1 - the block onset (time + location) is predicted from the causal series
#   T2 - the observed delay is recovered from the light curves
#   T3 - the frozen zeta rule classifies all three planted outcomes
#   B  - the blind protocol: outcomes are unreadable before predictions exist
#   H  - the frozen-law SHA-256 integrity
import json, os, sys, hashlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v, predict, evaluate, baseline
from solar.hmi_inputs import make_grid, bipole_bz, eps_a_from_field

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
a_max = F["locked_constants"]["a_max"]["value"]
MP = 1.6726e-27

# ---------------- planted scenario ----------------
NX, NY, CELL = 32, 32, 3.0e7           # m
HEIGHT = 1.0e8                          # m  coronal extent
V_A = 3.0e23                            # m^3 participating volume (planted)
RHO_Q = 3.0e8 * 1e6 * MP                # quiet density
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
EPS_STAR = (C_Q / c0) ** 2              # block threshold (frozen law)
TAU_RAMP = 43200.0                      # s  planted ramp timescale (12 h)
DT_STEP = 3600.0                        # s  hourly series
N_FRAMES = 73                           # 0..72 h
TIMES = np.arange(N_FRAMES) * DT_STEP

X, Y = make_grid(NX, NY, CELL)
Bz = bipole_bz(X, Y, -2.2e8, 0.0, 2.2e8, 0.0, 1000.0, 8.0e7)
eps_raw = eps_a_from_field(Bz, X, Y)
eps_static = np.where(eps_raw < 0.5, 0.10, 1.0)   # planted two-zone AR: core 0.10, periphery 1.0
core_mask = eps_static <= 0.10
T_STAR = TAU_RAMP * np.log(0.10 / EPS_STAR)   # planted first crossing (s)

results = {}
# clean slate: the blind check must see no stale prediction from prior runs
for _kind in ("T1", "T2", "T3"):
    _f = os.path.join(config.PREDICTIONS_DIR, f"{_kind}_demo1.json")
    if os.path.exists(_f):
        os.remove(_f)
print("=" * 78)
print("GATE G2 - SYNTHETIC VERIFICATION (planted truths known by construction)")
print("=" * 78)
print(f"eps_star = {EPS_STAR:.4f}; planted first block at t* = {T_STAR/3600:.2f} h")

# ---------------- H: frozen-law integrity ----------------
raw = json.dumps({k: v for k, v in F.items() if k != "sha256"}, sort_keys=True, indent=1)
h = hashlib.sha256(raw.encode()).hexdigest()
results["frozen_hash_ok"] = (h == F["sha256"])
print(f"H. frozen-law SHA-256 intact: {results['frozen_hash_ok']}")

# ---------------- T1: block onset prediction ----------------
eps_core = [float(np.mean(eps_static[core_mask] * np.exp(-t / TAU_RAMP))) for t in TIMES]
t_predict_idx = 12
try:
    predict.read_outcome("demo1", "T1", {"x": 0, "y": 0, "t": T_STAR})
    results["blind_denial"] = False
except RuntimeError:
    results["blind_denial"] = True
print(f"B. outcome read BEFORE prediction correctly denied: {results['blind_denial']}")

t_star, dt = pi_v.block_onset_time(eps_core, TIMES, EPS_STAR, t_predict_idx)
cx = float(np.mean(X[core_mask])); cy = float(np.mean(Y[core_mask]))
predict.write_prediction("demo1", "T1",
    {"x": cx, "y": cy, "t": t_star, "dx": CELL, "dy": CELL, "dt": dt},
    made_at_index=t_predict_idx)
outcome = predict.read_outcome("demo1", "T1", {"x": 0.0, "y": 0.0, "t": T_STAR})
s = evaluate.score_t1(
    {"x": cx, "y": cy, "t": t_star, "dx": CELL, "dy": CELL, "dt": dt}, outcome)
results["t1"] = s
print(f"T1. predicted t* = {t_star/3600:.2f} h (+/- {dt/3600:.2f} h) vs planted {T_STAR/3600:.2f} h"
      f" at ({cx/1e7:.0f},{cy/1e7:.0f}) cells vs (0,0)  ->  hit: {s['hit']}")

# ---------------- T2: delay measurement fidelity ----------------
demand = 1.0 - np.array(eps_core)                     # closed share rising
t_d_half = TAU_RAMP * np.log(2.0)                     # half-rise of 1-e^{-t/tau}
LAG_PLANTED = 7200.0                                  # s
thermal = 1.0 / (1.0 + np.exp(-(TIMES - (t_d_half + LAG_PLANTED)) / 900.0))
t_d, t_th, lag_obs = evaluate.measure_delay(demand, thermal, TIMES)
results["t2"] = {"lag_planted": LAG_PLANTED, "lag_measured": lag_obs,
                 "fidelity_ok": abs(lag_obs - LAG_PLANTED) <= 0.1 * LAG_PLANTED}
L_ch = V_A ** (1.0 / 3.0)
tau_a = L_ch / C_Q
print(f"T2. lag planted {LAG_PLANTED:.0f} s, measured {lag_obs:.0f} s -> "
      f"fidelity: {results['t2']['fidelity_ok']}")
print(f"    frozen tau_a at block onset = {tau_a:.2f} s (the pre-registered "
      f"residual: model predicts ~seconds; real data will show hours - T2 is "
      f"exactly this confrontation)")

# ---------------- T3: three planted outcomes ----------------
ZETA_YIELD = pi_v.zeta_yield(a_max, L_ch, C_Q)
rho_map = np.full_like(eps_static, RHO_Q)

def classify(eps_series, times):
    pi_series = [(C_Q / c0) ** 2 / np.mean(e) for e in eps_series]
    zeta_dot = [pi_v.zeta_dot_map(np.full_like(rho_map, pi_series[k]),
                                  rho_map, np.full_like(rho_map, np.mean(eps_series[k])),
                                  V_A, mdot_deep).mean()
                for k in range(len(eps_series))]
    zeta = pi_v.integrate_zeta(zeta_dot, times)
    if zeta[-1] >= ZETA_YIELD:
        return "eruption", zeta[-1]
    if max(pi_series) > 1.0:
        return "blocked-settles", zeta[-1]
    return "accommodates", zeta[-1]

scen = {}
# (a) quiet: eps = 0.5 constant
eps_a = [np.full_like(eps_static, 0.5)] * N_FRAMES
scen["quiet"] = classify(eps_a, TIMES)[0]
# (b) confined: eps dips to 0.02 for 1 h then recovers
eps_b = []
for t in TIMES:
    e = 0.5 - 0.48 * np.exp(-((t - 24 * 3600) ** 2) / (2 * (1800.0) ** 2))
    eps_b.append(np.clip(np.full_like(eps_static, e), 0.02, 1.0))
scen["confined"] = classify(eps_b, TIMES)[0]
# (c) eruptive: eps = 0.01 held for 5 days (long enough for zeta to
#     reach zeta_yield ~ 3.9 days after block onset)
N_C = 121
TIMES_C = np.arange(N_C) * DT_STEP
eps_c = [np.full_like(eps_static, 0.01)] * N_C
scen["eruptive"], zeta_c = classify(eps_c, TIMES_C)
print(f"T3. zeta_yield = {ZETA_YIELD:.3e}; planted outcomes -> classified:")
for k, v in scen.items():
    print(f"    {k:10s} -> {v}")
results["t3_correct"] = (scen == {"quiet": "accommodates",
                                  "confined": "blocked-settles",
                                  "eruptive": "eruption"})
print(f"    all three correct: {results['t3_correct']}")

# ---------------- baseline runs on the same three ----------------
core_x, core_y = baseline.core_centroid(Bz, X, Y)
proxy = baseline.free_energy_proxy(Bz)
dbl = baseline.doubling_time([proxy] * N_FRAMES, TIMES)
print("B0. baseline (magnetic free-energy): core at "
      f"({core_x/1e7:.0f},{core_y/1e7:.0f}) cells; doubling time {dbl} s "
      f"(constant planted flux - no growth signal, as expected)")

# ---------------- gate ----------------
gate = all([results["frozen_hash_ok"], results["blind_denial"], results["t1"]["hit"],
            results["t2"]["fidelity_ok"], results["t3_correct"]])
results["gate_G2"] = "PASS" if gate else "FAIL"
with open(os.path.join(config.RESULTS_DIR, "gate_G2_result.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1)
print("-" * 78)
print(f"GATE G2: {results['gate_G2']}")
if not gate:
    sys.exit(1)
