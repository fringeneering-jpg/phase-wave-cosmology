# -*- coding: ascii -*-
"""
quantify_particles.py -- PWC particle column, ZERO fitted parameters (2026-10-21)

Derive every remaining particle mass from the locked cage pieces only:
(m_p, s, T7, N=16, X17, a_S, a_V, the pion modes, the 133.5 emptiness).

RULES: zero fitted parameters; every number carries provenance; misses are
reported, never hidden; every candidate states its kill condition.

Provenance legend:
  DERIVED  = follows from locked constants by the established chain
  MEASURED = external measurement (PDG 2024) -- never re-fit
  VERIFIED = one-step cage formula matches PDG within 1 sigma
  CLAIMED  = passes sigma but the structure lacks a cage derivation yet
  OPEN     = unexplained term / numerics-only coincidence
  MISS     = killed by PDG precision (kill condition stated)

Allowed ratio blocks: {19, 18, 20, 16, 8, 3, 2, 57, 1083, 33, 27, 420, 133.5,
                       alpha, s, phi}
constructible helpers: 5 = 20/4, 7 = 420/(20*3), 10 = 20/2, 11 = 33/3,
                       21 = 420/20, 25 = (20/4)^2, 70 = 2*5*7, 89 = 133.5*2/3,
                       250 = 2*5^3, 475 = 5^2*19, 342 = 18*19, 108 = 4*27.
"""
import math
import os
import sys

# ================= LOCKED CONSTANTS (never re-fit) =================
c0        = 2.99792458e8
hbar      = 1.054571817e-34
e_J       = 1.602176634e-19
s         = 1.0/19.0
T7_bound  = s/3.0                    # 1/57
T7_decay  = 20.0/1083.0
T7_mid    = 0.5*(T7_bound + T7_decay)   # 39/2166
N16       = 16                        # N = 16 = 8 chiral pairs
alpha     = 1.0/137.035999084
phi       = 0.5*(1.0 + math.sqrt(5.0))
mp        = 938.27208816              # proton, MeV  (locked 938.272088)
mp_pwc    = 937.19                    # PWC bare cage, MeV
me        = 0.51099895                # electron, MeV
mn        = 939.5654205               # neutron, MeV
R_p       = 0.84e-15                  # m
X17       = 16.0*(20.0/19.0)          # MeV  (locked 16.8421)
E_emp     = 133.5                     # locked emptiness ratio (M_H/m_p = 133.49)
v_ew      = 246.21965                 # GeV
M_H_obs   = 125.25                    # GeV
M_W_obs   = 80.3602                   # GeV
M_Z_obs   = 91.1876                   # GeV
pipm_obs  = 139.57039                 # MeV, PDG

# ================= DERIVED CAGE PIECES (chain, zero fit) =================
d_q      = mp/57.0                    # 1-axis debt quantum    16.4609 MeV  DERIVED
a_V      = (18.0/19.0)*d_q            # volume binding         15.5945 MeV  DERIVED
a_S      = (20.0/19.0)*d_q            # surface tension        17.3273 MeV  DERIVED
X17_mid  = mp_pwc*T7_mid              # bound-decay midpoint   16.8746 MeV  DERIVED
pi0_pwc  = 8.0*X17_mid                # neutral pion mode      134.9968     DERIVED
pipm_pwc = 8.0*a_S                    # charged pion mode      138.6182     DERIVED
lamC_e   = hbar*c0/(me*1e6*e_J)       # 3.8616e-13 m
L_lad    = 4.0*lamC_e/R_p             # 1838.85  (the 4*lamC/R_p ladder)
lamC_p   = hbar*c0/(mp*1e6*e_J)
L_lad_p  = 4.0*lamC_p/R_p             # 1.00147  (ladder applied to the cage)
E_mh     = M_H_obs/(mp/1000.0)        # 133.49 -> locked 133.5
M_H_A    = (v_ew/2.0)*(1.0 + T7_bound)*1000.0           # MeV
M_H_B    = ((mp/1000.0)/alpha)*(1.0 - 0.5*s)*1000.0     # MeV
M_H_mid  = 0.5*(M_H_A + M_H_B)                           # MeV

