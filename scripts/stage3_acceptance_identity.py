# stage3_acceptance_identity.py - the acceptance speed, identified (2026-10-18)
# The choke = the high-tension high-pressure coronal field trying to expand
# into the high-tension, PRESSURE-STABLE (expanding) and adiabatically
# COOLING baseline field. The resistance = the entropic rates maintaining
# the pressure of expansion - the same machinery regulating the burn, the
# expansion, and the growth. This script states the two fields, computes
# the acceptance rate identity, and ties tau_choke to it.
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
s = F["locked_constants"]["s"]["value"]
R_p = F["locked_constants"]["R_p"]["value"]
MP = 1.6726e-27

RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
V_A = 1.21e25
DELTA_GAP = s ** 2

# ---- the global entropic rate (the wall) ----
H_wall = rho0 * c0 / (rho_max * R_p)     # s^-1  the discrete unlocking rate

print("=" * 78)
print("THE ACCEPTANCE SPEED, IDENTIFIED - the two fields and the one rate")
print("=" * 78)
print("the two fields at the choke:")
print(f"  LOCAL GEOMETRIC FIELD (corona): high tension, HIGH pressure,")
print(f"    trying to expand. K = rho C^2 = {K_Q:.2e} Pa; the stall's stored")
print(f"    pressure-energy = K*delta_gap*V_a = {K_Q*DELTA_GAP*V_A:.2e} J")
print(f"  UNIVERSAL BASELINE FIELD: high tension, PRESSURE STABLE - it expands")
print(f"    (d ln V/dt = 3 H_wall, H_wall = {H_wall:.2e} s^-1) and cools")
print(f"    adiabatically (T ~ a^-2, the heat diluting into the new volume).")
print()
print("the one entropic rate, three readings:")
M_SUN = 1.989e30
rate_star = mdot_deep / M_SUN          # per-kg burn rate of the star
print(f"  THE BURN:   the star's controlled-burn rate = mdot_deep/M_sun = "
      f"{rate_star:.2e} s^-1 per kg")
print(f"  THE EXPANSION: the wall rate H_wall = {H_wall:.2e} s^-1 (per knot)")
print(f"  THE GROWTH:  structure's growth reads the same machinery")
print(f"  -> the star runs {H_wall/rate_star:.0f}x hotter per unit mass than the")
print(f"     global wall: the heat's return accelerates the front locally")
print(f"     (the speed-up law's tightening - the star is a hot spot in the web)")
print()
print("the loop's symmetry - the untying runs the same tempo:")
FACTOR = H_wall / rate_star
G_star = FACTOR * H_wall                    # the star's per-kg untying rate
M_active = mdot_deep / G_star               # the consuming skin this implies
print(f"  the star's knots untie at the SAME factor: Gamma_star = {FACTOR:.0f} x")
print(f"  Gamma_ambient = {G_star:.2e} s^-1 per kg of ACTIVE matter")
print(f"  -> the star's consuming skin: M_active = mdot_deep/Gamma_star = "
      f"{M_active:.2e} kg = {M_active/1.989e30:.2e} M_sun")
print(f"  -> the skin's full loop turnover: 1/Gamma_star = "
      f"{1/G_star/3.156e7/1e6:.1f} Myr")
print(f"  (the burn AND the consumption are one tempo - the phase loop's")
print(f"   two sides, both accelerated by the heat's return)")
print()
print("the acceptance speed, identified:")
P_accept = f_esc * mdot_deep * c0 ** 2
tau_choke = K_Q * DELTA_GAP * V_A / P_accept
print(f"  acceptance power at the corona = f_esc * mdot_deep * c0^2")
print(f"    = the baseline's expansion-pressure maintenance = {P_accept:.2e} W")
print(f"  tau_choke = E_fault / P_accept = {tau_choke:.2e} s = "
      f"{tau_choke/86400:.2f} days")
print(f"  (the waves are not deleted: they dilute adiabatically into the")
print(f"   expanding, pressure-stable baseline - the bath absorbs them)")
print()
res = {"K_Q": K_Q, "E_fault_J": K_Q * DELTA_GAP * V_A, "H_wall": H_wall,
       "rate_star_per_kg": rate_star, "ratio": H_wall / rate_star,
       "Gamma_star_untying": G_star, "M_active_skin_kg": M_active,
       "loop_turnover_Myr": 1.0 / G_star / 3.156e7,
       "P_accept_W": P_accept, "tau_choke_days": tau_choke / 86400.0}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "acceptance_identity.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("result written:", out)
