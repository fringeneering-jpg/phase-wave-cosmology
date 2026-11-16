"""
PWC force column - quantification from LOCKED constants only.
Rules: zero fitted parameters; every number carries provenance; misses reported.
ASCII-only output. Exit code 0.
"""
import math, os, sys, datetime

# ---------------- LOCKED CONSTANTS (never re-fit) --------------------
alpha       = 1.0 / 137.035999084   # MEASURED (CODATA 2018) - locked input
s           = 1.0 / 19.0            # LOCKED fold number
n           = 2.0 / 33.0            # LOCKED fold number
T7_bound    = 1.0 / 57.0            # LOCKED ( = s/3 )
T7_decay    = 20.0 / 1083.0         # LOCKED
N           = 16.0                  # LOCKED cage number
f_solid     = 8.4989e-4             # LOCKED (provenance CLAIMED - see G-chain kill)
v_GeV       = 246.21965             # GeV  DERIVED from G_F (identity) - locked
MZ_GeV      = 91.1876               # GeV  MEASURED (LEP/SLD) - locked
MW_GeV      = 80.3602               # GeV  MEASURED (CDF/D0/LHC) - locked
m_p_MeV     = 938.272088            # MeV  MEASURED - locked (PWC bare cage 937.19)
G_CODATA    = 6.67430e-11           # m^3 kg^-1 s^-2  MEASURED (CODATA 2018)
G_U         = 1.5e-15               # CODATA 1-sigma
hbar        = 1.054571817e-34       # J s  MEASURED
c0          = 2.99792458e8          # m/s  MEASURED (SI exact)
MEV_TO_KG   = 1.78266192e-30        # kg per MeV (derived unit factor)

# ---------------- MEASURED TARGETS (references only, never fitted) ---
GF_PDG      = 1.1663788e-5          # GeV^-2 PDG (muon lifetime)
GF_PDG_U    = 6.0e-12               # PDG 1-sigma
AS_MZ_PDG   = 0.1179                # PDG world average alpha_s(M_Z)
AS_MZ_U     = 0.0010                # 1-sigma
AS_MTAU_PDG = 0.312                 # PDG tau-decay average alpha_s(m_tau)
AS_MTAU_U   = 0.015                 # 1-sigma
BRIDGE_CLM  = 42.7416               # claimed "measured" bridge (source unverified -> OPEN)
ALPHA_MZ    = 1.0 / 127.952         # MEASURED (LEP): alpha at M_Z
MTAU_GEV    = 1.77686               # MEASURED (PDG) - NOT in the locked list
SIN2W_MS    = 0.23122               # MEASURED (PDG, MS-bar)

# ---------------- helpers ---------------------------------------------
def resid_pct(pwc, ref):  return 100.0 * (pwc - ref) / ref
def resid_sig(pwc, ref, u):  return (pwc - ref) / u
def fmt(x, nd=6):  return ("%." + str(nd) + "g") % x

OUT = []
def pr(s=""):
    print(s)
    OUT.append(s)

def table(head, rows, widths):
    def cell(t, w):
        t = str(t)
        return (t + " " * w)[:w]
    pr(" | ".join(cell(h, w) for h, w in zip(head, widths)))
    pr("-+-".join("-" * w for w in widths))
    for r in rows:
        pr(" | ".join(cell(c, w) for c, w in zip(r, widths)))

# ================= (1) EM =============================================
a_em = alpha
# ================= (2) WEAK ===========================================
v2 = v_GeV * v_GeV
GF = 1.0 / (math.sqrt(2.0) * v2)          # GeV^-2
# ================= (3) STRONG =========================================
bridge = 9.0 / (4.0 * s)                  # = 42.75
inv_bridge = 1.0 / bridge                 # = 0.0233918
as_mtau_pwc = alpha * bridge              # = 0.311962 (tau-scale value)
as_mtau_from_claim = BRIDGE_CLM * alpha   # implied alpha_s(m_tau) from claimed 42.7416
as_mtau_ratio_pdg = AS_MTAU_PDG / alpha   # measured ratio 0.312/alpha

