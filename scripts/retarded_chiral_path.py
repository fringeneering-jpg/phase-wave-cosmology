"""
Wire_Retarded_Path.py (v2 - Corrected Chiral Log-Density Integral + Naked SPARC Check)
1. Fixes the triple-product cancellation in compute_retarded_chiral_correction
2. Uses the locked 19:1:18 axial pitch (0.2465 deg per unit d(ln rho)) + two-motion retarded shift
3. Automatically runs the -2 Fits Naked Geometric Check on probes_accel.csv if present
"""
import os
import sys
import math
from pathlib import Path
import numpy as np
from scipy.special import gamma

CANDIDATE_DIRS = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY\scripts"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC\scripts"),
    Path(r"C:\Users\jaden\cosmology\PWC\scripts"),
    Path.cwd(),
]

SCRIPTS_DIR = next((d for d in CANDIDATE_DIRS if d.exists()), Path.cwd())
print(f"[AUTO-WIRE] Target scripts directory: {SCRIPTS_DIR}")

# =====================================================================
# LOCKED PWC CONSTANTS
# =====================================================================
c0 = 2.99792458e8                                     # m/s
a0 = 6.6110e-11                                       # m/s^2 (stiffness / holding threshold)
s_debt = 1.0 / 19.0                                   # 19:1:18 axial pitch share
pitch_3d = math.sqrt(19.0 / (288.0 * math.pi ** 2))   # 0.081760 (from k_final_19_18.py)
chiral_rad_per_ln_rho = s_debt * pitch_3d             # 4.30315e-3 rad = 0.24655 deg

H_wall_kms_Mpc = 73.935                               # km/s/Mpc (locked untie rate)
Mpc_m = 3.085677581e22                                # m
H_wall_si = (H_wall_kms_Mpc * 1e3) / Mpc_m            # 2.396e-18 s^-1

# CMB / static medium observer velocity (~369.82 km/s toward Galactic l=264.02, b=48.25)
V_OBS_KMS = 369.82
L_DIPOLE_DEG, B_DIPOLE_DEG = 264.021, 48.253

# Great Attractor pole direction (Galactic l=307.0, b=9.0, bulk flow ~350 km/s)
L_GA_DEG, B_GA_DEG = 307.0, 9.0
V_GA_FLOW_KMS = 350.0

# Locked 3D Geometric Heliospheric Bloom Constants (-2 Fits)
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0    # 1.01831
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)  # +0.24306 (+24.306%)
X_GEOM = 1.5 * DELTA_RHO_GEOM                         # 0.36459


def gal_to_unit_vec(l_deg, b_deg):
    l_rad = np.radians(l_deg)
    b_rad = np.radians(b_deg)
    return np.stack([
        np.cos(b_rad) * np.cos(l_rad),
        np.cos(b_rad) * np.sin(l_rad),
        np.sin(b_rad)
    ], axis=-1)


def eq_to_gal(ra_deg, dec_deg):
    ra = np.radians(ra_deg)
    dec = np.radians(dec_deg)
    ra_gp = np.radians(192.85948)
    dec_gp = np.radians(27.12825)
    l_ncp = np.radians(122.93192)

    sin_b = np.sin(dec) * np.sin(dec_gp) + np.cos(dec) * np.cos(dec_gp) * np.cos(ra - ra_gp)
    b = np.arcsin(np.clip(sin_b, -1.0, 1.0))

    y = np.cos(dec) * np.sin(ra - ra_gp)
    x = np.sin(dec) * np.cos(dec_gp) - np.cos(dec) * np.sin(dec_gp) * np.cos(ra - ra_gp)
    l = (l_ncp - np.arctan2(y, x)) % (2.0 * np.pi)
    return np.degrees(l), np.degrees(b)


