#!/usr/bin/env python3
"""
quantify_cmb_web.py — PWC CMB & cosmic-web falsifiable scoreboard (2026-10-21)
================================================================================
RULES: ZERO fitted parameters. Provenance per number (DERIVED / MEASURED /
VERIFIED / BACK-SOLVED / CLAIMED / OPEN). Misses reported, never hidden.
Kill condition per candidate. Locked constants only for the PWC side.

Workspace cross-refs: papers/PHASE_WAVE_COSMOLOGY_DERIVATIONS.md (D14/D30/D31/D42),
papers/subsectors/COSMOLOGY_ASTROPHYSICS.md, scripts/t27_cubic_tempo_closed.py,
scripts/effective_drag_closure.py, scripts/quantify_universe_census_ledger.md,
scripts/stage4_wall_void_y_contrast.py (run this session), audit/PILLAR2_HEAT_LAW_AUDIT.md
(F1/F3), audit/OPEN_ITEMS_LEDGER.md (A1/P2-A, C4, C9).

External measurements verified this session:
  Muller+2013 A&A 551 A109 (arXiv:1212.5456)   : T_CMB(z=0.89) = 5.08 +/- 0.10 K
  Riechers+2022 Nature 602 58 (arXiv:2202.00693): T_CMB(z=6.34) = 20.6 K, 1sigma [16.4, 30.2]
  DES Y6 (arXiv:2601.14559)                     : S8 = 0.789 +/- 0.012
  Planck 2018 (TT,TE,EE+lowE)                   : S8 = 0.832 +/- 0.013
  Combined CMB 2026 review (arXiv:2602.12238)   : S8 = 0.836 +0.012/-0.013
  Planck 2018 TT                                : first peak l1 = 220.0 +/- 0.5
  Planck 2018                                   : z* = 1089.92 +/- 0.25; t* ~ 377.7 kyr
  FIRAS (Fixsen 2009)                           : T0 = 2.72548 +/- 0.00057 K
  Planck 2018                                   : CMB dipole 3.3621 +/- 0.0010 mK
  Bowman+2018 (EDGES)                           : T21 = -500 mK (+200/-500, 99% CL) at z~17
  Singh+2022 (SARAS 3)                          : rejects EDGES best-fit profile at >95% CL
"""
import sys
import textwrap
import numpy as np
from scipy.integrate import quad

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ LOCKED --
LOCK = {
    "c0":      2.99792458e8,      # MEASURED (SI exact)
    "rho0":    8.74e-27,          # LOCKED  (ledger median density, kg/m^3)
    "rho_max": 1.29032e15,        # DERIVED (shell 1.304e15)
    "s":       1.0 / 19.0,        # LOCKED  (debt share)
    "Y_bow":   5.9307e26,         # LOCKED
    "n":       2.0 / 33.0,        # LOCKED
    "f_solid": 8.4989e-4,         # LOCKED  (solid/tied fraction)
    "T":       27.0,              # LOCKED  (3^3 tightening)
    "tempo":   28.0 / 19.0,       # LOCKED  = s(1+T) = 1.473684
    "alpha":   1.0 / 137.035999084,  # MEASURED (CODATA)
    "m_p":     938.272088,        # MEASURED (CODATA, MeV)
    "G":       6.67430e-11,       # MEASURED (CODATA)
    "hbar":    1.054571817e-34,   # MEASURED (CODATA)
    "kB":      1.380649e-23,      # MEASURED (SI exact)
    "Q_CMB":   4.175e-14,         # DERIVED (a*T_CMB^4; recompute below)
    "T_CMB":   2.7255,            # LOCKED = FIRAS 2.72548+/-0.00057 K (bath)
    "H0_wall": 73.935,            # LOCKED  (wall clock, km/s/Mpc)
    "H0_planck": 67.36,           # MEASURED (Planck 2018)
    "k":       3069.87,           # LOCKED  (unshielded tariff)
    "dRho_geom": 0.24313,         # LOCKED  (geometric decompression boost, papers)
}

MPC_M = 3.0856775814913673e22     # m per Mpc
YR_S  = 3.15576e16                # s per Gyr
KYR_S = 3.15576e10                # s per kyr

def H0_si(H0_km):
    """km/s/Mpc -> 1/s."""
    return H0_km * 1e3 / MPC_M

def t_age_gyr(z, H0_km, Om=0.3166):
    """Age of the universe at redshift z (flat LCDM), Gyr. No fitting: standard integral."""
    H0 = H0_si(H0_km)
    Or = 4.1835e-5 / (H0_km / 100.0) ** 2
    Ol = 1.0 - Om - Or
    f = lambda zp: 1.0 / ((1.0 + zp) * H0 * np.sqrt(Om * (1 + zp) ** 3 + Or * (1 + zp) ** 4 + Ol))
    val, _ = quad(f, z, 2.0e4, limit=200)
    return val / YR_S

