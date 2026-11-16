# stage3_flux_load.py - flux as load: the demand side on 121 real magnetograms
# The mechanical reading: dE_B/dt (the HMI-visible field reconfiguration) IS
# the flux load; the choke is Pi_V; the backup is zeta; the snap is the
# frozen failure rule. Verdict vs the day's recorded flares.
import os, sys, json
import numpy as np
import imageio.v3 as iio
import urllib.request, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v
from solar.hmi_inputs import eps_a_from_field

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
a_max = F["locked_constants"]["a_max"]["value"]
MP = 1.6726e-27
MU0 = 1.25663706212e-6
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
EPS_STAR = (C_Q / c0) ** 2
APIX = (0.6 * 725e3) ** 2          # m^2 per px (0.6 arcsec/px)
H_SCALE = 1.0e8                    # m coronal extent

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "data", "solar", "raw", "ar12192_20141022"))
mag_dir = os.path.join(BASE, "hmi_720s_day")
mag_files = sorted(f for f in os.listdir(mag_dir) if f.endswith(".jp2"))

def read(p): return np.asarray(iio.imread(p), dtype=float)

def load_B(path):
    raw = read(path)
    B = (raw / 255.0) * 6000.0 - 3000.0
    yy, xx = np.mgrid[0:B.shape[0], 0:B.shape[1]]
    rr = np.hypot(xx - 2048.0, yy - 2048.0)
    disk = (rr < 0.92 * 2048.0) & (raw < 254) & (raw > 1)
    return np.where(disk, B, 0.0)

def wide_boxcar(A, W=61):
    A = np.asarray([np.convolve(r, np.ones(W) / W, mode="same") for r in A])
    return np.asarray([np.convolve(c, np.ones(W) / W, mode="same") for c in A.T]).T

# ---- AR box from frame 0 (wide boxcar on |B|, southern half) ----
B0 = load_B(os.path.join(mag_dir, mag_files[0]))
As = wide_boxcar(np.abs(B0))
south = As[2048:, :]
y0, x0 = np.unravel_index(np.argmax(south), south.shape)
yc, xc = y0 + 2048, x0
BOX = 400
y1, y2 = max(0, yc - BOX), min(4096, yc + BOX)
x1, x2 = max(0, xc - BOX), min(4096, xc + BOX)
print(f"AR box: y[{y1}:{y2}] x[{x1}:{x2}]")

# ---- the day's recorded flares (NOAA SWPC event report; HV fallback) ----
flares = []
try:
    nu = "https://www.swpc.noaa.gov/pub/warehouse/2014/2014_Events/20141022events.txt"
    with urllib.request.urlopen(nu, timeout=60) as r:
        report = r.read().decode("utf-8", "ignore")
    for line in report.splitlines():
        if "Flare" in line and ("M" in line or "X" in line or "C" in line):
            flares.append({"line": line.strip()[:160]})
    if not flares:
        for line in report.splitlines():
            if "XRA" in line:
                flares.append({"line": line.strip()[:160]})
except Exception as e:
    print("NOAA report fetch failed:", e)
if not flares:
    u = "https://api.helioviewer.org/v2/getEvents/?" + urllib.parse.urlencode(
        {"startTime": "2014-10-22T00:00:00Z", "endTime": "2014-10-23T00:00:00Z"})
    with urllib.request.urlopen(u, timeout=60) as r:
        events = json.loads(r.read().decode())
    for e in events:
        if e.get("event_type") == "FL" or e.get("goes_class"):
            flares.append({"line": f"{e.get('starttime')} class={e.get('goes_class')} "
                                   f"HPC=({e.get('hpc_x')}, {e.get('hpc_y')})"})
print(f"flare records: {len(flares)}")
for fl in flares:
    print(f"  {fl['line']}")

