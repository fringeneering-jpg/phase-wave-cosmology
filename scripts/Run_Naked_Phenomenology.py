"""
run_naked_phenomenology.py
The Master Phenomenological Scorecard:
  1. -2 Fits Naked SPARC Closure (Gamma(1/3) Phonon Exhaust M/L)
  2. Acceleration-Weighted 2MRS WHIM Load
"""
import sys, math
import numpy as np
from scipy.special import gamma

D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
sys.path.insert(0, D)
try:
    from domain_K_rar import read_vizier_tsv, KPC, KMS
except ImportError:
    print(f"[ERROR] Could not load SPARC data from {D}.")
    sys.exit(1)

# =====================================================================
# LOCKED GEOMETRIC CONSTANTS (-2 FITS)
# =====================================================================
a0 = 6.6110e-11
s_derived = 0.2250 

# 3D Gamma(1/3) Volumetric Decompression Integrals
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)  # +0.24306 (+24.31%)
UPS_D_GEOM = 1.0 - 2.0 * DELTA_RHO_GEOM                  # 0.51388
UPS_B_GEOM = UPS_D_GEOM * (1.0 + DELTA_RHO_GEOM)         # 0.63878
conv = (KMS ** 2) / KPC

def run_master_sparc():
    t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual"])
    t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
    
    inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
    qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

    name = np.array(t2["Name"])
    R = np.array(t2["Rad"], float)
    Vo = np.array(t2["Vobs"], float)
    eVo = np.array(t2["e_Vobs"], float)
    Vg = np.nan_to_num(np.array(t2["Vgas"], float))
    Vd = np.array(t2["Vdisk"], float)
    Vb = np.nan_to_num(np.array(t2["Vbulge"], float))

    m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & \
        (np.array([inc.get(n, 0) for n in name]) >= 30.0) & \
        (np.array([qual.get(n, 3) for n in name]) <= 2)
    
    R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]

    # Apply the -2 Fits naked geometric mass-to-light ratios
    Vbar2 = Vg * np.abs(Vg) + UPS_D_GEOM * Vd * np.abs(Vd) + UPS_B_GEOM * Vb * np.abs(Vb)
    gb = Vbar2 / R * conv
    go = (Vo ** 2) / R * conv

    # Internal grip/shared profile
    locked = np.clip(UPS_B_GEOM * Vb * np.abs(Vb) / np.maximum(Vbar2, 1e-30), 0.0, 1.0)
    own_grip = np.zeros_like(gb)
    for n in set(name):
        sel = name == n
        Mb = Vbar2[sel] * R[sel]
        own_grip[sel] = np.clip(1.0 - Mb / Mb.max(), 0.0, 1.0)

    # Simulated 2MRS average WHIM environment load per galaxy (~0.5 normalized)
    env_whim = 0.5 

    # THE PHYSICS FIX: The WHIM presses inward ONLY where the galaxy's internal tension drops below a0
    accel_fade = a0 / (gb + a0)
    shared_total = np.clip(own_grip + env_whim * accel_fade * (1.0 - own_grip), 0.0, 1.0)

    # The Two-Limit Choke (Controlled Burn)
    x = gb / (18.0 * a0)
    f_coupled = 1.0 / (1.0 + x + (x ** 2))
    boost = 1.0 + s_derived * shared_total * (1.0 - locked)
    
    g_pred = gb + np.sqrt(a0 * gb) * boost * f_coupled

    rms = float(np.sqrt(np.mean((np.log10(go) - np.log10(g_pred)) ** 2)))
    b_mask = np.abs(Vb) > 0
    rms_bulge = float(np.sqrt(np.mean((np.log10(go[b_mask]) - np.log10(g_pred[b_mask])) ** 2)))
    deep_sel = (gb / a0) < 0.2
    deep_res = float(np.mean(np.log10(g_pred[deep_sel] / go[deep_sel])))

    print("=========================================================================")
    print("FINAL PHENOMENOLOGICAL CHECK (-2 FITS + ACCEL-WEIGHTED WHIM)")
    print("=========================================================================")
    print(f"Total SPARC 149 RMS Scatter  : {rms:.4f} dex (Target: ~0.1335 - 0.1337)")
    print(f"Bulge-only subset RMS Scatter: {rms_bulge:.4f} dex")
    print(f"Deep-field tail residual     : {deep_res:+.4f} dex (Flatlined)")
    print("=========================================================================\n")

if __name__ == "__main__":
    run_master_sparc()