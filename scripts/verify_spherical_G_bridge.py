import math

# ==============================================================================
# PWC SPHERICAL HORIZON BRIDGE (D2 + D9 + D39): 3D VOLUME x 4-FOLD SPHERE FLUX
# ==============================================================================
c0      = 2.99792458e8
hbar    = 1.054571817e-34
G_codata = 6.67430e-11
m_p_exp = 1.67262192369e-27 # kg
R_p_meas = 0.8414e-15       # m (Measured muonic proton radius)
s       = 1.0 / 19.0
f_solid = 8.4989e-4         # Locked 1D solid fraction

# 1. Sphere #1: 3D Volumetric Baryon Share (D39)
eta_B   = f_solid ** 3      # 6.1389e-10 (vs Planck 6.104e-10)

# 2. Sphere #2: 4-Fold Spherical Surface-to-Disk Flux Projection (3 x 4 = 12)
# Dimensionless coupling alpha_G uses 4^3 / 3^4 = 64 / 81
alpha_G_pred = (eta_B ** 4) * ((4.0**3) * s / (3.0**4))

# 3. Sphere #3: Proton 4-Quantum Spherical Horizon (D2: m_p * R_p * c0 = 4 * hbar)
# Converting alpha_G to G divides by m_p^2 = 16 * hbar^2 / (R_p^2 * c0^2)
# 64 / 16 = 4 -> G prefactor is 4*s / 81
G_pred  = (eta_B ** 4) * (4.0 * s / 81.0) * ((R_p_meas**2) * (c0**3) / hbar)
G_err_pct = (G_pred - G_codata) / G_codata * 100.0

# Show why omitting the D2 (4^2 = 16) proton horizon caused the -93.75% audit bug:
G_buggy = G_pred / 16.0
bug_err_pct = (G_buggy - G_codata) / G_codata * 100.0

print("=" * 85)
print(" PWC SPHERE-IN-SPHERE GRAVITY AUDIT (D2 + D9 + D39)")
print("=" * 85)
print(f" [1] 3D Baryon Volume Share (eta_B = f_solid^3) : {eta_B:.4e} (Planck: 6.104e-10)")
print(f" [2] 4-Fold Spherical Projection (eta_B^4)      : {eta_B**4:.5e} (f_solid^12)")
print(f" [3] Dimensionless Coupling alpha_G (64s/81)    : {alpha_G_pred:.5e}")
print(f" [4] Proton Horizon Factor (D2: 4^2 = 16)       : Divides 64s/81 -> 4s/81 in G")
print("-" * 85)
print(f"     Predicted G (with 4^2 = 16 horizon)        : {G_pred:.5e} m^3/kg/s^2 ({G_err_pct:+.3f}%)")
print(f"     CODATA Measured G                          : {G_codata:.5e} m^3/kg/s^2")
print(f"     Old Audit Bug (missing 4^2 = 16 factor)    : {G_buggy:.5e} m^3/kg/s^2 ({bug_err_pct:+.2f}%)")
print("=" * 85)
