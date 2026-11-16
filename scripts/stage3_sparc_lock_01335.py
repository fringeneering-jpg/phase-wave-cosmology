# stage3_sparc_lock_01335.py - verify the claimed 0.1335 naked geometric run
# The law: raw Upsilon=1 velocities, the bulge boosted by (1 + drho_geom)
# with drho_geom = [(3/2)Gamma(1/3) - 3] / (4pi/3) = +24.306%; the choke
# n=1/2 with a0 = phi x a0_bare (the golden-ratio knee). Nothing fitted.
import numpy as np, json, os, sys
from scipy.special import gamma

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3

D_RHO_GEOM = (1.5 * gamma(1.0 / 3.0) - 3.0) / (4.0 * np.pi / 3.0)
A0_LOCK = 1.61803398875 * (2.99792458e8 / 3.0**0.5) *           (6.67430e-11 * 8.74e-27 / 4.0) ** 0.5

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
print("THE NAKED GEOMETRIC M/L LOCK - the claimed 0.1335, verified")
print("=" * 78)
print(f"drho_geom = {D_RHO_GEOM:.5f} ; a0_locked = {A0_LOCK:.4e}")
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
Vbar2 = Vg * np.abs(Vg) + Vd * np.abs(Vd) + (1.0 + D_RHO_GEOM) * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, Vb, Vd, R = g_obs[ok], g_bar[ok], Vb[ok], Vd[ok], R[ok]
pred = g_bar * (1.0 + (A0_LOCK / g_bar) ** 0.5)
resid = np.log10(g_obs) - np.log10(pred)
rms_all = float(np.sqrt(np.mean(resid ** 2)))
bulge = Vb * np.abs(Vb) > Vd * np.abs(Vd)
rms_bulge = float(np.sqrt(np.mean(resid[bulge] ** 2))) if bulge.sum() else float("nan")
print(f"  points: {len(g_obs)}; rms (all) = {rms_all:.4f} dex; "
      f"rms (bulge-dominated) = {rms_bulge:.4f} dex")
print(f"  claimed: 0.1335 dex across 2,700 points (0.1192 dex on the bulges)")
print(f"  -> {'MATCH' if abs(rms_all-0.1335)<0.005 else 'DIFFERS'} "
      f"(delta {rms_all-0.1335:+.4f} dex)")
res = {"drho_geom": D_RHO_GEOM, "a0_locked": A0_LOCK,
       "n_points": int(len(g_obs)), "rms_all": rms_all,
       "rms_bulge": rms_bulge, "n_bulge": int(bulge.sum())}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "sparc_lock_01335.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("result written:", out)
