"""Spin-correlation audit of the PWC merger residual (scratch analysis, session workspace - NOT in the PWC clone).

Reproduces the recorded residual check (188 events = 84 GWTC-4 + 104 GWTC-5) and tests:
  1. residual correlations (chi_f, chi_eff, q, lnMt) and joint R^2
  2. partial correlations after removing ln(total mass) [and q]
  3. head-to-head: PWC spin-free min(E,S) vs GR-style spin-dependent fits (in-sample + train/test split)
"""
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import pearsonr, spearmanr

BASE = r"C:\Users\jaden\Downloads\PWC-Check\PWC\PWC"
G, C0, MS, A_MAX, K = 6.6743e-11, 299792458.0, 1.989e30, 3.23e11, 0.868899
core = lambda m: brentq(lambda c: c + K * c ** (2 / 3) - m, 1e-6, m)

# Rezzolla et al. 2008 aligned-spin final-spin fit, exactly as used in the repo blind tests
def chi_f_r08(m1, m2, a):
    q = min(m1, m2) / max(m1, m2)
    nu = q / (1 + q) ** 2
    at = (a + a * q * q) / (1 + q * q)
    return at + nu * (-0.1229 * at * at * nu + 0.4537 * at * nu - 2.8904 * at
                      + 2 * np.sqrt(3) - 3.5171 * nu + 2.5763 * nu * nu)

merg = pd.read_csv(f"{BASE}\\merger_energy_balance_results.csv")
b4 = pd.read_csv(f"{BASE}\\gwtc4_blind_results.csv")
b5 = pd.read_csv(f"{BASE}\\gwtc5_blind_results.csv")
print(f"merger CSV rows: {len(merg)} (sets: {merg['set'].value_counts().to_dict()})")
print(f"blind4: {len(b4)}  blind5: {len(b5)}  named DEV: {merg[merg['set']=='DEV'].event.tolist()}")

# ---- assemble the 188-event set (GWTC-4 + GWTC-5 only, excludes the 5 named events) ----
spin = pd.concat([b4[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]],
                  b5[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]]], ignore_index=True)
d = merg.merge(spin, on="event", suffixes=("", "_b"))
assert len(d) == 188, len(d)
d["q"] = d.m2 / d.m1
d["eta"] = d.q / (1 + d.q) ** 2
d["lnMt"] = np.log(d.m1 + d.m2)
r = d["diff_pct"].to_numpy()  # PWC min(E,S) residual in %, spin-free (k frozen)

print(f"\n188-set: {len(d)}  resid sd={r.std():.4f}%  mean|resid|={np.abs(r).mean():.4f}%")

# ---- reproduce locked-input sanity numbers ----
dev = merg[merg["set"] == "DEV"].copy(); out = merg[merg["set"] == "OUT"].copy()
print(f"\nmin(E,S): DEV89 mean|err|={np.abs(dev.diff_pct).mean():.3f}%  OUT104 mean|err|={np.abs(out.diff_pct).mean():.3f}%")
# k-rule on the 89 DEV events (5 named + 84 blind): need Cf-based pred
named = {"GW150914": (36.0, 29.0, 62.0), "GW190521": (85.0, 66.0, 142.0),
         "GW170104": (31.2, 19.4, 48.7), "GW170814": (30.5, 25.3, 53.2), "GW151226": (14.2, 7.5, 20.8)}
kdev = []
for ev, (m1, m2, mf) in named.items():
    pred = core(m1) + core(m2); pred = pred + K * pred ** (2 / 3)
    kdev.append((pred - mf) / mf * 100)
for _, row in b4.iterrows():
    pred = row.Cf + K * row.Cf ** (2 / 3)
    kdev.append((pred - row.Mf) / row.Mf * 100)
kdev = np.array(kdev)
print(f"k-rule DEV89: mean={kdev.mean():+.3f}%  std={kdev.std():.3f}%  (locked: -0.97%, 2.02%)")

# ---- STEP 1: reproduce recorded correlations ----
print("\n===== STEP 1: residual correlations (188 events) =====")
cols = ["chi_f", "chi_eff", "q", "lnMt"]
print(f"{'var':>8} {'pearson':>9} {'spearman':>9} {'p(pear)':>9}")
cors = {}
for c in cols:
    pr, pp = pearsonr(d[c], r)
    sr = spearmanr(d[c], r)[0]
    cors[c] = pr
    print(f"{c:>8} {pr:+9.4f} {sr:+9.4f} {pp:9.3e}")
