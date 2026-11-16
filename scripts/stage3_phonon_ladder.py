# stage3_phonon_ladder.py - the hot/cold differential test (2026-10-18)
# The phonon expands what it meets and absorbs into thawing knots; its range
# = the stiffness of the tension and the localized pressure (c_s =
# sqrt(gamma P / rho)). The test: the day/night differentials of a string
# of planets vs distance - the day side carries the drive (d^-1/2), the
# differential carries the phonon's travel (the wrap-around W).
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()

# name, d (AU), R (m), rotation (s), gamma, P_surf (Pa), rho_surf (kg/m^3),
# observed day T (K), observed night T (K), note
bodies = [
    ("Mercury", 0.387, 2.440e6, 58.6*86400.0, None, 0.0,    0.0,   700.0, 100.0,
     "no atmosphere: the phonons stop at the regolith"),
    ("Venus",   0.723, 6.052e6, 243.0*86400.0, 1.3, 9.2e6,  65.0,  737.0, 737.0,
     "92 bar CO2: the phonons wrap the night completely"),
    ("Earth",   1.000, 6.371e6, 86400.0,      1.4, 1.013e5, 1.225, 288.0, 278.0,
     "1 bar: partial wrap-around"),
    ("Mars",    1.524, 3.390e6, 88642.0,      1.3, 636.0,   0.02,  293.0, 183.0,
     "6 mbar: the phonons barely travel"),
    ("Moon",    1.000, 1.737e6, 27.3*86400.0, None, 0.0,    0.0,   390.0, 110.0,
     "no atmosphere: full differential at Earth's distance"),
]

print("=" * 78)
print("THE PHONON LADDER - how far they travel, how much they affect")
print("=" * 78)
print(f"{'body':9s} {'d AU':>6s} {'T_day':>7s} {'T_night':>8s} {'swing':>7s} "
      f"{'c_s m/s':>8s} {'travel m':>10s} {'W_eff':>9s}  effect")
rows = []
for name, d, R, prot, gam, Ps, rhos, tday, tnight, note in bodies:
    swing = tday - tnight
    if gam:
        c_s = (gam * Ps / rhos) ** 0.5
        travel = c_s * prot
        W = travel / (2 * 3.14159265358979 * R)
        W_eff = W * (Ps / 1.013e5)      # the pressure = the heat capacity
    else:
        c_s, travel, W, W_eff = 0.0, 0.0, 0.0, 0.0
    rows.append({"name": name, "d_AU": d, "T_day": tday, "T_night": tnight,
                 "swing": swing, "c_s": c_s, "travel": travel, "W_eff": W_eff})
    effect = ("total wrap - no differential" if swing < 5 else
              "partial wrap-around" if swing < 50 else
              "phonons stop at the surface")
    print(f"{name:9s} {d:6.3f} {tday:7.0f} {tnight:8.0f} {swing:7.0f} "
          f"{c_s:8.0f} {travel:10.3e} {W_eff:9.3f}  {effect}")
    print(f"           {note}")
print()
print("the reading:")
print("  - the DAY side carries the distance: Mercury (0.39 AU) bakes at 700 K,")
print("    the Moon (1.00 AU) at 390 K - the drive falls with distance.")
print("  - the DIFFERENTIAL carries the phonon's travel: Venus's 92-bar field")
print("    wraps the night completely (swing ~0); Mercury's bare regolith and")
print("    the Moon stop the phonons at the surface (swings 600 K / 280 K);")
print("    Earth's 1-bar field wraps partially (~10 K); Mars's 6-mbar field")
print("    barely travels (~110 K swing despite the faster rotation).")
print("  - the range IS the stiffness and the pressure: c_s = sqrt(gamma P/rho),")
print("    and the pressure carries the heat capacity - W_eff = (c_s * P_rot /")
print("    2 pi R) * (P/1 bar): Venus ~20,000, Earth ~0.7, Mars ~0.005.")
print("  - so the phonons travel as far as the body's own field lets them, and")
print("    their effect (the swing) is that travel, exactly as designed.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "phonon_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
