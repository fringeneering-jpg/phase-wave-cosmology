"""Diagnostic 2b: implied contact separation per regime. (scratch, session workspace)"""
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import pearsonr

BASE = r"C:\Users\jaden\Downloads\PWC-Check\PWC\PWC"
G, C0, MS, A_MAX, K = 6.6743e-11, 299792458.0, 1.989e30, 3.23e11, 0.868899
RHO_CORE = 2.3e17
core = lambda m: brentq(lambda c: c + K * c ** (2 / 3) - m, 1e-6, m)

merg = pd.read_csv(f"{BASE}\\merger_energy_balance_results.csv")
b4 = pd.read_csv(f"{BASE}\\gwtc4_blind_results.csv")
b5 = pd.read_csv(f"{BASE}\\gwtc5_blind_results.csv")
spin = pd.concat([b4[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]],
                  b5[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]]], ignore_index=True)
d = merg.merge(spin, on="event", suffixes=("", "_b"))
d["q"] = d.m2 / d.m1
d["eta"] = d.q / (1 + d.q) ** 2
m1 = d.m1.to_numpy(); m2 = d.m2.to_numpy(); mf = d.Mf.to_numpy(); mt = m1 + m2
dump_cat = mt - mf
print(f"dump_cat <= 0 events: {(dump_cat <= 0).sum()}  ->  {list(d.event[dump_cat <= 0])}")
C1 = np.array([core(m) for m in m1]); C2 = np.array([core(m) for m in m2])
E1 = np.sqrt(G * m1 * MS / A_MAX); E2 = np.sqrt(G * m2 * MS / A_MAX)
R1 = (3 * C1 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
R2 = (3 * C2 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
t1 = E1 - R1; t2 = E2 - R2
S = K * (C1 ** (2 / 3) + C2 ** (2 / 3) - (C1 + C2) ** (2 / 3))
E_old = G * (m1 * MS) * (m2 * MS) / (2 * (E1 + E2) * C0 ** 2) / MS
E_new = G * (C1 * MS) * (C2 * MS) / (2 * (t1 + t2) * C0 ** 2) / MS
drop_old = np.minimum(E_old, S); drop_new = np.minimum(E_new, S)

# pinch ring (waist) of the layer spheres at core-touch d0 = R1+R2
d0 = R1 + R2
x1 = (d0 ** 2 + E1 ** 2 - E2 ** 2) / (2 * d0)
rho_p = np.sqrt(np.clip(E1 ** 2 - x1 ** 2, 0, None))

ok = dump_cat > 0
X = np.column_stack([np.log(mt[ok]), np.log(d.q.to_numpy()[ok]), np.ones(ok.sum())])
print("\n=== log-log shape (events with dump>0) ===")
for name, yv in (("catalog", np.log(dump_cat[ok])), ("E_old", np.log(E_old[ok])),
                 ("E_new", np.log(E_new[ok])), ("S", np.log(S[ok])), ("eta*Mt", np.log((d.eta.to_numpy() * mt)[ok]))):
    b, res, *_ = np.linalg.lstsq(X, yv, rcond=None)
    print(f"   log({name:<8}) ~ {b[0]:+.3f}*logMt {b[1]:+.3f}*logq   resid sd={res.std():.3f}")

print("\n=== implied separation with M1M2 numerator (old-E-limited events) ===")
r_impl_old = G * (m1 * MS) * (m2 * MS) / (2 * dump_cat * MS * C0 ** 2)
mask_old = (E_old < S) & ok
print(f"old-E-limited & dump>0: {mask_old.sum()}")
cands = {"E1+E2": E1 + E2, "t1+t2": t1 + t2, "R1+R2": R1 + R2, "rho_p": rho_p,
         "2 rho_p": 2 * rho_p, "E1+E2-t1-t2+R1+R2": E1 + E2 - t1 - t2 + R1 + R2}
for name, L in cands.items():
    pr = pearsonr(np.log(L[mask_old]), np.log(r_impl_old[mask_old]))[0]
    print(f"   r_impl(M1M2) vs {name:<22} corr(log)={pr:+.3f}  median(r_impl/L)={np.median(r_impl_old[mask_old]/L[mask_old]):.3f}")

print("\n=== implied separation with C1C2 numerator (new-E-limited events) ===")
r_impl_new = G * (C1 * MS) * (C2 * MS) / (2 * dump_cat * MS * C0 ** 2)
mask_new = (E_new < S) & ok
print(f"new-E-limited & dump>0: {mask_new.sum()}")
for name, L in cands.items():
    pr = pearsonr(np.log(L[mask_new]), np.log(r_impl_new[mask_new]))[0]
    print(f"   r_impl(C1C2) vs {name:<22} corr(log)={pr:+.3f}  median(r_impl/L)={np.median(r_impl_new[mask_new]/L[mask_new]):.3f}")

print("\n=== residual by Mt bin: old vs new ===")
r_old = (mt - drop_old - mf) / mf * 100
r_new = (mt - drop_new - mf) / mf * 100
for lo, hi in [(0, 25), (25, 40), (40, 60), (60, 100), (100, 300)]:
    m = (mt >= lo) & (mt < hi)
    print(f"   Mt[{lo:3d},{hi:3d}) n={m.sum():3d}: old {r_old[m].mean():+6.2f}% (sd {r_old[m].std():.2f})   "
          f"new {r_new[m].mean():+6.2f}% (sd {r_new[m].std():.2f})")

print("\n=== residual by q bin within old-E-limited only: old vs new ===")
bins = [0, .3, .5, .7, .85, 1.01]
for lo, hi in zip(bins[:-1], bins[1:]):
    m = (d.q >= lo) & (d.q < hi) & mask_old
    if m.sum() == 0:
        continue
    print(f"   q[{lo:.2f},{hi:.2f}) n={m.sum():3d}: old {r_old[m].mean():+6.2f}%  new {r_new[m].mean():+6.2f}%")

print("\n=== implied r in q bins (old-E-limited) vs E1+E2 / t1+t2 (km) ===")
for lo, hi in zip(bins[:-1], bins[1:]):
    m = (d.q >= lo) & (d.q < hi) & mask_old
    if m.sum() < 2:
        continue
    print(f"   q[{lo:.2f},{hi:.2f}) n={m.sum():3d}: r_impl={np.median(r_impl_old[m])/1e3:7.1f}  "
          f"E1+E2={np.median(E1[m]+E2[m])/1e3:7.1f}  t1+t2={np.median(t1[m]+t2[m])/1e3:7.1f}  rho_p={np.median(rho_p[m])/1e3:7.1f}")

print("\n=== worst events old vs new ===")
idx = np.argsort(np.abs(r_old))[::-1][:12]
for i in idx:
    print(f"   {d.event.iloc[i]:<20} m1={m1[i]:5.1f} m2={m2[i]:5.1f} q={d.q.iloc[i]:.2f} dump_cat={dump_cat[i]:5.2f} "
          f"E_old={E_old[i]:5.2f} E_new={E_new[i]:5.2f} S={S[i]:5.2f} | old {r_old[i]:+6.2f}%  new {r_new[i]:+6.2f}%")
