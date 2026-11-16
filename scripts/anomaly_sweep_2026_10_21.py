"""
anomaly_sweep_2026_10_21.py
Verifies the 11 zero-parameter anomaly sweeps & derivations from the Full-Framework Audit
using ONLY locked PWC constants.
"""
import math

c0 = 2.99792458e8
G = 6.67430e-11
k_B = 1.380649e-23
e_J = 1.602176634e-19
rho0 = 8.74e-27
s = 1.0 / 19.0
T_7_bound = s / 3.0                      # 1/57 = 0.01754386
T_7_decay = (20.0 / 19.0) * T_7_bound    # 20/1083 = 0.01846722
N_stages = 16
phi = (1.0 + math.sqrt(5.0)) / 2.0
f_solid = 8.498917e-4
s_derived = 0.2250
drho_geom = ((1.5 * math.gamma(1.0 / 3.0)) - 3.0) / (4.0 * math.pi / 3.0)  # +0.24313
a0_bare = (c0 / math.sqrt(3.0)) * math.sqrt(G * rho0 / 4.0)                # 6.6110e-11 m/s^2
a0_knee = phi * a0_bare                                                    # 1.0695e-10 m/s^2
H0_kmsMpc = 73.935
Mpc_m = 3.085677581491367e22
H0_SI = (H0_kmsMpc * 1000.0) / Mpc_m     # 2.39607e-18 s^-1
mp_pwc_MeV = 937.19
dU_eV = 2.470

# 1. Voyager 1/2 Heliopause Solid-Debt Pressure Step (1 pPa = 1e-12 Pa)
P_base_pPa = (rho0 * (c0 ** 2) / 3.0) * 1.0e12      # 261.84 pPa (0.2618 nPa)
P_amb_pPa = (1.0 - s) * P_base_pPa                  # 248.06 pPa (0.2481 nPa)
P_hp_min = f_solid * P_base_pPa                     # 0.2225 pPa
P_hp_max = f_solid * (1.0 + drho_geom) * P_amb_pPa  # 0.2621 pPa
P_hp_mid = 0.5 * (P_hp_min + P_hp_max)              # 0.2423 pPa (vs 0.230-0.251 pPa Voyager/Cassini)

# 2. Gaia DR3 Wide Binaries (M_tot = 1.56 Msun)
M_bin = 1.56 * 1.98847e30
AU_m = 1.495978707e11
r_knee_AU = math.sqrt(G * M_bin / a0_knee) / AU_m
r_onset_AU = r_knee_AU / math.sqrt(1.0 + 27.0 / 3.0)
G_boost_min = 1.0 + drho_geom
G_boost_max = phi
G_boost_mid = 0.5 * (G_boost_min + G_boost_max)

# 3. Nuclear EMC Effect
emc_lin_swell = (1.0 / (1.0 - s)) - 1.0
emc_area_min = ((19.0 / 18.0) ** 2) - 1.0
emc_area_max = 3.0 * s

# 4. Atomki X17 Boson
E_X17_A = N_stages * (20.0 / 19.0)
E_X17_B = mp_pwc_MeV * 0.5 * (T_7_bound + T_7_decay)
E_X17_obs = 16.84

# 5. Cosmological Lithium-7 Problem
Li7_BBN = 5.40e-10
Li7_obs = 1.58e-10
Li7_obs_err = 0.11e-10
S_Li_A = (3.0 * 19.0) / 16.0
S_Li_B = 3.0 * (19.0 / 18.0)
Li7_pwc_A = Li7_BBN / S_Li_A
Li7_pwc_B = Li7_BBN / S_Li_B

# 6. Pioneer 10/11 Anomaly
a_bare = c0 * H0_SI
a_pioneer_pwc = a_bare * (1.0 + drho_geom)
a_pioneer_obs = 8.74e-10
a_pioneer_err = 1.33e-10

# 7. Cosmic Baryon-to-Photon Ratio (eta_B) & Stage-3 Normalizations
eta_B_pwc = f_solid ** 3
eta_B_obs = 6.104e-10
eta_B_err = 0.058e-10
eta_tail_norm = (f_solid ** 3) * T_7_bound
f_bulge_retain = T_7_bound * (1.0 - drho_geom)