def compute_retarded_chiral_correction(ra_deg, dec_deg, z_or_dist_mpc, is_redshift=True, chirality=1.0):
    """
    Computes:
      1. Two-motion retarded shadow angle: |v_obs_perp - v_src_perp| / c0 * (1 + z_growth)
      2. Chiral diamond-lattice void birefringence: (s * pitch_3d) * d(ln rho) * |n x p_GA|
    """
    ra_arr = np.asarray(ra_deg, dtype=float)
    dec_arr = np.asarray(dec_deg, dtype=float)
    val_arr = np.asarray(z_or_dist_mpc, dtype=float)

    dist_mpc = (val_arr * (c0 * 1e-3)) / H_wall_kms_Mpc if is_redshift else val_arr
    l_deg, b_deg = eq_to_gal(ra_arr, dec_arr)
    n_obs = gal_to_unit_vec(l_deg, b_deg)

    p_dipole = gal_to_unit_vec(L_DIPOLE_DEG, B_DIPOLE_DEG)
    p_ga = gal_to_unit_vec(L_GA_DEG, B_GA_DEG)

    # 1. Untying volume / distance growth along route: (1+z) = (rho_emit/rho_obs)^(1/3)
    D0_m = dist_mpc * Mpc_m
    growth_factor = np.exp((H_wall_si * D0_m) / c0)
    d_ln_rho = 3.0 * np.log(growth_factor)  # Exact lattice log-density integral

    # 2. Two-motion retarded velocity vector (Observer CMB motion vs Source GA pole flow)
    v_obs_vec = (V_OBS_KMS * 1e3) * p_dipole
    v_src_vec = -(V_GA_FLOW_KMS * 1e3) * p_ga
    dv_rel = v_obs_vec - v_src_vec

    # Transverse component across the line of sight n_obs
    dot_dv_n = np.sum(dv_rel * n_obs, axis=-1, keepdims=True)
    dv_perp = dv_rel - dot_dv_n * n_obs
    dv_perp_mag = np.linalg.norm(dv_perp, axis=-1)

    # Observer-rotation shadow (Ruling #31, #32, #46)
    psi_observer_shadow_deg = np.degrees((dv_perp_mag / c0) * growth_factor)

    # 3. Chiral diamond-lattice void term (Ruling #27, #70, #71)
    # Driven by the 19:1:18 axial pitch across the void's log-density drop
    chiral_sin = np.linalg.norm(np.cross(n_obs, p_ga), axis=-1)
    psi_chiral_pole_deg = np.degrees(chirality * chiral_rad_per_ln_rho * (1.0 + d_ln_rho) * chiral_sin * d_ln_rho)

    psi_total_deg = psi_observer_shadow_deg + psi_chiral_pole_deg

    return {
        "dist_mpc": dist_mpc,
        "growth_factor": growth_factor,
        "d_ln_rho": d_ln_rho,
        "psi_observer_shadow_deg": psi_observer_shadow_deg,
        "psi_chiral_pole_deg": psi_chiral_pole_deg,
        "psi_total_deg": psi_total_deg,
    }


