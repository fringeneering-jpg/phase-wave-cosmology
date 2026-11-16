"""
quantify_bbn.py -- the BBN nucleosynthesis ladder of Phase Wave Cosmology (PWC),
quantified from LOCKED constants only.

RULES (task brief 2026-10-21):
  * ZERO fitted parameters -- every number is a locked constant or a named
    literature measurement, with provenance stated per number.
  * Provenance per number.  Misses reported, never hidden -- killed
    candidates are printed, not suppressed.
  * Kill condition per candidate: survives iff |PWC - measured| <= 3 sigma.
  * Exit code 0 always (a killed candidate is a reported result, not a crash).

The cage (LOCKED in the brief):
  c0, rho0, s = 1/19, f_solid = 8.4989e-4, T = 27, T7b = 1/57, T7d = 20/1083,
  N = 16, alpha, m_p, m_e, m_n, m_n - m_p = 1.293332 MeV, X17 = 16.8421,
  pi0 = 134.9768, a_V = 15.5945, a_S = 17.3273, G, hbar, kB, Q_CMB, T_CMB,
  28/19 = 1.473684, eta_B = f_solid^3 = 6.139e-10.
"""
import math
import sys

# ----------------------------------------------------------------------
# LOCKED CONSTANTS (provenance per number)
# ----------------------------------------------------------------------
c0        = 2.99792458e8       # exact, SI definition (CGPM 1983)
rho0      = 8.74e-27           # PWC locked resting density (Planck 2018 mean; PWC closure 8.70 vs 8.74, +0.5%)
s         = 1.0 / 19.0         # PWC locked debt share, F_EM/F_debt = 19 (D3)
f_solid   = 8.4989e-4          # PWC locked solid sieve fraction (D39, back-solved to G)
T_t       = 27.0               # PWC locked tightening coefficient T = 3^3 (D14/D31, Planck LSS tempo closure)
T7b       = 1.0 / 57.0         # PWC locked bound T7 shear = s/3 (lepton T7 spread, CLOSED 2026-10-20)
T7d       = 20.0 / 1083.0      # PWC locked decay T7 shear = (20/19)(1/57) = 1.8263% (unspooling debt)
N         = 16.0               # PWC locked 16-fold clock
ALPHA_INV = 137.035999084      # CODATA 2018 fine-structure inverse
m_p       = 938.272088         # CODATA 2018 proton mass [MeV]
m_e       = 0.51099895         # CODATA 2018 electron mass [MeV]
m_n       = 939.5654205        # CODATA 2018 neutron mass [MeV]
dM_lock   = 1.293332           # PWC locked neutron-proton mass gap [MeV]
X17       = 16.8421            # PWC locked X17 energy = N*(20/19) = 320/19 [MeV]
pi0       = 134.9768           # PDG 2020 neutral pion [MeV]
a_V       = 15.5945            # PWC locked volume term (18/19)(m_p/57) [MeV] (D43)
a_S       = 17.3273            # PWC locked surface term (20/19)(m_p/57) = m_p*T7d [MeV] (D43)
G         = 6.67430e-11        # CODATA 2018
HBAR      = 1.054571817e-34    # CODATA 2018
KB        = 1.380649e-23       # exact, SI definition (CGPM 2019)
Q_CMB     = 4.175e-14          # Planck 2018 CMB energy density [J/m^3]
T_CMB     = 2.7255             # FIRAS/COBE 2009 CMB temperature [K]
TEMPO     = 28.0 / 19.0        # PWC locked LSS tempo s(1+T) = 1.473684 (D31, +0.0554% vs Planck 380/258)

# ----------------------------------------------------------------------
# MEASUREMENTS (provenance per number)
# ----------------------------------------------------------------------
Yp_obs   = 0.2470              # Planck 2018 He-4 mass fraction (locked by the task brief)
Yp_err   = 0.0002
DH_obs   = 2.527e-5            # Cooke+ 2018 primordial D/H (locked by the task brief)
DH_err   = 0.030e-5
Li7_BBN  = 5.40e-10            # SBBN literature 7Li/H prediction (EXTERNAL input -- FLAGGED, not derived in PWC)
Li7_obs  = 1.58e-10            # Spite plateau 7Li/H, Sbordone+ 2010 (as used in anomaly_sweep_2026_10_21.py sec.5)
Li7_err  = 0.11e-10
eta_obs  = 6.104e-10           # Planck 2018 baryon-to-photon ratio
eta_err  = 0.058e-10

