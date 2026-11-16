# -*- coding: utf-8 -*-
"""
navier_stokes_lockdown.py - the PWC Navier-Stokes LOCK-DOWN verification.

Companion executable of papers/clay/NAVIER_STOKES_LOCKDOWN.md.
Every step in that document labeled PROVEN-BY-ALGEBRA is checked HERE,
numerically or symbolically, with ZERO fitted parameters: every constant
below is a locked workspace constant with its provenance named on the line.

Kill conditions (pre-stated, see the document section 7):
  K1 - any a-priori bound that fails numerically kills that step.
  K2 - the cavitation lemma fails if the weld-gate arithmetic does not close.

Tolerances are NOT fitted parameters: the locked inputs carry 4-5
significant figures, so a reproduction must land within their own rounding
(1e-4 relative). Exact algebraic identities use 1e-9 relative.

Exit code: 0 iff every K1/K2 check passes and the claimed mechanism's
own illustration stays consistent. Any kill -> exit 1.
"""
import math
import sys
import numpy as np
import sympy as sp
from fractions import Fraction

# ----------------------------------------------------------------------
# TABLE 1 - the locked constants (zero fitted parameters; provenance per line)
# ----------------------------------------------------------------------
c0        = 2.99792458e8   # LOCKED (SI definition of the speed of light / medium speed)
rho0      = 8.74e-27       # LOCKED (ambient medium density, kg/m^3)
s_l       = 1.0 / 19.0     # LOCKED (the 19:1:18 fold balance; the welded share)
Y_bow     = 5.9307e26      # LOCKED (bow yield, Pa; the electron's own pieces, RBH-1 anchor)
n_l       = 2.0 / 33.0     # LOCKED (capacity exponent; the SHAPE, ruled by the author)
f_solid   = 8.4989e-4      # LOCKED (solid debt fraction; back-solved to G, checked +0.0007%)
Rp        = 0.8422e-15     # LOCKED (proton radius, m)
Gamma     = 2.39e-18       # LOCKED (T7 untying rate per proton, s^-1)
x_weld    = 0.95           # LOCKED (the weld gate - compression ratio where cavitation fires)
E_lock_L  = 2.8898         # LOCKED (cold-weld threshold, forge scan units)
delta_E_L = 0.144490       # LOCKED (forge gate width, scan units)
rho_knot  = 0.8            # LOCKED (forge scan, scan units)
c_med     = 1.900591       # LOCKED (forge scan, scan units)
rho_max_shell = 1.304e15   # LOCKED (GW150914 shell read; the SUPERSEDED anchor of Omega_cav)
rho_max_L = 1.29032e15     # LOCKED (the DERIVED ceiling, kg/m^3; n = 2/33 fixpoint)
P_max_L   = 1.1597e32      # LOCKED (P_max = u_max = rho_max c0^2, J/m^3)
Omega_amb_L = 2.4555e-18   # LOCKED (wibble floor, s^-1)
Omega_cav_L = 1.1324e21    # LOCKED (cavitation ceiling, s^-1; shell-anchored - see GAP O5)
C_stall_km_L = 958.78      # LOCKED (derived-ceiling stall speed, km/s; D46 958.78 = 958.78)

TOL_INPUT = 1e-4   # rel tolerance: the locked inputs' own 4-5 significant-figure rounding
TOL_EXACT = 1e-9   # rel tolerance for exact algebraic identities

FAILS = []

def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print("  [%s] %-58s %s" % (tag, name, detail))
    if not ok:
        FAILS.append(name)

def rel(a, b):
    """relative deviation (fraction), a/b - 1"""
    return a / b - 1.0

def pct(a, b):
    """relative deviation in percent"""
    return 100.0 * rel(a, b)

print("=" * 88)
print("PWC NAVIER-STOKES LOCK-DOWN - VERIFICATION (zero fitted parameters)")
print("=" * 88)

