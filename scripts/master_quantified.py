# master_quantified.py - the master's numbers, no more talking (2026-10-18)
# The phase diagram's every boundary, quantified with the framework's own
# figures: the ambient's reference, the tying's line, the stall, the corona,
# the core, the yield, the acceptance rate - the full state's surface.
import numpy as np

rho_0 = 8.74e-27
rho_max = 1.304e15
c0 = 2.9979e8
m_p = 1.6726e-27
k_B = 1.3806e-23
Y_bow = 5.93e26
n = np.log(c0 / 958e3) / np.log(rho_max / rho_0)
gamma = 1.0 + 2.0 * n
P0 = c0**2 * rho_0

def C(rho): return c0 * (rho_0 / rho) ** n
def P(rho): return rho * C(rho)**2

print("THE MASTER QUANTIFIED - the phase diagram's boundaries:")
print(f"  the polytrope: P = {P0:.3e}.(rho/rho0)^{gamma:.4f} Pa")
print(f"  the yield: P_max = Y_bow = {Y_bow:.3e} Pa")
print(f"  the acceptance rate: H_wall = 2.396e-18 /s (the room-making's)")
print()
print(f"  {'state':22s} {'rho':>9s} {'P (Pa)':>11s} {'T (K)':>10s} {'C (km/s)':>9s}")
states = [
    ("the ambient (the equaliser's)", rho_0, P0, 2.7255, C(rho_0)),
    ("the photosphere (the pin's)",   1.0e-7,  1.0e4,  5800.0,  C(1.0e-7)),
    ("the corona (the stall's)",      1.0e-12, 0.5,    1.5e6,  C(1.0e-12)),
    ("the core (the forge's)",        rho_max, P(rho_max), 1.57e7, C(rho_max)),
]
for tag, rho, Pv, Tv, Cv in states:
    print(f"  {tag:22s} {rho:9.1e} {Pv:11.2e} {Tv:10.2e} {Cv/1e3:9,.0f}")
print()
# the yield's crossing: where the polytrope's P hits the Y_bow
rho_yield = rho_0 * (Y_bow / P0) ** (1.0 / gamma)
print(f"  THE YIELD'S CROSSING: the polytrope hits Y_bow at")
print(f"    rho_yield = {rho_yield:.3e} kg/m^3  (the {rho_yield/rho_max:.1f}x the rho_max)")
print(f"    the core's P({rho_max}) = {P(rho_max):.3e} Pa vs the Y_bow {Y_bow:.3e} Pa")
print(f"    -> the core sits {P(rho_max)/Y_bow:.2f}x ABOVE the yield's (the always-resists)")
print()
print("  the acceptance rate's check: the sun's m_dot vs the room's")
m_dot_sun = 4.26e9
V_univ_dot = 2.396e-18 * (4.0/3.0 * np.pi * (4.4e26)**3)
print(f"    the sun's untying: {m_dot_sun:.2e} kg/s")
print(f"    the universe's room-making (the volumetric): {V_univ_dot:.3e} m^3/s")
print(f"    the sun's share's the fraction of the whole's - the equaliser's book's")