# ------------------------------------------------ zero-fit derived helpers --
a_rad = np.pi**2 * LOCK["kB"]**4 / (15.0 * LOCK["hbar"]**3 * LOCK["c0"]**3)
Q_cmb_re = a_rad * LOCK["T_CMB"]**4                       # J/m^3 recompute
T_tempo  = LOCK["s"] * (1.0 + LOCK["T"])                  # 28/19
t_pwc    = 380.0 / T_tempo                                # kyr
H_wall_gyr  = H0_si(LOCK["H0_wall"])    * YR_S            # 1/Gyr
H_planck_gyr = H0_si(LOCK["H0_planck"]) * YR_S
slope_wall   = -H_wall_gyr    * LOCK["T_CMB"]             # K/Gyr (z=0)
slope_planck = -H_planck_gyr  * LOCK["T_CMB"]

# tempo sensitivity: replace rounded 380 kyr by the true Planck t*
t_star_planck = 377.7                                     # kyr (Planck 2015 XIII: 377.6+/-3.2)
ratio_fixed   = t_star_planck / 258.0
tempo_resid_fixed = (T_tempo / ratio_fixed - 1.0) * 100.0 # +0.66%

# audit F3/C4 cross-check: t(z) at candidate epochs (Planck 2018 best-fit)
t_zstar = t_age_gyr(1089.92, LOCK["H0_planck"], 0.3166) * 1e6   # Gyr -> kyr
t_zdrag = t_age_gyr(1059.94, LOCK["H0_planck"], 0.3166) * 1e6
t_z1350 = t_age_gyr(1350.00, LOCK["H0_planck"], 0.3166) * 1e6

# D30 chain: l1 = 219.0  (effective_drag_closure.py, in-paper inputs)
ell_free = 179.5
H0_cal   = 32.371
paid     = 1.0 - (H0_cal - np.log(1101.0)) / H0_cal
f_lss    = 0.05 / (1.0 - paid)
R_bare   = 3.0 * f_lss / (4.0 * (1.0 - f_lss))
R_eff    = 21.0 * R_bare
l1_pwc   = ell_free * (R_eff / (2.0 * (np.sqrt(1.0 + R_eff) - 1.0)))

# T(z) standard line vs measured points
T_z089_line = LOCK["T_CMB"] * 1.89
T_z634_line = LOCK["T_CMB"] * 7.34
T_z089_meas, e_z089 = 5.08, 0.10              # Muller+2013 (arXiv:1212.5456)
T_z634_meas, e_z634_lo, e_z634_hi = 20.6, 4.2, 9.6   # Riechers+2022 (arXiv:2202.00693)
sig_z089 = (T_z089_meas - T_z089_line) / e_z089
sig_z634 = (T_z634_meas - T_z634_line) / e_z634_lo  # +0.14 sigma (uses lower error)

# literal constant-rate reading of the PWC slope (killed?)
t0_wall   = t_age_gyr(0.0,  LOCK["H0_wall"], 0.315)
t089_wall = t_age_gyr(0.89, LOCK["H0_wall"], 0.315)
t634_wall = t_age_gyr(6.34, LOCK["H0_wall"], 0.315)
lb089 = t0_wall - t089_wall
lb634 = t0_wall - t634_wall
T_lit_089 = LOCK["T_CMB"] + slope_wall * lb089
T_lit_634 = LOCK["T_CMB"] + slope_wall * lb634
sig_lit_089 = (T_lit_089 - T_z089_meas) / e_z089
sig_lit_634 = (T_lit_634 - T_z634_meas) / e_z634_lo
# measured two-point slope in K/Gyr vs the standard line between the same points
slope_meas = (T_z634_meas - T_z089_meas) / (lb089 - lb634)     # dT/dt along the data pair
slope_line = (T_z634_line - T_z089_line) / (lb089 - lb634)
e_slope    = np.sqrt(e_z089**2 + e_z634_lo**2) / (lb089 - lb634)

# S8 board
s8_planck = 0.832; e_s8_planck = 0.013
s8_des    = 0.789; e_s8_des    = 0.012
s8_comb   = 0.836; e_s8_comb   = 0.0125
s8_pwc    = s8_planck * (19.0 / 20.0)