def verdict(pwc, obs, err):
    sig = (pwc - obs) / err
    pct = 100.0 * (pwc / obs - 1.0)
    return sig, pct, ("SURVIVES (<=3 sigma)" if abs(sig) <= 3.0 else "KILLED (>3 sigma)")

def Yp(x):
    """All-neutrons-to-He4 bookkeeping: Y_p = 2 x_n / (1 + x_n)."""
    return 2.0 * x / (1.0 + x)

print("=" * 92)
print("PWC BBN NUCLEOSYNTHESIS LADDER -- FROM LOCKED CONSTANTS ONLY (zero fitted parameters)")
print("=" * 92)

# ----------------------------------------------------------------------
# CAGE SELF-CHECKS: locked constants against each other
# ----------------------------------------------------------------------
print()
print("CAGE SELF-CHECKS (locked numbers cross-checked, provenance stated)")
print("  m_n - m_p       = %.7f MeV  vs locked 1.293332 MeV -> delta %+.3e MeV (CODATA masses)"
      % (m_n - m_p, (m_n - m_p) - dM_lock))
print("  T7b = s/3       = %.10f vs locked 1/57  = %.10f" % (s / 3.0, 1.0 / 57.0))
print("  T7d = (20/19)T7b = %.10f vs locked 20/1083 = %.10f" % ((20.0 / 19.0) * T7b, 20.0 / 1083.0))
print("  28/19 = s(1+T)  = %.10f vs locked 1.473684" % (s * (1.0 + T_t)))
print("  eta_B = f_solid^3 = %.6e vs locked 6.139e-10" % (f_solid ** 3))
print("  1083 = 19*57    = %d (T7d denominator)" % (19 * 57))
print("  a_S = m_p*T7d   = %.6f MeV vs locked a_S = 17.3273 MeV" % (m_p * T7d))

# ----------------------------------------------------------------------
# ROW 1 -- He-4 mass fraction Y_p from the neutron/proton cage share
# ----------------------------------------------------------------------
print()
print("-" * 92)
print("ROW 1.  He-4 MASS FRACTION  Y_p = 2 x_n/(1+x_n),  x_n = n/p at freeze-out")
print("        x_n built from the debt s and the T7 shears ONLY (no fitted knob)")
print("-" * 92)
cage = [
    ("x_n = s = 1/19            (debt share itself)",          s),
    ("x_n = T7b = 1/57          (bound shear)",                T7b),
    ("x_n = T7d = 20/1083       (decay shear)",                T7d),
    ("x_n = s + T7b = 4/57",                                   s + T7b),
    ("x_n = (N/2)*T7b = 8/57    (half the 16-fold clock over the 57 = 19*3-thread cage)", (N / 2.0) * T7b),
    ("x_n = (N/2)*T7d = 160/1083",                             (N / 2.0) * T7d),
    ("x_n = 1/7                 (locked fold grip 7)",          1.0 / 7.0),
    ("x_n = s/(1-s) = 1/18",                                   s / (1.0 - s)),
]
best_key, best_val, best_sig, best_pct, best_ver = None, 0.0, 1e18, 0.0, ""
for label, x in cage:
    y = Yp(x)
    sg, pc, ver = verdict(y, Yp_obs, Yp_err)
    print("    %-62s -> Y_p = %.6f   residual %+.4f%%  (%+.2f sigma)  %s" % (label, y, pc, sg, ver))
    if abs(sg) < abs(best_sig):
        best_key, best_val, best_sig, best_pct, best_ver = label, y, sg, pc, ver
