# heat_calculator.py - the core/shell/speed -> T(x) calculator (2026-10-17)
# INPUT: the core radius, the shell thickness, the surface area, the speed,
# the vent fraction (the cover's), and the distance X -> OUTPUT: the
# surrounding temperature at X. The framework's own equation:
#   T(x) = T_max . f_vent . (1 + (v/C_bow)^2) . (R_shell / x)^(1/2)
import numpy as np

T_MAX = 5.51e7      # the MaxP's universal heat (the Y_bow.m_p/(rho_max.k_B))
C_BOW = 958e3       # the bow's compressed cap (m/s)

def T_surrounding(R_core, dR_shell, v, f_vent, x):
    """
    R_core   : the core radius (m)
    dR_shell : the shell's thickness (m)
    v        : the speed (m/s)
    f_vent   : the vent fraction (the leak's share - the cover's 1 - f_vent)
    x        : the distance from the core's centre (m)
    """
    R_shell = R_core + dR_shell
    mu_everyday = (v / 2.9979e8)**2            # the ambient's register's
    mu_bow = (v / C_BOW)**2                     # the bow's register's
    T_surf = T_MAX * f_vent * (1.0 + mu_bow + mu_everyday)
    if x <= R_shell:
        return T_surf
    return T_surf * (R_shell / x) ** 0.5

if __name__ == "__main__":
    print("THE SURROUNDING-TEMPERATURE CALCULATOR")
    print("  T(x) = T_max . f_vent . (1 + (v/C_bow)^2 + (v/c0)^2) . (R_shell/x)^(1/2)")
    print()
    # the demonstration: the RBH-1 vs the Andromeda's
    cases = [
        ("RBH-1",        3e7*1.477e3*0.5, 0.15e-15*1e0, 954e3, 0.9, None),  # the open vent's
        ("the Andromeda", 1.4e8*1.477e3*0.5, 0.15e-15*1e3, 954e3, 0.1, None),  # the covered's
        ("the neutron",  1.1e-15, 0.15e-15, 600e3, 0.01, None),
    ]
    for name, R, dR, v, fv, _ in cases:
        # the shell's thickness scales with the surface's (the dR ~ R^2's)
        dR_eff = dR * (R / 1.1e-15) ** 2 if R > 1e-10 else dR
        R_shell = R + dR_eff
        x_out = 10.0 * R_shell
        T_at_x = T_surrounding(R, dR_eff, v, fv, x_out)
        print(f"  {name:14s}: R={R:.2e}, dR={dR_eff:.2e}, v={v/1e3:.0f} km/s, f_vent={fv:.2f}")
        print(f"      T at x = 10.R_shell ({x_out:.2e} m):  {T_at_x:.2e} K = {T_at_x/1e6:.2f} million K")
    print()
    print("the inputs the framework wants: the core size, the shell thickness,")
    print("the volumetric area (the 4.pi.R_shell^2), the speed, the vent's share,")
    print("and the distance X - the output's the surrounding temperature at X.")
