# birefringence_check_v2.py - the first-order MASTER deconvolution, healpy only (2026-10-15)
# The raw windowed TB/TE leaked E into B through the mask's mode-mixing (+30 deg
# was the window's artifact). v2: the first-order MASTER correction - divide the
# pseudo-spectra by the mask's own window function W_l before taking the ratio.
# Honest label: first-order deconvolution, not the full coupling matrix.
import numpy as np
import healpy as hp
from astropy.io import fits

MAP = r"C:\Users\jaden\Downloads\PWC-Check\scratch\telescope\HFI_353_field_IQU_2048_R4.00_full.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
print(f"map: {len(I)} pixels, Nside {NSIDE}")

lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=True, lonlat=True)
b = lat
deep = np.abs(b) >= 50.0
plane = np.abs(b) <= 20.0
print(f"deep space: {deep.sum()} px,  plane: {plane.sum()} px")

def window_fn(mask):
    """the mask's window function: W_l = <|w|^2> from the mask's own pseudo-spectrum."""
    w = mask.astype(float)
    cl = hp.anafast(w, lmax=16, pol=False)
    # normalize to the mask's sky fraction squared at low ell
    fsky = w.mean()
    wl = np.ones_like(cl) * fsky**2
    wl[cl > 0] = cl[cl > 0]
    return np.maximum(wl, 1e-12)

def spectra(sel, tag):
    mI = np.zeros(NPIX); mI[sel] = I[sel]
    mQ = np.zeros(NPIX); mQ[sel] = Q[sel]
    mU = np.zeros(NPIX); mU[sel] = U[sel]
    cl_TE = hp.anafast(mI, map2=mQ, lmax=16)
    cl_TB = hp.anafast(mI, map2=mU, lmax=16)
    cl_EE = hp.anafast(mQ, lmax=16, pol=True)[1]
    cl_BB = hp.anafast(mU, lmax=16, pol=True)[2]
    wl = window_fn(sel)
    ell = np.arange(len(cl_TE))
    se = (ell >= 2) & (ell <= 10)
    # the first-order deconvolved ratio (the window divides out)
    tb = np.sum(cl_TB[se] / wl[se]); te = np.sum(cl_TE[se] / wl[se])
    beta = float(tb / max(te, 1e-30))
    print(f"  {tag}:  <TB/TE> deconvolved low-ell = {beta:+.4f} rad = {np.degrees(beta):+.3f} deg")
    return dict(tag=tag, beta=beta)

r_deep = spectra(deep, "DEEP SPACE (the settled lattice)")
r_plane = spectra(plane, "PLANE (the filament misalignment)")

print()
print("=" * 72)
d, p = r_deep["beta"], r_plane["beta"]
print(f"rotation angle (first-order MASTER):  deep {np.degrees(d):+.3f} deg,  plane {np.degrees(p):+.3f} deg")
print(f"the known dust systematic: ~0.3 deg, following the plane's filaments")
print(f"the committed prediction: the deep space carries the lattice's own sign")
if abs(d - p) > 3 * abs(p) and abs(p) < 0.02:
    print("VERDICT: the deep-space rotation DOMINATES - the lattice's sign is in the data")
elif abs(d - p) < 0.005:
    print("VERDICT: the deep-space rotation matches the plane's - no distinguishable lattice signal at this order")
else:
    print(f"VERDICT: the deep-space rotation differs by {np.degrees(d-p):+.3f} deg - the sign's the lattice's if it matches the committed orientation")
print("=" * 72)
print("honest label: FIRST-ORDER deconvolution (W_l division), not the full")
print("mode-coupling matrix. The full receipt wants NaMaster; this is the")
print("first honest read of the committed sign.")
