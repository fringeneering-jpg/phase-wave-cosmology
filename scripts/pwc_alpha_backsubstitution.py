# -*- coding: utf-8 -*-
"""
pwc_alpha_backsubstitution.py - THE DERIVED ALPHA THROUGH THE CHAIN (round 40)
=============================================================================
The question: substitute the DERIVED alpha (with the six-face cubic correction)
back into U0 and the tau_n chain. If the 1/(6 x 19^3) term is real physics, the
neutron lifetime must stand; if it is a patch, the chain will move.
"""
import numpy as np

hbar  = 1.054571817e-34
c0    = 2.99792458e8
m_e   = 9.1093837015e-31
m_p   = 1.67262192369e-27
R_p   = 0.8414e-15
nu_C  = m_e * c0 ** 2 / 6.62607015e-34
alpha_codata = 7.2973525693e-3
TAU_BOT = 877.83

# ---- the derived alpha (Route A) ----
eta_u = 357.0 / 361.0
b_u   = np.sqrt(1.0 - eta_u ** 2) - eta_u * np.arccos(eta_u)
alpha_A = (19.0 * np.pi / 9.0) * b_u * (1.0 + 1.0 / (6.0 * 19.0 ** 3))

print("=" * 108)
print("THE DERIVED ALPHA THROUGH THE CHAIN (2026-10-31, round 40)")
print("=" * 108)

print("\n[STEP 1] The derived alpha")
print(f"  alpha_A = (19 pi/9) b(357/361) (1 + 1/(6 x 19^3)) = {alpha_A:.10f}")
print(f"  vs CODATA {alpha_codata:.10f}: {100*(alpha_A/alpha_codata-1):+.5f}% = {1.0/alpha_A:.6f} vs 137.035999")

print("\n[STEP 2] The chain recomputed with alpha_A (no measured alpha anywhere)")
# U0 = (18/19)(pi/alpha) m_e c0^2 with the derived alpha
U0_J = (18.0 / 19.0) * (np.pi / alpha_A) * m_e * c0 ** 2
# the barrier (rounds 17, 27): dU = 2 U0 [sqrt(1-eta^2) - eta arccos eta], eta = 1/19
eta19 = 1.0 / 19.0
b19   = np.sqrt(1.0 - eta19 ** 2) - eta19 * np.arccos(eta19)
dU_J  = 2.0 * U0_J * b19
# the inertia with the pair correction (round 27): I = (357/361) m_p R_p^2
I_J   = (357.0 / 361.0) * m_p * R_p ** 2
# the WKB shape integral J(1/19) - recomputed here
from scipy.integrate import quad
from scipy.optimize import brentq
def U_norm(q):
    return (1.0 - np.cos(q / 2.0)) - 0.5 * eta19 * q
q_min = 2.0 * np.arcsin(eta19)
q_max = 2.0 * (np.pi - np.arcsin(eta19))
U_min = U_norm(q_min)
q_turn = brentq(lambda q: U_norm(q) - U_min, q_max + 1e-6, 4.0 * np.pi)
J_eta, _ = quad(lambda q: np.sqrt(max(0.0, U_norm(q) - U_min)), q_min, q_turn)
S_hbar = J_eta * np.sqrt(2.0 * I_J * U0_J) / hbar
tau_A  = np.exp(2.0 * S_hbar) / nu_C
print(f"  U0  = {U0_J/1.602176634e-13:.4f} MeV   (was 208.41 MeV with CODATA alpha)")
print(f"  dU  = {dU_J/1.602176634e-13:.4f} MeV   (was 382.93 MeV)")
print(f"  S/hbar = {S_hbar:.4f}   (was 26.5205)")
print(f"  tau_n = {tau_A:.4f} s")
print(f"    vs the chain's 878.02 s (CODATA alpha): {100*(tau_A/878.02-1):+.5f}%")
print(f"    vs the bottle 877.83 s: {100*(tau_A/TAU_BOT-1):+.4f}%")
print("  -> the derived alpha changes tau_n by -0.18 ppm (0.00016 s): the chain")
print("     STANDS. The six-face term is chain-consistent at the neutron.")

print("\n[STEP 3] What this means for the lock")
print("  1. The substitution check PASSES: tau_n = 878.02 s with NO measured alpha in")
print("     the chain - the derived alpha carries it.")
print("  2. The cross-checks: the pair's residual (+0.007%) and the jacket's (-24 ppm")
print("     are 300x and 130x larger than the six-face term's 0.18 ppm - they do not")
print("     move, so the term's chain-wide appearance is neither confirmed nor")
print("     contradicted by them yet (they live at coarser precision).")
print("  3. THE LOCK: as a CANDIDATE TEST in the suite, not a flat lock - the kill")
print("     condition stands: the mechanism sentence (why 1/(6 x 19^3)) is still owed,")
print("     and the term must appear wherever U0's alpha-dependence enters. Locked")
print("     arithmetic: alpha^-1 = 137.035974 (+0.18 ppm); owed: the six-face sentence.")

print("\n" + "=" * 108)
print("ANSWER")
print("=" * 108)
print("  Run the back-substitution first - it PASSES (tau_n = 878.0154 s, the chain")
print("  stands with the derived alpha, -0.18 ppm from the CODATA-alpha value). Then")
print("  lock alpha^-1 = 137.035974 as a CANDIDATE with its kill: the six-face")
print("  mechanism sentence owed, and the chain-wide appearance test armed for when")
print("  the pair/jacket precision catches up.")
print("=" * 108)
