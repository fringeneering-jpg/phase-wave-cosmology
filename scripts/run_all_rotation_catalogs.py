"""
run_all_rotation_catalogs.py
Head-to-head across ALL four rotation catalogs on disk:
  PROBES 1,342 spirals | ALFALFA 331 gas | GHASP 81 | LITTLE THINGS 16
under the zero-parameter derived & naked geometric recipes.
"""
import math, os, subprocess, sys
import numpy as np
import pandas as pd
from scipy.special import gamma

SPARC_DIR = r"C:\Users\jaden\cosmology\sparc"
VENV_PY = r"C:\Users\jaden\Downloads\PWC-Check\PWC\.venv-solar\Scripts\python.exe"

# ---------------- locked constants ----------------
c0 = 2.99792458e8
hbar = 1.054571817e-34
rho0 = 8.74e-27
Rp = 8.414e-16
s_fold = 1.0 / 19.0
f_solid = 8.4989e-4
phi = (1.0 + math.sqrt(5.0)) / 2.0
G_chain = (f_solid ** 12) * (4.0 * s_fold / 81.0) * (Rp ** 2) * (c0 ** 3) / hbar
a0_bare = (c0 / math.sqrt(3.0)) * math.sqrt(G_chain * rho0 / 4.0)
a0_knee = phi * a0_bare
s_derived = 0.2250
s_legacy_fit = 0.2264
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)
UPS_D_LOCKED = 0.51375
UPS_B_LOCKED = 0.63865

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
    if "g_gas" in df.columns and "g_disk" in df.columns:
        g_gas = df["g_gas"].values.astype(float)
        g_disk05 = df["g_disk"].values.astype(float)
        g_bul07 = df["g_bulge"].values.astype(float) if "g_bulge" in df.columns else gb * lk
        gb_naked = g_gas + (UPS_D_LOCKED / 0.50) * g_disk05 + (UPS_B_LOCKED / 0.70) * g_bul07
    else:
        gb_naked = gb * ((1.0 - lk) * (UPS_D_LOCKED / 0.50) + lk * (UPS_B_LOCKED / 0.70))
    a0_rar = 1.20e-10
    gp_rar_emp = gb / (1.0 - np.exp(-np.sqrt(np.maximum(gb / a0_rar, 1e-30))))
    gp_base = gb + np.sqrt(a0_bare * gb)
    gp_legacy = gb + np.sqrt(a0_bare * gb) * (1.0 + s_legacy_fit * sh * (1.0 - lk))
    gp_derived = gb + np.sqrt(a0_bare * gb) * (1.0 + s_derived * sh * (1.0 - lk))
    gp_naked_shared = gb_naked + np.sqrt(a0_bare * gb_naked) * (1.0 + s_derived * sh * (1.0 - lk))
    env_whim = 0.5
    accel_fade = a0_bare / (gb_naked + a0_bare)
    sh_whim = np.clip(sh + env_whim * accel_fade * (1.0 - sh), 0.0, 1.0)
    x_choke = gb_naked / (18.0 * a0_bare)
    f_coupled = 1.0 / (1.0 + x_choke + (x_choke ** 2))
    gp_naked_whim = gb_naked + np.sqrt(a0_bare * gb_naked) * (1.0 + s_derived * sh_whim * (1.0 - lk)) * f_coupled
    w_env = a0_knee / (gb_naked + a0_knee)
    gp_stage3 = gb_naked * (1.0 + w_env * np.sqrt(a0_knee / gb_naked))
    models = [
        ("McGaugh RAR (fitted)", gp_rar_emp),
        ("Base sqrt(a0*g_bar) s=0", gp_base),
        ("Legacy PWC fitted s=0.2264", gp_legacy),
        ("Derived PWC s=0.2250 (0-fit)", gp_derived),
        ("Naked Geometric -2 Fits", gp_naked_shared),
        ("Naked + WHIM + 18a0 Choke", gp_naked_whim),
        ("Stage-3 phi*a0 W_env Fade", gp_stage3),
    ]
    rows = []
    for m_name, gp in models:
        rows.append((m_name, rms_gal_balanced(names, go, gp), rms_point(go, gp)))
    print(f"\n--- {label} (N_gal = {names.nunique()}, N_pts = {len(df)}) ---")
    print(f"{'Model Pipeline':38s} | {'Gal-Bal':>8s} | {'Point':>8s}")
    print("-" * 62)
    for m_name, gb_rms, pt_rms in rows:
        print(f"{m_name:38s} | {gb_rms:8.4f} | {pt_rms:8.4f}")
    return rows