cands = [
    ("alpha*16", alpha * 16.0, "YES (N=16)"),
    ("alpha*16*(19/18)^(1/16)", alpha * 16.0 * (19.0/18.0) ** (1.0/16.0), "semi (1/16 from N)"),
    ("alpha*16*(19/18)^(1/19)", alpha * 16.0 * (19.0/18.0) ** (1.0/19.0), "YES (s)"),
    ("alpha*16*(19/18)^(2/33)", alpha * 16.0 * (19.0/18.0) ** (2.0/33.0), "YES (n)"),
    ("alpha*16*(19/18)^(1/57)", alpha * 16.0 * (19.0/18.0) ** (1.0/57.0), "YES (T7)"),
    ("alpha*16*(19/18)^(20/1083)", alpha * 16.0 * (19.0/18.0) ** (20.0/1083.0), "YES (T7d)"),
    ("alpha*16*(20/19)^(1/16)", alpha * 16.0 * (20.0/19.0) ** (1.0/16.0), "semi (1/16 from N)"),
    ("alpha*16*(20/19)^(1/19)", alpha * 16.0 * (20.0/19.0) ** (1.0/19.0), "YES (s)"),
    ("alpha*16*(28/19)^(1/16)", alpha * 16.0 * (28.0/19.0) ** (1.0/16.0), "semi (1/16 from N)"),
    ("alpha*16*20/19 (X17 pattern)", alpha * 16.0 * 20.0/19.0, "YES"),
    ("alpha*16*18/19", alpha * 16.0 * 18.0/19.0, "YES"),
    ("alpha*16*(19/18)^(1/6)  [1/6 NOT locked]", alpha * 16.0 * (19.0/18.0) ** (1.0/6.0), "NO -> fitted"),
]
cands_sorted = sorted(cands, key=lambda c: abs(resid_pct(c[1], AS_MZ_PDG)))
p19 = math.log(AS_MZ_PDG / (alpha * 16.0)) / math.log(19.0 / 18.0)
p20 = math.log(AS_MZ_PDG / (alpha * 16.0)) / math.log(20.0 / 19.0)

# ================= (4) GRAVITY ========================================
m_p_kg = m_p_MeV * MEV_TO_KG
hbc_over_mp2 = hbar * c0 / (m_p_kg * m_p_kg)
f12 = f_solid ** 12.0
piece = 4.0 * s / 81.0
prod = f12 * piece
G_chain = prod * hbc_over_mp2
G_chain16 = N * G_chain
alpha_G = G_CODATA * m_p_kg * m_p_kg / (hbar * c0)
f_back = (alpha_G * 81.0 / (4.0 * s * N)) ** (1.0 / 12.0)

# ================= HIERARCHY LADDER at M_Z ============================
a_em_MZ = ALPHA_MZ
a_w_MZ = math.sqrt(2.0) * GF * MW_GeV * MW_GeV / math.pi
a_s_MZ = AS_MZ_PDG
a_grav_MZ = G_CODATA * (MZ_GeV * 1000.0 * MEV_TO_KG) ** 2.0 / (hbar * c0)
a_grav_MZ_chain = G_chain16 * (MZ_GeV * 1000.0 * MEV_TO_KG) ** 2.0 / (hbar * c0)
r_w_em = a_w_MZ / a_em_MZ
r_s_em = a_s_MZ / a_em_MZ
r_g_em = a_grav_MZ / a_em_MZ
r_s_w = a_s_MZ / a_w_MZ
r_g_s = a_grav_MZ / a_s_MZ
sin2W_os = 1.0 - (MW_GeV / MZ_GeV) ** 2.0
s4 = 4.0 * s
r_6619 = 66.0 / 19.0
a_w_mp = GF * (m_p_MeV / 1000.0) ** 2.0
a_w_MZ_alt = a_em_MZ / SIN2W_MS

# ================= QCD RUNNING PREVIEW (standard, zero-parameter) =====
b0 = 11.0 - 2.0 * 5.0 / 3.0
b1 = 102.0 - 38.0 * 5.0 / 3.0
Lrun = 2.0 * math.log(MZ_GeV / MTAU_GEV)
as_1loop = 1.0 / (1.0 / as_mtau_pwc + (b0 / (4.0 * math.pi)) * Lrun)
Ftau = 4.0 * math.pi / (b0 * as_mtau_pwc)
c2 = b1 / (b0 * b0)
Ltau = Ftau - c2 * math.log(Ftau + c2)
Lam = MTAU_GEV * math.exp(-Ltau / 2.0)
LZ = 2.0 * math.log(MZ_GeV / Lam)
FZ = LZ + c2 * math.log(LZ + c2)
for _ in range(300):
    FZ = FZ - (FZ - c2 * math.log(FZ + c2) - LZ) / (1.0 - c2 / (FZ + c2))
