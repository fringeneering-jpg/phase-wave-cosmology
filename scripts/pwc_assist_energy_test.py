# -*- coding: utf-8 -*-
"""
pwc_assist_energy_test.py - THE ASSIST'S WORK vs THE BETA ENERGY BOOKKEEPING (round 62)
======================================================================================
The test: the open-end assist's work per pass must match the unspooling's energy
budget - the beta continuum's (E0 - E)^2 shape. Compute the real-scale work:
  strip charge = (17/19)e x (section fraction), at R_+ = 0.8056 fm
  open tip charge = f0 e, orbiting at R_e = 1.3403 fm
  F_tan = (17/19) f0 A R_+ sin(delta phi) / d^3,  W = integral F_tan R_e d phi
Compare against Q = 782.33 keV and the antineutrino's average share.
"""
import numpy as np
from scipy.integrate import quad

hbar = 1.054571817e-34
c0   = 2.99792458e8
alpha = 7.2973525693e-3
m_e  = 9.1093837015e-31
r_e  = alpha * hbar / (m_e * c0)
v0f  = 11.0 / 12.0
g0   = 1.0 / np.sqrt(1.0 - v0f ** 2)
R_e0 = r_e / (g0 * v0f ** 2)
f0   = (2.0 / 19.0) * (361.0 / 357.0)
A    = alpha * hbar * c0
R_plus = 0.8414e-15 / np.sqrt(12.0/11.0)
e     = 1.602176634e-19
KEV   = 1.602176634e-16          # J per keV

Q_BETA = 782.33          # keV - the weld's tariff (the full release energy)
E_NU_AVG = 547.0         # keV - the antineutrino's average share (~0.7 Q)

print("=" * 108)
print("THE ASSIST'S WORK vs THE BETA ENERGY BOOKKEEPING (2026-10-31, round 62)")
print("=" * 108)

print("\n[STEP 1] The real-scale assist work per pass")
const = (17.0/19.0) * f0 * A * R_plus * R_e0     # J m^2 (the geometry prefactor)
def integrand(dp):
    d2 = R_e0**2 + R_plus**2 - 2.0*R_e0*R_plus*np.cos(dp)
    return np.sin(dp) / d2**1.5
I, _ = quad(integrand, 0.0, 0.5)                # the one-sided approach arc
W_full = const * I
print(f"  full-ring section:  W = (17/19) f0 A R_+ R_e x integral = {W_full/KEV:.2f} keV per pass")
for name, frac in [("half-ring section", 0.5), ("sixth-ring (a cage face)", 1.0/6.0)]:
    W = W_full * frac
    print(f"  {name:<24} W = {W/KEV:.2f} keV per pass")

print("\n[STEP 2] The beta bookkeeping targets")
print(f"  Q (the full release)      = {Q_BETA:.2f} keV")
print(f"  antineutrino average share = {E_NU_AVG:.2f} keV  (~0.7 Q)")
print(f"  electron's endpoint energy  = 782.33 - 510.999 = 271.3 keV")
print(f"  ratios: W_full/Q = {W_full/KEV/Q_BETA:.5f}  vs f0 = {f0:.5f}  vs 2/19 = {2.0/19.0:.5f}")

print("\n[STEP 3] The comparison - does the single-pass assist close?")
print(f"  W(full ring) = {W_full/KEV:.1f} keV vs the antineutrino's {E_NU_AVG:.0f} keV:")
print(f"  -> SHORT by {E_NU_AVG/(W_full/KEV):.1f}x. The one-pass assist at the natural")
print("     scales does NOT close the unspooling's energy on its own.")
print("  The match would need: (a) a section factor (the 1/6 face makes it WORSE, not")
print("     better), (b) a different pass structure (multiple strips adding per pass,")
print("     or the tip's arc spanning more of the orbit), or (c) the assist being one")
print("     term among several in the unspooling's budget (the weld's release itself).")
print(f"  CANDIDATE: the assist is REAL ({W_full/KEV:.1f} keV/pass - Q's ~9%, near f0")
print(f"  = 0.106 but not equal - flagged), but the single-pass closure is not")
print("  automatic - the pass structure is the next named item.")

print("\n" + "=" * 108)
print("THE TEST'S VERDICT")
print("=" * 108)
print(f"  The open-end assist delivers ~{W_full/KEV:.0f} keV per pass at the full-ring")
print(f"  section - the right decade ({W_full/KEV/Q_BETA*100:.0f}% of Q) but {E_NU_AVG/(W_full/KEV):.1f}x")
print("  short of the antineutrino's 547 keV share.")
print("  The mechanism is quantitatively ALIVE but not CLOSED: the section/pass")
print("  structure must supply the remaining factor. The (E0 - E)^2 continuum's")
print("  bookkeeping is the arbiter - the next derivation is the pass count, named")
print("  and printed, not chosen.")
print("=" * 108)
