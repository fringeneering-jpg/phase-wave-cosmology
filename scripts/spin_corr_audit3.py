"""Spin-correlation audit v3 (scratch, session workspace - NOT in the PWC clone).
Final robustness: reverse split, per-set partial correlations, GR-consistency of fitted coefficients,
PWC+spin-correction transfer, variance decomposition."""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

BASE = r"C:\Users\jaden\Downloads\PWC-Check\PWC\PWC"
merg = pd.read_csv(f"{BASE}\\merger_energy_balance_results.csv")
b4 = pd.read_csv(f"{BASE}\\gwtc4_blind_results.csv")
b5 = pd.read_csv(f"{BASE}\\gwtc5_blind_results.csv")
spin = pd.concat([b4[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]],
                  b5[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]]], ignore_index=True)
d = merg.merge(spin, on="event", suffixes=("", "_b"))
d["q"] = d.m2 / d.m1; d["eta"] = d.q / (1 + d.q) ** 2; d["lnMt"] = np.log(d.m1 + d.m2)
d["eta2"] = d.eta ** 2; d["eta_chi"] = d.eta * d.chi_eff
r = d["diff_pct"].to_numpy(); mf = d.Mf.to_numpy(); mt = d.Mt.to_numpy()
tr4 = d.event.isin(b4.event).to_numpy(); tr5 = ~tr4

def ols(X, y):
    X = np.column_stack([X, np.ones(len(y))])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b, y - X @ b

def sd(pred, idx):
    e = (pred[idx] - mf[idx]) / mf[idx] * 100
    return e.std(), np.abs(e).mean()

# --- per-set partial correlations (spin vs residual, controlling q and lnMt) ---
print("per-set partial correlations:")
for lab, idx in (("GWTC-4 84", tr4), ("GWTC-5 104", tr5)):
    C = np.column_stack([d.q[idx], d.lnMt[idx], np.ones(idx.sum())])
    rr = r[idx] - C @ np.linalg.lstsq(C, r[idx], rcond=None)[0]
    for s in ("chi_eff", "chi_f"):
        ss = d[s][idx] - C @ np.linalg.lstsq(C, d[s][idx], rcond=None)[0]
        pr, pp = pearsonr(ss, rr)
        print(f"   [{lab}] pcorr(resid, {s} | q,lnMt) = {pr:+.3f} (p={pp:.2e})")
# per-set fitted spin slopes on Mf/Mt (control eta)
print("per-set OLS Mf/Mt = a + b*eta + c*chi_eff:")
for lab, idx in (("GWTC-4 84", tr4), ("GWTC-5 104", tr5), ("both 188", np.ones(len(d), bool))):
    b = ols(np.column_stack([d.eta[idx], d.chi_eff[idx]]), mf[idx] / mt[idx])[0]
    print(f"   [{lab}] eta={b[0]:+.4f}  chi_eff={b[1]:+.4f}  const={b[2]:+.4f}")

# --- reverse split: train on 104, test on 84 ---
print("reverse split (train GWTC-5 104, test GWTC-4 84):")
pwc = (mt - d.dump_min.to_numpy())
print(f"   PWC OOS sd={sd(pwc, tr4)[0]:.4f}%  mean|e|={sd(pwc, tr4)[1]:.4f}%")
for name, feats in {"eta only": ["eta"], "q only": ["q"], "chi_eff only": ["chi_eff"],
                    "chi_eff+eta": ["chi_eff", "eta"]}.items():
    b, _ = ols(d[feats].to_numpy()[tr5], (mf / mt)[tr5])
    pred = (np.column_stack([d[feats].to_numpy()[tr4], np.ones(tr4.sum())]) @ b) * mt[tr4]
    e = (pred - mf[tr4]) / mf[tr4] * 100
    print(f"   GR {name} -> OOS sd={e.std():.4f}%  mean|e|={np.abs(e).mean():.4f}%")

# --- PWC + fitted spin correction: does a chi_eff term on the PWC residual transfer OOS? ---
print("PWC + linear chi_eff correction (fit on 84, apply to 104):")
b, _ = ols(d.chi_eff.to_numpy()[tr4], r[tr4])
corr = np.column_stack([d.chi_eff.to_numpy()[tr5], np.ones(tr5.sum())]) @ b
e0 = r[tr5]; e1 = r[tr5] - corr
print(f"   resid sd OOS: {e0.std():.4f}% -> {e1.std():.4f}%   (fitted slope {b[0]:+.3f}%/unit chi)")
# GR reference magnitude: Hemberger+2013 equal-mass spin slope on Mf/M ~ -0.040
print(f"   GR reference (Hemberger+13, equal mass): d(Mf/M)/d(chi) = -0.0403")

# --- variance decomposition of the PWC residual (188) ---
print("variance decomposition of PWC residual (188):")
tss = ((r - r.mean()) ** 2).sum()
C1 = np.column_stack([d.lnMt, np.ones(len(d))])
C2 = np.column_stack([d.lnMt, d.q, np.ones(len(d))])
C3 = np.column_stack([d.lnMt, d.q, d.chi_eff, np.ones(len(d))])
C4 = np.column_stack([d.lnMt, d.q, d.chi_eff, d.chi_f, np.ones(len(d))])
rss = lambda C: (r - C @ np.linalg.lstsq(C, r, rcond=None)[0] ** 0 - (C @ np.linalg.lstsq(C, r, rcond=None)[0])) ** 2
def R2(C):
    res = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]
    return 1 - (res ** 2).sum() / tss
print(f"   lnMt:            R2={R2(C1):.4f}")
print(f"   +q:              R2={R2(C2):.4f}  (q increment {R2(C2)-R2(C1):+.4f})")
print(f"   +chi_eff:        R2={R2(C3):.4f}  (spin increment {R2(C3)-R2(C2):+.4f})")
print(f"   +chi_f:          R2={R2(C4):.4f}  (chi_f increment {R2(C4)-R2(C3):+.4f})")
print(f"   -> sd(resid) = {r.std():.4f}% ; after all 4: {(r - C4@np.linalg.lstsq(C4,r,rcond=None)[0]).std():.4f}%")

# --- GR-consistency of the free fit vs Hemberger+13 ---
print("GR-consistency check of free fit on catalogue data (188):")
b, _ = ols(np.column_stack([d.eta, d.chi_eff]), mf / mt)
print(f"   Mf/Mt = {b[2]:+.4f} + {b[0]:+.4f}*eta + {b[1]:+.4f}*chi_eff")
print(f"   -> at eta=0.25, chi=0: Mf/Mt = {b[2]+0.25*b[0]:.4f}  (NR nonspinning equal-mass: 0.9516)")
print(f"   -> spin slope {b[1]:+.4f} vs Hemberger+13 equal-mass -0.0403 (sample spans eta<0.25, slope scales ~eta)")