print("  BEST CANDIDATE: %s" % best_key)
print("    PWC        : Y_p = 2*(8/57)/(1+8/57) = 16/65 = %.6f" % best_val)
print("    measured   : 0.2470 +/- 0.0002 (Planck 2018, locked by task brief)")
print("    residual   : %+.6f  (%+.4f%%, %+.2f sigma)" % (best_val - Yp_obs, best_pct, best_sig))
print("    provenance : N = 16 (16-fold clock, locked); T7b = 1/57 = s/3 (locked bound shear);")
print("                 57 = 19*3 threads; 8 = N/2 pairs; Y_p = 2x/(1+x) standard all-n-to-He4.")
print("                 NEW probe (candidate per task brief; no paper equation yet).")
print("    kill cond. : |Y_p - 0.2470| <= 3*0.0002  ->  %.2f sigma  ->  %s" % (best_sig, best_ver))
print("    NOTE       : -0.34% in value but outside Planck's +/-0.0002 bar; reported, never hidden.")

# ----------------------------------------------------------------------
# ROW 2 -- D/H from the 28/19 tempo ratio as the dilution
# ----------------------------------------------------------------------
print()
print("-" * 92)
print("ROW 2.  DEUTERIUM  D/H -- try the 28/19 tempo ratio as the dilution")
print("        (28/19 = s(1+T) = 1.473684, locked by the Planck LSS tempo closure D31)")
print("-" * 92)
dh_cand = [
    ("raw dilution 19/28",                                    19.0 / 28.0),
    ("(19/28)^(T-1) = (19/28)^26",                            (19.0 / 28.0) ** (T_t - 1.0)),
    ("(19/28)^T = (19/28)^27   (dilution over T = 3^3 stages)", (19.0 / 28.0) ** T_t),
    ("(19/28)^(T+1) = (19/28)^28",                            (19.0 / 28.0) ** (T_t + 1.0)),
    ("(19/28)^(T*19/20)",                                     (19.0 / 28.0) ** (T_t * 19.0 / 20.0)),
    ("(19/28)^(T*20/19)",                                     (19.0 / 28.0) ** (T_t * 20.0 / 19.0)),
]
best_dh = None
for label, d in dh_cand:
    sg, pc, ver = verdict(d, DH_obs, DH_err)
    print("    %-42s -> %.4e   residual %+8.2f%%  (%+.2f sigma)  %s" % (label, d, pc, sg, ver))
    if best_dh is None or abs(sg) < abs(best_dh[3]):
        best_dh = (label, d, pc, sg, ver)
print("  BEST CANDIDATE: %s" % best_dh[0])
print("    PWC        : %.4e" % best_dh[1])
print("    measured   : 2.527e-5 +/- 0.030e-5 (Cooke+ 2018, locked by task brief)")
print("    residual   : %+.4e  (%+.2f%%, %+.2f sigma)" % (best_dh[1] - DH_obs, best_dh[2], best_dh[3]))
print("    provenance : 28/19 = s(1+T) locked (D31); dilution compounded over T = 3^3 = 27 stages.")
print("                 NEW probe (candidate per task brief; no paper equation yet).")
print("    kill cond. : |D/H - 2.527e-5| <= 3*0.030e-5  ->  %+.2f sigma  ->  %s" % (best_dh[3], best_dh[4]))
print("    NOTE       : OPEN -- no locked exponent lands inside 3 sigma of the measurement.")

# ----------------------------------------------------------------------
# ROW 3 -- Li-7/H re-verification
# ----------------------------------------------------------------------
print()
print("-" * 92)
print("ROW 3.  LITHIUM-7  (7Li/H)_PWC = (7Li/H)_BBN / (3 x 19/16)  -- RE-VERIFY")
print("-" * 92)
S_Li_A = (3.0 * 19.0) / 16.0
S_Li_B = 3.0 * (19.0 / 18.0)
Li7_pwc_A = Li7_BBN / S_Li_A
Li7_pwc_B = Li7_BBN / S_Li_B
print("  Path A divisor 3*19/16 = %.4f  (locked 3-dim gauge partition; the three axes that carry T = 3^3)" % S_Li_A)
print("    PWC        : 5.40e-10 / 3.5625 = %.4e" % Li7_pwc_A)
print("    measured   : 1.58e-10 +/- 0.11e-10 (Spite plateau, Sbordone+ 2010)")
sgA, pcA, verA = verdict(Li7_pwc_A, Li7_obs, Li7_err)
print("    residual   : %+.4e  (%+.2f%%, %+.2f sigma)  %s   [task brief said -0.58 sigma: RE-VERIFIED]"
      % (Li7_pwc_A - Li7_obs, pcA, sgA, verA))
