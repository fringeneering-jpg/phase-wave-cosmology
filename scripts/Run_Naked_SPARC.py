"""
Run_Naked_SPARC.py (v3)
1. Tests the -1 Fit and -2 Fits Naked Geometric Heliospheric Bulge Exhaust
   directly on the 149 SPARC galaxies (2,700 quality-cut points).
2. Inspects and runs whim_shared_sparc.py with the locked Gamma(1/3) constants.
"""
import sys
import math
from pathlib import Path
import numpy as np
from scipy.special import gamma

SPARC_DIR = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
sys.path.insert(0, SPARC_DIR)
from domain_K_rar import read_vizier_tsv, KPC, KMS, UPS_D, UPS_B

# =====================================================================
# LOCKED PWC & 3D GEOMETRIC CONSTANTS (Zero Free Fits)
# =====================================================================
a0 = 6.6110e-11
s_derived = 0.2250        # Derived mist ram: (3/2)*3*0.05
s_locked  = 0.22650       # Value in two_limit_choke.py

# Analytic 3D surface-to-volume Gamma(1/3) heliospheric bloom integral
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0        # 1.01831
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)   # +0.24306 (+24.306%)
X_GEOM = 1.5 * DELTA_RHO_GEOM                             # 0.36459

# 1. Load SPARC exactly as in two_limit_choke.py
t1 = read_vizier_tsv(f"{SPARC_DIR}/vizier_t1.txt", ["Name", "i", "Qual", "Vflat", "Dist"])
t2 = read_vizier_tsv(f"{SPARC_DIR}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.where(np.isnan(np.array(t2["Vgas"], float)), 0.0, np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float))

inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS ** 2) / KPC
g_obs = (Vo ** 2) / R * conv


def evaluate_sparc(ups_d, ups_b, s_val, label):
    Vbar2 = Vg * np.abs(Vg) + ups_d * Vd * np.abs(Vd) + ups_b * Vb * np.abs(Vb)
    g_bar = Vbar2 / R * conv
    ok = (g_bar > 0) & (g_obs > 0)
    go, gb, r_ok, vb_ok, vbar2_ok, n_ok = g_obs[ok], g_bar[ok], R[ok], Vb[ok], Vbar2[ok], name[ok]

    locked = np.clip(ups_b * vb_ok * np.abs(vb_ok) / np.maximum(vbar2_ok, 1e-30), 0.0, 1.0)
    shared = np.zeros_like(gb)
    for n in set(n_ok):
        sel = n_ok == n
        Mb = vbar2_ok[sel] * r_ok[sel]
        shared[sel] = np.clip(1.0 - Mb / Mb.max(), 0.0, 1.0)

    g_c = 18.0 * a0
    x = gb / g_c
    f_series = 1.0 / (1.0 + x + (x ** 2))
    boost = 1.0 + s_val * shared * (1.0 - locked)
    g_pred = gb + np.sqrt(a0 * gb) * boost * f_series

    rms_all = float(np.sqrt(np.mean((np.log10(go) - np.log10(g_pred)) ** 2)))
    bulge_mask = np.abs(vb_ok) > 0
    rms_bulge = float(np.sqrt(np.mean((np.log10(go[bulge_mask]) - np.log10(g_pred[bulge_mask])) ** 2)))
    return rms_all, rms_bulge, int(np.sum(bulge_mask))


print("=" * 78)
print("1. SPARC 149 GALAXIES: STANDARD M/L vs NAKED GEOMETRIC PHONON EXHAUST")
print("=" * 78)
print(f"Locked Gamma(1/3) Bulge Phonon Density Pack : +{DELTA_RHO_GEOM * 100:.3f}%")
print(f"Standard SPARC Empirical Bulge M/L          : UPS_D = {UPS_D:.4f}, UPS_B = {UPS_B:.4f}")

# Case 1: Original two_limit_choke.py (UPS_D = 0.5, UPS_B = 0.7)
rms1, b_rms1, n_b = evaluate_sparc(0.5, 0.7, s_locked, "Standard (0.5 / 0.7)")

# Case 2: -1 Fit (Rip out empirical 0.7 bulge M/L; lock bulge to Disk * (1 + delta_rho_geom) = 0.6215)
ups_b_geom = 0.5 * (1.0 + DELTA_RHO_GEOM)
rms2, b_rms2, _ = evaluate_sparc(0.5, ups_b_geom, s_derived, "Naked Bulge (-1 fit)")

# Case 3: -2 Fits (Both disk and bulge M/L locked from 3D geometry: ups_d = 1 - 2*delta_rho_geom = 0.5139)
ups_d_geom = 1.0 - 2.0 * DELTA_RHO_GEOM
ups_b_geom2 = ups_d_geom * (1.0 + DELTA_RHO_GEOM)
rms3, b_rms3, _ = evaluate_sparc(ups_d_geom, ups_b_geom2, s_derived, "Full Naked (-2 fits)")

print(f"\n{'Configuration':42s} | {'UPS_D':>6s} | {'UPS_B':>6s} | {'All 2700':>9s} | {'Bulge ({n_b} pts)':>14s}")
print("-" * 78)
print(f"{'1. Standard SPARC M/L (0.50 / 0.70)':42s} | {0.5000:6.4f} | {0.7000:6.4f} | {rms1:9.4f} | {b_rms1:14.4f}")
print(f"{'2. Geometric Bulge Pack (-1 Fit, +24.31%)':42s} | {0.5000:6.4f} | {ups_b_geom:6.4f} | {rms2:9.4f} | {b_rms2:14.4f}")
print(f"{'3. Full Geometric M/L (-2 Fits, 0 params)':42s} | {ups_d_geom:6.4f} | {ups_b_geom2:6.4f} | {rms3:9.4f} | {b_rms3:14.4f}")

# 2. Inspect whim_shared_sparc.py to wire the 2MRS WHIM outer load
whim_file = Path(r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\whim_shared_sparc.py")
if whim_file.exists():
    print("\n" + "=" * 78)
    print(f"2. INSPECTING {whim_file}:")
    print("=" * 78)
    print(whim_file.read_text(encoding="utf-8", errors="ignore"))   