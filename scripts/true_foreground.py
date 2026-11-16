# true_foreground.py - the source excluded, the units locked (2026-10-17)
# The fix: the lens must be a FOREGROUND (z_L < z_source - eps). 3C 273 itself
# (z = 0.158) cannot lens itself. The output's in milliarcseconds (mas), the
# enclosed-mass profile's active, the M/L = 0.6 and R_gal = 10 kpc stated.
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
z_lens = cz / 299792.458       # the cz's the km/s, the c's the km/s
z_src = 0.158
d_pc = cz / 73.0 * 1e6
K_abs = kt - 5.0*np.log10(np.maximum(d_pc, 1.0)) + 5.0
L_K = 10.0**(-0.4*(K_abs - 3.28))
M = 0.6 * L_K * M_sun
d_m = d_pc * 3.0857e16
R_gal = 10.0e3 * 3.0857e16

c1 = SkyCoord(ra=187.2779*u.deg, dec=2.0524*u.deg, frame="icrs")
c2 = SkyCoord(ra=ra2*u.deg, dec=de2*u.deg, frame="icrs")
sep = c1.separation(c2)
# THE CUT: the strict foreground - the lens strictly in front of the source
fore = (sep < 2.0*u.deg) & (z_lens < z_src - 0.005) & (cz > 0)
b_phys = sep[fore].to(u.rad).value * d_m[fore]
frac = np.minimum(b_phys / R_gal, 1.0)
M_enc = M[fore] * frac
pulls = 4.0*G*M_enc/(b_phys * c0**2)
pa = c1.position_angle(c2[fore]).to(u.rad).value
x = (pulls * np.sin(pa)).sum(); y = (pulls * np.cos(pa)).sum()
mas = 206264806.7
print("THE TRUE FOREGROUND SUM (the source excluded, the units locked):")
print(f"  the foreground lenses: {fore.sum()}  (the z < 0.158 cut)")
print(f"  |dtheta| = {np.sqrt(x*x+y*y)*mas:8.2f} mas  =  {np.sqrt(x*x+y*y)*mas/1000:8.4f} arcsec")
print(f"  the signed components:  dRA.cosd = {x*mas:+.2f} mas,  dDec = {y*mas:+.2f} mas")
print()
print("the honest ledger: the pipeline is now the physics's - the foreground's")
print("the lens's, the source can't lens itself, the units are the mas, and the")
print("M/L = 0.6 + R_gal = 10 kpc are the stated inputs. The receipt: this")
print("predicted vector vs the observed astrometric's.")
