# ============================================================================
# E_lock = 2.8898  -- NUMERICAL ANATOMY AUDIT
# Exhaustive sweep of every candidate the locked integer set forces,
# vs the framework's own closed form (PBA-9):
#   E_lock = rho_knot * c_med^2 ,  c_med^2 = dP/drho(x=0.3)
#           = 0.8 * (0.3/0.49 + 3.0) = 0.8 * 177/49 = 2.889795918...
# Locked set: {19,18,9,16,7,4,28,17,58,55,33,27}
# Related frozen: e_avail = 2.9122 (dRho=0.76), R_knot = 1.3770, gap = 0.0224
# ============================================================================
import itertools, math
from fractions import Fraction

EL_FROZEN = 2.8898            # the frozen rounding used across the audit
EL_EXACT  = 0.8 * (0.3/0.49 + 3.0)     # PBA-9 closed form = 708/245
RKNOT = 1.3770
EAVAIL = 2.9122
GAP   = EAVAIL - EL_FROZEN

L = [4, 7, 9, 16, 17, 18, 19, 27, 28, 33, 55, 58]

lines = []
def out(s=""):
    print(s); lines.append(s)

def pct(v, ref=EL_FROZEN):
    return 100.0 * (v/ref - 1.0)

def fmt(v):
    return "%11.8f" % v

# ---------------- pools: every integer the locked set forces ----------------
sums = set()
for k in (1, 2, 3):
    for c in itertools.combinations_with_replacement(L, k):
        sums.add(sum(c))
prods = set()
for a, b in itertools.combinations_with_replacement(L, 2):
    prods.add(a * b)
pool = sorted(sums | prods | set(L))
out("Pool sizes: sums of 1-3 locked ints (rep allowed) = %d ; products of 2 = %d ; combined pool = %d"
    % (len(sums), len(prods), len(pool)))
out("")

# ============================================================================
# 0. THE TRUE CLOSED FORM (framework's own PBA-9, PROVEN-BY-ALGEBRA)
# ============================================================================
out("="*78)
out("0. TRUE CLOSED FORM (framework record, PBA-9 / S9)")
out("="*78)
out("  dP/drho(x=0.3) = A*x/(rho_max*(1-x)^2) + B*rho_bg = 0.3/0.49 + 3.0")
out("                 = %.12f + 3.0 = %.12f" % (0.3/0.49, 0.3/0.49+3.0))
out("                 0.3/0.49 = 30/49 ; 3.0 = 147/49  ->  177/49")
out("  c_med  = sqrt(177/49) = %.9f" % math.sqrt(177/49))
out("  rho_knot = rho_bg + DRHO_LOCK = 0.3 + 0.5 = 0.8 = 4/5")
out("  E_lock = 0.8 * 177/49 = 708/245 = %.12f" % EL_EXACT)
out("  vs frozen 2.8898: %+.6f%% ; vs framework's frozen 2.889796: %+.6f%%"
    % (pct(EL_EXACT), 100.0*(EL_EXACT/2.889796 - 1.0)))
out("  Locked-set content of the true form: 49 = 7^2 (electron modes squared, via")
out("  (1-x)^2 = 0.7^2); 4 (rho_knot = 4/5). 177 is NOT in the locked set.")
out("")

# ============================================================================
# 1. OVER-19 FAMILY:  a/19  (the weld's parts, s = 1/19)
# ============================================================================
out("="*78)
out("1. OVER-19 FAMILY  a/19  (weld-part distribution)")
out("="*78)
hits = []
for a in pool:
    v = a/19.0
    d = pct(v)
    if abs(d) < 2.0:
        hits.append((abs(d), d, a, v))
hits.sort()
out("  candidates within 2%% of 2.8898 (numerator a from the forced pool):")
for ad, d, a, v in hits:
    out("    %3d/19 = %s   %+.4f%%" % (a, fmt(v), d))
out("  named decompositions of the nearest numerators:")
out("    54 = 19+18+17 (weld+heat+peak) | 27+27 | 18*3")
out("    55 = 9+7+4+18+17 (modes+heat+peak) | 28+27 | 4*7+27 | 33+18+4")
out("          | 19+18+9+9 | 16+9+7+4+19 | 58-3 (3 = 27^(1/3))")
out("    56 = 9+19+28 (cage+weld+fill) | 28*2 | 4*7*2 | 16+9+4+27")
out("")

# ============================================================================
# 2. SQRT FAMILY:  sqrt(p/q)  -- is E_lock the geometric mean of a locked ratio?
# ============================================================================
out("="*78)
out("2. SQRT FAMILY  sqrt(p/q)   (E_lock^2 = 8.35104 must be a locked ratio)")
out("="*78)
hits = []
for p in pool:
    for q in pool:
        v = math.sqrt(p/q)
        d = pct(v)
        if abs(d) < 1.0:
            hits.append((abs(d), d, p, q, v))
hits.sort()
out("  candidates within 1.0%% (p,q from the forced pool):")
for ad, d, p, q, v in hits[:40]:
    out("    sqrt(%4d/%3d) = %s   %+.4f%%" % (p, q, fmt(v), d))