print("    provenance : divisor 3 x 19/16 locked (COSMOLOGY_ASTROPHYSICS.md sec.17; anomaly_sweep_2026_10_21.py sec.5);")
print("                 (7Li/H)_BBN = 5.40e-10 is the SBBN literature prediction -- EXTERNAL INPUT, FLAGGED.")
print("    kill cond. : |Li-7 - 1.58e-10| <= 3*0.11e-10  ->  %.2f sigma  ->  %s" % (sgA, verA))
print("  Path B divisor 3*(19/18) = %.4f" % S_Li_B)
sgB, pcB, verB = verdict(Li7_pwc_B, Li7_obs, Li7_err)
print("    PWC        : 5.40e-10 / 3.1667 = %.4e   residual %+.2f%% (%+.2f sigma)  %s" % (Li7_pwc_B, pcB, sgB, verB))

# ----------------------------------------------------------------------
# ROW 4 -- n/p ratio from the mass gap and the T7/T=27 freeze-out
# ----------------------------------------------------------------------
print()
print("-" * 92)
print("ROW 4.  n/p AT FREEZE-OUT  x_n = exp(-dM/T_f),  dM = m_n - m_p = 1.293332 MeV (locked)")
print("        T_f from the locked freeze-out readings (T7 x T=27 family)")
print("-" * 92)
tf_cand = [
    ("T_f = 27*T7b = 27/57 = 0.4737 MeV     ('T7/T=27' reading, bound shear)",  T_t * T7b),
    ("T_f = 27*T7d = 540/1083 = 0.4986 MeV  ('T7/T=27' reading, decay shear)",  T_t * T7d),
    ("T_f = (2/s)*T7b = 38/57 = 2/3 MeV     (2/s = 38 threads; 2/3 = Koide fold)", (2.0 / s) * T7b),
    ("T_f = dM/2 = 0.6467 MeV",                                                 dM_lock / 2.0),
    ("T_f = 27 MeV (literal T = 27)",                                           T_t),
]
best_tf = None
for label, tf in tf_cand:
    xn = math.exp(-dM_lock / tf)
    y = Yp(xn)
    sg, pc, ver = verdict(y, Yp_obs, Yp_err)
    print("    %-52s -> x_n = %.5f   Y_p = %.5f   (%+.2f sigma)  %s" % (label, xn, y, sg, ver))
    if best_tf is None or abs(sg) < abs(best_tf[3]):
        best_tf = (label, xn, y, pc, sg, ver)
print("  BEST CANDIDATE: %s" % best_tf[0])
print("    x_n        : %.5f" % best_tf[1])
print("    Y_p via it : %.5f vs 0.2470 +/- 0.0002  (%+.2f%%, %+.2f sigma)" % (best_tf[2], best_tf[3], best_tf[4]))
print("    provenance : dM = 1.293332 MeV locked (CODATA m_n - m_p = 1.2933325 MeV); T7b, T7d, T = 27 locked.")
print("    kill cond. : consistency with Y_p at <= 3 sigma  ->  %.2f sigma  ->  %s" % (best_tf[4], best_tf[5]))
print("    NOTE       : OPEN -- no locked T_f lands inside 3 sigma. The standard SBBN freeze-out")
print("                 (T_f ~ 0.7 MeV) is NOT a locked PWC number and is excluded (flagged, not used).")

# ----------------------------------------------------------------------
# ROW 5 -- baryon share eta_B = f_solid^3
# ----------------------------------------------------------------------
print()
print("-" * 92)
print("ROW 5.  BARYON-TO-PHOTON RATIO  eta_B = f_solid^3")
print("-" * 92)
eta_pwc = f_solid ** 3
sgE, pcE, verE = verdict(eta_pwc, eta_obs, eta_err)
print("    PWC        : (8.4989e-4)^3 = %.6e" % eta_pwc)
print("    measured   : 6.104e-10 +/- 0.058e-10 (Planck 2018)")
print("    residual   : %+.4e  (%+.2f%%, %+.2f sigma)  %s" % (eta_pwc - eta_obs, pcE, sgE, verE))
print("    provenance : f_solid = 8.4989e-4 locked solid sieve fraction (D39 closure, 2026-10-21);")
print("                 eta_B = f_solid^3 = 6.139e-10 locked.")
print("    kill cond. : |eta_B - 6.104e-10| <= 3*0.058e-10  ->  %+.2f sigma  ->  %s" % (sgE, verE))

