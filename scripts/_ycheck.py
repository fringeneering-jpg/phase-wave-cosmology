import astropy
from astropy.io import fits
import numpy as np
print("astropy", astropy.__version__)
h = fits.open(r"D:\planck_milca_y_2048.fits")
h.info()
for i in range(1, len(h)):
    d = h[i].data
    if d is not None:
        print("EXT", i, "dtype", d.dtype, "shape", getattr(d, "shape", None))
        try:
            print("  cols:", d.names)
        except Exception:
            pass
        hdr = h[i].header
        for k in ("ORDERING","NSIDE","COORDSYS","FIRSTPIX","LASTPIX","TUNIT1"):
            if k in hdr:
                print("  ", k, "=", hdr[k])
h.close()