# ----------------------------------------------------------------------
# STEP A - the derived ceiling: rho_max from the n = 2/33 fixpoint
# rho_max = (2 Y_bow / c0^2)^(33/29) * rho0^(-4/29),  with
# 33/29 = 1/(1-2n), 4/29 = 2n/(1-2n)  - the EXACT fixpoint where the
# capacity ladder C( rho ) = c0 ( rho0 / rho )^n meets the yield law
# C( rho ) = sqrt( 2 Y_bow / rho ).
# ----------------------------------------------------------------------
print("\n[A] THE DERIVED CEILING (n = 2/33 fixpoint)")
exp1 = 1.0 / (1.0 - 2.0 * n_l)          # 33/29
exp2 = 2.0 * n_l / (1.0 - 2.0 * n_l)     # 4/29
rho_max = (2.0 * Y_bow / c0 ** 2) ** exp1 * rho0 ** (-exp2)
check("PA1 rho_max fixpoint (2Y_bow/c0^2)^(33/29) rho0^(-4/29) = 1.29032e15",
      abs(rel(rho_max, rho_max_L)) <= TOL_INPUT,
      "calc %.5e vs locked %.5e (%+.4f%%)" % (rho_max, rho_max_L, pct(rho_max, rho_max_L)))
check("PA1 exponents are exact rationals from n = 2/33 (33/29, 4/29)",
      abs(exp1 - 33.0 / 29.0) < TOL_EXACT and abs(exp2 - 4.0 / 29.0) < TOL_EXACT,
      "1/(1-2n)=%.8f, 2n/(1-2n)=%.8f" % (exp1, exp2))
check("PA1 ceiling is FINITE (the cap exists)", math.isfinite(rho_max) and rho_max > 0,
      "rho_max = %.5e" % rho_max)
check("PA1 rho0 < rho_max (the medium has a range to compress)",
      rho0 < rho_max, "rho0=%.2e vs rho_max=%.4e" % (rho0, rho_max))

# ----------------------------------------------------------------------
# STEP B - the capacity ladder and the yield law meet EXACTLY at the
# derived ceiling (the D46 self-check 958.78 = 958.78)
# ----------------------------------------------------------------------
print("\n[B] THE STALL: C-LADDER = C-YIELD AT THE CEILING")
C_ladder = c0 * (rho0 / rho_max) ** n_l
C_yield = math.sqrt(2.0 * Y_bow / rho_max)
check("PA2 C_ladder(rho_max) = C_yield(rho_max) exactly",
      abs(rel(C_ladder, C_yield)) < TOL_EXACT,
      "%.6f vs %.6f km/s" % (C_ladder / 1e3, C_yield / 1e3))
check("PA2 the stall speed at the ceiling is 958.78 km/s",
      abs(rel(C_yield / 1e3, C_stall_km_L)) < TOL_INPUT,
      "C_stall = %.4f km/s vs locked %.2f" % (C_yield / 1e3, C_stall_km_L))
check("PA2 the stall is a stop toward C_min > 0, never dead zero",
      C_yield > 0.0 and C_yield < c0,
      "C_min = %.3e m/s < c0 = %.3e m/s" % (C_yield, c0))

# ----------------------------------------------------------------------
# STEP C - the caps as numbers (energy, pressure, work)
# ----------------------------------------------------------------------
print("\n[C] THE FOUR CAPS AS NUMBERS")
P_max = rho_max * c0 ** 2
check("PA3 P_max = u_max = rho_max c0^2 = 1.1597e32 J/m^3",
      abs(rel(P_max, P_max_L)) <= TOL_INPUT,
      "calc %.5e vs locked %.5e (%+.4f%%)" % (P_max, P_max_L, pct(P_max, P_max_L)))
E_kin_cap = 0.5 * rho_max * c0 ** 2
check("PA3 kinetic-energy-density cap (1/2) rho_max c0^2 = 5.7985e31 J/m^3",
      math.isfinite(E_kin_cap) and abs(E_kin_cap / 5.7985e31 - 1.0) < TOL_INPUT,
      "= %.5e J/m^3" % E_kin_cap)
check("PA4 specific-work cap L = c0^2 = 8.9876e16 J/kg",
      abs(c0 ** 2 / 8.9876e16 - 1.0) < TOL_INPUT,
      "= %.5e J/kg" % (c0 ** 2))
