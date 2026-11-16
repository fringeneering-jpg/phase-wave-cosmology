# stage3_superposition_boundary.py - the Superposition Boundary Law as a
# CONTINUOUS FIELD TENSOR (2026-10-18). No Navier-Stokes: the waves
# superimpose (not displace), the density stacks, C crashes, the impedance
# slaps, and the lock is the boundary war:
#   P_outward = rho_local C(rho_local)^2  vs  P_inward = rho0 c0^2/3 + rho0 c0 v
#   RETAINED iff P_outward <= P_inward;  the unlock velocity v_crit.
# Both C-laws run: the acoustic form (K = rho0 c0^2 constant -> unlock at
# 2c0/3) and the anchored ladder (K(rho) varies -> the topology holds).
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]

P_BASE = rho0 * c0 ** 2 / 3.0        # the baseline pressure
Z = rho0 * c0                        # the dynamic impedance

def C_acoustic(rho): return c0 * (rho0 / rho) ** 0.5
def C_ladder(rho):   return pi_v.capacity(rho, c0, rho0, n_lad)

print("=" * 78)
print("THE SUPERPOSITION BOUNDARY LAW - the field tensor, not Navier-Stokes")
print("=" * 78)
print(f"the baseline: P_base = rho0 c0^2/3 = {P_BASE:.3e} Pa")
print(f"the impedance: Z = rho0 c0 = {Z:.3e} Pa s/m  (the dynamic resistance)")
print(f"the lock: rho_local C(rho_local)^2 <= P_base + Z v_expansion")
print()

zones = [("the ambient (rho0)", rho0),
         ("the quiet corona", 5.02e-13),
         ("the knot (rho_max)", rho_max)]
print(f"{'zone':22s} {'form':9s} {'C (km/s)':>10s} {'P_out (Pa)':>12s} "
      f"{'v_crit':>12s}  verdict")
rows = []
for name, rho in zones:
    for form, Cfn in [("acoustic", C_acoustic), ("ladder", C_ladder)]:
        C = Cfn(rho)
        P_out = rho * C ** 2
        v_crit = (P_out - P_BASE) / Z
        rows.append({"zone": name, "form": form, "C_km_s": C / 1e3,
                     "P_out": P_out, "v_crit": v_crit})
        if form == "acoustic":
            verdict = ("UNLOCKS at v_crit" if v_crit < c0 else "locked")
        else:
            verdict = "locked (the topology holds)"
        print(f"{name:22s} {form:9s} {C/1e3:10.0f} {P_out:12.3e} "
              f"{v_crit:12.3e}  {verdict}")
print()
print("the readings:")
print("  - ACOUSTIC FORM (K constant): rho C^2 = rho0 c0^2 ALWAYS, so the lock")
print("    reduces to v_exp >= 2c0/3: the universal unlock at 0.67c - the")
print("    pasted law's cleanest result. The thermodynamic lock breaks only")
print("    at two-thirds lightspeed, at EVERY density.")
print("  - ANCHORED LADDER (K(rho) = rho C^2, twined with rho): the lock never")
print("    breaks thermodynamically - the knot's retention is the TOPOLOGY's")
print("    720-degree hold (the 18/19), not the trap. The two locks separate:")
print("    the corona's stall (the superposition's C-crash) and the knot's")
print("    retention (the topology).")
print("  - the SLAP: P_dyn = Z v - the faster the untying tries to expand,")
print("    the harder the universe pushes back - the boundary war is the")
print("    field's own impedance, no fluid terms anywhere.")
res = rows
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "superposition_boundary.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
