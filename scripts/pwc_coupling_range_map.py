# -*- coding: utf-8 -*-
"""
pwc_coupling_range_map.py - THE (kappa, QUADRUPOLE) ALLOWED-REGION MAP (round 49)
================================================================================
Reconstruct the shape model's force equation and draw the map:
  F_in(R)  = alpha h-bar c0 / R^2 x [1 - q g (a0/R)^2]    (monopole + quadrupole)
  F_cent(R) = L^2 / (gamma(R) m_e R^3),  gamma = sqrt(1 + (L/(m_e c0 R))^2)
  g(kappa) = 1.5 (kappa - 1),  a0 = R_p,  L = gamma0 m_e v0 R0  (fixed)
Solve for the exterior root across kappa and coupling q; find the boundary where
the roots merge (saddle-node) - the allowed-region map.
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
L    = g0 * m_e * v0 * R0
A    = alpha * hbar * c0          # the Coulomb strength (J m)

def F_diff(R, q, kappa):
    g = 1.5 * (kappa - 1.0)
    fin = A / R ** 2 * (1.0 - q * g * (R_p / R) ** 2)
    gam = np.sqrt(1.0 + (L / (m_e * c0 * R)) ** 2)
    fce = L ** 2 / (gam * m_e * R ** 3)
    return fin - fce

def exterior_root(q, kappa, Rlo=1.0e-15, Rhi=8.0e-15):
    # find the largest root in [R_p, Rhi]; return None if none
    Rs = np.linspace(R_p, Rhi, 200001)
    Fs = F_diff(Rs, q, kappa)
    signs = np.sign(Fs)
    roots = []
    for i in range(len(Rs) - 1):
        if signs[i] != signs[i + 1] and signs[i] != 0:
            try:
                r = brentq(lambda R: F_diff(R, q, kappa), Rs[i], Rs[i + 1])
                roots.append(r)
            except Exception:
                pass
    if not roots:
        return None
    return max(roots)

print("=" * 108)
print("THE (kappa, QUADRUPOLE) ALLOWED-REGION MAP (2026-10-31, round 49)")
print("=" * 108)

print("\n[STEP 1] Sanity: the baseline at kappa = 1 (any coupling)")
for q in [0.05, 0.1, 0.3535]:
    r = exterior_root(q, 1.0)
    print(f"  q = {q:<7} -> R = {r*1e15:.5f} fm  (target 1.34027)")
print("  -> the quadrupole term vanishes at kappa = 1 (g = 0): baseline recovered.")

print("\n[STEP 2] The reconstructed tables vs the reported ones")
print(f"  {'kappa':>8} {'q=0.1 (mine)':>14} {'q=0.1 (reported)':>18} {'q=0.05 (mine)':>15} {'q=0.05 (reported)':>18} {'q=0.3535':>10}")
for kappa in [0.92, 0.96, 1.0, 1.04, 1.08]:
    r10 = exterior_root(0.1, kappa)
    r05 = exterior_root(0.05, kappa)
    r35 = exterior_root(0.3535, kappa)
    fmt = lambda x: f"{x*1e15:14.5f}" if x else f"{'NO ROOT':>14}"
    rep10 = {0.92: 1.181904, 0.96: 1.273430, 1.0: 1.340268, 1.04: 1.394682, 1.08: 1.441329}[kappa]
    rep05 = {0.92: 1.273430, 0.96: 1.308864, 1.0: 1.340268, 1.04: 1.368656, 1.08: 1.394682}[kappa]
    print(f"    {kappa:>8.2f} {fmt(r10)} {rep10:>18.5f} {fmt(r05)} {rep05:>18.5f} {fmt(r35)}")

print("\n[STEP 3] The allowed-region boundary (where the exterior roots merge and die)")
print(f"  {'kappa':>8} {'q_critical':>12} {'last R (fm)':>14}")
for kappa in [0.88, 0.90, 0.92, 0.94, 0.96, 0.98]:
    # bisect the largest q where a root still exists
    q_lo, q_hi = 0.0, 1.0
    for _ in range(60):
        q_mid = 0.5 * (q_lo + q_hi)
        if exterior_root(q_mid, kappa) is not None:
            q_lo = q_mid
        else:
            q_hi = q_mid
    q_c = q_lo
    r_last = exterior_root(q_c, kappa)
    print(f"    {kappa:>8.2f} {q_c:>12.4f} {r_last*1e15 if r_last else float('nan'):>14.5f}")
print("  -> for kappa > 1 the root ALWAYS exists (the repulsive near-surface term")
print("     cannot kill it); the boundary is the saddle-node curve on the loose side:")
print("     two roots merge and vanish as the coupling rises past q_c(kappa).")
print("     THE CONSTRAINT: the cage's derived (kappa, q) must land BELOW this curve.")

print("\n" + "=" * 108)
print("THE MAP'S VERDICT")
print("=" * 108)
print("  The allowed region is the plane below the saddle-node curve q_c(kappa) on the")
print("  loose side (and all couplings on the tight side). The cage's own geometry must")
print("  output a (kappa, q) inside it. The map is the fence; the derivation is the")
print("  thing that must land inside the fence.")
print("=" * 108)