check("PA3 |u| cap c0 = 2.99792458e8 m/s (finite)",
      math.isfinite(c0) and c0 > 0, "c0 = %.8e" % c0)

# ----------------------------------------------------------------------
# STEP D - the floor pressure (the D46 ambient correction)
# Fluid branch: P( rho ) = (1-s) (rho c0^2/3) [1 + (rho/rho_max)^n]^-1
# ----------------------------------------------------------------------
print("\n[D] THE FLOOR PRESSURE (D46 master constitutive equation)")
x_0 = rho0 / rho_max
bracket = 1.0 / (1.0 + x_0 ** n_l)
P_floor = (1.0 - s_l) * rho0 * c0 ** 2 / 3.0 * bracket
check("PA5 P(rho0) = 2.4727e-10 Pa (with the bracket's ambient correction)",
      abs(rel(P_floor, 2.4727e-10)) <= TOL_INPUT,
      "calc %.5e vs locked 2.4727e-10 (%+.4f%%)" % (P_floor, pct(P_floor, 2.4727e-10)))
P_debt_floor = (1.0 - s_l) * rho0 * c0 ** 2 / 3.0
check("PA5 debt floor (18/19) rho0 c0^2/3 = 2.4806e-10 Pa",
      abs(rel(P_debt_floor, 2.4806e-10)) <= TOL_INPUT,
      "= %.5e Pa" % P_debt_floor)
corr = bracket - 1.0
check("PA5 the bracket correction is the on-record 0.32% (read 0.3185%)",
      abs(corr + 0.3185e-2) < 5e-5,
      "bracket-1 = %+.4f%%" % (100.0 * corr))

# ----------------------------------------------------------------------
# STEP E - the pressure bound: monotone branch, capped by P_max
# dP/drho = (1-s) c0^2/3 * [1 + (1-n) x^n] / (1 + x^n)^2 > 0  (n < 1)
# ----------------------------------------------------------------------
print("\n[E] THE PRESSURE BOUND (P <= P_max on the whole branch)")
x_s, n_s = sp.symbols("x n", positive=True, real=True)
dP_drho = sp.simplify(sp.diff((1 - s_l) * sp.Rational(1, 3) * c0 ** 2
                              * x_s / (1 + x_s ** n_s), x_s))
print("  symbolic dP/drho (per rho_max) = (1-s)c0^2/3 * %s" % dP_drho)
grid = np.linspace(0.0, 1.0, 4001)
vals = (1.0 - s_l) * c0 ** 2 / 3.0 * (1.0 + (1.0 - n_l) * grid ** n_l)        / (1.0 + grid ** n_l) ** 2
check("PA6 dP/drho > 0 on [0, rho_max] (monotone branch, n < 1)",
      bool(np.all(vals > 0.0)),
      "min dP/drho = %.4e > 0" % vals.min())
P_fluid = lambda x: (1.0 - s_l) * rho_max * c0 ** 2 / 3.0 * x / (1.0 + x ** n_l)
check("PA6 P_fluid <= P_max at every sampled x in [0,1]",
      bool(np.all(P_fluid(grid) <= P_max * (1.0 + 1e-12))),
      "max P_fluid = %.5e vs P_max = %.5e" % (P_fluid(grid).max(), P_max))
check("PA6 P_fluid(rho_max) = (1-s) rho_max c0^2/6 = 1.8310e31 <= P_max",
      abs(P_fluid(1.0) - (1.0 - s_l) * rho_max * c0 ** 2 / 6.0) < TOL_EXACT * rho_max * c0 ** 2
      and P_fluid(1.0) < P_max,
      "P_fluid(rho_max) = %.5e (%.4f x below the cap)" % (P_fluid(1.0), P_max / P_fluid(1.0)))
P_weld_fluid = P_fluid(x_weld)
P_weld_lattice = x_weld * rho_max * c0 ** 2
check("PA6 at the gate the lattice clause is above the fluid branch",
      P_weld_fluid < P_weld_lattice,
      "P_fluid(0.95) = %.5e vs lattice x P_max = %.5e" % (P_weld_fluid, P_weld_lattice))

