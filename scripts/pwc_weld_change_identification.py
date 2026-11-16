# -*- coding: utf-8 -*-
"""
pwc_weld_change_identification.py - WHAT'S NEEDED: THE 76.941 keV IDENTIFICATION (round 69)
============================================================================================
Perplexity's correction, adopted: dE_weld = 76.941 keV is the weld's CHANGED state
(the final minus initial stored energy), and 859.271 = 782.330 + 76.941 is the
complete balance. What is needed now: identify dE_weld with a framework quantity -
test the candidates, correct the record, update the list.
"""
import numpy as np

KEV = 1.602176634e-16
m_e_keV = 510.998950
Q   = 782.33
W12 = 859.271
dE  = W12 - Q

print("=" * 108)
print("WHAT'S NEEDED: THE 76.941 keV IDENTIFICATION (2026-10-31, round 69)")
print("=" * 108)

print("\n[STEP 1] The corrected bookkeeping (adopted)")
print(f"  E(twelve-fold configuration) = E(outgoing) + dE(weld)")
print(f"  {W12:.3f} = {Q:.3f} + {dE:.3f} keV")
print("  Two operations, distinguished: exact retracing returns the full 859.271; the")
print("  DECAY ends at a CHANGED weld, releasing the gross minus the weld's increase.")

print("\n[STEP 2] RECORD CORRECTION (round 68's text)")
print(f"  'the retained share = 1/12 of the store' was WRONG: {dE:.3f}/{W12:.3f} = {dE/W12:.5f}")
print(f"  = 1/{1.0/(dE/W12):.2f}, not 1/12. The keep is 1/11.2 of the store. Corrected.")

print("\n[STEP 3] The identification sweep - what is 76.941 keV?")
cands = [
    ("Q/11 (the relief numerator)", Q/11.0),
    ("Q x f0", Q * (2.0/19.0) * (361.0/357.0)),
    ("Q/12", Q/12.0),
    ("m_e c0^2 x (2/19)", m_e_keV * 2.0/19.0),
    ("the 8Be gap", 91.84),
    ("m_e c0^2 / 6.64", m_e_keV/6.64),
]
print(f"  target: {dE:.3f} keV")
for name, val in cands:
    print(f"    {name:<26} = {val:>9.2f} keV  ({100*(val/dE-1):+6.2f}%)")
print("  -> no locked quantity matches at the <1% level yet. The target stands:")
print(f"     dE_weld = {dE:.3f} keV, to be OUTPUT by the framework's weld-state")
print("     difference (the neutron's pre-decay weld minus the proton's post-decay")
print("     weld). The identification is the item - not a mechanism search, a")
print("     bookkeeping identification.")

print("\n[STEP 4] The updated closing list (top of the board)")
print("  1. IDENTIFY dE_weld = 76.941 keV with the weld-state difference (the sharpest")
print("     single item - one number, one identification).")
print("  2. The pitch's fine structure -> the 0.29% in the 12-fold bookkeeping.")
print("  3. The convention (exact-4 vs 4.0007815) -> the magnetic 740 ppm.")
print("  4-7. The standing tiers: the 2/3 allocation, the decoupling distribution,")
print("      the six-face sentence, the neutrino ratio, the formation distribution.")

print("\n" + "=" * 108)
print("ANSWER TO 'THEN WHAT'S NEEDED'")
print("=" * 108)
print("  ONE identification: dE_weld = 76.941 keV = the weld's energy change across")
print("  the decay. The balance defines it; the framework must OUTPUT it from the")
print("  pre/post weld states. Everything else on the board is already named.")
print("=" * 108)
