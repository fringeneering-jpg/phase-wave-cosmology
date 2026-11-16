# stage3_first_look.py - first real-data confrontation (AR 12192, 2014-10-22)
# What it does:
#   1. HMI magnetogram -> invert Helioviewer's display scaling (approx B)
#   2. locate the strongest southern bipole = the AR box (algorithmic)
#   3. eps_a geometry proxy in the box -> Pi_V = C(rho)^2/(eps_a c0^2)
#      with the frozen law; report the blocked share vs the 2.15% threshold
#   4. AIA 171 light curves of the box: 12-min day + 1-min flare window
#   5. results -> data/solar/results/first_look_ar12192.json
# NOTE: Helioviewer JP2s are 8-bit display-scaled images. Fine for geometry,
# dynamics and light curves; NOT for quantitative EM-loci (needs JSOC FITS).
import os, sys, json
import numpy as np
import imageio.v3 as iio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v
from solar.hmi_inputs import eps_a_from_field

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
MP = 1.6726e-27
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
EPS_STAR = (C_Q / c0) ** 2

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "data", "solar", "raw", "ar12192_20141022"))

def read_jp2(path):
    return np.asarray(iio.imread(path), dtype=float)

# 1. HMI magnetogram, first frame of the day
mag_dir = os.path.join(BASE, "hmi_720s_day")
mag_files = sorted(os.listdir(mag_dir))
mag0 = read_jp2(os.path.join(mag_dir, mag_files[0]))
# Helioviewer HMI mag scaling: 0..255 covers -3000..+3000 G (approx, linear)
B = (mag0 / 255.0) * 6000.0 - 3000.0
# disk mask: off-disk pixels read as 0/255 -> false +/-3000 G at the limb
cy, cx = (np.array(B.shape) - 1) / 2.0
yy, xx = np.mgrid[0:B.shape[0], 0:B.shape[1]]
RR = np.hypot(xx - cx, yy - cy)
disk = RR < 0.92 * (B.shape[0] / 2.0)
B = np.where(disk, B, 0.0)
print(f"HMI magnetogram {mag_files[0]}: shape {B.shape}, |B| max on disk {np.abs(B).max():.0f} G")

# 2. locate the strongest southern bipole (strictly inside the disk,
#    smoothed, to avoid saturated limb/off-disk pixels)
inner = (RR < 0.92 * (B.shape[0] / 2.0)) & (mag0 < 254) & (mag0 > 1)
print(f"masked pixels: {inner.sum()}")
Bsm = np.where(inner, np.abs(B), 0.0)
W = 61  # wide boxcar: the AR blob beats any thin limb ring
Bsm = np.asarray([np.convolve(r, np.ones(W) / W, mode="same") for r in Bsm])
Bsm = np.asarray([np.convolve(c, np.ones(W) / W, mode="same") for c in Bsm.T]).T
half = B.shape[0] // 2
south = Bsm[half:, :]
y0, x0 = np.unravel_index(np.argmax(np.abs(south)), south.shape)
yc, xc = y0 + half, x0
print(f"on-disk median raw value: {np.median(mag0[inner]):.0f} (0 G should be ~128)")
print(f"|B| at AR center: {abs(Bsm[yc, xc]):.0f} G")
box = 400   # pixels = ~240 arcsec
y1, y2 = max(0, yc - box), min(B.shape[0], yc + box)
x1, x2 = max(0, xc - box), min(B.shape[1], xc + box)
Bbox = B[y1:y2, x1:x2]
print(f"AR box: pixels y[{y1}:{y2}] x[{x1}:{x2}], center y={yc} x={xc}")

