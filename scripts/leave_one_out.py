# leave_one_out.py - the closest entry's autopsy and the leave-one-out (2026-10-17)
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

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

c0 = 2.9979e8; G = 6.674e-11; M_sun = 1.989e30
d_pc = cz / 73.0 * 1e6
K_abs = kt - 5.0*np.log10(np.maximum(d_pc, 1.0)) + 5.0
L_K = 10.0**(-0.4*(K_abs - 3.28))
M = 0.6 * L_K * M_sun
d_m = d_pc * 3.0857e16

c1 = SkyCoord(ra=187.2779*u.deg, dec=2.0524*u.deg, frame="icrs")
c2 = SkyCoord(ra=ra2*u.deg, dec=de2*u.deg, frame="icrs")
sep = c1.separation(c2)
cone = sep < 2.0*u.deg
idx = np.where(cone)[0]
sep_arcmin = sep[cone].to(u.arcmin).value
i_near = idx[np.argmin(sep_arcmin)]

print("THE CLOSEST ENTRY'S AUTOPSY:")
print(f"  index {i_near}, RA {ra2[i_near]:.4f}, Dec {de2[i_near]:.4f}")
print(f"  the raw cz field = {cz[i_near]:.1f} (km/s), distance = {d_pc[i_near]/1e6:.2f} Mpc")
print(f"  K_app = {kt[i_near]:.3f}, K_abs = {K_abs[i_near]:.2f}, L_K = {L_K[i_near]:.2e} L_sun")
print(f"  adopted M = {M[i_near]/M_sun:.2e} M_sun")
sep_rad = sep[i_near].to(u.rad).value
b_phys = sep_rad * d_m[i_near]
print(f"  separation = {sep[i_near].to(u.arcsec).value:.2f} arcsec, physical b = {b_phys/3.0857e16:.1f} pc")
pulls = 4.0*G*M[cone]/(sep[cone].to(u.rad).value * d_m[cone] * c0**2)
pa = c1.position_angle(c2[cone]).to(u.rad).value
print(f"  the single entry's deflection = {pulls[np.argmin(sep_arcmin)]*206264806.7:.2f} arcsec")
print()
print("THE LEAVE-ONE-OUT:")
for omit in [i_near]:
    keep = [j for j in idx if j != omit]
    x = (4.0*G*M[keep]/(sep[keep].to(u.rad).value * d_m[keep] * c0**2) * np.sin(c1.position_angle(c2[keep]).to(u.rad).value)).sum()
    y = (4.0*G*M[keep]/(sep[keep].to(u.rad).value * d_m[keep] * c0**2) * np.cos(c1.position_angle(c2[keep]).to(u.rad).value)).sum()
    print(f"  without the closest: |v| = {np.sqrt(x*x+y*y)*206264806.7:.2f} arcsec")
x_all = (pulls * np.sin(pa)).sum(); y_all = (pulls * np.cos(pa)).sum()
print(f"  the full sum:        |v| = {np.sqrt(x_all*x_all+y_all*y_all)*206264806.7:.2f} arcsec")
print()
print("the honest read: does ONE entry control the whole answer?")