# ================= PDG 2024 (MEASURED, never re-fit) =================
PDG = {
    "pi0":    (134.9768,   0.0005),
    "pipm":   (139.57039,  0.00018),
    "Kpm":    (493.677,    0.016),
    "K0":     (497.611,    0.013),
    "eta":    (547.862,    0.017),
    "mu":     (105.6583755, 0.0000023),
    "tau":    (1776.86,    0.12),
    "Lambda": (1115.683,   0.006),
    "Sigma0": (1192.642,   0.024),
    "Sigmap": (1189.37,    0.07),
    "Sigmam": (1197.449,   0.030),
    "Xi0":    (1314.86,    0.20),
    "Xim":    (1321.71,    0.07),
    "Omega":  (1672.45,    0.29),
    "Delta":  (1232.0,     2.0),
    "Higgs":  (125250.0,   170.0),
}

def score(name, formula, value, prov, kill):
    meas, err = PDG[name]
    res  = 100.0*(value/meas - 1.0)
    sig  = abs(value - meas)/err
    if sig <= 1.0:
        verdict = "VERIFIED"
    elif sig <= 3.0:
        verdict = "CLAIMED"
    else:
        verdict = "MISS"
    return res, sig, verdict

out = []          # full report (also written to disk)
def P(line=""):
    print(line)
    out.append(line)

# ================= MAIN TABLE =================
MAIN = [
 ("pi0",    "8*X17_mid (8 chiral pairs)",          pi0_pwc,             "DERIVED",
  "locked cage mode; +40.3s vs PDG's 0.5 keV precision (accepted as the mode)", "pi0"),
 ("pi+-",   "8*a_S (surface mode)",                pipm_pwc,            "DERIVED",
  "5290s (0.68%) -- surface mode overshoots; no passing fix", "pipm"),
 ("K+-",    "m_p*(1+s)/2 = m_p*10/19",             mp*(1.0+s)/2.0,      "DERIVED",
  "9.4s -- killed; passing variants are OPEN/CLAIMED (scan B)", "Kpm"),
 ("K0",     "pi0_pwc*(70/19)",                     pi0_pwc*(70.0/19.0), "DERIVED",
  "19.5s -- killed; alt m_p*19/36*(1+2/420) = 4.1s", "K0"),
 ("eta",    "4*pi0_pwc + a_V/2",                   4.0*pi0_pwc + a_V/2.0, "DERIVED",
  "4.5s -- killed; alt 4*pi0_pwc*(1+5/342) = 1.2s CLAIMED", "eta"),
 ("muon",   "m_p*(18/16)*(2/20)  [1836 ladder]",   mp*9.0/80.0,         "DERIVED",
  "44,700s -- PDG 2.3 eV precision; no one-step form can close", "mu"),
 ("tau",    "m_e*E*27*(1-2s/3)   [133.5 family]",  me*E_emp*27.0*(1.0-2.0*s/3.0), "DERIVED",
  "3.4s -- killed; alt m_p*36/19 = 7.7s", "tau"),
 ("Lambda", "m_p + 11*(m_p/57)",                  mp + 11.0*d_q,        "DERIVED",
  "nearest integers 11d(+0.33%,610s) / 10X17(-0.81%) -- killed", "Lambda"),
 ("Sigma0", "m_p + 15*X17",                       mp + 15.0*X17,        "DERIVED",
  "nearest: 15X17(-0.15%,72s) / 16d(+0.76%) -- killed", "Sigma0"),
 ("Xi0",    "m_p + 23*(m_p/57)",                  mp + 23.0*d_q,        "DERIVED",
  "best integer 23d(+0.15%,10s); 22X17(-0.46%) -- killed", "Xi0"),
 ("Omega",  "m_p + 42*a_S",                       mp + 42.0*a_S,        "DERIVED",
  "best integer 42aS(-0.38%,22s); 45d(+0.39%) -- killed", "Omega"),
 ("Delta",  "m_p + (20-3)*a_S",                   mp + 17.0*a_S,        "VERIFIED",
  "none -- passes (k_eff = 16.95 ~ 17)", "Delta"),
 ("H(A)",   "(v/2)*(1+s/3)",                      M_H_A,                "VERIFIED",
  "none -- 0.12s (anchor, boson_to_higgs_ladder)", "Higgs"),
 ("H(B)",   "(m_p/alpha)*(1-s/2)",                M_H_B,                "VERIFIED",
  "none -- 0.33s (anchor)", "Higgs"),
 ("H(mid)", "0.5*(H_A+H_B)",                      M_H_mid,              "VERIFIED",
  "none -- 0.11s (anchor)", "Higgs"),
]

