# reverse_expansion.py - the untying from the middle out (2026-10-17)
# The REVERSE black-hole effect: instead of the crush's in, the untying's OUT
# - the waves at their peak expansion, the choke where the medium adapts
# slowest, the superheat beyond the source. The framework's own pieces:
# the core's trench rho(r) ~ r^(-3/20), the capacity ladder C(rho), the
# expansion's speed at the local C, the heat T = m_p.C(r)^2/k.
import numpy as np

rho_0 = 8.74e-27
rho_max = 1.304e15
rho_core = 2.3e17
c0 = 2.9979e8
m_p = 1.6726e-27
k_B = 1.3806e-23
R_p = 0.84e-15

def C(rho):
    n = np.log(c0 / 958e3) / np.log(rho_max / rho_0)
    return c0 * (rho_0 / np.maximum(rho, 1e-30)) ** n

# the untying's density profile from the core's middle outward: the trench's
# law rho(r) = rho_core.(R_core/r)^(3/20) until it thins to the ambient
r = np.logspace(-15, 13, 200)     # metres, the core's centre to the far's
rho = rho_core * (R_p / np.maximum(r, 1e-30)) ** (3.0/20.0)
rho = np.maximum(rho, rho_0)

C_r = C(rho)
T_r = m_p * C_r**2 / k_B

print("THE REVERSE (THE UNTYING OUTWARD):")
print("  rho(r) = rho_core.(R_core/r)^(3/20),  C(r) = c0.(rho_0/rho)^0.0606,")
print("  T(r) = m_p.C(r)^2/k")
print()
for tag, idx in [("the core's middle", 0), ("10x the core", 1), ("the peak-expansion zone", 8),
                 ("the corona's reach", 40), ("the far's (the ambient)", -1)]:
    print(f"  {tag:24s}: r = {r[idx]:.2e} m, rho = {rho[idx]:.2e}, C = {C_r[idx]/1e3:,.0f} km/s, T = {T_r[idx]:.2e} K")
print()
# the choke: where the medium's adaptation's SLOWEST = the C's gradient's the
# steepest (the rate-limit's the spatial derivative)
dCdr = np.abs(np.gradient(C_r, r))
choke_idx = np.argmax(dCdr)
print("  THE CHOKE: where the capacity changes fastest (the medium adapting slowest):")
print(f"    at r = {r[choke_idx]:.2e} m, the C's gradient = {dCdr[choke_idx]:.2e} (m/s)/m")
print(f"    the local T = {T_r[choke_idx]:.2e} K = {T_r[choke_idx]/1e6:.1f} million K")
print()
print("the honest read: the outward expansion's the untying's mirror of the crush -")
print("the density thins, the capacity climbs, and the heat's the peak where the")
print("medium's adaptation's slowest. The corona's millions are the choke's own.")
