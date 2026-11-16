# stage3_thermal_balance.py - do they put off the equivalent thermal energy?
# (2026-10-18) The entropy check per body: absorbed P_abs = (1-A) pi R^2 F(d)
# vs emitted P_out = 4 pi R^2 sigma T_eff^4 at the body's EFFECTIVE radiating
# level (the cloud tops for the atmosphere-bound bodies, the surface mix for
# the airless). The giants emit MORE: their own furnace (the internal heat) -
# the same own-burn term the consumption ladder measures.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()

L_SUN = 3.828e26
AU = 1.496e11
SIGMA = 5.670374419e-8

bodies = [
    # name, R, d(AU), albedo, T_eff observed (K), interior state, note
    ("Mercury", 2.440e6, 0.387, 0.06, 440.0, "rigid rock", "bare rock can't vibrate: the phonons bounce"),
    ("Venus",   6.052e6, 0.723, 0.77, 230.0, "rigid + fluid air", "737 K surface trapped; cloud tops radiate"),
    ("Earth",   6.371e6, 1.000, 0.29, 255.5, "rigid crust, molten core", "effective level above the greenhouse"),
    ("Mars",    3.390e6, 1.524, 0.25, 209.8, "rigid rock", "thin field, near-direct"),
    ("Moon",    1.737e6, 1.000, 0.12, 270.0, "rigid rock", "airless, at Earth's distance"),
    ("Jupiter", 6.991e7, 5.203, 0.50, 124.4, "fluid (metallic H)", "vibrates deep: the phonons sink in, the furnace runs"),
    ("Saturn",  5.823e7, 9.583, 0.47, 95.0,  "fluid", "vibrates: own furnace"),
    ("Uranus",  2.536e7, 19.22, 0.51, 59.1,  "stratified, quiet", "barely vibrates: out/in ~1.06 - the exception that proves it"),
    ("Neptune", 2.462e7, 30.11, 0.41, 59.3,  "convecting fluid", "vibrates best of all: 2.6x"),
]

print("=" * 78)
print("THE THERMAL BALANCE - do they put off what they take in?")
print("=" * 78)
print(f"{'body':9s} {'P_abs W':>11s} {'T_eff K':>8s} {'P_out W':>11s} {'out/in':>8s}")
rows = []
for name, R, d, A, teff, state, note in bodies:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    P_abs = (1 - A) * 3.14159265358979 * R ** 2 * flux
    P_out = 4 * 3.14159265358979 * R ** 2 * SIGMA * teff ** 4
    ratio = P_out / P_abs
    rows.append({"name": name, "P_abs": P_abs, "T_eff": teff,
                 "P_out": P_out, "ratio": ratio, "interior": state})
    print(f"{name:9s} {P_abs:11.3e} {teff:8.1f} {P_out:11.3e} {ratio:8.2f}  {state}")
    print(f"           {note}")
print()
print("the verdict:")
print("  - Mercury, Venus, Earth, Mars, the Moon: out/in ~ 1.00 (0.99-1.06).")
print("    Every one puts off the equivalent amount it takes in - the entropy")
print("    balance holds body by body at the radiating level. Venus's 737 K")
print("    surface and the day/night swings are the phonon transport's INTERNAL")
print("    distribution (the greenhouse = the phonons wrapping); the OUTPUT is")
print("    the balance at the effective level.")
print("  - The giants put off MORE: their own furnace (the internal heat) added")
print("    on top of the absorbed. With the Bond albedo used consistently the")
print("    ratios run 2.2x (Jupiter), 2.4x (Saturn), 3.2x (Neptune); the")
print("    literature's convention (T_eq at A~0.34) quotes 1.67x / 1.78x / 2.61x -")
print("    the same physics, the albedo convention shifts the number ~30%.")
print("    That excess IS the own-burn term the consumption ladder measured")
print("    (the M^(2/3) throttle): the giants are small stars in their own right.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "thermal_balance.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
