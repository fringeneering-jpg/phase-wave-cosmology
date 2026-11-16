import math

# --- LOCKED PWC FRAMEWORK CONSTANTS (ZERO FREE PARAMETERS) ---
G = 6.67430e-11           # Gravitational constant [m^3 kg^-1 s^-2]
C = 299792458.0           # Wave speed [m/s]
AU = 1.495978707e11       # Astronomical Unit [m]
RHO_0 = 8.74e-27          # Rest medium density [kg/m^3]
A_ENTROPY = 8.9297e-10    # Locked c_0 * H_0 * (1 + dRho) [m/s^2]
MU_SUN = 1.32712440041e20 # Solar GM [m^3/s^2]

PLANETS = [
    ("Mercury", 0.387098, 2.203186855e13, "MESSENGER Perih.", 2640.0,   "BepiColombo/Hill", 1.75e5),
    ("Venus",   0.723332, 3.248585920e14, "Magellan Perih.",  6300.0,   "Solar Wake Edge",  5.00e5),
    ("Earth",   1.000000, 3.986004418e14, "LAGEOS-1 (MEO)",   12270.0,  "Moon (Lunar SLR)", 384399.0),
    ("Mars",    1.523679, 4.282837521e13, "Phobos",           9376.0,   "Deimos",           23463.2),
    ("Jupiter", 5.204400, 1.266865349e17, "Io",               421700.0, "Callisto",         1882700.0),
    ("Saturn",  9.582600, 3.793118790e16, "Mimas",            185539.0, "Iapetus",          3560820.0),
    ("Uranus",  19.21840, 5.793939900e15, "Miranda",          129390.0, "Oberon",           583520.0),
    ("Neptune", 30.11000, 6.836529900e15, "Proteus",          117647.0, "Nereid",           5513810.0),
]

def pwc_dressing_accel(r_sun_au, r_local_m, gm_planet):
    # Pure dimensionless solar potential compression (no 1e6 hack)
    solar_phi = 2.0 * MU_SUN / (C**2 * r_sun_au * AU)
    a_strain = A_ENTROPY * (1.0 + solar_phi)
    
    # Solar-wake Mach dipole coupling
    v_orb_planet = math.sqrt(MU_SUN / (r_sun_au * AU))
    v_local = math.sqrt(gm_planet / r_local_m)
    a_dipole = -(gm_planet / (r_local_m**2)) * ((v_orb_planet * v_local) / (C**2))
    return a_strain + a_dipole

if __name__ == "__main__":
    print("=" * 105)
    print("PWC LOCKED ENTROPIC DRESSING & TRUE PLANETARY WEIGHT UN-DRESSING MAP")
    print(f"Locked a_entropy = {A_ENTROPY:.4e} m/s^2 | Earth LAGEOS->Moon Convergence = +331.0 ppb")
    print("=" * 105)
    for name, r_au, gm_jpl, in_name, r_in_km, out_name, r_out_km in PLANETS:
        r_in_m, r_out_m = r_in_km * 1000.0, r_out_km * 1000.0
        d_gm_in = pwc_dressing_accel(r_au, r_in_m, gm_jpl) * (r_in_m**2)
        d_gm_out = pwc_dressing_accel(r_au, r_out_m, gm_jpl) * (r_out_m**2)
        span_ppm = ((d_gm_out - d_gm_in) / gm_jpl) * 1e6
        undressed_mass_diff_kg = (d_gm_out - d_gm_in) / G
        print(f"{name:<8} | {r_au:>5.2f} AU | {in_name:<16} -> {out_name:<16} | "
              f"Dressing: {span_ppm:>+8.4f} ppm | Absorbed: {undressed_mass_diff_kg:>+10.3e} kg")
    print("=" * 105)
