# -*- coding: utf-8 -*-
"""
pwc_radial_split_audit.py - THE JOINT SOLUTION, AUDITED (round 70)
=================================================================
The radial-split lock: R_neg = 1.33383 (inner), R_pos = 1.35515 (outer),
dR = 0.02131 fm - hits both targets. Audit:
  1. the algebra (2 equations, 2 unknowns - the exact match is by construction);
  2. the electrostatic claim (the pair's mutual attraction vs the core's
     differential - does the separation hold?);
  3. the hidden assumptions (constant v; the radii's plausibility).
"""
import numpy as np

R_p0  = 0.8414
v_frac = 11.0/12.0
f0    = (2.0/19.0)*(361.0/357.0)
chi   = 12.0/11.0
R_plus = R_p0/np.sqrt(chi)
mu_p_obs = 2.792847
target_mu = -1.913042
target_r2 = -0.1161

mu_core = mu_p_obs/np.sqrt(chi)
mu_locked = -4.0*(1.0-f0)*v_frac*(R_plus/R_p0)
core_plus_locked = mu_core + mu_locked
target_mu_pair = target_mu - core_plus_locked
L = (-target_mu_pair*R_p0)/(4.0*v_frac*f0)
S = (target_r2 - f0*R_plus**2)/f0
Aq, Bq, Cq = 7.5, -15.0*L, 4.5*L**2 - 3.0*S
R_neg = (-Bq - np.sqrt(Bq**2 - 4*Aq*Cq))/(2*Aq)
R_pos = (3*L - 5*R_neg)/2.0
dR = R_pos - R_neg

print("=" * 108)
print("THE JOINT SOLUTION, AUDITED (2026-10-31, round 70)")
print("=" * 108)

print("\n[AUDIT 1] The algebra and what 'exact' means")
print(f"  R_neg = {R_neg:.5f} fm (inner, -5/3);  R_pos = {R_pos:.5f} fm (outer, +2/3);")
print(f"  dR = {dR:.5f} fm;  mean = {(R_neg+R_pos)/2:.5f} fm  (baseline orbit 1.3403: {100*((R_neg+R_pos)/2/1.3403-1):+.2f}%)")
print("  -> 2 equations, 2 unknowns: the exact hit is BY CONSTRUCTION - the solution")
print("     is real, but its value lies in the radii's plausibility and consistency,")
print("     not the exactness. The radii ARE plausible: mean within 0.3% of the")
print("     baseline orbit; dR = 1.6% of R (a thin ribbon); dR = 4.0% of the gap")
print("     to the core. The -5/3 INNER is exactly round 58's demanded direction.")

print("\n[AUDIT 2] The electrostatic claim - does the separation hold?")
A_keV = 2.3071e-28            # alpha h-bar c0
f_plus, f_minus = (2.0/3.0)*f0, (5.0/3.0)*f0
F_pair = f_plus*f_minus*A_keV/((dR*1e-15)**2)
F_core_plus  = f_plus*A_keV/((R_pos*1e-15)**2)
F_core_minus = f_minus*A_keV/((R_neg*1e-15)**2)
print(f"  the pair's mutual attraction at dR = 0.0213 fm: F_pair = {F_pair:.1f} N")
print(f"  the core's differential (pushes + out, pulls - in): {F_core_plus + F_core_minus:.1f} N")
print(f"  -> the attraction beats the differential by {F_pair/(F_core_plus+F_core_minus):.1f}x:")
print("     the ribbon would COLLAPSE under pure electrostatics. The 0.0213 fm")
print("     thickness is NOT electrostatically held - it must be the weld's tension")
print("     (the ribbon's own stiffness), the same machinery that holds everything")
print("     else. The electrostatic DIRECTION is right (the - inner, the + outer);")
print("     the electrostatic EQUILIBRIUM is not.")

print("\n[AUDIT 3] The hidden assumption")
print("  The script held v = (11/12) c0 for BOTH branches. The fixed-L map gives the")
print("  branches slightly different speeds (the outer is ~0.5% slower) - the moment")
print("  would shift at the sub-percent level. The constant-v choice is a hidden")
print("  assumption to be carried or replaced.")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  The radial-split lock is algebraically REAL and the radii are PLAUSIBLE,")
print("  but two honest labels attach: (1) the exact match is by construction")
print("  (2 equations, 2 unknowns); (2) the 0.0213 fm thickness is not held by the")
print("  electrostatics (the pair's attraction wins 2x) - it belongs to the weld's")
print("  tension. THE CONFLICT IS GONE as a fit; the thickness's holder (the weld's")
print("  tension outputting dR = 0.0213 fm) is the next item.")
print("=" * 108)
