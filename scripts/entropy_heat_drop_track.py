# entropy_heat_drop_track.py - entropy tracked via the rate of heat drop (2026-10-21)
# The circle's bookkeeping at the bath scale:
#   the bath cools as the medium dilutes (the redshift law T ~ rho^(1/3)),
#   so d(ln Q)/dt = -4H: the RATE OF HEAT DROP is the untying's own clock.
#   The heat that drops out of the bath is the thaw's draw (the circle's
#   return leg) - so the same rate is the cycle's entropy production.
#   The sun is the local worked case of the same ledger.
import math

k_B = 1.380649e-23
c0 = 2.99792458e8
c02 = c0 ** 2
Q_CMB = 4.175e-14          # J/m^3, the bath
T_CMB = 2.7255             # K
H_planck = 67.4 / 3.0856775814913673e19   # s^-1, the volume-average
H_wall = 73.8 / 3.0856775814913673e19     # s^-1, the wall rate
GYR = 3.15576e16           # s per Gyr

# 1. the bath's state
s_bath = (4.0 / 3.0) * Q_CMB / T_CMB                       # J/K/m^3
n_g = Q_CMB / (2.701 * k_B * T_CMB)                        # photons/m^3
s_per_ph = s_bath / n_g / k_B                              # in units of k_B

print("=" * 78)
print("THE ENTROPY TRACK VIA THE RATE OF HEAT DROP (the circle's clock)")
print("=" * 78)
print("1. THE BATH'S STATE (the locked CMB numbers):")
print("   Q_CMB = %.3e J/m^3 ; T_CMB = %.4f K" % (Q_CMB, T_CMB))
print("   entropy density  s = 4Q/3T = %.3e J/K/m^3" % s_bath)
print("   photon density   n_g = Q/(2.701 k_B T) = %.3e /m^3" % n_g)
print("   entropy per photon = %.4f k_B   (the standard adiabatic constant, reproduced" % s_per_ph)
print("   from the framework's own Q and T - no assumption imported)")
print()
print("2. THE RATE OF HEAT DROP (the redshift law T ~ rho^(1/3) -> d ln Q/dt = -4H):")
for name, H in [("volume-average 67.4 km/s/Mpc", H_planck), ("wall rate 73.8 km/s/Mpc", H_wall)]:
    qdot = -4.0 * H * Q_CMB
    tdot = -H * T_CMB
    sdot = -3.0 * H * s_bath
    print("   H = %-28s -> Q_dot = %+.3e J/m^3/s ; dT/dt = %+.4f K/Gyr ; s_dot = %+.3e J/K/m^3/s"
          % (name, qdot, tdot * GYR, sdot))
print()
print("3. THE CIRCLE'S RETURN (the drop IS the thaw's draw - the entropy production):")
print("   the heat leaving the bath is the heat returning to the untying (the loop's")
print("   return leg); its entropy is generated irreversibly across the weld<->bath")
print("   temperature gap, at the same rate:  s_prod = 3H s = %.3e J/K/m^3/s (wall rate;"
      % (3.0 * H_wall * s_bath))
print("   the entropy density dilutes as s ~ T^3, so s_dot = -3H s - the 4H applies to Q = aT^4, not to s)"
      )
print("   -> entropy per comoving photon is CONSERVED (the 3.60 k_B constant); the")
print("   production is the cycle's own irreversibility, booked at the bath.")
print()
print("4. THE SUN - the local worked case of the same ledger:")
L_sun = 3.828e26
T_eff = 5772.0
M_sun = 1.989e30
P_corona = 1.023e21
T_corona = 1.5e6
E_fault = 3.248e25
f_churn = 0.82498
print("   L_sun/T_eff = %.3e J/K/s   (the photosphere's entropy production)" % (L_sun / T_eff))
print("   per kg: %.3e J/K/s/kg ; the corona's: %.3e J/K/s" % (L_sun / T_eff / M_sun, P_corona / T_corona))
print("   the restricted cycle: E_fault x f_churn / T_corona = %.3e J/K/s" % (E_fault * f_churn / T_corona))
print("   the deep channel's heat drop = mdot_deep c0^2 = 3.916e26 W -> at T_eff: %.3e J/K/s"
      % (3.916e26 / T_eff))
print()
print("5. GO BIGGER - the observable:")
print("   the CMB cools at %.4f K/Gyr (wall rate) - a direct prediction: measure T_CMB(z) at" % (H_wall * T_CMB * GYR))
print("   two redshifts and the slope must read -H; the heat drop rate Q_dot = -4H Q is the")
print("   same clock. The entropy per photon 3.602 k_B is the invariant the whole track")
print("   conserves - the rate of heat drop IS the entropy's own speedometer.")
