"""Figure-8 contact-energy correction audit (scratch, session workspace - NOT in the PWC clone).

Task: fix the q-dependence of the PWC merger-mass rule. Locked inputs only; ZERO fitted PWC parameters.

GEOMETRY (all constants locked):
  - cores C_i at rho_core = 2.3e17 kg/m^3, incompressible, volumes add; R_i = (3 C_i/(4 pi rho_core))^(1/3)
  - layer edge E_i = sqrt(G M_i / a_max), a_max = 3.23e11 (total mass M_i inside), C_i + k C_i^(2/3) = M_i, k = 0.868899
  - layer thickness t_i = E_i - R_i
  - FIGHT LENGTH (figure-8): from layer-touch (d = E1+E2) to whichever comes first:
      core-touch d = R1+R2  OR  pinch-closure d = |E1-E2| (smaller layer engulfed, figure-8 degenerate)
    =>  d_eff = (E1+E2) - max(R1+R2, |E1-E2|) = min(t1+t2, 2*min(E1,E2))
  - CORRECTED ENERGY (heat included: fight deceleration work = released medium latent heat, c0^2 J/kg):
      E(q) = G*C1*C2 / (2*c0^2 * d_eff)          [no fitted constant]
  - storage limit S unchanged (k-rule frozen): S = k*(C1^(2/3)+C2^(2/3)-(C1+C2)^(2/3))
  - drop = min(E, S);  Mf = M1+M2 - drop

Baseline (locked deficiency): E_old = G*M1*M2/(2*c0^2*(E1+E2)); OOS sd 1.038% vs GR q-only 0.771% (104 OOS).
"""
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import pearsonr, spearmanr

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
assert len(d) == 188 and d.event.is_unique
d["q"] = d.m2 / d.m1
d["eta"] = d.q / (1 + d.q) ** 2
d["lnMt"] = np.log(d.m1 + d.m2)

