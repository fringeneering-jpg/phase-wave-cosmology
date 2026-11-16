import warnings; warnings.filterwarnings("ignore")
from astroquery.mast import Observations

def query(name, filters=None):
    print("=" * 70)
    print("MAST QUERY:", name)
    try:
        t = Observations.query_object(name, radius="0.05 deg")
        if t is None or len(t) == 0:
            print("  no results"); return
        print("  total rows:", len(t))
        cols = [c for c in ("obs_id","obs_collection","instrument_name","filters","wavelength_region","dataproduct_type","target_name","s_ra","s_dec","obsid") if c in t.colnames]
        if filters:
            mask = None
            for col, vals in filters.items():
                m = (t[col] == vals[0])
                for v in vals[1:]:
                    m |= (t[col] == v)
                mask = m if mask is None else (mask & m)
            t = t[mask]
            print("  filtered rows:", len(t))
        for row in t:
            line = "  " + str(row["obs_id"]) + " | " + str(row["obs_collection"])
            if "instrument_name" in t.colnames: line += " | " + str(row["instrument_name"])
            if "filters" in t.colnames: line += " | " + str(row["filters"])
            if "wavelength_region" in t.colnames: line += " | " + str(row["wavelength_region"])
            print(line[:150])
    except Exception as e:
        print("  ERROR:", str(e)[:300])

query("Cas A", {"obs_collection": ["JWST"]})
query("SN 1987A", {"obs_collection": ["JWST"]})
query("AT2023fhn", {"obs_collection": ["HST"]})
