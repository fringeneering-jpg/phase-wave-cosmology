# -*- coding: utf-8 -*-
"""
pwc_weld_torsion_derivation.py - THE WELD'S TORSIONAL SCALE, DERIVED (round 17)
===============================================================================
Perplexity's 4pi-periodic trial potential + Google's execution path:
  U(q) = U0 [1 - cos(q/2)] - T_drive q,
  eta = 2 T_drive / U0,   barrier  dU = 2 U0 [sqrt(1-eta^2) - eta arccos(eta)].
Execution:
  1. U0 = the topological restoring force's work over the 720-degree loop.
     F_top = 60 pi^4 Y_bow r_e^2 = (18/19) F_EM   (the framework's locked identity).
     Work over half a Compton wavelength:  U0 = F_top * (lambda_C / 2).
  2. eta = 1/19  (the exposed thread's geometric debt fraction).
  3. dU = the torsional activation energy.
"""
import math

C0     = 2.99792458e8
M_E    = 9.1093837015e-31
H      = 6.62607015e-34
H_BAR  = H / (2.0 * math.pi)
Y_BOW  = 5.9307e26
ALPHA  = 7.2973525693e-3
R_E    = 2.8179e-15
LAM_C  = H / (M_E * C0)
R_LOOP = LAM_C / (4.0 * math.pi)
RHO_MAX = 1.29032e15
RHO0   = 8.74e-27
L      = (H / (RHO_MAX * C0)) ** (1.0 / 4.0)  # the framework's characteristic length (h, not h-bar)
E0     = RHO_MAX * L ** 3 * C0 ** 2
E_LOCK = 2.8898 * E0
KEV    = 1.602176634e-13  # J per MeV

def mev(j):
    return j / KEV

print("=" * 108)
print("THE WELD'S TORSIONAL SCALE - DERIVATION-SHAPED (2026-10-30, round 17)")
print("=" * 108)

# ===========================================================================
print("\n[STEP 1] U0 from the topological force over the 720-degree loop")
# ===========================================================================
f_em  = (1.602176634e-19) ** 2 / (4.0 * math.pi * 8.8541878128e-12 * R_E ** 2)
f_top = 60.0 * math.pi ** 4 * Y_BOW * R_E ** 2
print(f"  F_EM = e^2/(4 pi eps0 r_e^2) = {f_em:.4f} N")
print(f"  F_top = 60 pi^4 Y_bow r_e^2 = {f_top:.4f} N   (ratio {f_top/f_em:.6f} = 18/19)")
print(f"  Loop radius (Williamson-van der Mark): R = lambda_C/4pi = {R_LOOP*1e15:.4f} fm")
u0 = f_top * (LAM_C / 2.0)
u0_form = (18.0 / 19.0) * (math.pi / ALPHA) * M_E * C0 ** 2
print(f"  U0 = F_top x (lambda_C/2) = {u0:.4e} J = {mev(u0):.4f} MeV")
print(f"  Closed form: U0 = (18/19)(pi/alpha) m_e c0^2 = {mev(u0_form):.4f} MeV   ({100*(u0/u0_form-1):+.3f}%)")
print(f"  -> U0/m_e c0^2 = (18/19)(pi/alpha) = {u0/(M_E*C0**2):.4f}")
print(f"  Cross-check vs E0: U0/E0 = {u0/E0:.5f}   (E0 = {mev(E0):.4f} MeV)")

# ===========================================================================
print("\n[STEP 2] eta = 1/19 and the barrier")
# ===========================================================================
eta = 1.0 / 19.0
bracket = math.sqrt(1.0 - eta ** 2) - eta * math.acos(eta)
dU = 2.0 * u0 * bracket
print(f"  eta = 1/19 = {eta:.6f}")
print(f"  bracket = sqrt(1-eta^2) - eta arccos(eta) = {bracket:.7f}")
print(f"  dU = 2 U0 x bracket = {mev(dU):.4f} MeV")

# ===========================================================================
print("\n[STEP 3] The comparison the framework's own weld scale")
# ===========================================================================
ratio = dU / E_LOCK
print(f"  E_lock = 2.8898 E0 = {mev(E_LOCK):.4f} MeV")
print(f"  dU / E_lock = {ratio:.6f}")
print(f"  11/16 = {11.0/16.0:.6f}   (11 = the relief numerator, 16 = the clock)")
print(f"  -> off by {100*(ratio/(11.0/16.0)-1):+.3f}%")
print("  VERDICT: dU = 2 (18/19)(pi/alpha) m_e c0^2 [sqrt(1-eta^2) - eta arccos(eta)] with")
print("  eta = 1/19 is a DERIVATION-SHAPED barrier: every factor is a locked framework")
print("  quantity. The near-identity dU ~ (11/16) E_lock (+0.02%) is printed as a")
print("  CANDIDATE (named integers, no mechanism for the exact equality yet).")

# ===========================================================================
print("\n[STEP 4] The rate - what remains after the barrier is shaped")
# ===========================================================================
rho_med = (12.0 / 11.0) ** 2 * (2.0 * Y_BOW / C0 ** 2)
D = (RHO0 / rho_med) ** (1.0 / 3.0)
nu_c = M_E * C0 ** 2 / H
f_obs = D * (11.0 / 12.0) * nu_c
kbt_loc = H_BAR * nu_c * D
t_loc = kbt_loc / 1.380649e-23
print(f"  Observer attempt clock: f = D (11/12) nu_C = {f_obs:.4e} Hz")
print(f"  Thermal route: T_local = {t_loc*1e3:.3f} mK -> exp(-dU/k_B T_local) = 0 (frozen)")
print("  -> the escape is the ramp (eta(t) -> 1) or tunneling; the barrier's MAGNITUDE")
print("     is now derivation-shaped, and the rate needs ONE more piece: either the")
print("     ramp law d(eta)/dt from the drive, or the tunneling prefactor I_eff (the")
print("     weld's twist inertia) for the WKB rate. Both named, neither fitted.")

print("\n" + "=" * 108)
print("RESULT OF THE EXECUTION")
print("=" * 108)
print("  U0 = (18/19)(pi/alpha) m_e c0^2 = 208.42 MeV  [F_top x lambda_C/2, derived]")
print("  eta = 1/19  ->  dU = 382.98 MeV  [the torsional activation energy]")
print("  dU / E_lock = 0.6877 ~ 11/16 (+0.02%)  [CANDIDATE: relief numerator x clock]")
print("  Rate: the barrier is shaped; the ramp law (or the tunneling inertia) is the")
print("  single remaining machine -> tau_n, then annihilation, then the neutrino tie.")
print("=" * 108)
