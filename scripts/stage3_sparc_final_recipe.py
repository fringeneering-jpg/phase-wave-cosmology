# stage3_sparc_final_recipe.py - the COMPLETE naked geometric recipe (2026-10-20)
# Upsilon_D = 1 - 2 drho_geom ; Upsilon_B = Upsilon_D (1 + drho_geom)
# the 2MRS acceleration choke fade: W_env = a0/(g_bar + a0)
# the law: g_obs = g_bar (1 + W_env (a0/g_bar)^(1/2)), a0 = phi x a0_bare
# Target: 0.1335 dex across 2,700 points (0.1177 bulges, bias -0.0023)
import numpy as np, json, os, sys
from scipy.special import gamma

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3

D_RHO = (1.5 * gamma(1.0/3.0) - 3.0) / (4.0 * np.pi / 3.0)
UPS_D = 1.0 - 2.0 * D_RHO
UPS_B = UPS_D * (1.0 + D_RHO)
A0 = 1.61803398875 * (2.99792458e8 / 3.0**0.5) * (6.67430e-11 * 8.74e-27 / 4.0) ** 0.5

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip():
            continue
        if "	" in l and "recno" in l:
            hdr_i = i
            break
    names = lines[hdr_i].split("	")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("	", "").strip()) <= set("- "):
            dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split("	")
        if len(f) < len(names):
            continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else
                              (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out

print("=" * 78)
print("THE COMPLETE NAKED GEOMETRIC RECIPE - verification")
print("=" * 78)
print(f"drho_geom = {D_RHO:.5f}; Upsilon_D = {UPS_D:.5f}; Upsilon_B = {UPS_B:.5f}")
print(f"a0 = {A0:.4e}; W_env = a0/(g_bar + a0)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Vflat", "Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt",
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}
name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float)
Vd = np.array(t2["Vdisk"], float)
Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb)
Vg = np.where(np.isnan(Vg), 0.0, Vg)
inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo / Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]
conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, Vb, Vd = g_obs[ok], g_bar[ok], Vb[ok], Vd[ok]
W_env = A0 / (g_bar + A0)
pred = g_bar * (1.0 + W_env * (A0 / g_bar) ** 0.5)
resid = np.log10(g_obs) - np.log10(pred)
rms_all = float(np.sqrt(np.mean(resid ** 2)))
bulge = Vb * np.abs(Vb) > Vd * np.abs(Vd)
rms_b = float(np.sqrt(np.mean(resid[bulge] ** 2))) if bulge.sum() else float("nan")
deep = g_bar < 0.2 * A0
bias = float(np.mean(resid[deep])) if deep.sum() else float("nan")
print(f"  points {len(g_obs)}: rms all = {rms_all:.4f} dex; bulge = {rms_b:.4f}; "
      f"deep bias = {bias:+.4f}")
print(f"  target: 0.1335 / 0.1177 / -0.0023")
print(f"  -> {'MATCHES' if abs(rms_all-0.1335) < 0.004 else 'DIFFERS'} "
      f"(delta {rms_all-0.1335:+.4f})")
res = {"drho_geom": D_RHO, "Ups_D": UPS_D, "Ups_B": UPS_B, "a0": A0,
       "rms_all": rms_all, "rms_bulge": rms_b, "deep_bias": bias,
       "n_points": int(len(g_obs))}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "sparc_final_recipe.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("result written:", out)
