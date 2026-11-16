# stage3_tau_choke_derivation.py - closure #5: the differential-limited choke
# Jaden's mechanism (2026-10-18, corrected): the corona does NOT swallow
# untied waves. The untied waves are WARMER and more BUOYANT - they ARE the
# boundary. The choke = the DIFFERENTIAL between the buoyant layer and the
# cooler lattice - the differential makes re-unification (absorption) hard.
# The corona keeps untying; without absorption local P and T rise; the waves
# want to spread and cannot; pressure builds; the corona heats above the
# surface. The medium accepts only at the rate it can MAKE THE ROOM
# (entropy-competitive); the tension is the stabilising factor.
# -> tau_choke = the buoyant layer's equalization time through the
#    differential at the acceptance (room-making) rate.
# Also: the vertical structure - hot core, cool phase-pinned surface, hot
# corona: T_core > T_corona > T_surface.
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2

V_A = 1.21e25           # m^3  AR box
EPS0 = 1.0e-5           # the SEALED core share (PFSS will measure; proxy floor was 0.02)
DELTA_GAP = s ** 2      # the 2-D wave-gap fraction

# ---- tau_choke: differential-limited equalization ----
# stored pressure-energy at the fault: K * delta_gap * V_a
# absorption power at the choke: f_esc * mdot_deep * (1-eps) * c0^2
E_fault = K_Q * DELTA_GAP * V_A
P_absorb = f_esc * mdot_deep * (1.0 - EPS0) * c0 ** 2
tau_choke = E_fault / P_absorb

print("=" * 78)
print("CLOSURE #5 - THE ABSORPTION-LIMITED CHOKE (Jaden's mechanism)")
print("=" * 78)
print(f"stored pressure-energy at the fault:  E_fault = K*delta_gap*V_a")
print(f"  K = rho C^2 = {K_Q:.2e} Pa, delta_gap = s^2 = {DELTA_GAP:.4e}")
print(f"  E_fault = {E_fault:.2e} J")
print(f"absorption power at the choke:  P_absorb = f_esc*mdot_deep*(1-eps)*c0^2")
print(f"  f_esc = {f_esc:.2e}, mdot_deep = {mdot_deep:.2e} kg/s")
print(f"  P_absorb = {P_absorb:.2e} W  (the corona's own share of the star's output)")
print(f"tau_choke = E_fault/P_absorb = {tau_choke:.2e} s = {tau_choke/86400:.2f} days")
print()
print("THE CLOSURE CHECK against the observed AR 12192 day:")
# observed load: E_B grew ~1e25 J over the day (proxy) -> ~1.2e20 W average
P_load_obs = 1.2e20                      # W  day-average flux load (HMI proxy scale)
E_fault_obs = E_fault
t_fault_obs = E_fault_obs / P_load_obs
print(f"  observed day-average load ~ {P_load_obs:.1e} W")
print(f"  time to pack the fault: E_fault/load = {t_fault_obs/86400:.2f} days")
print(f"  observed flare cadence in AR 12192: 6 X-flares / 10 days ~ 1.7 days")
print()
print("the sealed-core block + runaway check:")
mdot_load = P_load_obs / c0 ** 2        # the load-driven untying demand
V_dem = mdot_load / RHO_Q
V_cap = V_A * EPS0 / tau_choke
piv = V_dem / V_cap
print(f"  demand from the load: {mdot_load:.2e} kg/s -> V_dem = {V_dem:.2e} m^3/s")
print(f"  sealed-core accommodation: eps={EPS0:.0e} -> V_cap = {V_cap:.2e} m^3/s")
print(f"  Pi_V = {piv:.1f}  ->  {'BLOCKED (fault lines load up)' if piv > 1 else 'open'}")
print()
print("the runaway (the dam break): m_u = m_u0/(1-eps); at eps -> eps_max=0.3")
print(f"  V_dem(relief) = {V_dem/0.7:.2e} m^3/s vs V_cap(eps=0.3) = "
      f"{V_A*0.3/tau_choke:.2e} m^3/s -> "
      f"{'RUNAWAY WINS (eruption)' if V_dem/0.7 > V_A*0.3/tau_choke else 'dam re-holds (confined)'}")
print()
print("THE VERTICAL STRUCTURE (the phase-pinned surface):")
T_core = 1.57e7      # K  interior-model comparison value (Perplexity's table)
T_corona = 1.5e6     # K  the blocked buoyant layer (frozen observation equation)
T_surface = 5800.0   # K  the tying phase-transition pin (observed)
print(f"  T_core   = {T_core:.2e} K  (the forge - hottest)")
print(f"  T_corona = {T_corona:.2e} K  (the blocked buoyant layer - hotter than the surface)")
print(f"  T_surface= {T_surface:.2e} K  (trapped between them -> the tying phase change pins it)")
print(f"  ordering: T_core > T_corona > T_surface  ->  "
      f"{T_core > T_corona > T_surface}")
print(f"  the surface is cool BECAUSE the crossing energy is spent on the phase")
print(f"  change (latent), not on temperature - the boiling layer of the medium.")
print(f"  OPEN ITEM: deriving the pin's value (5800 K) from the heat:wave ladder")
print(f"  at the photospheric pressure.")
print()
print("SENSITIVITY - the consistency window (fault onset days vs sealed eps):")
print(f"  {'eps_sealed':>12s} {'Pi_V':>10s} {'fault_onset':>14s}")
for eps in (1e-6, 3e-6, 1e-5, 3e-5, 1e-4):
    vcap = V_A * eps / tau_choke
    piv = V_dem / vcap
    t_fault = E_fault / max(P_load_obs * (piv - 1) / piv, 1e-30) if piv > 1 else float("nan")
    print(f"  {eps:12.0e} {piv:10.1f} {('blocked, ' + f'{t_fault/86400:.1f} d') if piv > 1 else 'open'}")
print()
res = {"tau_choke_s": tau_choke, "tau_choke_days": tau_choke/86400.0,
       "E_fault_J": E_fault, "P_absorb_W": P_absorb, "delta_gap": DELTA_GAP,
       "K_Q": K_Q, "fault_onset_days_observed_load": t_fault_obs/86400.0,
       "Pi_V_sealed": piv,
       "vertical_structure": {"T_core": T_core, "T_corona": T_corona,
                              "T_surface": T_surface,
                              "ordering_holds": bool(T_core > T_corona > T_surface)}}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "tau_choke_derivation.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("result written:", out)
