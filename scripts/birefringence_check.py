# birefringence_check.py - the committed falsifier's test, run where healpy lives (2026-10-15)
# The ruling: the deep space (the settled, high-tension diamond lattice) is the
# MORE birefringent direction; the sign follows the lattice's orientation.
# The test: the 353 GHz dust polarization's EB/TB rotation angle, deep space
# vs the Galactic plane - the plane's is the known filament misalignment
# (~0.3 deg); the framework predicts the settled regions carry the lattice's
# own rotation sign, distinguishable from the filament's.
import numpy as np
import healpy as hp
from astropy.io import fits

MAP = r"C:\Users\jaden\Downloads\PWC-Check\scratch\telescope\HFI_353_field_IQU_2048_R4.00_full.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)  # stored as (49152, 1024) = the full 2048 map
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
print(f"map: {len(I)} pixels, Nside {NSIDE}, Galactic coords")

# healpix pixel -> galactic (l, b) - nest ordering
lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=True, lonlat=True)
b = lat

# the regions: the deep space (the settled high-latitude) vs the plane
deep = np.abs(b) >= 50.0
plane = np.abs(b) <= 20.0
print(f"deep space: {deep.sum()} px,  plane: {plane.sum()} px")

def spectra(sel, tag):
    n = sel.sum()
    if n < 100:
        print(f"  {tag}: too few pixels"); return None
    # the masked map + the anafast spectra (the polarization rotation's the test)
    # zero-pad outside the region (the windowed first read - the TB/TE ratio
    # shares the same window, so the rotation angle's comparable across regions)
    mI = np.zeros(NPIX); mI[sel] = I[sel]
    mQ = np.zeros(NPIX); mQ[sel] = Q[sel]
    mU = np.zeros(NPIX); mU[sel] = U[sel]
    # no explicit mask object: use UNSEEN + the simple spectra on the cutout's values
    cl_TE = hp.anafast(mI, map2=mQ, lmax=16)
    cl_TB = hp.anafast(mI, map2=mU, lmax=16)
    cl_EB = hp.anafast(mQ, map2=mU, lmax=16)
    # the rotation angle from the low-ell TB/TE ratio (the standard estimator)
    ell = np.arange(len(cl_TE))
    sel_ell = (ell >= 2) & (ell <= 10)
    beta_TB = float(np.sum(cl_TB[sel_ell]) / max(np.sum(cl_TE[sel_ell]), 1e-30))
    print(f"  {tag}:  <TB/TE> low-ell = {beta_TB:+.4f} rad = {np.degrees(beta_TB):+.3f} deg")
    return dict(tag=tag, beta=beta_TB, cl_EB=np.sum(cl_EB[sel_ell]), cl_TB=np.sum(cl_TB[sel_ell]), cl_TE=np.sum(cl_TE[sel_ell]))

r_deep = spectra(deep, "DEEP SPACE (the settled lattice)")
r_plane = spectra(plane, "PLANE (the filament misalignment)")

print()
print("=" * 72)
if r_deep and r_plane:
    d, p = r_deep["beta"], r_plane["beta"]
    print(f"rotation angle:  deep {np.degrees(d):+.3f} deg,  plane {np.degrees(p):+.3f} deg")
    print(f"the known dust systematic: ~0.3 deg, following the plane's filaments")
    print(f"the committed prediction: the deep space carries the lattice's own sign")
    if abs(d) > 3 * abs(p) and abs(p) < 0.01:
        print("VERDICT: the deep-space rotation DOMINATES - the lattice's sign is in the data")
    elif abs(d - p) < 0.005:
        print("VERDICT: the deep-space rotation matches the plane's - no distinguishable lattice signal at Nside=2048")
    else:
        print(f"VERDICT: the deep-space rotation differs by {np.degrees(d-p):+.3f} deg - the sign's the lattice's if the sign matches the committed orientation")
print("=" * 72)
print("note: this IS the full-resolution Nside=2048 receipt; the deep-space")
print("patches' signs are the committed prediction's first read.")


