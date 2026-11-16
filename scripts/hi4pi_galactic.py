import healpy as hp
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

m = hp.read_map("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HI4PI_NHI_HPX.fits.gz")
nside = hp.get_nside(m)

sample = [
    ("3C 273", 187.2779, 2.0524),
    ("3C 279", 194.0465, -5.7893),
    ("PKS 2155-304", 329.7169, -30.2256),
    ("Centaurus A", 201.3651, -43.0191),
    ("M87", 187.7059, 12.3911),
]
print(f"  {'source':14s} {'l':>9s} {'b':>9s} {'N_HI':>12s}")
for name, ra, dec in sample:
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs")
    g = c.galactic
    pix = hp.ang2pix(nside, g.l.deg, g.b.deg, lonlat=True)
    val = m[pix]
    print(f"  {name:14s} {g.l.deg:9.2f} {g.b.deg:9.2f} {val:12.2f}")