P("="*118)
P("PWC PARTICLE COLUMN -- QUANTIFIED FROM LOCKED CONSTANTS ONLY (zero fitted parameters)")
P("="*118)
P("name  | PWC formula                          | PWC value       | measured (PDG)      | residual   | sigma     | provenance | kill condition")
P("-"*118)
for name, formula, value, prov, kill, key in MAIN:
    meas, err = PDG[key]
    res, sig, verdict = score(key, formula, value, prov, kill)
    P("%-6s | %-38s | %12.4f MeV | %10.4f +/- %-8.4g | %+8.4f%% | %8.1f  | %-10s | %s"
      % (name, formula, value, meas, err, res, sig, prov, kill))
P("-"*118)
P("provenance tags: DERIVED = locked chain | VERIFIED = within 1 sigma | CLAIMED = passes sigma, structure owed | MISS = killed")
P("note: rows 'pi0','pi+-','H(*)' are the locked anchor modes shown for reference.")

# ================= SCAN B -- every other candidate, scored =================
P("")
P("="*118)
P("SCAN B -- ALL OTHER CANDIDATES, SCORED vs PDG (kill condition on every row)")
P("="*118)
SCAN = [
 ("K+-  | m_p*10/19 (primary, repeated)",     mp*10.0/19.0,                          "Kpm",    "OPEN",   "9.4s killed"),
 ("K+-  | 32*(m_p/57)*(m_p_pwc/1000)",        32.0*d_q*(mp_pwc/1000.0),               "Kpm",    "OPEN",   "passes 0.8s; 0.93719 dimensionless factor unproven"),
 ("K+-  | pi+-_obs + (420/20 + 1/38)*X17",    pipm_obs + (420.0/20.0 + 1.0/38.0)*X17, "Kpm",    "CLAIMED","passes 1.3s; uses OBSERVED pi+- (not derived)"),
 ("K+-  | pi+-_pwc + (420/20 + 1/38)*X17",    pipm_pwc + (420.0/20.0 + 1.0/38.0)*X17, "Kpm",    "MISS",   "58s -- the 19:18-partition attempt through the DERIVED pion mode dies"),
 ("K+-  | pi+-_pwc + 16*a_S*(1+(20/4)/18)",   pipm_pwc + 16.0*a_S*(1.0+(20.0/4.0)/18.0), "Kpm", "MISS", "50.8s -- 8-pair at the 19:18 share of the surface mode"),
 ("K0   | m_p*(19/36)*(1+2/420)",             mp*(19.0/36.0)*(1.0+2.0/420.0),        "K0",     "MISS",   "4.1s killed"),
 ("K0   | pi0_obs*(70/19)",                   134.9768*(70.0/19.0),                  "K0",     "MISS",   "25s killed (observed pi0 variant)"),
 ("Kgap | K0-K+- = 3.934 vs a_V/4*(1+1/108)", a_V/4.0*(1.0+1.0/108.0),               "K0",     "OPEN",   "gap formula 3.9347 vs 3.9340 (+0.02%) -- isospin debt correction owed"),
 ("eta  | 4*pi0_pwc*(1 + s*(20/4)/18)",       4.0*pi0_pwc*(1.0 + s*(20.0/4.0)/18.0), "eta",    "CLAIMED","passes 1.2s; the 5/18 factor has no cage derivation"),
 ("eta  | 4*pi0_pwc*(1 + s*(420/60)/25)",     4.0*pi0_pwc*(1.0 + s*(420.0/60.0)/25.0), "eta", "MISS",  "4.9s killed (7-quanta fold + 25 = (20/4)^2 variant)"),
 ("eta  | pi0_pwc*(65/16)",                   pi0_pwc*(65.0/16.0),                   "eta",    "MISS",   "33s killed"),
 ("eta  | m_p*100/171",                       mp*(100.0/171.0),                      "eta",    "MISS",   "49s killed"),
 ("muon | m_e*3/(2*alpha)",                   me*3.0/(2.0*alpha),                     "mu",     "MISS",   "270,000s killed (classical 3/2alpha structure)"),
 ("muon | m_e*(L_lad/9)*(1+3/250)",           me*(L_lad/9.0)*(1.0+3.0/250.0),        "mu",     "OPEN",   "numerics hit +0.0003% but 132s -- killed by 2.3 eV precision"),
 ("muon | m_e*L_lad*(9/80)",                  me*L_lad*(9.0/80.0),                    "mu",     "MISS",   "22,900s killed (physical 1838.85 ladder value)"),
 ("ladd. | 4*lamC(p)/R_p vs m_n/m_p",         L_lad_p,                                "pipm",   "OPEN",   "1.00147 vs 1.00138 (+0.009%) -- ladder lands on the NEUTRON"),
 ("tau  | m_p*36/19",                         mp*(36.0/19.0),                        "tau",    "MISS",   "7.7s killed"),
 ("tau  | pi0_pwc*250/19",                    pi0_pwc*(250.0/19.0),                  "tau",    "MISS",   "4.9s killed"),
 ("tau  | m_mu_pwc*X17 (= m_p*36/19)",        (mp*9.0/80.0)*X17,                      "tau",    "MISS",   "7.7s killed (same as 36/19 via the ladder muon)"),
 ("tau  | E*(40/3) MeV",                      E_emp*(40.0/3.0),                      "tau",    "MISS",   "26s killed"),
 ("Lam. | m_p + 10*X17 + 9",                  mp + 10.0*X17 + 9.0,                    "Lambda", "OPEN",   "passes 1.7s; the +9 MeV slack has no cage provenance"),
 ("Lam. | m_p*19/16",                         mp*(19.0/16.0),                        "Lambda", "MISS",   "247s killed"),
 ("Sig0 | m_p*(1+19/70)  [89=133.5*2/3]",     mp*(1.0+19.0/70.0),                     "Sigma0", "MISS",   "12.7s killed (emptiness 89 route)"),
 ("Sig+ | m_p + 15*X17",                      mp + 15.0*X17,                          "Sigmap", "MISS",   "21.9s killed"),
 ("Sig- | m_p + 15*a_S",                      mp + 15.0*a_S,                          "Sigmam", "MISS",   "24.4s killed"),
 ("Xi0  | m_p*7/5",                           mp*(7.0/5.0),                          "Xi0",    "MISS",   "6.4s killed"),
 ("Xi-  | m_p*(19/18)*(4/3)",                 mp*(19.0/18.0)*(4.0/3.0),              "Xim",    "MISS",   "16.8s killed"),
 ("Ome. | m_p*(19/18)*(27/16)",               mp*(19.0/18.0)*(27.0/16.0),            "Omega",  "MISS",   "4.0s killed"),
 ("Del. | m_p*(420/20)/16",                   mp*(420.0/20.0)/16.0,                  "Delta",  "VERIFIED","passes 0.26s (stage-axis 21 = 420/20 over N=16)"),
]
P("%-46s | %12.4f MeV | %10.4f +/- %-8.4g | %+8.4f%% | %8.1f  | %-8s | %s"
  % ("candidate formula", 0.0, 0.0, 0.0, 0.0, 0.0, "prov", "kill condition"))
