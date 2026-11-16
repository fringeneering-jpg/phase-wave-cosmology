# friction_coefficient.py - the framework's own friction (2026-10-17)
# THE RELATION: when the friction coefficient surpasses max-P, you go luminal.
# The friction = the dynamic pressure's share of the medium's max: mu = rho.v^2
# / (the max's). The local cap C(rho) = sqrt(Y/rho) - the same wave-speed the
# relaxation runs at. So the friction's mu = (v / C(rho))^2: the object's speed
# against the AMBIENT's cap. Luminal = mu -> 1 = the speed hits the local cap.
# The mass enters through the CORE's density (the bigger the core, the slower
# the cap, the lower the luminal speed) and the shell's thickness (the
# interaction's length). The heat's the mu's fraction of the max's budget.
import numpy as np

# the framework's locked figures
rho_0 = 8.74e-27          # the ambient's rest density
rho_max = 1.304e15        # the proton's tied density
rho_core = 2.3e17         # the neutron's stacked core
Y_bow = 5.93e26           # the max-P's yield (Pa)
a_max = 3.23e11           # the holding yield acceleration (N/kg)
c0 = 2.9979e8

def C(rho):
    # the framework's capacity ladder: anchored at C(rho_0) = c0 (the locked's)
    # and C(rho_max) = 958 km/s (the RBH-1's 0.996 C_max). The two anchors give
    # C(rho) = c0 . (rho_0/rho)^n with n = ln(c0/958e3)/ln(rho_max/rho_0).
    n = np.log(c0 / 958e3) / np.log(rho_max / rho_0)
    return c0 * (rho_0 / rho) ** n

print("THE FRICTION COEFFICIENT - the framework's own relation:")
print("  mu = rho.v^2 / max-P  ->  mu = (v / C(rho))^2,  C anchored: c0 at rho_0,")
print(f"  958 km/s at rho_max  ->  C(rho) = c0.(rho_0/rho)^{np.log(c0/958e3)/np.log(rho_max/rho_0):.4f}")
print()
print("  the local caps (the luminal speeds) at each density:")
for tag, rho in [("the ambient (rho_0)", rho_0), ("the proton's core (rho_max)", rho_max),
                 ("the neutron's core (rho_core)", rho_core)]:
    c_local = C(rho)
    print(f"    {tag:26s}: C = {c_local/1e3:,.0f} km/s")
print()
# the observable heats: the friction's fraction of the max budget's the
# temperature's - the RBH-1's bow's 10^7 K at v = 954 km/s, the no-shock's 600.
print("  the friction mu = (v/C_ambient)^2 at the observed speeds:")
for v_km in [600.0, 954.0]:
    mu = (v_km * 1e3 / C(rho_0))**2
    print(f"    v = {v_km:5.0f} km/s:  mu = {mu:.3e}   (the ambient's cap is c0)")
print()
print("  the size/speed ratio (the framework's):")
print("    the luminal speed v_lum = C(rho_core): the black hole's core's dense ->")
print(f"    C(rho_core) = {C(rho_core)/1e3:,.0f} km/s (the relatively SLOW luminal)")
print("    the photon's massless (no core) -> the ambient's C = c0 (the FAST luminal)")
print("    the gamma's the slightly slowed wave (the framework's own) -> slightly below c")
print()
print("the honest state: the friction's the (v/C)^2's the rate-limit's own form;")
print("the luminal threshold's the local cap's; the mass/density/speed relation's")
print("the core's density ladder (the heavier, the slower the cap, the lower the")
print("luminal). The heats scale with mu - the 10^7 K bow's the near-luminal's")
print("receipt. The relaxation rate's the same C - the healing and the cap are one.")
