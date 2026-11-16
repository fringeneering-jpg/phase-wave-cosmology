# stage4_wall_void_stack.py - PILLAR 5 RANK-1 ATTACK (auditor run, 2026-10-21)
# The wall/void 19/18 = 1.0556 contrast, stacked over the Douglass+ 2023 void
# catalog on the Planck MILCA y-map. Kill conditions PRE-REGISTERED (from the
# Pillar 5 audit): (1) decisiveness gate: bootstrap 68% band half-width <= 0.0556;
# (2) KILL if 2-sigma band excludes 19/18, i.e. R <= 1.02 or R >= 1.09;
# (3) KILL if the stacked wall-minus-center profile is flat or negative;
# (4) ACT cross-check named (not run here - no ACT map on disk).
# This file lives in scratch/ - it is NOT part of the repo. No fitted parameters.
import math
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import astropy_healpix as ah

YMAP = r"D:\planck_milca_y_2048.fits"
VOIDS = r"C:\Users\jaden\Downloads\PWC-Check\PWC\data\voids\voids_vf.txt"
NSIDE = 2048
PRED = 19.0 / 18.0  # the frozen zero-parameter prediction

rng = np.random.default_rng(20261021)

print("loading y-map ...")
hdu = fits.open(YMAP)
y = np.asarray(hdu[1].data["FULL"], dtype=np.float64)
hdu.close()
print("y-map pixels:", len(y), "| finite:", np.isfinite(y).sum())

hp = ah.HEALPix(nside=NSIDE, order="ring")

