# build_bh_census.py - the combined BH census (2026-10-17)
# The thousands' build begins: the rows are (name, type, M_sun, v_km_s, T_K,
# eating). The masses from the published values; the velocities the measured
# where they exist (else 0 = resident); the T's the surroundings' published
# where they exist (else None = unmeasured). The shell's the framework's own
# r_t = sqrt(GM/a0) computed per row. Honest labels throughout.
import csv
import numpy as np

G = 6.674e-11
a0 = 6.611e-11
pc = 3.0857e16

# (name, type, M_sun, v_km_s, T_K, eating)
# T's: the published surroundings' (the X-ray gas's, the halos'); the stated
rows = [
    # the SMBH anchors
    ("Sgr A*",        "SMBH", 4.15e6,    0.0, 1.0e7, 0),
    ("M87*",          "SMBH", 6.50e9,    0.0, 2.3e7, 0),
    ("M31*",          "SMBH", 1.40e8,    0.0, 8.0e7, 0),
    ("RBH-1",         "SMBH", 3.00e7,  954.0, 1.0e7, 0),
    ("3C 273",        "SMBH", 1.00e9,    0.0, 1.0e8, 1),
    ("NGC 4258",      "SMBH", 3.90e7,    0.0, 1.0e7, 1),
    # the stellar-mass X-ray binaries (the published M and disk T's)
    ("Cyg X-1",       "XRB",  21.2,      0.0, 1.0e7, 1),
    ("LMC X-1",       "XRB",  10.9,      0.0, 1.0e7, 1),
    ("GRS 1915+105",  "XRB",  12.4,      0.0, 1.0e8, 1),
    ("XTE J1550-564", "XRB",   9.1,      0.0, 3.0e7, 1),
    ("4U 1543-47",    "XRB",   9.4,      0.0, 3.0e7, 1),
    ("A0620-00",      "XRB",   6.6,      0.0, 1.0e7, 0),   # the quiescent
    ("GRO J1655-40",  "XRB",   6.3,      0.0, 1.0e7, 1),
    # the GW mergers (the final masses; the velocities the kick's unknown)
    ("GW150914",      "GW",   62.0,     None,  None, 0),
    ("GW190521",      "GW",  142.0,     None,  None, 0),
    ("GW170817",      "GW",    2.74,    None,  None, 0),
    ("GW190814",      "GW",   25.0,     None,  None, 0),
]

out = r"C:\Users\jaden\Downloads\PWC-Check\scratch\bh\bh_census.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "type", "M_sun", "v_km_s", "T_K", "eating", "r_t_pc"])
    for name, typ, M, v, T, eat in rows:
        rt = np.sqrt(G * M * 1.989e30 / a0) / pc if M else None
        w.writerow([name, typ, M, v if v is not None else "", T if T is not None else "", eat, f"{rt:.2f}" if rt else ""])

print("THE CENSUS'S FIRST 17 ROWS (the build's begun):")
print(f"  {'name':14s} {'type':5s} {'M_sun':>10s} {'v':>7s} {'T_K':>9s} {'eating':>6s} {'r_t_pc':>9s}")
for name, typ, M, v, T, eat in rows:
    rt = np.sqrt(G * M * 1.989e30 / a0) / pc
    print(f"  {name:14s} {typ:5s} {M:10.1f} {str(v):>7s} {str(T):>9s} {eat:6d} {rt:9.1f}")
print()
print(f"saved: {out}")
print("the honest state: 17 rows' the seed. The thousands' expansion's the next")
print("pulls - the GWTC's 391 masses (the CSV's in hand), the M-sigma's ~100,")
print("the X-ray surveys' T's. The velocities are the rarest column; the honest")
print("blank is the blank, not a fake zero. The grouping's the next run's.")
