# baseline_astrometric_audit.py - the clean 5-step audit, run (2026-10-17)
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

G = 6.67430e-11
c0 = 2.99792458e8
Msun = 1.98847e30
Mpc = 3.08567758e22
kpc = 3.08567758e19
a0 = 6.6110e-11
H_wall = 73.8
UPSILON_K = 0.6
R_GAL = 10.0 * kpc
RAD2MAS = (180.0 / np.pi) * 3600.0 * 1000.0
RUN_EXPERIMENTAL_TENSION = False
R_STAG = 1.0 * Mpc

RA0_DEG, DEC0_DEG = 187.277915, 2.052388
CZ_SRC = 47469.0
D_S = (CZ_SRC / H_wall) * Mpc

# --- the 2MRS parse (the aligned four columns) ---
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

def project_cmb_dipole(ra0_deg, dec0_deg):
    v_cmb = 369.82e3
    ra_d, dec_d = np.radians(167.942), np.radians(-6.944)
    ra0, dec0 = np.radians(ra0_deg), np.radians(dec0_deg)
    v_vec = v_cmb * np.array([np.cos(dec_d)*np.cos(ra_d), np.cos(dec_d)*np.sin(ra_d), np.sin(dec_d)])
    e_alpha = np.array([-np.sin(ra0), np.cos(ra0), 0.0])
    e_delta = np.array([-np.sin(dec0)*np.cos(ra0), -np.sin(dec0)*np.sin(ra0), np.cos(dec0)])
    return float(np.dot(v_vec, e_alpha)), float(np.dot(v_vec, e_delta))

def gnomonic(ra_deg, dec_deg, ra0_deg, dec0_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    ra0, dec0 = np.radians(ra0_deg), np.radians(dec0_deg)
    dra = ra - ra0
    cos_c = np.sin(dec0)*np.sin(dec) + np.cos(dec0)*np.cos(dec)*np.cos(dra)
    dx = (np.cos(dec)*np.sin(dra)) / cos_c
    dy = (np.cos(dec0)*np.sin(dec) - np.sin(dec0)*np.cos(dec)*np.cos(dra)) / cos_c
    sep_rad = np.arccos(np.clip(cos_c, -1.0, 1.0))
    return dx, dy, sep_rad

v_east, v_north = project_cmb_dipole(RA0_DEG, DEC0_DEG)
print("== THE BASELINE AUDIT ==")
print(f"observer motion: v_East = {v_east/1e3:+.2f} km/s, v_North = {v_north/1e3:+.2f} km/s")
print(f"  (|v_perp| = {np.hypot(v_east, v_north)/1e3:.2f} km/s - the computed values, not the prose's)")
print()

dx, dy, sep_rad = gnomonic(ra2, de2, RA0_DEG, DEC0_DEG)
sep_deg = np.degrees(sep_rad)
sep_arcsec = sep_deg * 3600.0

fg = (sep_arcsec > 5.0) & (cz > 100.0) & (cz < CZ_SRC - 1000.0) & (kt > 0.0)
dx, dy, sep_rad, sep_deg = dx[fg], dy[fg], sep_rad[fg], sep_deg[fg]
kt, cz = kt[fg], cz[fg]

D_L = (cz / H_wall) * Mpc
d_pc = (cz / H_wall) * 1e6
K_abs = kt - 5.0*np.log10(d_pc) + 5.0
L_K = 10.0**(-0.4*(K_abs - 3.28))
M_tot = UPSILON_K * L_K * Msun
norm = np.hypot(dx, dy)
ux, uy = dx/norm, dy/norm
b1 = sep_rad * D_L
lever = 1.0 - (D_L / D_S)

M_enc1 = M_tot * np.minimum(1.0, b1/R_GAL)
alpha1 = 4.0*G*M_enc1/(b1*c0**2)
# Perplexity's sign: the image displaces AWAY from the lens
img1_x = -lever * alpha1 * ux * RAD2MAS
img1_y = -lever * alpha1 * uy * RAD2MAS

dt_sec = 1.0 * 3.15576e7
bx1, by1 = b1*ux, b1*uy
bx2 = bx1 - lever * (v_east * dt_sec)
by2 = by1 - lever * (v_north * dt_sec)
b2 = np.hypot(bx2, by2)
ux2, uy2 = bx2/b2, by2/b2
M_enc2 = M_tot * np.minimum(1.0, b2/R_GAL)
alpha2 = 4.0*G*M_enc2/(b2*c0**2)
img2_x = -lever * alpha2 * ux2 * RAD2MAS
img2_y = -lever * alpha2 * uy2 * RAD2MAS
dtheta_x = img2_x - img1_x
dtheta_y = img2_y - img1_y

print("== THE ANNULAR CONVERGENCE SWEEP ==")
edges = [0.0, 2.0, 5.0, 10.0, 15.0]
for i in range(len(edges)-1):
    r_in, r_out = edges[i], edges[i+1]
    ring = (sep_deg > r_in) & (sep_deg <= r_out)
    cum = sep_deg <= r_out
    rx, ry = np.sum(img1_x[ring]), np.sum(img1_y[ring])
    cx, cy = np.sum(img1_x[cum]), np.sum(img1_y[cum])
    ex, ey = np.sum(dtheta_x[cum])*1e6, np.sum(dtheta_y[cum])*1e6
    print(f"  {r_in:4.1f}-{r_out:4.1f} deg (n={ring.sum():4d}): d_img=({rx:+7.3f},{ry:+7.3f}) mas | "
          f"cum (n={cum.sum():4d}): img=({cx:+7.3f},{cy:+7.3f}) mas (|img|={np.hypot(cx,cy):7.3f}) | "
          f"drift=({ex:+.4f},{ey:+.4f}) nas")