# 8. W-Boson Mass (8-Pair N=16 Winding)
M_Z = 91187.6
sin2_thetaW_pwc = s_derived * (1.0 - 8.0 * f_solid * (20.0 / 19.0))
M_W_pwc = M_Z * math.sqrt(1.0 - sin2_thetaW_pwc)
M_W_lhc = 80360.2
M_W_err = 9.9

# 9. S8 Weak-Lensing Void Shift & High-Tc Cuprate Pairing
S8_planck = 0.832
S8_pwc = S8_planck * (19.0 / 20.0)
S8_des_y6 = 0.789
S8_des_err = 0.012
gap_2Delta_meV = 1000.0 * dU_eV * T_7_bound
Tc_cuprate_K = (18.0 / 19.0) * (gap_2Delta_meV * 1e-3 * e_J) / (3.528 * k_B)

print("=" * 88)
print("PWC ZERO-PARAMETER ANOMALY SWEEP VERIFICATION (2026-10-21)")
print("=" * 88)
print(f" 1. Voyager Heliopause Floor    : f_solid*P_base = {P_hp_min:.4f}..{P_hp_max:.4f} pPa (mid {P_hp_mid:.4f} vs 0.230-0.251 pPa obs)")
print(f" 2. Gaia Wide-Binary Boost      : Onset {r_onset_AU:.0f}-{r_knee_AU:.0f} AU | G_eff/G = {G_boost_min:.3f}..{G_boost_max:.3f} (mid {G_boost_mid:.3f} vs 1.43 +/- 0.06)")
print(f" 3. Nuclear EMC Swelling        : Linear +{100*s:.2f}%..+{100*emc_lin_swell:.2f}% (obs ~5.5%) | Area +{100*emc_area_min:.2f}%..+{100*emc_area_max:.2f}% (DIS 10-16%)")
print(f" 4. Atomki X17 Transition       : Path A (16*20/19) = {E_X17_A:.4f} MeV ({100*(E_X17_A/E_X17_obs - 1):+.4f}%) | Path B = {E_X17_B:.4f} MeV vs 16.84 +/- 0.12 MeV")
print(f" 5. Cosmological Li-7 Problem   : {Li7_pwc_A*1e10:.3f}e-10 ({(Li7_pwc_A-Li7_obs)/Li7_obs_err:+.2f}s) to {Li7_pwc_B*1e10:.3f}e-10 vs 1.58 +/- 0.11e-10")
print(f" 6. Pioneer 10/11 Drift (a_P)   : {a_pioneer_pwc:.4e} m/s^2 vs {a_pioneer_obs:.2e} +/- {a_pioneer_err:.2e} ({100*(a_pioneer_pwc/a_pioneer_obs - 1):+.2f}%, {(a_pioneer_pwc-a_pioneer_obs)/a_pioneer_err:+.2f}s)")
print(f" 7. Baryon Asymmetry (eta_B)    : f_solid^3 = {eta_B_pwc:.3e} vs Planck {eta_B_obs:.3e} +/- {eta_B_err:.2e} ({100*(eta_B_pwc/eta_B_obs - 1):+.2f}%, {(eta_B_pwc-eta_B_obs)/eta_B_err:+.2f}s)")
print(f" 8. Decompression Tail Norm eta : f_solid^3 * (s/3) = {eta_tail_norm:.4e} (closes Stage-3 eta ~ 1e-11 target)")
print(f" 9. Bulge Exhaust Retention     : (s/3)*(1 - drho_geom) = {100*f_bulge_retain:.3f}% (closes Stage-3 ~1% target)")
print(f"10. W-Boson Mass (8-Pair N=16)  : {M_W_pwc:.1f} MeV vs LHC/CMS {M_W_lhc:.1f} +/- {M_W_err:.1f} MeV ({(M_W_pwc-M_W_lhc)/M_W_err:+.2f}s)")
print(f"11. S8 Tension & High-Tc Pairing: S8 = {S8_pwc:.4f} vs DES Y6 {S8_des_y6:.3f} +/- {S8_des_err:.3f} ({(S8_pwc-S8_des_y6)/S8_des_err:+.2f}s) | Cuprate Tc = {Tc_cuprate_K:.1f} K (2Delta = {gap_2Delta_meV:.2f} meV)")
print("=" * 88)
