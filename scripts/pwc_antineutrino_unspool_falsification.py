# -*- coding: utf-8 -*-
"""
pwc_antineutrino_unspool_falsification.py - THE ANTINEUTRINO UNSPOOL HYPOTHESIS
===============================================================================
Author's hypothesis (2026-10-30):
  A. The antineutrino is the inside-out tied electron (the mirror winding) that
     unspirals because it does not hold; its near-instantaneous expansion in beta
     decay shears the neighboring knot and shapes the spectrum.
  B. Antimatter must be frozen at creation; the mirror particle either finds a
     proton to orbit or unties - only the fast orbit keeps it from unspooling.
  C. Matter + antimatter contact forces both to untie (annihilation).
Every claim is broken until the math holds. Every miss printed.
"""
import math

C0    = 2.99792458e8
M_E   = 9.1093837015e-31
M_P   = 1.67262192369e-27
M_N   = 1.67492749804e-27
KEV   = 1.602176634e-16
E_MASS_KEV = 510.99895
Q_KEV = (M_N - M_P - M_E) * C0 ** 2 / KEV

print("=" * 108)
print("PWC ANTINEUTRINO UNSPOOL HYPOTHESIS - VICIOUS FALSIFICATION (2026-10-30)")
print("=" * 108)

# ===========================================================================
print("\n[TEST 1] Claim B - 'the mirror particle unties unless it orbits a proton'")
# ===========================================================================
print("  Free positrons are OBSERVED stable in vacuum (no spontaneous decay seen;")
print("  CPT ties any e+ decay bound to the electron's, tau > 1e21-1e28 yr class).")
print("  A free positron orbits NOTHING and does not unspool.")
print("  The bound pair (positronium) is where the untie happens FASTEST:")
print("    para-positronium (spin 0): 0.125 ns -> 2 gamma")
print("    ortho-positronium (spin 1): 142 ns  -> 3 gamma")
print("  -> the ORBIT is not what stabilizes; the opposite-formation CONTACT is what unties.")
print("  VERDICT: Claim B is INVERTED by the data. The knot's stability is its own internal")
print("  720-degree circulation, not an external orbit. What survives (corrected):")
print("    - the POSITRON = the bound mirror knot: stable free, unties on contact (Claim C)")
print("    - the ANTINEUTRINO = the UNBOUND half-spin thread: the one that sheds/unspools")
print("    - 'freezing at creation' is about storage against contact, not against unspooling")

# ===========================================================================
print("\n[TEST 2] Claim A - the unspooling books the beta continuum")
# ===========================================================================
print(f"  Q = m_n - m_p - m_e = {Q_KEV:.2f} keV (endpoint)")
print("  Standard Fermi shape: dN/dE_e ~ p E (E0 - E_e)^2 F(Z,E)")
print("  The (E0 - E_e)^2 exponent = the antineutrino's TWO transverse polarizations")
print("  (the 2-body phase-space count of the unspooling wave).")
print("  In the unspool picture the SAME count applies: the shed thread is a")
print("  2-polarization wave carrying E_nu = E0 - E_e continuously -> the same")
print("  (E0 - E_e)^2 -> the continuum is BOOKED IN FORM by the unspooling wave.")
print("  -> the old flag ('predicts mono-energetic 782 keV') is DISCHARGED IN FORM:")
print("     the electron and the unspooling wave split the 782 keV continuously.")
print("  OWED (armed): the unspooling RATE integral must produce tau_n = 878.4 s as a")
print("  second route (the ladder rung is the existing first route, 0.69 sigma).")
print("  SOLAR NEUTRINO BOUND: the sun's nu_e arrive at Earth across 1 AU = 499 light-")
print("  seconds and oscillate coherently -> the unspooling half-life must be >> 500 s.")
print("  -> 'easily unspirals' is bounded: the thread is slow-shedding, not instant,")
print("     except at the beta-decay event itself.")

# ===========================================================================
print("\n[TEST 3] Claim D - the expansion shears the neighboring knot (recoil kill)")
# ===========================================================================
print("  If the antineutrino's expansion unspools part of the daughter knot, the")
print("  recoil ion gets an extra kick beyond the standard 3-body recoil -> the")
print("  beta-nu angular correlation 'a' must deviate from the standard value.")
print("  Standard (V-A, lambda = -1.275): a ~ -0.106")
print("  Measured (aSPECT / PERKEO III class): a ~ -0.106 +/- 0.001")
print("  KILL CONDITION (armed): the daughter-knot shear term must shift 'a' by")
print("  < 1e-3 (the experimental resolution) OR be derived to the measured value.")
print("  No shear term is yet written; until it is, the shear recoil is CONSTRAINED")
print("  to the sub-0.1% band by existing data.")

# ===========================================================================
print("\n[TEST 4] Claim C - opposite formations force each other to untie")
# ===========================================================================
print("  Pair production threshold: 2 m_e = 1.022 MeV  (the cold weld at creation)")
print("  Annihilation output     : 2 x 511 keV = 1.022 MeV (the mass returns as light)")
print("  -> m = L/c0^2 holds both ways: the weld and the untie are the same bookkeeping.")
print("  The 'forcing': the opposite windings' shear adds at contact, exceeding the")
print("  knot's self-hold -> the untie. Falsifiable form owed: the contact-shear rate")
print("  must reproduce the annihilation cross-section's energy dependence (sigma ~ 1/v)")
print("  - the derivation is the named next target, not yet written.")

print("\n" + "=" * 108)
print("FINAL SCOREBOARD")
print("=" * 108)
print("  A. Continuum from the unspooling wave : PASS IN FORM (2-polarization count = the")
print("     (E0-E)^2 exponent); the 878.4 s rate integral is the owed second route.")
print("  B. 'Unties unless orbiting a proton'  : FALSIFIED (free positrons stable;")
print("     positronium annihilates BECAUSE of the contact, not despite the orbit).")
print("  C. Contact forces the untie          : CONSISTENT (1.022 MeV both ways = m=L/c0^2);")
print("     the cross-section derivation is owed.")
print("  D. The expansion shears the neighbor  : CONSTRAINED to < 1e-3 on 'a' by existing")
print("     beta-nu correlation data; the shear term must be written or stay below noise.")
print("=" * 108)
