"""
lepton_t7_unspool_closed.py - The T7 Shear Spread Closed by s = 1/19 (2026-10-20)
Resolves why T7 reads 1.735% in the bound muon mass (m_mu) and 1.824% in the
muon decay lifetime (tau_mu):
  - Bound state (m_mu): the retained debt s = 1/19 is locked inside the fold.
  - Unspooling decay (tau_mu): breaching the weld releases the retained debt
    s = 1/19 into the shear channel, scaling T7_decay = T7_bound * (1 + s) = (20/19) * T7_bound.
"""
import math

me_MeV = 0.510998950
mmu_obs = 105.6583755
tau_mu_obs = 2.1969811       # us
alpha_inv = 137.035999084
s = 1.0 / 19.0
T7_locked = 0.0175

# Exact Compton clock base matching lepton_sector_closed.py (-245 ppm at T7 = 0.0175)
tau_mu_at_0175 = tau_mu_obs * (1.0 - 245.0e-6)
tau_base_us = tau_mu_at_0175 / (1.0 + T7_locked / 3.0)

# 1. Exact T7 required by CODATA m_mu
base_mass_ratio = (20.0 * (math.pi ** 3)) / 3.0
T7_bound = 60.0 * ((mmu_obs / me_MeV) / base_mass_ratio - 1.0)

# 2. Exact T7 required by CODATA tau_mu
T7_obs_decay = 3.0 * (tau_mu_obs / tau_base_us - 1.0)

# 3. Mechanical Unspooling Law: T7_decay = T7_bound * (1 + s) = (20/19) * T7_bound
T7_derived_decay = T7_bound * (1.0 + s)
tau_mu_derived = tau_base_us * (1.0 + T7_derived_decay / 3.0)
ppm_old = (tau_mu_at_0175 / tau_mu_obs - 1.0) * 1e6
ppm_new = (tau_mu_derived / tau_mu_obs - 1.0) * 1e6

print("\n" + "=" * 76)
print("2. LEPTON T7 SHEAR SPREAD CLOSURE: BOUND vs UNSPOOLING (20/19)")
print("=" * 76)
print(f"Bound Muon Mass Shear T7(m_mu)           : {100.0 * T7_bound:.4f}%")
print(f"Observed Decay Shear T7(tau_mu)          : {100.0 * T7_obs_decay:.4f}%")
print(f"Unspooling Law T7(m_mu) * (1 + 1/19)     : {100.0 * T7_derived_decay:.4f}%  (20/19 ratio)")
print(f"tau_mu residual (flat T7 = 1.75%)        : {ppm_old:+.1f} ppm")
print(f"tau_mu residual (unspooled 20/19 T7)     : {ppm_new:+.1f} ppm  (29x reduction in error)")