# dipole / EDGES one-step multiplier
mult_pwc = LOCK["s"] * (1 + LOCK["T"]) * (1 + LOCK["dRho_geom"])
short_dip = (mult_pwc / 2.19 - 1.0) * 100.0
short_edg = (mult_pwc / 2.39 - 1.0) * 100.0

# heat : matter
u_matter = LOCK["rho0"] * LOCK["s"] * LOCK["c0"]**2
hm_ratio = u_matter / LOCK["Q_CMB"]              # 1:990 (locked Q_CMB)
hm_obs, e_hm = 904.5, 6.1
hm_resid = (hm_ratio - hm_obs) / hm_obs * 100.0
hm_sigma = (hm_ratio - hm_obs) / e_hm

# bath
t0_firas, e_firas = 2.72548, 0.00057
bath_dK   = LOCK["T_CMB"] - t0_firas
bath_sig  = bath_dK / e_firas
q_locked  = (LOCK["Q_CMB"] - Q_cmb_re) / LOCK["Q_CMB"] * 100.0

# wall/void (this session's gauge run)
y_c, y_w = -6.606e-8, -5.647e-8
contrast = y_w - y_c
r_meas   = y_w / y_c
r_pwc    = 19.0 / 18.0
frac_sign = 1222.0 / 2347.0

# ------------------------------------------------------------------- rows --
R = []
R.append(dict(
    pred="1. 28/19 tempo (380/28/19)",
    formula="s(1+T)=(1/19)(1+27)=28/19; t_PWC=380/(28/19) [T=3^3=27 locked]",
    pwc=f"257.857 kyr",
    meas="258.0 kyr  (CLAIMED)",
    resid=f"-0.0554% value = +0.0554% ratio; +0.66% if 380->377.7 kyr",
    prov="PWC DERIVED (locked s,T) | obs CLAIMED (audit F3/C4: two hard-coded figures)",
    kill="Planck 2018 z*=1089.92+/-0.25 -> t*~377.7 kyr: 258.0 kyr names no Planck epoch "
         "(this script: t(z*)=%.1f, t(z_drag)=%.1f, t(z=1350)=%.1f kyr; audit: 389 / 258.4). "
         "Unless 380/258 is reproduced from the Planck 2018 tables, the observed side stays "
         "CLAIMED and the +0.0554%% is unverifiable." % (t_zstar, t_zdrag, t_z1350),
    tag="PENDING"))
R.append(dict(
    pred="2. l1 first peak",
    formula="l1 = l_free * R_eff/(2(sqrt(1+R_eff)-1)); R_eff=21*3f/(4(1-f)) "
           "(reach x grip = 3x7 = 21; D30)",
    pwc="219.0",
    meas="220.0 +/- 0.5  (Planck TT)",
    resid="-0.4545%  =  -2.00 sigma",
    prov="DERIVED(in-paper) but inputs NOT locked: l_free=179.5, caloric H0=32.371 "
         "(f_lss=%.4f) -> OPEN on inputs" % f_lss,
    kill="Planck 2018 TT first-peak position 220.0+/-0.5 (219.0 already -2.0 sigma); "
         "an ACT DR6/SPT-3G peak position with sigma<=0.3 kills 219.0 outright.",
    tag="MARGINAL"))
R.append(dict(
    pred="3. wall/void contrast",
    formula="y_wall/y_void = 19/18 = (1/s)/((1/s)-1) = 1.0556 (5.26% = s excess)",
    pwc="1.05556",
    meas="MILCA y-map, 2347 voids (this session): center %.3e, edge %.3e, "
         "contrast %+.3e, ratio %.4f; 1222/2347 wall>center" % (y_c, y_w, contrast, r_meas),
    resid="sign right (wall>center, %+.2e); amplitude noise-limited - ratio %.4f is "
          "noise-dominated (|y|~1e-8 at the single-pixel floor); 19/18 undecidable"
          % (contrast, r_meas),
    prov="PWC DERIVED (locked s) | measured VERIFIED(direction)/OPEN(amplitude) "
         "(audit C9: 2347 rows double-count WMAP5+Planck2018, no edge mask)",
    kill="P2-A stacked wall/void SZ profile (805 edge-masked voids): kill if r<1 at 3sigma, "
         "|r-1.0556|>3 sigma_tot (1% sys floor), no front peak, or sigma_stat>0.028. "
         "Fastest single: a >35-sigma void stack from Planck/ACT/SPT.",
    tag="PENDING"))
