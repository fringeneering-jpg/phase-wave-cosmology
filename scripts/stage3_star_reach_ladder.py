# stage3_star_reach_ladder.py - the luminous reach across the stars (2026-10-18)
# Jaden: "if we match it to some of the furthest stars we can see, does the
# same thing hold?" The law: r_lum = sqrt(L / 4 pi c0 u_cmb) per star, and
# the wear = H_wall * (d/c0) over the line of sight. At the naked-eye
# horizon (~16,000 ly) the wear is ~1e-6 - the visibility is the PURE
# inverse square; the tired light only accumulates at cosmic scales.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
R_p = F["locked_constants"]["R_p"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
LY = 9.4607e15
A_RAD = 7.5657e-16
U_CMB = A_RAD * 2.7255 ** 4
H_wall = rho0 * c0 / (rho_max * R_p)

def r_lum(L):
    return (L / (4 * 3.14159265358979 * c0 * U_CMB)) ** 0.5

stars = [
    ("the Sun",       1.0,       0.0),
    ("Proxima Cen",   0.0017,    4.24),
    ("Sirius",        25.4,      8.6),
    ("Rigel",         1.2e5,     860.0),
    ("Deneb",         2.0e5,     2615.0),
    ("Betelgeuse",    1.26e5,    548.0),
    ("V762 Cas",      4.0e5,     16300.0),   # the furthest naked-eye candidate
]

print("=" * 78)
print("THE STAR REACH LADDER - the same law, every star")
print("=" * 78)
print(f"{'star':14s} {'L/L_sun':>9s} {'distance':>10s} {'r_lum':>12s} "
      f"{'wear along sight':>17s}")
rows = []
for name, L_ratio, d_ly in stars:
    rl = r_lum(L_ratio * L_SUN)
    wear = H_wall * (d_ly * LY / c0) if d_ly > 0 else 0.0
    rows.append({"name": name, "L_Lsun": L_ratio, "d_ly": d_ly,
                 "r_lum_AU": rl / AU, "r_lum_ly": rl / LY, "wear": wear})
    print(f"{name:14s} {L_ratio:9.2e} {d_ly:8.0f} ly {rl/AU:10,.0f} AU "
          f"{wear:16.2e}")
print()
print("the reading:")
print("  - every star's light dies into the bath at its own r_lum = sqrt(L):")
print("    Proxima ~430 AU, the Sun ~10,400 AU, Sirius ~0.8 ly, the bright")
print("    giants (Rigel/Deneb/Betelgeuse) ~55-75 ly.")
print("  - the furthest naked-eye stars (V762 Cas ~16,300 ly): the wear along")
print("    the sight line is ~1e-6 - NOTHING. The eye sees them by the pure")
print("    inverse square; the framework's tired light only accumulates at the")
print("    cosmic scale. So the same thing holds: the visibility law is the")
print("    1/d^2 to the eye's floor, and each star's luminous reach scales as")
print("    sqrt(L) - the bright giants' light walks ~100 ly before wearing")
print("    into the bath, the Sun's ~0.16 ly, Proxima's ~0.007 ly.")
res = rows
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "star_reach_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
