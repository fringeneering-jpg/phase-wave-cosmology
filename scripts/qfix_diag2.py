"""Diagnostic 2: what q-shape do the catalog dumps demand, and which geometric length matches?
All constants locked; no fitting on the PWC side. (scratch, session workspace - NOT in the PWC clone)"""
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
m1 = d.m1.to_numpy(); m2 = d.m2.to_numpy(); mf = d.Mf.to_numpy(); mt = m1 + m2
dump_cat = mt - mf
C1 = np.array([core(m) for m in m1]); C2 = np.array([core(m) for m in m2])
E1 = np.sqrt(G * m1 * MS / A_MAX); E2 = np.sqrt(G * m2 * MS / A_MAX)
R1 = (3 * C1 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
R2 = (3 * C2 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
t1 = E1 - R1; t2 = E2 - R2
S = K * (C1 ** (2 / 3) + C2 ** (2 / 3) - (C1 + C2) ** (2 / 3))
E_old = G * (m1 * MS) * (m2 * MS) / (2 * (E1 + E2) * C0 ** 2) / MS
E_new = G * (C1 * MS) * (C2 * MS) / (2 * (t1 + t2) * C0 ** 2) / MS

# pinch ring at core-touch: waist circle of the two LAYER spheres at d = R1+R2
d0 = R1 + R2
x1 = (d0 ** 2 + E1 ** 2 - E2 ** 2) / (2 * d0)
rho_p = np.sqrt(np.clip(E1 ** 2 - x1 ** 2, 0, None))
waist_travel1 = E1 - x1                       # from layer-touch (x=E1) to core-touch, core-1 frame
waist_travel2 = E2 - (d0 - x1)                # core-2 frame

print("=== log-log shape: log(dump) ~ log(Mt) + log(q) (OLS, catalog vs models) ===")
X = np.column_stack([np.log(mt), np.log(d.q), np.ones(len(d))])
for name, yv in (("catalog dump", np.log(dump_cat)), ("E_old", np.log(E_old)),
                 ("E_new", np.log(E_new)), ("S", np.log(S))):
    b, res, *_ = np.linalg.lstsq(X, yv, rcond=None)
    print(f"   {name:<13} dlog/dlogMt={b[0]:+.3f}   dlog/dlogq={b[1]:+.3f}   (sd resid {res.std():.3f})")

print("\n=== implied fight length d_impl = G C1 C2 / (2 c0^2 dump_cat), vs geometric candidates ===")
d_impl = G * (C1 * MS) * (C2 * MS) / (2 * dump_cat * C0 ** 2) / MS * 0  # placeholder replaced below
d_impl = G * (C1 * MS) * (C2 * MS) / (2 * dump_cat * MS * C0 ** 2)
cands = {
    "t1+t2": t1 + t2,
    "E1+E2": E1 + E2,
    "R1+R2": R1 + R2,
    "rho_p (waist radius @core-touch)": rho_p,
    "2*rho_p": 2 * rho_p,
    "waist travel1+2": waist_travel1 + waist_travel2,
    "2*min(t1,t2)": 2 * np.minimum(t1, t2),
    "2*min(E1,E2)": 2 * np.minimum(E1, E2),
}
r_d = np.log(d_impl)
for name, L in cands.items():
    pr = pearsonr(np.log(L), r_d)[0]
    # also ratio median
    ratio = np.median(d_impl / L)
    print(f"   d_impl vs {name:<32} corr(log)={pr:+.3f}   median(d_impl/L)={ratio:.3f}")

print("\n=== d_impl in q bins (km), and t1+t2, E1+E2 alongside ===")
bins = [0, .3, .5, .7, .85, 1.01]
for lo, hi in zip(bins[:-1], bins[1:]):
    m = (d.q >= lo) & (d.q < hi)
    print(f"   q[{lo:.2f},{hi:.2f}) n={m.sum():3d}: d_impl={np.median(d_impl[m])/1e3:7.1f}  "
          f"t1+t2={np.median(t1[m]+t2[m])/1e3:7.1f}  E1+E2={np.median(E1[m]+E2[m])/1e3:7.1f}  "
          f"rho_p={np.median(rho_p[m])/1e3:7.1f}")

print("\n=== E_old vs E_new vs dump_cat: q-dependence at fixed Mt (partial out log Mt) ===")
def qslope(yv):
    X = np.column_stack([np.log(mt), np.log(d.q), np.ones(len(d))])
    b, *_ = np.linalg.lstsq(X, np.log(yv), rcond=None)
    return b[1]
print(f"   dlog/dlogq: catalog={qslope(dump_cat):+.3f}  E_old={qslope(E_old):+.3f}  E_new={qslope(E_new):+.3f}  S={qslope(S):+.3f}")

print("\n=== where is min(E,S) active? ===")
oldE = E_old < S
newE = E_new < S
print(f"   E-limited: old {oldE.sum()}/188, new {newE.sum()}/188  (S-limited rest)")
print("   crossover by Mt bin (n old-E / n new-E):")
for lo, hi in [(0, 25), (25, 40), (40, 60), (60, 100), (100, 300)]:
    m = (mt >= lo) & (mt < hi)
    print(f"      Mt[{lo:3d},{hi:3d}) n={m.sum():3d}: old-E {oldE[m].sum():3d}, new-E {newE[m].sum():3d}")

print("\n=== does dump_cat itself follow eta=q/(1+q)^2 at fixed Mt? (the GR-fit target shape) ===")
X = np.column_stack([np.log(mt), np.log(d.eta), np.ones(len(d))])
b, *_ = np.linalg.lstsq(X, np.log(dump_cat), rcond=None)
print(f"   dlog(dump_cat)/dlog(eta) = {b[1]:+.3f}   dlog/dlogMt = {b[0]:+.3f}")
X = np.column_stack([np.log(mt), np.log(d.eta), np.ones(len(d))])
b2, *_ = np.linalg.lstsq(X, np.log(E_old), rcond=None)
print(f"   dlog(E_old)/dlog(eta)    = {b2[1]:+.3f}   dlog/dlogMt = {b2[0]:+.3f}")
b3, *_ = np.linalg.lstsq(X, np.log(E_new), rcond=None)
print(f"   dlog(E_new)/dlog(eta)    = {b3[1]:+.3f}   dlog/dlogMt = {b3[0]:+.3f}")
b4_, *_ = np.linalg.lstsq(X, np.log(S), rcond=None)
print(f"   dlog(S)/dlog(eta)        = {b4_[1]:+.3f}   dlog/dlogMt = {b4_[0]:+.3f}")
