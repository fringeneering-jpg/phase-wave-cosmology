# galaxy_weather_report.py - the WEATHER of galaxies from the heat events
# (2026-10-21, Jaden's ruling: heat events either way show what is happening).
# The weather state of a galaxy = its choke factor x = g_bar/(18 a0) and the
# shared tension: SETTLED (the controlled burn) / STALLING (x approaching 1)
# / RUNAWAY (the choke's relief opening). Read straight off the rotation
# catalogs on disk - the same data the -2 fits score.
import numpy as np
import pandas as pd

c0 = 2.99792458e8
rho0 = 8.74e-27
Rp = 8.414e-16
s = 1.0 / 19.0
f_solid = 8.4989e-4
G_chain = (f_solid ** 12) * (4.0 * s / 81.0) * (Rp ** 2) * (c0 ** 3) / 1.054571817e-34
a0_bare = (c0 / np.sqrt(3.0)) * np.sqrt(G_chain * rho0 / 4.0)

paths = {
    "PROBES": r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\probes\probes_accel.csv",
    "GHASP": r"C:\Users\jaden\cosmology\sparc\ghasp\ghasp_accel.csv",
    "ALFALFA": r"C:\Users\jaden\cosmology\sparc\alfalfa_gas_accel.csv",
}

def weather(df):
    gb = df["g_bar"].values.astype(float)
    x = gb / (18.0 * a0_bare)
    xm = float(np.median(x))
    sh = df["shared"].values.astype(float) if "shared" in df.columns else np.zeros_like(gb)
    sm = float(np.median(sh))
    if xm >= 1.0:
        state = "RUNAWAY (the choke is open)"
    elif xm >= 0.5:
        state = "STALLING (the burn is gated)"
    else:
        state = "SETTLED (the controlled burn)"
    return xm, sm, state

print("=" * 74)
print("THE GALAXY WEATHER REPORT (the choke factor x = g_bar / 18 a0)")
print("=" * 74)
tot = 0
counts = {}
stalling_names = []
for name, p in paths.items():
    try:
        df = pd.read_csv(p)
    except Exception as e:
        print(name, "skip:", str(e)[:80]); continue
    df["Name"] = df["Name"].astype(str)
    print()
    print("--- %s (%d galaxies) ---" % (name, df["Name"].nunique()))
    for n, g in df.groupby("Name"):
        xm, sm, state = weather(g)
        key = state.split(" (")[0]
        counts[key] = counts.get(key, 0) + 1
        tot += 1
        if key == "STALLING":
            stalling_names.append("%s (%.4f)" % (n, xm))
    # the catalog's weather distribution
print()
print("THE STALLING TAIL (the galaxies whose weather is the interesting one):")
for n in stalling_names:
    print("  ", n)
print()
print("=" * 74)
print("ALL-CATALOG WEATHER (%d galaxies scored)" % tot)
print("=" * 74)
for k in ("SETTLED", "STALLING", "RUNAWAY"):
    c = counts.get(k, 0)
    print("  %-10s : %5d galaxies  (%.1f%%)" % (k, c, 100.0 * c / max(tot, 1)))
print()
print("READ: most galaxies live in the SETTLED regime (x << 1, the controlled")
print("burn); the STALLING tail is where the bulge's load approaches the gate;")
print("a RUNAWAY galaxy is one whose median acceleration sits past the choke -")
print("the weather states the heat events read out, catalog by catalog.")
