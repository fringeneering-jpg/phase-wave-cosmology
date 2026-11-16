# stage3_restricted_force.py - the 7% is a FORCE, not a mass stream (2026-10-18)
# Jaden's scale-check: the photon at the EM-wave scale weighs ~50 fg per
# km^3 at 1 AU - the mass is nothing. So the 7% must live in the FORCE:
#   F_rest = P_rest / c0 = 2.6796e25 / 3e8 = 8.93e16 N
#   at the photosphere: 0.0147 Pa = 7% of the radiation pressure (0.21 Pa)
#   at 1 AU: 0.32 microPa = 7% of the sail's 4.5 microPa
# The force is huge while the mass is tiny because the momentum is m*c0:
# femtograms at c0 become the pressure. The choke holds 7% of the push.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
R_SUN = 6.96e8

P_REST = 0.07 * L_SUN                     # Jaden's 7%
F_REST = P_REST / c0                      # the restricted FORCE
A_PHOTO = 4 * 3.14159265358979 * R_SUN ** 2
P_PHOTO = (L_SUN / A_PHOTO) / c0          # the photospheric radiation pressure
P_REST_PHOTO = F_REST / A_PHOTO           # the restricted pressure at the surface

F_1AU = L_SUN / (4 * 3.14159265358979 * AU ** 2) / c0   # the sail's 4.5 uPa
m_km3_1AU = (L_SUN / (4 * 3.14159265358979 * AU ** 2)) / c0 ** 3 * 1e9

print("=" * 78)
print("THE 7% IS A FORCE - the mass is nothing, the push is not")
print("=" * 78)
print(f"the photon's mass per km^3 at 1 AU: {m_km3_1AU:.1e} kg = "
      f"{m_km3_1AU*1e15:.0f} femtograms - the scale-check: NOTHING.")
print(f"the restricted share: 7% of L = {P_REST:.4e} W")
print(f"-> THE RESTRICTED FORCE: F_rest = P_rest/c0 = {F_REST:.3e} N")
print()
print(f"at the photosphere: the radiation pressure = {P_PHOTO:.3f} Pa")
print(f"  the restricted 7% = {P_REST_PHOTO:.4f} Pa = "
      f"{P_REST_PHOTO/P_PHOTO*100:.1f}% of the push")
print(f"at 1 AU: the sail feels {F_1AU*1e6:.1f} microPa; the restricted 7% = "
      f"{0.07*F_1AU*1e6:.2f} microPa")
print()
print("the reading: the photon's mass is 50 femtograms per cubic km, but the")
print("FORCE it represents is the pressure - and 7% of that force is 8.93e16 N")
print("held back by the choke. The mass is nothing and the force is everything")
print("because the momentum is m*c0: femtograms at max-P become the push. The")
print("choke doesn't hold back mass - it holds back 7% of the PUSH, and the")
print("refused push is the untying knots' volumetric growth, amplified by the")
print("heat, compounding.")
res = {"m_km3_fg": m_km3_1AU * 1e15, "F_restricted_N": F_REST,
       "P_photosphere_Pa": P_PHOTO, "P_restricted_photosphere_Pa": P_REST_PHOTO,
       "sail_1AU_uPa": F_1AU * 1e6, "restricted_1AU_uPa": 0.07 * F_1AU * 1e6}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "restricted_force.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
