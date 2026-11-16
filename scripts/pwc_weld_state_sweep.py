# -*- coding: utf-8 -*-
"""
pwc_weld_state_sweep.py - THE ONE TASK: FIND 76.941 keV IN THE WELD STATES (round 71)
=====================================================================================
Instruction: identify dE_weld = 76.941 keV = E_weld(neutron, pre-decay) minus
E_weld(proton, post-decay), using ONLY the locked quantities. Sweep the weld-state
candidates and print everything within 1%.
"""
import itertools
import numpy as np

Q      = 782.33          # keV
E_LOCK = 556.93e3        # keV  (2.8898 E0)
M_E    = 510.998950      # keV
TARGET = 76.941

# locked factors
factors = {
    "11/12": 11.0/12.0, "12/11": 12.0/11.0, "18/19": 18.0/19.0,
    "357/361": 357.0/361.0, "1/19": 1.0/19.0, "(11/12)^2": (11.0/12.0)**2,
    "(18/19)^2": (18.0/19.0)**2, "f0": (2.0/19.0)*(361.0/357.0),
    "1": 1.0,
}
# weld-state energies (pre and post candidates), in keV
pre  = {"E_lock": E_LOCK, "E_lock+Q": E_LOCK+Q, "Q": Q, "E_lock(12/11)": E_LOCK*12.0/11.0}
post = {"E_lock(11/12)": E_LOCK*11.0/12.0, "E_lock": E_LOCK, "0": 0.0,
        "E_lock(11/12)^2": E_LOCK*(11.0/12.0)**2, "E_lock(18/19)": E_LOCK*18.0/19.0}

print("=" * 100)
print("THE WELD-STATE SWEEP - TARGET 76.941 keV (round 71)")
print("=" * 100)

hits = []
print(f"  {'pre state':<20} {'post state':<20} {'difference (keV)':>16} {'dev':>9}")
for (pn, pv), (qn, qv) in itertools.product(pre.items(), post.items()):
    d = pv - qv
    dev = 100*(d/TARGET - 1)
    if abs(dev) < 5:
        hits.append((pn, qn, d, dev))
        print(f"    {pn:<20} {qn:<20} {d:>16.2f} {dev:>+8.2f}%")

print("\n  Cross-checks against the pure fractions of Q:")
for name, f in factors.items():
    d = Q * f
    dev = 100*(d/TARGET - 1)
    if abs(dev) < 8:
        print(f"    Q x {name:<12} = {d:>12.2f} keV  ({dev:+.2f}%)")

print("\n" + "=" * 100)
if hits:
    print("RESULT: the closest candidates are above - read the best dev.")
else:
    print("RESULT: NOTHING within 5% - the identification is genuinely open; the")
    print("  sweep's miss is the finding: dE_weld = 76.941 keV has no locked-state")
    print("  source yet, and the next move is to print this miss and widen the search")
    print("  to the fine-structure terms (the pitch residual, the 361/357 family).")
print("=" * 100)
