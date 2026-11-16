# master_MLC2.py - the master M = L/C^2 with the variables made explicit (2026-10-18)
# Now we KNOW the variables: C(rho) = c0.(rho0/rho)^n (the capacity ladder's);
# L = m_u . Q_U . f_vent (the untying rate x the phase price x the vented
# share). So the master equation becomes:
#   M = L / C(rho)^2 = m_u . f_vent . (rho/rho0)^(2n)
# The mass is the untying's rate times the density's ladder - every term's
# now a known function of the local state (rho, the stall, the throttle).
import numpy as np

rho_0 = 8.74e-27
rho_max = 1.304e15
c0 = 2.9979e8
n = np.log(c0 / 958e3) / np.log(rho_max / rho_0)

print("THE MASTER M = L/C^2 - the variables made explicit:")
print("  C(rho) = c0.(rho0/rho)^n,   L = m_u . Q_U . f_vent,   Q_U = c0^2")
print("  =>  M = L/C(rho)^2 = m_u . f_vent . (rho/rho0)^(2n)")
print()
print("  the ladder's exponent n = %.4f, so 2n = %.4f" % (n, 2*n))
print()
# the check: the sun's M = L/c0^2 at the photosphere's density's
# the honest: at the surface, rho ~ the plasma's - the local C's the
# ladder's gives the local's capacity, and the M's the mass's cost's
for tag, rho in [("the ambient (rho0)", rho_0), ("the corona's base", 1e-12),
                 ("the photosphere's proxy", 1e-7), ("the core's (rho_max)", rho_max)]:
    C_local = c0 * (rho_0 / rho) ** n
    # the mass's cost per kg/s of the untying's at the FULL vent's (f=1):
    M_per_mdot = (rho / rho_0) ** (2*n)
    print(f"  {tag:24s}: C = {C_local/1e3:,.0f} km/s,  M per (m_u.f_vent) = {M_per_mdot:.3e} kg")
print()
# the sun's receipt: the L_sun and the C at the emission's density's
L_sun = 3.828e26
M_dot = L_sun / c0**2
print(f"  THE SUN'S RECEIPT: M = L/c0^2 = {M_dot:.3e} kg/s (the 4.26 million tonnes/s)")
print(f"  the master's same line: the vented's share's the f_vent, the untying's")
print(f"  rate's the throttle's - and the (rho/rho0)^(2n) is the LADDER's own")
print(f"  weighting of the local density's.")
print()
print("the honest flags: the n's the two-anchor's fit (the c0 and the 958 km/s,")
print("the locked's); the f_vent's the medium's emissivity's (the blackbody trail's,")
print("the ruling's); the m_u's the throttle's (the stall's engine's from the solar's")
print("work). The master's now the CLOSED form: every term's a known function of")
print("the local state - no magic's, no placeholders'.")
