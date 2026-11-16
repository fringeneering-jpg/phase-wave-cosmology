# stage3_rotation_new_a0.py - THE RERUN WITH THE NEW CLOSED-FORM a0 (2026-10-28)
# Last time: a0 = phi x a0_bare = 1.0695e-10 (golden-ratio knee), zero fit.
# Tonight AI Studio CLOSED the first-principles derivation: the terminal floor of
# the growing road around a closed orbit is a0 = c0 H0 / (2 pi) = 1.1432e-10.
# Same zero-fit discipline (derived Upsilon_disk/bulge replace both fitted knobs),
# same -2 Newtonian baseline, same choke n=1/2 law. Only the a0 changes - frozen.
import numpy as np, json, os, sys
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
A0_LIT = 1.2e-10

# THE NEW LOCKED a0 (the CLOSED derivation - frozen before evaluation)
C0 = 299792458.0
H0 = 73.935                      # the framework's locked H0
MPC = 3.085677581e19
A0_NEW = C0 * (H0/MPC) / (2.0*np.pi)      # = 1.1432e-10
A0_OLD = 1.61803398875 * (C0 / 3.0**0.5) * (6.67430e-11 * 8.74e-27 / 4.0) ** 0.5
UPS_D, UPS_B = 0.5118, 0.7166             # the derived M/L (zero fit, unchanged)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip():
            continue
        if "\t" in l and "recno" in l:
            hdr_i = i
            break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("\t", "").strip()) <= set("- "):
            dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split("\t")
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
print("THE RERUN - the NEW closed-form a0 = c0*H0/(2*pi) vs the old, frozen")
print("=" * 78)
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
R, Vo, eVo, Vg, Vd, Vb = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m]
conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar = g_obs[ok], g_bar[ok]
y = np.log10(g_obs)

def scatter(pred):
    r = y - np.log10(pred)
    return float(np.sqrt(np.mean(r ** 2))), float(np.std(r))

def choke(gb, a0):
    return gb * (1.0 + (a0 / gb) ** 0.5)          # n=1/2 = g_bar + sqrt(g_bar a0)

def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))

print(f"  usable points: {len(g_obs)} across {len(set(name[m & ok])) if False else 'n/a'} galaxies")
print(f"  NEW a0 = c0*H0/(2 pi) = {A0_NEW:.4e} m/s^2  (the closed-form terminal floor)")
print(f"  OLD a0 = phi x a0_bare  = {A0_OLD:.4e} m/s^2  (the golden-ratio knee)")
print()
print(f"  {'model':<52} {'params':>7} {'rms (dex)':>11}")
print(f"  {'-'*52} {'-'*7} {'-'*11}")
rms, _ = scatter(g_bar)
print(f"  {'Newtonian baryons only (-2 baseline)':<52} {0:>7} {rms:>11.4f}")
rms_lit, _ = scatter(rar(g_bar, A0_LIT))
print(f"  {'RAR at the literature a0=1.2e-10 (fitted law)':<52} {0:>7} {rms_lit:>11.4f}")
rms_old, _ = scatter(choke(g_bar, A0_OLD))
print(f"  {'choke n=1/2 at the OLD a0 (1.0695e-10)':<52} {0:>7} {rms_old:>11.4f}")
rms_new, _ = scatter(choke(g_bar, A0_NEW))
print(f"  {'choke n=1/2 at the NEW a0 (1.1432e-10)':<52} {0:>7} {rms_new:>11.4f}")
rms_new_rar, _ = scatter(rar(g_bar, A0_NEW))
print(f"  {'RAR form at the NEW a0 (1.1432e-10)':<52} {0:>7} {rms_new_rar:>11.4f}")
o = minimize_scalar(lambda la0: np.mean((y - np.log10(choke(g_bar, 10**la0))) ** 2),
                    bounds=(-12.0, -8.0), method="bounded")
rms_fit, _ = scatter(choke(g_bar, 10**o.x))
print(f"  {'choke n=1/2 with a0 FITTED (reference knob)':<52} {1:>7} {rms_fit:>11.4f}"
      f"   -> a0 = {10**o.x:.3e}")
print()
print(f"  THE VERDICT:")
print(f"  * new locked a0: {rms_new:.4f} dex  (old locked: {rms_old:.4f}, lit RAR: {rms_lit:.4f})")
print(f"  * the new closed-form a0 {'BEATS' if rms_new < rms_old else 'does not beat'} the old")
print(f"    golden-ratio knee by {abs(rms_new-rms_old):.4f} dex, and sits "
      f"{abs(rms_new-rms_lit):.4f} dex from the literature-RAR line.")
print(f"  * published total scatter for reference: ~0.13 dex")
res = {"n_points": int(len(g_obs)), "a0_new": A0_NEW, "a0_old": A0_OLD,
       "rms_newton": rms, "rms_rar_lit": rms_lit, "rms_old": rms_old,
       "rms_new": rms_new, "rms_new_rar": rms_new_rar, "rms_fitted": rms_fit,
       "a0_fitted": 10**o.x}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "rotation_new_a0.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
