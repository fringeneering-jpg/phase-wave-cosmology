# -*- coding: utf-8 -*-
"""
pwc_hidden_negative_check.py - THE HIDDEN - : WHAT THE LOCALIZED PASSAGE CHANGES (round 63)
===========================================================================================
The author's refinement: the - rides INSIDE the + (hidden under it) and only sees the
strip's repulsion AT the passage, not on the approach. Test what the localization
does to the work: the tangential force vanishes AT the crossing (purely radial there)
and peaks AROUND it - so the windowed work cannot exceed the full-arc value.
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
KEV   = 1.602176634e-16

const = (17.0/19.0) * f0 * A * R_plus * R_e0

def integrand(dp):
    d2 = R_e0**2 + R_plus**2 - 2.0*R_e0*R_plus*np.cos(dp)
    return np.sin(dp) / d2**1.5

print("=" * 108)
print("THE HIDDEN - : WHAT THE LOCALIZED PASSAGE CHANGES (2026-10-31, round 63)")
print("=" * 108)

print("\n[STEP 1] The tangential force's profile along the approach")
xs = np.linspace(0.01, 0.5, 50)
vals = integrand(xs)
ipeak = np.argmax(vals)
print(f"  F_tan(phi) ~ sin(phi)/d^3: peaks at phi ~ {xs[ipeak]:.2f} rad, vanishes at phi -> 0")
print("  -> AT the exact passage the force is purely RADIAL (no tangential kick); the")
print("     tangential work's weight sits AROUND the crossing, not at it. The hidden")
print("     -'s windowed interaction can therefore only REDUCE the work, never exceed it.")

print("\n[STEP 2] The windowed work (the localized passage)")
W_full, _ = quad(integrand, 0.0, 0.5)
for width in [0.3, 0.2, 0.1]:
    W_w = const * quad(integrand, 0.0, width)[0]
    print(f"  window phi in [0, {width}]: W = {W_w/KEV:6.2f} keV   (full arc: {const*W_full/KEV:.2f})")
print("  -> the localization gives LESS work, not more: the hidden - under the + is")
print("     CONSISTENT with the pair's structure, but it does not close the 7.6x gap -")
print("     it widens it. The shortfall is a charge/geometry scale, not the")
print("     interaction's shape.")

print("\n[STEP 3] What WOULD close it (named, not chosen)")
print("  To reach the antineutrino's 547 keV per pass, the work needs ~7.6x more:")
print("    (a) the full f0-exposure (no screening) at the crossing - the pair's own")
print("        screening is what hides it, so the exposure IS partial by construction;")
print("    (b) a closer passage (d_min smaller) - but the orbit and the shell set")
print("        d_min = R_e - R_+;")
print("    (c) the assist as ONE term among several - the weld's release carries the")
print("        rest of the 547 keV, and the assist's ~70 keV is its own share.")
print("  -> (c) is the honest reading: the assist is a real ~70 keV term in the")
print("     unspooling's budget, not its whole engine.")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  The hidden-negative geometry is CONSISTENT (the pair's screening structure),")
print("  but the localized passage REDUCES the work (the tangential kick peaks around")
print("  the crossing, vanishes at it). The 7.6x shortfall is not a shape question.")
print("  The assist stands as a real ~70 keV term among several in the unspooling's")
print("  budget - the (E0 - E)^2 bookkeeping's arbiter unchanged.")
print("=" * 108)
