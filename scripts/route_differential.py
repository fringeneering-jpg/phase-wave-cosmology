# route_differential.py - the single differential with the predictive outcome (2026-10-17)
# The route's equation: the light's path bends where the medium's speed
# capacity's gradient is transverse to the path - the single differential
#     dtheta/ds = (1/C) . grad_perp(C)
# (the refractive route: the bends are the pulls' gradient, nothing else).
# The predictive outcome: the integrated deflection along a source's line of
# sight, from the HI4PI's density + the 2MRS bodies - checked against the
# observed position's offset. Expanded sample: the known bright sources.
import healpy as hp
import numpy as np

m = hp.read_map("/mnt/c/Users/jaden/Downloads/PWC-Check/scratch/telescope/HI4PI_NHI_HPX.fits.gz", nest=True)
m = hp.reorder(m, n2r=True)
nside = hp.get_nside(m)

# the route's speed capacity: C(rho) ~ sqrt(2 Y / rho); the H1's the density's
# tracer, so the local capacity's C ~ N_HI^(-1/2) (the refractive index n = c0/C
# ~ N_HI^(+1/2)). The bending's the transverse gradient of the index.
def predict_deflection(ra, dec, ap=2.0):
    """the predicted deflection toward a source: the transverse index gradient
    integrated over the route's near leg (the annulus around the line of sight)."""
    pix = hp.ang2pix(nside, ra, dec, lonlat=True)
    vv0 = np.array(hp.pix2vec(nside, pix))
    idx = hp.query_disc(nside, vv0, np.radians(ap))
    nhi = m[idx]
    # the index's transverse gradient's proxy: the annulus's index's asymmetry
    # (the weighted centroid's offset = the route's bend's direction and scale)
    vv = np.array(hp.pix2vec(nside, idx)).T
    n_i = np.sqrt(np.maximum(nhi, 1e-6))
    w = n_i - n_i.mean()
    if np.abs(w).sum() < 1e-12:
        return 0.0, 0.0
    cx = (w * vv[:, 0]).sum() / np.abs(w).sum()
    cy = (w * vv[:, 1]).sum() / np.abs(w).sum()
    cz = (w * vv[:, 2]).sum() / np.abs(w).sum()
    # the deflection's the centroid's transverse magnitude (the unitless scale)
    transverse = np.sqrt(max(0.0, 1.0 - (cx*vv0[0]+cy*vv0[1]+cz*vv0[2])**2))
    return transverse, float(np.mean(nhi))

print("THE ROUTE'S SINGLE DIFFERENTIAL:  dtheta/ds = (1/C) . grad_perp(C)")
print("the predictive outcome: the integrated transverse gradient toward each")
print("source - the bends should SCALE with the nearby medium's asymmetry.")
print()
print("the expanded sample (the known bright sources with the precise positions):")
sample = [
    ("3C 273", 187.2779, 2.0524, 0.158),
    ("3C 279", 194.0465, -5.7893, 0.536),
    ("PKS 2155-304", 329.7169, -30.2256, 0.116),
    ("Centaurus A", 201.3651, -43.0191, 0.00183),
    ("M87", 187.7059, 12.3911, 0.00428),
]
print(f"  {'source':12s} {'N_HI (1e20)':>12s} {'transverse':>12s} {'redshift':>8s}")
for name, ra, dec, z in sample:
    t, nhi = predict_deflection(ra, dec)
    print(f"  {name:12s} {nhi/1e20:12.1f} {t:12.5f} {z:8.3f}")
print()
print("the predictive outcome: the observed position's offsets should CORRELATE")
print("with the transverse gradient (the route's bends) - the denser and more")
print("asymmetric the near route, the larger the observed's deviation from the")
print("straight-line position. The check: the known offsets vs this prediction.")
