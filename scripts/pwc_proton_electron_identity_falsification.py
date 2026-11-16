# -*- coding: utf-8 -*-
"""
pwc_proton_electron_identity_falsification.py - PROTON vs ELECTRON IDENTITY CLAIMS
==================================================================================
Author's claims (2026-10-30):
  A. The electron is a single +/- chiral that torques down and CAN EASILY FLIP CHARGE.
  B. In neutron decay the proton and electron break apart; the electron DOESN'T LAST
     LONG on its own, the proton does.
  C. The proton is 5 chirals (2 upper + central + 2 lower) locked and cold-welded
     with a rigid thermally vacant centre; harder to untie in all cases.
  D. The electron isn't the same (single chiral vs the 5-chiral cage).
Every claim broken until the math holds. Every miss printed.
"""
import math

print("=" * 108)
print("PWC PROTON vs ELECTRON IDENTITY CLAIMS - VICIOUS FALSIFICATION (2026-10-30)")
print("=" * 108)

# ===========================================================================
print("\n[TEST 1] Claim A - 'the electron can easily flip charge'")
# ===========================================================================
tau_e_bound = 6.6e28          # yr, Borexino-class bound on e- invisible decay
tau_univ    = 1.38e10         # yr
print("  e- -> e+ transitions: NONE observed. Charge is absolutely conserved;")
print("  every electron ever made is still an electron (disappearance bound")
print(f"  tau_e > {tau_e_bound:.1e} yr = {tau_e_bound/tau_univ:.1e}x the age of the universe).")
print("  The framework's own topology: the face order admits EXACTLY two states (+e, -e);")
print("  a 'flip' is a full re-ravel of the 720-deg fold - annihilation-class, not easy.")
print("  Where charge DOES flip easily: INSIDE the 2-1-2 cage (u <-> d face projections,")
print("  +2/3+2/3-1/3 = +1 vs 0) - that is the PROTON's internal rearrangement, not the")
print("  free electron's.")
print("  VERDICT: 'easily flips charge' FALSIFIED for the free electron. The flip freedom")
print("  lives in the cage, exactly where the framework already put it.")

# ===========================================================================
print("\n[TEST 2] Claim B - 'the electron doesn't last long on its own'")
# ===========================================================================
tau_n_s = 878.4             # neutron mean life (ledger: PDG 2024; UCNtau 877.75)
print(f"  Free electrons: stable (tau_e > 6.6e28 yr). The universe is full of free")
print(f"  electrons (plasmas, cosmic rays) - they do not expire.")
print(f"  Neutron: tau_n = {tau_n_s:.1f} s - it is the neutron's WELD that holds 878 s,")
print("  not the electron that fails afterward. The ejected electron persists forever.")
print("  VERDICT: INVERTED. Inside the neutron the electron THREAD is the finite piece")
print("  (the cage+thread weld = 878 s); outside, the electron is the locked knot.")
print("  The neutron decays; the electron doesn't.")

# ===========================================================================
print("\n[TEST 3] Claim C - the 5-chiral cold-welded cage with the vacant centre")
# ===========================================================================
print("  2-1-2 = 2 + 1 + 2 = 5 cells  (the cage count, locked)")
print("  Core = the rho_max ball: r_core = 6.7640 fm vs 8 R_p = 6.7376 fm (core-shell")
print("  audit, 2026-10-30: the sealed derivation, C-gap -1.05% is the residual)")
print("  Cold weld: E_lock = 708/245 = 2.8898 (log-EOS, PBA-9)")
print("  VERDICT: CONSISTENT with the existing framework - the claim adds no new number,")
print("  and every number it names is already locked. (The 'thermally vacant centre' is")
print("  the zero-heat core reading from the core-shell falsification: survives only as")
print("  the mass bookkeeping at rho_max, not as a 1/19 geometric volume.)")

# ===========================================================================
print("\n[TEST 4] Claim D - 'harder to untie in all cases' - the lifetime hierarchy")
# ===========================================================================
hier = [
    ("proton  (5-chiral cage)",        2.4e34, "yr", "Super-K 2022 class bound"),
    ("electron (single chiral)",       6.6e28, "yr", "disappearance bound"),
    ("neutron (cage + welded thread)", 878.4,  "s",  "mean life"),
    ("muon    (single chiral, strained)", 2.197e-6, "s", "mean life"),
]
print(f"  {'object':<32} {'lifetime':>14} {'unit':>4}")
for name, val, unit, note in hier:
    print(f"  {name:<32} {val:>14.4g} {unit:>4}   ({note})")
print("  The proton IS the hardest to untie - the claim HOLDS as a hierarchy.")
print("  BUT the muon kills the generalization: the muon is a SINGLE chiral (like the")
print("  electron) and unties in 2.2 microseconds, while the electron never does.")
print("  -> stability is decided by STRAIN + WELD, not by chiral count.")
print("     muon = the electron's strained overtone (20 pi^3 / 3, the T7 debt) - unspools;")
print("     electron = the unstrained knot - locked;")
print("     proton = the 5-cell cage weld - locked hardest.")
print("  VERDICT: 'harder in all cases' HOLDS for the proton; 'single chiral = weak'")
print("  FAILS via the muon. The five-chiral cage is ONE route to stability, not the rule.")

# ===========================================================================
print("\n[TEST 5] The neutron break-up, re-checked with the new picture")
# ===========================================================================
C0 = 2.99792458e8; KEV = 1.602176634e-16
m_n, m_p, m_e = 1.67492749804e-27, 1.67262192369e-27, 9.1093837015e-31
Q = (m_n - m_p - m_e) * C0 ** 2 / KEV
print(f"  n -> p + e- + nu-bar : Q = {Q:.2f} keV")
print("  The weld fails -> the electron thread leaves as the STABLE free knot;")
print("  the mirror half-thread unspools (the antineutrino - the 2-polarization wave")
print("  that books the continuum, falsification round 3); the proton cage stays locked.")
print("  Consistent with all three prior rounds. No new number added; the unspooling-")
print("  rate integral for tau_n = 878.4 s remains the owed second route.")

print("\n" + "=" * 108)
print("FINAL SCOREBOARD")
print("=" * 108)
print("  A. 'Electron easily flips charge'   : FALSIFIED (no e- -> e+ ever seen;")
print("     tau_e > 6.6e28 yr; the flip freedom lives in the CAGE, not the free knot).")
print("  B. 'Electron doesn't last on its own': FALSIFIED/INVERTED (free electrons are")
print("     permanent; the NEUTRON's weld is the 878 s piece).")
print("  C. 5-chiral cage + vacant centre    : CONSISTENT - all its numbers already locked.")
print("  D. 'Proton hardest to untie'        : HOLDS (tau_p > 2.4e34 yr > tau_e > 6.6e28 yr")
print("     > tau_n 878 s > tau_mu 2.2 us); but the muon kills 'single chiral = weak':")
print("     stability = strain + weld, not knot count.")
print("=" * 108)
