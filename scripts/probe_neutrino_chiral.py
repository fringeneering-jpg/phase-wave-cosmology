"""
probe_neutrino_chiral.py -- PWC probe: chiral-charge-opposite neutrino mechanism.

Author's ruling under test (Phase Wave Cosmology):
  the neutrino is the same 720-degree chiral fold as the electron, but its
  winding went the opposite way, so the charge winds against itself:
  (+e) + (-e) = 0.

Consequences probed:
  T1 charge cancellation   -> exact algebra (sympy)
  T2 mass residual         -> six prescribed zero-parameter candidates + 2 extras
  T3 oscillation lengths   -> Delta m^2 pattern IF a locked ordering exists
  T4 left-handedness       -> claimed consequence, no arithmetic
  T5 three generations     -> does the fold structure emit three chiral orders?
  T6 verdict               -> checkable number within 2 orders, or mechanism-only?

Rules: ZERO fitted parameters. Provenance per number. Misses reported, never
hidden. Kill conditions per candidate. Exit 0.
"""

import math
import sys
import sympy as sp

# ---------------------------------------------------------------------
# LOCKED SET (PWC locked constants + CODATA). Nothing below is fitted.
# ---------------------------------------------------------------------
C0    = 2.99792458e8        # m/s                [CODATA]
HBAR  = 1.054571817e-34     # J s                [CODATA]
S     = 1.0 / 19.0          # fold coupling      [PWC locked]
N     = 16                  #                    [PWC locked]
T     = 27                  #                    [PWC locked]
T7B   = 1.0 / 57.0          # = 1/(3*19)         [PWC locked]
T7D   = 20.0 / 1083.0       # = (1+s)*T7b        [PWC locked]
ALPHA = 1.0 / 137.035999084 # fine structure     [CODATA]
M_E   = 0.51099895          # MeV, electron      [CODATA]
M_P   = 938.272088          # MeV, proton        [CODATA]
DELTA = 1.5321e-5           # golden-bridge residual [PWC locked]
X17   = 16.8421             # MeV                [PWC locked]
DU    = 2.470               # eV, 502 nm frustration [PWC locked]
EV_J  = 1.602176634e-19     # J/eV               [CODATA]

M_E_EV = M_E * 1.0e6        # 510998.95 eV
WELD_HEAT_EV = M_E_EV       # m_e*c0^2 = 8.1871e-14 J = 510998.95 eV (identity)

# Measured neutrino observables (standard values; targets only, never fitted)
SUM_BOUND = 0.12            # eV    cosmological sum of masses upper bound
DM21SQ    = 7.42e-5         # eV^2  solar splitting (NuFIT standard)
DM31SQ    = 2.51e-3         # eV^2  atmospheric |splitting| (NuFIT standard)
SQ_DM21   = math.sqrt(DM21SQ)            # 8.614 meV
SQ_DM31   = math.sqrt(DM31SQ)            # 50.10 meV
GEO_SPLIT = math.sqrt(SQ_DM21 * SQ_DM31) # 20.77 meV (derived target)

def dex(c, t):
    return math.log10(abs(c / t))

def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)

# =====================================================================
# T1  CHARGE CANCELLATION -- exact algebra
# =====================================================================
banner("T1  CHARGE CANCELLATION (exact algebra, sympy)")
e = sp.Symbol('e', positive=True)
q_fwd  = +e          # forward winding carries +e
q_back = -e          # opposite winding carries -e
q_tot  = sp.simplify(q_fwd + q_back)
w_tot  = sp.simplify(4 * sp.pi + (-4) * sp.pi)
print("  forward winding charge  : +e")
print("  opposite winding charge : -e")
print("  neutrino charge         : (+e) + (-e) =", q_tot, "   (exact zero)")
print("  winding-angle sum       : +720 deg + (-720 deg) =", w_tot, "rad (exact zero)")
print("  Status: EXACT -- but by construction.  The mechanism ASSUMES the")
print("  opposite winding, so neutrality is a bookkeeping identity, not a")
print("  falsifiable prediction.  Consistent with the bound |q_nu| < ~1e-14 e.")

# =====================================================================
# T2  MASS RESIDUAL -- six prescribed candidates (+ two locked extras)
# =====================================================================
banner("T2  MASS RESIDUAL: zero-parameter neutrino-mass-scale candidates")
c1A = WELD_HEAT_EV * DELTA              # reading A: (m_e*c0^2) * delta
c1B = WELD_HEAT_EV * DELTA * DELTA      # reading B: residual(=delta*m_e*c0^2) * delta
c2  = S * DELTA * M_E_EV
c3  = DELTA * M_E_EV
c4  = T7B * DELTA * M_E_EV
c5  = DELTA * DELTA * M_E_EV
c6  = S * S * DELTA * M_E_EV
cX1 = T7D * DELTA * M_E_EV             # extra locked probe
cX2 = (T7D - T7B) * DELTA * M_E_EV     # extra locked probe (= s*T7b*delta*m_e)

