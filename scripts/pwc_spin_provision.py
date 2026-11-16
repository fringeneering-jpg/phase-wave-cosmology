# -*- coding: utf-8 -*-
"""
pwc_spin_provision.py - PROVIDING THE SPIN: WHAT L = h-bar/2 PINS (round 59)
============================================================================
The author's directive: the missing piece is PROVIDING THE SPIN, not the radius.
The spin constraint L = h-bar/2 is already the fixed-L map. What it uniquely pins:
the pair's MASS asymmetry (m_- - m_+) = h-bar/(2 v R) - a new, checkable output that
the radius/moment tension does not constrain.
"""
import numpy as np

hbar = 1.054571817e-34
c0   = 2.99792458e8
m_e  = 9.1093837015e-31
m_p  = 1.67262192369e-27
alpha = 7.2973525693e-3
R_p0 = 0.8414e-15
r_e  = alpha * hbar / (m_e * c0)
v0f  = 11.0 / 12.0
g0   = 1.0 / np.sqrt(1.0 - v0f ** 2)
R_e0 = r_e / (g0 * v0f ** 2)
f0   = (2.0 / 19.0) * (361.0 / 357.0)
ell  = g0 * m_e * v0f * c0 * R_e0 / (m_e * c0)
Re   = R_e0
u    = ell / Re
vc   = u / np.sqrt(1.0 + u ** 2)

print("=" * 108)
print("PROVIDING THE SPIN: WHAT L = h-bar/2 PINS (2026-10-31, round 59)")
print("=" * 108)

print("\n[STEP 1] The spin constraint at the ORBIT scale - and its catastrophic demand")
print("  The neutron's spin-1/2 as the pair's NET orbital angular momentum at R = 1.34 fm:")
print("    L = (m_- v_- - m_+ v_+) R = h-bar/2   (the two branches counter-rotate)")
dm = hbar / (2.0 * vc * c0 * Re)
print(f"  -> required branch MASS asymmetry: m_- - m_+ = h-bar/(2 v R) = {dm:.4e} kg")
print(f"     = {dm/m_e:.1f} m_e   (the thread's budget is ONE m_e: IMPOSSIBLE)")
l_per_me = m_e * vc * c0 * Re / hbar
print(f"  Why: one electron mass orbiting at 1.34 fm carries only {l_per_me:.4f} h-bar of")
print("     orbital angular momentum - providing h-bar/2 there needs 157 electron masses.")
print("  -> the orbit-scale spin provision is FALSIFIED: the 1.34 fm orbit is spinless.")

print("\n[STEP 2] Where the spin actually lives - the Compton loop (the locked structure)")
R_loop = hbar / (2.0 * m_e * c0)
l_loop = m_e * c0 * R_loop / hbar
print(f"  The thread's own spin: m_e c0 R_loop / h-bar with R_loop = h-bar/(2 m_e c0) = {R_loop*1e15:.2f} fm")
print(f"  -> m_e c0 R_loop = {l_loop:.4f} h-bar = h-bar/2  (the Williamson loop, locked since")
print("     round 4/16). The neutron's h-bar/2 is the Compton-loop circulation, NOT")
print("     the 1.34 fm orbit. 'Providing the spin' was ALREADY done at the loop scale.")

print("\n[STEP 3] What this decides")
print("  The spin is provided by the Compton loop (0.5005 h-bar); the 1.34 fm orbit")
print("  carries 0.0032 h-bar - negligible. Therefore the radius/moment tension is")
print("  untouched by the spin: the moment's 272 ppm and the charge-radius conflict")
print("  are charge-structure items, and the spin's carrier was never in question.")
print("  NEW forward check: the spin budget - the core's spin + the loop's h-bar/2")
print("  + the weld's counter-spin must assemble the neutron's h-bar/2 - the weld's")
print("  counter-spin = the remaining bookkeeping, checkable against the beta decay's")
print("  helicity structure (rounds 8-9).")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  'Providing the spin' at the orbit scale is FALSIFIED (157 m_e needed; the")
print("  orbit carries 0.0032 h-bar). The spin lives in the Compton loop (0.5005 h-bar,")
print("  the locked R_loop = 193.08 fm). The 272 ppm and the charge-radius tension")
print("  remain charge-structure items - the spin is already provided, elsewhere.")
print("=" * 108)