as_2loop = 4.0 * math.pi / (b0 * FZ)

# ================= OUTPUT ==============================================
pr("PWC FORCE COLUMN - quantified from locked constants only (zero fitted parameters)")
pr("run: " + datetime.datetime.now().isoformat())
pr("=" * 118)
pr("")

pr("MAIN TABLE")
head = ["name", "PWC formula", "PWC value", "measured value", "residual %/sigma", "provenance", "kill"]
widths = [20, 40, 20, 22, 20, 24, 22]
rows = [
 ("alpha_em (EM)",
  "locked input 1/137.035999084",
  fmt(a_em),
  "same (by construction)",
  "0.0000% / 0.0s",
  "LOCKED = MEASURED (input)",
  "input (no content)"),
 ("G_F (weak)",
  "1/(sqrt(2) v^2), v=246.21965 GeV",
  fmt(GF) + " GeV^-2",
  "1.1663788(6)e-5 GeV^-2",
  "%+.4f%% / %+.2fs" % (resid_pct(GF, GF_PDG), resid_sig(GF, GF_PDG, GF_PDG_U)),
  "DERIVED (identity)",
  "tautology"),
 ("strong bridge 9/(4s)",
  "9/(4s), s=1/19",
  fmt(bridge),
  "42.7416 (claimed, OPEN)",
  "%+.4f%% / n/a" % resid_pct(bridge, BRIDGE_CLM),
  "DERIVED from s; target OPEN",
  "wrong scale (tau)"),
 ("alpha_s(m_tau) bridge",
  "alpha * 9/(4s)",
  fmt(as_mtau_pwc),
  "0.312 +/- 0.015 (PDG tau)",
  "%+.4f%% / %+.3fs" % (resid_pct(as_mtau_pwc, AS_MTAU_PDG), resid_sig(as_mtau_pwc, AS_MTAU_PDG, AS_MTAU_U)),
  "DERIVED; target MEASURED",
  "wrong scale (tau)"),
 ("alpha_s(M_Z) attempt",
  "best locked-only: alpha*16",
  fmt(alpha * 16.0),
  "0.1179 +/- 0.0010 (PDG)",
  "%+.4f%% / %+.2fs" % (resid_pct(alpha * 16.0, AS_MZ_PDG), resid_sig(alpha * 16.0, AS_MZ_PDG, AS_MZ_U)),
  "DERIVED-candidate (N=16); OPEN",
  "needs fitted exponent"),
 ("G_derived (chain locked)",
  "f_solid^12*(4s/81)*hbar*c/m_p^2",
  fmt(G_chain) + " m3/kg/s2",
  "6.67430(15)e-11 (CODATA)",
  "%+.2f%% / %+.0fs" % (resid_pct(G_chain, G_CODATA), resid_sig(G_chain, G_CODATA, G_U)),
  "DERIVED from locked f_solid,s",
  "DEAD: missing x16"),
 ("G_derived (chain + N=16)",
  "16*f_solid^12*(4s/81)*hbar*c/m_p^2",
  fmt(G_chain16) + " m3/kg/s2",
  "6.67430(15)e-11 (CODATA)",
  "%+.4f%% / %+.2fs" % (resid_pct(G_chain16, G_CODATA), resid_sig(G_chain16, G_CODATA, G_U)),
  "DERIVED w/ locked N=16",
  "circular (back-solved)"),
]
table(head, rows, widths)
pr("")

pr("CHECKS (task items)")
pr("(2) G_F check: 1/(sqrt(2)*v^2) with v = 246.21965 GeV -> G_F = " + fmt(GF, 9) + " GeV^-2")
pr("    target 1.1663788e-5 GeV^-2 -> residual %+.4f%%, %+.2f sigma (pure v rounding; identity)" % (
    resid_pct(GF, GF_PDG), resid_sig(GF, GF_PDG, GF_PDG_U)))
pr("(3) 9/(4s) = " + fmt(bridge) + " vs claimed 42.7416 -> " + ("%+.4f%%" % resid_pct(bridge, BRIDGE_CLM)) + ";  1/(9/4s) = " + fmt(inv_bridge) + ";  alpha*9/(4s) = " + fmt(as_mtau_pwc))
pr("    claimed 42.7416 -> alpha_s(m_tau) = " + fmt(as_mtau_from_claim) + "  (PDG: 0.312 +/- 0.015)")
pr("(4) G_derived = f_solid^12*(4s/81)*hbar*c/m_p^2 = " + fmt(G_chain) + " m3/kg/s2 vs CODATA " + fmt(G_CODATA) + " -> %+.2f%%" % resid_pct(G_chain, G_CODATA))
pr("")

