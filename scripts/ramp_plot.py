"""Render the radial profile PNGs with Pillow (no matplotlib in the bundled env)."""
import numpy as np
from PIL import Image, ImageDraw

data = np.genfromtxt("ramp_out_profile.csv", delimiter=",", skip_header=1)
r, rho, P, cs, S, acc = data.T

c0   = 2.99792458e8
G    = 6.6743e-11
Msun = 1.989e30
M    = 62.0*Msun
rhomax = 1.304e15
rhog   = rhomax/2.0
Rg     = G*M/c0**2          # GM/c0^2 in m
Rc     = 47.22e3
Redge  = 159.63e3
r_in, r_out = 2*Rg, 6*Rg
r_fold = 192.7e3
r_reach = np.sqrt(G*M/(6.61e-11))

W, H = 1400, 780
MARG = dict(l=95, r=25, t=45, b=70)

def panel(logx_min, logx_max, logy_min, logy_max):
    def X(lx): return MARG['l'] + (lx - logx_min)/(logx_max - logx_min)*(W - MARG['l'] - MARG['r'])
    def Y(ly): return H - MARG['b'] - (ly - logy_min)/(logy_max - logy_min)*(H - MARG['t'] - MARG['b'])
    return X, Y

img = Image.new("RGB", (W, H), (255, 255, 255))
dr = ImageDraw.Draw(img)

# ---------------- panel 1: rho(r) ----------------
lx0, lx1, ly0, ly1 = np.log10(Rc*0.95), np.log10(r_reach*1.05), np.log10(1e-28), np.log10(rhomax*2)
X, Y = panel(lx0, lx1, ly0, ly1)
dr.text((MARG['l'], 12), "PWC held-medium radial profile (M = 62 Msun, m-family ramp m=1) -- rho(r)", fill=(0,0,0))
# grid
for lx in range(int(np.ceil(lx0)), int(lx1)+1):
    dr.line([X(lx), MARG['t'], X(lx), H-MARG['b']], fill=(235,235,235))
    dr.text((X(lx)+2, H-MARG['b']+8), f"1e{lx} m", fill=(120,120,120))
for ly in range(-28, 17, 4):
    dr.line([MARG['l'], Y(ly), W-MARG['r'], Y(ly)], fill=(235,235,235))
    dr.text((10, Y(ly)-6), f"1e{ly}", fill=(120,120,120))
dr.text((MARG['l'], H-MARG['b']+30), "radius r [m] (log)", fill=(0,0,0))
dr.text((14, MARG['t']+8), "rho [kg/m^3] (log)", fill=(0,0,0))
# curve
pts = [(X(np.log10(rr)), Y(np.log10(pp))) for rr, pp in zip(r, rho) if rr >= Rc]
dr.line(pts, fill=(20, 60, 200), width=3)
# shell plateau
y_rmax = Y(np.log10(rhomax))
dr.line([X(np.log10(Rc)), y_rmax, X(np.log10(Redge)), y_rmax], fill=(200, 40, 40), width=3)
# markers
for rx, lab, col in [(Redge, "shell edge\n159.6 km", (200,40,40)),
                     (r_in, "2GM/c0^2", (0,0,0)),
                     (r_out, "6GM/c0^2 = ISCO", (0,0,0)),
                     (r_fold, "fold rho_max/2\n192.7 km", (150,60,160)),
                     (r_reach, "reach 0.36 pc\nrho=rho0", (0,120,0))]:
    dr.line([X(np.log10(rx)), MARG['t'], X(np.log10(rx)), H-MARG['b']], fill=col, width=1)
    dr.text((X(np.log10(rx))+3, MARG['t']+20), lab, fill=col)

# ---------------- panel 2: S(r), c_s(r)/c0 ----------------
img2 = Image.new("RGB", (W, H), (255, 255, 255))
dr2 = ImageDraw.Draw(img2)
lx0, lx1 = np.log10(1e5), np.log10(2e13)      # 100 km .. 2e13 m focus on decompression
X2 = lambda lx: MARG['l'] + (lx - lx0)/(lx1 - lx0)*(W - MARG['l'] - MARG['r'])
Y2 = lambda v: H - MARG['b'] - v*(H - MARG['t'] - MARG['b'])
dr2.text((MARG['l'], 12), "order parameter S(r) and sound speed c_s(r)/c0 through the decompression", fill=(0,0,0))
for lx in range(int(np.ceil(lx0)), int(lx1)+1):
    dr2.line([X2(lx), MARG['t'], X2(lx), H-MARG['b']], fill=(235,235,235))
    dr2.text((X2(lx)+2, H-MARG['b']+8), f"1e{lx}", fill=(120,120,120))
for v in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    dr2.line([MARG['l'], Y2(v), W-MARG['r'], Y2(v)], fill=(235,235,235))
    dr2.text((10, Y2(v)-6), f"{v:.1f}", fill=(120,120,120))
dr2.text((MARG['l'], H-MARG['b']+30), "radius r [m] (log)", fill=(0,0,0))
m = r >= 1e5
ptsS = [(X2(np.log10(rr)), Y2(min(ss, 1.0))) for rr, ss in zip(r[m], S[m])]
ptsc = [(X2(np.log10(rr)), Y2(cc/c0)) for rr, cc in zip(r[m], cs[m])]
dr2.line(ptsS, fill=(20, 60, 200), width=3)
dr2.line(ptsc, fill=(200, 40, 40), width=3)
for rx, lab, col in [(Redge, "shell edge", (200,40,40)), (r_in, "2GM/c0^2", (0,0,0)),
                     (r_out, "6GM/c0^2", (0,0,0)), (r_fold, "fold", (150,60,160)),
                     (r_reach, "reach", (0,120,0))]:
    dr2.line([X2(np.log10(rx)), MARG['t'], X2(np.log10(rx)), H-MARG['b']], fill=col, width=1)
    dr2.text((X2(np.log10(rx))+3, MARG['t']+15), lab, fill=col)
dr2.text((MARG['l']+15, H-MARG['b']-30), "blue = S(r)", fill=(20,60,200))
dr2.text((MARG['l']+15, H-MARG['b']-50), "red  = c_s(r)/c0", fill=(200,40,40))

img.save("ramp_profile_rho.png")
img2.save("ramp_profile_S_cs.png")
print("saved ramp_profile_rho.png and ramp_profile_S_cs.png")
