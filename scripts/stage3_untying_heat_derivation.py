# stage3_untying_heat_derivation.py - heat unties, cold welds (2026-10-18)
# Jaden's ruling: HEAT is the untying - the opposite of the COLD WELD that
# solidified the knot. The subatomic cycle:
#   TYING (the cold weld): the wave wears out (the amplitude drops below
#     the luminous threshold), the heat is EXPULSED (the tying's exotherm,
#     c0^2/kg leaves), and the wave freezes into the knot - the cold weld.
#   UNTYING (the heat): the heat RETURNS (the environment's heat absorbed -
#     the star's interior, the friction), e_avail climbs, crosses E_lock,
#     and the weld thaws: the knot blooms back into the wave.
# The onset law: the grip/untying switches at e_avail = E_lock (phi = 1/2,
# the tanh's inflection) - the heat's absorption is the driver both ways.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]

M_E = 9.1093837e-31
M_P = 1.6726219e-27
M_N = 1.6749275e-27
Q_KG = c0 ** 2                        # J/kg  the heat per kg, both directions
E_LOCK_RATIO = 18.0 / 19.0            # the 18-part debt of the 19:1:18 fold

print("=" * 78)
print("HEAT UNTIES, COLD WELDS - the subatomic cycle")
print("=" * 78)
print(f"the heat per kg: c0^2 = {Q_KG:.3e} J/kg - the SAME number, both ways:")
print(f"  the tying EXPELS it (the cold weld: the heat leaves, the wave")
print(f"  freezes into the knot at the cold state)")
print(f"  the untying ABSORBS it (the heat returns, the weld thaws, the")
print(f"  knot blooms back into the wave)")
print()
print(f"{'knot':10s} {'mass (kg)':>12s} {'the weld\'s heat':>16s} "
      f"{'the thaw\'s draw':>16s} {'T at that heat':>14s}")
rows = []
KB = 1.3806e-23
for name, m in (("electron", M_E), ("proton", M_P), ("neutron", M_N)):
    q_weld = m * Q_KG                    # the tying's exotherm
    q_thaw = E_LOCK_RATIO * m * Q_KG     # the untying's endotherm (18/19)
    T_thaw = q_thaw / KB                 # the heat's own temperature
    rows.append({"knot": name, "mass": m, "weld_heat_J": q_weld,
                 "thaw_heat_J": q_thaw, "T_K": T_thaw})
    print(f"{name:10s} {m:12.2e} {q_weld:16.3e} {q_thaw:16.3e} {T_thaw:14.2e}")
print()
print("the onset law (the grip switches at the thaw):")
print(f"  e_avail(t) = e_avail0 + Q_heat(t) - the heat's return raises the")
print(f"  available energy; at e_avail = E_lock (phi = 1/2) the weld thaws:")
print(f"  the grip switches ON, the bloom begins. Before: cold, tied, solid.")
print(f"  The tying is the reverse: the heat's expulsion drops e_avail below")
print(f"  E_lock - delta_E, the wave freezes - the cold weld solidifies it.")
print()
print("the circle (the phase loop with the heat as the driver):")
print(f"  the star's interior heat (15 MK) IS the thaw: the knots inside the")
print(f"  star absorb it, the welds release, the deep channel runs. The cold")
print(f"  bath (2.7255 K) IS the weld: the worn-out waves give up their heat")
print(f"  and freeze back into knots. Heat unties, cold welds - one circle,")
print(f"  no independent forces.")
res = rows
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "untying_heat_derivation.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
