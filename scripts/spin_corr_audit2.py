"""Spin-correlation audit v2 (scratch, session workspace - NOT in the PWC clone). Fixes R^2 bug,
adds GR control models (eta-only, q-only, lnMt-only), nested OOS spin-term test, per-set robustness,
fit-coefficient signs, exact-catalogue k-rule recheck, and catalogue chi_eff uncertainty info."""
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import pearsonr, spearmanr, f as fdist

BASE = r"C:\Users\jaden\Downloads\PWC-Check\PWC\PWC"
G, C0, MS, A_MAX, K = 6.6743e-11, 299792458.0, 1.989e30, 3.23e11, 0.868899
core = lambda m: brentq(lambda c: c + K * c ** (2 / 3) - m, 1e-6, m)

def chi_f_r08(m1, m2, a):
    q = min(m1, m2) / max(m1, m2); nu = q / (1 + q) ** 2; at = (a + a * q * q) / (1 + q * q)
    return at + nu * (-0.1229 * at * at * nu + 0.4537 * at * nu - 2.8904 * at
                      + 2 * np.sqrt(3) - 3.5171 * nu + 2.5763 * nu * nu)

merg = pd.read_csv(f"{BASE}\\merger_energy_balance_results.csv")
b4 = pd.read_csv(f"{BASE}\\gwtc4_blind_results.csv")
b5 = pd.read_csv(f"{BASE}\\gwtc5_blind_results.csv")
spin = pd.concat([b4[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]],
                  b5[["event", "m1", "m2", "Mf", "chi_eff", "chi_f"]]], ignore_index=True)
d = merg.merge(spin, on="event", suffixes=("", "_b"))
assert len(d) == 188 and d.event.is_unique
d["q"] = d.m2 / d.m1; d["eta"] = d.q / (1 + d.q) ** 2; d["lnMt"] = np.log(d.m1 + d.m2)
d["eta2"] = d.eta ** 2; d["eta_chi"] = d.eta * d.chi_eff; d["eta_chi_f"] = d.eta * d.chi_f
r = d["diff_pct"].to_numpy()
tss = ((r - r.mean()) ** 2).sum()

def ols(X, y):
    X = np.column_stack([X, np.ones(len(y))])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b, y - X @ b

# ---------- STEP 1 (fixed) ----------
print("===== STEP 1: residual correlations (188 events) =====")
cols = ["chi_f", "chi_eff", "q", "lnMt"]
for c in cols:
    pr, pp = pearsonr(d[c], r)
    print(f"   corr(resid, {c:>7}) = {pr:+.4f}  (spearman {spearmanr(d[c], r)[0]:+.4f})  p={pp:.2e}")
beta, res = ols(d[cols].to_numpy(), r)
print(f"   joint R^2 = {1 - (res**2).sum()/tss:.4f}   adjusted = {1 - (res**2).sum()/tss*(187/183):.4f}")
print("   coefs: " + ", ".join(f"{c}={b:+.4f}" for c, b in zip(cols, beta)))
print(f"   resid sd after removing all 4 predictors: {res.std(ddof=4):.4f}%")

# per-set robustness
for lab, sub in (("GWTC-4 (84)", d[d.event.isin(b4.event)]), ("GWTC-5 (104)", d[d.event.isin(b5.event)])):
    rr = sub["diff_pct"].to_numpy()
    print(f"   [{lab}] corr chi_f={pearsonr(sub.chi_f, rr)[0]:+.3f}  chi_eff={pearsonr(sub.chi_eff, rr)[0]:+.3f}  "
          f"q={pearsonr(sub.q, rr)[0]:+.3f}  lnMt={pearsonr(sub.lnMt, rr)[0]:+.3f}")

# ---------- STEP 2: partial correlations ----------
print("\n===== STEP 2: partial correlations (Pearson on residualized vars) =====")
def pcorr(y, x, ctrls):
    C = np.column_stack([d[c] for c in ctrls] + [np.ones(len(d))])
    yy = y - C @ np.linalg.lstsq(C, y, rcond=None)[0]
    xx = d[x] - C @ np.linalg.lstsq(C, d[x], rcond=None)[0]
    return pearsonr(xx, yy)
