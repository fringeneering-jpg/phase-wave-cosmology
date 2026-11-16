# stage3_restricted_volume.py - the 7% is the VOLUME GROWTH being refused (2026-10-18)
# Jaden's correction: it's not the photon mass traveling at c that's the
# force - it's the VOLUMETRICALLY INSANE GROWTH of the untying knots that
# is RESTRICTED, with the heat amplifying the issue COMPOUNDINGLY.
# The numbers: each restricted kg of untying demands dV_u = 1/rho (~2e12
# m^3). The restricted volume rate = m_rest x dV_u. The heat feedback
# multiplies the demand, which is itself restricted - the compound.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27

L_SUN = 3.828e26
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
V_A = 1.21e25
DELTA_GAP = s ** 2

M_REST = 0.07 * L_SUN / c0 ** 2        # the restricted untying mass rate
DV_U = 1.0 / RHO_Q                     # the volume each kg demands
V_REST = M_REST * DV_U                 # the restricted VOLUME growth rate

V_EARTH = 1.083e21                     # m^3
V_CORONA = 6.0e26                      # m^3 (the shell's order)
V_FAULT = DELTA_GAP * V_A              # the fault's strain capacity (volume)

print("=" * 78)
print("THE 7% IS THE VOLUME GROWTH BEING REFUSED - the full scale")
print("=" * 78)
print(f"the restricted untying mass: {M_REST:.3e} kg/s (7% of the deep channel)")
print(f"each kg demands dV_u = 1/rho = {DV_U:.3e} m^3")
print(f"-> the RESTRICTED VOLUME GROWTH: V_rest = {V_REST:.3e} m^3/s")
print()
print(f"that is {V_REST/V_EARTH:.2f} EARTH-VOLUMES PER SECOND - refused")
print(f"per day: {V_REST*86400:.2e} m^3 = {V_REST*86400/V_CORONA*100:.1f}% of")
print(f"the corona's own volume")
print(f"the fault's strain capacity (delta_gap x V_a) = {V_FAULT:.2e} m^3:")
print(f"the restricted rate fills it every {V_FAULT/V_REST:.0f} seconds")
print()
print("the compounding (the heat's amplification):")
print("  the refused growth becomes the stalled pressure -> the stalled heat ->")
print("  the heat multiplier (1 + kappa x over_heat) raises the untying demand")
print("  -> MORE volume demanded -> MORE refused -> MORE heat - the compound.")
print("  Each cycle multiplies the issue; the throttle is the only thing")
print("  holding the circle at the controlled burn instead of the runaway.")
print()
print("the reading: the 7% is not a modest mass stream - it is the star's")
print("untying demanding ~half an Earth-volume of NEW space every second and")
print("the choke refusing it, with the refusal's own heat feeding the demand")
print("compoundingly. The vacuum model can't see the refused growth at all;")
print("the field feels every cubic metre of it.")
res = {"M_restricted": M_REST, "dV_u": DV_U, "V_restricted_m3_s": V_REST,
       "earth_volumes_per_second": V_REST / V_EARTH,
       "corona_pct_per_day": V_REST * 86400 / V_CORONA * 100,
       "fault_fill_seconds": V_FAULT / V_REST}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "restricted_volume.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