# ---------------- 1. PROBES ----------------
probes = r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\probes\probes_accel.csv"
d = pd.read_csv(probes)
rows_probes = score_dataset(d, "PROBES 1,342")

# ---------------- 2. GHASP ----------------
gh = pd.read_csv(os.path.join(SPARC_DIR, "ghasp", "ghasp_accel.csv"))
gh["Name"] = gh["Name"].astype(str)
rows_ghasp = score_dataset(gh, "GHASP 81")

# ---------------- 3. LITTLE THINGS (replicate the blind loader) ----------------
os.chdir(SPARC_DIR)
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("model = lambda")[0])
cols = [(0, 8), (9, 14), (15, 23), (24, 34), (35, 44), (45, 54), (55, 63)]
names = ["Name", "Type", "R03", "V03", "R", "V", "eV"]
tot = pd.read_fwf("littlethings/lt_rotdmbar.dat", colspecs=cols, names=names)
dm = pd.read_fwf("littlethings/lt_rotdm.dat", colspecs=cols, names=names)
tot, dm = tot[tot.Type == "Data"], dm[dm.Type == "Data"]
EXCL = {"DDO_50", "DDO_87", "DDO_126", "DDO_154", "DDO_168", "NGC_2366"}
out = []
for n, t in tot.groupby("Name"):
    if n in EXCL: continue
    dd = dm[dm.Name == n]
    if dd.empty: continue
    t = t.sort_values("R"); dd = dd.sort_values("R")
    R = t.R.values * t.R03.values; Vt = t.V.values * t.V03.values
    Rd = dd.R.values * dd.R03.values; Vdd = dd.V.values * dd.V03.values
    Vd = np.interp(R, Rd, Vdd, left=np.nan, right=np.nan)
    vb2 = Vt ** 2 - Vd ** 2; ok = np.isfinite(vb2) & (vb2 > 0) & (R > 0) & (Vt > 0)
    R, Vt, vb2 = R[ok], Vt[ok], vb2[ok]
    if len(R) < 3: continue
    gb = vb2 / R
    M = np.maximum(gb * R ** 2 / G, 0); dmr = np.clip(np.diff(np.concatenate([[0.0], M])), 0, None)
    a = np.concatenate([[R[0] / 2], (R[1:] + R[:-1]) / 2])
    gin = np.array([-ring_gr(r, a, dmr)[a < r].sum() for r in R])
    gout = np.array([ring_gr(r, a, dmr)[a > r].sum() for r in R])
    shared = np.clip(np.minimum(gin, gout) / gin, 0, 1)
    go, gbs = Vt ** 2 / R * CONV, gb * CONV
    for Ri, goi, gbi, si in zip(R, go, gbs, shared):
        out.append(dict(Name=n, g_obs=goi, g_bar=gbi, shared=float(si), locked=0.0))
lt = pd.DataFrame(out)
rows_lt = score_dataset(lt, "LITTLE THINGS 16")

# ---------------- 4. ALFALFA gas (build from D:/probes) ----------------
gas_out = os.path.join(SPARC_DIR, "alfalfa_gas_accel.csv")
r = subprocess.run([VENV_PY, "probes_gas_build.py", "0.5", "gas", gas_out],
                   cwd=SPARC_DIR, capture_output=True, text=True)
print("\n--- ALFALFA GAS BUILD ---")
print((r.stdout or "")[-1200:])
if r.returncode != 0:
    print("GAS BUILD STDERR:", (r.stderr or "")[-800:])
    rows_gas = None
else:
    g = pd.read_csv(gas_out)
    g["Name"] = g["Name"].astype(str)
    rows_gas = score_dataset(g, "ALFALFA 331 (gas)")

# ---------------- combined summary ----------------
print("\n" + "=" * 62)
print("COMBINED GAL-BALANCED RMS (same metric, same 8 pipelines, all catalogs)")
print("=" * 62)
labels = ["PROBES 1342", "ALFALFA 331", "GHASP 81", "LITTLE THINGS 16"]
sets = [rows_probes, rows_gas, rows_ghasp, rows_lt]
hdr = f"{'Pipeline':38s}"
for L in labels:
    hdr += f" | {L:>10s}"
print(hdr)
for i, m_name in enumerate(rows_probes):
    line = f"{m_name[0]:38s}"
    for rows in sets:
        if rows is None:
            line += f" | {'n/a':>10s}"
        else:
            line += f" | {rows[i][1]:10.4f}"
    print(line)
