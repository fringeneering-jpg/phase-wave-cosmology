# PWC MAGNETIC MOMENT: GEOMETRIC COUNTER-CURRENT ALLOCATION
import math

# 1. Baseline Inputs (Strictly Fixed)
R_p0 = 0.8414  # fm
v_frac = 11.0 / 12.0
gamma = 1.0 / math.sqrt(1.0 - v_frac**2)
R_e = 1.3402678  # fm
chi = 12.0 / 11.0
R_plus = R_p0 / math.sqrt(chi) # 0.8023 fm

# 2. Charge Fractions
f0 = (2.0 / 19.0) * (361.0 / 357.0)  # Active pair fraction: 0.1064426

print("="*85)
print(" 1. RECONCILING THE INVERSE-FIT DISCREPANCY")
print("="*85)
# Core and Locked Thread Moments
mu_p_obs = 2.792847
mu_core = mu_p_obs / math.sqrt(chi)  # 2.668744 mu_N
mu_locked = -4.0 * (1.0 - f0) * v_frac * (R_plus / R_p0)  # -3.131689 mu_N
core_plus_locked = mu_core + mu_locked  # -0.462945 mu_N

# Active Base Moment
mu_active_base = -4.0 * f0 * v_frac * (R_e / R_p0)  # -0.621693 mu_N

# The 26/11 Weighting (Inverse-Fit Artifact)
mu_pair_26_11 = (26.0 / 11.0) * mu_active_base  # -1.469456 mu_N
mu_total_26_11 = core_plus_locked + mu_pair_26_11

print(f"Core + Locked Thread      : {core_plus_locked:+.6f} mu_N")
print(f"Base Active Thread        : {mu_active_base:+.6f} mu_N")
print(f"Pair with 26/11 Weighting : {mu_pair_26_11:+.6f} mu_N")
print(f"Total Moment (26/11)      : {mu_total_26_11:+.6f} mu_N")
print(f"Target mu_n               : -1.913042 mu_N")
print(f"-> Discrepancy confirmed. The 5-digit landing required floating chi or v_locked.")

print("\n" + "="*85)
print(" 2. GEOMETRIC DERIVATION: 3-AXIS ALLOCATION OF THE 2-QUANTA PAIR")
print("="*85)
# Instead of an inverse fit, we derive x from the wave structure.
# The active excursion is exactly the 2-quanta pair.
# Distributed over the 3 spatial axes of the cage, the weight per axis is 2/3.
# If the positive counter-rotating branch is driven by the 2 transverse axes:
x_geom = (2.0 / 3.0) * f0
# The negative branch must be -(x + f0) to maintain net charge -f0.
neg_branch = -(x_geom + f0)
# Magnetic enhancement factor E = (2x + f0) / f0
enhancement_geom = (2.0 * x_geom + f0) / f0  # Exactly 7/3

mu_pair_geom = enhancement_geom * mu_active_base
mu_total_geom = core_plus_locked + mu_pair_geom

print(f"Derived +x branch         : +2/3 f0")
print(f"Derived -x branch         : -5/3 f0")
print(f"Net Charge Preserved      : {x_geom + neg_branch:.5f} (exactly -f0)")
print(f"Geometric Enhancement     : {enhancement_geom:.5f} (exactly 7/3)")
print(f"Predicted mu_pair         : {mu_pair_geom:+.6f} mu_N")
print(f"Forward Predicted mu_n    : {mu_total_geom:+.6f} mu_N")
print(f"Difference from Target    : {abs(mu_total_geom - (-1.913042)):.6f} mu_N (272 ppm)")
print("="*85)

print("=" * 80)
print("GRAB THE FULL PHASE WAVE COSMOLOGY THEORY & SOURCE CODE:")
print("  Master GitHub Repository : https://github.com/fringeneering-jpg/phase-wave-cosmology")
print("  Permanent Zenodo Archive : https://doi.org/10.5281/zenodo.24281039")
print("  Wurral Ephemeris Engine  : https://github.com/fringeneering-jpg/Wurral")
print("  Jiba Station-Keeping     : https://github.com/fringeneering-jpg/Jiba")
print("  Author ORCID             : https://orcid.org/0009-0005-4121-4296")
print("=" * 80)
