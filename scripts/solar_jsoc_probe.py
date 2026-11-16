import sys, os, json
sys.path.insert(0, os.path.join(os.getcwd(), "solar"))
from solar import jsoc
q = jsoc.build_query("aia.lev1_euv_12s", "2017-09-06T12:00:00", ["image"], None)
try:
    jsoc.fetch_metadata(q + "[171][?QUALITY>=0 ?]")
    print("JSOC REACHABLE")
except Exception as e:
    print("JSOC PROBE FAILED:", type(e).__name__, str(e)[:300])
