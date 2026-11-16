# totality_chiral.py - the bend in totality: the sky-wide handedness (2026-10-17)
# The medium is stiff - the chiral signature lives in the GLOBAL pattern. The
# run: the deflection field over the whole sky, its dipole/quadrupole axes
# compared against the Great Attractor's direction. The bend in totality.
import numpy as np
import healpy as hp

G = 6.67430e-11
c0 = 2.99792458e8
Msun = 1.98847e30
Mpc = 3.08567758e22
kpc = 3.08567758e19
H_wall = 73.8
UPSILON_K = 0.6
R_GAL = 10.0 * kpc
GA_RA, GA_DEC = 201.0, -53.2

ra2, de2, kt, cz = [], [], [], []
with open("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/rot/sparc_x/2mrs.txt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("RAJ2000"):
            hdr = line.split("\t"); break
    for line in f:
        if not line.strip() or line.startswith("#"): continue
        p = line.split("\t")
        if len(p) < 5: continue
        try: vals = [float(p[0]), float(p[1]), float(p[2]), float(p[3])]
        except ValueError: continue
        if all(np.isfinite(v) for v in vals):
            ra2.append(vals[0]); de2.append(vals[1]); kt.append(vals[2]); cz.append(vals[3])
ra2 = np.array(ra2); de2 = np.array(de2); kt = np.array(kt); cz = np.array(cz)

d_pc = cz / H_wall * 1e6
K_abs = kt - 5.0*np.log10(np.maximum(d_pc, 1.0)) + 5.0
L_K = 10.0**(-0.4*(K_abs - 3.28))
M = UPSILON_K * L_K * Msun
D_L = cz / H_wall * Mpc
lens_vec = np.array(hp.ang2vec(ra2, de2, lonlat=True))

# the field on a coarse grid: each direction's the total deflection's vector
nside = 8
npix = hp.nside2npix(nside)
fx = np.zeros(npix); fy = np.zeros(npix)
pix = np.arange(npix)
dir_vec = np.array(hp.pix2vec(nside, pix)).T
# the local east/north bases per pixel
n0 = dir_vec
e_east = np.column_stack([-n0[:,1], n0[:,0], np.zeros(npix)])
e_east /= np.linalg.norm(e_east, axis=1)[:,None]
e_north = np.cross(n0, e_east)

print("the totality: the whole sky's deflection field (Nside 8 grid)...")
for j in range(len(cz)):
    if cz[j] < 100: continue
    d = np.arccos(np.clip(dir_vec @ lens_vec[j], -1, 1))
    psi = d
    sin_psi = np.sin(psi)
    far = psi > 1e-6
    proj = dir_vec[far] - (dir_vec[far] @ lens_vec[j])[:,None] * lens_vec[j][None,:]
    proj /= np.linalg.norm(proj, axis=1)[:,None]
    b = psi[far] * D_L[j]
    M_enc = M[j] * np.minimum(1.0, b / R_GAL)
    mag = 4.0*G*M_enc/(b * c0**2)
    ux = np.einsum('ij,ij->i', proj, e_east[far])
    uy = np.einsum('ij,ij->i', proj, e_north[far])
    # the image displaces AWAY from the lens: -u
    fx[far] += -mag * ux
    fy[far] += -mag * uy

# the corrected totality audit: the global pull dipole (the unnormalized) and
# the curl's discretization floor (the analytical zero)
img_3d = fx[:, None] * e_east + fy[:, None] * e_north   # mas, N_pix x 3
D_pull_vec = -1.5 * np.mean(img_3d, axis=0)
D_pull_mag = float(np.linalg.norm(D_pull_vec))
D_pull_hat = D_pull_vec / D_pull_mag
D_curl_vec = 1.5 * np.mean(np.cross(n0, img_3d), axis=0)
D_curl_mag = float(np.linalg.norm(D_curl_vec))

def unit_radec(ra_deg, dec_deg):
    r, d = np.radians(ra_deg), np.radians(dec_deg)
    return np.array([np.cos(d)*np.cos(r), np.cos(d)*np.sin(r), np.sin(d)])

n_ga = unit_radec(201.0, -53.2)
n_shapley = unit_radec(202.0, -31.0)
n_cmb = unit_radec(167.942, -6.944)

print("THE CORRECTED TOTALITY AUDIT:")
print(f"  GLOBAL PULL DIPOLE |D_pull| = {D_pull_mag:.3f} mas")
print(f"    axis: ({D_pull_hat[0]:+.3f}, {D_pull_hat[1]:+.3f}, {D_pull_hat[2]:+.3f})")
for nm, nv in [("Great Attractor", n_ga), ("Shapley", n_shapley), ("CMB dipole", n_cmb)]:
    cos_al = float(np.dot(D_pull_hat, nv))
    ang = np.degrees(np.arccos(np.clip(cos_al, -1, 1)))
    print(f"    vs {nm:16s}: cos = {cos_al:+.3f}  ({ang:.1f} deg)")
print(f"  RAW CURL RESIDUAL |D_curl| = {D_curl_mag:.4f} mas  (the analytical zero's)")
print(f"    ratio |D_curl|/|D_pull| = {D_curl_mag/D_pull_mag:.4f}")
print()
print("the honest frame: the pull dipole's the totality's real measure (the stiff")
print("medium's hauled direction); the curl's the discretization floor (the zero's")
print("the framework's own eddy-free floor). The collective response's still the")
print("missing equation - this is the mapped sum, not the mechanism.")