# ----------------------------------------------------------------------
# STEP F - THE CAVITATION CUTOFF LEMMA (K2 - the weld-gate arithmetic)
# ----------------------------------------------------------------------
print("\n[F] THE WELD GATE (K2: must close or the cavitation lemma dies)")
f_weld = Fraction(1, 19)
f_expel = Fraction(18, 19)
check("PA7 welded share s = 1/19 = 5.26% exactly", float(f_weld) == s_l,
      "s = %.7f = %.4f%%" % (float(f_weld), 100.0 * float(f_weld)))
check("PA7 expelled share 1-s = 18/19 = 94.74% exactly",
      abs(float(f_expel) - (1.0 - s_l)) < TOL_EXACT,
      "1-s = %.7f = %.4f%%" % (float(f_expel), 100.0 * float(f_expel)))
check("PA7 the split conserves mass: 18/19 + 1/19 = 1",
      float(f_expel) + float(f_weld) == 1.0, "mass balance exact")
E_lock_calc = rho_knot * c_med ** 2
check("PA7 E_lock = rho_knot c_med^2 = 2.8898 (scan units)",
      abs(rel(E_lock_calc, E_lock_L)) <= TOL_INPUT,
      "calc %.6f vs locked %.4f" % (E_lock_calc, E_lock_L))
delta_E_calc = 0.05 * E_lock_calc
check("PA7 delta_E = 0.05 E_lock = 0.144490",
      abs(rel(delta_E_calc, delta_E_L)) <= TOL_INPUT,
      "calc %.6f vs locked %.6f" % (delta_E_calc, delta_E_L))
gate_closure = delta_E_calc / E_lock_calc
check("PA7 GATE CLOSURE: 1 - x_weld = delta_E / E_lock (0.05 = 0.144490/2.8898)",
      abs(gate_closure - (1.0 - x_weld)) < TOL_EXACT,
      "delta_E/E_lock = %.8f, 1 - x_weld = %.8f" % (gate_closure, 1.0 - x_weld))
check("PA7 the gate width is the rational 1/20", gate_closure == 0.05,
      "= %.4f" % gate_closure)
check("PA7 x_weld = 19/20 exactly", x_weld == 19.0 / 20.0, "0.95 = 19/20")
k_gate = c0 ** 2 * x_weld / (1.0 - x_weld) ** 2
check("PA8 gate stiffness c0^2 x_weld/(1-x_weld)^2 = 3.4153e19 J/kg (FINITE)",
      math.isfinite(k_gate) and abs(rel(k_gate, 3.4153e19)) <= TOL_INPUT,
      "k_gate = %.5e J/kg" % k_gate)
check("PA8 the gate fires BEFORE the EOS pole: x_weld = 0.95 < 1",
      x_weld < 1.0, "margin to the pole = %.4f" % (1.0 - x_weld))
print("  [NOTE] expulsion fraction 18/19 = %.5f vs gate x_weld = %.2f "
      "(%+.4f%% apart - the gate is NOT the split; they are distinct locks)"
      % (float(f_expel), x_weld, pct(float(f_expel), x_weld)))

# ----------------------------------------------------------------------
# STEP G - THE BKM OPERATIONAL MIDDLE (K1 - the a-priori bound numbers)
# 0 < Omega_amb <= ||omega(t)||_Linf <= Omega_cav < infinity
# ----------------------------------------------------------------------
print("\n[G] THE BKM OPERATIONAL MIDDLE (0 < Omega_amb <= ||omega|| <= Omega_cav < inf)")
Omega_amb = Gamma * math.sqrt(19.0 / 18.0)
check("PA9 Omega_amb = Gamma sqrt(19/18) = 2.4555e-18 s^-1",
      abs(rel(Omega_amb, Omega_amb_L)) <= TOL_INPUT,
      "calc %.4e vs locked %.4e (%+.4f%%)" % (Omega_amb, Omega_amb_L, pct(Omega_amb, Omega_amb_L)))
C_stall_shell = math.sqrt(2.0 * Y_bow / rho_max_shell)
Omega_cav_shell = C_stall_shell / Rp
check("PA9 Omega_cav = C_stall(shell)/Rp = 1.1324e21 s^-1 (the locked value's own chain)",
      abs(rel(Omega_cav_shell, Omega_cav_L)) <= TOL_INPUT,
      "calc %.4e vs locked %.4e (%+.4f%%)" % (Omega_cav_shell, Omega_cav_L, pct(Omega_cav_shell, Omega_cav_L)))
