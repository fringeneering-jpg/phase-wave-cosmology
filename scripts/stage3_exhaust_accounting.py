# stage3_exhaust_accounting.py - the 10-Gyr exhaust: where the mass went (2026-10-18)
# The standard's accounting error: the stars' untied mass is DELETED (the
# radiation is treated as massless). The framework: the mass RELOCATES -
# the untied knots become EM waves that still hold the weight. The photons
# left at c0 (Channel 1); the phonons (Channel 2, the heavy heat waves)
# stuck around. The bulge's accumulated exhaust = the field's density
# loading. The honest accounting + the gravity check.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]

M_SUN = 1.989e30
G = 6.67430e-11
GYR = 3.156e16

print("=" * 78)
print("THE 10-GYR EXHAUST - the accounting the standard forgot")
print("=" * 78)
print(f"the per-kg untying rate (the Sun's own): mdot/M = "
      f"{mdot_deep/M_SUN:.2e} /s")
print(f"over 10 Gyr each kg loses {mdot_deep/M_SUN*10*GYR*100:.2f}% of itself")
print()
print("the bulge's ledger (2e10 M_sun of old stars, the CURRENT rate):")
M_bulge = 2.0e10 * M_SUN
mdot_bulge = mdot_deep * 2.0e10
M_exh = mdot_bulge * 10 * GYR
print(f"  the current untying rate: {mdot_bulge:.2e} kg/s")
print(f"  the 10-Gyr exhaust: {M_exh:.2e} kg = {M_exh/M_bulge*100:.2f}% of the")
print(f"  bulge's stellar mass (the standard DELETES this; it is not zero)")
print()
print("where it went (the two channels):")
M_ph = 0.476 * M_exh
M_pn = 0.524 * M_exh
print(f"  Channel 1 (photons, left at c0): {M_ph:.2e} kg - gone from the bulge")
print(f"  Channel 2 (phonons, the heavy heat waves, still there): {M_pn:.2e} kg")
V_bulge_1kpc = 4/3*3.14159265358979*(3.1e19)**3
V_gal = 4/3*3.14159265358979*(5.0e20)**3
for V, lbl in ((V_bulge_1kpc, "the bulge's own volume (1 kpc)"),
               (V_gal, "the whole galaxy (16 kpc)")):
    rho_exh = M_pn / V
    print(f"  spread over {lbl:38s}: rho_exh = {rho_exh:.2e} kg/m^3 "
          f"= {rho_exh/rho0:.1f}x rho0")
print()
print("the gravity check (the exhaust's own pull, honestly):")
g_exh = G * M_pn / (3.1e19) ** 2
print(f"  at the bulge's edge: g = G M_exh/r^2 = {g_exh:.2e} m/s^2")
print(f"  vs the rotation's need (~a0 ~ 1e-10): {1e-10/g_exh:.0f}x TOO SMALL")
print(f"  -> the exhaust is NOT dark matter as GRAVITY (it is 0.5% of the")
print(f"  stellar mass, spread thin). Its real role: the FIELD'S DENSITY")
print(f"  LOADING - the ambient's elevation drives the impedance stiffening")
print(f"  (the bulge's 1.40x Upsilon), not the Newtonian pull.")
print()
print("the reconciliation (the named item):")
print(f"  the M/L derivation needed x = 0.371 (+24% dimensionless loading); the")
print(f"  exhaust accounting gives ~{M_pn/V_bulge_1kpc/rho0:.0f}x rho0 at 1 kpc or")
print(f"  ~{M_pn/V_gal/rho0:.1f}x over the galaxy - the 24% holds only if ~1% of")
print(f"  the phonons are RETAINED (the rest wears out into the bath). The")
print(f"  retention fraction is the open number: how much of the exhaust stays")
print(f"  in the field vs rejoins the baseline.")
res = {"per_kg_rate": mdot_deep/M_SUN, "M_exhaust": M_exh,
       "share_of_stellar": M_exh/M_bulge, "M_photons": M_ph,
       "M_phonons": M_pn, "rho_exh_1kpc": M_pn/V_bulge_1kpc,
       "rho_exh_galaxy": M_pn/V_gal, "g_exh": g_exh}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "exhaust_accounting.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