def run_naked_probes_check():
    """Finds probes_accel.csv and runs the zero-parameter / -2 fits check."""
    probe_paths = [
        SCRIPTS_DIR / "probes_accel.csv",
        Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\probes\probes_accel.csv"),
    ]
    csv_path = next((p for p in probe_paths if p.exists()), None)
    if not csv_path:
        hits = list(Path(r"C:\Users\jaden\Downloads\PWC-Check").rglob("probes_accel.csv"))
        if hits:
            csv_path = hits[0]

    if not csv_path:
        print("\n[INFO] probes_accel.csv not found in default paths; skipping PROBES run.")
        return

    import pandas as pd
    d = pd.read_csv(csv_path)
    rms_dex = lambda go, gp: float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))

    # 1. Standard derived PWC (s_shared = 0.2250, a0 = 6.611e-11)
    s_derived = 0.2250
    g_pwc_std = d.g_bar + np.sqrt(a0 * d.g_bar) * (1.0 + s_derived * d.shared * (1.0 - d.locked))

    # 2. Controlled Two-Limit Choke (x = g_bar / (18 * a0)) + Geometric Bulge Phonon Exhaust (+24.306%)
    x_choke = d.g_bar / (18.0 * a0)
    choke_gate = 1.0 / (1.0 + x_choke + (x_choke ** 2))
    # Locked bulge receives the analytic +24.306% interstitial phonon exhaust boost
    g_bar_naked = d.g_bar * (1.0 + DELTA_RHO_GEOM * d.locked)
    g_pwc_naked = g_bar_naked + np.sqrt(a0 * g_bar_naked) * (1.0 + s_derived * d.shared * (1.0 - d.locked * choke_gate))

    print("\n" + "=" * 74)
    print(f"3. PROBES 1,342 GALAXIES NAKED GEOMETRIC CHECK ({csv_path.name})")
    print("=" * 74)
    print(f"  - Analytic Gamma(1/3) Bulge Density Pack : +{DELTA_RHO_GEOM*100:.3f}% (x_geom = {X_GEOM:.5f})")
    print(f"  - Base sqrt(a0*g_bar) scatter            : {rms_dex(d.g_obs, d.g_bar + np.sqrt(a0 * d.g_bar)):.4f} dex")
    print(f"  - Derived PWC (s=0.2250) scatter         : {rms_dex(d.g_obs, g_pwc_std):.4f} dex")
    print(f"  - Naked Geometric + Choke (-2 fits)      : {rms_dex(d.g_obs, g_pwc_naked):.4f} dex")


if __name__ == "__main__":
    module_path = SCRIPTS_DIR / "retarded_chiral_path.py"
    try:
        current_code = Path(__file__).read_text(encoding="utf-8")
        if Path(__file__).resolve() != module_path.resolve():
            module_path.write_text(current_code, encoding="utf-8")
            print(f"[UPDATED] Saved corrected module to: {module_path}")
    except Exception:
        pass

    print("\n" + "=" * 74)
    print("1. DOUGLASS+ VOID CORRIDOR & CHIRAL POLE CHECK (Corrected Log-Density Integral)")
    print("=" * 74)
    corridor = compute_retarded_chiral_correction(ra_deg=146.0, dec_deg=38.5, z_or_dist_mpc=0.06, is_redshift=True)
    print(f"Frozen Top Void Corridor (RA 146.0°, Dec +38.5°, D = {float(corridor['dist_mpc']):.1f} Mpc):")
    print(f"  - Untying distance growth (1+z)  : {float(corridor['growth_factor']):.5f} (d_ln_rho = {float(corridor['d_ln_rho']):.4f})")
    print(f"  - Two-motion observer shadow     : {float(corridor['psi_observer_shadow_deg']):.4f}°")
    print(f"  - Chiral 19:1:18 lattice term    : {float(corridor['psi_chiral_pole_deg']):.4f}°")
    print(f"  - Total corridor amplitude       : {float(corridor['psi_total_deg']):.4f}° (Frozen target: ~0.15°)")

    print("\n" + "=" * 74)
    print("2. COSMIC SPRINKLER JET CURVATURE CHECK (Rulings #42, #43, #47)")
    print("=" * 74)
    for jet_kpc, d_mpc, v_host in [(1.5, 16.8, 450.0), (5.0, 100.0, 550.0)]:
        ell_m = (jet_kpc * 1e-3) * Mpc_m
        D0_m = d_mpc * Mpc_m
        v_jet = 0.92 * c0
        v_perp = v_host * 1e3
        growth_path = (H_wall_si * D0_m) / c0
        dx_kpc = (ell_m / v_jet) * v_perp * (1.0 + growth_path) / Mpc_m * 1e3
        bend_deg = math.degrees(math.atan2(dx_kpc, jet_kpc))
        print(f"  Jet L={jet_kpc:4.1f} kpc at D={d_mpc:5.1f} Mpc (v_host={v_host:.0f} km/s) -> "
              f"Tip offset = {dx_kpc*1e3:6.2f} pc ({bend_deg:.3f}° apparent curve)")

    run_naked_probes_check()