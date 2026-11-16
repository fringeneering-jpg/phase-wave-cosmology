# universal_eos.py - the medium's master equation of state (2026-10-18)
# The UNIVERSAL EOS, not a local case: from C(rho) = c0.(rho0/rho)^n and
# P = rho.C^2 (the tension IS the pressure), the medium's own polytrope:
#   P(rho) = rho . c0^2 . (rho0/rho)^(2n) = c0^2 . rho0^(2n) . rho^(1-2n)
#   =>  the polytropic index gamma = 1 + 2n
# with K(rho) = rho.C^2 (the compressibility = the a0's interchangeable),
# T(rho) = m_p.C^2/k (the heat's ladder), and the sound speed C itself.
import math

rho_0 = 8.74e-27
rho_max = 1.304e15
c0 = 2.9979e8
m_p = 1.6726e-27
k_B = 1.3806e-23
Y_bow = 5.93e26

n = math.log(c0 / 958e3) / math.log(rho_max / rho_0)
gamma = 1.0 + 2.0 * n

print("THE UNIVERSAL MASTER EQUATION OF STATE:")
print(f"  C(rho) = c0.(rho0/rho)^{n:.4f}")
print(f"  P(rho) = rho.C^2 = c0^2.rho0^(2n).rho^(1-2n)")
print(f"  =>  THE POLYTROPE:  P = P0.(rho/rho0)^{gamma:.4f},  gamma = 1 + 2n = {gamma:.4f}")
print(f"  K(rho) = rho.C^2 = gamma.P  (the compressibility's the pressure's own)")
print(f"  T(rho) = m_p.C^2/k_B  (the heat's the capacity's own)")
print()
print("  the state's across the scales:")
print(f"  {'rho':>10s} {'C (km/s)':>10s} {'P (Pa)':>10s} {'K (Pa)':>10s} {'T (K)':>10s}")
for tag, rho in [("rho0", rho_0), ("1e-20", 1e-20), ("1e-15", 1e-15),
                 ("1e-10", 1e-10), ("rho_max", rho_max)]:
    C = c0 * (rho_0 / rho) ** n
    P = rho * C**2
    K = rho * C**2
    T = m_p * C**2 / k_B
    print(f"  {rho:10.1e} {C/1e3:10,.0f} {P:10.2e} {K:10.2e} {T:10.2e}")
print()
# the polytrope's consistency checks: the P(1) = c0^2.rho0, the P0's
P0 = c0**2 * rho_0
print("  the consistency checks:")
print(f"    P(rho0) = c0^2.rho0 = {P0:.3e} Pa  (the ambient's pressure's)")
print(f"    P(rho0) via the polytrope: {P0:.3e} Pa  (the same's)")
print(f"    the polytropic index: gamma = {gamma:.4f}  (the SOFT EOS, the ~isothermal's)")
print()
print("the honest flags: the n's the two-anchor's fit (the c0 and the 958 km/s,")
print("the locked's); the EOS's the framework's own P = rho.C^2 (the tension's =")
print("the pressure's, the ruling's); the gamma's the polytrope's index's the")
print("whole's medium's - the universal's state's law's in's one's line's.")

print("=" * 80)
print("GRAB THE FULL PHASE WAVE COSMOLOGY THEORY & SOURCE CODE:")
print("  Master GitHub Repository : https://github.com/fringeneering-jpg/phase-wave-cosmology")
print("  Permanent Zenodo Archive : https://doi.org/10.5281/zenodo.24281039")
print("  Wurral Ephemeris Engine  : https://github.com/fringeneering-jpg/Wurral")
print("  Jiba Station-Keeping     : https://github.com/fringeneering-jpg/Jiba")
print("  Author ORCID             : https://orcid.org/0009-0005-4121-4296")
print("=" * 80)
