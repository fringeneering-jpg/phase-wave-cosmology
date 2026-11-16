# stage3_photon_wind.py - the photon sail's scale vs the planets' absorption (2026-10-18)
# Jaden: "there IS a photon wind - a photon sail at certain sizes, right?
# That scale should match the photon absorption of the planets."
# The photon wind = the momentum of the untied waves: F_sail = (1+A) P_abs/c0.
# It scales EXACTLY as the absorption (both ~ pi R^2 / d^2). The scale-match
# is the beta ratio vs gravity: beta = F_sail/F_grav ~ (R^2/M) / ... - the
# surface-to-mass crossover. The planets sit ~1e-14 (gravity holds); the
# crossover (beta ~ 1) lands at the micron dust - the zodiacal dust and the
# comet tails, where the photon wind visibly blows.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
G = 6.67430e-11
M_SUN = 1.989e30

bodies = [
    # name, R (m), M (kg), d (AU), albedo
    ("Mercury", 2.440e6, 3.301e23, 0.387, 0.06),
    ("Earth",   6.371e6, 5.972e24, 1.000, 0.29),
    ("Jupiter", 6.991e7, 1.898e27, 5.203, 0.50),
]

print("=" * 78)
print("THE PHOTON WIND - the sail's push vs the planets' absorption")
print("=" * 78)
print(f"{'body':9s} {'P_abs W':>11s} {'F_sail N':>10s} {'F_grav N':>11s} {'beta':>10s}")
rows = []
for name, R, M, d, A in bodies:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    P_abs = (1 - A) * 3.14159265358979 * R ** 2 * flux
    F_sail = (1 + A) * P_abs / c0          # absorbed + reflected momentum
    F_grav = G * M_SUN * M / (d * AU) ** 2
    beta = F_sail / F_grav
    rows.append({"name": name, "P_abs": P_abs, "F_sail": F_sail,
                 "F_grav": F_grav, "beta": beta})
    print(f"{name:9s} {P_abs:11.3e} {F_sail:10.3e} {F_grav:11.3e} {beta:10.2e}")
print()
print("the scale-match: the sail's push IS the absorption's momentum twin -")
print("F_sail = (1+A) P_abs/c0 scales exactly as the absorption. The beta ratio")
print("against gravity is the surface-to-mass crossover:")
print()
print("the crossover (beta = 1) - the photon sail's size:")
for rho, label in [(2500.0, "rock dust"), (1000.0, "ice/comet dust")]:
    # beta = (1+A)(pi R^2 F)(1+...)/c0 / (G M_sun (4/3 pi R^3 rho)/d^2)
    #      = (1+A) 3 F d^2 / (4 c0 G M_sun rho R)
    flux = L_SUN / (4 * 3.14159265358979 * AU ** 2)
    A = 0.1
    R_crit = (1 + A) * 3 * flux * AU ** 2 / (4 * c0 * G * M_SUN * rho)
    print(f"  {label:18s}: R_crit = {R_crit*1e6:.2f} microns (beta=1 at 1 AU)")
print()
print("the reading: the planets sit at beta ~ 1e-14 - the photon wind is")
print("nothing to them, gravity holds by fourteen orders. The sail's scale is")
print("the MICRON dust - the zodiacal grains and the comet tails, where the")
print("photon wind visibly blows (the Poynting-Robertson spiral). The same")
print("absorption law, matched by the surface-to-mass ratio: big bodies ignore")
print("the wind, small bodies sail on it.")
res = {"planets": rows, "dust_crossover_microns": {
       "rock": R_crit * 1e6}}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "photon_wind.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
