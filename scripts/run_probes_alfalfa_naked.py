"""
run_probes_alfalfa_naked.py
Evaluates the 1,342 PROBES spirals + 331 ALFALFA gas galaxies (and any companion
rotation catalogs on disk) under the zero-parameter derived & naked geometric recipes.
"""
import math, os, glob
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import gamma

# =====================================================================
# LOCKED PWC GEOMETRIC CONSTANTS (ZERO FITTED PARAMETERS)
# =====================================================================
c0 = 2.99792458e8
hbar = 1.054571817e-34
rho0 = 8.74e-27
Rp = 8.414e-16
s_fold = 1.0 / 19.0
f_solid = 8.4989e-4
phi = (1.0 + math.sqrt(5.0)) / 2.0

# Step-by-step G -> a0 chain
G_chain = (f_solid ** 12) * (4.0 * s_fold / 81.0) * (Rp ** 2) * (c0 ** 3) / hbar
a0_bare = (c0 / math.sqrt(3.0)) * math.sqrt(G_chain * rho0 / 4.0)  # 6.6110e-11 m/s^2
a0_knee = phi * a0_bare                                            # 1.0695e-10 m/s^2
s_derived = 0.2250                                                 # (3/2) * 3 * 0.05 mist ram
s_legacy_fit = 0.2264                                              # retired fitted value

# 3D Gamma(1/3) Volumetric Decompression Integrals (-2 Fits Naked M/L)
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)            # +0.24306 (+24.31%)
UPS_D_GEOM = 1.0 - 2.0 * DELTA_RHO_GEOM                            # 0.51388 (locked 0.51375)
UPS_B_GEOM = UPS_D_GEOM * (1.0 + DELTA_RHO_GEOM)                   # 0.63878 (locked 0.63865)

UPS_D_LOCKED = 0.51375
UPS_B_LOCKED = 0.63865

# Locate probes_accel.csv and any companion files (ALFALFA, GHASP, LITTLE THINGS)
candidates = [
    r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\probes\probes_accel.csv",
    r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\probes_accel.csv",
    r"C:\Users\jaden\Downloads\PWC-Check\PWC\scripts\probes_accel.csv",
]
csv_path = next((p for p in candidates if os.path.exists(p)), None)
if not csv_path:
    raise FileNotFoundError("Could not find probes_accel.csv")

d = pd.read_csv(csv_path)
print("=" * 82)
print(f"LOADED: {csv_path}")
print(f"Rows: {len(d):,} | Galaxies: {d['Name'].nunique():,} | Columns: {list(d.columns)}")
print("=" * 82)

def rms_point(go, gp):
    return float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))

def rms_gal_balanced(df_names, go, gp):
    res2 = (np.log10(go) - np.log10(gp)) ** 2
    s = pd.Series(res2).groupby(df_names.values).mean()
    return float(np.sqrt(s.mean()))