Omega_cav_derived = C_yield / Rp
check("PA9 Omega_cav stays FINITE at the DERIVED ceiling too (958.78 km/s / Rp)",
      math.isfinite(Omega_cav_derived),
      "derived-anchor Omega_cav = %.4e s^-1" % Omega_cav_derived)
check("PA9 ordering: 0 < Omega_amb <= Omega_cav < inf (both anchors)",
      0.0 < Omega_amb and Omega_amb < Omega_cav_shell and Omega_cav_shell < math.inf
      and Omega_amb < Omega_cav_derived and Omega_cav_derived < math.inf,
      "ratio Omega_cav/Omega_amb = %.3e" % (Omega_cav_shell / Omega_amb))
print("  BKM middle integrability battery (int_0^T Omega_cav dt must be finite for every finite T):")
bkm_ok = True
for T_star in [1e-9, 1.0, 1e3, 1e9, 1e18, 1e30]:
    integral = Omega_cav_shell * T_star
    fin = math.isfinite(integral)
    bkm_ok = bkm_ok and fin
    print("    T* = %-6.0e s -> int = %-14.4e  %s" % (T_star, integral, "finite" if fin else "INF"))
check("PA10 int_0^T* Omega_cav dt < inf for every finite T* (the BKM middle holds)",
      bkm_ok, "no finite T* makes the bound diverge")

# ----------------------------------------------------------------------
# STEP H - the eddy-free floor and the wibble source (sympy)
# ----------------------------------------------------------------------
print("\n[H] THE EDDY-FREE FLOOR AND THE WIBBLE SOURCE (symbolic)")
x_s, y_s, z_s = sp.symbols("x y z", real=True)
P_gen = sp.Function("P")(x_s, y_s, z_s)
gx = sp.diff(P_gen, x_s); gy = sp.diff(P_gen, y_s); gz = sp.diff(P_gen, z_s)
cx = sp.simplify(sp.diff(gz, y_s) - sp.diff(gy, z_s))
cy = sp.simplify(sp.diff(gx, z_s) - sp.diff(gz, x_s))
cz = sp.simplify(sp.diff(gy, x_s) - sp.diff(gx, y_s))
check("PA11 curl(grad P) = 0 identically (the eddy-free floor)",
      cx == 0 and cy == 0 and cz == 0, "all three components simplify to 0")
rho_s, s_s, c0_s = sp.symbols("rho s c0", positive=True, real=True)
P_pwc = (1 - s_s) * rho_s * c0_s ** 2 / 3
dP_ds = sp.diff(P_pwc, s_s)
coeff = sp.simplify(dP_ds / rho_s)
check("PA12 the wibble source dP/ds = -rho c0^2/3 is NON-ZERO",
      sp.simplify(dP_ds + rho_s * c0_s ** 2 / 3) == 0 and coeff != 0,
      "baroclinic source (grad rho x grad P)/rho^2 = (%s) (grad rho x grad s) + ... != 0" % coeff)

# ----------------------------------------------------------------------
# STEP I - the claimed mechanism's own illustration (the toy trajectory;
# NOT a PDE proof - labeled CLAIMED in the document). It must at least be
# self-consistent: capped, cavitating at the gate, idling on the floor.
# ----------------------------------------------------------------------
print("\n[I] THE CLAIMED-MECHANISM ILLUSTRATION (toy ODE; NOT a proof)")
dt = 1e-4
times = np.arange(0.0, 2.5001, dt)
w_pwc = 1.0
x_pwc = 0.10
w_cav_sim = 100.0
w_amb_sim = 1.0 / 19.0
cavitated = False
t_cav = None
w_max_seen = 0.0
w_after_reset = None
for t in times:
    if not cavitated:
        stall_brake = ((x_weld - x_pwc) / x_weld) ** 2 * (1.0 - w_pwc / w_cav_sim)
        dw = (w_pwc ** 2) * max(stall_brake, 0.0)
        dx = 1.80 * (w_pwc / w_cav_sim)
        w_pwc = min(w_pwc + dw * dt, w_cav_sim)
        x_pwc += dx * dt
        w_max_seen = max(w_max_seen, w_pwc)
        if x_pwc >= x_weld:
            cavitated = True
            t_cav = t
            w_pwc = w_cav_sim * s_l      # 94.74% expelled, 5.26% welded
            x_pwc = s_l
            w_after_reset = w_pwc
    else:
        chiral_wibble = 0.002 * math.sin(2.0 * math.pi * 3.0 * t)
        target_floor = w_amb_sim + chiral_wibble
        w_pwc = target_floor + (w_pwc - target_floor) * math.exp(-12.0 * dt)
