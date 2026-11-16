# tight_friction.py - the volumetric friction for the neutron core and the
# max-P shell (2026-10-17)
# The tight coefficient: mu = (rho . v^2 . V_shell) / (Y_bow . A_shell . L)
# - the dynamic pressure over the yield, weighted by the shell's volume-to-
# surface ratio (the geometry's). The neutron's core and the max-P shell,
# at the differential speeds; the relaxation rate's the LATER factor.
import numpy as np

rho_core = 2.3e17          # the neutron's stacked core (kg/m^3)
rho_max = 1.304e15         # the max-P shell's tied density
Y_bow = 5.93e26            # the max-P yield (Pa)
R_n = 1.1e-15              # the neutron's core radius (m)
dR_shell = 0.15e-15        # the shell's thickness (the skin's, the stated)
L = 2.0 * R_n              # the interaction length (the core's diameter)

def mu(rho, R, dR, v):
    # the volumetric friction: the dynamic pressure over the yield, with the
    # shell's volume/surface weighting (the geometry's)
    V = 4.0/3.0 * np.pi * ((R + dR)**3 - R**3)
    A = 4.0 * np.pi * (R + dR)**2
    return (rho * v**2 * V) / (Y_bow * A * L)

print("THE TIGHT FRICTION COEFFICIENT:")
print("  mu = rho . v^2 . V_shell / (Y_bow . A_shell . L)")
print()
print("  the neutron core and the max-P shell at the differential speeds:")
for tag, rho, R, dR in [("the neutron core", rho_core, R_n, dR_shell),
                         ("the max-P shell", rho_max, R_n, dR_shell)]:
    print(f"  {tag} (rho = {rho:.2e}, R = {R:.1e} m):")
    for v_km in [600.0, 954.0]:
        m = mu(rho, R, dR, v_km * 1e3)
        print(f"      v = {v_km:5.0f} km/s ->  mu = {m:.3e}")
print()
print("  the differential: the SAME geometry, the speeds' square's the warmth's:")
for tag, rho, R, dR in [("the neutron core", rho_core, R_n, dR_shell),
                         ("the max-P shell", rho_max, R_n, dR_shell)]:
    ratio = mu(rho, R, dR, 954e3) / mu(rho, R, dR, 600e3)
    print(f"      {tag}: mu(954)/mu(600) = {ratio:.3f}  (the v^2's)")
print()
print("the honest flags: the shell's thickness dR and the interaction length L")
print("are the STATED inputs (the framework's skin's values); the relaxation's")
print("the NEXT factor (the tau_relax/tau_passage's the healing's) - not in this")
print("coefficient yet. The geometry's the volumetric's; the numbers are the")
print("framework's own densities and the locked yield.")
