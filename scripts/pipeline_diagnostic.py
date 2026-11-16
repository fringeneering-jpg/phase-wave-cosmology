# pipeline_diagnostic.py - the 6-point autopsy of the vanished galaxies (2026-10-17)
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

ra2, de2, kt, cz = [], [], [], []
hdr = None
with open("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/rot/sparc_x/2mrs.txt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("RAJ2000"):
            hdr = line.split("\t")
            break
    for line in f:
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 5:
            continue
        try:
            vals = [float(p[0]), float(p[1]), float(p[2]), float(p[3])]
        except ValueError:
            continue
        if all(np.isfinite(v) for v in vals):
            ra2.append(vals[0]); de2.append(vals[1]); kt.append(vals[2]); cz.append(vals[3])
ra2 = np.array(ra2); de2 = np.array(de2); kt = np.array(kt); cz = np.array(cz)
print(f"1. ROWS PARSED: {len(ra2)}   (header cols: {hdr[:5]})")

# the target's cone
c1 = SkyCoord(ra=187.2779*u.deg, dec=2.0524*u.deg, frame="icrs")
c2 = SkyCoord(ra=ra2*u.deg, dec=de2*u.deg, frame="icrs")
sep = c1.separation(c2)
cone = sep < 2.0 * u.deg
print(f"2. CONE COUNT (2 deg): {cone.sum()}   (expected ~14)")
if cone.sum() > 0:
    print(f"   nearest separation: {sep[cone].min().to(u.arcmin).value:.2f} arcmin")
    print(f"   the cone's K magnitudes: {kt[cone][:5]}")
    print(f"   the cone's cz: {cz[cone][:5]}")
print(f"3. NEAREST OVERALL: {sep.min().to(u.arcmin).value:.2f} arcmin  (RA {ra2[sep.argmin()]:.3f}, Dec {de2[sep.argmin()]:.3f})")

# the masses: the K-band's the Ks_Mag - the ABSOLUTE magnitude needs the
# distance (the apparent K corrected by the distance modulus), then the
# luminosity's 10^(-0.4 (K_abs - K_sun_abs)), K_sun_abs ~ 3.28; M/L = 0.6 stated
d_pc = cz / 73.0 * 1e6
K_abs = kt - 5.0 * np.log10(d_pc) + 5.0
K_sun = 3.28
L_K = 10.0 ** (-0.4 * (K_abs - K_sun))
M_sun_kg = 1.989e30
M = 0.6 * L_K * M_sun_kg
valid = np.isfinite(M) & (M > 0)
print(f"4. SURVIVAL COUNT (valid masses): {valid.sum()}")

# the single largest pull within the cone
c0 = 2.9979e8; G = 6.674e-11
if cone.sum() > 0:
    d_lens = cz[cone] / 73.0 * 3.0857e22
    b_phys = sep[cone].to(u.rad).value * d_lens
    pulls = 4.0 * G * M[cone] / (b_phys * c0**2)
    print(f"5. LARGEST SINGLE PULL: {pulls.max()*206264806.7:.3f} mas  (at {sep[cone].min().to(u.arcmin).value:.2f} arcmin)")

# the raw vector sum over the cone
pa = c1.position_angle(c2[cone])
x = (pulls * np.sin(pa.to(u.rad).value)).sum()
y = (pulls * np.cos(pa.to(u.rad).value)).sum()
print(f"6. RAW SUM:  x = {x:.6e} rad,  y = {y:.6e} rad  ->  |v| = {np.sqrt(x*x+y*y)*206264806.7:.3f} mas")
