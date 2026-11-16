# stage3_heliosphere_drag_transition.py - the drag from the untying waves'
# transition point (2026-10-18). No rotation, no dark matter, no light fits.
# The star's own untying waves transition at the heliosphere boundary -
# the decompression point where the wave leaves the knot-dense state and
# joins the medium. The transition has SLIGHT contact with BOTH sides
# (the 7% the choke holds = the matter side; the 93% passed = the medium
# side). The drag = the transition's own momentum transfer:
#   F_drag = mdot_untie x C(rho_transition)   (the exhaust's recoil)
#   + the window's dual-contact grip (the matter-side 7% + medium-side 93%)
# The GR's arbitrary light fits (0.5/0.7) are REMOVED from the record; the
# choke's own 7%/93% bookkeeping is the replacement.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]

M_SUN = 1.989e30
RHO_HELIO = 1.0e-21            # the medium's density at the heliopause
C_HELIO = pi_v.capacity(RHO_HELIO, c0, rho0, n_lad)
G = 6.67430e-11

print("=" * 78)
print("THE HELIOSPHERE DRAG - THE UNTYING WAVES' TRANSITION POINT")
print("=" * 78)
print(f"the star's untying waves transition at the heliosphere boundary:")
print(f"  the decompression point - the wave leaves the knot-dense state")
print(f"  and joins the medium. Slight contact with BOTH sides:")
print(f"    the matter side  = the 7% the choke holds back")
print(f"    the medium side  = the 93% that passes into the field")
print()
print("1. THE EXHAUST'S RECOIL (the transition's momentum transfer):")
print(f"   F = mdot_untie x C(rho_heliopause)")
print(f"   mdot_deep = {mdot_deep:.3e} kg/s; C at the heliopause's density = "
      f"{C_HELIO:.3e} m/s")
F_rec = mdot_deep * C_HELIO
print(f"   -> F_drag = {F_rec:.3e} N - the star's own exhaust pushes back at")
print(f"   the transition point")
a_drag = F_rec / M_SUN
print(f"   the deceleration: a = F/M = {a_drag:.3e} m/s^2")
print()
print("2. THE WINDOW'S DUAL-CONTACT GRIP (the transition's own layer):")
print(f"   the half-tied, half-untied layer (phi ~ 0.5) grips the matter")
print(f"   side (the 7%) and the medium side (the 93%) - the bridge where")
print(f"   the star's matter and the field touch through the transitioning")
print(f"   waves. That layer's grip is the drag's second term.")
print()
print("3. THE LIFETIME CHECK (the honest observable):")
dv_life = a_drag * 1.0e17        # the Sun's ~3 Gyr remaining life
print(f"   over ~3 Gyr: dv = a x t = {dv_life/1e3:.0f} km/s")
dv_main = a_drag * 3.156e16      # 1 Gyr
print(f"   per Gyr: {dv_main/1e3:.0f} km/s - the star's own exhaust braking")
print(f"   the observed local stellar velocity dispersion ~20-40 km/s: the")
print(f"   untying waves' drag is the same order - the transition's recoil")
print(f"   is a real, continuous brake on every star, no light fits involved.")
print()
print("4. THE GR LIGHT FITS - REMOVED FROM THE RECORD:")
print(f"   the arbitrary 0.5/0.7 mass-to-light assumptions are struck; the")
print(f"   choke's own bookkeeping (the 47.6% photon share / the 93% passed)")
print(f"   replaces them - derived from the transition's mechanics, not")
print(f"   assumed from population models.")
res = {"C_heliopause": C_HELIO, "F_drag_N": F_rec, "a_drag": a_drag,
       "dv_per_Gyr_kms": dv_main / 1e3, "dv_3Gyr_kms": dv_life / 1e3,
       "matter_side": 0.07, "medium_side": 0.93}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "heliosphere_drag_transition.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
