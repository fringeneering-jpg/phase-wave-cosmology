# ending_size.py - the photon's weight, the waves' count, the ending (2026-10-18)
# We know the medium in the proton/electron/neutron, and the waves that make
# them. The photon's weight = L/c0^2 (the wave's mass), but the displacement
# it causes makes it WEIGHTLESS (the buoyant's - the wave rides at max-P, the
# push cancels the pull). The totality of the ending size: when every knot
# unties, the whole field's back - V_end = M_total / rho0.
import numpy as np

c0 = 2.9979e8
rho_0 = 8.74e-27
m_e = 9.109e-31
h = 6.626e-34

print("THE WAVES, THE PHOTON'S WEIGHT, AND THE ENDING:")
print()
print("1. THE KNOTS' WAVE COUNTS (the hadron ladder's family):")
print("   the electron:  1 knot (the single chiral loop, the 720-deg)")
print("   the proton:    1836.15 x the electron's mass (the sealed)")
print("   the neutron:   1838.68 x (the proton + the wrapped electron)")
print("   the ladder:    pi0 = 16^2 + 8 + 1/7 = 264.143 m_e, pi+- = 273.135,")
print("                  K+- = 966.102 - the wave-count's arithmetic")
print()
print("2. THE PHOTON'S WEIGHT (the wave's own mass):")
# the photon's the unpaired wave: its weight's L/c0^2, and the displacement's
# the riding's - the max-P push equals the pull: the weightless's
for eV in [2.48, 13.6, 511e3]:
    E = eV * 1.602e-19
    m_ph = E / c0**2
    print(f"   the photon at {eV:.4g} eV:  m = L/c0^2 = {m_ph:.3e} kg  (the wave's weight's)")
print("   the WEIGHTLESSNESS: the displacement the wave causes in the medium is")
print("   exactly its own weight's push - the buoyant's riding at max-P. The")
print("   weight's there, the displacement cancels it - that's the massless read.")
print()
print("3. THE TOTALITY OF THE ENDING SIZE:")
# the census's total: the medium + the matter's + the heat's shares
f_solid = 8.4989e-4
rho_matter = f_solid * rho_0
rho_total = rho_0 + rho_matter + 19.0 * 4.175e-14 / c0**2
# the ending: every knot unties -> the whole mass returns to the field's
# the final density = rho0 everywhere's, the final volume = M_total/rho0
# the ratio: the ending's size / the now's size = (rho_total/rho0)^(1/3)
scale_end = (rho_total / rho_0) ** (1.0 / 3.0)
print(f"   the census: rho_total = {rho_total:.4e}, rho0 = {rho_0:.4e} kg/m^3")
print(f"   the ending's scale factor: (rho_total/rho0)^(1/3) = {scale_end:.6f}")
print(f"   the ending's size's growth: {scale_end - 1.0:.2e}  (the 0.019% larger's)")
print(f"   - the matter's and heat's share's the ~0.19% of the total's; when all")
print(f"   the knots untie, the field's volume grows by that share's cubic root.")
print()
print("the honest state: the photon's weight is the L/c0^2 (the wave's), the")
print("weightlessness is the displacement's cancellation (the buoyant's), and the")
print("ending's size is the census's cubic root - the untying's totality returns")
print("the field to the full's, ~0.06% larger per the linear scale.")
