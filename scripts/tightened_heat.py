# tightened_heat.py - the four refinements into the one equation (2026-10-17)
# 1. the shell's thickness scales with the surface area (dR ~ R^2 -> the
#    shell's volume ~ R^4);
# 2. the mergers dropped the medium off (the shell's mass = rho_max . V_shell);
# 3. the core/shell sizing's the framework's own derivations;
# 4. the medium can't pass through itself at MaxP - the shock's capped, the
#    heat's trapped, the vent's the only leak.
import numpy as np

rho_max = 1.304e15
Y_bow = 5.93e26
c0 = 2.9979e8
m_p = 1.6726e-27
k_B = 1.3806e-23

# the core/shell sizing: the neutron's anchor (the papers')
R_n = 1.1e-15          # the core radius
dR_n = 0.15e-15        # the shell's thickness at the neutron's scale

# the shell's thickness scales with the SURFACE AREA: dR = dR_n . (R/R_n)^2
# (the bigger the core, the thicker the shell)
def dR(R):
    return dR_n * (R / R_n) ** 2

def T_int(R):
    # the internal bow's heat: the shock's kinetic at the local cap; the cap
    # ladder's anchored (the c0 and the 958 km/s), but the MaxP no-pass caps
    # the shock at the yield: the heat's the min of the kinetic and the
    # yield's own temperature scale (Y_bow . V_shell / (N . k_B)-ish)
    V_shell = 4.0/3.0 * np.pi * ((R + dR(R))**3 - R**3)
    # the shock's kinetic at the core's cap: C(R) from the anchored ladder
    rho_0 = 8.74e-27
    n = np.log(c0 / 958e3) / np.log(rho_max / rho_0)
    rho_R = rho_max * (R_n / R) ** (1.0/3.0)  # the core's density's the size's (the simple's)
    C_R = c0 * (rho_0 / max(rho_R, 1e-30)) ** n
    T_kin = m_p * C_R**2 / k_B
    # the no-pass cap: the yield's work per the shell's mass's the temperature's ceiling
    M_shell = rho_max * V_shell
    T_cap = Y_bow * V_shell / (M_shell / m_p * k_B)  # the Y.V / (N.k) = the yield's per-particle
    return min(T_kin, T_cap), T_kin, T_cap, V_shell, M_shell

print("THE TIGHTENED HEAT - the four refinements:")
print()
print("  the neutron's anchor:")
t, tk, tc, vs, ms = T_int(R_n)
print(f"    R = {R_n:.2e} m, dR = {dR(R_n):.2e} m, V_shell = {vs:.3e} m^3, M_shell = {ms:.3e} kg")
print(f"    T_kin = {tk:.2e} K, T_cap = {tc:.2e} K ->  T_int = {t:.2e} K")
print()
print("  the scale's ladder (the same physics across the sizes):")
for tag, R in [("the neutron core", 1.1e-15), ("the proton core", 0.84e-15),
               ("the 10x core", 1.1e-14), ("the 1e6x core", 1.1e-9)]:
    t, tk, tc, vs, ms = T_int(R)
    print(f"    {tag:16s}: R = {R:.2e}, dR = {dR(R):.2e} ->  T_int = {t:.2e} K (kin {tk:.1e}, cap {tc:.1e})")
print()
print("the honest read: the no-pass cap and the kinetic cross where the shell's")
print("thick enough; below it the kinetic's the heat, above it the yield's the")
print("ceiling. The shell's R^4-ish volume's the shed's medium's (the merger's")
print("dropped-off), and the vent's the observable's fraction.")