out("  total hits: %d" % len(hits))
out("")

# ============================================================================
# 3. FOLD-CLOCK FAMILY:  a/16  (the fold's fractions)
# ============================================================================
out("="*78)
out("3. FOLD-CLOCK FAMILY  a/16   (fold fractions; 16-mode clock)")
out("="*78)
hits = []
for a in pool:
    v = a/16.0
    d = pct(v)
    if abs(d) < 1.6:
        hits.append((abs(d), d, a, v))
hits.sort()
for ad, d, a, v in hits:
    out("    %3d/16 = %s   %+.4f%%" % (a, fmt(v), d))
out("  also: 16*9/(2(16+9)) = 144/50 = 2.880000  %+.4f%%  [fold x cage per 2(fold+cage)]"
    % pct(2.88))
out("")

# ============================================================================
# 4. OTHER DENOMINATORS  a/d  for each locked integer d (named-role families)
# ============================================================================
out("="*78)
out("4. OTHER DENOMINATOR FAMILIES  a/d  (d = each locked integer)")
out("="*78)
rows = []
for d in L:
    for a in pool:
        v = a/float(d)
        dd = pct(v)
        if abs(dd) < 1.2:
            rows.append((abs(dd), dd, d, a, v))
rows.sort()
for ad, dd, d, a, v in rows[:50]:
    out("    %4d/%-3d = %s   %+.4f%%" % (a, d, fmt(v), dd))
out("  total hits <1.2%%: %d" % len(rows))
out("")

# ============================================================================
# 5. R_KNOT FAMILY  (does 1.377 combine with the mode counts?)
# ============================================================================
out("="*78)
out("5. R_KNOT FAMILY  (R_knot = 1.3770 in the forge's units)")
out("="*78)
rk = RKNOT
named = [
    ("E_lock * R_knot (should be 4?)",        EL_FROZEN*rk),
    ("4 / R_knot  [proton quanta per knot radius]", 4.0/rk),
    ("R_knot + 1.5128  (the forced addend)",  rk + (EL_FROZEN - rk)),
    ("R_knot + sqrt(16/7)  [fold clock per electron mode]", rk + math.sqrt(16.0/7.0)),
    ("R_knot + 50/33 = 1.377 + 2(16+9)/33",   rk + 50.0/33.0),
    ("R_knot * 2.1 (= 21/10, 21 = 3*7)",      rk * 2.1),
    ("2.8898 / R_knot = 2.0986... (the forced quotient)", EL_FROZEN/rk),
    ("R_knot vs sqrt(4*9/19) = 6/sqrt(19)",   math.sqrt(4.0*9.0/19.0)),
    ("R_knot vs 22/16 = (18+4)/16",           22.0/16.0),
    ("R_knot vs sqrt(17/9)  [peak load per cage mode]", math.sqrt(17.0/9.0)),
    ("R_knot vs sqrt(19/10)",                 math.sqrt(19.0/10.0)),
]
for name, v in named:
    ref = RKNOT if ("R_knot vs" in name) else EL_FROZEN
    out("    %-48s = %s   %+.4f%%  (ref=%s)" % (name, fmt(v), pct(v, ref), ref))
out("  R_knot^2 = %.6f  (36/19 = %.6f -> +%.4f%% ; 17/9 = %.6f -> +%.4f%% ; 19/10 = %.6f)"
    % (rk*rk, 36.0/19.0, 100.0*(rk*rk/(36.0/19.0)-1.0), 17.0/9.0, 100.0*(rk*rk/(17.0/9.0)-1.0), 19.0/10.0))
out("")

# ============================================================================
# 6. GAP / E_AVAIL FAMILY
# ============================================================================
out("="*78)
out("6. GAP / E_AVAIL FAMILY  (2.9122 - 2.8898 = 0.0224 at dRho = 0.76)")
out("="*78)
out("  gap = e_avail - E_lock = %.4f exactly" % GAP)
out("  0.0224 = 14/625 = 2*7/25^2 = 28/(2*25^2), 25 = 16+9  ->  gap = 2*7/(16+9)^2")
out("  dRho = 0.76 = 19/25 = 19/(16+9)  EXACT  (weld parts over fold+cage)")
out("  0.0224 = (19/25)*(14/25)/19 = dRho * (2*7/25) / 19")
out("  gap * 19 = %.6f = dRho * 0.56 ; 0.56 = 14/25 = 28/50" % (GAP*19))
out("  E_lock*(1 + 1/129) = %.6f  (129 = 58+55+16)  vs e_avail: %+.6f%%"
    % (EL_FROZEN*(1+1.0/129.0), pct(EL_FROZEN*(1+1.0/129.0), EAVAIL)))
out("  e_avail/130 = %.6f vs gap %.6f (130 = 58+55+17)" % (EAVAIL/130.0, GAP))
out("  e_avail = 2*(55+28)/(3*19) = 166/57 = %.6f  vs 2.9122: %+.6f%%"
    % (166.0/57.0, 100.0*((166.0/57.0)/EAVAIL - 1.0)))
