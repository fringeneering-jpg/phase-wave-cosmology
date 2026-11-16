import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import vso

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "solar", "raw", "smoke_test")
print("querying VSO: AIA 171, 2014-10-20T00:00-01:00, 30 min cadence ...")
try:
    q = vso.query_aia("2014-10-20T00:00:00", "2014-10-20T01:00:00", 171, sample_min=30)
    print(q)
    n = sum(len(t) for t in q) if q else 0
    print("records found:", n)
    if n:
        paths = vso.download(q, out)
        print("downloaded:", len(paths))
        for p in paths[:4]:
            print("  ", os.path.basename(p), os.path.getsize(p), "bytes; sidecar:", os.path.exists(p + ".sha256"))
        # verify the FITS opens
        from astropy.io import fits
        for p in paths[:1]:
            with fits.open(p) as hdul:
                print("FITS ok:", hdul[0].header.get("T_OBS"), hdul[0].header.get("WAVELNTH"))
except Exception as e:
    print("SMOKE FAILED:", type(e).__name__, str(e)[:500])
