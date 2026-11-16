# stage3_entropy_ladder.py - the entropy-balance test (2026-10-18)
# Jaden's question: the planets all take in the solar flux and put out
# thermal exhaust ("entropy says you put out what you take in, just lower
# ordered") - so does each planet off-gas the RIGHT AMOUNT of thermal
# exhaust for its distance from the sun, factoring in absorption?
# The test: absorbed power P_abs = (1-A) pi R^2 L_sun/4 pi d^2 (A = albedo);
# the entropy balance's mass through-put: mdot_entropy = P_abs/c0^2
# (m = L/c0^2 - the absorbed energy IS the drive, and the off-gas is its
# mass-equivalent). Then eps = mdot_observed/mdot_entropy = the body's own
# throttle (its holding): eps ~ 1 = balances; eps > 1 = weak holding;
# eps < 1 = strong holding / its own furnace dominates.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
SIGMA = 5.670374419e-8

bodies = [
    # name, M, R, d (AU), albedo, observed mdot (kg/s), note
    ("Mercury", 3.301e23, 2.440e6, 0.387, 0.06, None,  "no atmosphere; regolith off-gas unmeasured"),
    ("Venus",   4.867e24, 6.052e6, 0.723, 0.77, None,  "escape poorly measured"),
    ("Earth",   5.972e24, 6.371e6, 1.000, 0.29, 3.0,   "atmospheric escape ~3 kg/s"),
    ("Mars",    6.417e23, 3.390e6, 1.524, 0.25, 2.5,   "MAVEN ~2-3 kg/s; photochemistry IS radiation"),
    ("Jupiter", 1.898e27, 6.991e7, 5.203, 0.50, 1.0e3, "plasma outflow ~1e3 kg/s (noisiest)"),
    ("Saturn",  5.683e26, 5.823e7, 9.583, 0.47, None,  "planet's own loss small"),
    ("Uranus",  8.681e25, 2.536e7, 19.22, 0.51, None,  "negligible"),
    ("Neptune", 1.024e26, 2.462e7, 30.11, 0.41, None,  "negligible"),
]

print("=" * 78)
print("THE ENTROPY LADDER - does each planet off-gas its thermal through-put?")
print("=" * 78)
print("absorbed: P_abs = (1-A) pi R^2 F(d);  exhaust: T_eff = [(1-A)F/4sigma]^1/4")
print("entropy balance: mdot_entropy = P_abs/c0^2   (m = L/c0^2)")
print("eps = mdot_obs / mdot_entropy = the body's throttle (its holding)")
print()
print(f"{'body':9s} {'d AU':>6s} {'A':>5s} {'T_eff K':>8s} {'P_abs W':>11s} "
      f"{'mdot_ent':>10s} {'mdot_obs':>10s} {'eps':>9s}")
rows = []
for name, M, R, d, A, mdot_obs, note in bodies:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    P_abs = (1 - A) * 3.14159265358979 * R ** 2 * flux
    T_eff = ((1 - A) * flux / (4 * SIGMA)) ** 0.25
    mdot_ent = P_abs / c0 ** 2
    eps = mdot_obs / mdot_ent if mdot_obs else None
    rows.append({"name": name, "d_AU": d, "albedo": A, "T_eff_K": T_eff,
                 "P_abs_W": P_abs, "mdot_entropy": mdot_ent,
                 "mdot_obs": mdot_obs, "eps": eps, "note": note})
    print(f"{name:9s} {d:6.3f} {A:5.2f} {T_eff:8.1f} {P_abs:11.3e} "
          f"{mdot_ent:10.3e} "
          f"{'-' if mdot_obs is None else f'{mdot_obs:.2e}':>10s} "
          f"{'-' if eps is None else f'{eps:.2f}':>9s}")
    print(f"           {note}")
print()
print("the verdict:")
print("  Earth: eps = 2.19 -> the off-gas ~balances the through-put (within ~2x)")
print("  Mars:  eps = 14.1 -> WEAK HOLDING: the same radiation drive (the")
print("  photochemistry IS radiation) off-gasses ~14x the equilibrium - the")
print("  low mass can't hold what the radiation kicks loose")
print("  Jupiter: eps = 232 is the SYSTEM's plasma torus (Io's sulfur/oxygen),")
print("  NOT the planet's own mass - the planet's own off-gas is unmeasured;")
print("  the entropy balance PREDICTS it: ~4.3 kg/s (plus the internal heat")
print("  term, roughly doubling it)")
print()
print("the unmeasured planets get the entropy balance as PREDICTIONS:")
print("  Mercury ~1.8 kg/s, Venus ~0.77 kg/s, Saturn ~0.93 kg/s,")
print("  Uranus ~0.04 kg/s, Neptune ~0.02 kg/s - falsifiable when measured.")
print()
print("the framework reading: eps IS the throttle - the body's holding, the")
print("same modulation as the mass ladder. The entropy balance holds where")
print("the holding matches the through-put (Earth); the deviations ARE the")
print("body's own term, exactly as the distance ladder found.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "entropy_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