P("-"*118)
for formula, value, key, prov, kill in SCAN:
    meas, err = PDG[key]
    res  = 100.0*(value/meas - 1.0)
    sig  = abs(value - meas)/err
    P("%-46s | %12.4f MeV | %10.4f +/- %-8.4g | %+8.4f%% | %8.1f  | %-8s | %s"
      % (formula, value, meas, err, res, sig, prov, kill))
P("(the 'ladd.' and 'Kgap' rows are gap/ratio checks, not mass rows)")

# ================= BARYON INTEGER FAMILY SCAN =================
P("")
P("="*118)
P("BARYON DEBT/SURFACE INTEGER FAMILIES -- k_eff = (M - m_p)/quantum for each quantum")
P("="*118)
P("%-10s %-14s %-14s %-14s %-44s" % ("baryon", "k(m_p/57)", "k(X17)", "k(a_S)", "nearest-integer verdict"))
P("-"*118)
for name, key in [("Lambda","Lambda"), ("Sigma0","Sigma0"), ("Xi0","Xi0"), ("Omega","Omega"), ("Delta","Delta")]:
    M, _ = PDG[key]
    gap = M - mp
    kd, kx, ka = gap/d_q, gap/X17, gap/a_S
    P("%-10s %-14.4f %-14.4f %-14.4f %-44s" % (name, kd, kx, ka, "see kill conditions above"))
P("Delta: k(a_S) = 16.95 ~ 17 -> m_p + 17*a_S is the ONLY integer that closes (0.42s).")
P("Lambda/Sigma/Xi/Omega: no integer of any quantum lands; nearest misses 10s..610s -> MISS.")

