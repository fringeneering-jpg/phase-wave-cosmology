#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
astrodynamic_anomalies_anderson.py
Verifies the 5 Orbital & Deep-Space Anomalies & Eisenhart Lift Geodesic Formulation
using ONLY locked Phase Wave Cosmology (PWC) constants (Zero Free Parameters).
Dedicated to John D. Anderson for his refusal to settle on Pioneer 10/11 and Ulysses telemetry.
"""
import math
from math import gamma

# ==============================================================================
# LOCKED PWC CONSTANTS (ZERO FREE PARAMETERS)
# ==============================================================================
c0       = 2.99792458e8          # m/s (Ambient baseline wave capacity)
G        = 6.67430e-11           # m^3 kg^-1 s^-2 (Locked gravitational bridge)
rho0     = 8.74e-27              # kg/m^3 (Ambient resting medium density)
H0       = 2.396e-18             # s^-1 (Cosmic untie rate, 73.935 km/s/Mpc)
s        = 1.0 / 19.0            # 19:1:18 axial debt share
f_solid  = 8.4989e-4             # Solid debt share (matter sieve fraction)
AU       = 1.496e11              # m (Astronomical Unit)
SEC_YR   = 3.1558e7              # s/yr (Julian/sidereal year seconds)
g_sun_1AU = 5.9303e-3            # m/s^2 (Solar gravitational acceleration at 1 AU)

# 3D Gamma(1/3) Volumetric Decompression Integral (+24.313%)
EXCESS_BLOOM = 1.5 * float(gamma(1.0 / 3.0)) - 3.0
DELTA_RHO_GEOM = EXCESS_BLOOM / ((4.0 * math.pi) / 3.0)  # +0.24313

# 1. Secular Increase of the Astronomical Unit (dAU/dt)
# Matter is a sieve; forward-hemisphere projection (1/4) * debt share (s = 1/19) = 1/76
dAU_dt_m_yr = AU * H0 * (s / 4.0) * SEC_YR
dAU_dt_cm_yr = dAU_dt_m_yr * 100.0
dAU_obs_cm_yr = 15.0
dAU_err_cm_yr = 4.0
dAU_pct_err = (dAU_dt_cm_yr - dAU_obs_cm_yr) / dAU_obs_cm_yr * 100.0

# 2. Pioneer 10/11 Ecliptic Anomaly (a_P)
# Constant (1+z) untie floor in the 2D ecliptic disk
a_P_pwc = c0 * H0 * (1.0 + DELTA_RHO_GEOM)  # 8.93e-10 m/s^2
a_P_obs = 8.74e-10
a_P_err = 1.33e-10

# 3. Ulysses Polar Chimney Anomaly (a_U)
# 3D spherical polar chimney vs 2D planar ecliptic disk projection ratio = 4/3
a_U_pwc = (4.0 / 3.0) * a_P_pwc             # 1.191e-9 m/s^2
a_U_obs = 1.20e-9
a_U_err = 0.30e-9
a_U_pct_err = (a_U_pwc - a_U_obs) / a_U_obs * 100.0

# 4. 'Oumuamua 1/R^2 Solid-Debt Deficit (a_ng at 1 AU)
# Ordinary matter pays the solid debt share f_solid on the local 1/R^2 solar potential
a_oumuamua_pwc = f_solid * g_sun_1AU        # 5.0401e-6 m/s^2
a_oumuamua_obs = 4.920e-6
a_oumuamua_err = 0.160e-6
a_oumuamua_pct = (a_oumuamua_pwc - a_oumuamua_obs) / a_oumuamua_obs * 100.0
a_oumuamua_sig = (a_oumuamua_pwc - a_oumuamua_obs) / a_oumuamua_err

# 5. Gravitational Saddle Point (grad Phi = 0 -> Ambient Floor Revealed)
a_saddle_pwc = (c0 / math.sqrt(3.0)) * math.sqrt(G * rho0 / 4.0)  # 6.6110e-11 m/s^2

print("=" * 88)
print("THE ASTRODYNAMIC PHENOMENOLOGY OF THE MEDIUM (5 ANOMALIES & EISENHART LIFT)")
print("Credit: John D. Anderson (Pioneer 10/11 & Ulysses Deep-Space Telemetry)")
print("=" * 88)
print(f"- Astronomical Unit Drift (1 AU)  : dAU/dt = (AU*H0)*(s/4) = {dAU_dt_cm_yr:.2f} cm/yr "
      f"(vs {dAU_obs_cm_yr:.1f} +/- {dAU_err_cm_yr:.1f} cm/yr, {dAU_pct_err:+.2f}%)")
print(f"- Pioneer 10/11 (Ecliptic, >20 AU): a_P = c0*H0*(1 + drho_geom) = {a_P_pwc:.2e} m/s^2 "
      f"(vs {a_P_obs:.2e} +/- {a_P_err:.2e} m/s^2)")
print(f"- Ulysses (Polar Orbit)           : a_U = (4/3)*a_P = {a_U_pwc:.3e} m/s^2 "
      f"(vs {a_U_obs:.2e} +/- {a_U_err:.2e} m/s^2, {a_U_pct_err:+.2f}%)")
print(f"- 'Oumuamua (1 AU Flyby)          : a_ng = f_solid * g_sun = {a_oumuamua_pwc:.4e} m/s^2 "
      f"(vs {a_oumuamua_obs:.3e} +/- {a_oumuamua_err:.2e} m/s^2, {a_oumuamua_pct:+.2f}%, {a_oumuamua_sig:+.2f}s)")
print(f"- Saddle Point (grad Phi = 0)     : a_saddle = a0,bare = {a_saddle_pwc:.4e} m/s^2 "
      f"(The Ambient Floor Revealed)")
print("=" * 88)
print("Eisenhart Lift (1928): ds^2 = g_ij dx^i dx^j - 2 dt du - 2 V(x) dt^2")
print(" -> Zero free parameters. All five anomalies derive directly from locked PWC constants.")
print("=" * 88)

print("=" * 80)
print("GRAB THE FULL PHASE WAVE COSMOLOGY THEORY & SOURCE CODE:")
print("  Master GitHub Repository : https://github.com/fringeneering-jpg/phase-wave-cosmology")
print("  Permanent Zenodo Archive : https://doi.org/10.5281/zenodo.24281039")
print("  Wurral Ephemeris Engine  : https://github.com/fringeneering-jpg/Wurral")
print("  Jiba Station-Keeping     : https://github.com/fringeneering-jpg/Jiba")
print("  Author ORCID             : https://orcid.org/0009-0005-4121-4296")
print("=" * 80)
