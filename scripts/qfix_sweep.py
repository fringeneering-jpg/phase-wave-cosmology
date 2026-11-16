"""Sweep: zero-parameter geometric fight-length candidates for the figure-8 contact energy.
E = G * (num) / (2 c0^2 d_eff); drop = min(E, S). All constants locked. (scratch, session workspace)"""
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
m1 = d.m1.to_numpy(); m2 = d.m2.to_numpy(); mf = d.Mf.to_numpy(); mt = m1 + m2
q = d.m2.to_numpy() / d.m1.to_numpy()
C1 = np.array([core(m) for m in m1]); C2 = np.array([core(m) for m in m2])
E1 = np.sqrt(G * m1 * MS / A_MAX); E2 = np.sqrt(G * m2 * MS / A_MAX)
R1 = (3 * C1 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
R2 = (3 * C2 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
t1 = E1 - R1; t2 = E2 - R2
S = K * (C1 ** (2 / 3) + C2 ** (2 / 3) - (C1 + C2) ** (2 / 3))
E_old = G * (m1 * MS) * (m2 * MS) / (2 * (E1 + E2) * C0 ** 2) / MS

# figure-8 waist at core-touch d0 = R1+R2: cap heights h1 (big side), h2 (small side)
d0 = R1 + R2
x1 = (d0 ** 2 + E1 ** 2 - E2 ** 2) / (2 * d0)
rho_p = np.sqrt(np.clip(E1 ** 2 - x1 ** 2, 0, None))
h1 = E1 - x1
h2 = E2 - (d0 - x1)          # = E2 + x1 - d0; h1+h2 = t1+t2 exactly
assert np.allclose(h1 + h2, t1 + t2, rtol=1e-9)

def E_of(num1, num2, d_eff):
    return G * (num1 * MS) * (num2 * MS) / (2 * d_eff * C0 ** 2) / MS

cands = {
    "old: M1M2 / (E1+E2)":                 (m1, m2, E1 + E2),
    "C1C2 / (t1+t2)":                      (C1, C2, t1 + t2),
    "C1C2 / 2sqrt(h1 h2)":                 (C1, C2, 2 * np.sqrt(h1 * h2)),
    "C1C2 / 4h1h2/(h1+h2)  [harm.mean]":   (C1, C2, 4 * h1 * h2 / (h1 + h2)),
    "C1C2 / 2 min(h1,h2)":                 (C1, C2, 2 * np.minimum(h1, h2)),
    "C1C2 / 2 max(h1,h2)":                 (C1, C2, 2 * np.maximum(h1, h2)),
    "C1C2 / rho_p":                        (C1, C2, rho_p),
    "C1C2 / 2 rho_p":                      (C1, C2, 2 * rho_p),
    "C1C2 / (E1+E2)":                      (C1, C2, E1 + E2),
    "M1M2 / (t1+t2)":                      (m1, m2, t1 + t2),
    "M1M2 / 2sqrt(h1 h2)":                 (m1, m2, 2 * np.sqrt(h1 * h2)),
    "M1M2 / 2 rho_p":                      (m1, m2, 2 * rho_p),
    "M1M2 / 4h1h2/(h1+h2)":                (m1, m2, 4 * h1 * h2 / (h1 + h2)),
    "C1C2 / sqrt((t1+t2)(R1+R2))":         (C1, C2, np.sqrt((t1 + t2) * (R1 + R2))),
    "M1M2 / sqrt((t1+t2)(R1+R2))":         (m1, m2, np.sqrt((t1 + t2) * (R1 + R2))),
    "C1C2 / sqrt((E1+E2)(R1+R2))":         (C1, C2, np.sqrt((E1 + E2) * (R1 + R2))),
    "M1M2 / sqrt((E1+E2)(R1+R2))":         (m1, m2, np.sqrt((E1 + E2) * (R1 + R2))),
    "C1C2 / (t1+t2) * (1 - |h1-h2|/(h1+h2))": (C1, C2, (t1 + t2) * (1 - np.abs(h1 - h2) / (h1 + h2))),
    "C1C2 / (t1+t2)*(1+min(R1,R2)/max(R1,R2))/2": (C1, C2, (t1 + t2) * (1 + np.minimum(R1, R2) / np.maximum(R1, R2)) / 2),
}
tr = d.event.isin(b4.event).to_numpy(); te = ~tr
print(f"{'candidate':<44} {'E914':>6} {'sd188':>7} {'sd104':>7} {'sd84':>7} {'mean104':>7} {'corr q':>7} {'corr chi':>9}")
for name, (n1, n2, deff) in cands.items():
    E = E_of(n1, n2, deff)
    drop = np.minimum(E, S)
    pred = mt - drop
    e = (pred - mf) / mf * 100
    i914 = d.event.to_numpy() == "GW150914"
    # GW150914 not in the 188 blind set; use the DEV row of merg for the closure check
    row = merg[merg.event == "GW150914"].iloc[0]
    Cc = core(row.m1); E1c = np.sqrt(G * row.m1 * MS / A_MAX)
    print(f"{name:<44} {E[0]:6.2f} {e.std():7.3f} {e[te].std():7.3f} {e[tr].std():7.3f} "
          f"{e[te].mean():+7.3f} {pearsonr(q, e)[0]:+7.3f} {pearsonr(d.chi_eff, e)[0]:+9.3f}")

# implied d_eff for the E-limited events of the best C1C2 family (t1+t2 rule)
E_A = E_of(C1, C2, t1 + t2)
mask = (E_A < S)
d_impl = (t1 + t2) * E_A / (mt - mf)
print("\nimplied d_impl/(t1+t2) = E_new/dump_cat for E-limited events, in q bins:")
for lo, hi in [(0, .3), (.3, .5), (.5, .7), (.7, .85), (.85, 1.01)]:
    m = (q >= lo) & (q < hi) & mask
    if m.sum() >= 2:
        print(f"   q[{lo:.2f},{hi:.2f}) n={m.sum():3d}: median ratio={np.median(d_impl[m] / (t1[m] + t2[m])):.3f} "
              f"mean={np.mean(d_impl[m] / (t1[m] + t2[m])):.3f}")
print("   in Mt bins:")
for lo, hi in [(0, 25), (25, 40), (40, 60), (60, 100)]:
    m = (mt >= lo) & (mt < hi) & mask
    if m.sum() >= 2:
        print(f"   Mt[{lo:3d},{hi:3d}) n={m.sum():3d}: median ratio={np.median(d_impl[m] / (t1[m] + t2[m])):.3f}")
print("\nGW150914 E values (closure target 2.957, catalog 3.0):")
row = merg[merg.event == "GW150914"].iloc[0]
Cc1, Cc2 = core(row.m1), core(row.m2)
Ec1 = np.sqrt(G * row.m1 * MS / A_MAX); Ec2 = np.sqrt(G * row.m2 * MS / A_MAX)
Rc1 = (3 * Cc1 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3); Rc2 = (3 * Cc2 * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
tc1 = Ec1 - Rc1; tc2 = Ec2 - Rc2
for name, deff in (("t1+t2", tc1 + tc2), ("2sqrt(h1h2)", 2 * np.sqrt((Ec1 - (Rc1 + Rc2)) * 0 + 0)),
                   ("E1+E2 (old)", Ec1 + Ec2)):
    pass
x1c = ((Rc1 + Rc2) ** 2 + Ec1 ** 2 - Ec2 ** 2) / (2 * (Rc1 + Rc2))
h1c = Ec1 - x1c; h2c = Ec2 + x1c - Rc1 - Rc2
for name, deff in (("t1+t2", tc1 + tc2), ("2sqrt(h1h2)", 2 * np.sqrt(h1c * h2c)),
                   ("4h1h2/(h1+h2)", 4 * h1c * h2c / (h1c + h2c)), ("2rho_p", 2 * np.sqrt(Ec1 ** 2 - x1c ** 2))):
    print(f"   d={name:<16} {deff/1e3:7.1f} km  ->  E = {G*(Cc1*MS)*(Cc2*MS)/(2*deff*C0**2)/MS:.3f} Msun")
