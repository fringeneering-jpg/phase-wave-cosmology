import math

# ==============================================================================
# D46 & D48: SUBATOMIC-TO-COSMOLOGY SYNC & FULL PERIODIC TABLE CLOSURE
# ==============================================================================
c0      = 2.99792458e8
hbar    = 1.054571817e-34
alpha   = 7.2973525693e-3
hc_MeV  = 197.3269804      # MeV * fm
alpha_hc = alpha * hc_MeV  # 1.439964 MeV * fm

m_e     = 0.51099895       # MeV
m_p_exp = 938.272088       # MeV (CODATA)
R_p     = 0.8414           # fm (Measured anchor)
s       = 1.0 / 19.0
T       = 27.0             # 3^3 cubic boundary
n_fold  = 2.0 / 33.0       # 2 / (2*19 - 5)

# 1. D46 <-> Proton Knot Relief (n = 2/33 across 3 spatial axes = 1/11)
m_knot_raw = 2.0 * m_e * 1000.0 * (1.0 + 1.0 / (T**2))
relief_3D  = 1.5 * n_fold  # 3/33 = 1/11
m_p_deriv  = m_knot_raw * (1.0 / (1.0 + relief_3D)) # * 11/12
mp_err_pct = (m_p_deriv - m_p_exp) / m_p_exp * 100.0

# 2. D46 Master Constitutive Ceiling & RBH-1 Stall
Y_bow   = 5.9307e26        # Pa (D8 electron fold yield)
rho_0   = 8.74e-27         # kg/m^3
rho_max = ((2.0 * Y_bow / (c0**2))**(33.0/29.0)) * (rho_0**(-4.0/29.0))
C_min   = math.sqrt(2.0 * Y_bow / rho_max) / 1000.0 # km/s

# 3. D48 Coulomb Lattice Lock (57/40 & 6/5 Cage Factor)
r0_cage = R_p * (57.0 / 40.0) # 1.1990 fm (at R_p=0.8414) or 1.1970 fm (at R_p=0.8400)
a_C_bare = alpha_hc / (2.0 * r0_cage)
cage_factor = 6.0 / 5.0    # 6 cubic faces / 5 core units (2-1-2)
a_C     = cage_factor * a_C_bare

# 4. Nuclear Force Ladder (D43) & Heavy Magic Shells (50, 82, 126)
a_V     = (18.0 / 19.0) * (m_p_exp / 57.0)
a_S     = (20.0 / 19.0) * (m_p_exp / 57.0)
E_scale = 2.0 * (a_S - a_V)
E_shell_heavy = E_scale * (17.0 / 19.0) # Spin-1/2 slip (1 - 2/19)

fission_limit = (2.0 * a_S) / a_C

print("=" * 85)
print(" PWC D46 <-> D48 UNIFICATION AUDIT: SUBATOMIC KNOT TO PERIODIC TABLE")
print("=" * 85)
print(f" [1] PROTON KNOT & D46 SHAPE EXPONENT (n = 2/33 = {n_fold:.6f})")
print(f"     Raw 3D Baryon Knot (2*m_e*10^3*(1+1/729)) : {m_knot_raw:.3f} MeV")
print(f"     3-Axis Knot Relief (11/12 from n=2/33)    : {m_p_deriv:.3f} MeV (vs {m_p_exp:.3f}, {mp_err_pct:+.3f}%)")
print(f"     D46 Derived rho_max Ceiling               : {rho_max:.5e} kg/m^3")
print(f"     D46 Terminal Acoustic Stall (C_min)       : {C_min:.2f} km/s")
print("-" * 85)
print(f" [2] D48 PERIODIC TABLE COULOMB LOCK & HEAVY SHELLS")
print(f"     Lattice Cage Spacing r0 = R_p*(57/40)     : {r0_cage:.4f} fm")
print(f"     Bare Electrostatic Scale a_C,bare         : {a_C_bare:.5f} MeV")
print(f"     6/5 Cage Factor (6 faces / 5 core units)  : {a_C:.5f} MeV")
print(f"     Bohr-Wheeler Fission Limit (2*a_S / a_C)  : {fission_limit:.2f} (Empirical: 47-50)")
print(f"     Heavy Magic Shell (50, 82, 126) Closure   : +{E_shell_heavy:.4f} MeV per shell")
print(f"     Doubly-Magic Pb-208 Shell Lock (2x)       : +{2*E_shell_heavy:.3f} MeV")
print("=" * 85)
