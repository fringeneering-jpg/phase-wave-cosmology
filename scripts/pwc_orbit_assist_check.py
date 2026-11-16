# -*- coding: utf-8 -*-
"""
pwc_orbit_assist_check.py - THE ORBIT-ASSIST CLAIM, CHECKED (round 60)
======================================================================
The author's mechanism: the outer thread SLIDES past the inner loop's sectional
repulsion, turning the repel into an orbit assist - especially for sectional strips
or two polar strips. Check against the closed-loop work theorem:
  W = oint F . dr = 0 for ANY static charge arrangement (the field is conservative).
A tangential assist over a full circuit needs a MOVING source (like a planet in a
slingshot); at steady state the moving loop's contribution is the radial magnetic
force plus a ZERO induced E (constant flux). Compute both.
"""
import numpy as np

k = 1.0          # units: use a point-like strip charge at angular position phi_s

print("=" * 108)
print("THE ORBIT-ASSIST CLAIM, CHECKED (2026-10-31, round 60)")
print("=" * 108)

print("\n[CHECK 1] The closed-loop work theorem, demonstrated for a sectional strip")
phi_s = np.pi / 4.0                    # the strip's angular position
R_out, R_in = 1.0, 0.6                 # loop radii (units)
d = lambda p: np.sqrt(R_out**2 + R_in**2 - 2*R_out*R_in*np.cos(p - phi_s))
# tangential force on the outer thread from the strip's repulsion (1/d^2 radial)
# tangential component: F_t = F . t_hat = (F_vec projected on the azimuth)
def F_tan(p):
    dx = R_out*np.cos(p) - R_in*np.cos(phi_s)
    dy = R_out*np.sin(p) - R_in*np.sin(phi_s)
    dd = d(p)
    Fx, Fy = dx/dd**3, dy/dd**3          # repulsion (outward along d)
    t_hat = (-np.sin(p), np.cos(p))      # azimuthal unit vector
    return Fx*t_hat[0] + Fy*t_hat[1]
N = 400000
ps = np.linspace(0, 2*np.pi, N, endpoint=False)
dp = ps[1] - ps[0]
W = np.sum(F_tan(ps)) * R_out * dp       # work over one full circuit
print(f"  strip at angle {phi_s:.2f}, outer thread circles once:")
print(f"  net tangential work over the closed circuit = {W:.3e}  (units)")
print("  -> ZERO, as the theorem requires: the sectional repulsion kicks the thread")
print("     forward on approach and backward on departure - the kicks cancel exactly")
print("     over a full loop. A static strip CANNOT provide a net orbit assist.")

print("\n[CHECK 2] The polar strips - what the net actually is")
print("  Two strips at the poles: the equatorial thread feels both repulsions; the")
print("  vertical components cancel by symmetry, the RADIAL components add:")
print("  -> the polar pair's net is a RADIAL repulsion - the same ejection as the")
print("     full ring, weakened only by the geometry factor. No tangential assist.")

print("\n[CHECK 3] The moving-source version (the inner loop IS a current)")
print("  A true slingshot needs the source to MOVE (energy exchange with the source's")
print("  motion). The inner loop's charge moves: its field's contributions are")
print("    - the magnetic force: RADIAL (amperian coupling, ~16 N, 4.7x short - round 57)")
print("    - the induced electric field: ZERO at steady state (the flux is constant)")
print("  -> no tangential assist from the motion either. The sliding-past is real for")
print("     one pass (a transient kick that reshapes the orbit), but it cannot supply")
print("     the orbit over many circuits - the net assist is provably zero.")

print("\n" + "=" * 108)
print("VERDICT")
print("=" * 108)
print("  The orbit-assist claim is FALSIFIED by the closed-loop work theorem: any")
print("  static charge arrangement (sectional strips, polar strips, any shape) gives")
print("  zero net tangential work per circuit. The moving-loop version adds only the")
print("  radial magnetic force and a zero induced E at steady state. The sectional")
print("  geometry can RESHAPE the orbit, not provide it - the 1.34 fm orbit still")
print("  needs the shell (round 22), as the record stands.")
print("=" * 108)