X = np.column_stack([d[c] for c in cols] + [np.ones(len(d))])
beta, res_, rank, sv = np.linalg.lstsq(X, r, rcond=None)
rss = (res_ ** 2).sum(); tss = ((r - r.mean()) ** 2).sum()
print(f"joint OLS resid ~ chi_f + chi_eff + q + lnMt : R^2 = {1 - rss/tss:.4f} (recorded 0.33)")
print(f"  coefs: " + ", ".join(f"{c}={b:+.4f}" for c, b in zip(cols, beta)))
print(f"  predictor intercorrelations (Pearson):")
print(pd.DataFrame({c1: {c2: pearsonr(d[c1], d[c2])[0] for c2 in cols} for c1 in cols}).round(3).to_string())

# ---- STEP 2: partial correlations ----
print("\n===== STEP 2: partial correlations =====")
def partial(resid, x, controls, df):
    """partial corr of resid with x controlling for controls, via residualization."""
    C = np.column_stack([df[c] for c in controls] + [np.ones(len(df))])
    rx = resid - C @ np.linalg.lstsq(C, resid, rcond=None)[0]
    xx = df[x] - C @ np.linalg.lstsq(C, df[x], rcond=None)[0]
    return pearsonr(xx, rx)

for controls in (["lnMt"], ["lnMt", "q"]):
    print(f"-- controlling for {controls} --")
    for c in cols:
        if c in controls:
            continue
        pr, pp = partial(r, c, controls, d)
        print(f"   pcorr(resid, {c:>7} | {','.join(controls):>9}) = {pr:+9.4f}   p = {pp:9.3e}")
# nested-R^2 increments (semipartial): how much variance does each spin var add beyond controls?
print("-- semipartial R^2 increments --")
for controls in (["lnMt"], ["lnMt", "q"]):
    C = np.column_stack([d[c] for c in controls] + [np.ones(len(d))])
    rr = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]
    base_rss = (rr ** 2).sum()
    for c in cols:
        if c in controls:
            continue
        Xc = np.column_stack([C, d[c]])
        res2 = r - Xc @ np.linalg.lstsq(Xc, r, rcond=None)[0]
        print(f"   R^2 gain from {c:>7} | {','.join(controls):>9}: {1 - (res2**2).sum()/base_rss:+.4f}  (R^2 of resid-explanation)")
# bootstrap CI for the key partial correlation
rng = np.random.default_rng(7)
boots = []
for _ in range(2000):
    idx = rng.integers(0, len(d), len(d))
    pr, _ = partial(r[idx], "chi_f", ["lnMt"], d.iloc[idx])
    boots.append(pr)
print(f"\n   bootstrap 95% CI for pcorr(resid, chi_f | lnMt): [{np.percentile(boots,2.5):+.3f}, {np.percentile(boots,97.5):+.3f}]")
boots = []
for _ in range(2000):
    idx = rng.integers(0, len(d), len(d))
    pr, _ = partial(r[idx], "chi_eff", ["lnMt"], d.iloc[idx])
    boots.append(pr)
print(f"   bootstrap 95% CI for pcorr(resid, chi_eff | lnMt): [{np.percentile(boots,2.5):+.3f}, {np.percentile(boots,97.5):+.3f}]")

# ---- STEP 3: head-to-head GR-style spin-dependent models vs PWC ----
print("\n===== STEP 3: head-to-head residual comparison =====")
def metrics(y_pred_Mf, y_true_Mf, label, n_params=None):
    e = (y_pred_Mf - y_true_Mf) / y_true_Mf * 100
    r2 = 1 - ((y_pred_Mf - y_true_Mf) ** 2).sum() / ((y_true_Mf - y_true_Mf.mean()) ** 2).sum()
    extra = f"  npar={n_params}" if n_params is not None else "  npar=0 (fixed)"
    print(f"   {label:<38} sd={e.std():.4f}%  mean|e|={np.abs(e).mean():.4f}%  R^2(Mf/Mt)={r2:.4f}{extra}")
    return e

def fit_ols(Xt, y):
    return np.linalg.lstsq(np.column_stack([Xt, np.ones(len(y))]), y, rcond=None)[0]

# PWC: spin-free, fixed (k frozen) - predicted final mass from merger CSV
pwc_pred = (d.Mt - d.dump_min).to_numpy()
print("-- all 188, in-sample --")
metrics(pwc_pred, d.Mf.to_numpy(), "PWC min(E,S) (no fitted params)")
# GR-style families (state: leading-order spin dependence of the radiated fraction is linear in chi_eff;
# polynomial family in (eta, chi) as used by NR remnant fits, e.g. Jimenez-Forteza+2017 / Varma+2019).
y = d.Mf.to_numpy() / d.Mt.to_numpy()
fam = {
    "GR lin chi_eff":             (["chi_eff"], None),
    "GR lin chi_eff + eta":       (["chi_eff", "eta"], None),
    "GR lin chi_f + eta":         (["chi_f", "eta"], None),
    "GR rad-frac (chi_eff,eta,eta^2,eta*chi)": (["chi_eff", "eta", "eta2", "eta_chi"], None),
    "GR rad-frac (chi_f,eta,eta^2,eta*chi_f)": (["chi_f", "eta", "eta2", "eta_chi_f"], None),
}
d["eta2"] = d.eta ** 2
d["eta_chi"] = d.eta * d.chi_eff
d["eta_chi_f"] = d.eta * d.chi_f
for name, (feats, _) in fam.items():
    Xt = d[feats].to_numpy()
    beta = fit_ols(Xt, y)
    pred = (np.column_stack([Xt, np.ones(len(y))]) @ beta) * d.Mt.to_numpy()
    metrics(pred, d.Mf.to_numpy(), name, n_params=len(feats) + 1)