m1 = d.m1.to_numpy(); m2 = d.m2.to_numpy(); mf = d.Mf.to_numpy(); mt = (m1 + m2)
C1 = np.array([core(m) for m in m1]); C2 = np.array([core(m) for m in m2])
E1 = np.sqrt(G * m1 * MS / A_MAX); E2 = np.sqrt(G * m2 * MS / A_MAX)
R1 = (3 * C1 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
R2 = (3 * C2 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
t1 = E1 - R1; t2 = E2 - R2
S = K * (C1 ** (2 / 3) + C2 ** (2 / 3) - (C1 + C2) ** (2 / 3))

E_old = G * (m1 * MS) * (m2 * MS) / (2 * (E1 + E2) * C0 ** 2) / MS
d_plain = t1 + t2
d_cap = np.minimum(t1 + t2, 2 * np.minimum(E1, E2))
E_A = G * (C1 * MS) * (C2 * MS) / (2 * d_plain * C0 ** 2) / MS          # fight length, no cap
E_B = G * (C1 * MS) * (C2 * MS) / (2 * d_cap * C0 ** 2) / MS            # pinch-closure cap
dump_old = np.minimum(E_old, S)
dump_A = np.minimum(E_A, S)
dump_B = np.minimum(E_B, S)

# ---- GW150914 closure check (locked: G C1 C2/(2 c0^2 (t1+t2)) = 2.957 vs 3.0 release, -1.4%) ----
i914 = d.event.to_numpy() == "GW150914"
if i914.any():
    i = np.where(i914)[0][0]
    print(f"GW150914 closure: C1={C1[i]:.3f} C2={C2[i]:.3f}  R1={R1[i]/1e3:.1f}km R2={R2[i]/1e3:.1f}km "
          f"E1={E1[i]/1e3:.1f}km E2={E2[i]/1e3:.1f}km  t1={t1[i]/1e3:.1f}km t2={t2[i]/1e3:.1f}km "
          f"t1+t2={d_plain[i]/1e3:.1f}km")
    print(f"   E_new(A) = {E_A[i]:.4f} Msun  E_new(B) = {E_B[i]:.4f} Msun  E_old = {E_old[i]:.4f}  S = {S[i]:.4f}  "
          f"catalog dump = {mt[i]-mf[i]:.3f}")

# ---- metrics machinery (replicates spin_corr_audit2.py exactly) ----
def ols(X, y):
    X = np.column_stack([X, np.ones(len(y))])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b, y - X @ b

def met(pred, true, label, npar="fixed"):
    e = (pred - true) / true * 100
    r2 = 1 - ((pred - true) ** 2).sum() / ((true - true.mean()) ** 2).sum()
    print(f"   {label:<44} sd={e.std():.4f}%  mean={e.mean():+.4f}%  mean|e|={np.abs(e).mean():.4f}%  R2={r2:.4f}  [{npar}]")
    return e

y = mf / mt  # Mf/Mt for GR fits

def gr_q_only(tr, te, lab):
    Xtr = d.q.to_numpy()[tr]
    b, _ = ols(Xtr, y[tr])
    pred = (d.q.to_numpy()[te] * b[0] + b[1]) * mt[te]
    return met(pred, mf[te], lab, npar=2)

print("\n===== BASELINE REPRODUCTION (locked numbers) =====")
pwc_old_pred = mt - dump_old
met(pwc_old_pred, mf, "PWC-old min(E,S) [188 in-sample]")
tr = d.event.isin(b4.event).to_numpy(); te = ~tr
print(f"train GWTC-4 n={tr.sum()}, test GWTC-5 n={te.sum()}")
met(pwc_old_pred[te], mf[te], "PWC-old [OOS 104]")
gr_q_only(tr, te, "GR q-only [OOS 104]")
met(pwc_old_pred[tr], mf[tr], "PWC-old [OOS 84]")
b, _ = ols(d.q.to_numpy()[te], y[te])
pred = (d.q.to_numpy()[tr] * b[0] + b[1]) * mt[tr]
met(pred, mf[tr], "GR q-only [OOS 84]", npar=2)

print("\n===== CORRECTED RULE (zero fitted parameters) =====")
pwc_A = mt - dump_A
pwc_B = mt - dump_B
met(pwc_A, mf, "PWC-new A (t1+t2, no cap) [188]")
met(pwc_B, mf, "PWC-new B (pinch-closure cap) [188]")
print("-- train 84 GWTC-4 -> test 104 GWTC-5 --")
met(pwc_old_pred[te], mf[te], "PWC-old [OOS 104]")
met(pwc_A[te], mf[te], "PWC-new A [OOS 104]")
met(pwc_B[te], mf[te], "PWC-new B [OOS 104]")
gr_q_only(tr, te, "GR q-only [OOS 104]")
print("-- reverse: train 104 GWTC-5 -> test 84 GWTC-4 --")
met(pwc_old_pred[tr], mf[tr], "PWC-old [OOS 84]")
met(pwc_A[tr], mf[tr], "PWC-new A [OOS 84]")
met(pwc_B[tr], mf[tr], "PWC-new B [OOS 84]")
b, _ = ols(d.q.to_numpy()[te], y[te])
pred = (d.q.to_numpy()[tr] * b[0] + b[1]) * mt[tr]
met(pred, mf[tr], "GR q-only [OOS 84]", npar=2)

print("\n===== residual q-shape (the deficiency) =====")
r_old = (pwc_old_pred - mf) / mf * 100
r_A = (pwc_A - mf) / mf * 100
r_B = (pwc_B - mf) / mf * 100
for lab, r in (("old", r_old), ("A", r_A), ("B", r_B)):
    pr, pp = pearsonr(d.q, r)
    print(f"   corr(resid, q) [{lab:>3}] = {pr:+.4f} (p={pp:.2e})   corr(resid,lnMt) = {pearsonr(d.lnMt, r)[0]:+.4f}")
    bins = [0, .3, .5, .7, .85, 1.01]
    out = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (d.q >= lo) & (d.q < hi)
        out.append(f"q[{lo:.2f},{hi:.2f}): {r[m].mean():+.2f}% (n={m.sum()})")
    print("      bins: " + "  ".join(out))

print("\n===== residual spin correlation: does the corrected q-shape kill it? =====")
def pcorr(yy, x, ctrls):
    C = np.column_stack([d[c] for c in ctrls] + [np.ones(len(d))])
    yy = yy - C @ np.linalg.lstsq(C, yy, rcond=None)[0]
    xx = d[x] - C @ np.linalg.lstsq(C, d[x], rcond=None)[0]
    return pearsonr(xx, yy)
for lab, r in (("old", r_old), ("A", r_A), ("B", r_B)):
    print(f"   [{lab}] corr chi_eff={pearsonr(d.chi_eff, r)[0]:+.3f} chi_f={pearsonr(d.chi_f, r)[0]:+.3f} "
          f"| pcorr chi_eff|q={pcorr(r, 'chi_eff', ['q'])[0]:+.3f} "
          f"pcorr chi_f|q={pcorr(r, 'chi_f', ['q'])[0]:+.3f} "
          f"pcorr chi_eff|q,lnMt={pcorr(r, 'chi_eff', ['q', 'lnMt'])[0]:+.3f} "
          f"pcorr chi_f|q,lnMt={pcorr(r, 'chi_f', ['q', 'lnMt'])[0]:+.3f}")
    C = np.column_stack([d.q, d.lnMt, np.ones(len(d))])
    r_base = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]
    Xb = np.column_stack([C, d.chi_eff])
    r_chi = r - Xb @ np.linalg.lstsq(Xb, r, rcond=None)[0]
    print(f"       sd(resid)={r.std():.4f} -> after(q,lnMt): {r_base.std():.4f} -> after(q,lnMt,chi_eff): {r_chi.std():.4f}")

# how many events hit the pinch cap?
ncap = (d_cap < d_plain).sum()
print(f"\npinch-closure cap binds on {ncap}/188 events (q range {d.q[d_cap < d_plain].min():.3f}-{d.q[d_cap < d_plain].max():.3f})")

# ---- save full table for the parent ----
out = d[["event", "m1", "m2", "Mf", "q", "chi_eff", "chi_f"]].copy()
out["C1"] = C1; out["C2"] = C2
out["R1_km"] = R1 / 1e3; out["R2_km"] = R2 / 1e3
out["E1_km"] = E1 / 1e3; out["E2_km"] = E2 / 1e3
out["t1_km"] = t1 / 1e3; out["t2_km"] = t2 / 1e3
out["d_eff_km"] = d_cap / 1e3
out["E_old"] = E_old; out["E_new"] = E_B; out["S"] = S
out["dump_old"] = dump_old; out["dump_new"] = dump_B; out["dump_cat"] = mt - mf
out["Mf_old"] = pwc_old_pred; out["Mf_new"] = pwc_B
out["resid_old_pct"] = r_old; out["resid_new_pct"] = r_B
out.to_csv(r"C:\Users\jaden\Downloads\PWC-Check\qfix_figure8_results.csv", index=False)
print("wrote qfix_figure8_results.csv")
