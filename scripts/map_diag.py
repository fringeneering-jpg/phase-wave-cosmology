import healpy as hp
import numpy as np

m = hp.read_map("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HI4PI_NHI_HPX.fits.gz", nest=True)
print("max:", m.max(), "mean:", m.mean(), "nonzero:", (m > 0).sum())
m2 = hp.reorder(m, n2r=True)
for name, ra, dec in [("3C273", 187.28, 2.05), ("M87", 187.71, 12.39), ("CenA", 201.37, -43.02)]:
    p = hp.ang2pix(hp.get_nside(m2), ra, dec, lonlat=True)
    print(name, "ring pix", p, "=", m2[p])
