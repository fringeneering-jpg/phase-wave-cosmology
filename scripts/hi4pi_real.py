import gzip
import numpy as np
import healpy as hp
from astropy.coordinates import SkyCoord
import astropy.units as u

# the real columns: pix, l, b, pa, ring, N_HI (cm^-2)
rows = []
with gzip.open("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HI4PI_NHI_HPX.dat.gz", "rt") as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 6:
            try:
                rows.append((int(parts[0]), float(parts[-1])))
            except ValueError:
                continue
rows = np.array(rows)
nside = hp.npix2nside(len(rows))
m = np.zeros(len(rows))
m[rows[:, 0].astype(int)] = rows[:, 1]
print(f"the real NHI map: {len(m)} pixels, Nside {nside}")
print(f"  range {m.min():.2e} to {m.max():.2e}, median {np.median(m):.2e} cm^-2")
print()

sample = [
    ("3C 273", 187.2779, 2.0524),
    ("3C 279", 194.0465, -5.7893),
    ("PKS 2155-304", 329.7169, -30.2256),
    ("Centaurus A", 201.3651, -43.0191),
    ("M87", 187.7059, 12.3911),
]
print(f"  {'source':14s} {'l':>9s} {'b':>9s} {'N_HI (1e20)':>12s}")
for name, ra, dec in sample:
    g = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs").galactic
    pix = hp.ang2pix(nside, g.l.deg, g.b.deg, lonlat=True)
    print(f"  {name:14s} {g.l.deg:9.2f} {g.b.deg:9.2f} {m[pix]/1e20:12.2f}")