# 3. eps_a geometry -> Pi_V
XX, YY = np.meshgrid(np.arange(Bbox.shape[1]), np.arange(Bbox.shape[0]))
eps = eps_a_from_field(Bbox, XX.astype(float), YY.astype(float))
pi_map = pi_v.pi_v_map(np.full_like(eps, RHO_Q), eps, c0, rho0, n_lad)
blocked = pi_map > 1.0
res = {
  "event": "AR 12192 flare day 2014-10-22",
  "note": "Helioviewer JP2s are 8-bit display-scaled: geometry/dynamics/light curves only, not quantitative EM",
  "mag_frame": mag_files[0],
  "ar_box": {"y1": int(y1), "y2": int(y2), "x1": int(x1), "x2": int(x2)},
  "eps_star": EPS_STAR,
  "eps_a_in_box": {"min": float(eps.min()), "median": float(np.median(eps)),
                   "max": float(eps.max())},
  "blocked_share": float(blocked.mean()),
  "pi_v_in_box": {"median": float(np.median(pi_map)), "max": float(pi_map.max())},
  "B_in_box": {"min_G": float(Bbox.min()), "max_G": float(Bbox.max())},
}
print(f"eps_a in AR box: min {res['eps_a_in_box']['min']:.4f}, "
      f"median {res['eps_a_in_box']['median']:.4f}, max {res['eps_a_in_box']['max']:.4f}")
print(f"block threshold eps* = {EPS_STAR:.4f} -> blocked share of box: "
      f"{100*res['blocked_share']:.2f}%")
print(f"Pi_V in box: median {res['pi_v_in_box']['median']:.3f}, max {res['pi_v_in_box']['max']:.3f}")

# 3b. authoritative flare record for the day (Helioviewer GOES/FlareDetective)
import urllib.request, urllib.parse as _up
try:
    _u = "https://api.helioviewer.org/v2/getEvents/?" + _up.urlencode(
        {"startTime": "2014-10-22T00:00:00Z", "endTime": "2014-10-23T00:00:00Z"})
    with urllib.request.urlopen(_u, timeout=60) as _r:
        _ev = json.loads(_r.read().decode())
    _fl = [e for e in _ev if e.get("event_type") == "FL"]
    flare_pos = [{"hpc_x": e.get("hpc_x"), "hpc_y": e.get("hpc_y"),
                  "hgs_x": e.get("hgs_x"), "hgs_y": e.get("hgs_y"),
                  "starttime": e.get("starttime")} for e in _fl]
    res["flare_events"] = flare_pos
    print(f"flare events on record: {len(flare_pos)}")
    for fp in flare_pos:
        print(f"  FL: HPC({fp['hpc_x']}, {fp['hpc_y']}) arcsec, HGS({fp['hgs_x']}, {fp['hgs_y']}) deg, {fp['starttime']}")
except Exception as _e:
    print("event fetch failed:", _e)

# 4. AIA 171 light curves
def series_lightcurve(d, y1s, y2s, x1s, x2s):
    fs = sorted(f for f in os.listdir(d) if f.endswith(".jp2"))
    ts, vals = [], []
    for f in fs:
        arr = read_jp2(os.path.join(d, f))
        ts.append(f.split("_")[-1].replace(".jp2", ""))
        vals.append(float(arr[y1s:y2s, x1s:x2s].mean()))
    return ts, np.array(vals)

# JP2 downscale: Helioviewer scale=1 -> 4096px; box coords map 1:1 for 171
ts_day, lc_day = series_lightcurve(os.path.join(BASE, "aia_12min_day", "aia_171"), y1, y2, x1, x2)
win_dir = os.path.join(BASE, "aia_1min_window", "171")
ts_win, lc_win = series_lightcurve(win_dir, y1, y2, x1, x2)
flare_idx = int(np.argmax(lc_win))
res["day_series"] = {"n": len(ts_day), "first": ts_day[0], "last": ts_day[-1],
                     "lc_min": float(lc_day.min()), "lc_max": float(lc_day.max())}
res["flare_window"] = {"n": len(ts_win),
                       "peak_time": ts_win[flare_idx],
                       "peak_val": float(lc_win[flare_idx]),
                       "quiet_mean": float(np.median(lc_win))}
print(f"day 171 series: {len(ts_day)} frames {ts_day[0]}..{ts_day[-1]}, "
      f"intensity range [{lc_day.min():.0f}, {lc_day.max():.0f}]")
print(f"1-min window: peak at {ts_win[flare_idx]} (value {lc_win[flare_idx]:.0f} vs "
      f"median {np.median(lc_win):.0f}) - the flare rise")

os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "first_look_ar12192.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("\nresult written:", out)
