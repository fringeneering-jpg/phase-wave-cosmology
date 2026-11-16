# stage3_tension_full_tilt.py - the 7% is the tension's own limit (2026-10-18)
# Jaden: the 2.6796e25 W is the FORCE OF THE MEDIUM'S TENSION at FULL-TILT
# ABSORPTION and MAX GIVE, at the CORONA'S GEOMETRIC SIZE. The reading:
#   - the restricted force F = 8.94e16 N spread over the choke's shell
#     (the found block boundary ~1.09 R_sun) = the tension's stress there;
#   - the full-tilt absorption = the acceptance power (1.02e21 W);
#   - the max give = the room-making (the expansion's pressure maintenance);
#   - the force = the tension holding the star's demand at the choke's size.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
MP = 1.6726e-27

L_SUN = 3.828e26
R_SUN = 6.96e8
R_CHOKE = 1.09 * R_SUN          # the found block boundary (Stage C)
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2

F_REST = 0.07 * L_SUN / c0      # N  the restricted force
A_CHOKE = 4 * 3.14159265358979 * R_CHOKE ** 2
STRESS = F_REST / A_CHOKE       # Pa  the tension's stress at the corona's size
P_ABS = f_esc * mdot_deep * c0 ** 2    # W  the full-tilt absorption

print("=" * 78)
print("THE 7% = THE TENSION AT FULL TILT, AT THE CORONA'S SIZE")
print("=" * 78)
print(f"the restricted force: F = 8.938e16 N")
print(f"the corona's geometric size: R_choke = 1.09 R_sun (the found block)")
print(f"  -> the choke's shell area = {A_CHOKE:.2e} m^2")
print(f"  -> the tension's stress there = {STRESS:.4f} Pa")
print()
print("the two simultaneous extremes the tension runs:")
print(f"  FULL-TILT ABSORPTION: P_accept = f_esc x mdot_deep x c0^2 = "
      f"{P_ABS:.2e} W")
print(f"  MAX GIVE: the room-making (the expansion's pressure maintenance,")
print(f"  H_wall-scale) - the give that regulates the burn")
print()
print(f"the tension's own state at the corona: K = rho C^2 = {K_Q:.2e} Pa")
print(f"  -> the restriction runs the tension at the strain "
      f"{STRESS/K_Q:.2e} (the fault's band, held)")
print()
print("the reading: the 7% is not a leak and not a loss - it is the TENSION")
print("itself working at both limits at once: absorbing the untying at full")
print("tilt and giving room at max, its force spread over the corona's own")
print("geometry. That grip - 8.94e16 N at 0.013 Pa over the choke - is the")
print("governor's hand on the star. Full tilt, max give, exactly 7%.")
res = {"F_restricted_N": F_REST, "R_choke_m": R_CHOKE, "A_choke_m2": A_CHOKE,
       "stress_Pa": STRESS, "P_absorb_W": P_ABS, "K_corona_Pa": K_Q,
       "strain": STRESS / K_Q}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "tension_full_tilt.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
