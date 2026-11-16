# sparc_failpoints.py - where the LDL/HDL forms fail, bin by bin (2026-10-15)
import numpy as np, sys
sys.path.insert(0, r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x")
from domain_K_rar import read_vizier_tsv, KPC, KMS, UPS_D, UPS_B
D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}; qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
name = np.array(t2["Name"]); R = np.array(t2["Rad"], float); Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float); Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float)
Vb = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float)); Vg = np.where(np.isnan(Vg), 0.0, Vg)
inc_a = np.array([inc.get(n, np.nan) for n in name], float); qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo/Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
conv = (KMS**2)/KPC; g_obs = Vo**2/R*conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb); g_bar = Vbar2/R*conv
ok = (g_bar > 0) & (g_obs > 0); g_obs, g_bar, R, Vb, Vbar2, name = g_obs[ok], g_bar[ok], R[ok], Vb[ok], Vbar2[ok], name[ok]
locked = np.clip(UPS_B*Vb*np.abs(Vb)/np.maximum(Vbar2,1e-30), 0, 1)
shared = np.zeros_like(g_bar)
for n in set(name):
    sel = name == n; Mb = Vbar2[sel]*R[sel]; shared[sel] = np.clip(1.0 - Mb/Mb.max(), 0, 1)
a0 = 6.6110e-11; s = 0.22650
boost = 1.0 + s*shared*(1.0-locked); x = g_bar/(18.0*a0)
pred_C = g_bar + np.sqrt(a0*g_bar/np.sqrt(1.0+x**2))*boost
pred_E = g_bar + np.sqrt(a0*g_bar)*boost/(1.0+x**2)
def rar(gb): return gb/(1.0-np.exp(-np.sqrt(gb/1.2e-10)))
res_C = np.log10(pred_C/g_obs); res_E = np.log10(pred_E/g_obs); res_R = np.log10(rar(g_bar)/g_obs)
print("regime bins (g_bar/a0):  [n pts]  mean residual dex  C / E / RAR  (pos = model HIGH)")
edges = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
rat = g_bar/a0
for i in range(len(edges)-1):
    sel = (rat >= edges[i]) & (rat < edges[i+1])
    if sel.sum() < 10: continue
    print(f"  {edges[i]:5.2f}-{edges[i+1]:5.2f}: {sel.sum():5d}   {res_C[sel].mean():+7.4f} {res_E[sel].mean():+7.4f} {res_R[sel].mean():+7.4f}")
print("worst UNDER-predicting galaxies for Form E (the bleed's home):")
per = {}
for n in set(name):
    sel = name == n; per[n] = res_E[sel].mean()
for n, v in sorted(per.items(), key=lambda kv: kv[1])[:6]:
    sel = name == n
    print(f"  {n:12s} n={sel.sum():3d}  mean E residual {v:+.4f}  (RAR {res_R[sel].mean():+.4f})")
