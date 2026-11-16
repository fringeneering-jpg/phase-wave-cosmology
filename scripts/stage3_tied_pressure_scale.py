# stage3_tied_pressure_scale.py - the 7% before it unties (2026-10-18)
# Jaden: the 2.6796e25 W is the untied waves' force at c into a sail - the
# missing EM energy per second. But BEFORE it unties, the same mass sits
# TIED at the knot density: volumetrically ~1e27x SMALLER, holding the
# stored pressure wanting to untie. Then the extreme heat joins the desire
# to expand - it gets intense. The numbers:
#   tied volume/s = m_rest/rho_max  vs  untied volume/s = m_rest/rho_corona
#   stored pressure = rho_max c0^2  vs  the released light's pressure.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]

L_SUN = 3.828e26
RHO_CORONA = 5.02e-13     # the untied state's density (the quiet corona)

M_REST = 0.07 * L_SUN / c0 ** 2

V_TIED = M_REST / rho_max                    # m^3/s  the tied state's volume
V_UNTIED = M_REST / RHO_CORONA               # m^3/s  the released state's volume
P_TIED = rho_max * c0 ** 2                   # Pa  the stored pressure
U_TIED = rho_max * c0 ** 2                   # J/m^3  the stored energy density
U_RELEASED_1AU = (L_SUN / (4*3.14159265358979*(1.496e11)**2)) / c0

print("=" * 78)
print("THE 7% BEFORE IT UNTIES - the tied state's true scale")
print("=" * 78)
print(f"the missing energy per second: 2.6796e25 W = {M_REST:.3e} kg/s")
print(f"  as UNTIED waves into a sail: the force = {M_REST*c0:.3e} N")
print()
print("the SAME mass, TIED:")
print(f"  tied volume per second:  m/rho_max = {V_TIED:.2e} m^3/s")
print(f"  = {V_TIED*1e9:.2f} mm^3/s - a GRAIN OF SAND every second")
print(f"  untied volume per second: m/rho_corona = {V_UNTIED:.2e} m^3/s")
print(f"  = {V_UNTIED/1.083e21:.2f} EARTH-VOLUMES per second")
print(f"  the volumetric contrast: {V_UNTIED/V_TIED:.1e}x")
print()
print("the stored pressure, wanting to untie:")
print(f"  P_tied = rho_max c0^2 = {P_TIED:.2e} Pa")
print(f"  the stored energy density: {U_TIED:.2e} J/m^3")
print(f"  vs the released light at 1 AU: {U_RELEASED_1AU:.2e} J/m^3")
print(f"  -> the tied state packs the 7% at {U_TIED/U_RELEASED_1AU:.1e}x the")
print(f"  released form's density")
print()
print("and then the heat joins the desire to expand: the stalled heat raises")
print("the multiplier on the untying demand - the stored pressure's expansion")
print("drive compounds with the temperature. A grain of sand of knot-stuff,")
print("holding the pressure that would fill half the Earth, heated - intense")
print("is the right word.")
res = {"M_restricted": M_REST, "V_tied_m3_s": V_TIED,
       "V_tied_mm3_s": V_TIED * 1e9, "V_untied_m3_s": V_UNTIED,
       "volumetric_contrast": V_UNTIED / V_TIED, "P_tied_Pa": P_TIED,
       "u_tied": U_TIED, "u_released_1AU": U_RELEASED_1AU,
       "energy_density_contrast": U_TIED / U_RELEASED_1AU}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "tied_pressure_scale.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