print("  weld heat m_e*c0^2 = 8.1871e-14 J = %.2f eV  [identity, CODATA]" % M_E_EV)
print("  NOTE: the six prescribed candidates collapse to FIVE distinct numbers,")
print("  because every reading of 'weld-heat residual x delta' coincides with")
print("  another listed candidate:")
print("    reading A: (m_e*c0^2)*delta        = delta*m_e   -> candidate 3")
print("    reading B: delta*(m_e*c0^2)*delta  = delta^2*m_e -> candidate 5")
print("    reading C: s*(m_e*c0^2)*delta      = s*delta*m_e -> candidate 2")

def show(name, formula, val):
    print("  %-38s %-30s = %.6g eV  (%.6g meV)"
          % (name, formula, val, val * 1e3))
    print("      vs sum bound %.3f eV      : x%.3g (%+.2f dex)"
          % (SUM_BOUND, val / SUM_BOUND, dex(val, SUM_BOUND)))
    print("      vs sqrt(dm21^2) = %.4g eV : x%.3g (%+.2f dex)"
          % (SQ_DM21, val / SQ_DM21, dex(val, SQ_DM21)))
    print("      vs sqrt(dm31^2) = %.4g eV : x%.3g (%+.2f dex)"
          % (SQ_DM31, val / SQ_DM31, dex(val, SQ_DM31)))

show("1.  weld-heat residual x delta  [A]", "(m_e*c0^2)*delta", c1A)
show("1'. weld-heat residual x delta  [B]", "(m_e*c0^2)*delta^2", c1B)
show("2.  s*delta*m_e", "s*delta*m_e,  s = 1/19", c2)
show("3.  delta*m_e", "delta*m_e", c3)
show("4.  T7b*delta*m_e", "T7b*delta*m_e,  T7b = 1/57", c4)
show("5.  delta^2*m_e", "delta^2*m_e", c5)
show("6.  s^2*delta*m_e", "s^2*delta*m_e,  s^2 = 1/361", c6)
show("X1. T7d*delta*m_e            [extra]", "T7d*delta*m_e,  T7d = 20/1083", cX1)
show("X2. (T7d-T7b)*delta*m_e      [extra]", "(1/1083)*delta*m_e = s*T7b*delta*m_e", cX2)

# ---------------------------------------------------------------------
banner("TABLE: candidate | formula | value | target | residual | status | kill condition")

rows = [
    ("1.  weld-heat residual x delta [A]", "(m_e*c0^2)*delta",
     "%.4f eV" % c1A, "sum bound 0.12 eV",
     "%+.2f dex (x%.3g)" % (dex(c1A, SUM_BOUND), c1A / SUM_BOUND),
     "KILL", "65x above sum bound; duplicate of candidate 3"),
    ("1'. weld-heat residual x delta [B]", "(m_e*c0^2)*delta^2",
     "%.4e eV (%.4f meV)" % (c1B, c1B * 1e3), "sqrt(dm21^2) 8.61 meV",
     "%.2f dex (x%.3g low)" % (dex(c1B, SQ_DM21), SQ_DM21 / c1B),
     "KILL", "72x below nearest split; duplicate of candidate 5"),
    ("2.  s*delta*m_e", "s*delta*m_e, s=1/19",
     "%.5f eV (%.1f meV)" % (c2, c2 * 1e3), "sum bound 0.12 eV",
     "%+.2f dex (x%.3g)" % (dex(c2, SUM_BOUND), c2 / SUM_BOUND),
     "KILL", "3.4x above sum bound"),
    ("3.  delta*m_e", "delta*m_e",
     "%.4f eV" % c3, "sum bound 0.12 eV",
     "%+.2f dex (x%.3g)" % (dex(c3, SUM_BOUND), c3 / SUM_BOUND),
     "KILL", "65x above sum bound; ~10x above KATRIN 0.8 eV"),
    ("4.  T7b*delta*m_e", "T7b*delta*m_e, T7b=1/57",
     "%.5f eV (%.1f meV)" % (c4, c4 * 1e3), "sum bound 0.12 eV",
     "%+.3f dex (x%.3g)" % (dex(c4, SUM_BOUND), c4 / SUM_BOUND),
     "MARGINAL MISS", "bound violated by 14.5%; no locked 0.87x fix"),
    ("5.  delta^2*m_e", "delta^2*m_e",
     "%.4e eV (%.4f meV)" % (c5, c5 * 1e3), "sqrt(dm21^2) 8.61 meV",
     "%.2f dex (x%.3g low)" % (dex(c5, SQ_DM21), SQ_DM21 / c5),
     "KILL", "72x below nearest split"),
    ("6.  s^2*delta*m_e", "s^2*delta*m_e, s^2=1/361",
     "%.6f eV (%.2f meV)" % (c6, c6 * 1e3), "geo-mean 20.77 meV",
     "%+.3f dex (x%.3g)" % (dex(c6, GEO_SPLIT), c6 / GEO_SPLIT),
     "ALIVE (BEST)", "none: sits inside [8.61, 50.1] meV, below 0.12 eV"),
    ("X1. T7d*delta*m_e  [extra]", "T7d*delta*m_e, T7d=20/1083",
     "%.5f eV (%.1f meV)" % (cX1, cX1 * 1e3), "sum bound 0.12 eV",
     "%+.3f dex (x%.3g)" % (dex(cX1, SUM_BOUND), cX1 / SUM_BOUND),
     "MARGINAL MISS", "bound violated by 20%"),
    ("X2. (T7d-T7b)*delta*m_e [extra]", "(T7d-T7b)*delta*m_e",
     "%.6f eV (%.2f meV)" % (cX2, cX2 * 1e3), "sqrt(dm21^2) 8.61 meV",
     "%.3f dex (x%.3g)" % (dex(cX2, SQ_DM21), cX2 / SQ_DM21),
     "NEAR MISS", "16% below sqrt(dm21^2); = candidate 6 / 3"),
]