def score_dataset(df, label):
    go = df["g_obs"].values.astype(float)
    gb = df["g_bar"].values.astype(float)
    sh = df["shared"].values.astype(float) if "shared" in df.columns else np.zeros_like(gb)
    lk = df["locked"].values.astype(float) if "locked" in df.columns else np.zeros_like(gb)
    names = df["Name"]

    # Reconstruct Naked Geometric g_bar (-2 Fits: Disk 0.50 -> 0.51375, Bulge 0.70 -> 0.63865)
    if "g_gas" in df.columns and "g_disk" in df.columns:
        g_gas = df["g_gas"].values.astype(float)
        g_disk05 = df["g_disk"].values.astype(float)
        g_bul07 = df["g_bulge"].values.astype(float) if "g_bulge" in df.columns else gb * lk
        gb_naked = g_gas + (UPS_D_LOCKED / 0.50) * g_disk05 + (UPS_B_LOCKED / 0.70) * g_bul07
    else:
        # Scale disk (1 - locked) from M/L 0.50 -> 0.51375 and bulge (locked) from 0.70 -> 0.63865
        gb_naked = gb * ((1.0 - lk) * (UPS_D_LOCKED / 0.50) + lk * (UPS_B_LOCKED / 0.70))

    # 1. McGaugh RAR (a0 = 1.20e-10 literature)
    a0_rar = 1.20e-10
    gp_rar_emp = gb / (1.0 - np.exp(-np.sqrt(np.maximum(gb / a0_rar, 1e-30))))
    gp_rar_nak = gb_naked / (1.0 - np.exp(-np.sqrt(np.maximum(gb_naked / a0_rar, 1e-30))))

    # 2. Base sqrt(a0_bare * g_bar) (0 params, s = 0)
    gp_base = gb + np.sqrt(a0_bare * gb)

    # 3. Legacy Fitted s_shared = 0.2264 (M/L 0.50)
    gp_legacy = gb + np.sqrt(a0_bare * gb) * (1.0 + s_legacy_fit * sh * (1.0 - lk))

    # 4. Zero-Param Derived s_derived = 0.2250 (M/L 0.50)
    gp_derived = gb + np.sqrt(a0_bare * gb) * (1.0 + s_derived * sh * (1.0 - lk))

    # 5. Naked Geometric (-2 Fits: UPS_D=0.51375, UPS_B=0.63865, s_derived=0.2250, a0_bare)
    gp_naked_shared = gb_naked + np.sqrt(a0_bare * gb_naked) * (1.0 + s_derived * sh * (1.0 - lk))

    # 6. Naked + Controlled Burn + W_env Acceleration Fade
    env_whim = 0.5
    accel_fade = a0_bare / (gb_naked + a0_bare)
    sh_whim = np.clip(sh + env_whim * accel_fade * (1.0 - sh), 0.0, 1.0)
    x_choke = gb_naked / (18.0 * a0_bare)
    f_coupled = 1.0 / (1.0 + x_choke + (x_choke ** 2))
    gp_naked_whim = gb_naked + np.sqrt(a0_bare * gb_naked) * (1.0 + s_derived * sh_whim * (1.0 - lk)) * f_coupled

    # 7. Stage-3 W_env Recipe (a0 = phi * a0_bare = 1.0695e-10, W_env = a0 / (gb + a0))
    w_env = a0_knee / (gb_naked + a0_knee)
    gp_stage3 = gb_naked * (1.0 + w_env * np.sqrt(a0_knee / gb_naked))

    models = [
        ("McGaugh RAR (M/L 0.50, a0=1.2e-10)", gp_rar_emp),
        ("McGaugh RAR (Naked M/L 0.5138)",     gp_rar_nak),
        ("Base sqrt(a0*g_bar) (s=0)",          gp_base),
        ("Legacy PWC (fitted s=0.2264)",       gp_legacy),
        ("Derived PWC (0-fit, s=0.2250)",      gp_derived),
        ("Naked Geometric (-2 Fits, s=0.2250)",gp_naked_shared),
        ("Naked + WHIM + 18a0 Choke (-2 Fits)",gp_naked_whim),
        ("Stage-3 phi*a0 W_env Fade (-2 Fits)",gp_stage3),
    ]

    print(f"\n--- {label} (N_gal = {names.nunique()}, N_pts = {len(df)}) ---")
    print(f"{'Model Pipeline':40s} | {'Gal-Balanced RMS':>16s} | {'Point RMS':>10s}")
    print("-" * 74)
    for m_name, gp in models:
        gb_rms = rms_gal_balanced(names, go, gp)
        pt_rms = rms_point(go, gp)
        print(f"{m_name:40s} | {gb_rms:16.4f} | {pt_rms:10.4f}")

score_dataset(d, "FULL PROBES CATALOG")

# Check for gas / ALFALFA columns or companion CSVs/scripts in the repo
for col in d.columns:
    if col not in ["Name", "R", "Rad", "g_obs", "g_bar", "shared", "locked"]:
        print(f"Extra column detected in probes_accel.csv: {col}")

search_roots = [
    r"C:\Users\jaden\Downloads\PWC-Check",
    r"C:\Users\jaden\cosmology",
]
found_files = []
for sr in search_roots:
    if os.path.exists(sr):
        for root, _, files in os.walk(sr):
            for f in files:
                fl = f.lower()
                if any(k in fl for k in ["probes", "alfalfa", "ghasp", "little", "jaden_probes"]):
                    found_files.append(os.path.join(root, f))

print("\n" + "=" * 82)
print("DISCOVERED PROBES / ALFALFA / ROTATION FILES ON DISK:")
print("=" * 82)
for ff in sorted(set(found_files)):
    print(" ", ff)
