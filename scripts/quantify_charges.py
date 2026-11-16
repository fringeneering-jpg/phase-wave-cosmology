#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
quantify_charges.py -- Phase Wave Cosmology: CHARGE COLUMN audit.

ZERO fitted parameters. Every number is computed from LOCKED constants only
(or is a locked claim restated verbatim). Residuals are against external
MEASURED values. Misses are reported, never hidden. Exit code 0.

THE COLUMN'S COLLAPSE (exact algebra, no fit):
  q'/e = sqrt(3/(16 pi^3 alpha)) = 0.9103   [eps0, h, hbar, c all cancel]
  (e/q')^2 = 16 pi^3 alpha/3                [the same identity inverted]
  -> the whole charge column is ONE datum (alpha) plus pi; the single free
     claim is g_locked = 20^(1/16) = (e/q')^2, tested in row 7.

Rows:
  1 electron winding charge q' ; 2-4 Hall nu = 1/3, 2/5, 2/3 ;
  5-6 quark -1/3, +2/3 ; 7 coupling g ; 8 two-regime bridge 9/(4s).
"""
import math

# ---------------- LOCKED CONSTANTS (never re-fit) ----------------
s        = 1.0/19.0          # LOCKED stretch (19:1:18 ledger)
N        = 16.0              # LOCKED 16-fold winding / harmonic count
alpha    = 1.0/137.035999084 # LOCKED fine-structure constant
hbar     = 1.054571817e-34   # LOCKED
c0       = 2.99792458e8      # LOCKED
rho0     = 8.74e-27          # LOCKED
g_locked = 20.0**(1.0/16.0)  # LOCKED (20:1 medium:matter ledger, 16 modes)
rho_max  = 1.29032e15        # DERIVED (shell read 1.304e15)
rho_core = 2.3e17            # LOCKED
R_p_lock = 0.84e-15          # LOCKED (bridge script evaluates at measured 8.414e-16)

# SI-defined anchors (definitions, never fitted)
EPS0     = 8.8541878128e-12  # F/m, exact SI-2019
E_SI     = 1.602176634e-19   # C,   exact SI-2019
M_P_KG   = 1.67262192369e-27 # kg, CODATA (bridge_derivation.py)
R_P_MEAS = 8.414e-16         # m,  measured-R_p evaluation (bridge_derivation.py)
ALPHA_SIGMA_REL = 1.5e-10    # CODATA-2018: 0.0072973525693(11)

# ---------------- derived intermediates (locked constants only) ----------------
h           = 2.0*math.pi*hbar                    # exact relation, locked hbar
q_prime     = math.sqrt(3.0*EPS0*h*c0/(8.0*math.pi**3))
ratio_q     = q_prime/E_SI
ratio_q_alpha = math.sqrt(3.0/(16.0*math.pi**3*alpha))  # identical, eps0-free form
g_target    = 16.0*math.pi**3*alpha/3.0
algebra_residual = (E_SI/q_prime)**2 - g_target  # must be ~0: the identity is exact
alpha_pred  = 3.0*g_locked/(16.0*math.pi**3)
inv_alpha_pred = 1.0/alpha_pred
g_resid_pct   = 100.0*(g_locked/g_target - 1.0)
g_sigma_exact = abs(alpha_pred - alpha)/alpha/ALPHA_SIGMA_REL
completion  = math.sqrt(g_target)                # the asserted 2/3-fold completion factor

bridge      = 9.0/(4.0*s)
bridge_meas = 42.7416
r_p_quantum = 4.0*hbar/(M_P_KG*c0)               # from m_p R_p c0 = 4 hbar
r_p_implied = r_p_quantum/(bridge_meas/bridge)
r_p_resid_pct = 100.0*(r_p_quantum/R_P_MEAS - 1.0)
r_p_sigma     = r_p_resid_pct/0.2258             # CODATA R_p = 0.8414(19) fm -> 0.2258%

# 16-fold winding partitions from the locked 19:18 geometry
ex19 = 19 - int(N)   # 3
ex18 = 18 - int(N)   # 2
e3 = E_SI/3.0
e5 = E_SI/5.0

print("=" * 96)
print("PWC CHARGE COLUMN -- quantified from LOCKED constants only (zero fitted)")
print("=" * 96)
print("  q' = sqrt(3 eps0 h c / 8 pi^3) = %.6e C = %.6f e" % (q_prime, ratio_q))
print("  identical eps0-free form : q'/e = sqrt(3/(16 pi^3 alpha)) = %.6f" % ratio_q_alpha)
print("  algebra check            : (e/q')^2 - 16 pi^3 alpha/3 = %.2e (identity exact; drift = locked-alpha last digits)" % algebra_residual)
print("  g_locked = 20^(1/16)     = %.9f" % g_locked)
print("  g_target = 16 pi^3 a/3   = %.9f   residual %+.4f%%" % (g_target, g_resid_pct))
print("  inverse claim            : 3g/(16 pi^3) -> 1/alpha = %.6f vs 137.035999084 (%.1e sigma)" % (inv_alpha_pred, g_sigma_exact))
print("  bridge 9/(4s)            = %.4f vs measured %s (%+.4f%%)" % (bridge, bridge_meas, 100*(bridge/bridge_meas-1)))
print("  partitions               : 19-16 = %d, 18-16 = %d  ->  e/3, e/5, 2e/3, 2e/5" % (ex19, ex18))
print("=" * 96)
print()

rows = [
    # (name, formula, pwc value, measured value, residual, provenance, kill condition)
    ("1. electron winding charge",
     "q' = sqrt(3 eps0 h c / 8 pi^3), h = 2 pi hbar  [= sqrt(3/(16 pi^3 alpha)) e]",
     "%.6e C = %.4f e" % (q_prime, ratio_q),
     "e = %.9e C (exact SI-2019)" % E_SI,
     "%+.4f%% | gap by design" % (100.0*(ratio_q-1.0)),
     "DERIVED (D5; quicycle_charge_map.py; VERIFIED)",
     "KILL: q' is not directly measurable; if claimed = e, -8.97% at infinite sigma (e exact). All testable content passes to the completion g -> row 7."),

    ("2. Hall nu=1/3 quasiparticle",
     "e/3 = e/(19-16)  [3 = excess of the 19-loop over the N=16 fold]",
     "%.6e C" % e3,
     "e/3 at nu=1/3 (Laughlin; shot-noise de-Picciotto & Saminadayar 1997, ~1-4%)",
     "0.0000% | by construction",
     "TRIAL from locked 19:18/N=16 (no workspace derivation)",
     "KILL: partition must emit the full observed ladder nu=1/5,1/7,1/9,3/7,... with zero choices; {3,5} alone is a retrofit, and Laughlin already gives e/(2m+1) with no 19:18 input."),

    ("3. Hall nu=2/5 quasiparticle",
     "e/5 = e/((19-16)+(18-16))  [3+2 excesses of the 19:18 pair over N=16]",
     "%.6e C" % e5,
     "e/5 at nu=2/5 (Reznikov et al., Nature 399, 238 (1999))",
     "0.0000% | by construction",
     "TRIAL from locked 19:18/N=16 (no workspace derivation)",
     "KILL: same extension rule as row 2; must also fix why 2/5 (not 1/5, 3/5) carries charge e/5, and why the 2-excess alone (1/2) is never a fractional charge."),

    ("4. Hall nu=2/3 filling",
     "2/3 = 2/(19-16)  [two units of the 3-partition]",
     "0.6666667 (2/3)",
     "nu=2/3 plateau, R_H = 3 h/(2 e^2), exact quantization",
     "0.0000% | by construction",
     "TRIAL from locked 19:18/N=16 (no workspace derivation)",
     "KILL: same extension rule; the rule must forbid the unobserved single-layer nu=4/3, 2/9, ... while emitting 2/3 - selection, not prediction, until it generalizes."),

    ("5. down quark charge",
     "-e/3 = -e/(19-16)",
     "%.6e C" % (-e3),
     "-e/3 (SM hypercharge; exact by definition; anomaly cancellation, DIS)",
     "0.0000% | by construction",
     "TRIAL from locked 19:18/N=16 (no workspace derivation)",
     "KILL: must reproduce the complete SM charge table (u=+2/3, d=-1/3, e=-1, nu=0, x3 generations) with zero free choices incl. signs; a 2-row subset is not a derivation."),

    ("6. up quark charge",
     "+2e/3 = +2e/(19-16)",
     "%.6e C" % (2.0*e3),
     "+2e/3 (SM hypercharge; exact by definition)",
     "0.0000% | by construction",
     "TRIAL from locked 19:18/N=16 (no workspace derivation)",
     "KILL: same as row 5."),

    ("7. coupling g",
     "g = 20^(1/16)  vs  (e/q')^2 = 16 pi^3 alpha/3",
     "%.6f" % g_locked,
     "%.6f" % g_target,
     "%+.4f%% | %.1e sigma if exact" % (g_resid_pct, g_sigma_exact),
     "g LOCKED (20:1 ledger, 16 modes); target DERIVED (D5/D6; VERIFIED)",
     "KILL: (e/q')^2 = 16 pi^3 alpha/3 is exact algebra - not independent of row 1; the single free claim g = 20^(1/16) = that number inverts to 1/alpha = %.3f vs 137.035999084 (rel. sigma 1.5e-10) -> 4.6e6 sigma. Survives only as a -0.069%% coincidence." % inv_alpha_pred),

    ("8. two-regime bridge",
     "9/(4s) = 9*19/4  [G cancels; Y_cav = s rho0 c0^2/3, V_pair = m_p/(3 rho0), m_p R_p c0 = 4 hbar]",
     "42.7500",
     "42.7416 (self-coupling/alpha_G at measured R_p = 8.414e-16)",
     "%+.4f%% | %.2f sigma of R_p" % (100.0*(bridge/bridge_meas-1), abs(r_p_sigma)),
     "DERIVED (D9; bridge_derivation.py; VERIFIED)",
     "KILL: 42.7416 is not independent - it is the quantization law m_p R_p c0 = 4 hbar re-evaluated through measured R_p; the residual is R_p's own last digit (implied R_p = %.4e vs quantum %.4e, %+.3f%% = 0.08 sigma of 0.8414(19) fm). Single-counted." % (r_p_implied, r_p_quantum, r_p_resid_pct)),
]

cols = [("NAME", 20), ("PWC FORMULA", 32), ("PWC VALUE", 22), ("MEASURED VALUE", 26),
        ("RESIDUAL %/SIGMA", 18), ("PROVENANCE", 20), ("KILL CONDITION", 44)]

def wrap(text, width):
    out = []
    for chunk in str(text).split("\n"):
        cur = ""
        for w in chunk.split(" "):
            t = (cur + " " + w).strip()
            if len(t) <= width:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out or [""]

header = " | ".join(h.ljust(w) for h, w in cols)
print(header)
print("-" * len(header))
for r in rows:
    cells = [wrap(r[i], w) for i, (_, w) in enumerate(cols)]
    n = max(len(c) for c in cells)
    for j in range(n):
        line = " | ".join((c[j] if j < len(c) else "").ljust(w)
                          for c, (_, w) in zip(cells, cols))
        print(line.rstrip())
    print("-" * len(header))

print()
print("NOTES (honest misses, never hidden)")
print("-" * 96)
print("  N1. (e/q')^2 = 16 pi^3 alpha/3 EXACTLY (algebra): e^2 = 4 pi eps0 hbar c alpha, h = 2 pi hbar;")
print("      so row 7's target is row 1's definition inverted - the bridge is NOT an independent match.")
print("  N2. q'/e = %.6f exact; the paper's '0.9103' rounds at %+.3f%%." % (ratio_q, 100*(0.9103/ratio_q-1)))
print("  N3. The completion factor sqrt(16 pi^3 alpha/3) = %.6f is asserted as 'the dichromal" % completion)
print("      2/3 fold' (the same 2/3 that runs the tau): no closed form links 2/3 to 1.0985 - ASSERTED, OPEN.")
print("  N4. The e/5 partition recurs in the proton cage ledger (five knots x 1/5 = +1, charge_distribution.py):")
print("      internal consistency, not an independent confirmation.")
print("  N5. Bridge residual maps onto R_p: implied %.4e m vs quantum %.4e m" % (r_p_implied, r_p_quantum))
print("      (%+.3f%%); within CODATA R_p = 0.8414(19) fm by 0.08 sigma - a weak, single-counted test." % r_p_resid_pct)
print("  N6. g residual -0.069%% <-> fuel fraction 1/%.4f = %.4f%%" % (g_target**16, 100.0/g_target**16))
print("      vs the locked 5% (20:1) - the fuel gauge's own last digit.")
print()

print("SUMMARY (5 lines)")
print("-" * 96)
print("1. BEST HIT:   bridge 9/(4s) = 42.75 vs 42.7416 (%+.3f%%) - the only locked-only formula landing on a"
      % (100*(bridge/bridge_meas-1)))
print("   measured number; but it is single-counted: the residual IS the quantization law m_p R_p c0 = 4 hbar")
print("   read through measured R_p (0.08 sigma of 0.8414(19) fm).")
print("2. WORST MISS: g = 20^(1/16) = %.6f vs 16 pi^3 alpha/3 = %.6f (-%.3f%%); as an exact identity it inverts"
      % (g_locked, g_target, abs(g_resid_pct)))
print("   to 1/alpha = %.3f vs 137.035999084 -> %.1e sigma. It survives only as an approximate coincidence." % (inv_alpha_pred, g_sigma_exact))
print("3. STRUCTURAL: q' = %.4fe is %.2f%% short of e BY DESIGN; the completion sqrt(16 pi^3 alpha/3) = %.4f is"
      % (ratio_q, 100*(1-ratio_q), completion))
print("   asserted as the dichromal 2/3 fold with no closed form - OPEN.")
print("4. Hall nu=1/3,2/5,2/3 and quark +-1/3,+-2/3: every 0.0000% residual is BY CONSTRUCTION (the formula outputs")
print("   the targeted fraction); the 19:18/N=16 partition emits only {3,5} - retrofit until it generalizes.")
print("5. NEXT DERIVATION: generalize the 16-fold winding partition to the full odd-denominator ladder (3,5,7,9,...")
print("   = Laughlin m) with zero choices - if it closes, the Hall column becomes a real prediction; if it does not,")
print("   kill the partition rule.")
print()
print("EXIT: 0")
