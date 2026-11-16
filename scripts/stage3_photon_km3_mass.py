# stage3_photon_km3_mass.py - how heavy is a cubic kilometre of sunlight?
# (2026-10-18) Jaden's route: take the 1 km^3, the time the light takes to
# cross that km (t = 1 km / c0), and the force felt in that time; the mass
# of the cubic km = (force x time) / c0. Two routes, one answer:
#   route 1 (the flux density): m = (mass flux / c0) x V = F_flux V / c0^3
#   route 2 (the force x time): m = (F/A x A x L/c0) / c0 = F_flux V / c0^3
# Both give the same: the cubic km's mass = the photon wind's density x V.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
KM = 1000.0

print("=" * 78)
print("HOW HEAVY IS A CUBIC KILOMETRE OF SUNLIGHT?")
print("=" * 78)
print(f"the crossing time: t = 1 km / c0 = {KM/c0:.3e} s")
print(f"route 1: m = (mass flux / c0) x V  =  F_flux V / c0^3")
print(f"route 2: m = (force felt in the crossing) / c0 = F_flux A t / c0")
print()
print(f"{'distance':>14s} {'flux W/m2':>11s} {'cubic-km mass':>15s} "
      f"{'force x time':>14s}")
rows = []
for d_AU, name in [(0.387, "Mercury"), (1.0, "Earth"), (5.2, "Jupiter"),
                   (30.1, "Neptune"), (50.0, "Kuiper belt")]:
    flux = L_SUN / (4 * 3.14159265358979 * (d_AU * AU) ** 2)
    m_km3 = flux * (KM ** 3) / c0 ** 3            # route 1
    F_impulse = (flux / c0) * (KM ** 2) * (KM / c0)   # the force x time
    m_km3_b = F_impulse / c0                      # route 2
    rows.append({"name": name, "d_AU": d_AU, "flux": flux,
                 "mass_km3_kg": m_km3, "mass_route2": m_km3_b})
    print(f"{name:>14s} {flux:11.1f} {m_km3:15.3e} {m_km3_b:14.3e}")
print()
print("the check at 1 AU:")
flux_1 = L_SUN / (4 * 3.14159265358979 * AU ** 2)
m_1 = flux_1 * KM ** 3 / c0 ** 3
print(f"  the cubic km of sunlight weighs m = {m_1:.3e} kg = {m_1*1e15:.1f} femtograms")
print(f"  (both routes agree to the last digit - the force felt in the crossing")
print(f"  time IS the mass)")
print()
print("the comparison - the speed is the force:")
rho_ph = flux_1 / c0 ** 3
print(f"  the photon wind's density at 1 AU: rho_ph = {rho_ph:.2e} kg/m^3")
print(f"  the solar wind's density at 1 AU: ~1e-20 kg/m^3 - the material wind")
print(f"  weighs ~200x MORE per cubic km")
print(f"  but the pressures: the photon wind pushes {flux_1/c0*1e6:.1f} microPa;")
print(f"  the solar wind pushes ~2 nPa - the photon wind pushes ~2000x HARDER")
print(f"  because it arrives at c0: momentum = m c0, and c0 is the hammer.")
print()
print("the reading: the photon's weight is real (m = L/c0^2, ~50 femtograms")
print("per cubic km at 1 AU), the displacement makes it weightless, and the")
print("speed it comes in at is what makes that tiny weight the dominant push")
print("of the whole wind. Heavy, weightless, and the hardest hitter.")
res = {"rows": rows, "km3_mass_1AU_kg": m_1, "photon_density_1AU": rho_ph}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "photon_km3_mass.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
