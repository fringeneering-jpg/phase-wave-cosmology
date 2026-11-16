# movers_census.py - the movers' seed (2026-10-17)
# The zeros don't get hot - the movers are the sample. The known candidates
# with the measured/estimated velocities; the honest labels for the proxies.
import csv
import numpy as np

G = 6.674e-11
a0 = 6.611e-11
pc = 3.0857e16

# (name, type, M_sun, v_km_s, T_K, the source/label)
movers = [
    ("RBH-1",            "SMBH", 3.00e7,  954.0,  1.0e7, "the measured runaway"),
    ("3C 186",           "SMBH", 1.00e9, 2140.0,  None,  "the recoiling quasar's offset"),
    ("CXO J101527+625911","SMBH", 4.00e7,  100.0,  None,  "the offset candidate"),
    ("SDSS J0927+2943",  "SMBH", 6.00e8, 2650.0,  None,  "the broad-line offset (the proxy)"),
    ("Eracleous-88 max", "SMBH", 1.00e9, 5000.0,  None,  "the 88-quasar sample's upper offset (the proxy)"),
    ("MaNGA-14 max",     "SMBH", 1.00e8,  600.0,  None,  "the off-nuclear AGN's upper (the proxy)"),
]

out = r"C:\Users\jaden\Downloads\PWC-Check\scratch\bh\movers_census.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "type", "M_sun", "v_km_s", "T_K", "label", "r_t_pc"])
    for name, typ, M, v, T, label in movers:
        rt = np.sqrt(G * M * 1.989e30 / a0) / pc
        w.writerow([name, typ, M, v, T if T else "", label, f"{rt:.1f}"])

print("THE MOVERS' SEED:")
print(f"  {'name':18s} {'v km/s':>8s} {'M_sun':>10s} {'T_K':>9s}  label")
for name, typ, M, v, T, label in movers:
    print(f"  {name:18s} {v:8.0f} {M:10.1e} {str(T):>9s}  {label}")
print()
print(f"saved: {out}")
print("the honest read: 6 movers (the 954 measured; the others the offsets'")
print("proxies - the broad-line shifts, not the confirmed travel speeds). The")
print("Eracleous 2012ApJS 88-quasar sample and the MaNGA 14 are the real")
print("catalogs to pull for the thousands-grade mover census. The proxies are")
print("labelled, not dressed.")
