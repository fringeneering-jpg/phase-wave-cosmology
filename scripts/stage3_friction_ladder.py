# stage3_friction_ladder.py - the photon meets the lowered C (2026-10-18)
# The photon rides c0 = max-P; the body's field RAISES the local density and
# LOWERS C(rho); the photon now exceeds the local cap and sheds through the
# friction law mu = (v/C)^2 (friction_coefficient.py). The deeper the density,
# the lower C, the higher the friction, the faster the luminous energy sheds.
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]

# (name, density kg/m^3, note)
zones = [
    ("the corona",           1.0e-12, "near-vacuum: low friction, the light escapes"),
    ("Mars air",             0.02,    "thin CO2 field"),
    ("Earth air",            1.2,     "1-bar field"),
    ("Jupiter clouds",       0.2,     "the gas giant's upper field"),
    ("Jupiter deep",         1000.0,  "the metallic-hydrogen field"),
    ("the photosphere",      2.0e-4,  "the star's own boundary field"),
    ("rho_max (the ceiling)", 1.304e15, "the absolute cap: C = 958 km/s"),
]

print("=" * 78)
print("THE FRICTION LADDER - the photon at max-P vs the lowered C")
print("=" * 78)
print(f"{'zone':22s} {'rho':>12s} {'C (km/s)':>10s} {'v/C':>8s} {'mu=(v/C)^2':>12s}")
rows = []
for name, rho, note in zones:
    C = pi_v.capacity(rho, c0, rho0, n_lad)
    vc = c0 / C
    mu = vc ** 2
    rows.append({"zone": name, "rho": rho, "C_km_s": C / 1e3, "v_over_C": vc,
                 "mu": mu})
    print(f"{name:22s} {rho:12.3e} {C/1e3:10.0f} {vc:8.1f} {mu:12.0f}")
    print(f"{'':22s}  {note}")
print()
print("the reading:")
print("  - a FLUID would block its locale outright; a FIELD does not - the")
print("    knots are ~99.99% empty and the medium threads through.")
print("  - but the field's pressure/density LOWERS C, and the photon at c0 now")
print("    exceeds the local cap: the friction mu = (v/C)^2 sheds the luminous")
print("    energy as heat, progressively with depth.")
print("  - the corona sheds at mu ~ 50 (the light escapes); the gas giant's")
print("    deep field sheds at mu ~ 3200 (the photon's energy becomes the")
print("    interior's heat - the own furnace's fuel).")
print("  - each band sheds at its own mu: the UV is absorbed high, the IR")
print("    penetrates deeper - the band ladder's physics, now as friction.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "friction_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