for ctrls in (["lnMt"], ["lnMt", "q"], ["q"]):
    for c in ("chi_f", "chi_eff"):
        if c in ctrls: continue
        pr, pp = pcorr(r, c, ctrls)
        print(f"   pcorr(resid, {c:>7} | {','.join(ctrls):>9}) = {pr:+.4f}  p={pp:.2e}")
# effect size: sd of resid after removing spin beyond (lnMt,q)
C = np.column_stack([d.lnMt, d.q, np.ones(len(d))])
r_base = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]
Xb = np.column_stack([C, d.chi_eff])
r_chi = r - Xb @ np.linalg.lstsq(Xb, r, rcond=None)[0]
print(f"   sd(resid)={r.std():.4f}  -> after (q,lnMt): {r_base.std():.4f}  -> after (q,lnMt,chi_eff): {r_chi.std():.4f}")

# catalogue-side check: does catalogue Mf/Mt itself rise with spin (the GR hang-up direction)?
y = (d.Mf / d.Mt).to_numpy()
pr, pp = pearsonr(d.chi_eff, y)
pr2, pp2 = pcorr(y, "chi_eff", ["eta"])
pr3, pp3 = pcorr(y, "chi_f", ["eta"])
print(f"   catalogue Mf/Mt: corr with chi_eff = {pr:+.3f} (p={pp:.2e}); partial | eta: chi_eff {pr2:+.3f} (p={pp2:.2e}), chi_f {pr3:+.3f} (p={pp3:.2e})")

# ---------- STEP 3: head-to-head ----------
print("\n===== STEP 3: head-to-head residual comparison =====")
def met(pred, true, label, npar="fixed"):
    e = (pred - true) / true * 100
    r2 = 1 - ((pred - true) ** 2).sum() / ((true - true.mean()) ** 2).sum()
    print(f"   {label:<42} sd={e.std():.4f}%  mean|e|={np.abs(e).mean():.4f}%  R2(Mf/Mt)={r2:.4f}  [{npar}]")
    return e
pwc = (d.Mt - d.dump_min).to_numpy(); mf = d.Mf.to_numpy()
families = {
    "GR chi_eff only":            ["chi_eff"],
    "GR chi_f only":              ["chi_f"],
    "GR eta only (no spin)":      ["eta"],
    "GR q only (no spin)":        ["q"],
    "GR lnMt only (no spin)":     ["lnMt"],
    "GR chi_eff + eta":           ["chi_eff", "eta"],
    "GR chi_f + eta":             ["chi_f", "eta"],
    "GR chi_eff+eta+eta2+eta*chi": ["chi_eff", "eta", "eta2", "eta_chi"],
    "GR chi_f+eta+eta2+eta*chi_f": ["chi_f", "eta", "eta2", "eta_chi_f"],
}
print("-- in-sample, all 188 (GR coefficients fitted on same 188) --")
met(pwc, mf, "PWC min(E,S)")
coef_rec = {}
for name, feats in families.items():
    b, _ = ols(d[feats].to_numpy(), y)
    coef_rec[name] = b
    pred = (np.column_stack([d[feats].to_numpy(), np.ones(len(d))]) @ b) * d.Mt.to_numpy()
    met(pred, mf, name, npar=len(feats) + 1)
    if "chi_eff" in feats and "eta" in feats:
        print(f"        coefs: {dict(zip(feats + ['1'], b.round(4)))}")
print("-- honest split: train 84 GWTC-4, test 104 GWTC-5 --")
tr = d.event.isin(b4.event).to_numpy(); te = ~tr
met(pwc[tr], mf[tr], "PWC [train set, fixed]"); met(pwc[te], mf[te], "PWC [OOS 104]")
res_te = {}
for name, feats in families.items():
    b, _ = ols(d[feats].to_numpy()[tr], y[tr])
    pred = (np.column_stack([d[feats].to_numpy()[te], np.ones(te.sum())]) @ b) * d.Mt.to_numpy()[te]
    res_te[name] = met(pred, mf[te], name + " -> OOS", npar=len(feats) + 1)
