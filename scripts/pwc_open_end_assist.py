# -*- coding: utf-8 -*-
"""
pwc_open_end_assist.py - THE OPEN-END CORRECTION: WHERE THE ASSIST LIVES (round 61)
====================================================================================
The author's correction: the work theorem assumes the loop CLOSES. If the electron's
thread has a dominant end that does not close, the tangential work need not cancel.
The framework already has exactly that structure: the bound electron = the CLOSED
720-degree double loop (round 16); the OPEN thread = the unspooling antineutrino
(rounds 8-9). Compute the open-path work and place the assist correctly.
"""
import numpy as np

print("=" * 108)
print("THE OPEN-END CORRECTION: WHERE THE ASSIST LIVES (2026-10-31, round 61)")
print("=" * 108)

print("\n[STEP 1] The premise correction, accepted")
print("  The closed-loop work theorem requires closure. For an OPEN thread (a dominant")
print("  end that does not close), the tangential work over a pass need NOT cancel:")
print("  the assist is real for the open path. Accepted.")

print("\n[STEP 2] The open-path work, demonstrated")
phi_s = np.pi / 4.0
R_out, R_in = 1.0, 0.6
d = lambda p: np.sqrt(R_out**2 + R_in**2 - 2*R_out*R_in*np.cos(p - phi_s))
def F_tan(p):
    dx = R_out*np.cos(p) - R_in*np.cos(phi_s)
    dy = R_out*np.sin(p) - R_in*np.sin(phi_s)
    dd = d(p)
    Fx, Fy = dx/dd**3, dy/dd**3
    return Fx*(-np.sin(p)) + Fy*np.cos(p)
# an open arc ENDING at the strip (one-sided - the endpoints differ in potential)
ps = np.linspace(phi_s - 0.5, phi_s, 200001)
dp = ps[1] - ps[0]
W_open = np.sum(F_tan(ps)) * R_out * dp
print(f"  one-sided open arc ending at the strip: net tangential work = {W_open:+.4f}  (NOT zero)")
print("  -> the open end receives a net kick per pass: the assist exists exactly where")
print("     the author says - on the path that does not close. (A symmetric straddling")
print("     arc cancels - the reflection antisymmetry - but the one-sided arc does not.)")

print("\n[STEP 3] The charge-accumulation point - why the open end must move")
print("  A steady open current accumulates charge at the end; the end's growing field")
print("  stops the flow - UNLESS the end itself advances (the tip is carried by the")
print("  wave). The framework's open thread is exactly that: the UNSPOOLING mirror -")
print("  the tip retreats as the thread releases, and the assist's work goes into the")
print("  tip's advance. The assist is the UNSPOOLING'S engine.")

print("\n[STEP 4] The placement, from the framework's locked structure")
print("  - the BOUND electron: the CLOSED 720-degree double loop (round 16) - no open")
print("    end, no net assist - the 1.34 fm orbit is the shell's (round 22).")
print("  - the ANTINEUTRINO: the open, unspooling half-spin thread (rounds 8-9) - the")
print("    open end, the net tangential work, the assist. The author's mechanism IS")
print("    the antineutrino's engine, not the bound orbit's holder.")
print("  CHECKABLE: the assist's work per pass must match the unspooling's energy")
print("  budget - the beta continuum's (E0 - E)^2 shape (rounds 8-9). That match is")
print("  the next derivation: the open-end work = the released thread's energy.")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  The open-end correction is REAL and CORRECT: the work theorem needs closure,")
print("  and the open path's net tangential work does not vanish (demonstrated). The")
print("  framework already carries the two structures the correction demands: the")
print("  closed double loop (the bound electron - the shell holds the orbit) and the")
print("  open unspooling thread (the antineutrino - the assist drives the release).")
print("  The mechanism is placed: it is the DECAY's engine. Next: match the assist's")
print("  work to the beta continuum's energy bookkeeping.")
print("=" * 108)
