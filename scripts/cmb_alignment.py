# cmb_alignment.py - the settled sky's ANGLES, not its twist (2026-10-17)
# The sky does NOT twist (the medium doesn't rotate; the matter ALIGNS).
# The framework's test is the alignment's COHERENCE: the settled regions
# should show a single template's orientation (the Rayleigh R high) against
# the plane's filament-varying angles. The same statistic the 353 dust read.
import numpy as np
import healpy as hp
from astropy.io import fits

MAP  = "/mnt/c/Users/jaden/Downloads/Lambda.fits"
MASK = "/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/mask_pol.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

print("loading the CMB IQU and the Planck mask...")
h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
m = fits.open(MASK)
mask = m[1].data.astype(float).reshape(-1) if len(m) > 1 else m[0].data.astype(float).reshape(-1)

I = hp.reorder(I, n2r=True); Q = hp.reorder(Q, n2r=True); U = hp.reorder(U, n2r=True)
mask = hp.reorder(mask, n2r=True)
lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=False, lonlat=True)
b = lat

# the matter's orientation and the region split
psi = 0.5 * np.arctan2(U, Q)

def coherence(bmin, bmax, tag):
    sel = (np.abs(b) >= bmin) & (np.abs(b) <= bmax) & (mask > 0.5) & np.isfinite(psi)
    n = sel.sum()
    if n < 1000:
        print(f"  {tag}: too few pixels ({n})"); return None
    z = np.exp(2j * psi[sel])
    R = float(np.abs(z.mean()))
    ang = float(0.5 * np.angle(z.mean()))
    print(f"  {tag}: n={n}, alignment R={R:.4f}, mean orientation={np.degrees(ang):+.2f} deg")
    return dict(R=R, ang=ang)

print()
r_deep  = coherence(50.0, 90.0, "DEEP SPACE (the settled lattice)")
r_plane = coherence(0.0, 20.0, "PLANE (the filaments)")
print()
print("=" * 72)
if r_deep and r_plane:
    print(f"alignment coherence:  deep R={r_deep['R']:.4f},  plane R={r_plane['R']:.4f}")
    print("the committed prediction: the settled deep space follows the lattice's")
    print("single template - its angles should COHERE (R high) against the plane's")
    if r_deep["R"] > 1.3 * r_plane["R"]:
        print("VERDICT: the deep space aligns MORE coherently - the template is in the data")
    elif abs(r_deep["R"] - r_plane["R"]) < 0.05:
        print("VERDICT: equal alignment - no distinguishable template at this read")
    else:
        print(f"VERDICT: the deep space aligns LESS coherently (R {r_deep['R']:.4f} vs {r_plane['R']:.4f})")
print("=" * 72)
print("honest notes: the sky does NOT twist - the question is the angles'")
print("coherence, not the rotation. The CMB's polarization is the early light's;")
print("the settled-region read is the template's first CMB test.")
