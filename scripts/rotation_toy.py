import numpy as np

# ==============================================================================
# JIBA TOY MODEL: SHELL TAUTNESS (SURFACE AREA GRADIENT) VS POINT-MASS BASELINE
# Zero free parameters. All inputs are raw physical constants (GM, R, omega).
# ==============================================================================

C = 299792458.0
AU = 149597870697.0
GM_SUN = 1.32712440018e20
R_SUN = 6.957e8
OMEGA_SUN = 2.8653e-6
K_SUN = (2.0 * OMEGA_SUN * R_SUN) / C

# Planets: GM [m^3/s^2], Radius R [m], Semi-major axis a [m], Eccentricity e, Spin omega [rad/s]
PLANETS = {
    "Mercury": {"GM": 2.203209e13,    "R": 2.4397e6,  "a": 0.38709893*AU, "e": 0.20563069, "omega": 1.24001e-6},
    "Venus":   {"GM": 3.24858592e14,  "R": 6.0518e6,  "a": 0.72333199*AU, "e": 0.00677323, "omega": -2.9924e-7},
    "Earth":   {"GM": 3.986004415e14, "R": 6.3710e6,  "a": 1.00000011*AU, "e": 0.01671022, "omega": 7.292115e-5},
    "Mars":    {"GM": 4.28283762e13,  "R": 3.3895e6,  "a": 1.52366231*AU, "e": 0.09341233, "omega": 7.088218e-5},
    "Jupiter": {"GM": 1.26712765e17,  "R": 6.9911e7,  "a": 5.20336301*AU, "e": 0.04839266, "omega": 1.7585e-4},
    "Saturn":  {"GM": 3.79406803e16,  "R": 5.8232e7,  "a": 9.53707032*AU, "e": 0.05415060, "omega": 1.6378e-4},
}

def analyze_shell_tautness():
    print(f"{'Body':<9} | {'Surf Area (m^2)':<15} | {'String Freq (mHz)':<17} | {'Surf Gravity (m/s^2)':<20} | {'Relax Scale R (km)':<18}")
    print("-" * 88)
    for name, p in PLANETS.items():
        area = 4.0 * np.pi * (p["R"]**2)
        # Fundamental Kepler/Helmholtz "twang" frequency at the shell: f = (1/2pi)*sqrt(GM / R^3)
        freq_mhz = (1.0 / (2.0 * np.pi)) * np.sqrt(p["GM"] / (p["R"]**3)) * 1000.0
        g_surf = p["GM"] / (p["R"]**2)
        print(f"{name:<9} | {area:<15.3e} | {freq_mhz:<17.4f} | {g_surf:<20.3f} | {p['R']/1000.0:<18.1f}")

def compare_mars_saturn_mercury_residuals():
    print("\n=== SOLAR + PLANETARY SHELL RELAXATION TOY BENCHMARK ===")
    for name in ["Mercury", "Mars", "Saturn"]:
        p = PLANETS[name]
        r_peri = p["a"] * (1.0 - p["e"])
        r_aphe = p["a"] * (1.0 + p["e"])
        
        # 1. Baseline Solar Rotational + z+1 Radial Swing (Model A: Point Mass)
        dr_point_mass = p["a"] * p["e"] * K_SUN
        
        # 2. Shell Tautness / Area Ratio Correction (Model B: Finite Shell Relaxation)
        # Solar shell relaxation factor (R_sun / r)^2 + Planetary shell compactness
        shell_ratio_peri = (R_SUN / r_peri)**2
        shell_ratio_aphe = (R_SUN / r_aphe)**2
        delta_shell_sun = shell_ratio_peri - shell_ratio_aphe
        
        # Planet's own internal shell frequency ratio relative to Sun's shell frequency
        omega_shell_planet = np.sqrt(p["GM"] / (p["R"]**3))
        omega_shell_sun = np.sqrt(GM_SUN / (R_SUN**3))
        tautness_ratio = omega_shell_planet / omega_shell_sun
        
        # Additional radial phase shift from the shell-area tension gradient
        dr_shell_tension = (p["a"] * p["e"]) * delta_shell_sun * tautness_ratio
        
        print(f"\n[{name.upper()}]")
        print(f"  Tautness Ratio (f_planet / f_sun) : {tautness_ratio:.4f}")
        print(f"  Solar Shell Area Swing d(R_s/r)^2 : {delta_shell_sun:.6e}")
        print(f"  Model A (Point-Mass K_sun Drift)  : {dr_point_mass:,.2f} m")
        print(f"  Model B (Shell Tension Addition)  : {dr_shell_tension:,.2f} m")
        print(f"  Total Combined Unfitted Wave      : {dr_point_mass + dr_shell_tension:,.2f} m")

if __name__ == "__main__":
    analyze_shell_tautness()
    compare_mars_saturn_mercury_residuals()