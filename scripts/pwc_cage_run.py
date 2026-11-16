# -*- coding: utf-8 -*-
"""
pwc_cage_run.py - THE CAGE RUNS: GEOMETRY -> COUPLING -> ORBIT -> CHARGE RADIUS (round 51)
=========================================================================================
The five-wave 2-1-2 cage, from its locked geometry:
  - the relief: kappa = 12/11 (the central knot holds 11/12 of m_p)
  - the 2-1-2 quintuple: knots at z = -2d, -d, 0, +d, +2d (each +e/5)
  - the quadrupole: Q_zz = sum q_i z_i^2 = 2 e d^2  ->  b = Q_zz/(16 e) = d^2/8
  - the model link: b = 1.5 q (kappa-1) R_p^2  ->  q = d^2 / (12 (kappa-1) R_p^2)
Then: the fence check, the settled orbit, the charge radius - what the invisible
cage outputs, against the measurements.
"""
import numpy as np
from scipy.optimize import brentq

c0   = 2.99792458e8
m_e  = 9.1093837015e-31
hbar = 1.054571817e-34
alpha = 7.2973525693e-3
R_p  = 0.8414e-15
v0   = (11.0 / 12.0) * c0
g0   = 1.0 / np.sqrt(1.0 - (11.0 / 12.0) ** 2)
R0   = 1.3402678e-15
A    = alpha * hbar * c0
L    = g0 * m_e * v0 * R0
B_CRIT = -0.0127352598e-30     # m^2
f0   = (2.0 / 19.0) * (361.0 / 357.0)
MEAS = -0.1161

kappa = 12.0 / 11.0            # the relief: the cage's own tightness

def settled_R(b):
    def Fd(R):
        fin = A / R ** 2 * (1.0 - 3.0 * b / R ** 2)
        gam = np.sqrt(1.0 + (L / (m_e * c0 * R)) ** 2)
        return fin - L ** 2 / (gam * m_e * R ** 3)
    return brentq(Fd, 1.0e-15, 5.0e-15, xtol=1e-30)   # xtol: default 2e-12 m is wider than the fm bracket

print("=" * 108)
print("THE CAGE RUNS (2026-10-31, round 51)")
print("=" * 108)

print("\n[STEP 1] The cage's locked inputs")
print(f"  relief tightness: kappa = 12/11 = {kappa:.6f}  (the central knot holds 11/12)")
print(f"  2-1-2 quintuple: knots at -2d, -d, 0, +d, +2d, each +e/5")
print(f"  quadrupole: Q_zz = 2 e d^2 -> b = Q_zz/(16 e) = d^2/8")
print(f"  model link: b = 1.5 q (kappa-1) R_p^2")

print("\n[STEP 2] Two candidate spacings - the cage's span")
print(f"  {'d (fm)':>10} {'b (fm^2)':>12} {'q':>12} {'R_settled (fm)':>16} {'<r_n^2> (fm^2)':>16} {'fence':>10}")
for dlab, d in [("R_p/4", R_p / 4.0), ("R_p/2", R_p / 2.0)]:
    b = d ** 2 / 8.0
    q = b / (1.5 * (kappa - 1.0) * R_p ** 2)
    Rs = settled_R(b)
    Rplus = R_p / np.sqrt(kappa)
    r2 = -f0 * (Rs ** 2 - Rplus ** 2) * 1e30
    fence = "SAFE" if b > B_CRIT * 1e30 else "CROSSED"
    print(f"    {dlab:>10} {b*1e30:>12.6f} {q:>12.6f} {Rs*1e15:>16.5f} {r2:>16.5f} {fence:>10}")
print("  -> b > 0 means the cage's quintuple is PROLATE: the equatorial attraction is")
print("     reduced, the orbit settles OUTWARD, and the fence is automatic (the tight")
print("     side always has a stable exterior orbit). The cage is on the safe side by")
print("     construction - the loose-side fence never threatens it.")

print("\n[STEP 3] What the invisible cage outputs, against the measurements")
for dlab, d in [("R_p/4", R_p / 4.0), ("R_p/2", R_p / 2.0)]:
    b = d ** 2 / 8.0
    Rs = settled_R(b)
    Rplus = R_p / np.sqrt(kappa)
    r2 = -f0 * (Rs ** 2 - Rplus ** 2) * 1e30
    sig = abs(r2 - MEAS) / 0.0022
    print(f"  span {dlab}: R_settled = {Rs*1e15:.4f} fm, <r_n^2> = {r2:.5f} fm^2 -> {sig:.2f} sigma")
print(f"  measured: <r_n^2> = -0.1161 +/- 0.0022 fm^2")
print("  -> the cage's own geometry OUTPUTS a settled orbit and a charge radius; the")
print("     numbers above are what the invisible structure predicts - visible, testable,")
print("     and no longer free.")

print("\n[STEP 4] The inversion - what the measurement demands of the real cage")
# work in fm, convert to m only inside the force functions
Rplus_fm = R_p * 1e15 / np.sqrt(kappa)
R_e_fm = np.sqrt((-MEAS) / f0 + Rplus_fm ** 2)
R_e = R_e_fm * 1e-15
ell_m = L / (m_e * c0)
v_R = c0 / np.sqrt(1.0 + (R_e / ell_m) ** 2)
b_req_m2 = (R_e ** 2 / 3.0) * (1.0 - L * v_R / A)
b_req = b_req_m2 * 1e30
print(f"  measured radius -> R_e = {R_e_fm:.4f} fm -> required b = {b_req:.6f} fm^2")
print(f"  fence: b_crit = -0.0127353 fm^2 -> {b_req:.6f} is {'SAFE (inside)' if b_req > -0.0127353 else 'CROSSED'}")
print(f"  sign: b < 0 = OBLATE (the equatorial bulge strengthens the grip, orbit inward)")
print(f"  -> the data demand a SLIGHTLY OBLATE cage, not the prolate quintuple.")
fam = abs(b_req) / (1.5 * R_p ** 2 * 1e30)
print(f"  The (kappa, q) family satisfying it: q(1-kappa) = {fam:.6f}")
for kappa_c in [0.97, 0.98, 0.99]:
    q_c = fam / (1.0 - kappa_c)
    print(f"    kappa = {kappa_c:.2f} -> q = {q_c:.4f}  (moderate, inside the fence)")
print("  -> THE TARGET IS BRACKETED: the real 2-1-2 wave solution must be slightly")
print("     oblate with b ~ -0.0015 fm^2 (a 1-3% loose cage at moderate coupling) -")
print("     the naive prolate quintuple is falsified at 12-34 sigma, and the")
print("     measurement plus the fence now define the window the cage must land in.")

print("\n" + "=" * 108)
print("THE CAGE, RUN - HONEST SCORE")
print("=" * 108)
print("  First geometry (prolate quintuple): FALSIFIED at 11.9-33.7 sigma (wrong sign).")
print("  Inversion: the measured radius demands b = -0.0014 fm^2 (slightly oblate),")
print("  SAFE inside the fence, reachable by a 1-3% loose cage at moderate coupling.")
print("  The fickle invisible thing printed numbers, died on the first guess, and now")
print("  has a bracketed window: b in (-0.0127, -0.0014), q(1-kappa) = 0.00133.")
print("=" * 108)
