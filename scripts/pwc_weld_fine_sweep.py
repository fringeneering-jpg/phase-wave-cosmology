# -*- coding: utf-8 -*-
"""
pwc_weld_fine_sweep.py - THE WIDENED SWEEP: FINE-STRUCTURE COMBINATIONS (round 71b)
==================================================================================
Widen the search to products of the locked factors (two- and three-factor
combinations on Q and on the E_lock differences), target 76.941 keV.
"""
import itertools
import numpy as np

Q      = 782.33
E_LOCK = 556.93e3
TARGET = 76.941

f = {
    "1/19": 1.0/19.0, "2/19": 2.0/19.0, "18/19": 18.0/19.0, "17/19": 17.0/19.0,
    "11/12": 11.0/12.0, "12/11": 12.0/11.0, "357/361": 357.0/361.0,
    "361/357": 361.0/357.0, "(11/12)^2": (11.0/12.0)**2, "(12/11)^2": (12.0/11.0)**2,
    "f0": (2.0/19.0)*(361.0/357.0), "1/12": 1.0/12.0, "1/11": 1.0/11.0,
}
names = list(f.keys())

print("=" * 100)
print("THE FINE-STRUCTURE SWEEP - TARGET 76.941 keV (round 71b)")
print("=" * 100)

best = []
# single factors
for n in names:
    d = Q * f[n]
    best.append((abs(d/TARGET-1), f"Q x {n}", d))
# two-factor products on Q
for a, b in itertools.product(names, names):
    d = Q * f[a] * f[b]
    best.append((abs(d/TARGET-1), f"Q x {a} x {b}", d))
# three-factor products on Q
for a, b, c in itertools.product(names, names, names):
    d = Q * f[a] * f[b] * f[c]
    best.append((abs(d/TARGET-1), f"Q x {a} x {b} x {c}", d))
# E_lock fine differences: E_lock x (a - b)
for a, b in itertools.product(names, names):
    d = E_LOCK * abs(f[a] - f[b])
    best.append((abs(d/TARGET-1), f"E_lock x |{a} - {b}|", d))

best.sort(key=lambda t: t[0])
print("  the 10 closest (all combinations):")
for dev, label, d in best[:10]:
    print(f"    {label:<40} = {d:>12.3f} keV  ({100*(d/TARGET-1):+8.3f}%)")
print("\n" + "=" * 100)
print("RESULT: the top line is the framework's best candidate for dE_weld = 76.941 keV.")
print("If nothing lands < 1%, the identification is genuinely absent - and the next")
print("single move is to take the closest named form and derive its mechanism.")
print("=" * 100)
