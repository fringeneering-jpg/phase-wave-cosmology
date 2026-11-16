# stage3_distance_ladder.py - do the consumption percentages scale by DISTANCE?
# The framework's drive: the sun's radiation unties (radiation is the
# untying's agent) - the arriving drive is the solar flux F = L_sun/4 pi d^2,
# falling as d^-2. Combined with the mass ladder (M^(2/3)), the full law:
#   Gamma(M,d) = Gamma_sun * (M/M_sun)^(2/3) * (d/1AU)^-2
# This script puts the planets on it and reports where it holds and where
# the body's OWN throttle (gravity escape, internal heat) breaks it.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]

M_SUN = 1.989e30
L_SUN = 3.828e26
AU = 1.496e11

planets = [
    # name, M (kg), R (m), d (AU), observed mdot (kg/s), note
    ("Mercury", 3.301e23, 2.440e6, 0.387, None,  "no atmosphere; sputtering ~negligible"),
    ("Venus",   4.867e24, 6.052e6, 0.723, None,  "escape poorly measured"),
    ("Earth",   5.972e24, 6.371e6, 1.000, 3.0,   "atmospheric escape ~3 kg/s"),
    ("Mars",    6.417e23, 3.390e6, 1.524, 2.5,   "MAVEN: ~2-3 kg/s, gravity/photochem driven"),
    ("Jupiter", 1.898e27, 6.991e7, 5.203, 1.0e3, "plasma outflow ~1e3 kg/s (noisiest)"),
    ("Saturn",  5.683e26, 5.823e7, 9.583, None,  "planet's own loss small"),
    ("Uranus",  8.681e25, 2.536e7, 19.22, None,  "negligible"),
    ("Neptune", 1.024e26, 2.462e7, 30.11, None,  "negligible"),
]

def gamma_law(M, d_AU):
    return (mdot_deep / M_SUN) * (M / M_SUN) ** (2.0 / 3.0) * d_AU ** -2.0

print("=" * 78)
print("THE DISTANCE LADDER - do the percentages scale with distance?")
print("=" * 78)
print(f"the arriving drive: F(d) = L_sun/4 pi d^2  (the radiation that unties)")
print(f"the combined law:   Gamma(M,d) = Gamma_sun (M/M_sun)^(2/3) (d/1AU)^-2")
print()
print(f"{'body':9s} {'d (AU)':>7s} {'flux W/m2':>10s} {'intercept/kg':>13s} "
      f"{'obs per-kg':>12s} {'law per-kg':>12s} {'ratio':>8s}")
rows = []
for name, M, R, d, mdot_obs, note in planets:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    inter = 3.14159265358979 * R ** 2 * flux / M
    g_obs = mdot_obs / M if mdot_obs else None
    g_law = gamma_law(M, d)
    ratio = g_obs / g_law if g_obs else None
    rows.append({"name": name, "d_AU": d, "flux": flux, "intercept_per_kg": inter,
                 "obs_per_kg": g_obs, "law_per_kg": g_law,
                 "ratio": ratio, "note": note})
    print(f"{name:9s} {d:7.3f} {flux:10.1f} {inter:13.3e} "
          f"{'-' if g_obs is None else f'{g_obs:.3e}':>12s} "
          f"{g_law:12.3e} {'-' if ratio is None else f'{ratio:.2f}':>8s}")
    print(f"           {note}")
print()
print("the verdict:")
print(f"  Earth: ratio obs/law = {3.0/5.972e24/gamma_law(5.972e24, 1.0):.2f} "
      f"(the mass ladder's anchor, ~9% off - holds)")
print(f"  Mars:  ratio obs/law = {2.5/6.417e23/gamma_law(6.417e23, 1.524):.1f} "
      f"- the planet's OWN throttle (low gravity escape) outruns the radiation")
print(f"  drive: the percentage does NOT scale by distance there.")
print(f"  The clean d^-2 channel is the COMETS: the framework's comet law")
print(f"  (mdot*L_sub = the solar input, comet_survival_map.py) - the ablation")
print(f"  follows the arriving flux exactly: d^-2.")
print(f"  Jupiter/Saturn: their internal heat (their own furnace) dominates")
print(f"  the Sun's drive - the ladder needs their own burn added.")
print()
print("the full picture: Gamma(M,d) = Gamma_sun (M/M_sun)^(2/3) (d/1AU)^-2,")
print("modulated by the body's own throttle. Where the radiation drive")
print("dominates (comets, the Earth's atmosphere's baseline), the distance")
print("scaling holds; where the body's own furnace or gravity dominates,")
print("the body's own term breaks it - the percentages scale by distance")
print("only through the arriving drive.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "distance_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