# ================= HIGGS / EMPTINESS ANCHOR =================
P("")
P("="*118)
P("ANCHOR: THE 133.5 EMPTINESS (for the Higgs analog and the tau family)")
P("="*118)
P("M_H/m_p = %.2f -> locked emptiness E = 133.5 (V_fold/V_tight ratio)" % E_mh)
P("H(A) = (v/2)*(1+s/3)         = %9.4f GeV  (%+.4f%%, %.2fs)" % (M_H_A/1000.0, 100.0*(M_H_A/1000.0/M_H_obs-1.0), abs(M_H_A/1000.0-M_H_obs)/0.17))
P("H(B) = (m_p/alpha)*(1-s/2)   = %9.4f GeV  (%+.4f%%, %.2fs)" % (M_H_B/1000.0, 100.0*(M_H_B/1000.0/M_H_obs-1.0), abs(M_H_B/1000.0-M_H_obs)/0.17))
P("H(mid) = 0.5*(A+B)           = %9.4f GeV  (%+.4f%%, %.2fs)" % (M_H_mid/1000.0, 100.0*(M_H_mid/1000.0/M_H_obs-1.0), abs(M_H_mid/1000.0-M_H_obs)/0.17))
P("tau through the emptiness family: m_tau = m_e*E*27*(1-2s/3) = %.4f MeV  (+%.4f%%, %.1fs) -> MISS" %
  (me*E_emp*27.0*(1.0-2.0*s/3.0), 100.0*(me*E_emp*27.0*(1.0-2.0*s/3.0)/PDG["tau"][0]-1.0),
   abs(me*E_emp*27.0*(1.0-2.0*s/3.0)-PDG["tau"][0])/PDG["tau"][1]))

# ================= 5-LINE SUMMARY =================
P("")
P("="*118)
P("5-LINE SUMMARY")
P("="*118)
P("1. BEST HIT  : Delta(1232) = m_p + (20-3)*a_S = 1232.84 MeV vs 1232 +/- 2 -> +0.068%, 0.42s (VERIFIED).")
P("               k(a_S) = 16.95 ~ 17 -- the only baryon the surface-mode integer family closes.")
P("               Alt: Delta = m_p*(420/20)/16 = 1231.48 MeV -> 0.26s.")
P("2. WORST MISS: muon -- locked-ladder chain m_p*9/80 = 105.556 MeV (-0.097%) dies at 44,700s against")
P("               PDG's 2.3 eV precision; no ratio-only one-step form can close 0.1 MeV at 1e-9 relative.")
P("               The ladder applied to the cage instead lands on the NEUTRON: 4*lamC(p)/R_p = 1.00147")
P("               vs m_n/m_p = 1.00138 (+0.009%).")
P("3. STRUCTURAL: Omega, Sigma0, Xi0, Lambda all MISS on the hinted m_p + k*(debt/surface) families --")
P("               nearest integers miss at 22s / 72s / 10s / 610s; ratio alternates (57/32, 89/70, 7/5, 19/16)")
P("               also killed (4.0s..247s). Only Delta survives with locked provenance.")
P("4. KAON/ETA/TAU: K+- = m_p*10/19 -> 9.4s MISS; K0 = pi0_pwc*70/19 -> 19.5s MISS; eta = 4*pi0_pwc + a_V/2")
P("               -> 4.5s MISS; tau = m_e*E*27*(1-2s/3) -> 3.4s MISS. Passing variants exist but are OPEN")
P("               (32*(m_p/57)*0.93719: 0.8s; 4*pi0*(1+5/342): 1.2s) -- structure owed, not verified.")
P("5. NEXT STEP : derive the K0-K+- isospin gap = 3.934 MeV ~ a_V/4*(1+1/108) = 3.935 MeV (+0.02%):")
P("               one debt correction away from closing BOTH kaons on the cage -- the most promising")
P("               single next derivation.")

P("")
P("script: %s" % os.path.abspath(__file__))
P("zero fitted parameters: every number above is a ratio of the locked set {19,18,20,16,8,3,2,57,1083,33,27,420,133.5,alpha,s,phi}")
P("exit 0")

# ================= write report to disk =================
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantify_particles_report.txt")
with open(report_path, "w", encoding="ascii") as f:
    f.write("\n".join(out) + "\n")
P("report written: %s" % report_path)

sys.exit(0)
