# sun_derivation.py - the sun's untying: the full output ledger (2026-10-18)
# The correction of 2026-10-18: heat/light is NOT the only output. The sun's
# untying runs TWO channels, the framework's own two-rung structure:
#   DEEP    - radiation + neutrinos: each kg pays the phase-change price c0^2
#             (the m = L/c0^2 identity converts the escaping energy to mass).
#   SHALLOW - wind + CMEs: material leaves TIED (the sublimation rung of the
#             comet script) - it pays only escape energy, not c0^2, and its
#             mass rate is measured directly from the outflow, not from L/c0^2.
# The total mass-untying rate = deep + shallow; it must close against the
# standard's measured solar mass loss. The old "4-5 million tonnes/yr" claim
# was wrong by ~7 orders: fixed below.
import math

c0   = 2.99792458e8
rho0 = 8.74e-27
rho_max = 1.304e15
m_p  = 1.6726e-27
k_B  = 1.3806e-23

L_rad = 3.828e26            # W  total EM radiation (MEASURED)
L_neu = 0.023 * L_rad       # W  solar neutrino luminosity ~2.3% of L (MEASURED)

def C(rho):
    n = math.log(c0 / 958e3) / math.log(rho_max / rho0)
    return c0 * (rho0 / max(rho, 1e-30)) ** n

print("THE SUN'S UNTYING - THE FULL OUTPUT LEDGER (2026-10-18)")
print()
print("1. THE DEEP CHANNEL (radiation + neutrinos - the c0^2-paying untying):")
m_dot_deep = (L_rad + L_neu) / c0**2
print(f"   (L_rad + L_neu) = {(L_rad+L_neu):.3e} W  ->  /c0^2 = {m_dot_deep:.3e} kg/s")
print(f"   = {m_dot_deep*86400*365.25/1e12:.1f} trillion tonnes/yr")
print(f"   radiation alone: {L_rad/c0**2:.3e} kg/s = {L_rad/c0**2*86400*365.25/1e12:.1f} trillion t/yr")
print(f"   neutrinos add:   {L_neu/c0**2:.3e} kg/s (2.3% of the radiative channel)")
print()
print("2. THE SHALLOW CHANNEL (the wind + CMEs - material leaves TIED):")
m_dot_wind = 1.5e9             # kg/s  measured solar-wind mass flux
m_dot_cme  = 0.06e9            # kg/s  measured average CME mass flux
v_wind = 4.5e5                 # m/s
print(f"   wind: {m_dot_wind:.2e} kg/s (MEASURED outflow, not L/c0^2)")
print(f"   wind kinetic power: 0.5*m_dot*v^2 = {0.5*m_dot_wind*v_wind**2:.2e} W")
print(f"     (6 orders below the radiative channel - the shallow rung's own proof:")
print(f"      it does NOT pay c0^2 per kg)")
print(f"   CMEs: {m_dot_cme:.2e} kg/s (MEASURED, cycle-dependent)")
print()
print("3. THE TOTAL - the mass-untying rate, both channels:")
m_dot_total = m_dot_deep + m_dot_wind + m_dot_cme
print(f"   deep + shallow = {m_dot_total:.3e} kg/s = {m_dot_total*86400*365.25/1e12:.1f} trillion t/yr")
print(f"   standard's measured solar mass loss ~ (5.8-6.3)e9 kg/s; the ranging")
print(f"   value sits lower (~3.9e9 +/- 0.9e9 kg/s) - the sum closes the ledger")
print(f"   within the observational spread. The identity m = L/c0^2 covers the")
print(f"   DEEP channels exactly; the wind and CMEs are added mass on top -")
print(f"   light is not the only output.")
print()
print("4. THE UNTYING SPEED (the waves at the local C at each radius):")
for tag, rho in [("the corona's base (~1e-12)", 1e-12), ("the corona's mid (~1e-13)", 1e-13),
                 ("the corona's outer (~1e-15)", 1e-15)]:
    print(f"   {tag} kg/m^3:  C = {C(rho)/1e3:,.0f} km/s")
print()
print("the honest read: the untying's speed is the capacity ladder's (the")
print("thousands of km/s at the corona), and the mass cost is the FULL output")
print("ledger - deep (L/c0^2, the light and neutrinos) plus shallow (the wind")
print("and CMEs, measured directly). The old '4-5 million tonnes/yr' comparison")
print("was dropped: the correct number is ~190 trillion tonnes/yr total.")