hdr = ["candidate", "formula", "value", "target", "residual", "status", "kill condition"]
w = [36, 28, 26, 26, 22, 15]
line = " | ".join(h.ljust(w[i]) if i < 6 else h for i, h in enumerate(hdr))
print(line)
print("-" * (len(line) + 55))
for r in rows:
    print(" | ".join((r[i].ljust(w[i]) if i < 6 else r[i]) for i in range(7)))

# =====================================================================
# T3  OSCILLATION LENGTHS
# =====================================================================
banner("T3  OSCILLATION LENGTHS: does a residual-mass ordering emerge?")
print("  Locked-ordering check: the locked set contains exactly one multi-member")
print("  family: (T7b, T7d) with T7d/T7b = 20/19 = 1 + s = %.4f.  Two members, no" % (T7D / T7B))
print("  third, and no rule assigning them to mass orders.  The six prescribed")
print("  candidates are single scales, not a spectrum.")
print("  RESULT: NO LOCKED ORDERING EXISTS -> MISS (as expected).")
print()
print("  Illustrative assignment (EXPLICITLY NOT LOCKED, shown for completeness):")
print("  m1 = delta^2*m_e,  m2 = s^2*delta*m_e,  m3 = T7b*delta*m_e  (normal order)")
m1 = c5
m2 = c6
m3 = c4
dm21i = m2 * m2 - m1 * m1
dm31i = m3 * m3 - m1 * m1
print("  masses (meV): m1 = %.4f,  m2 = %.4f,  m3 = %.4f" % (m1 * 1e3, m2 * 1e3, m3 * 1e3))
print("  implied dm21^2 = %.4g eV^2  vs measured %.3g eV^2  -> x%.3g" % (dm21i, DM21SQ, dm21i / DM21SQ))
print("  implied dm31^2 = %.4g eV^2  vs measured %.3g eV^2  -> x%.3g" % (dm31i, DM31SQ, dm31i / DM31SQ))
print("  ratio dm31^2/dm21^2 = %.2f vs measured %.2f  (shape x%.2f)"
      % (dm31i / dm21i, DM31SQ / DM21SQ, (dm31i / dm21i) / (DM31SQ / DM21SQ)))
print("  sum of masses = %.1f meV vs bound 120 meV -> VIOLATED by x%.2f"
      % ((m1 + m2 + m3) * 1e3, (m1 + m2 + m3) * 1e3 / 120.0))
print("  oscillation lengths at E = 1 MeV  (L[km] = 2.48 * E[MeV] / dm^2[eV^2]):")
print("    implied L21 = %.0f km vs measured %.0f km ;  L31 = %.0f km vs measured %.0f km"
      % (2.48 / dm21i, 2.48 / DM21SQ, 2.48 / dm31i, 2.48 / DM31SQ))
print("  SCORE: MISS.  Both splittings ~6-7.5x too large, sum bound violated.")
print()
print("  Alternative s-power family  m_k = s^k * delta * m_e  (k = 4,3,2 ascending):")
m1b = S**4 * DELTA * M_E_EV
m2b = S**3 * DELTA * M_E_EV
m3b = S**2 * DELTA * M_E_EV
d21b = m2b * m2b - m1b * m1b
d31b = m3b * m3b - m1b * m1b
print("  masses (meV): %.3f, %.3f, %.3f -> dm21^2 = %.4g eV^2 (x%.3g), dm31^2 = %.4g eV^2 (x%.3g)"
      % (m1b * 1e3, m2b * 1e3, m3b * 1e3, d21b, d21b / DM21SQ, d31b, d31b / DM31SQ))
