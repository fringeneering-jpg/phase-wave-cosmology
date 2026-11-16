# birefringence_alignment.py - the corrected falsifier: matter aligns to the template (2026-10-16)
# The medium does NOT rotate (it is the static field). The MATTER (the dust's
# knots) aligns with the settled lattice's axes. The test is therefore the
# alignment's COHERENCE per region: the deep space should show the lattice's
# single orientation (tightly aligned), the plane the filaments' varying one.
# Retarded-path note: the light's travel-delay correction needs the 3D dust
# distances - named below, not yet applied (the raw alignment is the first read).
import numpy as np
import healpy as hp
from astropy.io import fits

MAP = "/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HFI_353_field_IQU_2048_R4.00_full.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
print(f"map: {len(I)} pixels, Nside {NSIDE}")

# RING for the coordinate routines
I = hp.reorder(I, n2r=True); Q = hp.reorder(Q, n2r=True); U = hp.reorder(U, n2r=True)
lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=False, lonlat=True)
b = lat

# the matter's orientation and its strength (the polarization fraction)
psi = 0.5 * np.arctan2(U, Q)          # rad, the alignment angle
Pfrac = np.sqrt(Q**2 + U**2) / np.maximum(I, 1e-12)

def region_stats(bmin, bmax, tag):
    sel = (np.abs(b) >= bmin) & (np.abs(b) <= bmax) & np.isfinite(psi) & (I > 0.5e-6)
    n = sel.sum()
    if n < 1000:
        print(f"  {tag}: too few pixels ({n})"); return None
    # the Rayleigh alignment statistic: R = |<e^{2i psi}>|, 0=random, 1=perfectly aligned
    z = np.exp(2j * psi[sel])
    R = float(np.abs(z.mean()))
    ang_mean = float(0.5 * np.angle(z.mean()))
    pfrac_mean = float(Pfrac[sel].mean())
    print(f"  {tag}: n={n}, alignment R={R:.4f}, mean orientation={np.degrees(ang_mean):+.2f} deg, "
          f"mean P-fraction={pfrac_mean:.4f}")
    return dict(tag=tag, R=R, ang=ang_mean, pfrac=pfrac_mean)

print()
r_deep  = region_stats(50.0, 90.0, "DEEP SPACE (the settled lattice)")
r_plane = region_stats(0.0, 20.0, "PLANE (the filaments)")
print()
print("=" * 72)
if r_deep and r_plane:
    print(f"alignment coherence:  deep R={r_deep['R']:.4f},  plane R={r_plane['R']:.4f}")
    print(f"mean orientation:     deep {np.degrees(r_deep['ang']):+.2f} deg,  plane {np.degrees(r_plane['ang']):+.2f} deg")
    print(f"the committed prediction: the settled deep space follows the lattice's")
    print(f"single template - its alignment should be COHERENT (R high) against the")
    print(f"plane's filament-varying orientations")
    if r_deep['R'] > 1.3 * r_plane['R']:
        print("VERDICT: the deep space aligns MORE coherently - the lattice's template is in the data")
    elif abs(r_deep['R'] - r_plane['R']) < 0.05:
        print("VERDICT: the deep space and the plane align equally - no distinguishable lattice template at this read")
    else:
        print(f"VERDICT: the deep space aligns LESS coherently (R {r_deep['R']:.4f} vs {r_plane['R']:.4f}) - the template's not in this raw read")
print("=" * 72)
print("honest notes: (1) RAW read - the retarded-path correction (the light's")
print("travel delay, t - d/c) is NOT yet applied; it needs the 3D dust distance")
print("map. (2) the medium does not rotate; the matter aligns. The -87 deg")
print("rotation angles from the old estimator are retired - they measured the")
print("wrong thing.")
