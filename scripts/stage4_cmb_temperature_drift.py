#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stage4_cmb_temperature_drift.py - the stage-4 T_CMB(z) cold-drift falsifier for
the D47 (the Elephant) endothermic read (2026-10-21, Australia/Perth).

THE FRAMEWORK'S CLAIM (papers/PHASE_WAVE_COSMOLOGY_DERIVATIONS.md D47, lines
883-900; capture/2026-10-21_the_elephant.md; briefs/ARGON_BRIEF_HEAT_LAW_2026-10-21.md):
  the untying absorbs heat (the thaw draws L = c0^2 back per kg), so the T_CMB(z)
  curve should drift COLD from the pure adiabatic T0(1+z) line, and the framework's
  wall-vs-volume H0 split predicts the drift's sign and size family:
    dT_CMB/dt = -H*T_CMB = -0.206 K/Gyr (wall H0 = 73.935) to -0.188 K/Gyr
    (Planck H0 ~ 67.4) at z~0   (predictions/FALSIFIABLE_CATALOG.md row 6; row 52).

RULES: ZERO fitted parameters (every number from the locked set or a cited
measurement, each with its provenance). Kill conditions pre-stated. Misses are
reported, never hidden. Exit code 0 (a falsifier reports; it does not crash).

CROSS-REFS: scripts/quantify_cmb_web.py (the same two measurements, verified
2026-10-21); scripts/entropy_heat_drop_track.py (the -4H*Q heat-drop ledger);
scripts/heat_tying_expansion_ledger.py (L = c0^2 per kg, both sides);
audit/PILLAR2_HEAT_LAW_AUDIT.md (candidate (b): "not discriminating - keep as
consistency ledger only"); predictions/FALSIFIABLE_CATALOG.md row 6 (armed).
No paper is edited by this script.
"""
import sys
import math
import datetime
import numpy as np
from scipy.integrate import quad

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ LOCKED --
# Every number below is locked or measured; nothing here is fitted or free.
LOCK = {
    "c0":       2.99792458e8,     # MEASURED (SI exact) - the thaw's currency L = c0^2 J/kg
    "rho0":     8.74e-27,         # LOCKED (ledger median density, kg/m^3) - the dilution anchor
    "rho_max":  1.29032e15,       # DERIVED (D46 ceiling; GW150914 shell read 1.304e15)
    "s":        1.0 / 19.0,       # LOCKED (debt share)
    "Y_bow":    5.9307e26,        # LOCKED
    "n":        2.0 / 33.0,       # LOCKED (EOS shape)
    "f_solid":  8.4989e-4,        # LOCKED (solid/tied fraction)
    "T":        27.0,             # LOCKED (3^3 tightening)
    "tempo":    28.0 / 19.0,      # LOCKED = s(1+T) = 1.473684
    "G":        6.67430e-11,      # MEASURED (CODATA)
    "hbar":     1.054571817e-34,  # MEASURED (CODATA)
    "kB":       1.380649e-23,     # MEASURED (SI exact)
    "Q_CMB":    4.175e-14,        # DERIVED (a*T_CMB^4; recomputed below)
    "T_CMB":    2.7255,           # LOCKED = FIRAS 2.72548 +/- 0.00057 K (the bath)
    "H0_wall":  73.935,           # LOCKED (wall clock, km/s/Mpc)
    "H0_planck": 67.36,           # MEASURED (Planck 2018)
}

MPC_M = 3.0856775814913673e22     # m per Mpc (IAU)
GYR_S = 3.15576e16                # s per Gyr

# ------------------------------------------------ embedded measurements ----
# (MEASURED; embedded per the task - no API, the same rows already verified in
#  scripts/quantify_cmb_web.py this session.)
MEAS = [
    dict(name="Muller+2013", ref="A&A 551 A109 (arXiv:1212.5456)",
         z=0.89, T=5.08, e_lo=0.10, e_hi=0.10,          # symmetric +/- 0.10 K
         note="SZ + CO excitation, COSMOS field"),
    dict(name="Riechers+2022", ref="Nature 602 58 (arXiv:2202.00693)",
         z=6.34, T=20.6, e_lo=4.2, e_hi=9.6,            # 1sigma [16.4, 30.2]
         note="H2O absorption toward quasar P183+05"),
]
# Compilation-level slope read (audit-quoted): beta = d ln[T/(1+z)] / d ln(1+z)
BETA_COMP, SIG_BETA_COMP = 0.007, 0.013   # MEASURED (published SZ/ALMA compilations,
                                          # audit/PILLAR2_HEAT_LAW_AUDIT.md; Saro+2014 et al.)

def H0_si(h0_km):
    """km/s/Mpc -> 1/s."""
    return h0_km * 1e3 / MPC_M

def t_age_gyr(z, h0_km, om=0.315):
    """Age of the universe at redshift z (flat LCDM age map), Gyr.
    STANDARD integral, imported ONLY to place the naive time-axis drift
    candidates and the two-point slope baseline on a time axis - the PWC
    family itself is z-space and needs no age map. Om = 0.315 MEASURED
    (Planck 2018)."""
    h0 = H0_si(h0_km)
    omr = 4.1835e-5 / (h0_km / 100.0) ** 2
    oml = 1.0 - om - omr
    f = lambda zp: 1.0 / ((1.0 + zp) * h0 * np.sqrt(om * (1 + zp) ** 3
                                                     + omr * (1 + zp) ** 4 + oml))
    val, _ = quad(f, z, 2.0e4, limit=200)
    return val / GYR_S

def t_lb_gyr(z, h0_km):
    """Lookback time to redshift z, Gyr."""
    return t_age_gyr(0.0, h0_km) - t_age_gyr(z, h0_km)

c0  = LOCK["c0"]
T0  = LOCK["T_CMB"]
Q0  = LOCK["Q_CMB"]
Hw  = H0_si(LOCK["H0_wall"])
Hp  = H0_si(LOCK["H0_planck"])

# bath radiation constant from the locked pieces (a = pi^2 kB^4 / 15 hbar^3 c0^3)
a_rad  = np.pi**2 * LOCK["kB"]**4 / (15.0 * LOCK["hbar"]**3 * c0**3)
Q_re   = a_rad * T0**4                                   # J/m^3 recompute
q_resid = (Q_re - Q0) / Q0 * 100.0                       # % vs locked Q_CMB

# the drift band at z~0: dT/dt = -H*T0, the two locked clocks
rate_wall   = -Hw * T0 * GYR_S                           # K/Gyr
rate_planck = -Hp * T0 * GYR_S                           # K/Gyr
band_w      = abs(rate_wall - rate_planck)               # K/Gyr width
split_pct   = (LOCK["H0_wall"] / LOCK["H0_planck"] - 1.0) * 100.0

# lookback times under both clocks (for the naive candidates / slope baseline)
lb = {}
for tag, h0 in (("wall", LOCK["H0_wall"]), ("planck", LOCK["H0_planck"])):
    lb[tag] = {m["z"]: t_lb_gyr(m["z"], h0) for m in MEAS}
    lb[tag][0.0] = t_lb_gyr(0.0, h0)

print("=" * 100)
print("STAGE 4 - THE D47 (ELEPHANT) ENDOTHERMIC T_CMB(z) COLD-DRIFT FALSIFIER")
print("=" * 100)
print("run:", datetime.datetime.now().isoformat(timespec="seconds"))
print("rules: ZERO fitted parameters | provenance per number | kill conditions")
print("pre-stated | misses reported, never hidden | exit 0")
print()

print("#" * 100)
print("0. KILL CONDITIONS, PRE-STATED (frozen before the data are read)")
print("#" * 100)
print("K1 (adiabatic line): any point with |T_meas - T0(1+z)| > 3 sigma_T kills")
print("    the pure adiabatic line T0(1+z).")
print("K2 (PWC family):     the PWC drift family survives ONLY if every point lands")
print("    inside it (the 3-sigma corridor of its z-space curve, below).")
print("K3 (drift band):     a dT/dt at z~0 outside [%.4f, %.4f] K/Gyr excludes the"
      % (rate_wall, rate_planck))
print("    band's content (catalog row 6: the band's own H0 span [%.2f, %.2f] km/s/Mpc)."
      % (LOCK["H0_planck"], LOCK["H0_wall"]))
print("K4 (naive drifts):   the literal constant-rate and constant-H exponential")
print("    cold-drift curves (built from the same locked pieces) are scored against")
print("    the same two points; if dead, they die loudly, not silently.")
print("K5 (compilation):    the published SZ/ALMA compilation beta = %.3f +/- %.3f:"
      % (BETA_COMP, SIG_BETA_COMP))
print("    a beta != 0 at >= 3 sigma breaks adiabaticity (row 6's own kill).")
print()

print("#" * 100)
print("1. THE PREDICTED FAMILY: T(z) = T0(1+z)[1 - epsilon(z)]")
print("#" * 100)
print("The endothermic epsilon(z) is built from the LOCKED pieces only. Which pieces")
print("and why (no free parameters - each entry states its role):")
print()
print("  L = c0^2 J/kg       c0 = 2.99792458e8 (MEASURED, SI exact) is the thaw's")
print("                      currency: the untying of one kg absorbs exactly L back")
print("                      (heat_tying_expansion_ledger.py - the circle's two sides).")
print("  Q_CMB, T_CMB        the bath the draw is paid from (Q_CMB = %.3e J/m^3,"
      % Q0)
print("                      T_CMB = %.4f K LOCKED = FIRAS; a = pi^2 kB^4/15 hbar^3 c0^3"
      % T0)
print("                      recomputes Q = %.4e J/m^3, %+.3f%% vs locked - kB, hbar"
      % (Q_re, q_resid))
print("                      MEASURED, c0 MEASURED).")
print("  H0_wall = 73.935     LOCKED (wall clock) and H0_planck = 67.36 (MEASURED,")
print("  H0_planck = 67.36    Planck 2018): the two drift rates - the family's sign")
print("                      (colder) and size family (the band below).")
print("  rho0 = 8.74e-27      LOCKED: the dilution/redshift law (1+z) =")
print("                      (rho_emit/rho_obs)^(1/3) anchors the z-space shape.")
print("  s = 1/19             LOCKED: the debt-share bookkeeping that identifies the")
print("                      bath's heat drop WITH the thaw's draw (below).")
print("  NOT used and why:   rho_max, Y_bow, n, f_solid set the knot-side (tying)")
print("                      physics, not the bath's cooling; T = 27 and 28/19 are the")
print("                      tempo, not the heat ledger - they do not enter epsilon.")
print()
print("THE -4H*Q IDENTITY (the framework's own locked bookkeeping):")
print("  the bath's heat drop is Q_dot = -4H*Q (T ~ rho^(1/3) -> d ln Q/dt = -4H), and")
print("  the framework books this drop AS the thaw's draw: 'the heat that leaves the")
print("  bath is the thaw's draw (the circle's return leg)' - entropy_heat_drop_track.py")
print("  lines 34-50. The endothermic sink and the adiabatic dilution are ONE channel,")
print("  not two. Hence dT/dt = -H*T and, with the locked redshift law, the z-space")
print("  curve is EXACTLY the adiabatic line:")
print()
print("  T_PWC(z) = T0(1+z),   epsilon(z) = 0 for every z   (both family members)")
print()
print("THE WALL-VS-VOLUME SPLIT (the drift's sign and size family):")
print("  dT/dt(z=0) = -H*T0 = %+.5f K/Gyr (wall, 73.935) .. %+.5f K/Gyr (Planck, 67.36)"
      % (rate_wall, rate_planck))
print("  sign: COLD (negative). size: the band width %.5f K/Gyr = the %.2f%% H0 split."
      % (band_w, split_pct))
print("  (the -0.188/-0.206 labels: -0.1879 at the catalog's rounded H0 = 67.4.)")
print("  The two members coincide in z-space; the split lives on the TIME axis only -")
print("  at a fixed past time the wall member sits warmer by %.5f K per Gyr of"
      % band_w)
print("  lookback. A (z, T) measurement cannot see the split (the audit's 'identity').")
print()
print("THE TWO NONZERO COLD-DRIFT CANDIDATES THE SAME PIECES SUGGEST (scored, not")
print("hidden - if one insists the endothermic draw displaces T(z) from the line, the")
print("locked pieces give exactly these two literal readings):")
print("  (a) constant-rate : T_cr(z)  = T0 - H*T0*t_lb(z)   ->  epsilon_cr(z) = 1 - (1 - H*t_lb(z))/(1+z)")
print("  (b) constant-H    : T_exp(z) = T0*exp(-H*t_lb(z))  ->  epsilon_exp(z) = 1 - exp(-H*t_lb(z))/(1+z)")
print("  (H = the locked H0; t_lb from the standard age map - the only imported piece.)")
print()

# ------------------------------------------------------------ the residuals --
print("#" * 100)
print("2. THE MEASUREMENTS (embedded, MEASURED) AND THEIR RESIDUALS")
print("#" * 100)
print("  adiabatic line values:  T0(1+z) = %.4f K at z=0.89 ; %.4f K at z=6.34"
      % (T0 * 1.89, T0 * 7.34))
print("  (framework anchor at the LSS, informational: T0*1101 = %.1f K vs the ~3000 K"
      % (T0 * 1101.0))
print("  decoupling temperature - the same dilution law at z* = 1100.)")
print()
print("  %-14s %5s %9s %10s %10s %9s %8s %10s" % (
    "point", "z", "T_meas (K)", "T_line (K)", "dT (K)", "sigma", "beta", "in family?"))
print("  " + "-" * 88)
sig_max = 0.0
for m in MEAS:
    z, Tm = m["z"], m["T"]
    Tline = T0 * (1.0 + z)
    dT = Tm - Tline
    e = m["e_lo"]        # lower 1-sigma error (adverse side for the significance read)
    sig = dT / e
    sig_max = max(sig_max, abs(sig))
    beta = 1.0 - math.log(Tm / T0) / math.log(1.0 + z)
    beta_sig = e / (Tm * math.log(1.0 + z))
    inside = abs(sig) <= 3.0
    print("  %-14s %5.2f %9.2f %10.4f %+10.4f %+9.2f %+8.3f %10s" % (
        m["name"], z, Tm, Tline, dT, sig, beta, "YES" if inside else "NO"))
    print("    %-13s %s" % ("", m["ref"] + " - " + m["note"]))
    if m["e_hi"] != m["e_lo"]:
        print("    %-13s %s" % ("", "asymmetric 1sigma [%.1f, %.1f]: beta sigma %.3f (lower side)"
                              % (Tm - m["e_lo"], Tm + m["e_hi"], beta_sig)))
    else:
        print("    %-13s %s" % ("", "symmetric sigma: beta sigma %.3f" % beta_sig))
print()
print("  beta = 1 - ln(T/T0)/ln(1+z);  beta = 0 <=> adiabatic (row 6's parameter).")
print("  compilation-level read (audit): beta = %.3f +/- %.3f -> +%.2f sigma, consistent"
      % (BETA_COMP, SIG_BETA_COMP, BETA_COMP / SIG_BETA_COMP))
print()

# ------------------------------ naive candidates vs the two measurements ------
print("  K4 - THE NAIVE NONZERO DRIFT CANDIDATES (the rate is nearly H0-independent")
print("       because H*t_lb is nearly constant - printed for both clocks):")
print("  %-10s %5s %11s %10s %9s %9s %10s" % ("clock", "z", "T_cr (K)", "T_exp (K)",
                                             "sig_cr", "sig_exp", "verdict"))
print("  " + "-" * 84)
for tag in ("wall", "planck"):
    for m in MEAS:
        z, Tm, e = m["z"], m["T"], m["e_lo"]
        tlb = lb[tag][z] * GYR_S                       # seconds
        H = Hw if tag == "wall" else Hp
        T_cr = T0 - H * T0 * tlb
        T_exp = T0 * math.exp(-H * tlb)
        s_cr = (T_cr - Tm) / e
        s_exp = (T_exp - Tm) / e
        print("  %-10s %5.2f %11.4f %10.4f %+9.1f %+9.1f %10s" % (
            tag, z, T_cr, T_exp, s_cr, s_exp,
            "KILLED" if abs(s_cr) > 3 and abs(s_exp) > 3 else "?"))
print("  verdict: BOTH naive cold-drift curves are dead at BOTH points - the")
print("  endothermic read cannot displace T(z) from the line at the locked rates;")
print("  the only surviving zero-parameter family member is epsilon(z) = 0.")
print()

# --------------------------- two-point slope (consistency, not the band test) --
tlw = lb["wall"]
slope_meas = (MEAS[0]["T"] - MEAS[1]["T"]) / (tlw[MEAS[0]["z"]] - tlw[MEAS[1]["z"]])
slope_line = (T0 * 1.89 - T0 * 7.34) / (tlw[0.89] - tlw[6.34])
e_slope = math.sqrt(MEAS[0]["e_lo"] ** 2 + MEAS[1]["e_lo"] ** 2) / abs(tlw[0.89] - tlw[6.34])
sig_slope = (slope_meas - slope_line) / e_slope
print("  two-point slope check (wall age map, baseline %.3f Gyr): measured %+.3f vs"
      % (abs(tlw[0.89] - tlw[6.34]), slope_meas))
print("  line %+.3f K/Gyr, error %.3f -> %+.2f sigma. This is a consistency check of"
      % (slope_line, e_slope, sig_slope))
print("  the LINE, not a test of the z~0 band (the band is a local rate).")
print()

print("#" * 100)
print("3. KILL VERDICTS (against the pre-stated kills)")
print("#" * 100)
print("  K1 adiabatic line:  max |sigma| = %.2f < 3 -> NO KILL. The pure adiabatic"
      % sig_max)
print("      line T0(1+z) SURVIVES the two points.")
print("  K2 PWC family:      epsilon(z) = 0 -> the family IS the line; both points")
print("      land inside its 3-sigma corridor -> the PWC drift family SURVIVES")
print("      (degenerately - the family can only be killed, never confirmed by T(z);")
print("      the audit's 'identity' stands).")
print("  K3 drift band:      NOT TESTABLE by these points. The band (width %.5f K/Gyr)"
      % band_w)
print("      needs dT/dt at z~0 to +/- %.4f K/Gyr (half-width); the two-point slope"
      " error here is %.3f K/Gyr (43x the width), and its baseline mixes z."
      % (band_w / 2.0, e_slope))
print("      The band's own content is the H0 split [%.2f, %.2f] km/s/Mpc - decided"
      % (LOCK["H0_planck"], LOCK["H0_wall"]))
print("      by H0 measurements (SH0ES vs Planck), not by T(z). NOTE (honest arithmetic):")
print("      catalog row 6's phrase 'a dT/dt outside the band excludes H0 <= 69' is")
print("      not supported by the band itself - H0 = 69 gives -%.4f K/Gyr, INSIDE"
      " [%.4f, %.4f]; the band excludes H0 < %.2f or > %.2f. Recorded, not hidden."
      % (H0_si(69.0) * T0 * GYR_S, rate_wall, rate_planck,
         LOCK["H0_planck"], LOCK["H0_wall"]))
print("  K4 naive drifts:    KILLED (see table above - every entry >= 4.6 sigma).")
print("      Recorded as misses of the literal time-axis reading, never hidden.")
print("  K5 compilation:     beta = %.3f +/- %.3f -> +%.2f sigma -> NO KILL."
      % (BETA_COMP, SIG_BETA_COMP, BETA_COMP / SIG_BETA_COMP))
print()

print("#" * 100)
print("4. CURRENT VERDICT AND THE DECIDING MEASUREMENT")
print("#" * 100)
print("  CURRENT VERDICT: the two points CANNOT discriminate. The PWC drift")
print("  (epsilon(z) = 0 in z-space; the cold drift -%.4f..-%.4f K/Gyr lives on the"
      % (abs(rate_planck), abs(rate_wall)))
print("  time axis) sits INSIDE every measurement error: Muller +-0.10 K (1.9% of the")
print("  line) and Riechers +4.2/-9.6 K (20-47% of the line). No kill fires; the")
print("  adiabatic line and the PWC family stand or fall together.")
print()
print("  THE DECIDING MEASUREMENT (predictions/FALSIFIABLE_CATALOG.md row 6, verbatim")
print("  kill): 'A measured beta != 0 in the published SZ/ALMA T(z) compilations")
print("  breaks adiabaticity' - concretely, ONE future point with")
print("      |T_meas - T0(1+z)| > 3 sigma_T")
print("  kills the pure adiabatic line AND the PWC family together (they coincide).")
print("  Arithmetic for the required precision: to 3-sigma-resolve a beta-class")
print("  deviation of |beta| ~ 0.013 (today's compilation error) a future point")
print("  needs sigma_T <= |beta|*T0(1+z)*ln(1+z)/3 = %.3f K at z = 1, %.3f K at z = 2"
      % (BETA_COMP * T0 * 2.0 * math.log(2.0) / 3.0,
         BETA_COMP * T0 * 3.0 * math.log(3.0) / 3.0))
print("  (SPT-3G/ACT cluster T(z) points at z~1-2, or a second ALMA z>4 point, are")
print("  the named data routes in row 6). The band's own content (wall 73.935 vs")
print("  Planck 67.36) is decided by the H0 measurement itself, not by T(z): a dT/dt")
print("  at z~0 to +/- %.1f mK/Gyr (the audit's ~2e-11 K/yr) is unreachable on Gyr"
      % (band_w / 2.0 * 1e3))
print("  baselines by any planned program.")
print()
print("  HONEST STATUS: as the PILLAR2 audit already ruled, the PWC T(z) curve is")
print("  degenerate with LCDM (the same T0(1+z) line) - this falsifier can kill the")
print("  framework on beta != 0 but can never distinguish it from standard cosmology")
print("  on T(z) alone. Consistency-ledger row, armed kill.")
print()
print("=" * 100)
print("MISSES / HONEST NOTES KEPT VISIBLE: (1) the naive constant-rate and exponential")
print("cold-drift curves are dead (>= 4.6 sigma); (2) row 6's 'excludes H0 <= 69'")
print("does not follow from the band's own arithmetic (H0 = 69 -> %+.4f K/Gyr is"
      % (H0_si(69.0) * T0 * GYR_S))
print("inside it); (3) epsilon(z) = 0 makes the family identical to the adiabatic")
print("line - a kill-only, never a confirmation.")
print("=" * 100)
print("FALSIFIER EXIT: verdict computed, exit code 0 (no kill fired this run).")
sys.exit(0)
