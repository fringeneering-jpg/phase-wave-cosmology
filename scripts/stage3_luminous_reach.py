# stage3_luminous_reach.py - the 1/r^2 scaled to the luminous threshold (2026-10-18)
# Jaden: the photon mass scales as 1/r^2, so scale it out to where there's
# not even enough to LUMINESS anymore. The framework's threshold: the wave
# must carry more energy density than the baseline's own heat (the CMB bath,
# u_cmb = a T^4). When the star's photon density drops to the bath's, the
# light has WORN OUT - it rejoins the 2.7255 K graveyard. So:
#   u_ph(r) = L / (4 pi r^2 c0) = u_cmb  ->  r_lum = sqrt(L / (4 pi c0 u_cmb))
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11
LY = 9.4607e15
A_RAD = 7.5657e-16
T_CMB = 2.7255
U_CMB = A_RAD * T_CMB ** 4

r_lum = (L_SUN / (4 * 3.14159265358979 * c0 * U_CMB)) ** 0.5

print("=" * 78)
print("THE LUMINOUS REACH - scale the 1/r^2 to the floor")
print("=" * 78)
print(f"the bath: u_cmb = a T^4 = {U_CMB:.2e} J/m^3 (the 2.7255 K baseline)")
print(f"the star's photon energy density: u_ph(r) = L / (4 pi r^2 c0)")
print(f"the luminous threshold: u_ph = u_cmb  ->  the wave has worn out")
print()
print(f"r_lum = sqrt(L / (4 pi c0 u_cmb)) = {r_lum:.3e} m")
print(f"      = {r_lum/AU:,.0f} AU = {r_lum/LY:.3f} light-years")
print()
print("the mass at the floor (the cubic km again):")
m_flux_1AU = L_SUN / (4 * 3.14159265358979 * AU ** 2) / c0 ** 2
m_km3_1AU = m_flux_1AU * 1000.0 ** 3 / c0
m_km3_lum = m_km3_1AU * (AU / r_lum) ** 2
print(f"  at 1 AU:      {m_km3_1AU:.2e} kg/km^3 = 50.5 femtograms")
print(f"  at the floor: {m_km3_lum:.2e} kg/km^3 = {m_km3_lum*1e15:.2e} femtograms")
print()
print("the reading: the Sun's light wears below the luminous threshold at")
print("~10,400 AU (0.165 light-years) - the Oort cloud's own doorstep. Beyond")
print("that the star's waves have diluted below the bath's own energy density:")
print("they rejoin the 2.7255 K baseline, the CMB's graveyard. A star's")
print("luminous reach is finite: r_lum = sqrt(L / 4 pi c0 u_cmb) - every star's")
print("light dies into the bath at its own distance, and the 1/r^2 finds the")
print("floor exactly where the mass runs out.")
res = {"u_cmb": U_CMB, "r_lum_m": r_lum, "r_lum_AU": r_lum/AU,
       "r_lum_ly": r_lum/LY, "m_km3_1AU_kg": m_km3_1AU,
       "m_km3_at_floor_kg": m_km3_lum}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "luminous_reach.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