# ----------------------------------------------------------------------
# COMPACT TABLE
# ----------------------------------------------------------------------
print()
print("=" * 92)
print("COMPACT TABLE  (abundance | formula | PWC | measured | residual | provenance | kill)")
print("=" * 92)
xn_lit = math.exp(-dM_lock / (T_t * T7b))
y_lit = Yp(xn_lit)
sg_lit, pc_lit, ver_lit = verdict(y_lit, Yp_obs, Yp_err)

rows = [
    ("Y_p      ", "2x/(1+x), x=(N/2)*T7b=8/57", "0.246154", "0.2470 +/- 0.0002 Planck18",
     "%+.4f%% %+.2fs" % (best_pct, best_sig), "N=16, T7b=1/57=s/3 (new probe)", best_ver),
    ("D/H      ", "(19/28)^T=(28/19)^-27", "2.8384e-5", "2.527e-5 +/- 0.030e-5 Cooke18",
     "%+.2f%% %+.2fs" % (best_dh[2], best_dh[3]), "28/19=s(1+T), T=27 (new probe)", best_dh[4]),
    ("Li-7/H   ", "BBN/(3*19/16)=5.40e-10/3.5625", "1.5158e-10", "1.58e-10 +/- 0.11e-10 Spite",
     "%+.2f%% %+.2fs" % (pcA, sgA), "3*19/16 locked; BBN 5.40e-10 EXTERNAL", verA),
    ("n/p      ", "exp(-dM/T_f), T_f=27*T7b=27/57 MeV", "0.06520 (Y_p=0.12241)", "Y_p = 0.2470 +/- 0.0002 Planck18",
     "%+.2f%% %+.2fs" % (pc_lit, sg_lit), "dM=1.293332 MeV, T=27, T7b locked", ver_lit),
    ("eta_B    ", "f_solid^3=(8.4989e-4)^3", "6.1389e-10", "6.104e-10 +/- 0.058e-10 Planck18",
     "%+.2f%% %+.2fs" % (pcE, sgE), "f_solid=8.4989e-4 locked (D39)", verE),
]
for name, formula, pwc, meas, res, prov, kill in rows:
    print("  %-9s| %-28s| %-10s| %-24s| %-16s| %-34s| %s" % (name, formula, pwc, meas, res, prov, kill))

# ----------------------------------------------------------------------
# 5-LINE SUMMARY
# ----------------------------------------------------------------------
print()
print("5-LINE SUMMARY")
print("1. BEST HIT   : Li-7/H = 5.40e-10/(3*19/16) = 1.5158e-10 vs 1.58+/-0.11e-10 (-0.58 sigma, re-verified);")
print("                eta_B = f_solid^3 = 6.1389e-10 vs 6.104+/-0.058e-10 (+0.60 sigma) -- both SURVIVE.")
print("2. WORST MISS : n/p Boltzmann at T_f = 27*T7b = 27/57 MeV -> Y_p = 0.1224 (-50%, -623 sigma);")
print("                D/H best candidate (19/28)^27 = 2.8384e-5 (+12.3%, +10.4 sigma) -- both KILLED, reported.")
print("3. HE-4       : best cage share x_n = (N/2)*T7b = 8/57 -> Y_p = 16/65 = 0.246154 vs 0.2470+/-0.0002:")
print("                -0.34% in value but -4.23 sigma on Planck's bar -> KILLED formally (recorded, never hidden).")
print("4. SCORE      : 2/5 survive (Li-7, eta_B); 3/5 killed (Y_p, D/H, n/p) -- zero fitted parameters everywhere.")
print("5. NEXT DERIV : fix T_f structurally from the cage counts (instead of guessing 27*T7) and fold in the neutron")
print("                endurance window (14:38 / 878 s) between freeze-out and He-4 assembly to close the -4.2 sigma Y_p.")

print()
print("EXIT 0 -- all rows quantified, kills reported, no fitted parameter used.")
sys.exit(0)