out("  e_avail vs R_knot * 55/26 = %.6f  (26 = 19+7): %+.6f%%"
    % (rk*55.0/26.0, 100.0*(rk*55.0/26.0/EAVAIL - 1.0)))
out("  e_avail vs sqrt(17/2) = %.6f : %+.6f%%" % (math.sqrt(17.0/2.0), 100.0*(math.sqrt(17.0/2.0)/EAVAIL-1.0)))
out("  e_avail^2 = %.6f  (17/2 = %.6f)" % (EAVAIL*EAVAIL, 17.0/2.0))
out("")

# ============================================================================
# 7. EXPLICIT NAMED CANDIDATES FROM THE BRIEF (print regardless of distance)
# ============================================================================
out("="*78)
out("7. THE BRIEF'S NAMED CANDIDATES, COMPUTED")
out("="*78)
brief = [
    ("55/19",                   55.0/19.0),
    ("(28+9+18)/19",            (28+9+18)/19.0),
    ("(4*7+9+18)/19",           (4*7+9+18)/19.0),
    ("(58-3)/19",               (58-3)/19.0),
    ("(19+18+17)/19 = 54/19",   54.0/19.0),
    ("(9+19+28)/19 = 56/19",    56.0/19.0),
    ("(3*19)/19 = 3.0",         3.0),
    ("sqrt(58/7)",              math.sqrt(58.0/7.0)),
    ("sqrt(33/4)",              math.sqrt(33.0/4.0)),
    ("sqrt(18*27/58)",          math.sqrt(18.0*27.0/58.0)),
    ("sqrt(17*28/(3*19))",      math.sqrt(17.0*28.0/(3.0*19.0))),
    ("sqrt(17*55/(4*28))",      math.sqrt(17.0*55.0/(4.0*28.0))),
    ("sqrt(4*7*17/(3*19))",     math.sqrt(4.0*7.0*17.0/(3.0*19.0))),
    ("(19+7)/9 = 26/9",         26.0/9.0),
    ("2(19+7)/18 = 52/18",      52.0/18.0),
    ("2(28+7+4)/27 = 78/27",    78.0/27.0),
    ("9^2/28 = 81/28",          81.0/28.0),
    ("7^2/17 = 49/17",          49.0/17.0),
    ("58/(9+7+4) = 58/20",      58.0/20.0),
    ("(19+27)/16 = 46/16",      46.0/16.0),
    ("16*9/(2(16+9)) = 144/50", 144.0/50.0),
    ("(33+28+17+18)/33 = 96/33", 96.0/33.0),
    ("(58+55+28+18)/55 = 159/55", 159.0/55.0),
    ("(55+58+28+27)/58 = 168/58", 168.0/58.0),
    ("4/R_knot",                4.0/rk),
    ("R_knot + sqrt(16/7)",     rk + math.sqrt(16.0/7.0)),
    ("R_knot + 50/33",          rk + 50.0/33.0),
    ("R_knot * 2.1",            rk * 2.1),
    ("2.9122 - 14/625",         EAVAIL - 14.0/625.0),
    ("2.9122 - 2*7/25^2",       EAVAIL - 2.0*7.0/625.0),
    ("0.8*177/49 (TRUE, PBA-9)", EL_EXACT),
]
out("  %-34s %12s %9s" % ("candidate", "value", "d% vs 2.8898"))
for name, v in brief:
    out("  %-34s %s  %+.4f%%" % (name, fmt(v), pct(v)))
out("")

# ============================================================================
# 8. MASTER RANKING of every hit < 1.2% across all families
# ============================================================================
out("="*78)
out("8. MASTER RANKING (all families, |d| < 1.2%%, sorted)")
out("="*78)
master = []
# ratios
for d in L + [19, 16]:
    for a in pool:
        v = a/float(d); dd = pct(v)
        if abs(dd) < 1.2: master.append(("%4d/%d" % (a, d), v, dd, "ratio"))
# sqrts
for p in pool:
    for q in pool:
        v = math.sqrt(p/q); dd = pct(v)
        if abs(dd) < 1.2: master.append(("sqrt(%d/%d)" % (p, q), v, dd, "sqrt"))
# rknot
for name, v in named:
    dd = pct(v)
    if abs(dd) < 1.2: master.append((name, v, dd, "rknot"))
# closed form
master.append(("0.8*177/49 (PBA-9 true form)", EL_EXACT, pct(EL_EXACT), "EOS"))
# dedupe by (expr, value)
seen = set(); uniq = []
for expr, v, dd, fam in master:
    key = (round(v, 8),)
    if key in seen: continue
    seen.add(key); uniq.append((expr, v, dd, fam))
uniq.sort(key=lambda r: abs(r[2]))
out("  %-40s %12s %9s  %s" % ("candidate", "value", "d%", "family"))
for expr, v, dd, fam in uniq[:60]:
    out("  %-40s %s  %+.4f%%  %s" % (expr, fmt(v), dd, fam))
out("  total unique hits printed: %d" % min(60, len(uniq)))
out("")

with open(__file__.replace(".py", "_RESULTS.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\n[results written to E_LOCK_ANATOMY_RESULTS.txt]")
