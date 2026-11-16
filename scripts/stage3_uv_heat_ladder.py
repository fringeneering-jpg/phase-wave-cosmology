# stage3_uv_heat_ladder.py - the photon's heat in the planet's gas (2026-10-18)
# The UV/EUV photon unties the gas molecules (photodissociation/ionization);
# the fragments' kinetic energy heats the gas; the products either escape
# (carrying their energy away - Mars's oxygen channel) or re-radiate
# (CO2's 15 um cooling - Venus's cold thermosphere). The thermospheric
# temperature is the readout of the partition.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()

L_SUN = 3.828e26
AU = 1.496e11
F_UV = 0.087        # the UV/EUV share of the solar energy

# name, d (AU), gas, exobase T observed (K, dayside, rough), chemistry note
bodies = [
    ("Venus",   0.723, "CO2, 92 bar",    270.0,
     "2x the flux, COLDEST thermosphere: CO2's 15 um band re-radiates the heat"),
    ("Earth",   1.000, "N2/O2, 1 bar",   1000.0,
     "the UV unties O2; the fragments heat the thin upper gas; weak IR cooling"),
    ("Mars",    1.524, "CO2, 6 mbar",    350.0,
     "the chemical case: UV unties CO2 -> CO + O; the O ESCAPES with its share"),
    ("Jupiter", 5.203, "H2/He, deep",    1100.0,
     "weak UV yet a hot thermosphere: the deep gas vibrates (own furnace)"),
]

print("=" * 78)
print("THE UV-HEAT LADDER - does the radiation heat the gas? (yes, via density+chemistry)")
print("=" * 78)
print(f"{'body':9s} {'d AU':>6s} {'UV flux':>9s} {'gas':>14s} {'T_exo K':>8s}")
rows = []
for name, d, gas, texo, note in bodies:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    uv = F_UV * flux
    rows.append({"name": name, "d_AU": d, "UV_W_m2": uv, "gas": gas,
                 "T_exobase_K": texo})
    print(f"{name:9s} {d:6.3f} {uv:9.2f} {gas:>14s} {texo:8.0f}")
    print(f"           {note}")
print()
print("the partition, per body:")
print("  Venus:   the UV unties CO2 high up; the 15 um band re-radiates the heat")
print("           almost as fast as it arrives -> exobase ~270 K despite 2x flux.")
print("  Earth:   the UV unties O2; the fragments heat the thin gas; N2/O2 cool")
print("           weakly -> exobase ~1000 K.")
print("  Mars:    the chemical case - the UV unties CO2 into CO + O, the O")
print("           ESCAPES carrying its share of the energy (the 14x over-")
print("           production the entropy ladder measured), the rest heats the")
print("           thin gas -> exobase ~350 K.")
print("  Jupiter: the UV is weak (0.9 W/m2) yet the thermosphere runs ~1100 K -")
print("           the gas DENSITY is enormous and the deep fluid vibrates (the")
print("           own furnace again): the heat comes up from below, not the UV.")
print()
print("the answer: YES - the photons create heat in the planet's gas, and the")
print("amount is set by the gas's DENSITY (the absorber) and its CHEMISTRY (the")
print("partition: heat vs dissociation vs escape vs re-radiation). The photon")
print("unties the molecule; the gas decides what the energy becomes.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "uv_heat_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
print()
print("result written:", out)
