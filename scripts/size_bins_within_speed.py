# size_bins_within_speed.py - the 5 MaxP size bins within each speed (2026-10-17)
import csv
import numpy as np

G = 6.674e-11
a0 = 6.611e-11
pc = 3.0857e16

rows = []
with open(r"C:\Users\jaden\Downloads\PWC-Check\scratch\bh\bh_census.csv") as f:
    for r in csv.DictReader(f):
        try:
            v = float(r["v_km_s"]) if r["v_km_s"] else None
            T = float(r["T_K"]) if r["T_K"] else None
            M = float(r["M_sun"]) if r["M_sun"] else None
            if M and M > 0:
                rt = np.sqrt(G * M * 1.989e30 / a0) / pc
            else:
                rt = None
            rows.append((r["name"], M, v, T, rt, int(r["eating"]) if r["eating"] else 0))
        except ValueError:
            continue

have = [r for r in rows if r[2] is not None and r[3] is not None and r[4] is not None]
# the 5 MaxP size bins (log-spaced over the census's range)
rt_vals = np.array([r[4] for r in have])
edges = np.logspace(np.log10(0.05), np.log10(5000.0), 6)
labels = ["0.05-0.3 pc", "0.3-1.5 pc", "1.5-8 pc", "8-45 pc", "45-5000 pc"]

# the speed groups
speeds = sorted(set(int(r[2] // 100) * 100 for r in have))
print("THE 5 MAXP SIZE BINS WITHIN EACH SPEED:")
for s in speeds:
    group = [r for r in have if int(r[2] // 100) * 100 == s]
    print(f"  speed {s:5d} km/s (n={len(group)}):")
    for i in range(5):
        inbin = [r for r in group if edges[i] <= r[4] < edges[i+1]]
        if inbin:
            Ts = [r[3] for r in inbin]
            eats = sum(r[5] for r in inbin)
            print(f"      {labels[i]:12s} (n={len(inbin):2d}, eating={eats}):  T's = {[f'{t:.1e}' for t in Ts]}")
        else:
            print(f"      {labels[i]:12s} (n= 0)")
print()
print("the honest read: the commonality the question hunts is the SAME T's")
print("within the same speed AND the same MaxP size, with the eating split")
print("out. The sparse v's leave the bins thin - the full trails need the")
print("velocity census - but the structure's the right sort now.")