# nested OOS question: does the spin term improve the eta-model out of sample?
print("-- OOS increment of the spin term on top of eta --")
for base, spinfeat in (("GR eta only (no spin)", "chi_eff"), ("GR eta only (no spin)", "chi_f")):
    b0, _ = ols(d[["eta"]].to_numpy()[tr], y[tr])
    e0 = (np.column_stack([d["eta"].to_numpy()[te], np.ones(te.sum())]) @ b0) * d.Mt.to_numpy()[te]
    b1, _ = ols(d[["eta", spinfeat]].to_numpy()[tr], y[tr])
    e1 = (np.column_stack([d[["eta", spinfeat]].to_numpy()[te], np.ones(te.sum())]) @ b1) * d.Mt.to_numpy()[te]
    s0 = ((e0 - mf[te]) / mf[te] * 100).std(); s1 = ((e1 - mf[te]) / mf[te] * 100).std()
    print(f"   eta-only OOS sd={s0:.4f}%  ->  +{spinfeat} OOS sd={s1:.4f}%   (change {s1-s0:+.4f}pp)")

# ---------- k-rule recheck with exact catalogue masses for the 5 named ----------
print("\n===== k-rule 89-event recheck =====")
named = {"GW150914": None, "GW190521": None, "GW170104": None, "GW170814": None, "GW151226": None}
seen = {}
for f in ("cat_GWTC-1-confident.json", "cat_GWTC-2.1-confident.json"):
    for v in json.load(open(f"{BASE}\\{f}", encoding="utf-8"))["events"].values():
        n = v.get("commonName")
        if n in named and n not in seen:
            seen[n] = (v["mass_1_source"], v["mass_2_source"], v["final_mass_source"], v["chi_eff"])
for n, (m1, m2, mf, ce) in seen.items():
    pred = core(m1) + core(m2); pred = pred + K * pred ** (2 / 3)
    print(f"   {n}: cat m1={m1}, m2={m2}, Mf={mf}  chi_eff={ce}  k-rule dev={100*(pred-mf)/mf:+.2f}%")
kdev = []
for n, (m1, m2, mf, _) in seen.items():
    pred = core(m1) + core(m2); pred = pred + K * pred ** (2 / 3)
    kdev.append(100 * (pred - mf) / mf)
for _, row in b4.iterrows():
    pred = row.Cf + K * row.Cf ** (2 / 3)
    kdev.append(100 * (pred - row.Mf) / row.Mf)
kdev = np.array(kdev)
print(f"   k-rule 89 DEV (exact cat masses for named): mean={kdev.mean():+.3f}%  std={kdev.std():.3f}%")
kd84 = np.array([100 * (row.Cf + K * row.Cf ** (2 / 3) - row.Mf) / row.Mf for _, row in b4.iterrows()])
print(f"   k-rule 84 blind alone: mean={kd84.mean():+.3f}%  std={kd84.std():.3f}%")

# ---------- chi_eff uncertainties from the eventapi JSON (if present) ----------
print("\n===== chi_eff uncertainty info =====")
try:
    js = json.load(open(f"{BASE}\\gw_allevents.json", encoding="utf-8"))["events"]
    keys = set()
    for v in js.values(): keys |= set(v.keys())
    has_lo = "chi_eff_lower" in keys and "chi_eff_upper" in keys
    print(f"   gw_allevents.json has {len(js)} events; keys include chi_eff_lower/upper: {has_lo}")
    if has_lo:
        for lab, sub in (("GWTC-4", b4), ("GWTC-5", b5)):
            rows = []
            for _, r_ in sub.iterrows():
                v = js.get(r_.event)
                if v and v.get("chi_eff_lower") is not None and v.get("chi_eff_upper") is not None:
                    rows.append((v["chi_eff_upper"] - v["chi_eff_lower"]) / 2)
            rows = np.array(rows)
            if len(rows):
                print(f"   [{lab}] median chi_eff 1-sigma half-width: {np.median(rows):.2f} (n={len(rows)})")
except FileNotFoundError:
    print("   gw_allevents.json not found")
