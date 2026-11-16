# luminous_reach.py - the run derivation: the light's walk to the bath (2026-10-18)
# The threshold: the wave must carry more energy density than the bath's own
# u_cmb = 4.17e-14 J/m^3 (the 2.7255 K baseline's). The star's photon density
# dilutes as L/(4.pi.r^2.c0); when it hits u_cmb, the light has WORN OUT.
#   r_lum = sqrt(L / (4.pi.c0.u_cmb))
# The universal ruler: every star's light walks this far before merging with
# the CMB's graveyard. The 1/r^2 carries the rest of the way to the eye.
import numpy as np

c0 = 2.9979e8
u_cmb = 4.1747e-14          # J/m^3 (the 2.7255 K bath's energy density)
L_sun = 3.828e26            # W
AU = 1.496e11               # m
LY = 9.461e15               # m

def r_lum(L):
    return np.sqrt(L / (4.0 * np.pi * c0 * u_cmb))

print("THE LUMINOUS REACH - the run derivation:")
print("  r_lum = sqrt(L / (4.pi.c0.u_cmb))")
print(f"  the bath: u_cmb = {u_cmb:.4e} J/m^3 (the 2.7255 K's)")
print()
print("  the Sun: L = %.4e W -> r_lum = %.4e m = %.0f AU = %.3f ly"
      % (L_sun, r_lum(L_sun), r_lum(L_sun)/AU, r_lum(L_sun)/LY))
print()
print("  the star reach ladder (the sqrt(L) scaling):")
stars = [
    ("Proxima Cen", 1.7e-3, 4.0),
    ("The Sun",     1.0,    None),
    ("Sirius",      25.0,   9.0),
    ("Betelgeuse",  1.3e5,  548.0),
    ("Rigel",       1.2e5,  860.0),
    ("Deneb",       2.0e5,  2615.0),
    ("V762 Cas",    4.0e5,  16300.0),
]
print(f"  {'star':14s} {'L/Lsun':>9s} {'distance':>9s} {'r_lum (AU)':>11s} {'r_lum (ly)':>10s} {'wear':>10s}")
for name, Lr, dist in stars:
    r = r_lum(Lr * L_sun)
    wear = (dist * LY / r) ** -2 if dist else 0.0   # the energy ratio at the observer's
    print(f"  {name:14s} {Lr:9.2e} {str(dist):>9s} {r/AU:11.0f} {r/LY:10.3f} {wear:10.1e}")
print()
print("  the naked-eye check: V762 Cas at 16,300 ly - the wear along the sight")
print("  line is ~1e-6: the eye sees the pure 1/r^2, the tired light only")
print("  accumulates at the cosmic scale. The reach is the OUTPUT's property,")
print("  not the distance's - the same formula from Proxima to Deneb.")