# --- parse the canonical catalog (same columns as stage4_wall_void_y_contrast.py)
rows = []
with open(VOIDS, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
hdr_i = None
for i, ln in enumerate(lines):
    if "recno" in ln:
        hdr_i = i
        break
dash_i = None
for i in range(hdr_i + 1, min(hdr_i + 25, len(lines))):
    if set(lines[i].strip().replace("\t", "")) == set("-"):
        dash_i = i
        break
for ln in lines[dash_i + 1:]:
    if not ln.strip() or ln.startswith("#"):
        continue
    flds = ln.split()
    if len(flds) < 12:
        continue
    try:
        cosmo = flds[1]
        x, yy, zz = float(flds[2]), float(flds[3]), float(flds[4])
        rad, s = float(flds[5]), float(flds[8])
        ra, dec = float(flds[9]), float(flds[10])
        edge = int(flds[7])
    except ValueError:
        continue
    rows.append((cosmo, x, yy, zz, rad, s, ra, dec, edge))
print("catalog rows:", len(rows), "| Planck2018:", sum(r[0] == "Planck2018" for r in rows))

c = SkyCoord(ra=[r[6] for r in rows], dec=[r[7] for r in rows], unit="deg", frame="icrs")
gal = c.galactic
pix0 = hp.lonlat_to_healpix(gal.l, gal.b)

def sample_ring(lon0, lat0, r_deg, n):
    out = []
    for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
        dlon = r_deg * math.cos(a) / max(math.cos(math.radians(lat0)), 1e-6)
        dlat = r_deg * math.sin(a)
        pp = hp.lonlat_to_healpix((lon0 + dlon) * u.deg, (lat0 + dlat) * u.deg)
        v = y[int(pp)]
        if np.isfinite(v):
            out.append(v)
    return out

RBINS = [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35]
profiles = []   # per void: median y at each r/theta bin
wall_all, center_all = [], []
per_void_ratio = []
cosmo_list, s_list = [], []
for (cosmo, x, yy, zz, rad, s, ra, dec, edge), p in zip(rows, pix0):
    D = math.sqrt(x * x + yy * yy + zz * zz)
    if D <= 0:
        continue
    lat0 = float(gal.b[pix0 == p][0].deg)
    lon0 = float(gal.l[pix0 == p][0].deg)
    if abs(lat0) < 20.0:  # galactic-plane mask, pre-registered
        continue
    theta = np.clip(math.degrees(math.atan2(rad, D)), 0.2, 3.0)
    yc = y[int(p)]
    if not np.isfinite(yc):
        continue
    prof = []
    for rb in RBINS:
        vals = sample_ring(lon0, lat0, rb * theta, 12)
        prof.append(float(np.median(vals)) if vals else float("nan"))
    if not np.all(np.isfinite(prof)):
        continue
    profiles.append(prof)
    wall = float(np.median(sample_ring(lon0, lat0, 1.0 * theta, 24)))
    center = float(np.median(sample_ring(lon0, lat0, 0.35 * theta, 12)))
    wall_all.append(wall)
    center_all.append(center)
    if abs(center) > 1e-30:
        per_void_ratio.append(wall / center)
    cosmo_list.append(cosmo)
    s_list.append(s)

profiles = np.array(profiles)
wall_all = np.array(wall_all)
center_all = np.array(center_all)
per_void_ratio = np.array(per_void_ratio)
n = len(wall_all)
print("voids used (|b|>=20 deg, finite):", n)

# ---- frozen statistic: R = median(y_wall)/median(y_void)
R = np.median(wall_all) / np.median(center_all) if abs(np.median(center_all)) > 1e-30 else float("nan")

# ---- bootstrap 68% band over voids (resample voids, recompute R)
B = 2000
idx = np.arange(n)
Rboot = np.empty(B)
for b in range(B):
    i = rng.choice(idx, size=n, replace=True)
    wb, cb = wall_all[i], center_all[i]
    Rboot[b] = np.median(wb) / np.median(cb) if abs(np.median(cb)) > 1e-30 else float("nan")
Rboot = Rboot[np.isfinite(Rboot)]
lo, hi = np.percentile(Rboot, [16, 84])

print("=" * 74)
print("THE STACKED WALL/VOID PRESSURE CONTRAST (Planck MILCA y-map, %d voids)" % n)
print("=" * 74)
print("median y at void centers (r=0.35 theta): %+.4e" % np.median(center_all))
print("median y at void walls   (r=1.00 theta): %+.4e" % np.median(wall_all))
print("wall - center: %+.4e" % (np.median(wall_all) - np.median(center_all)))
print("voids with negative center y: %d / %d" % (int(np.sum(center_all < 0)), n))
print("voids with wall > center:     %d / %d" % (int(np.sum(wall_all > center_all)), n))
print()
print("PREDICTED wall/void = 19/18 = %.4f" % PRED)
print("MEASURED  R = median(wall)/median(center) = %.4f" % R)
print("bootstrap 68%% band: [%.4f, %.4f]  (half-width %.4f)" % (lo, hi, (hi - lo) / 2))
if np.isfinite(lo) and np.isfinite(hi):
    print("distance from prediction: %+.4f  (band half-width %.4f)" % (R - PRED, (hi - lo) / 2))
print("per-void median ratio (median of ratios): %.4f" % np.median(per_void_ratio))

# ---- stacked radial profile
prof_med = np.median(profiles, axis=0)
prof_lo, prof_hi = np.percentile(profiles, [16, 84], axis=0)
print()
print("STACKED RADIAL PROFILE (median over voids, r in units of void radius):")
print("  bin    median y       68%% band")
for rb, m, l, h in zip(RBINS, prof_med, prof_lo, prof_hi):
    print("  %.2f   %+.4e   [%+.4e, %+.4e]" % (rb, m, l, h))
wall_bin = np.median(profiles[:, 4])  # r=0.95
cent_bin = np.median(profiles[:, 1])  # r=0.35
print("  profile wall(r=0.95)-center(r=0.35): %+.4e" % (wall_bin - cent_bin))

# ---- distance-binned robustness (redshift proxy via comoving distance s)
print()
print("DISTANCE-BINNED (comoving distance s in h^-1 Mpc, redshift proxy):")
s_arr = np.array(s_list)
for lo_s, hi_s, lab in [(0, 200, "near  s<200"), (200, 260, "mid   200-260"), (260, 400, "far   s>260")]:
    m = (s_arr >= lo_s) & (s_arr < hi_s)
    if m.sum() < 30:
        continue
    wb, cb = wall_all[m], center_all[m]
    if abs(np.median(cb)) > 1e-30:
        print("  %-12s n=%4d  R=%.4f" % (lab, m.sum(), np.median(wb) / np.median(cb)))

# ---- kill-condition verdicts (pre-registered, evaluated in order)
print()
print("KILL-CONDITION VERDICTS (frozen before the data):")
band_half = (hi - lo) / 2 if np.isfinite(lo) and np.isfinite(hi) else float("inf")
if band_half > 0.0556:
    print("  1. DECISIVENESS GATE: band half-width %.4f > 0.0556 -> NOT DECISIVE. PENDING." % band_half)
else:
    print("  1. DECISIVENESS GATE: band half-width %.4f <= 0.0556 -> decisive band." % band_half)
    sig = (hi - lo) / 2 * 2  # 2-sigma ~ 2x the 68% half-width, crude
    lo2, hi2 = R - 2 * band_half, R + 2 * band_half
    if hi2 < PRED or lo2 > PRED:
        print("  2. KILL: 2-sigma band [%.4f, %.4f] excludes 19/18 -> PREDICTION DEAD." % (lo2, hi2))
    else:
        print("  2. SURVIVES: 2-sigma band [%.4f, %.4f] includes 19/18." % (lo2, hi2))
    if R <= 1.02 or R >= 1.09:
        print("  2b. KILL on the hard window: R=%.4f outside (1.02, 1.09)." % R)
    else:
        print("  2b. R=%.4f inside the hard window (1.02, 1.09)." % R)
prof_diff = wall_bin - cent_bin
if prof_diff <= 0:
    print("  3. KILL: stacked wall-minus-center profile is flat or negative (%+.4e)." % prof_diff)
else:
    print("  3. SURVIVES: profile wall-minus-center is positive (%+.4e)." % prof_diff)
print("  4. ACT DR6 cross-check: NOT RUN here (no ACT map on disk) - remains the armed cross-check.")
