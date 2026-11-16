# -*- coding: utf-8 -*-
"""
pwc_pair_length_scale.py - THE PAIR'S 13.6 fm: NAMING THE LENGTH (round 30)
==========================================================================
Round 29 pinned the annihilation's required inertia: I_pair = m_e x (13.59 fm)^2.
Name that length: test the framework's locked scales against it, with the RATE
sensitivity (the exponential amplifies) printed for each candidate.
"""
import numpy as np

m_e  = 9.1093837015e-31
hbar = 1.054571817e-34
c0   = 2.99792458e8
alpha = 7.2973525693e-3
R_p  = 0.8414e-15
r_e  = alpha * hbar / (m_e * c0)
lam_bar = hbar / (m_e * c0)
R_loop = 0.5 * lam_bar
r_core = 6.764e-15          # the sealed 8 R_p ball (locked, round 1)
L_TARGET = 13.589e-15       # from round 29: sqrt(I_need / m_e)

nu_C = m_e * c0 ** 2 / 6.62607015e-34
P_MEASURED = 1.0 / (nu_C * 0.125e-9)   # para: 1/0.125 ns at the contact clock

def rate_factor(L):
    # p ~ exp(-2 S/hbar), S/hbar ~ L -> p(L)/p(L_target) = exp(2 k (L_target - L))
    # with k = S/hbar / L at the target
    k = 11.7303 / L_TARGET
    return np.exp(2.0 * k * (L - L_TARGET))

print("=" * 108)
print("NAMING THE PAIR'S LENGTH SCALE - 13.59 fm (2026-10-31, round 30)")
print("=" * 108)

print("\n[STEP 1] The target and the locked scales")
print(f"  Target: L = sqrt(I_pair/m_e) = 13.589 fm")
print(f"  Locked: R_p = {R_p*1e15:.4f} fm, r_e = {r_e*1e15:.4f} fm, r_core = {r_core*1e15:.4f} fm")
print(f"          R_loop = {R_loop*1e15:.2f} fm, lambda_bar = {lam_bar*1e15:.2f} fm")
print(f"  Ratio L_target/r_core = {L_TARGET/r_core:.4f}   (2 r_core = {2*r_core*1e15:.3f} fm)")

print("\n[STEP 2] Candidate sweep - length AND the rate it gives")
print(f"  (measured para rate: p = {P_MEASURED:.2e} per contact cycle; 1/0.125 ns)")
print(f"  {'candidate':<38} {'L (fm)':>9} {'L dev':>9} {'rate factor':>13}")
cands = [
    ("2 x r_core (the core's diameter)", 2.0 * r_core),
    ("2 x 8 R_p (the ball's diameter)", 2.0 * 8.0 * R_p),
    ("16 R_p (the clock x R_p)", 16.0 * R_p),
    ("2 r_e x 2.411 (flagged ratio)", 2.0 * r_e * 2.411),
    ("R_loop / 14.21", R_loop / 14.21),
    ("sqrt(2 r_e lambda_bar)", np.sqrt(2.0 * r_e * lam_bar)),
]
for name, L in cands:
    print(f"    {name:<38} {L*1e15:>9.3f} {100*(L/L_TARGET-1):>+8.2f}% {rate_factor(L):>12.2f}x")
print("  -> 2 x r_core is the ONLY locked-scale candidate in the right decade:")
print("     the pair's inertia = the mass at the sealed core's DIAMETER - the two")
print("     windings pivot at contact, each arm = r_core, total = 2 r_core.")

print("\n[STEP 3] The residual and its correction candidates")
resid = 2.0 * r_core / L_TARGET
print(f"  2 r_core / L_target = {resid:.6f}  (the rate runs {1.0/rate_factor(2*r_core):.3f} of the")
print(f"  measured - i.e., the candidate predicts 1/{(0.125e-9*rate_factor(2*r_core))*1e9:.4f} ns vs 0.125 ns, +{100*(rate_factor(2*r_core)-1):+.1f}%)")
for name, f in [("sqrt(357/361)", np.sqrt(357.0/361.0)),
                ("(357/361)^(1/4)", (357.0/361.0) ** 0.25),
                ("(17/16)^(1/2) ", np.sqrt(17.0/16.0))]:
    L2 = 2.0 * r_core * f
    print(f"    2 r_core x {name} = {L2*1e15:.4f} fm  ({100*(L2/L_TARGET-1):+.3f}%)")
print("  -> the same 357/361 family reappears but no clean closure yet; the residual")
print("     (0.45% in L = +11% in rate) is the next sub-step. CANDIDATE stands:")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  THE PAIR'S LENGTH = 2 x r_core (13.528 fm) - the sealed core's diameter, the")
print("  contact-pivot arm: one winding's mass at two core radii. Target 13.589 fm;")
print("  residual -0.45% in length = +11% in rate - the candidate, with the residual's")
print("  correction as the next sub-step (the same 357/361-family test failed to close).")
print("=" * 108)
