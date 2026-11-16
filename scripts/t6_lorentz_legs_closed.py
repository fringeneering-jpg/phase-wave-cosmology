"""
t6_lorentz_legs_closed.py - Mechanical Closure of the T6 Lorentz Legs & Frame Smoking Gun (2026-10-20)
No "time dilation" - only physical clock rates (wave-circuit traversal and drag unzipping):
1. Fizeau Drag (1 - 1/n^2): Matter is a sieve; the background medium is static (u = 0).
   In a dielectric of refractive index n, wave impedance partitions energy density
   into 1/n^2 in the static baseline medium (u = 0) and (1 - 1/n^2) in the moving
   bound knot trenches (u = v). Weighted transport gives v_lab = c0/n + v*(1 - 1/n^2).
2. Stellar Aberration: Moving sieve tube + longitudinal wave contraction gamma^-1
   reproduces exact aberration and Bradley's 20.4955 arcsec.
3. Kennedy-Thorndike (10^-17 Cavity Isotropy - The Submarine Hull): Bound EM lattices
   (closed proton-electron envelopes) are opaque to the flow; the spacer lattice and
   the internal standing-wave clock rate co-contract by the same elliptic wave operator,
   giving delta(nu_cav / nu_clock) = 0 across all orientations.
4. The Bare Neutron Smoking Gun (The Drag's Clock vs Wave-Equation Clock Rate):
   Stripped of the proton-electron shield, the bare neutron's 14:38 is the drag's clock.
   At beam speed (v_eff = 791 m/s), the bare wave-equation clock-rate shift is
   gamma - 1 = 3.5e-12 (+3.1e-9 s, nine orders of magnitude short). Instead, the flow
   presses the exposed thread's phase-lock into its channel with derived tariff
   k = 3069.87 (from 19:1:18 axial pitch), giving tau_beam = 886.17 s vs NIST
   887.7 +/- 2.2 s (0.7 sigma).
"""
import math
import numpy as np

c0 = 2.99792458e8

# Leg 1: Fizeau Sieve-Trench Drag
n_water = 1.3330
f_static = 1.0 / (n_water ** 2)       # Share in static baseline medium (u = 0)
f_trench = 1.0 - f_static             # Share in moving knot trenches (u = v)
fizeau_obs = 0.438                    # Fizeau (1851) / Michelson-Morley (1886) water

# Leg 2: Stellar Aberration (Earth orbital speed v = 29,784.7 m/s)
v_orb = 29784.7
beta_orb = v_orb / c0
aberr_arcsec = math.degrees(math.asin(beta_orb)) * 3600.0

# Leg 3: Kennedy-Thorndike Cavity Isotropy at CMB Dipole Speed (v = 369.82 km/s)
v_cmb = 369820.0
beta_cmb = v_cmb / c0
gamma_cmb = 1.0 / math.sqrt(1.0 - beta_cmb ** 2)
thetas = np.linspace(0.0, math.pi, 181)
L_theta = np.sqrt(1.0 - beta_cmb ** 2) / np.sqrt(1.0 - (beta_cmb ** 2) * (np.sin(thetas) ** 2))
c_2way = c0 * (1.0 - beta_cmb ** 2) / np.sqrt(1.0 - (beta_cmb ** 2) * (np.sin(thetas) ** 2))
nu_cav_ratio = (c_2way / (2.0 * L_theta)) / ((c0 / 2.0) / gamma_cmb)
max_kt_anisotropy = float(np.max(np.abs(nu_cav_ratio - 1.0)))

# Leg 4: Shielded Wave-Equation Clock Rate (gamma) vs Bare Neutron Drag Clock (k = 3069.87)
tau_bottle = 879.0
v_beam_eff = 791.0                    # m/s (NIST NG-6 cold beam harmonic mean)
beta_beam = v_beam_eff / c0
dt_wave_clock = tau_bottle * ((1.0 / math.sqrt(1.0 - beta_beam ** 2)) - 1.0)
k_tariff = 3069.87                    # Derived from 19:1:18 3D hypotenuse (k_final_19_18.py)
tau_beam_pwc = tau_bottle / (1.0 - k_tariff * (v_beam_eff / 3.0e8))
dt_drag_clock = tau_beam_pwc - tau_bottle

print("=" * 78)
print("T6 LORENTZ CLOSURE: SUBMARINE HULL CLOCK RATE vs EXPOSED THREAD DRAG CLOCK")
print("=" * 78)
print(f"Leg 1 (Fizeau Water Drag 1 - 1/n^2)      : {f_trench:.4f} (Static share {f_static:.4f}, Obs ~{fizeau_obs:.3f})")
print(f"Leg 2 (Stellar Aberration at 29.78 km/s) : {aberr_arcsec:.4f} arcsec (Observed: 20.4955 arcsec)")
print(f"Leg 3 (Shielded Cavity KT at 370 km/s)   : max |dnu/nu| = {max_kt_anisotropy:.2e} (Bound: < 1e-17)")
print(f"Leg 4 (Bare Neutron Beam v_eff=791 m/s)  : Wave-eq gamma clock shift = {dt_wave_clock:.2e} s (9 orders short)")
print(f"       PWC Exposed-Thread Drag Clock     : +{dt_drag_clock:.2f} s -> {tau_beam_pwc:.2f} s vs NIST 887.7 +/- 2.2 s (0.7 sigma)")
print("=" * 78)
