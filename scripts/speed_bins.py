# speed_bins.py - the 100 km/s speed bins and the trail temps (2026-10-17)
import csv
import numpy as np

rows = []
with open(r"C:\Users\jaden\Downloads\PWC-Check\scratch\bh\bh_census.csv") as f:
    for r in csv.DictReader(f):
        try:
            v = float(r["v_km_s"]) if r["v_km_s"] else None
            T = float(r["T_K"]) if r["T_K"] else None
            M = float(r["M_sun"]) if r["M_sun"] else None
            rows.append((r["name"], M, v, T, int(r["eating"]) if r["eating"] else 0))
        except ValueError:
            continue

have_v = [r for r in rows if r[2] is not None]
have_vT = [r for r in have_v if r[3] is not None]
print(f"the census: {len(rows)} rows; with velocities: {len(have_v)}; with v AND T: {len(have_vT)}")
print()
print("the 100 km/s speed bins (the ones with the T's):")
bins = {}
for name, M, v, T, eat in have_vT:
    b = int(v // 100) * 100
    bins.setdefault(b, []).append((name, M, v, T, eat))
for b in sorted(bins):
    group = bins[b]
    Ts = [g[3] for g in group]
    print(f"  {b:5d}-{b+100:5d} km/s (n={len(group):2d}):  T's = {[f'{t:.1e}' for t in Ts]}")
print()
print("the honest read: the census's velocities are the RARE column - the bins")
print("populate only where the measured speeds exist (the residents' 0-bin and")
print("the RBH-1's 954-bin). The commonality needs the velocity census - the")
print("kicks' and offsets' - before the trails can show. The framework's own")
print("prediction stands ready: T ~ (v/C)^2's the square within each size class.")
