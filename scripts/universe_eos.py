# universe_eos.py - the UNIVERSE's equation of state (2026-10-18)
# Forget the local cases: the cosmic EOS. The medium's own w = P/(rho.c0^2):
# with P = rho.C^2 and C = c0 at the baseline, the universe's w = 1 - the
# Zel'dovich STIFF fluid. The census: the medium's rho0, the matter's the
# f_solid share, the heat's the 1:990 ledger, the expansion's the H_wall.
import numpy as np

c0 = 2.9979e8
rho_0 = 8.74e-27
f_solid = 8.4989e-4
Q_CMB = 4.175e-14          # J/m^3
H_wall = 2.396e-18          # /s (the 73.935 km/s/Mpc's)
P0 = c0**2 * rho_0

print("THE UNIVERSE'S EQUATION OF STATE:")
print()
print("  1. THE w-PARAMETER:")
w = P0 / (rho_0 * c0**2)
print(f"     w = P/(rho.c0^2) = c0^2.rho0/(rho0.c0^2) = {w:.4f}")
print(f"     -> the universe is a STIFF fluid (the w = 1, the Zel'dovich's)")
print()
print("  2. THE ENERGY CENSUS (the framework's own ledger):")
rho_medium = rho_0
rho_matter = f_solid * rho_0
rho_heat = 19.0 * Q_CMB / c0**2
rho_total = rho_medium + rho_matter + rho_heat
print(f"     the medium:     {rho_medium:.4e} kg/m^3")
print(f"     the matter's:   {rho_matter:.4e} kg/m^3  (the f_solid = {f_solid:.4e})")
print(f"     the heat's:     {rho_heat:.4e} kg/m^3  (the 19.Q_CMB/c0^2)")
print(f"     the total's:    {rho_total:.4e} kg/m^3")
print()
print("  3. THE EFFECTIVE w OF THE CENSUS:")
w_eff = (rho_medium * c0**2 + rho_heat * c0**2 / 3.0) / (rho_total * c0**2)
print(f"     the w_eff = (the medium's stiff + the heat's 1/3)/(the total's)")
print(f"     w_eff = {w_eff:.6f}")
print()
print("  4. THE EXPANSION'S CHECK (the framework's own H_wall):")
print(f"     H_wall = {H_wall:.4e} /s = the 73.935 km/s/Mpc's")
print(f"     the stiff-fluid's Friedmann's: (a_dot/a)^2 = 8.pi.G.rho_total/3")
G = 6.674e-11
H_fried = np.sqrt(8.0 * np.pi * G * rho_total / 3.0)
print(f"     the check: sqrt(8.pi.G.rho_total/3) = {H_fried:.4e} /s")
print(f"     vs the framework's H_wall: {H_wall:.4e} /s")
print(f"     the ratio: {H_fried/H_wall:.4f}  (the framework's H0 = 32.371 c0^2's bridge)")
print()
print("the honest state: the universe's EOS is the STIFF w=1 medium with the")
print("matter's and heat's as the census's shares. The expansion's the H_wall's")
print("(the framework's own untie-rate), NOT the Friedmann's gravity's - the")
print("wall's the pressure-side clock the k-H0 bridge derived.")