R.append(dict(
    pred="4. T_CMB(z) slope = -H",
    formula="dT/dt = -H*T0: %.4f (H0_wall) to %.4f (H0_planck) K/Gyr at z=0 "
           "(band 0.19-0.21; excludes H0<69.2)" % (slope_wall, slope_planck),
    pwc="slope -[0.188, 0.206] K/Gyr",
    meas="Muller+2013 z=0.89: 5.08+/-0.10 vs line 5.1512 K (-0.71 sigma); "
         "Riechers+2022 z=6.34: 20.6 [16.4,30.2] vs line 20.0052 K (+0.60 K, bracketed). "
         "Two-point slope %.2f vs line %.2f K/Gyr (+0.2 sigma)" % (slope_meas, slope_line),
    resid="0% vs T0(1+z) - the -H*T slope IS the standard adiabatic law (restatement, "
          "non-discriminating)",
    prov="PWC DERIVED but degenerate with LCDM | measured MEASURED (arXiv:1212.5456, "
         "2202.00693; note: the z=0.89 point is Muller+2013, not SPT - SPT's own is "
         "Saro+2014 alpha=0.017+0.030/-0.028)",
    kill="Any T_CMB(z) point >3 sigma off T0(1+z) (SPT-3G clusters z~1-2; a second ALMA "
         "z>4 point). Honest caveat: the literal constant-rate reading T=T0-H*T0*t is "
         "already killed: T_lit(z=0.89)=%.2f K -> %.1f sigma; T_lit(z=6.34)=%.2f K -> "
         "%.1f sigma." % (T_lit_089, sig_lit_089, T_lit_634, sig_lit_634),
    tag="PASS (trivial)"))
R.append(dict(
    pred="5. S8 weak-lensing shift",
    formula="S8_PWC = S8_Planck x 19/20 = 0.832 x 0.95 (19/20 = debt complement, D42)",
    pwc="0.7904",
    meas="DES Y6 0.789 +/- 0.012 (arXiv:2601.14559) | Planck 2018 0.832 +/- 0.013 | "
         "Combined CMB 2026 0.836 +0.012/-0.013",
    resid="+0.18% = +0.12 sigma vs DES;  -5.00% = -3.20 sigma vs Planck; "
          "-5.45% = -3.6 sigma vs Combined CMB",
    prov="BACK-SOLVED: the 19/20 factor is locked, but the anchor 0.832 is Planck's "
         "MEASURED S8 - not a locked-constant prediction",
    kill="Combined CMB 2026 S8 = 0.836+0.012/-0.013 (0.7904 is -3.6 sigma); Planck 2018 "
         "alone (-3.2 sigma) already kills D42 unless the Planck S8 itself is wrong.",
    tag="PASS vs DES only"))
R.append(dict(
    pred="6. dipole / EDGES partial",
    formula="s(1+T)(1+dRho_geom) = (28/19)(1.24313) = 1.8320 one-step multiplier",
    pwc="1.8320x  (covers 83.7% of dipole / 76.7% of EDGES)",
    meas="CMB dipole 3.3621+/-0.0010 mK (Planck): 2.19x target | EDGES T21=-500 mK "
         "(+200/-500, 99% CL; Bowman+2018): 2.39x target - UNVERIFIED (SARAS-3 rejects "
         "the EDGES profile at >95% CL)",
    resid="-16.3% of the 2.19x dipole excess; -23.3% of the 2.39x EDGES ratio "
          "(16-23% short, as recorded)",
    prov="PWC DERIVED (locked s,T,dRho_geom) | dipole MEASURED, EDGES CLAIMED/UNVERIFIED "
         "| recorded MISS (Bucket 3 #2, not claimed)",
    kill="An independent global 21-cm spectrum (REACH / SARAS-3-class) at z~15-25: "
         "SARAS-3 already excludes the EDGES profile (>95% CL); a confirmed trough "
         "deeper than 1.84x amplification kills the partial outright.",
    tag="MISS (recorded)"))
R.append(dict(
    pred="7. heat : matter",
    formula="Q_CMB : rho0*s*c0^2 = %.3e : %.3e J/m^3 (T/990 = %.4f mK)"
           % (Q_cmb_re, u_matter, LOCK["T_CMB"] / hm_ratio * 1e3),
    pwc="1 : %.1f" % hm_ratio,
    meas="1 : 904.5 +/- 6.1 (census: Planck Omega_b h^2 = 0.02237 +/- 0.00015)",
    resid="+%.2f%% in matter:heat = +%.1f sigma  (PWC needs Omega_b h^2 = 0.02449)"
          % (hm_resid, hm_sigma),
    prov="PWC DERIVED (locked rho0, s, Q_CMB) | measured MEASURED (Planck baryon census) "
         "| recorded MISS (census ledger, never hidden)",
    kill="Planck 2018 Omega_b h^2 = 0.02237 +/- 0.00015 - already +14.1 sigma; the single "
         "fastest kill is the same census re-confirmed by any next baryon measurement.",
    tag="MISS (recorded)"))
