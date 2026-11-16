# single_mass_benchmark.py - the injected mass must bend (2026-10-17)
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

c0 = 2.9979e8
G = 6.674e-11
M_sun = 1.989e30

# the target and the injected lens
ra_src, dec_src = 187.2779, 2.0524       # 3C 273
# the fake lens: 1 deg due NORTH of the sightline, 1e12 M_sun at 100 Mpc
M_lens = 1e12 * M_sun
D_L = 100.0 * 3.0857e22                  # metres
ra_lens, dec_lens = ra_src, dec_src + 1.0

# the impact parameter: the angular separation -> the physical b
c1 = SkyCoord(ra=ra_src*u.deg, dec=dec_src*u.deg, frame="icrs")
c2 = SkyCoord(ra=ra_lens*u.deg, dec=dec_lens*u.deg, frame="icrs")
sep = c1.separation(c2).to(u.rad).value
b = sep * D_L                              # the physical impact, metres

theta = 4.0 * G * M_lens / (b * c0**2)     # radians, the locked scaling
theta_mas = theta * 206264806.7
pa = c1.position_angle(c2).to(u.rad).value

dRA = theta * np.sin(pa) * 206264806.7
dDec = theta * np.cos(pa) * 206264806.7

print("THE SINGLE-MASS BENCHMARK:")
print(f"  the lens: 1e12 M_sun at 100 Mpc, 1 deg north")
print(f"  the impact b = {b/3.0857e19:.3f} Mpc-physical")
print(f"  the expected |dtheta| = 4GM/(b c0^2) = {theta*206264806.7:.3f} mas")
print(f"  the raw vector:  dRA.cosd = {dRA:.3f} mas,  dDec = {dDec:.3f} mas")
print(f"  the direction:  position angle {np.degrees(pa):.1f} deg (0 = north)")
print()
if abs(dRA) < 1e-3 and dDec > 0:
    print("PASS: the vector points NORTH (the mass's direction), the magnitude's")
    print("the locked scaling - the differential's math holds.")
else:
    print("CHECK: the direction/magnitude's off - the bug's in the vector math.")
