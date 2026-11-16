# Y(rho) power law from the two cavitation anchors + the path-(c) isothermal check
# Anchors: v_cav(rho0) = c0 (light threads the resting medium exactly at its limit),
#          v_cav(rho_max) = 954 km/s (RBH-1).  v_cav = sqrt(2Y/rho).
# Fit v(rho) = c0*(rho/rho0)^(-b) through the two points; then Y(rho) = 1/2 rho v^2.
import math

c0 = 2.998e8
rho0 = 8.74e-27
rho_max = 1.304e15
Y_max = 5.93e26          # RBH-1 anchor (DERIVATIONS row 15)
v_max = 954e3

# b from the two endpoints
b = math.log(c0/v_max)/math.log(rho_max/rho0)
print(f"passage-scale exponent b = ln(c0/954km/s)/ln(rho_max/rho0) = {b:.4f}")
print(f"v(rho) = c0*(rho/rho0)^(-{b:.4f})")
# check endpoints
print(f"  at rho0:   v = c0 = {c0:.3e} m/s")
print(f"  at rho_max: v = {c0*(rho_max/rho0)**(-b)/1e3:.0f} km/s (anchor 954)")

print("\nY(rho) = 1/2 * rho * c0^2 * (rho/rho0)^(-2b)")
print(f"  2b = {2*b:.4f}")
print(f"  Y(rho0)   = {0.5*rho0*c0**2:.3e} Pa  (the two-anchor constraint value)")
print(f"  Y(rho_max) = {0.5*rho_max*c0**2*(rho_max/rho0)**(-2*b):.3e} Pa vs anchor {Y_max:.3e}")
print(f"  Y/rho at rho0 = {0.5*c0**2:.3e} m^2/s^2; at rho_max = "
      f"{0.5*c0**2*(rho_max/rho0)**(-2*b):.3e}; ratio = "
      f"{(rho_max/rho0)**(2*b):.2e} (the 1e5 fall)")

print("\nThird-anchor probe: what density does the fastest pulsar (1,083 km/s) imply?")
vp = 1083e3
rho_p = rho0*(c0/vp)**(1/b)
print(f"  rho = rho0*(c0/1083km/s)^(1/b) = {rho_p:.3e} kg/m^3 = {rho_p/rho_max:.2f} rho_max")

print("\nPath-(c) check: isothermal branch rho_excess = c_s^2/(2 pi G r^2) at RBH-1's location")
G = 6.6743e-11
kpc = 3.0857e19
r62 = 62*kpc
rho_iso = (c0**2/3.0)/(2*math.pi*G*r62**2)
print(f"  at 62 kpc from the host: {rho_iso:.3e} kg/m^3 = {rho_iso/rho0:.2e} rho0")
M_swept_iso = rho_iso*math.pi*(0.7*kpc)**2*954e3*73e6*365.25*86400
print(f"  swept over 73 Myr through the 0.7 kpc trail: {M_swept_iso/1.989e30:.2e} Msun "
      f"(unphysical -> the isothermal branch as written cannot serve as path (c);")
print(f"  the local-medium profile is the open Domain-V item, not a number we can borrow)")
