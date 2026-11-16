# hi4pi_read.py - the growth map's first read + the route's column (2026-10-17)
import healpy as hp
import numpy as np

m = hp.read_map("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HI4PI_NHI_HPX.fits.gz")
print("pixels:", len(m), "Nside:", hp.get_nside(m))
print("NHI range: %.2e to %.2e cm^-2" % (m.min(), m.max()))
print("median: %.2e cm^-2" % np.median(m))

# the route's first leg: the column along a controlled source's line of sight.
# The classic test source: 3C 273 (the first quasar, the position/redshift known
# to high precision) - the H1 column toward it is the medium's density's integral
# for the near stretch of its route.
# 3C 273: RA 187.2779 deg, Dec +2.0524 deg (J2000)
ra, dec = 187.2779, 2.0524
nside = hp.get_nside(m)
pix = hp.ang2pix(nside, ra, dec, lonlat=True)
nhi = m[pix]
print()
print("the route's column toward 3C 273:  N_HI = %.3e cm^-2" % nhi)
print("  (the near-stretch density integral - the growth's local leg)")
print()
print("the honest frame: this is the FIRST leg - the local H1 column. The full")
print("route adds the cosmic growth (the redshift's), the heavy bodies' bends")
print("(the 2MRS), and the dense-cool birefringence. The receipt: does the")
print("route's accounting land the source's observed position?")
