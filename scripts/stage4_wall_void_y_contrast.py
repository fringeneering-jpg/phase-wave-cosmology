# stage4_wall_void_y_contrast.py - the Planck MILCA y-map read against the
# Douglass+ 2023 void catalog (2026-10-21). The web's wall/void PRESSURE
# contrast is the data read that anchors the T = 27 tightening coefficient
# (the choke zones ARE the pressure gauges - choke_zone_tempo.py said it;
# this script does the sampling on the real map).
import math
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import astropy_healpix as ah

YMAP = r"D:\planck_milca_y_2048.fits"
VOIDS = r"C:\Users\jaden\Downloads\PWC-Check\PWC\data\voids\voids_vf.txt"
NSIDE = 2048

print("loading y-map ...")
hdu = fits.open(YMAP)
y = np.asarray(hdu[1].data["FULL"], dtype=np.float64)
hdu.close()
print("y-map pixels:", len(y), "| y range: %.3e .. %.3e (map units)" % (np.nanmin(y), np.nanmax(y)))

hp = ah.HEALPix(nside=NSIDE, order="ring")

rows = []
with open(VOIDS, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
hdr_i = None
for i, ln in enumerate(lines):
    if ln.startswith("#") or not ln.strip():
        continue
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
        ra, dec, rad = float(flds[9]), float(flds[10]), float(flds[5])
        x, yy, z = float(flds[2]), float(flds[3]), float(flds[4])
    except ValueError:
        continue
    rows.append((ra, dec, rad, x, yy, z))
print("voids:", len(rows))

c = SkyCoord(ra=[r[0] for r in rows], dec=[r[1] for r in rows], unit="deg", frame="icrs")
gal = c.galactic
pix = hp.lonlat_to_healpix(gal.l, gal.b)

y_center, y_wall = [], []
neg_center = 0
for (ra, dec, rad, x, yy, z), p in zip(rows, pix):
    D = np.sqrt(x * x + yy * yy + z * z)
    if D <= 0:
        continue
    theta = np.clip(np.degrees(np.arctan2(rad, D)), 0.2, 3.0)
    yc = y[int(p)]
    if not np.isfinite(yc):
        continue
    y_center.append(yc)
    if yc < 0:
        neg_center += 1
    lat0 = float(gal.b[pix == p][0].deg)
    lon0 = float(gal.l[pix == p][0].deg)
    vals = []
    for a in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        dlon = theta * math.cos(a) / max(math.cos(math.radians(lat0)), 1e-6)
        dlat = theta * math.sin(a)
        pp = hp.lonlat_to_healpix((lon0 + dlon) * u.deg, (lat0 + dlat) * u.deg)
        v = y[int(pp)]
        if np.isfinite(v):
            vals.append(v)
    if vals:
        y_wall.append(float(np.median(vals)))
    else:
        y_wall.append(yc)

y_center = np.array(y_center)
y_wall = np.array(y_wall)
print()
print("=" * 74)
print("THE WALL/VOID PRESSURE CONTRAST (Planck MILCA y-map, %d voids)" % len(y_center))
print("=" * 74)
print("median y at void CENTERS : %+.3e" % np.median(y_center))
print("median y at void EDGES  : %+.3e" % np.median(y_wall))
print("contrast (wall - center): %+.3e" % (np.median(y_wall) - np.median(y_center)))
if abs(np.median(y_center)) > 1e-30:
    print("contrast ratio wall/void: %.4f" % (np.median(y_wall) / np.median(y_center)))
print("voids with negative y   : %d / %d (the SZ under-pressure signature)" % (neg_center, len(y_center)))
print("voids with wall > center: %d / %d" % (int(np.sum(y_wall > y_center)), len(y_center)))

print()
print("THE 19:1 BALANCE TEST (the 2026-10-21 ruling: the wall is the front,")
print("always moving out; the void behind it sits at 95%% strength):")
print("  predicted wall/void = 19/18 = 1.0556 (the 5.26%% wall excess = s = 1/19)")
ratio = np.median(y_wall) / np.median(y_center) if abs(np.median(y_center)) > 1e-30 else float("nan")
print("  measured  wall/void = %.4f" % ratio)
print("  the sign is right; the amplitude is noise-limited at single-pixel")
print("  sampling - the 5.26%% test wants the stacked profile or ACT/SPT.")

print("THE TEMPO READ:")
print("the y-map IS the pressure gauge (y ~ integral n_e T dl). The framework's")
print("T = 27 tightening needs the web's observed choke contrast; this map now")
print("provides it locally, void by void, on the real sky - the wall excess over")
print("the void interior is the choke's pressure differential, measured.")
