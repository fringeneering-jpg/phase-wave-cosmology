#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
probe_hodge.py
==============
PROBE: does Phase Wave Cosmology's LOCKED geometry (the 720-degree quicycle
4pi fold, the 19:1:18 balance, the 16-fold clock, the golden-bridge residual,
the 5 pi^2 topology equation, the G-chain, the steric ceiling) provide any
genuine algebraic-geometric statement about Hodge classes?

Scope of the Hodge conjecture used here: every rational Hodge class
H^{p,p}(X) cap H^{2p}(X,Q) on a smooth complex projective variety X is a
Q-linear combination of classes of algebraic cycles.

Protocol (fixed by the brief):
  * ZERO fitted parameters.
  * Provenance labels: DERIVED / MEASURED / VERIFIED / BACK-SOLVED /
    CLAIMED / OPEN.
  * VERIFIED is reserved for checkable algebraic identities (numerically
    confirmed classical values are flagged VERIFIED-numeric).
  * Every candidate statement carries a kill condition.
  * Misses are reported, never hidden.
  * Exit 0 means "probe completed honestly", NOT "conjecture supported".

No paper files are read-only-touched or edited; this script only creates
probe_hodge_report.txt next to itself.
"""

import math
import os
from fractions import Fraction
from math import comb, gcd, isqrt

# ----------------------------------------------------------------------------
# small exact-number tools
# ----------------------------------------------------------------------------

def sigma3(n):
    """sum of cubes of the positive divisors of n"""
    tot = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            tot += d ** 3
            if d * d != n:
                tot += (n // d) ** 3
        d += 1
    return tot


def reduced_forms(D):
    """SL2(Z)-reduced primitive positive definite binary quadratic forms of
    negative discriminant D.  Returns list of (a, b, c)."""
    forms = []
    amax = isqrt(abs(D) // 3)
    for a in range(1, amax + 1):
        for b in range(-a, a + 1):
            if (b * b - D) % (4 * a) != 0:
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            if (c == a or abs(b) == a) and b < 0:
                continue
            if gcd(gcd(a, b), c) != 1:
                continue
            forms.append((a, b, c))
    return forms


def j_from_qseries(tau, terms, dps=60):
    """Klein j-invariant from its q-expansion (float64, no mpmath needed):
    j = E4^3 / Delta,  E4 = 1 + 240 sum_n sigma3(n) q^n,
    Delta = q prod_n (1 - q^n)^24,  q = exp(2 pi i tau)."""
    import cmath
    q = cmath.exp(2.0 * math.pi * 1j * tau)
    s = 0.0 + 0.0j
    for n in range(1, terms + 1):
        s += sigma3(n) * q ** n
    E4 = 1.0 + 240.0 * s
    prod = 1.0 + 0.0j
    for n in range(1, terms + 1):
        prod *= (1.0 - q ** n)
    Delta = q * prod ** 24
    return E4 ** 3 / Delta


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    L = []
    P = L.append

    P("=" * 78)
    P("PROBE: Phase Wave Cosmology locked geometry  vs  the Hodge conjecture")
    P("=" * 78)
    P("Protocol: zero fitted parameters; provenance labels DERIVED/MEASURED/")
    P("VERIFIED/BACK-SOLVED/CLAIMED/OPEN; VERIFIED = checkable algebraic")
    P("identity only; kill condition per candidate; misses reported; exit 0.")
    P("")

    # ---------------- SECTION A: checkable identities ----------------
    P("-" * 78)
    P("SECTION A - checkable identities (the only things labeled VERIFIED)")
    P("-" * 78)

    # A1: 16-fold clock
    P("[VERIFIED] A1   N = 4*pi/(pi/4) = 16 exactly: pi cancels, N = 4*4 = 16.")
    P("      Content check: this is the tautology 4/(1/4) = 16; it carries no")
    P("      topology by itself - a '16-fold anything' must be imposed by hand.")
    P("")

    # A2: 19:1:18 balance
    P("[VERIFIED] A2   18/19 + 1/19 = 1 exactly (a bare rational split, no")
    P("      residue and no cohomological content).")
    P("")

    # A3: golden-bridge residual
    sqrt5 = math.sqrt(5)
    phi = (1.0 + sqrt5) / 2.0
    six_phi2 = 6.0 * phi * phi
    five_pi = 5.0 * math.pi
    delta = (six_phi2 - five_pi) / five_pi
    P("[VERIFIED] A3   delta = (6*phi^2 - 5*pi)/(5*pi) = %.10e  (numeric)." % delta)
    P("      6*phi^2 = %.12f ; 5*pi = %.12f" % (six_phi2, five_pi))
    P("      [VERIFIED-by-theorem] delta != 0 EXACTLY: phi is algebraic (a root")
    P("      of x^2 - x - 1), so delta = 0 would force pi = 6*phi^2/5 to be an")
    P("      algebraic number, contradicting Lindemann's theorem (pi is")
    P("      transcendental).  => the golden bridge can NEVER close; delta is a")
    P("      transcendental gap, not an invariant of any algebraic structure.")
    P("")

    # symbolic confirmation with sympy when available
    try:
        import sympy as sp
        phi_s = (1 + sp.sqrt(5)) / 2
        N_sym = sp.simplify(4 * sp.pi / (sp.pi / 4))
        delta_s = sp.simplify((6 * phi_s ** 2 - 5 * sp.pi) / (5 * sp.pi))
        mpoly = sp.minimal_polynomial(phi_s)
        P("[VERIFIED] A1-symbolic   4*pi/(pi/4) simplifies to %s." % N_sym)
        P("[VERIFIED] A3-symbolic   delta = %s (sympy, 14 digits)." % sp.N(delta_s, 14))
        P("[VERIFIED] A3-symbolic   phi is a root of %s = 0  (checked: %s)."
          % (mpoly.as_expr(), sp.simplify(phi_s ** 2 - phi_s - 1) == 0))
        P("[ENV] sympy %s present." % sp.__version__)
    except ImportError:
        P("[INFRASTRUCTURE-MISS] sympy unavailable; symbolic checks above are")
        P("      replaced by the float checks already printed (reported, not hidden).")
    P("")

    # A4: class numbers and CM j-values (Heegner discriminants -4 and -19)
    f4 = reduced_forms(-4)
    f19 = reduced_forms(-19)
    P("[VERIFIED] A4a   class number h(-4)  = %d  (reduced forms: %s)"
      % (len(f4), f4))
    P("[VERIFIED] A4a   class number h(-19) = %d  (reduced forms: %s)"
      % (len(f19), f19))
    P("      => 19 is a Heegner number (h(-19) = 1); -4 is the Gaussian case")
    P("      Z[i] (h(-4) = 1).  Classical CM theory: the j-invariant of a CM")
    P("      elliptic curve is an algebraic integer, so")
    P("      j(i) = 1728 = 12^3  and  j((-1+i*sqrt19)/2) = -96^3 = %d." % (-96 ** 3))
    try:
        j_i = j_from_qseries(1j, 800)
        tau19 = complex(-1.0, math.sqrt(19.0)) / 2.0
        j_19 = j_from_qseries(tau19, 12)
        ok_i = abs(j_i.real - 1728.0) < 1e-6
        ok_19 = abs(j_19.real + 884736.0) < 1e-4
        P("[VERIFIED-numeric] j(i)              = %.10f  vs 1728     (match: %s)"
          % (j_i.real, ok_i))
        P("[VERIFIED-numeric] j((-1+i*sqrt19)/2) = %.6f  vs -884736  (match: %s)"
          % (j_19.real, ok_19))
    except Exception as e:
        P("[INFRASTRUCTURE-MISS] q-series check failed; classical CM table")
        P("      values stated above; reported, not hidden.")
        P("      error: %r" % (e,))
    P("")

    # A5: Hodge numbers of the quicycle torus
    n = 1  # complex dimension of the quicycle torus
    h11 = comb(n, 1) * comb(n, 1)
    h20 = comb(n, 2) * comb(n, 0)
    b2 = comb(2 * n, 2)
    P("[VERIFIED] A5   torus of complex dim %d: h^{p,q} = C(n,p)C(n,q) gives" % n)
    P("      h^{1,1} = %d, h^{2,0} = h^{0,2} = %d, b_2 = %d." % (h11, h20, b2))
    P("      => H^2(E,C) = H^{1,1};  Hdg^2(E,Q) = Q.[E], and [E] is the class")
    P("      of the cycle E itself.  The rational Hodge conjecture HOLDS on")
    P("      the quicycle torus - Lefschetz's (1,1) theorem in dimension 1,")
    P("      classical (1924), true for EVERY smooth projective curve, and")
    P("      entirely independent of 19/18, 5*pi^2, 16*pi^3 and delta.")
    P("")

    # ---------------- SECTION B: candidate table ----------------
    P("-" * 78)
    P("SECTION B - candidate Hodge statements (status strictly CLAIMED/OPEN)")
    P("-" * 78)
    P("| # | candidate statement | framework input | status | kill condition | what a real algebraic geometer would demand |")
    P("|---|---|---|---|---|---|")
    P("| 1 | the 4pi winding constrains Hodge classes | quicycle 720-degree fold | CLAIMED | killed on arrival: the winding is a class in H_1(E,Z) (degree 1), while Hodge classes live in H^{2p}(X,Q); on E there is nothing to constrain (A5) | a named variety of complex dim >= 4 plus a Hodge class whose algebraicity the winding decides |")
    P("| 2 | the 19:1:18 split is an integrality / denominator condition on cycle classes | F_topology/F_EM = 18/19 | CLAIMED | killed: Hodge classes are Q-linear by definition, so a /19 denominator is allowed; A2 is pure arithmetic; no class is named | an explicit c in H^2(X,Z) such that c/19 is Hodge but not algebraic (a real integral-Hodge obstruction) |")
    P("| 3 | delta = 1.5321e-5 is a period invariant / golden-bridge measure | golden-bridge residual | OPEN | killed as invariant: delta != 0 exactly (A3, Lindemann-Weierstrass), so it can never be an algebraic invariant and the bridge can never close; no variety is named for the period-ratio reading | delta written as a ratio of two periods of named varieties, e.g. two entries of a period matrix of a named CM abelian variety |")
    P("| 4 | the quicycle torus satisfies the rational Hodge conjecture (zero-parameter) | the 4pi torus | OPEN (true but classical) | no kill needed - it is a theorem (Lefschetz (1,1)); the kill applies to authorship: it holds for every curve with or without PWC's constants | nothing; but note the proof never touches 19/18, 5pi^2, 16pi^3, delta |")
    P("| 5 | 16 = 4pi/(pi/4) is a Hodge number or cycle count | 16-fold clock | CLAIMED | killed: A1 shows the identity is just 4 x 4 = 16 (pi cancels); no variety carrying a 16 (Hodge number, node count, theta characteristics) is produced by the fold | a construction from the fold to a variety whose Hodge data contains a 16 |")
    P("| 6 | the framework's 19 selects the CM elliptic curve of discriminant -19 (integral j = -96^3) | the 19 of 19:1:18 | OPEN | killed while the lattice is unspecified: h(-19) = 1 and j((-1+i*sqrt19)/2) = -96^3 are real (A4), but PWC's 19 is a force-split denominator and the fold's complex structure tau is never stated; a square torus gives D = -4, j = 1728 | state tau of the fold lattice and show it is homothetic to Z[(-1+sqrt(-19))/2]; then j = -96^3 follows zero-parameter |")
    P("| 7 | 5pi^2 and R_loop = r_e/(5pi^2) constrain topology / periods | 5-pi^2 topology equation | CLAIMED | killed: every positive real number is the covolume of some flat torus (rescale the lattice), so '5pi^2 is a torus volume' decides nothing; r_e is dimensionful while periods are dimensionless | a canonical unscaled lattice with covolume 5pi^2, or a dimensionless invariant (period ratio, j-value, class number) |")
    P("| 8 | rho_max = 1.29032e15 enters a Hodge statement | steric ceiling | OPEN (input BACK-SOLVED) | disqualified under the zero-fitted-parameter rule: n = 2/33 is a fitted rational, so rho_max is back-solved, not derived from geometry | re-derive rho_max from a period / lattice computation containing no fitted rationals |")
    P("| 9 | 16pi^3 is a period / volume of the fold | 16pi^3 fold lore | OPEN | killed as stated: pi^3 is a period (product of periods), but no variety and no normalization is named; as a volume the claim is vacuous (see row 7) | the variety and the normalization under which 16pi^3 is one of its periods |")
    P("")

    P("DETAILS behind the table:")
    P("  R1: the 4pi winding number is an integer invariant of degree-1 cycles")
    P("      (homology classes on T^2), and every homology class on a curve is")
    P("      already algebraic; the Hodge conjecture says nothing about H_1.")
    P("  R2: denominator obstructions are the subject of the INTEGRAL Hodge")
    P("      conjecture, which is known to fail in general (Atiyah-Hirzebruch,")
    P("      torsion classes); the framework engages none of that machinery.")
    P("  R3: 6*phi^2 = 15.7082... vs 5*pi = 15.7079... is a documented numerical")
    P("      near-coincidence (pi ~ 6*phi^2/5), and Lindemann makes exact")
    P("      closure impossible - a theorem-grade negative result.")
    P("  R4: true, zero-parameter, but 100 years old and free of every PWC")
    P("      constant; a geometer reads it as background, not as a PWC result.")
    P("  R5: 16 does occur in algebraic geometry (16 nodes of the Kummer")
    P("      quartic, 16 theta characteristics in genus 2), but the fold never")
    P("      produces any such object - the echo is unredeemed.")
    P("  R6: 19 is a Heegner number and the CM curve with ring Z[(-1+sqrt(-19))/2]")
    P("      has integral j-invariant -96^3 (both checked in A4); but nothing in")
    P("      PWC constructs that lattice, so the 19 is an orphaned echo.")
    P("  R7: dimensional numerology: a length (r_e = classical electron radius,")
    P("      MEASURED QED input) can be scaled to anything; periods of varieties")
    P("      are dimensionless, so no length can BE a period.")
    P("  R8: rho_max is BACK-SOLVED (fitted n = 2/33) and is therefore excluded")
    P("      from a zero-parameter Hodge probe by protocol, whatever its role")
    P("      in the framework.")
    P("  R9: 16pi^3 is not among the locked tools and has no definition in the")
    P("      probe scope; probed anyway as fold lore and killed for missing data.")
    P("")

    # ---------------- MISSES ----------------
    P("-" * 78)
    P("MISSES (reported, never hidden)")
    P("-" * 78)
    P("  * The framework supplies NO variety of complex dimension >= 4 - the")
    P("    regime where the rational Hodge conjecture is OPEN in general (and")
    P("    where integral Hodge is known to fail, Atiyah-Hirzebruch).")
    P("  * No Hodge class, no period matrix, no algebraic cycle, and no mechanism")
    P("    tying any fold number to cohomology appears anywhere in the locked")
    P("    toolset (workspace grep for 'hodge': 0 hits across papers/, scripts/,")
    P("    briefs/, prompts/, sparc/, predictions/, audit/).")
    P("  * No positive claim survived: rows 1,2,3,5,7 are killed by vacuity or")
    P("    by theorem; rows 6,9 die on missing lattice/variety data; row 8 is")
    P("    disqualified as fitted; only row 4 is true - and it is classical")
    P("    mathematics to which PWC contributes nothing.")
    P("  * Even the best ladder step available - powers of a CM elliptic curve -")
    P("    is settled territory: the Hodge conjecture holds for abelian")
    P("    varieties of dimension <= 3 (Lefschetz + hard Lefschetz) and for CM")
    P("    abelian fourfolds (Tankeev/Shioda 1981), so PWC's torus cannot reach")
    P("    the open part of the conjecture from below.")
    P("")

    # ---------------- SECTION C: verdict ----------------
    P("-" * 78)
    P("SECTION C - verdict (5 lines)")
    P("-" * 78)
    P("1. VERDICT, SAID LOUDLY: Phase Wave Cosmology has NO GENUINE HODGE HANDLE YET -")
    P("   every locked number (19/18, 5pi^2, 16pi^3, delta = 1.5321e-5) fails to touch a")
    P("   Hodge class on any named variety, and the one true statement available is")
    P("   classical, not PWC.")
    P("2. Most promising angle: the quicycle torus itself - Hdg^2(E,Q) = Q.[E] with [E]")
    P("   algebraic (Lefschetz (1,1)) is a real zero-parameter Hodge fact, and 19 does")
    P("   exist in algebraic geometry as the Heegner discriminant -19 (j = -96^3")
    P("   integral, A4) - but neither is earned by the framework.")
    P("3. The honest gap: the torus theorem holds for every curve with or without PWC's")
    P("   constants, and the 19 stays a numerological echo unless PWC states the fold")
    P("   lattice's complex structure tau and shows it is homothetic to")
    P("   Z[(-1+sqrt(-19))/2] (a square torus gives D = -4, j = 1728, not -19).")
    P("4. Where Hodge content actually lives - smooth projective varieties of complex")
    P("   dim >= 4 with non-trivial Hodge classes, where the conjecture is open - the")
    P("   framework supplies no variety, no class, no period, no cycle.")
    P("5. Next step: to earn a handle, PWC must (a) declare tau of the fold torus and")
    P("   compute its periods/j-invariant, and (b) construct a specific dim >= 4 variety")
    P("   with a candidate non-algebraic Hodge class that a PWC constant decides; until")
    P("   then 'no genuine Hodge handle' is the correct, honest result.")
    P("")
    P("EXIT 0 - probe completed honestly; the exit code reflects protocol completion,")
    P("not endorsement of any candidate.")

    text = "\n".join(L)
    print(text)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "probe_hodge_report.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print("\n[report written to %s]" % out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
