# distance_factored.py - the same-seat rescale (2026-10-17)
# T(x) = T_surf . (R_shell/x)^(1/2) -> T_surf = T_measured . (x/R_shell)^(1/2)
# The measurement distances (the STATED assumptions): the XRB disks' the
# ISCO's (~6 GM/c^2); the SMBH halos' the ~50-100 pc (the resolved's).
import csv
import numpy as np

G = 6.674e-11
a0 = 6.611e-11
c0 = 2.9979e8
pc = 3.0857e16

rows = []
with open(r"C:\Users\jaden\Downloads\PWC-Check\scratch\bh\bh_census.csv") as f:
    for r in csv.DictReader(f):
        try:
            v = float(r["v_km_s"]) if r["v_km_s"] else None
            T = float(r["T_K"]) if r["T_K"] else None
            M = float(r["M_sun"]) if r["M_sun"] else None
            typ = r["type"]
            rows.append((r["name"], typ, M, v, T, int(r["eating"]) if r["eating"] else 0))
        except ValueError:
            continue

def x_measure(typ, M):
    # the stated measurement distance: the XRB's the ISCO; the SMBH's the 50 pc
    if typ == "XRB":
        return 6.0 * G * M * 1.989e30 / c0**2
    return 50.0 * pc

print("THE SAME-SEAT RESCALE (the distance's factored in):")
print(f"  {'name':14s} {'T_measured':>11s} {'x (m)':>10s} {'R_shell':>10s} {'T_surf':>11s}")
for name, typ, M, v, T, eat in rows:
    if M is None or T is None:
        continue
    rt = np.sqrt(G * M * 1.989e30 / a0)
    x = x_measure(typ, M)
    T_surf = T * (x / rt) ** 0.5
    print(f"  {name:14s} {T:11.1e} {x:10.2e} {rt:10.2e} {T_surf:11.2e}")
print()
print("the honest read: the T_surf is the SURFACE temperature (at R_shell), the")
print("common seat. The bins must now use the T_surf - the same-seat comparison.")
print("the STATED flags: the XRB x = ISCO, the SMBH x = 50 pc are the stated")
print("assumptions, not measured per-object; the next pull's the real per-object")
print("measurement radii.")