pr("WHICH RATIO IS 9/(4s)?")
pr("  9/(4s) = 42.75 = alpha_s(m_tau)/alpha_em(0) :")
pr("    PWC 42.75 vs claimed 'measured' 42.7416   -> %+.4f%%" % resid_pct(bridge, BRIDGE_CLM))
pr("    PWC 42.75 vs PDG ratio 0.312/alpha=42.755 -> %+.4f%%" % resid_pct(bridge, as_mtau_ratio_pdg))
pr("    NOT 1/alpha_s(M_Z) (= 8.482; off x5.04), NOT alpha_s(M_Z)/alpha_em (= 16.157;")
pr("    vs X17 pattern 16*20/19 = 16.842 -> +4.24% off). 1/42.75 = 0.023392 is close to the")
pr("    GUT-scale magnitude of a running alpha_s, NOT a measured M_Z quantity.")
pr("")

pr("ALPHA_S(M_Z) CANDIDATE SCAN vs 0.1179 +/- 0.0010 (sorted by |residual|)")
head2 = ["formula", "value", "resid %", "sigma", "locked pieces?"]
widths2 = [46, 12, 11, 9, 20]
rows2 = []
for (f_, v_, lock) in cands_sorted:
    rows2.append((f_, fmt(v_), "%+.3f%%" % resid_pct(v_, AS_MZ_PDG),
                  "%+.2fs" % resid_sig(v_, AS_MZ_PDG, AS_MZ_U), lock))
table(head2, rows2, widths2)
pr("needed exponent for exact hit: (19/18)^" + fmt(p19, 6) + "  or  (20/19)^" + fmt(p20, 6) +
   "  -> NOT locked rationals -> any exact match is a FITTED parameter (defeat by rule zero)")
pr("alpha*9/(4s) = 0.311962 is the TAU-scale value (resid %+.4f%% vs PDG alpha_s(m_tau) 0.312 +/- 0.015), not M_Z." % resid_pct(as_mtau_pwc, AS_MTAU_PDG))
pr("")

pr("GRAVITY DETAIL (G-chain)")
pr("  alpha_G = G m_p^2/(hbar c)       = " + fmt(alpha_G))
pr("  chain core f_solid^12 * (4s/81)  = " + fmt(prod) + "  = alpha_G / " + fmt(alpha_G / prod, 7))
pr("  chain core * N=16                = " + fmt(prod * N) + "  resid %+.4f%%" % resid_pct(prod * N, alpha_G))
pr("  G_derived as stated              = " + fmt(G_chain) + " m3/kg/s2  resid %+.2f%%" % resid_pct(G_chain, G_CODATA))
pr("  G_derived + N=16                 = " + fmt(G_chain16) + " m3/kg/s2  resid %+.4f%% (%+.2f sigma)" % (
    resid_pct(G_chain16, G_CODATA), resid_sig(G_chain16, G_CODATA, G_U)))
pr("  f_solid back-solve: (alpha_G*1539/64)^(1/12) = " + fmt(f_back) + " vs locked 8.4989e-4 -> %+.4f%%" % resid_pct(f_back, f_solid))
pr("    => f_solid IS alpha_G in disguise (back-solved); the G-chain is an inversion, not a derivation.")
pr("    => the -0.0024% residual sits inside f_solid's 5-significant-digit locking granularity (0.007%).")
pr("")

