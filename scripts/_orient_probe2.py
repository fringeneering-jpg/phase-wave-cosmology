import os, sys, numpy as np, imageio.v3 as iio
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.normpath(os.path.join(os.getcwd(), "..", "data", "solar", "raw", "ar12192_20141022"))
print("BASE:", BASE, flush=True)
def read(p): return np.asarray(iio.imread(p), dtype=float)
d171 = os.path.join(BASE, "aia_12min_day", "aia_171")
fs = sorted(os.listdir(d171))
print("files:", len(fs), flush=True)
arr = read(os.path.join(d171, fs[60]))
print("loaded", arr.shape, flush=True)
yy, xx = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
rr = np.hypot(xx-2048, yy-2048)
m = (rr < 0.9*2048) & (arr < 254)
A = np.where(m, arr, 0)
W = 61
As = np.asarray([np.convolve(r, np.ones(W)/W, mode="same") for r in A])
As = np.asarray([np.convolve(c, np.ones(W)/W, mode="same") for c in As.T]).T
south = As[2048:, :]
y0, x0 = np.unravel_index(np.argmax(south), south.shape)
print("171 brightest southern blob: x =", x0, "y =", y0+2048, flush=True)
print("helio approx: X =", round((x0-2048)*0.6), "arcsec, Y =", round((2048-y0)*0.6), "arcsec", flush=True)
