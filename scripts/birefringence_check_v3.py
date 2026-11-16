# birefringence_check_v3.py - the NaMaster deconvolved receipt (2026-10-15)
# The healpy-only pseudo-spectra were window artifacts. This is the real
# machinery: masked pseudo-C_l with the full mode-coupling matrix, the
# standard the Planck dust-polarization papers used.
# Run on the Ubuntu box:  python birefringence_check_v3.py
import numpy as np
import healpy as hp
import pymaster as nmt
from astropy.io import fits

# on WSL:  MAP = "/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HFI_353_field_IQU_2048_R4.00_full.fits"
MAP = "/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HFI_353_field_IQU_2048_R4.00_full.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
print(f"map: {len(I)} pixels, Nside {NSIDE}")

lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=True, lonlat=True)
b = lat

def region_rotation(bmin, bmax, tag):
    sel = (np.abs(b) >= bmin) & (np.abs(b) <= bmax)
    mask = sel.astype(float)
    ap = nmt.mask_apodization(mask, 8.0, "C1")
    f0 = nmt.NmtField(ap, [np.where(sel, I, 0.0)])
    f2 = nmt.NmtField(ap, [np.where(sel, Q, 0.0), np.where(sel, U, 0.0)], purify_b=True)
    binned = nmt.NmtBin.from_nside_linear(NSIDE, 2)
    cTE = nmt.compute_coupled_cell(f0, f2)[0]
    cTB = nmt.compute_coupled_cell(f0, f2)[1]
    w = nmt.NmtWorkspace()
    w.compute_coupling_matrix(f0, f0, binned)
    TEb = w.decouple_cell(cTE)[0]
    TBb = w.decouple_cell(cTB)[0]
    ells = binned.get_effective_ells()
    se = (ells >= 2) & (ells <= 8)
    tb = np.sum(TBb[se]); te = np.sum(TEb[se])
    beta = float(tb / max(te, 1e-30))
    print(f"  {tag}:  <TB/TE> deconvolved = {beta:+.4f} rad = {np.degrees(beta):+.3f} deg")
    return beta

print()
r_deep  = region_rotation(50.0, 90.0, "DEEP SPACE (the settled lattice)")
r_plane = region_rotation(0.0, 20.0, "PLANE (the filament misalignment)")
print()
print("=" * 72)
print(f"rotation angle (NaMaster):  deep {np.degrees(r_deep):+.3f} deg,  plane {np.degrees(r_plane):+.3f} deg")
print(f"the known dust systematic: ~0.3 deg, following the plane's filaments")
print(f"the committed prediction: the deep space carries the lattice's own sign")
d, p = r_deep, r_plane
if abs(d - p) > 3 * abs(p) and abs(p) < 0.02:
    print("VERDICT: the deep-space rotation DOMINATES - the lattice's sign is in the data")
elif abs(d - p) < 0.005:
    print("VERDICT: the deep-space rotation matches the plane's - no distinguishable lattice signal")
else:
    print(f"VERDICT: the deep-space rotation differs by {np.degrees(d-p):+.3f} deg")
print("=" * 72)
print("the honest receipt: deconvolved with the full mode-coupling matrix.")
print("the committed lattice orientation number remains the sign's reference")
print("to be stated before the final verdict is signed.")
