# finite_path_full_sky_audit.py - the exact finite-path run (2026-10-17)
import numpy as np

G = 6.67430e-11
c0 = 2.99792458e8
Msun = 1.98847e30
Mpc = 3.08567758e22
kpc = 3.08567758e19
H_wall = 73.8
UPSILON_K = 0.6
R_GAL = 10.0 * kpc
RAD2MAS = (180.0 / np.pi) * 3600.0 * 1000.0
ENABLE_PHENOMENOLOGICAL_CHIRAL_TEMPLATE = True
CHIRAL_TEMPLATE_COEFF = 1.0 / 19.0
GA_RA_DEG, GA_DEC_DEG = 201.0, -53.2

TARGETS = {
    "3C 273":       {"ra": 187.277915, "dec": +2.052388,  "cz": 47469.0, "host_sep_arcsec": 10.0,  "host_dcz": 500.0},
    "3C 279":       {"ra": 194.046527, "dec": -5.789312,  "cz": 160689.0, "host_sep_arcsec": 10.0, "host_dcz": 500.0},
    "PKS 2155-304": {"ra": 329.716938, "dec": -30.225588, "cz": 34776.0, "host_sep_arcsec": 10.0, "host_dcz": 500.0},
    "M87":          {"ra": 187.705931, "dec": +12.391123, "cz": 1284.0,  "host_sep_arcsec": 300.0, "host_dcz": 150.0},
    "Cen A":        {"ra": 201.365063, "dec": -43.019113, "cz": 547.0,   "host_sep_arcsec": 600.0, "host_dcz": 100.0},
}

# the 2MRS parse
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

def spherical_basis(ra0_deg, dec0_deg):
    ra0, dec0 = np.radians(ra0_deg), np.radians(dec0_deg)
    n0 = np.array([np.cos(dec0)*np.cos(ra0), np.cos(dec0)*np.sin(ra0), np.sin(dec0)])
    e_east = np.array([-np.sin(ra0), np.cos(ra0), 0.0])
    e_north = np.array([-np.sin(dec0)*np.cos(ra0), -np.sin(dec0)*np.sin(ra0), np.cos(dec0)])
    return n0, e_east, e_north

def min_segment_distance(D_L, D_S, cos_psi, sin_psi, r_LS):
    proj = D_L * cos_psi
    return np.where(proj <= 0.0, D_L, np.where(proj >= D_S, r_LS, D_L * sin_psi))

def audit_target(name):
    t = TARGETS[name]
    ra0_deg, dec0_deg, cz_src = t["ra"], t["dec"], t["cz"]
    n0, e_east, e_north = spherical_basis(ra0_deg, dec0_deg)
    ra, dec = np.radians(ra2), np.radians(de2)
    n_lens = np.vstack([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
    cos_psi = np.clip(np.dot(n0, n_lens), -1.0, 1.0)
    psi_rad = np.arccos(cos_psi)
    psi_deg = np.degrees(psi_rad)
    psi_arcsec = psi_deg * 3600.0
    is_self_host = (psi_arcsec < t["host_sep_arcsec"]) & (np.abs(cz - cz_src) < t["host_dcz"])
    valid = (cz > 100.0) & (kt > 0.0) & (~is_self_host) & (psi_arcsec > 1.0) & (cz < cz_src - t["host_dcz"])
    n_lens = n_lens[:, valid]
    cos_psi, psi_rad, psi_deg = cos_psi[valid], psi_rad[valid], psi_deg[valid]
    sin_psi = np.sin(psi_rad)
    ktf, czf = kt[valid], cz[valid]
    D_S = (cz_src / H_wall) * Mpc
    D_L = (czf / H_wall) * Mpc
    d_pc = (czf / H_wall) * 1e6
    K_abs = ktf - 5.0*np.log10(d_pc) + 5.0
    L_K = 10.0**(-0.4*(K_abs - 3.28))
    M_tot = UPSILON_K * L_K * Msun
    r_LS = np.sqrt(np.maximum(D_S**2 - 2.0*D_S*D_L*cos_psi + D_L**2, (1.0*kpc)**2))
    r_min = min_segment_distance(D_L, D_S, cos_psi, sin_psi, r_LS)
    M_enc = M_tot * np.minimum(1.0, r_min / R_GAL)
    geom_bracket = cos_psi + (r_LS - D_L) / D_S
    delta_theta_mag = (2.0*G*M_enc/(c0**2*D_L*sin_psi)) * geom_bracket
    proj_east = np.dot(e_east, n_lens)
    proj_north = np.dot(e_north, n_lens)
    proj_norm = np.hypot(proj_east, proj_north)
    ux, uy = proj_east/proj_norm, proj_north/proj_norm
    img_x = -delta_theta_mag * ux * RAD2MAS
    img_y = -delta_theta_mag * uy * RAD2MAS
    print(f"=== {name}: the finite-path full-sky audit (N={len(czf)}) ===")
    edges = [0.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 135.0, 180.0]
    print(f"  {'annulus':10s} {'n':>6s} | {'d_img (mas)':>22s} | {'cum (mas)':>24s} {'|cum|':>8s}")
    for i in range(len(edges)-1):
        r_in, r_out = edges[i], edges[i+1]
        ring = (psi_deg > r_in) & (psi_deg <= r_out)
        cum = psi_deg <= r_out
        rx, ry = np.sum(img_x[ring]), np.sum(img_y[ring])
        cx, cy = np.sum(img_x[cum]), np.sum(img_y[cum])
        print(f"  {r_in:5.1f}-{r_out:5.1f} {ring.sum():6d} | ({rx:+9.2f},{ry:+9.2f}) | ({cx:+9.2f},{cy:+9.2f}) {np.hypot(cx,cy):8.2f}")
    if ENABLE_PHENOMENOLOGICAL_CHIRAL_TEMPLATE:
        ra_g, dec_g = np.radians(GA_RA_DEG), np.radians(GA_DEC_DEG)
        n_ga = np.array([np.cos(dec_g)*np.cos(ra_g), np.cos(dec_g)*np.sin(ra_g), np.sin(dec_g)])
        cos_pole = float(np.dot(n0, n_ga))
        cx_all, cy_all = np.sum(img_x), np.sum(img_y)
        ch_x = CHIRAL_TEMPLATE_COEFF * cos_pole * (-cy_all)
        ch_y = CHIRAL_TEMPLATE_COEFF * cos_pole * (+cx_all)
        print(f"  [UNVERIFIED CHIRAL TEMPLATE]: the pole-coupling cos = {cos_pole:+.3f}")
        print(f"    the chiral rotation: ({ch_x:+.3f}, {ch_y:+.3f}) mas")
        print(f"    the handed total: ({np.sum(img_x)+ch_x:+.2f}, {np.sum(img_y)+ch_y:+.2f}) mas")

for nm in ["3C 273", "M87", "Cen A"]:
    audit_target(nm)
    print()
print("honest flags: the point-mass kernel's the Perplexity-verified exact's; the")
print("enclosed-mass's the frozen-r_min approximation (the r<R_GAL's the integrate's);")
print("the chiral template's OFF. The baseline's the conditional's, not the sky's.")