print("  (descending order would be INVERTED, |dm21^2| x6.3.)  SCORE: MISS.")

# =====================================================================
# T4  LEFT-HANDEDNESS
# =====================================================================
banner("T4  LEFT-HANDEDNESS (claimed, no arithmetic)")
print("  Claim: after (+e) + (-e) cancellation the SURVIVING chiral order is the")
print("  left-handed one, matching the observed V-A structure of weak interactions.")
print("  Status: CLAIMED -- stated as the mechanism's natural consequence;")
print("  consistent with observation (only left-handed neutrinos couple to the W),")
print("  but the mechanism does not derive WHY the survivor is left rather than")
print("  right.  The handedness of the surviving fold is an input, not an output.")
print("  No arithmetic content; cannot be scored in this probe.")

# =====================================================================
# T5  THREE GENERATIONS
# =====================================================================
banner("T5  THREE GENERATIONS: does the fold structure emit three chiral orders?")
print("  Locked structure scan:")
print("    fold balance 19:1:18  -> three ENTRIES, but they are the bridge")
print("       decomposition of 19, not three chiral orders.")
print("    T  = 27  = 3^3 ;  57 = 3*19 ;  1083 = 3*19^2  -> the factor 3 recurs,")
print("       so three generations are COMPATIBLE with the structure.")
print("    N  = 16  = 2^4  -> powers of 2, no 3.")
print("    Only TWO T7 variants are locked (T7b = 1/57, T7d = 20/1083, ratio")
print("       20/19 = 1 + s); no third member is given.")
print("  RESULT: the fold structure does NOT derive three distinct chiral orders")
print("  from the locked pieces.  Three generations = CLAIMED, not emitted.  MISS.")

# =====================================================================
# T6  VERDICT
# =====================================================================
banner("T6  VERDICT")
print("  Best zero-parameter number emitted by the mechanism:")
print("     s^2 * delta * m_e = 21.69 meV")
print("     -> 2.52x above sqrt(dm21^2), 0.43x of sqrt(dm31^2),")
print("        4.4% above the geometric mean of the two splittings (20.77 meV).")
print()
print("  *** NOT MECHANISM-ONLY: THE MECHANISM EMITS ONE CHECKABLE SCALE ***")
print("  *** WITHIN 2 ORDERS -- IN FACT WITHIN A FACTOR 2.6 -- OF THE     ***")
print("  *** MEASURED NEUTRINO SPLITTING SCALES.                          ***")
print()
print("  BUT: a single scale is not a spectrum.  No locked ordering, no three")
print("  masses, no handedness/generation derivation; the sum-bound candidate")
print("  T7b*delta*m_e = 137 meV misses by 14%; and 6 candidates were tried,")
print("  so the 4.4% geometric-mean hit carries multiple-comparison risk.")
print("  Only {s, T7b, T7d, delta, m_e, c0} are exercised; alpha, m_p, hbar,")
print("  N, T, X17, dU are inert for this mechanism.")
print("  Verdict: SCALE -> ALIVE (x1.04 vs geometric-mean target);")
print("           PATTERN -> MISS;  MECHANISM -> half-derived, not mechanism-only.")

# =====================================================================
# 5-LINE SUMMARY
# =====================================================================
banner("5-LINE SUMMARY")
print("  1. BEST: s^2*delta*m_e = 21.69 meV -- 4.4% from the geometric mean of")
print("     the two measured splittings, within a factor 2.6 of each.")
print("  2. HONEST GAP: one scale is not a spectrum -- no locked ordering, no")
print("     three masses; the illustrative ordering is ~6-7.5x high and the sum")
print("     violates the 0.12 eV bound.")
print("  3. HONEST GAP: T7b*delta*m_e = 137 meV misses the sum bound by 14%;")
print("     neutrality, handedness and generation count are inputs, not outputs;")
print("     6 candidates tried -> multiple-comparison risk on the hit.")
print("  4. VERDICT (LOUD): THE CHIRAL-CHARGE-OPPOSITE MECHANISM IS NOT")
print("     MECHANISM-ONLY -- IT EMITS A SCALE (21.69 meV) WITHIN 2 ORDERS OF")
print("     THE NEUTRINO SPLITTINGS -- BUT IT PREDICTS A SCALE, NOT A SPECTRUM.")
print("  5. NEXT DERIVATION: derive the locked third T7-series member (chiral")
print("     order index) and the left-survivor selection rule; then recompute")
print("     dm21^2 and dm31^2 from three masses alone.  The number to beat:")
print("     s^2*delta*m_e = 21.69 meV.")
print()
print("probe complete: exit 0")
sys.exit(0)