print("-- honest split: GR models trained on 84 GWTC-4, evaluated on 104 GWTC-5; PWC fixed --")
tr = d[d.event.isin(b4.event)].index.to_numpy(); te = d[d.event.isin(b5.event)].index.to_numpy()
metrics(pwc_pred[tr], d.Mf.to_numpy()[tr], "PWC min(E,S) [GWTC-4 84]")
metrics(pwc_pred[te], d.Mf.to_numpy()[te], "PWC min(E,S) [GWTC-5 104 OOS]")
for name, (feats, _) in fam.items():
    Xt_tr = d[feats].to_numpy()[tr]; y_tr = y[tr]
    beta = fit_ols(Xt_tr, y_tr)
    pred = (np.column_stack([d[feats].to_numpy()[te], np.ones(len(te))]) @ beta) * d.Mt.to_numpy()[te]
    metrics(pred, d.Mf.to_numpy()[te], f"{name} -> OOS", n_params=len(feats) + 1)

# train on all 89 DEV (adds the 5 named events; chi_eff from GWOSC cat JSONs, chi_f via Rezzolla fit)
print("-- variant split: GR trained on 89 DEV (incl. 5 named), tested on 104 GWTC-5 --")
cats = []
for f in ("cat_GWTC-1-confident.json", "cat_GWTC-2.1-confident.json", "cat_GWTC-3-confident.json"):
    js = json.load(open(f"{BASE}\\{f}", encoding="utf-8"))["events"]
    for v in js.values():
        if v.get("commonName") in named:
            cats.append(dict(event=v["commonName"], m1=v["mass_1_source"], m2=v["mass_2_source"],
                             Mf=v["final_mass_source"], chi_eff=v["chi_eff"]))
catn = pd.DataFrame(cats)
print("   named-event catalogue rows:", catn[["event", "chi_eff"]].to_string(index=False))
dev89 = pd.concat([b4[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]], catn], ignore_index=True)
dev89["q"] = dev89.m2 / dev89.m1; dev89["eta"] = dev89.q / (1 + dev89.q) ** 2
dev89.loc[dev89.chi_f.isna(), "chi_f"] = [chi_f_r08(r_.m1, r_.m2, r_.chi_eff) for r_ in
                                          dev89[dev89.chi_f.isna()].itertuples()]
dev89["eta2"] = dev89.eta ** 2; dev89["eta_chi"] = dev89.eta * dev89.chi_eff
dev89["eta_chi_f"] = dev89.eta * dev89.chi_f
dte = d[d.event.isin(b5.event)]
for name, (feats, _) in fam.items():
    beta = fit_ols(dev89[feats].to_numpy(), (dev89.Mf / (dev89.m1 + dev89.m2)).to_numpy())
    pred = (np.column_stack([dte[feats].to_numpy(), np.ones(len(dte))]) @ beta) * (dte.m1 + dte.m2).to_numpy()
    metrics(pred, dte.Mf.to_numpy(), f"{name} [train 89 DEV] -> OOS", n_params=len(feats) + 1)

# ---- does spin ADD to a mass-only GR fit of the PWC residual? (nested F) ----
print("\n-- nested test on the PWC residual: does chi explain resid beyond q and lnMt? --")
C = np.column_stack([d.q, d.lnMt, np.ones(len(d))])
res_small = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]
X_big = np.column_stack([C, d.chi_eff, d.chi_f])
res_big = r - X_big @ np.linalg.lstsq(X_big, r, rcond=None)[0]
n, k_small, k_big = len(r), 3, 5
F = ((res_small**2).sum() - (res_big**2).sum()) / (k_big - k_small) / ((res_big**2).sum() / (n - k_big))
from scipy.stats import f as fdist
print(f"   adding chi_eff, chi_f to (q, lnMt): R^2 {1-(res_small**2).sum()/((r-r.mean())**2).sum():.4f} -> "
      f"{1-(res_big**2).sum()/((r-r.mean())**2).sum():.4f},  F={F:.2f},  p={1-fdist.cdf(F, k_big-k_small, n-k_big):.3e}")
