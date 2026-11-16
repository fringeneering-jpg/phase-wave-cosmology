# linear_hunt.py - the straight line's the signature (2026-10-17)
# The claim: when nailed, the heat's LINEAR in the framework's own variables.
# The corrected run: a FIXED observer distance X, the medium's own emissivity
# as the vent (no free f_vent), the dormant's only. The check: does T_obs sit
# on a straight line against the framework's (r_t . (1 + (v/C)^2)) predictor?
import numpy as np

T_MAX = 5.51e7
C_BOW = 958e3
c0 = 2.9979e8
G = 6.674e-11
a0 = 6.611e-11
pc = 3.0857e16

def reach(M):
    return np.sqrt(G * M / a0)

# the dormant anchors (the non-eating's)
dormant = [
    ("Sgr A*", 4.15e6, 0.0, 1.0e7),
    ("M87*",   6.50e9, 0.0, 2.3e7),
    ("M31*",   1.40e8, 0.0, 8.0e7),
]
# the fixed observer's distance: X = 100 pc (the stated reference)
X = 100.0 * pc

print("THE LINEAR HUNT - the fixed-X dormant's:")
print(f"  the predictor: T_pred = T_MAX . (r_t/X)^(1/2) . (1 + (v/C_bow)^2), X = 100 pc")
print()
print(f"  {'name':10s} {'r_t (pc)':>9s} {'pred factor':>11s} {'T_pred (K)':>11s} {'T_obs (K)':>10s} {'ratio':>7s}")
preds, obs = [], []
for name, M, v, T_obs in dormant:
    rt = reach(M * 1.989e30)
    fac = (rt / X) ** 0.5 * (1.0 + (v / C_BOW)**2 + (v / c0)**2)
    T_pred = T_MAX * fac
    preds.append(T_pred); obs.append(T_obs)
    print(f"  {name:10s} {rt/pc:9.1f} {fac:11.3f} {T_pred:11.2e} {T_obs:10.1e} {T_obs/T_pred:7.2f}")
print()
# the linear's test: the T_obs vs the T_pred's straight line's fit
preds = np.array(preds); obs = np.array(obs)
slope, intercept = np.polyfit(preds, obs, 1)
fit = slope * preds + intercept
resid = obs - fit
r2 = 1.0 - (resid**2).sum() / ((obs - obs.mean())**2).sum()
print(f"  the linear fit: T_obs = {slope:.4f} . T_pred + {intercept:.2e}")
print(f"  the R^2 = {r2:.4f}")
print()
print("the honest read: the straight line's the framework's tell. R^2 near 1 =")
print("the linear's shown; the scatter's the missing's variable's. The fixed-X")
print("run's the corrected's (the size's dependence's now real's).")
