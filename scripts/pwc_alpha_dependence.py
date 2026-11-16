# -*- coding: utf-8 -*-
"""
pwc_alpha_dependence.py - EXAMINING THE ALPHA-DEPENDENCE INSIDE U0 (round 38)
=============================================================================
U0 = (18/19)(pi/alpha) m_e c0^2 - the jacket's closure is 'alpha-tied'. Examine:
  1. where alpha enters the chain and with what exponent;
  2. whether the untie-tilt match is actually an ALPHA EQUATION - i.e., whether
     the release threshold derives alpha from integers + pi.
"""
import numpy as np

alpha = 7.2973525693e-3
c0    = 2.99792458e8
m_e   = 9.1093837015e-31
hbar  = 1.054571817e-34
M_E_EV = m_e * c0 ** 2 / 1.602176634e-19

print("=" * 108)
print("THE ALPHA-DEPENDENCE INSIDE U0 (2026-10-31, round 38)")
print("=" * 108)

print("\n[STEP 1] Alpha's thread through the chain (exponents)")
print(f"  Y_bow  = 3 alpha h-bar c0 / (190 pi^4 r_e^4), r_e = alpha lambda_bar")
print(f"         -> Y_bow  ~ alpha^-3")
print(f"  rho_h  = 2 Y_bow / c0^2          ~ alpha^-3")
print(f"  rho_max = (2Y_bow/c0^2)^(33/29) rho0^(-4/29)  ~ alpha^(-99/29) = alpha^-3.414")
print(f"  U0     = (18/19)(pi/alpha) m_e c0^2   ~ alpha^-1")
print(f"  dU, S/hbar ~ alpha^-1/2;  ln(tau_n) ~ alpha^-1/2  (the exponential's argument)")
print("  -> alpha is not a decoration: the LIFETIME's logarithm rides on alpha^(-1/2).")

print("\n[STEP 2] The untie-tilt match, re-read as an alpha equation")
eta_u = 357.0 / 361.0
b_exact = np.sqrt(1.0 - eta_u ** 2) - eta_u * np.arccos(eta_u)
rhs = (9.0 / 19.0) * (alpha / np.pi)
print(f"  The jacket match: dU(eta=357/361) = (18/19)^2 m_e c0^2  [24 ppm]")
print(f"  Substitute dU = 2 U0 b, U0 = (18/19)(pi/alpha) m_e c0^2:")
print(f"    2 (18/19)(pi/alpha) m_e c0^2 b = (18/19)^2 m_e c0^2")
print(f"    -> b = (9/19)(alpha/pi)   [the match IS this equation]")
print(f"  Left side:  b(357/361) = {b_exact:.9f}")
print(f"  Right side: (9/19)(alpha/pi) = {rhs:.9f}")
print(f"  agreement: {100*(b_exact/rhs-1):+.4f}%")

print("\n[STEP 3] Solving the equation for alpha")
alpha_pred = (19.0 * np.pi / 9.0) * b_exact
print(f"  alpha = (19 pi/9) b(357/361) = {alpha_pred:.10f}")
print(f"  alpha_CODATA               = {alpha:.10f}")
print(f"  -> dev = {100*(alpha_pred/alpha-1):+.4f}% = {(alpha_pred/alpha-1)*1e6:+.1f} ppm")
print("  -> the untie tilt derives alpha from the integers 357/361 and pi, to -24 ppm")
print("     (the SAME residual as the jacket match - they are one identity). The")
print("     jacket's alpha-tie is therefore NOT an inherited defect - it is the")
print("     alpha equation itself: the release threshold OUTPUTS alpha.")

print("\n[STEP 4] The leading-order form (x = 4/361 small)")
x = 4.0 / 361.0
b_lead = (2.0 * np.sqrt(2.0) / 3.0) * x ** 1.5
alpha_lead = (19.0 * np.pi / 9.0) * b_lead
print(f"  b ~ (2 sqrt(2)/3) x^(3/2) = {b_lead:.9f}  (exact {b_exact:.9f})")
print(f"  alpha ~ (19 pi/9)(2 sqrt(2)/3)(4/361)^(3/2) = {alpha_lead:.10f}  ({100*(alpha_lead/alpha-1):+.4f}%)")
print("  -> the leading order alone gives alpha to 0.058% (579 ppm); the exact bracket")
print("     gives -24 ppm.")

print("\n" + "=" * 108)
print("THE EXAMINATION'S RESULT")
print("=" * 108)
print("  Tier 2's 'alpha-tied' label REFINES: the jacket does not merely inherit alpha -")
print("  the untie-tilt equation b(357/361) = (9/19)(alpha/pi) DERIVES alpha from the")
print("  release threshold's integers and pi, to -24 ppm. The residual (-24 ppm) is the")
print("  new sharpest target; the mechanism sentence (why the release tilt must equal")
print("  this bracket) is the owed physics.")
print("=" * 108)
