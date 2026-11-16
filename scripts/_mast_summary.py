import warnings; warnings.filterwarnings("ignore")
from astroquery.mast import Observations
from collections import Counter

def summarize(name, coll):
    try:
        t = Observations.query_object(name, radius="0.05 deg")
        if t is None or len(t) == 0:
            print(name, "-> no results"); return
        f = t[t["obs_collection"] == coll]
        print(name, "|", coll, "| rows:", len(f), "| obs_ids:", len(set(f["obs_id"])))
        print("   instruments:", dict(Counter(f["instrument_name"])))
    except Exception as e:
        print(name, "ERROR:", str(e)[:200])

summarize("Cas A", "JWST")
summarize("SN 1987A", "JWST")
summarize("AT2023fhn", "HST")