R.append(dict(
    pred="8. bath temperature",
    formula="T_bath = 2.7255 K (ledger-locked; Q = a*T^4 = %.4e vs locked %.4e, %+.3f%%)"
           % (Q_cmb_re, LOCK["Q_CMB"], q_locked),
    pwc="2.7255 K",
    meas="2.72548 +/- 0.00057 K (FIRAS, Fixsen 2009)",
    resid="+%.0e K = +%.5f%% = +%.2f sigma" % (bath_dK, bath_dK / t0_firas * 100, bath_sig),
    prov="CIRCULAR: T_CMB=2.7255 K is itself a LOCKED constant; the ledger adopts the "
         "FIRAS value (no locked-constant derivation found on disk) -> BACK-SOLVED, "
         "not a falsifiable",
    kill="An independent FIRAS-class absolute calibration (PIXIE-class, sigma<=0.5 mK) "
         "moving T0 off 2.7255 K; faster: exhibit the locked-constant derivation of "
         "2.7255 K - as recorded, none exists (circularity is the kill).",
    tag="PASS (circular)"))

# ---------------------------------------------------------------- renderer --
def wrap(s, w):
    return textwrap.wrap(s, w) or [""]

print("=" * 118)
print("PWC CMB & COSMIC-WEB FALSIFIABLE SCOREBOARD - locked constants only, ZERO fitted parameters")
print("Provenance tags: DERIVED | MEASURED | VERIFIED | BACK-SOLVED | CLAIMED | OPEN")
print("=" * 118)
print()

# compact one-line table (kill condition given per-row below)
W = [20, 26, 14, 30, 30, 12]
hdr = ["prediction", "PWC", "residual", "measured", "provenance", "verdict"]
print("{:<20} {:<26} {:<14} {:<30} {:<30} {:<12}".format(*hdr))
print("-" * 118)
for r in R:
    print("{:<20.20} {:<26.26} {:<14.14} {:<30.30} {:<30.30} {:<12}".format(
        r["pred"], r["pwc"], r["resid"], r["meas"], r["prov"], r["tag"]))
print("-" * 118)
print()

for r in R:
    print("#" * 118)
    print(r["pred"])
    print("  formula     : " + "\n                ".join(wrap(r["formula"], 100)))
    print("  PWC         : " + r["pwc"])
    print("  measured    : " + "\n                ".join(wrap(r["meas"], 100)))
    print("  residual    : " + "\n                ".join(wrap(r["resid"], 100)))
    print("  provenance  : " + "\n                ".join(wrap(r["prov"], 100)))
    print("  KILL        : " + "\n                ".join(wrap(r["kill"], 100)))
    print()

print("=" * 118)
print("5-LINE SUMMARY")
print("=" * 118)
print("1. Exact-but-circular passes: bath 2.7255 K (+0.04 sigma vs FIRAS) is a locked input, and the "
      "T(z) slope -H*T0 (0.188-0.206 K/Gyr) is the standard adiabatic law verbatim - both verify "
      "but cannot discriminate PWC from LCDM (and the band itself excludes H0 < 69.2 km/s/Mpc).")
print("2. S8 = 0.7904 nails DES Y6 0.789+/-0.012 (+0.12 sigma) but is -3.2 sigma from Planck 2018 and "
      "-3.6 sigma from Combined-CMB 2026: a back-solved re-anchor of Planck's measured 0.832 through "
      "the locked 19/20, not a locked-constant prediction.")
print("3. l1 = 219.0 is -2.0 sigma from Planck's 220.0+/-0.5 and leans on two NON-locked in-paper inputs "
      "(l_free = 179.5, caloric H0 = 32.371): internal consistency, OPEN, not a locked-constant hit.")
print("4. Wall/void 19/18: this session's 2,347-void MILCA y-map read shows the predicted direction "
      "(wall-center = +9.6e-9) but the amplitude is noise-limited (median ratio 0.8548 sits on the "
      "single-pixel noise floor; 52.1% wall>center) - the P2-A 805-void stack is the armed kill.")
print("5. Misses kept visible: heat:matter 1:990 vs 1:904.5+/-6.1 = +14.1 sigma; dipole/EDGES 1.8320x "
      "covers only 77-84% of the 2.19x/2.39x targets; tempo +0.0554% inflates to +0.66% once 380 -> "
      "377.7 kyr, and 258.0 kyr names no Planck epoch - the observed side stays CLAIMED.")
print("=" * 118)
sys.exit(0)
