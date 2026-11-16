# -*- coding: utf-8 -*-
"""
pwc_effort_form_falsification.py - THE EFFORT FORM (work, not speed)
====================================================================
Author's refinement (2026-10-30): the wear is the WORK the thread expends holding the
Max-P shell, not the speed itself. Denser ambient -> the shell has less pressure
difference to sustain -> the thread works less -> the decay slows. In a black hole the
ambient does nearly the whole job -> the neutron puts in almost no effort -> it lasts.
"The oldest trick in the thermodynamic book: insulate tight. Heat ultimately expands
everything."

Formalized:  wear rate  lambda ~ (P_shell - P_med)   [the effort]
             black-hole limit: P_med -> P_shell -> lambda -> 0
             lab prediction:   dtau/tau = P_med / P_shell
"""
import math

C0     = 2.99792458e8
Y_BOW  = 5.9307e26
RHO_MAX = 1.29032e15
RHO_N   = 2.0 * Y_BOW / ((11.0 / 12.0) * C0) ** 2     # the neutron thread's ambient
P_SHELL = RHO_N * C0 ** 2 / 3.0                        # the shell the thread sustains

print("=" * 108)
print("PWC EFFORT FORM - VICIOUS FALSIFICATION (2026-10-30, round 8)")
print("=" * 108)

# ===========================================================================
print("\n[TEST 1] The effort form and its endpoints")
# ===========================================================================
print(f"  The neutron thread's shell: rho_shell = 1.19 rho_h = {RHO_N:.4e} kg/m^3")
print(f"  The pressure the shell sustains: P_shell = rho_shell c0^2/3 = {P_SHELL:.4e} Pa")
print("  Wear law: lambda ~ (P_shell - P_med)  ->  tau = tau0 / (1 - P_med/P_shell)")
print(f"  Black-hole interior (P_med -> rho_max c0^2): the ambient IS the shell pressure,")
print(f"  the thread's effort -> 0, the wear -> 0. EXACT, not approximate - the stall.")
print("  VERDICT: the effort form holds at both ends; the BH limit is the deltaP -> 0 point.")

# ===========================================================================
print("\n[TEST 2] The lab magnitude - the same number, restated as effort")
# ===========================================================================
print("  dtau/tau = P_med / P_shell  (the effort the ambient takes off the thread's job)")
for label, u in [("UCN trap 300 K walls",       4.2e-14),
                 ("1 W/cm^2 CW laser",          1e4 / 3e8),
                 ("1e18 W/cm^2 extreme laser",  1e22 / 3e8)]:
    rho_g = u / C0 ** 2
    p_med = u / 3.0
    shift = p_med / P_SHELL
    print(f"    {label:<28} P_med = {p_med:.2e} Pa -> dtau/tau = {shift:.2e}")
print("  -> even the most extreme laboratory laser takes 1e-14 of the thread's job.")
print("  The effort form does NOT rescue the magnitude: the shell the thread holds is")
print("  4.7e26 Pa, and no lab photon field approaches 1e-14 of that.")

# ===========================================================================
print("\n[TEST 3] The 'proven and verified by science' claim - held to our protocol")
# ===========================================================================
tau_beam, tau_bot = 879.4, 877.75
print(f"  On record: beam {tau_beam} s vs bottle {tau_bot} s -> the bottle is")
print(f"  {(tau_bot/tau_beam-1)*100:+.2f}% SHORTER. The photon-richer environment (300 K")
print("  walls) reads SHORTER, not longer - the OPPOSITE sign of the photon-buffer")
print("  prediction under this coupling (which predicts +1e-41 at those densities).")
print("  The beam/bottle gap is therefore NOT the photon buffer; it is the known")
print("  unresolved systematic (wall losses / exotic channels).")
print("  PROTOCOL DEMAND: the claim 'the photon laser slows the decay, proven and")
print("  verified' needs its citation (arXiv/DOI) exactly like every framework number.")
print("  No paper = the claim stays in the ASSERTED column, per our own doctrine.")

print("\n" + "=" * 108)
print("FINAL SCOREBOARD")
print("=" * 108)
print("  1. The effort form          : lambda ~ (P_shell - P_med) - accepted as the sharper")
print("     statement of round 7's capacity law; wear = the work, not the speed.")
print("  2. The black-hole limit      : EXACT - P_med -> P_shell -> effort -> 0. The")
print("     neutron behind a Max-P shell does almost no work. 'Insulate tight' is the")
print("     stall, with numbers.")
print("  3. The lab magnitude         : unchanged - 1e-41 to 1e-14 even at 1e18 W/cm^2.")
print("     The effort form cannot produce a measurable laser slowdown.")
print("  4. The experimental claim    : beam/bottle gap is the WRONG SIGN (bottle shorter);")
print("     any 'laser slows decay' paper must be cited and its numbers re-derived before")
print("     it enters the framework. ASSERTED until then.")
print("=" * 108)
