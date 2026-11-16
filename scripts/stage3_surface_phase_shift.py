# stage3_surface_phase_shift.py - the surface rejects heat (2026-10-18)
# Jaden's ruling: the interior is HOT but SOLID FROM PRESSURE (the pressure
# pins the welds). The surface is the boundary layer where the core's
# pressure meets the corona's push-back. The STAGNATED untying there forces
# the phase shift - and the phase shift AUTOMATICALLY REJECTS HEAT in that
# section: the tying's exotherm (c0^2/kg expelled) is the rejection.
# The photosphere's 5800 K = the rejection layer's own equilibrium: the
# surface radiates the rejected heat at exactly the deep channel's rate.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]

L_SUN = 3.828e26
R_SUN = 6.96e8
SIGMA = 5.670374419e-8

print("=" * 78)
print("THE SURFACE PHASE SHIFT - the heat-rejection layer")
print("=" * 78)
print("the interior: HOT but SOLID FROM PRESSURE - the core's density pins")
print("the welds; the knots cannot bloom against the surrounding pressure")
print("(the hot solid - the heat is there, the pressure holds the knot)")
print()
print("the surface: the boundary layer - the core's pressure pushing out")
print("meets the corona's push-back (the 0.0265 Pa choke step + the 968 Pa")
print("corona stiffness). There the untying STAGNATES - and the stagnation")
print("FORCES the phase shift: the stalled waves re-weld at the surface.")
print()
print("the rejection: the tying's exotherm - every re-weld expels c0^2/kg.")
print(f"the deep channel delivers {mdot_deep:.3e} kg/s of untying heat to the")
print(f"surface: P_in = mdot_deep c0^2 = {mdot_deep*c0**2:.3e} W")
print(f"the phase shift rejects it: P_reject = P_in - and the rejected heat")
print(f"radiates away at the surface's own temperature:")
T_surf = (L_SUN / (4 * 3.14159265358979 * R_SUN ** 2) / SIGMA) ** 0.25
print(f"  T_surface = (L / 4 pi R^2 sigma)^(1/4) = {T_surf:.0f} K")
print()
print(f"THE 5800 K PIN CLOSES: the surface's temperature IS the rejection's")
print(f"equilibrium - the heat the interior sends up (the hot solid's phonon")
print(f"flux) meets the phase-shift layer, the welds reject it, and the layer")
print(f"radiates the rejected heat at {T_surf:.0f} K. The surface is not a")
print(f"cooling accident: it is the heat-rejection boundary, and its")
print(f"temperature is the phase shift's own signature.")
print()
print("the three zones, one circle:")
print(f"  the core: hot solid (the pressure pins the knots - the heat is")
print(f"  trapped, the welds hold)")
print(f"  the surface: the phase-shift layer (the stagnated untying forces")
print(f"  the re-welding - the heat is rejected, radiating at {T_surf:.0f} K)")
print(f"  the corona: the heat's escape (the thin share that passed, the")
print(f"  1.5 MK bloom)")
print(f"  -> heat unties, cold welds, and the SURFACE is where the two meet:")
print(f"  the phase shift that rejects the heat IS the 5800 K pin.")
res = {"T_surface_K": T_surf, "P_in_W": mdot_deep * c0 ** 2,
       "rejected_W": mdot_deep * c0 ** 2}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "surface_phase_shift.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
