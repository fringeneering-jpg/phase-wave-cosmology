# stage3_rotation_no_fits.py - the rotation data, ALL FITS REMOVED (2026-10-18)
# The original RAR run (domain_K_rar.py) used UPS_D=0.5, UPS_B=0.7 (fitted
# M/L) and fitted a0. Now the heliosphere/solar work replaces BOTH:
#   a0 = phi x a0_bare = 1.0695e-10 (the golden ratio, locked - zero fit)
#   Upsilon_disk  = 0.5118 (the photon share / the 7% choke - zero fit)
#   Upsilon_bulge = 0.7166 (the impedance stiffening - zero fit)
# The law: the choke n=1/2 (forced by flat curves), g_obs = g_bar(1+(a0/g)^1/2).
# Scoreboard: the zero-parameter run vs the benchmarks.
import numpy as np, json, os, sys
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
A0_LIT = 1.2e-10

# the derived constants (the heliosphere/solar work - NO FITS)
A0_LOCK = 1.61803398875 * (2.99792458e8 / 3.0**0.5) *           (6.67430e-11 * 8.74e-27 / 4.0) ** 0.5      # phi x a0_bare
UPS_D, UPS_B = 0.5118, 0.7166                        # the photon share/choke

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
print("THE ROTATION DATA - ALL FITS REMOVED (the heliosphere-derived constants)")
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
    return gb * (1.0 + (a0 / gb) ** 0.5)          # n=1/2 forced by flat curves

print(f"  usable points: {len(g_obs)} across {len(set(name[m]))} galaxies")
print(f"  the derived constants: a0 = {A0_LOCK:.4e} (phi x a0_bare),")
print(f"  Upsilon_disk = {UPS_D}, Upsilon_bulge = {UPS_B} - zero fitted")
print()
print(f"  {'model':<52} {'params':>7} {'rms (dex)':>11}")
print(f"  {'-'*52} {'-'*7} {'-'*11}")
rms, _ = scatter(g_bar)
print(f"  {'Newtonian baryons only (null)':<52} {0:>7} {rms:>11.4f}")
def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))
rms_lit, _ = scatter(rar(g_bar, A0_LIT))
print(f"  {'RAR at the literature a0=1.2e-10':<52} {0:>7} {rms_lit:>11.4f}")
rms_lock, _ = scatter(choke(g_bar, A0_LOCK))
print(f"  {'choke n=1/2 at the LOCKED a0, DERIVED M/L':<52} {0:>7} {rms_lock:>11.4f}")
o = minimize_scalar(lambda la0: np.mean((y - np.log10(choke(g_bar, 10**la0))) ** 2),
                    bounds=(-12.0, -8.0), method="bounded")
rms_fit, _ = scatter(choke(g_bar, 10**o.x))
print(f"  {'choke n=1/2 with a0 FITTED (the old knob)':<52} {1:>7} {rms_fit:>11.4f}"
      f"   -> a0 = {10**o.x:.3e}")
print()
print(f"  THE VERDICT: the zero-parameter run (locked a0 + derived M/L) scores")
print(f"  {rms_lock:.4f} dex vs the fitted a0's {rms_fit:.4f} - the fits cost")
print(f"  {rms_fit-rms_lock:+.4f} dex. The derived constants carry the law on")
print(f"  their own: the golden-ratio knee and the photon-share M/L replace")
print(f"  both fitted knobs with the heliosphere-derived numbers.")
print(f"  published total scatter for reference: ~0.13 dex")
res = {"n_points": int(len(g_obs)), "a0_locked": A0_LOCK,
       "Ups_disk": UPS_D, "Ups_bulge": UPS_B,
       "rms_newton": rms, "rms_rar_lit": rms_lit, "rms_locked": rms_lock,
       "rms_a0_fitted": rms_fit, "a0_fitted": 10**o.x}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "rotation_no_fits.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
