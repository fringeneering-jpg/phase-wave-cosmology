# The 20-black-hole volume-to-mass ladder (chat catalog, 2026-10-01) -> friction scale
import math
c0 = 2.99792458e8
G = 6.6743e-11
rho_core = 2.3e17
rho_max = 1.304e15
a_max = 3.23e11
Msun = 1.989e30
Y = 5.93e26

holes = [
    ("GRO J1655-40", 5.3), ("V404 Cyg", 9.0), ("Gaia BH1", 9.6), ("Cyg X-1", 21.2),
    ("Gaia BH3", 33.0), ("GW150914", 62.0), ("GW190521", 142.0),
    ("Omega Cen", 8.2e3), ("HLX-1", 2.0e4), ("Sgr A*", 4.3e6), ("Cen A", 5.5e7),
    ("M31", 1.4e8), ("M104", 1.0e9), ("M87*", 6.5e9), ("OJ 287", 1.83e10),
    ("Holm 15A", 4.0e10), ("S5 0014+81", 4.0e10), ("IC 1101", 1.0e11),
    ("TON 618", 6.6e10), ("Phoenix A*", 1.0e11),
]

print(f"{'hole':<12} {'M/Msun':>9} {'choke km':>10} {'core km':>10} {'edge km':>11}  V/M + friction caps")
print("="*100)
Vm_core = 1.0/rho_core
Vm_max = 1.0/rho_max
v_core = math.sqrt(2*Y/rho_core)/1e3
v_max = math.sqrt(2*Y/rho_max)/1e3
for name, M in holes:
    m = M*Msun
    r_choke = 2*G*m/c0**2
    r_core = (3*m/(4*math.pi*rho_core))**(1/3)
    r_edge = math.sqrt(G*m/a_max)
    solv = "OK" if m < 1910*Msun else "NO-SOLN(plain rule)"
    print(f"{name:<12} {M:>9.2e} {r_choke/1e3:>9,.0f} {r_core/1e3:>9,.0f} "
          f"{r_edge/1e3:>10,.0f}  [{solv}]")
print("="*100)
print(f"V/M is the SAME for every hole on each rung:")
print(f"  core:     V/M = 1/rho_core = {Vm_core:.3e} m^3/kg -> friction cap {v_core:.0f} km/s")
print(f"  rho_max:  V/M = 1/rho_max  = {Vm_max:.3e} m^3/kg -> friction cap {v_max:.0f} km/s")
print(f"  envelope: V/M rises 1/rho_max -> 1/rho0 -> cap rises 954 km/s -> c0 (dissolved)")
print(f"Mass only moves the RATIOS: core/choke, shell thickness, edge/choke. The friction scale")
print(f"is one universal ladder; the 20 holes are 20 combinations of the same two rungs.")
print(f"Above ~1,910 Msun the plain sqrt(GM/a_max) edge has no solution (session log 2026-10-02)")
print(f"- the k-rule/envelope law takes over; the rungs themselves never change.")