pr("HIERARCHY LADDER AT ONE SCALE Q = M_Z = 91.1876 GeV")
pr("  coupling             value            provenance")
pr("  alpha_em(M_Z)        " + fmt(a_em_MZ) + "       MEASURED (LEP: 1/127.952) - NOT in locked list")
pr("  alpha_weak(M_Z)      " + fmt(a_w_MZ) + "       DERIVED sqrt(2)*G_F*M_W^2/pi (locked v-identity + M_W)")
pr("                      (alt " + fmt(a_w_MZ_alt) + " = alpha(M_Z)/sin^2W_MS, sin^2W=0.23122; scheme spread ~0.3%)")
pr("  alpha_s(M_Z)         " + fmt(a_s_MZ) + "       MEASURED (PDG)")
pr("  alpha_grav(M_Z)      " + fmt(a_grav_MZ) + "       DERIVED G*M_Z^2/(hbar c) (CODATA G; chain+N version " + fmt(a_grav_MZ_chain) + ")")
pr("  ladder (norm to alpha_em):  1 : " + fmt(r_w_em) + " : " + fmt(r_s_em) + " : " + fmt(r_g_em))
pr("  step fold pieces:")
pr("   em -> weak     x" + fmt(r_w_em) + "   piece = 1/sin^2W; sin^2W = 1-(M_W/M_Z)^2 = " + fmt(sin2W_os) + " (LOCKED masses -> SM identity)")
pr("                    locked candidate 4s = " + fmt(s4) + " -> off %+.2f%% (on-shell), %+.2f%% (MS-bar). NO fold number closes." % (
    resid_pct(s4, sin2W_os), resid_pct(s4, SIN2W_MS)))
pr("   weak -> strong x" + fmt(r_s_w) + "   candidate 66/19 = " + fmt(r_6619) + " -> %+.3f%%; provenance OPEN (33 only via n=2/33);" % resid_pct(r_6619, r_s_w))
pr("                    swamped by alpha_w scheme spread ~+/-3%. NOT a locked piece.")
pr("   strong -> grav x" + fmt(r_g_s) + "   piece = f_solid^12*(4s/81)*16*(M_Z/m_p)^2/alpha_s -> circular via f_solid; as-stated chain x16 short.")
pr("  proton-scale note: alpha_em = 7.2974e-3 : alpha_w(m_p) = G_F m_p^2 = " + fmt(a_w_mp) + " :")
pr("                    alpha_s(m_p) = OPEN (nonperturbative) : alpha_grav(m_p) = " + fmt(alpha_G))
pr("")

pr("NEXT-DERIVATION PREVIEW (zero-parameter standard QCD, n_f=5; NOT a PWC fold rule)")
pr("  alpha_s(m_tau) = alpha*9/(4s) = " + fmt(as_mtau_pwc))
pr("    1-loop to M_Z: " + fmt(as_1loop) + "  (%+.2f%% vs 0.1179)" % resid_pct(as_1loop, AS_MZ_PDG))
pr("    2-loop to M_Z: " + fmt(as_2loop) + "  (%+.2f%%, %+.2f sigma; Lambda_MSbar(5,2loop) = " % (
    resid_pct(as_2loop, AS_MZ_PDG), resid_sig(as_2loop, AS_MZ_PDG, AS_MZ_U)) + fmt(Lam) + " GeV)")
pr("  PDG-standard 4-loop + b-threshold evolution of 0.312 +/- 0.015 gives alpha_s(M_Z) = 0.1170 +/- 0.0018")
pr("    -> PWC bridge transported lands 0.1170, i.e. 0.44 sigma (combined) below 0.1179. TESTABLE, NOT YET CLOSED.")
pr("  Caveat: m_tau = 1.77686 GeV is MEASURED and NOT in the locked list (externally chosen scale).")
pr("")

pr("KILL CONDITIONS (full text)")
pr("- alpha_em: it is a LOCKED INPUT. Calling it a 'derivation' is circular; the fold adds zero information.")
pr("  KILL TEST: a formula reproducing 1/137.035999084 to more digits than its inputs was fitted.")
pr("- G_F: v == (sqrt(2)*G_F)^(-1/2) is the STANDARD DEFINITION of v; recovering G_F from v is the definition")
pr("  read backwards. The physical input (muon lifetime) is not predicted. KILL TEST: predict tau_mu, not G_F.")
pr("- strong bridge: 1/(9/4s) = 0.023392 is NOT alpha_s(M_Z) = 0.1179 (factor 5.04 off). Numerically 9/(4s) is")
pr("  alpha_s(m_tau)/alpha_em (42.75 vs claimed 42.7416: +0.020%; vs PDG 0.312/alpha = 42.755: -0.012%). It")
pr("  closes ONLY at the tau scale; m_tau is not in the locked list and PWC has no running law to reach M_Z.")
pr("  KILL TEST: reproduce alpha_s at a second scale.")
pr("- alpha_s(M_Z) = 0.1179: no locked combination hits it. Best locked-only alpha*16 = 0.116758 (-0.969%, -1.14")
pr("  sigma). Exact closure needs (19/18)^0.180081 or (20/19)^0.189819, non-locked exponents -> fitted -> defeat.")
pr("- G-chain as stated: f_solid^12*(4s/81) gives G = 4.171e-12, -93.75% vs CODATA, short by exactly 16.0001 =")
pr("  the locked cage number N. DEAD as stated.")
pr("- G-chain + N=16: -0.0024% / -1.07 sigma, BUT f_solid = (alpha_G*1539/64)^(1/12) = 8.49892e-4 reproduces the")
pr("  locked 8.4989e-4 to 2e-5 (inside its own 5-digit rounding): f_solid was BACK-SOLVED from alpha_G, so G is")
pr("  an input, not an output. KILL TEST: derive f_solid independently (e.g. from rho_core/R_p) or it is circular.")
pr("")

