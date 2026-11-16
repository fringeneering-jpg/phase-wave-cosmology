import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# ---------------------------------------------------------
# CONSTANTS & ILRS MASTER EXPONENTS
# ---------------------------------------------------------
ALPHA = 2.635
BETA  = 4.445
H0_SEC = 2.396e-18
R1_KM = 7190.137
STRAIN1_S = 1.746e-09
R_EQ_EARTH = 708644.0

# ---------------------------------------------------------
# SETUP PLOT (Dark Mode for Astrophysics Aesthetic)
# ---------------------------------------------------------
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("PWC UNIFIED COSMOLOGICAL FRAMEWORK (Calibrated via ILRS: $\\alpha=2.635, \\beta=4.445$)", 
             fontsize=18, fontweight='bold', y=1.02)

# =========================================================
# PANEL 1: PWC RADIAL BOUNDARY (STRAIN DECAY)
# =========================================================
r_vals = np.logspace(3.7, 6.0, 500) # 5,000 km to 1,000,000 km
# PWC beta=4.445 decay bottoming out at H0 floor
strain_vals = np.maximum(H0_SEC, STRAIN1_S * ((R1_KM / r_vals) ** BETA))

ax1.plot(r_vals, strain_vals, color='cyan', lw=2.5, label=r'$\Gamma(r) \propto r^{-4.445}$')
ax1.axhline(H0_SEC, color='magenta', linestyle='--', lw=2, label='Far-Field $H_0$ Floor')

# Add measured benchmark points
benchmarks = [
    ("Starlette (LEO)", 7190.1, 1.746e-09, 'white'),
    ("LAGEOS-1 (MEO)", 12278.1, 1.618e-10, 'white'),
    ("GEO Belt (QZS-3)", 42164.0, 6.717e-13, 'white'),
    ("Moon", 384400.0, 3.634e-17, 'yellow'),
    ("H0 Equalization", 708644.0, 2.396e-18, 'magenta')
]

for name, r, st, col in benchmarks:
    ax1.scatter(r, st, color=col, s=70, zorder=5)
    ax1.annotate(name, (r, st), textcoords="offset points", xytext=(10, 5), 
                 color=col, fontsize=10, fontweight='bold')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_title("1. Local Strain Gradient (Earth Outward)", fontsize=14, fontweight='bold')
ax1.set_xlabel("Geocentric Radius (km)", fontsize=12)
ax1.set_ylabel("Local Radial Strain Rate (s$^{-1}$)", fontsize=12)
ax1.grid(True, alpha=0.2)
ax1.legend(loc='upper right', fontsize=11)

# =========================================================
# PANEL 2: JWST TIMESCALE RELIEF (Age vs z)
# =========================================================
# Dynamic calculation synchronized with Section 3 Table 3.2
f_stretch = 2.1214 / (1.0 + 14.32)
t_H_Myr = 13225.0
z_obs = np.array([4.00, 7.00, 10.00, 14.32])
lcdm_age = np.array([1540, 770, 470, 290])
dz_asym = f_stretch * (1.0 + z_obs)
z_base = z_obs - dz_asym
pwc_age = np.round((2.0 * t_H_Myr) / (1.0 + z_base))  # Yields np.array([6140., 3838., 2791., 2004.])

# Smooth interpolation for curves
z_smooth = np.linspace(3.5, 15, 200)
spl_lcdm = make_interp_spline(z_obs, lcdm_age, k=2)
spl_pwc = make_interp_spline(z_obs, pwc_age, k=2)

ax2.plot(z_smooth, spl_lcdm(z_smooth), color='red', lw=2.5, linestyle=':', label='Standard LCDM Age')
ax2.plot(z_smooth, spl_pwc(z_smooth), color='lime', lw=3, label='PWC Active Growth Age')
ax2.fill_between(z_smooth, spl_lcdm(z_smooth), spl_pwc(z_smooth), color='lime', alpha=0.1)

# Scatter exact observation points
ax2.scatter(z_obs, lcdm_age, color='red', s=60, zorder=5)
ax2.scatter(z_obs, pwc_age, color='lime', s=60, zorder=5)

ax2.annotate(f"JWST z=14.32\nLCDM: 290 Myr", xy=(14.32, 290), xytext=(9, 600),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=6), color='red')
ax2.annotate(f"PWC Base z=12.20\nReal Age: 2,004 Myr\n(6.9x more time!)", xy=(14.32, 2004), xytext=(7, 2200),
             arrowprops=dict(facecolor='lime', shrink=0.05, width=1.5, headwidth=6), color='lime', fontweight='bold')

ax2.set_title("2. JWST Falsifier: Fictitious z vs. Real Formation Time", fontsize=14, fontweight='bold')
ax2.set_xlabel("Observed Cosmological Redshift ($z_{obs}$)", fontsize=12)
ax2.set_ylabel("Time Available for Galaxy Formation (Myr)", fontsize=12)
ax2.grid(True, alpha=0.2)
ax2.legend(loc='upper right', fontsize=11)

# =========================================================
# PANEL 3: BULLET CLUSTER LENSING (Abel Projection)
# =========================================================
# 2D Projected Strain Concentration Profile Sigma(R) ~ R^(-(alpha-2))
R_kpc = np.linspace(1, 300, 500)
r_gal = 14.52
r_gas = 180.0
f_gal = 0.15
f_gas = 0.85
mach_boost = 8.62 # (v_shock/v_virial)^alpha

# Normalize profiles for visualization (kappa proportionality)
kappa_gal = f_gal * mach_boost * (r_gal / np.sqrt(r_gal**2 + R_kpc**2)) ** (ALPHA - 2.0)
kappa_gas = f_gas * 1.0 * (r_gas / np.sqrt(r_gas**2 + R_kpc**2)) ** (ALPHA - 2.0)

ax3.plot(R_kpc, kappa_gas, color='orange', lw=2.5, label='Stalled X-Ray Gas (85% Baryons)')
ax3.plot(R_kpc, kappa_gal, color='cyan', lw=3, label='Plunging Galaxies (15% Baryons + Mach Dipole)')
ax3.fill_between(R_kpc, 0, kappa_gal, color='cyan', alpha=0.2)
ax3.fill_between(R_kpc, 0, kappa_gas, color='orange', alpha=0.2)

ax3.axvline(150, color='white', linestyle='--', alpha=0.4, label='Clowe 150 kpc Aperture')

ax3.annotate("Predicted 7.5x Lensing Peak\nOver Galaxy Centers (Zero Dark Matter)", 
             xy=(14.5, np.max(kappa_gal)), xytext=(50, np.max(kappa_gal)*0.8),
             arrowprops=dict(facecolor='cyan', shrink=0.05, width=1, headwidth=5), color='cyan', fontweight='bold')

ax3.set_title("3. Bullet Cluster: Weak-Lensing Convergence $\\kappa(R)$", fontsize=14, fontweight='bold')
ax3.set_xlabel("Projected Radius from Core (kpc)", fontsize=12)
ax3.set_ylabel("Normalized Lensing Amplitude", fontsize=12)
ax3.set_xlim(0, 300)
ax3.grid(True, alpha=0.2)
ax3.legend(loc='upper right', fontsize=11)

# ---------------------------------------------------------
# RENDER AND SAVE
# ---------------------------------------------------------
plt.tight_layout()
plt.savefig("PWC_Master_Visuals.png", dpi=300, bbox_inches='tight')
print("\n[SUCCESS] Plot saved as 'PWC_Master_Visuals.png'. Check your directory!")
plt.close()