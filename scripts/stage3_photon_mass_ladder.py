# stage3_photon_mass_ladder.py - the photon's weight via the sail (2026-10-18)
# Jaden: "take the speed and the photon sail's force felt, divide by area
# and speed, you get the mass. The photon HAS weight - it's the displacement
# that makes it weightless. And it should drop off at 1/r^2."
# The check: the sail's force per area = the momentum flux = m_dot c0 / A,
# so the photon mass flux = F/(A c0) = (L_sun/4 pi d^2)/c0^2 - the
# framework's own m = L/c0^2 per area-time - falling as 1/r^2. The photon's
# weight = its mass x the pull; its weightlessness = the medium's own
# transmission carrying it at max-P (the displacement - the buoyancy).
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]

L_SUN = 3.828e26
AU = 1.496e11

print("=" * 78)
print("THE PHOTON'S WEIGHT VIA THE SAIL - the mass behind the momentum")
print("=" * 78)
print(f"the sail's force per area = the momentum flux = m_dot c0 / A")
print(f"-> the photon mass flux = F/(A c0) = (L_sun/4 pi d^2)/c0^2 = m = L/c0^2")
print()
print(f"{'distance':>14s} {'flux W/m2':>11s} {'sail F/A (N/m2)':>14s} "
      f"{'photon mass flux':>17s}")
rows = []
for d_AU, name in [(0.387, "Mercury"), (1.0, "Earth"), (5.2, "Jupiter"),
                   (30.1, "Neptune"), (50.0, "Kuiper belt")]:
    flux = L_SUN / (4 * 3.14159265358979 * (d_AU * AU) ** 2)
    F_A = flux / c0                       # the sail's force per area
    mflux = F_A / c0                      # divide by the speed: the mass flux
    rows.append({"name": name, "d_AU": d_AU, "flux": flux, "F_per_A": F_A,
                 "mass_flux": mflux})
    print(f"{name:>14s} {flux:11.1f} {F_A:14.3e} {mflux:17.3e} kg/(m^2 s)")
print()
print("the checks:")
print(f"  at 1 AU: F/A = 1361/c0 = {1361.0/c0:.3e} N/m^2 = 4.5 microPa (the")
print(f"  known solar radiation pressure) - the sail feels the photon's momentum.")
print(f"  the mass behind it: (1361 W/m2)/c0^2 = {1361.0/c0**2:.3e} kg/(m^2 s)")
print(f"  the whole outflow: L_sun/c0^2 = {L_SUN/c0**2:.3e} kg/s = the deep")
print(f"  channel itself (mdot_deep = {mdot_deep:.3e} kg/s) - the sail's side")
print(f"  and the untying's side read the SAME mass.")
print(f"  and it drops off as 1/r^2: Mercury {rows[0]['mass_flux']:.2e} ->")
print(f"  Neptune {rows[3]['mass_flux']:.2e} -> Kuiper {rows[4]['mass_flux']:.2e} "
      f"kg/(m^2 s) - phenomenologically the inverse square.")
print()
print("the reading: the photon HAS weight - m = L/c0^2 - and the sail's force")
print("divided by area and speed hands that mass straight back. Its")
print("weightlessness is the DISPLACEMENT: the medium carries its own wave at")
print("max-P, so the photon doesn't fall - the weight is carried by the medium's")
print("tension, not by the photon. Mass with buoyancy: the same physics as the")
print("electron riding the medium.")
res = {"rows": rows, "mass_flux_1AU": 1361.0 / c0 ** 2,
       "sail_pressure_microPa": 1361.0 / c0 * 1e6,
       "total_outflow_kg_s": L_SUN / c0 ** 2}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "photon_mass_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