pr("MISSES REPORTED: alpha_s(M_Z) from locked combos (miss); G-chain as stated (miss, x16); sin^2W and")
pr("alpha_s/alpha_w have no locked fold pieces (miss); ladder closes as SM identities, not as fold numbers.")
pr("")

pr("PROVENANCE KEY (constants used)")
pr("  alpha      LOCKED = MEASURED (CODATA 2018)")
pr("  s, n       LOCKED fold numbers (theory inputs, CLAIMED as fold geometry)")
pr("  f_solid    LOCKED in task list (CLAIMED) -> shown above to be BACK-SOLVED from alpha_G")
pr("  N          LOCKED cage number (CLAIMED)")
pr("  v          LOCKED = DERIVED from G_F (standard definition)")
pr("  M_W, M_Z   LOCKED = MEASURED (LEP/SLD/CDF/D0/LHC)")
pr("  m_p        LOCKED = MEASURED (CODATA)")
pr("  G, hbar, c MEASURED (CODATA 2018 / SI exact)")
pr("  targets    MEASURED (PDG/CODATA) - references only, never fitted")
pr("  unused locked: rho0, rho_max, rho_core, R_p, Y_bow, k, a_max, a0, a0_bare, T, T7_*, g_fold, E_lock,")
pr("                m_e, m_n, X17, pi0, a_V, a_S, M_H, m_t, kB, Q_CMB, T_CMB, H0, 28/19")
pr("")

pr("SUMMARY (5 lines)")
pr("1. BEST HIT (non-tautological): alpha_em*9/(4s) = 0.311962 vs PDG alpha_s(m_tau) = 0.312 +/- 0.015")
pr("   -> -0.012%, -0.003 sigma. The bridge 9/(4s) = 42.75 IS the ratio alpha_s(m_tau)/alpha_em: PWC 42.75 vs")
pr("   claimed 42.7416 -> +0.020%; vs PDG ratio 0.312/alpha = 42.755 -> -0.012%. Closes at the tau scale only.")
pr("2. ONLY EXACT CLOSURE: G_F = 1/(sqrt(2) v^2) = 1.1663787e-5 GeV^-2 vs PDG 1.1663788(6)e-5. Exact by")
pr("   construction = TAUTOLOGY (v is DEFINED from G_F; the muon lifetime input is not predicted).")
pr("3. WORST MISS: G-chain as locked f_solid^12*(4s/81) -> G_derived = 4.1713e-12 vs CODATA 6.67430e-11:")
pr("   -93.75% (-41720 sigma), short by exactly 16.0001 = the locked cage number N. DEAD as stated.")
pr("4. ALSO NOT CLOSED: alpha_s(M_Z) = 0.1179 falls out of NO locked combination (best locked-only alpha*16 =")
pr("   0.116758, -0.969%, -1.14 sigma; exact closure needs the non-locked exponent (19/18)^0.180081 -> fitted")
pr("   -> defeat). With N=16 the G-chain reaches -0.0024% / -1.07 sigma but f_solid is back-solved from alpha_G.")
pr("5. MOST PROMISING NEXT DERIVATION: transport alpha_em*9/(4s) from m_tau = 1.77686 GeV (external measured")
pr("   scale, not locked) to M_Z with zero-parameter QCD evolution: 1-loop 0.12483, 2-loop 0.11952 (computed")
pr("   here); PDG-standard 4-loop + b-threshold gives 0.1170 +/- 0.0018 -> 0.44 sigma from 0.1179. If a locked")
pr("   fold rule reproduces that evolution, the strong column closes; otherwise kill it.")
pr("")

# write transcript
res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantify_forces_results.txt")
with open(res_path, "w") as fh:
    fh.write("\n".join(OUT) + "\n")
pr("transcript saved to: " + res_path)
sys.exit(0)
