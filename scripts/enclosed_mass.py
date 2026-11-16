# enclosed_mass.py - the extended profile's enclosed-mass form (2026-10-17)
# The fix: not the total mass at a point - the enclosed M_2D(<b) inside the
# impact parameter. The SIS (the isothermal sphere, the flat-curve profile the
# framework's own rotation law matches at the flat part) has M_2D(<b) linear in
# b: the enclosed fraction = b/R_gal for b < R_gal. The deflection's the
# enclosed's, not the total's.
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

ra2, de2, kt, cz = [], [], [], []
with open("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/rot/sparc_x/2mrs.txt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("RAJ2000"):
            hdr = line.split("\t"); break
    for line in f:
        if not line.strip() or line.startswith("#"): continue
        p = line.split("\t")
        if len(p) < 5: continue
        try: vals = [float(p[0]), float(p[1]), float(p[2]), float(p[3])]
        except ValueError: continue
        if all(np.isfinite(v) for v in vals):
            ra2.append(vals[0]); de2.append(vals[1]); kt.append(vals[2]); cz.append(vals[3])
ra2 = np.array(ra2); de2 = np.array(de2); kt = np.array(kt); cz = np.array(cz)

c0 = 2.9979e8; G = 6.674e-11; M_sun = 1.989e30
d_pc = cz / 73.0 * 1e6
K_abs = kt - 5.0*np.log10(np.maximum(d_pc, 1.0)) + 5.0
L_K = 10.0**(-0.4*(K_abs - 3.28))
M = 0.6 * L_K * M_sun
d_m = d_pc * 3.0857e16

# the galaxy scale: the SIS's R_gal from the flat-curve's - R_gal ~ 10 kpc's the
# stated scale (the honest flag: the profile's scale's the stated input)
R_gal = 10.0e3 * 3.0857e16

c1 = SkyCoord(ra=187.2779*u.deg, dec=2.0524*u.deg, frame="icrs")
c2 = SkyCoord(ra=ra2*u.deg, dec=de2*u.deg, frame="icrs")
sep = c1.separation(c2)
cone = sep < 2.0*u.deg
b_phys = sep[cone].to(u.rad).value * d_m[cone]
# the enclosed fraction (the SIS): b/R_gal for b < R_gal, 1 beyond
frac = np.minimum(b_phys / R_gal, 1.0)
M_enc = M[cone] * frac
pulls = 4.0*G*M_enc/(b_phys * c0**2)
pa = c1.position_angle(c2[cone]).to(u.rad).value
x = (pulls * np.sin(pa)).sum(); y = (pulls * np.cos(pa)).sum()
print("THE ENCLOSED-MASS SUM (the SIS profile, R_gal = 10 kpc stated):")
print(f"  the total |v| = {np.sqrt(x*x+y*y)*206264806.7:.2f} arcsec")
print(f"  (the point-mass version was 83,719 arcsec)")
print()
print("the honest flags: the enclosed fraction tames the near-axis point, but the")
print("M/L = 0.6 and the R_gal = 10 kpc are the STATED inputs - the magnitudes")
print("remain model-estimated until the real prescriptions land. The structure's")
print("now the physics's: the enclosed mass, not the crammed point.")