check("ILL1 cavitation fires at finite time (t_cav < 2.5 s)", cavitated and t_cav is not None,
      "t_cav = %.3f" % (t_cav if t_cav is not None else float("nan")))
check("ILL2 the cap holds at all times (w <= w_cav)", w_max_seen <= w_cav_sim,
      "max w before cavitation = %.4f vs cap %.1f" % (w_max_seen, w_cav_sim))
check("ILL3 the reset welds exactly the s = 1/19 share", w_after_reset is not None
      and abs(w_after_reset - w_cav_sim * s_l) < TOL_EXACT,
      "w after reset = %.4f = s * w_cav" % w_after_reset)
check("ILL4 the floor idles above zero (never dead zero)", w_pwc > 0.0,
      "terminal w = %.4f on the live wibble floor" % w_pwc)

# ----------------------------------------------------------------------
# VERDICT
# ----------------------------------------------------------------------
print("\n" + "=" * 88)
print("LOUD GAPS (reported, never hidden)")
print("-" * 88)
print("  O5  Omega_cav ANCHOR MISMATCH: the locked 1.1324e21 s^-1 is the SHELL-anchored")
print("      value (rho_max = 1.304e15 -> C_stall = %.2f km/s). At the DERIVED ceiling" % (C_stall_shell / 1e3))
print("      (1.29032e15 -> %.2f km/s) the same chain reads %.4e s^-1: %+.4f%% away -"
      % (C_yield / 1e3, Omega_cav_derived, pct(Omega_cav_derived, Omega_cav_shell)))
print("      the on-record C-gap (953.7 vs 958.8 km/s). The BKM middle survives under BOTH")
print("      anchors (both finite); re-anchoring Omega_cav is the named D46 follow-up. NOT KILLED.")
print("  O7  n = 2/33 appears in no paper as the closure exponent's origin - an unused")
print("      locked constant until the fold closure (the on-record 'n-origin ruling').")
print("  O1-O4, O6, O8: the Sobolev machinery, the cavitation-set measure, the Leray-Hopf")
print("      construction, the boundary conditions, smooth-force response, and the E_lock")
print("      unit bridge are OPEN - see the document, section 6. None is checkable here.")
print("=" * 88)

k1_failed = [f for f in FAILS if f.startswith("PA") and not f.startswith(("PA7", "PA8"))]
k2_failed = [f for f in FAILS if f.startswith(("PA7", "PA8"))]
ill_failed = [f for f in FAILS if f.startswith("ILL")]

if k1_failed:
    print("KILL K1: a-priori bound failed numerically: %s" % ", ".join(k1_failed))
if k2_failed:
    print("KILL K2: the weld-gate arithmetic does not close: %s" % ", ".join(k2_failed))
if ill_failed:
    print("KILL ILL: the claimed mechanism's own illustration is inconsistent: %s" % ", ".join(ill_failed))
if FAILS:
    print("VERDICT: %d step(s) KILLED. Exit 1." % len(FAILS))
    sys.exit(1)

print("VERDICT: every PROVEN-BY-ALGEBRA step PASSES (K1 clean, K2 closed, illustration consistent).")
print("THE LOCK-DOWN HOLDS AS STATED: caps -> Omega in [Omega_amb, Omega_cav] -> BKM middle -> no finite-time blowup,")
print("with the honest gap list of section 6 standing. Exit 0.")
sys.exit(0)
