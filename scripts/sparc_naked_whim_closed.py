import sys
from pathlib import Path
import numpy as np
from scipy.special import gamma

D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
sys.path.insert(0, D)
from domain_K_rar import read_vizier_tsv, KPC, KMS

a0 = 6.6110e-11
s_derived = 0.2250
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * np.pi) / 3.0)
UPS_D_GEOM = 1.0 - 2.0 * DELTA_RHO_GEOM
UPS_B_GEOM = UPS_D_GEOM * (1.0 + DELTA_RHO_GEOM)

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Vflat", "Dist", "_RA", "_DE"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

name_all = np.array(t2["Name"])
R_all = np.array(t2["Rad"], float)
Vo_all = np.array(t2["Vobs"], float)
eVo_all = np.array(t2["e_Vobs"], float)
Vg_all = np.where(np.isnan(np.array(t2["Vgas"], float)), 0.0, np.array(t2["Vgas"], float))
Vd_all = np.array(t2["Vdisk"], float)
Vb_all = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float))

inc_a = np.array([inc.get(n, np.nan) for n in name_all], float)
qual_a = np.array([qual.get(n, np.nan) for n in name_all], float)
m = (R_all > 0) & (Vo_all > 0) & np.isfinite(eVo_all) & (eVo_all / Vo_all <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R_cut, Vo_cut, Vg_cut, Vd_cut, Vb_cut, name_cut = R_all[m], Vo_all[m], Vg_all[m], Vd_all[m], Vb_all[m], name_all[m]
conv = (KMS ** 2) / KPC

def parse_2mrs(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = next(i for i, l in enumerate(lines) if l.startswith("RAJ2000"))
    names = lines[hdr_i].split("\t")
    idx = {c: names.index(c) for c in ["RAJ2000", "DEJ2000", "cz"]}
    ra, de, cz = [], [], []
    for l in lines[hdr_i + 1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            v = f[idx["cz"]].strip()
            if v in ("", "---"): continue
            ra.append(float(f[idx["RAJ2000"]].strip()))
            de.append(float(f[idx["DEJ2000"]].strip()))
            cz.append(float(v))
        except ValueError: continue
    return np.array(ra), np.array(de), np.array(cz)

ra2, de2, cz2 = parse_2mrs(f"{D}/2mrs.txt")
d2 = cz2 / 73.935

gal_names = sorted(set(name_cut))
ra1 = np.array([t1["_RA"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)
de1 = np.array([t1["_DE"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)
d1 = np.array([t1["Dist"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)

ra1r, de1r = np.deg2rad(ra1), np.deg2rad(de1)
ra2r, de2r = np.deg2rad(ra2), np.deg2rad(de2)
shared_env_raw = {}
for k, n in enumerate(gal_names):
    if not (np.isfinite(ra1[k]) and np.isfinite(d1[k])):
        shared_env_raw[n] = 0.0
        continue
    ca = np.clip(np.sin(de1r[k]) * np.sin(de2r) + np.cos(de1r[k]) * np.cos(de2r) * np.cos(ra1r[k] - ra2r), -1.0, 1.0)
    sep = np.arccos(ca) * d1[k]
    shared_env_raw[n] = int(((sep < 5.0) & (np.abs(d2 - d1[k]) < 6.0)).sum())

vals = np.array([shared_env_raw[n] for n in gal_names], float)
n_scale = 2.0 * np.median(vals[vals > 0]) if (vals > 0).any() else 1.0
shared_env = {n: min(1.0, v / n_scale) for n, v in zip(gal_names, vals)}

def run_whim_pipeline(ups_d, ups_b, s_val):
    g_obs = (Vo_cut ** 2) / R_cut * conv
    Vbar2 = Vg_cut * np.abs(Vg_cut) + ups_d * Vd_cut * np.abs(Vd_cut) + ups_b * Vb_cut * np.abs(Vb_cut)
    g_bar = Vbar2 / R_cut * conv
    ok = (g_bar > 0) & (g_obs > 0)
    go, gb, r_ok, vb_ok, vbar2_ok, n_ok = g_obs[ok], g_bar[ok], R_cut[ok], Vb_cut[ok], Vbar2[ok], name_cut[ok]

    locked = np.clip(ups_b * vb_ok * np.abs(vb_ok) / np.maximum(vbar2_ok, 1e-30), 0.0, 1.0)
    shared_no_whim = np.zeros_like(gb)
    shared_whim_flat = np.zeros_like(gb)
    shared_whim_smooth = np.zeros_like(gb)

    for n in set(n_ok):
        sel = n_ok == n
        Mb = vbar2_ok[sel] * r_ok[sel]
        own = np.clip(1.0 - Mb / Mb.max(), 0.0, 1.0)
        env = shared_env.get(n, 0.0)
        shared_no_whim[sel] = own
        shared_whim_flat[sel] = np.clip(own + env * (1.0 - own), 0.0, 1.0)
        r_norm = r_ok[sel] / r_ok[sel].max()
        shared_whim_smooth[sel] = np.clip(own + env * r_norm * (1.0 - own), 0.0, 1.0)

    x = gb / (18.0 * a0)
    f_coupled = 1.0 / (1.0 + x + (x ** 2))
    y = np.log10(go)
    rms = lambda pred: float(np.sqrt(np.mean((y - np.log10(pred)) ** 2)))

    pred_no_whim = gb + np.sqrt(a0 * gb) * (1.0 + s_val * shared_no_whim * (1.0 - locked)) * f_coupled
    pred_flat = gb + np.sqrt(a0 * gb) * (1.0 + s_val * shared_whim_flat * (1.0 - locked)) * f_coupled
    pred_smooth = gb + np.sqrt(a0 * gb) * (1.0 + s_val * shared_whim_smooth * (1.0 - locked)) * f_coupled

    b_mask = np.abs(vb_ok) > 0
    rms_bulge_smooth = float(np.sqrt(np.mean((y[b_mask] - np.log10(pred_smooth[b_mask])) ** 2)))
    deep_sel = (gb / a0) < 0.2
    deep_res = float(np.log10(pred_flat[deep_sel] / go[deep_sel]).mean())
    return rms(pred_no_whim), rms(pred_flat), rms(pred_smooth), rms_bulge_smooth, deep_res

print("\n" + "=" * 84)
print("FINAL SPARC + 2MRS WHIM SYNTHESIS (149 Galaxies, 2,700 Points)")
print("=" * 84)
r_old_nw, r_old_fl, r_old_sm, r_old_b, d_old = run_whim_pipeline(0.5000, 0.7000, 0.22650)
r_nak_nw, r_nak_fl, r_nak_sm, r_nak_b, d_nak = run_whim_pipeline(UPS_D_GEOM, UPS_B_GEOM, s_derived)

print(f"{'Model Pipeline':42s} | {'No WHIM':>8s} | {'WHIM Flat':>9s} | {'WHIM Smooth':>11s} | {'Bulge Only':>10s}")
print("-" * 84)
print(f"{'1. Empirical M/L (0.50 / 0.70, s=0.2265)':42s} | {r_old_nw:8.4f} | {r_old_fl:9.4f} | {r_old_sm:11.4f} | {r_old_b:10.4f}")
print(f"{'2. Naked Geometric (-2 Fits, s=0.2250)':42s} | {r_nak_nw:8.4f} | {r_nak_fl:9.4f} | {r_nak_sm:11.4f} | {r_nak_b:10.4f}")
print("-" * 84)
print(f"Deep-field (g_bar < 0.2 a0) mean residual : {d_nak:+.4f} dex (was -0.0295 without WHIM)")
print(f"Locked Geometric Constants (-2 Fits)      : UPS_D = {UPS_D_GEOM:.5f}, UPS_B = {UPS_B_GEOM:.5f} (+{DELTA_RHO_GEOM*100:.3f}%)")