# ---- the load series over the day ----
times = []
E_B = []
eps_bar = []
blocked_share = []
pi_max = []
S_strain = []
V_A = (y2 - y1) * (x2 - x1) * APIX * H_SCALE
L_CH = V_A ** (1.0 / 3.0)
ZETA_YIELD = a_max * L_CH / C_Q ** 2
print(f"V_a = {V_A:.2e} m^3, L_ch = {L_CH:.2e} m, zeta_yield = {ZETA_YIELD:.2e}")

for f in mag_files:
    B = load_B(os.path.join(mag_dir, f))
    Bbox = B[y1:y2, x1:x2]
    tstr = f.replace("hmi_mag_", "").replace(".jp2", "").replace("Z", "")
    times.append(tstr)
    E_B.append(float(np.sum(Bbox ** 2) / (2 * MU0) * APIX))
    XX, YY = np.meshgrid(np.arange(Bbox.shape[1]), np.arange(Bbox.shape[0]))
    eps = eps_a_from_field(Bbox, XX.astype(float), YY.astype(float))
    pi_map = pi_v.pi_v_map(np.full_like(eps, RHO_Q), eps, c0, rho0, n_lad)
    blk = pi_map > 1.0
    eps_bar.append(float(eps.mean()))
    blocked_share.append(float(blk.mean()))
    pi_max.append(float(pi_map.max()))
    if blk.any():
        S_strain.append(float(blk.mean() * np.mean((pi_map[blk] - 1.0) / pi_map[blk])))
    else:
        S_strain.append(0.0)

times = np.array(times)
E_B = np.array(E_B)
eps_bar = np.array(eps_bar)
blocked_share = np.array(blocked_share)
pi_max = np.array(pi_max)
S_strain = np.array(S_strain)
t_sec = np.arange(len(times)) * 720.0
dEdt = np.gradient(E_B, t_sec)
load_untie = np.maximum(0.0, -dEdt)          # the untying flux load (W)
zeta_dot = mdot_deep * (1.0 - eps_bar) * S_strain / (RHO_Q * V_A)
zeta = np.cumsum(zeta_dot * 720.0)

print()
print("flux-as-load series (121 magnetograms):")
print(f"  E_B: {E_B.min():.2e} -> {E_B.max():.2e} J  (day change {E_B[-1]-E_B[0]:.2e} J)")
print(f"  load max(dE_B/dt): {np.abs(dEdt).max():.2e} W")
print(f"  eps_bar: {eps_bar.min():.3f}..{eps_bar.max():.3f} | blocked share: "
      f"{blocked_share.min():.3f}..{blocked_share.max():.3f} | Pi_V max: "
      f"{pi_max.min():.2f}..{pi_max.max():.2f}")
print(f"  zeta end-of-day: {zeta[-1]:.3e}  vs zeta_yield {ZETA_YIELD:.2e}  -> "
      f"{'ERUPTION' if zeta[-1] >= ZETA_YIELD else 'no snap (frozen rule)'}")

# where do the load spikes land?
order = np.argsort(load_untie)[::-1][:6]
print("  top load spikes:")
for k in order:
    print(f"    {times[k]}  {load_untie[k]:.2e} W  (blocked share {blocked_share[k]:.3f}, Pi_V max {pi_max[k]:.2f})")

res = {"ar_box": [int(y1), int(y2), int(x1), int(x2)],
       "V_a": V_A, "L_ch": L_CH, "zeta_yield": ZETA_YIELD,
       "flares": flares,
       "E_B_J": E_B.tolist(), "load_untie_W": load_untie.tolist(),
       "eps_bar": eps_bar.tolist(), "blocked_share": blocked_share.tolist(),
       "pi_max": pi_max.tolist(), "zeta": zeta.tolist(),
       "times": times.tolist(),
       "note": "display-scaled 8-bit JP2 magnetograms: E_B/load are proxies, "
               "monotone in the true values; quantitative EM needs JSOC FITS"}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "flux_load_ar12192.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print("\nresult written:", out)
