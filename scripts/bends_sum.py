# bends_sum.py - the 2MRS deflection vectors, the frozen model (2026-10-17)
# The locked bending: d n^/d l = (2/c0^2)(I - n^n^T) . g_bodies - the weak-field
# push-plus-pull, the 4GM/(b c0^2) scaling. The 2MRS's the frozen catalog; the
# output's the RAW predicted deflection vector - not a fitted origin.
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# --- the 2MRS (the same parse as the WHIM work) ---
ra2, de2, cz2 = [], [], []
with open("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/rot/sparc_x/2mrs.txt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("RAJ2000"):
            header = line.split("\t")
            break
    for line in f:
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < len(header):
            continue
        try:
            ra2.append(float(p[0])); de2.append(float(p[1])); cz2.append(float(p[2]))
        except ValueError:
            continue
ra2 = np.array(ra2); de2 = np.array(de2); cz2 = np.array(cz2)
print(f"2MRS bodies: {len(ra2)}")

c0 = 2.9979e8
G = 6.674e-11
M_sun = 1.989e30
# the honest mass: the 2MRS's K-band's the light; the M/L's the stated input
ML = 0.6          # M_sun/L_sun-ish, the standard's K-band's (stated, not fitted)
# the luminosity proxy: the K-magnitude's not in this parse, so the cz's the
# distance's; the mass's the simple cz-scaled placeholder (the honest label)
d = cz2 / 73.0    # Mpc
M = ML * (1e10 * (d / 10.0))  # the placeholder scaling - the honest flag below

sample = [
    ("3C 273", 187.2779, 2.0524),
    ("3C 279", 194.0465, -5.7893),
    ("PKS 2155-304", 329.7169, -30.2256),
    ("Centaurus A", 201.3651, -43.0191),
    ("M87", 187.7059, 12.3911),
]
print()
print("the RAW predicted deflection vectors (the 2MRS's frozen sum):")
print(f"  {'source':14s} {'dRA cosd (mas)':>14s} {'dDec (mas)':>12s} {'|dtheta| (mas)':>14s}")
for name, ra, dec in sample:
    # the impact parameters: the angular separations to the nearby 2MRS bodies
    c1 = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs")
    sep = c1.separation(SkyCoord(ra=ra2*u.deg, dec=de2*u.deg, frame="icrs"))
    near = sep < 2.0 * u.deg
    if near.sum() == 0:
        print(f"  {name:14s} {'-':>14s} {'-':>12s} {'-':>14s}")
        continue
    b = sep[near].to(u.rad).value
    # the deflection per body: 4GM/(b c0^2), the direction's the body's
    theta_E = 4.0 * G * M[near] / (b * c0**2)   # radians
    pos_ang = c1.position_angle(SkyCoord(ra=ra2[near]*u.deg, dec=de2[near]*u.deg, frame="icrs"))
    dRA = (theta_E * np.sin(pos_ang.to(u.rad).value)).sum() * 206264806.7
    dDec = (theta_E * np.cos(pos_ang.to(u.rad).value)).sum() * 206264806.7
    mag = np.sqrt(dRA**2 + dDec**2)
    print(f"  {name:14s} {dRA:14.3f} {dDec:12.3f} {mag:14.3f}")
print()
print("honest flags: the 2MRS parse here lacks the K-magnitudes, so the masses")
print("carry a stated placeholder scaling - the VECTOR's the structure, the")
print("magnitudes need the real K-band's. The receipt: these predicted vectors")
print("vs the independently constrained astrometric shifts (the epoch-differentials).")
