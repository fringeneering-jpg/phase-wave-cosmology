import numpy as np
import healpy as hp
import pymaster as nmt
from astropy.io import fits

MAP = "/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HFI_353_field_IQU_2048_R4.00_full.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

print("Loading 50M pixel map...")
h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)

print("Converting to RING ordering for NaMaster...")
I = hp.reorder(I, n2r=True)
Q = hp.reorder(Q, n2r=True)
U = hp.reorder(U, n2r=True)

lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=False, lonlat=True)
b = lat

deep_mask  = (np.abs(b) >= 50.0).astype(float)
plane_mask = (np.abs(b) <= 20.0).astype(float)

print("Apodizing region masks...")
apo_deep  = nmt.mask_apodization(deep_mask, 2.0, apotype="C2")
apo_plane = nmt.mask_apodization(plane_mask, 2.0, apotype="C2")

def spectra_master(apo_mask, tag):
    print(f"\nProcessing {tag}...")

    f0 = nmt.NmtField(apo_mask, [I])
    f2 = nmt.NmtField(apo_mask, [Q, U], purify_b=True)

    print("  Computing mode-coupling matrix...")
    # bins must span the fields' full lmax (3*Nside-1 = 6143)
    bins = nmt.NmtBin.from_nside_linear(NSIDE, 16)
    w02 = nmt.NmtWorkspace()
    w02.compute_coupling_matrix(f0, f2, bins)

    print("  Extracting decoupled pseudo-spectra...")
    cl02_coupled = nmt.compute_coupled_cell(f0, f2)
    cl02_decoupled = w02.decouple_cell(cl02_coupled)

    # decoupled shape (2, n_bins): [0] = TE, [1] = TB; sum the ell 2-10 bins
    ells = bins.get_effective_ells()
    low = (ells >= 2) & (ells <= 10)
    cl_TE = cl02_decoupled[0][low].sum()
    cl_TB = cl02_decoupled[1][low].sum()

    beta_TB = float(cl_TB / max(cl_TE, 1e-30))
    print(f"  {tag}:  <TB/TE> ell=2-10 = {beta_TB:+.4f} rad = {np.degrees(beta_TB):+.3f} deg")
    return dict(tag=tag, beta=beta_TB)

r_deep  = spectra_master(apo_deep, "DEEP SPACE (the settled lattice)")
r_plane = spectra_master(apo_plane, "PLANE (the filament misalignment)")

print("\n" + "=" * 72)
d, p = r_deep["beta"], r_plane["beta"]
print(f"DECONVOLVED rotation angle:  deep {np.degrees(d):+.3f} deg,  plane {np.degrees(p):+.3f} deg")
print(f"the known dust systematic: ~0.3 deg, following the plane's filaments")
print(f"the committed prediction: the deep space carries the lattice's own sign")
if abs(d) > 3 * abs(p) and abs(p) < 0.01:
    print("VERDICT: the deep-space rotation DOMINATES - the lattice's sign is in the data")
elif abs(d - p) < 0.005:
    print("VERDICT: the deep-space rotation matches the plane's - no distinguishable lattice signal")
else:
    print(f"VERDICT: the deep-space rotation differs by {np.degrees(d-p):+.3f} deg")
print("=" * 72)
print("the honest receipt: deconvolved with the full mode-coupling matrix.")
print("the committed lattice orientation number remains the sign's reference")
print("to be stated before the final verdict is signed.")
