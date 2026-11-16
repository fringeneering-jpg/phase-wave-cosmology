"""
probe_riemann.py
================
Probe of the Riemann Hypothesis through Phase Wave Cosmology's "No-Zeros law".
Honest labels only: PROVEN-BY-ALGEBRA / CLAIMED / OPEN.  Zero fitted parameters.

Framework constants under test (as given, provenance inline):
  phi   = (1+sqrt(5))/2
  delta = (6*phi^2 - 5*pi)/(5*pi)   ~ 1.5321e-5   ("golden-bridge residual")
  s     = 1/19,  T = 27,  N = 16 = 4*pi/(pi/4),  {1,5} spectrum,
  P_amb = 2.4806e-10 Pa,  Omega_amb = 2.4555e-18 s^-1  (the "wibble floor")
"""
import sys
import mpmath
from mpmath import mp

W = 78

def banner(t):
    print()
    print("=" * W)
    print(t)
    print("=" * W)

def xi(s):
    s = mp.mpc(s)
    return mp.mpf(1) / 2 * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)

print("mpmath version:", mpmath.__version__, "| python:", sys.version.split()[0])
mp.dps = 60

phi = (1 + mp.sqrt(5)) / 2
delta = (6 * phi ** 2 - 5 * mp.pi) / (5 * mp.pi)

banner("TASK 1 - THE GEOMETRY HANDLE: xi(s) = xi(1-s), axis Re(s) = 1/2")
print("The reflection s -> 1-s fixes exactly the vertical line Re(s) = 1/2.")
print("Numerical check of |xi(s) - xi(1-s)| at dps = %d:" % mp.dps)
worst = mp.mpf(0)
for s in [mp.mpc('0.3', '10.2'), mp.mpc('0.77', '-5.31'), mp.mpc('1.7', '3.3'),
          mp.mpc('0.5', '14.13472514173469379045725198356247027078425711569924'),
          mp.mpc('-0.2', '2.0')]:
    d = abs(xi(s) - xi(1 - s))
    worst = max(worst, d)
    print("    s = %s + %s i    |xi(s) - xi(1-s)| = %s"
          % (mp.nstr(s.real, 10), mp.nstr(s.imag, 10), mp.nstr(d, 6)))
print("    worst deviation = %s  -> symmetry holds to full working precision." % mp.nstr(worst, 6))
print("    STATUS: PROVEN-BY-ALGEBRA (Riemann 1859; classical functional equation).")
print("    The framework's 'geometry lever' IS this theorem and this axis - Riemann's, not the framework's.")
print("    Renaming a known theorem transfers no credit and adds no content.")
print("    Corollary check: xi is REAL on the critical line (FE + Schwarz reflection):")
for t in (mp.zetazero(1).imag, mp.mpf(27), mp.mpf(100)):
    v = xi(mp.mpc(0.5) + mp.mpc(0, 1) * t)
    print("        xi(1/2 + %s i):  Re = %s   Im = %s"
          % (mp.nstr(t, 14), mp.nstr(v.real, 22), mp.nstr(v.imag, 6)))

banner("TASK 2 - THE NO-ZEROS REINTERPRETATION: zeros vs 'equilibrium points'")
z1 = mp.zetazero(1)
print("First nontrivial zero computed by mpmath (dps=%d):" % mp.dps)
print("    rho_1 = 1/2 + i * %s" % mp.nstr(z1.imag, 60))
print("First 12 zero heights and |zeta| at each zero:")
for k in range(1, 13):
    z = mp.zetazero(k)
    print("    #%2d : 1/2 + %s i   |zeta(z)| = %s" % (k, mp.nstr(z.imag, 30), mp.nstr(abs(mp.zeta(z)), 5)))
print()
print("Is |zeta| at a zero really zero, or a 'floor'?  Same zero, increasing dps:")
for d in (20, 40, 80):
    mp.dps = d
    z = mp.zetazero(1)
    print("    dps=%3d : |zeta(rho_1)| = %s    <- scales like 10^-dps: pure rounding noise"
          % (d, mp.nstr(abs(mp.zeta(z)), 6)))
mp.dps = 60
print("    => |zeta| at rho_1 is consistent with EXACT zero to 80 digits.")
print("    => Any 'No-Zeros' floor on the critical line larger than ~1e-78 is FALSIFIED by computation;")
print("       P_amb = 2.4806e-10 (Pa) as a zeta floor is dead on arrival.")
print()
print("Shape of |zeta| around rho_1 (the 'equilibrium point'):")
t1 = mp.zetazero(1).imag
print("    along the line:   t                      |zeta(1/2 + i t)|")
for t in (t1 - mp.mpf('0.2'), t1 - mp.mpf('0.1'), t1, t1 + mp.mpf('0.1'), t1 + mp.mpf('0.2')):
    print("                     %s   %s" % (mp.nstr(t, 22), mp.nstr(abs(mp.zeta(mp.mpc(0.5) + mp.mpc(0, 1) * t)), 8)))
print("    at fixed height:  sigma   |zeta(sigma + i t1)|   (minimum at sigma = 1/2, as RH requires)")
for sig in ('0.35', '0.45', '0.50', '0.55', '0.65'):
    print("                      %s    %s" % (sig, mp.nstr(abs(mp.zeta(mp.mpc(sig) + mp.mpc(0, 1) * t1)), 8)))
print()
print("Off the critical line at the SAME height (no zero off the line at t1):")
for sig in ('0.30', '0.40', '0.60', '0.75'):
    s = mp.mpc(sig) + mp.mpc(0, 1) * t1
    print("    |zeta(%s + %s i)| = %s" % (sig, mp.nstr(t1, 22), mp.nstr(abs(mp.zeta(s)), 12)))
print("    Known (PROVEN-BY-ALGEBRA, Hadamard / de la Vallee Poussin 1896): zeta has NO zeros on Re(s)=1.")
print("    Known (computation, Gourdon 2004; Platt/Trudgian to 3e12): first 1e13 nontrivial zeros all on the line.")
print()
print("    PWC claim 'the floor forbids any off-line zero':  STATUS = CLAIMED.")
print("    Kill condition: derive from the framework's OWN axioms (pressure/density/geometry) a quantitative")
print("      bound |zeta(s)| >= c(Re s) > 0 for Re(s) != 1/2, WITHOUT assuming RH.  No such derivation exists;")
print("      asserting it is asserting RH in different words.")
print("    Also: P_amb (Pa) and Omega_amb (s^-1) are dimensionful; no dimensionless combination of them can")
print("      constrain an analytic function unless a bridge is defined.  None is.")

banner("TASK 3 - THE OPERATOR QUESTION: is {1,5} / N=16 a Hilbert-Polya candidate?")
print("Checklist for a Hilbert-Polya candidate:")
print("    [ ] a self-adjoint operator H on some Hilbert space ......... NO (nothing is defined)")
print("    [ ] a spectral measure / eigenvalue equation ................. NO")
print("    [ ] a bijection spec(H) <-> {t_n : zeta(1/2 + i t_n) = 0} .... NO")
print("    [ ] a trace formula or zeta-determinant linking to zeta ...... NO")
print()
print("N = 16 = 4*pi/(pi/4) = %s : an arithmetic identity (pi cancels). It counts nothing about zeta."
      % mp.nstr(4*mp.pi/(mp.pi/4), 10))
print("Do the first 16 zero heights show the {1,5} structure on the 16-fold clock?")
print("    k    t_n mod 2pi       t_n/(pi/4)     dist to nearest integer")
best = (0, mp.mpf(1))
for k in range(1, 17):
    t = mp.zetazero(k).imag
    q = t / (mp.pi / 4)
    d = abs(q - mp.nint(q))
    if d < best[1]:
        best = (k, d)
    print("   %2d    %12s     %12s        %s" % (k, mp.nstr(t % (2*mp.pi), 8), mp.nstr(q, 8), mp.nstr(d, 5)))
print("    best integer hit: k=%d, distance %s" % (best[0], mp.nstr(best[1], 6)))
print("    (16 uniform draws -> expected best distance 1/34 = 0.0294; an observed 0.003 is a ~9.5%-level fluke,")
print("     and k=1 is the most numerology-hunted index of all.  No {1,5}, no 2-1-2 cage, no 18/19 residues.)")
print("    The '2-1-2 cage' is not defined in the probe brief, so it cannot be tested: reported as a miss.")
print("    Even a perfect 16-point pattern could not discriminate RH: the spectral object needs ALL {t_n}.")
print("    STATUS: OPEN - and not yet a candidate: a Hilbert-Polya candidate IS an operator, and none is defined.")
print("    Kill condition: exhibit self-adjoint H and prove spec(H) = {t_n}.")

banner("TASK 4 - ARITHMETIC ECHOES: phi, 19, 27, delta, 18/19 in zeta land?")
print("Framework numbers (definitions only, zero fitting):")
print("    phi   = %s" % mp.nstr(phi, 22))
print("    delta = (6 phi^2 - 5 pi)/(5 pi) = %s  (= 1.5321e-5)" % mp.nstr(delta, 15))
print("    delta != 0: PROVEN-BY-ALGEBRA (pi transcendental, Lindemann 1882 => 6 phi^2 - 5 pi != 0).")
print("    Trivial nonzero-ness; it says NOTHING about zeta zeros.")
print()
print("Does delta equal any canonical zeta-land constant? (raw differences, no fitting):")
for name, c in [("euler gamma", mp.euler), ("ln 2", mp.log(2)), ("1/zeta(3)", 1/mp.zeta(3)),
                ("1/zeta(2)", 6/mp.pi**2), ("e - pi", mp.e - mp.pi), ("1/phi^2", 1/phi**2),
                ("zeta(1/2)", mp.zeta(mp.mpf('0.5'))), ("1/(2 pi)", 1/(2*mp.pi))]:
    print("    |delta - %-12s| = %s" % (name, mp.nstr(abs(delta - c), 6)))
print("    => delta matches nothing canonical in zeta land.  No echo.")
print()
print("phi:  zeta(phi) = %s , zeta(1/phi) = %s  - no closed forms; phi is absent from the classical"
      % (mp.nstr(mp.zeta(phi), 14), mp.nstr(mp.zeta(1/phi), 14)))
print("      zeta literature as a structural constant.  No echo.")
print()
print("19 and 27:")
print("    zeta(19) - 1 = %s  vs  2^-19 = %s   (geometric-tail identity for ANY integer n > 1; not an echo)"
      % (mp.nstr(mp.zeta(19) - 1, 10), mp.nstr(mp.mpf(2)**(-19), 10)))
print("    zeta(27) - 1 = %s  vs  2^-27 = %s   (same trivial tail; not an echo)"
      % (mp.nstr(mp.zeta(27) - 1, 10), mp.nstr(mp.mpf(2)**(-27), 10)))
print("    |zeta(1/2 + 27 i)| = %s  - 27 sits between zeros t=25.0109 and t=30.4249; nothing special."
      % mp.nstr(abs(mp.zeta(mp.mpc('0.5', '27'))), 12))
print("    the 27th zero height is %s (not 27)." % mp.nstr(mp.zetazero(27).imag, 12))
print()
print("18/19 split, honest arithmetic:")
print("    zeta(18/19)  = %s" % mp.nstr(mp.zeta(mp.mpf(18)/19), 14))
print("    -19 + gamma  = %s" % mp.nstr(mp.mpf(-19) + mp.euler, 14))
print("    zeta(s) = 1/(s-1) + gamma + O(s-1) near s=1: s = 18/19 inserts the pole term -19 BY DEFINITION.")
print("    Any s = 1 - 1/n gives zeta(s) ~ -n + gamma.  The 19 is pole arithmetic, not zeta structure.")
print("    zeta(1/19)   = %s  (sits near zeta(0) = -1/2; nothing canonical about 1/19)"
      % mp.nstr(mp.zeta(mp.mpf(1)/19), 14))
print("    1/19 has decimal period 18 because 10 has order 18 mod 19:")
for d in (1, 2, 3, 6, 9, 18):
    print("        10^%2d mod 19 = %d" % (d, pow(10, d, 19)))
print()
print("THE one real (18,19) fact inside zeta land - von Staudt-Clausen (1840, PROVEN-BY-ALGEBRA):")
print("    p | denom(B_k)  <=>  (p-1) | k.   With k = 18: p-1 | 18 gives p in {2,3,7,19}.")
print("    B_18 = %s ;  798 * B_18 = %s (an integer)" % (mp.nstr(mp.bernoulli(18), 22), mp.nstr(mp.mpf(798)*mp.bernoulli(18), 20)))
print("    denom(B_18) = 2*3*7*19 = 798, and zeta(18) = (-1)^{k+1} B_18 (2 pi)^18 / (2 * 18!), k=9.")
print("    i.e. 19 genuinely enters zeta(18) because 19-1 = 18.  TRUE arithmetic - but the framework never")
print("    invokes it, and its own 18/19 is 1 - 1/19 (pole at s=1), not k=18.  Retrofit, not derivation.")
print("    As an echo: COINCIDENCE UNTIL MECHANISM.  (Strongest echo found - and it is not the framework's.)")
print()
print("    The 'knot's prime-like structure' is not defined in the probe brief, so it cannot be tested")
print("    against the Euler product.  Reported as a miss, not hidden.")
print()
print("Standard zeta facts the framework cites (all PROVEN-BY-ALGEBRA; none derived by the framework):")
print("    zeta(2)  = %s  = pi^2/6 = %s   (Euler 1735)" % (mp.nstr(mp.zeta(2), 15), mp.nstr(mp.pi**2/6, 15)))
print("    zeta(-1) = %s  = -1/12           (Euler; analytic continuation)" % mp.nstr(mp.zeta(-1), 15))
print("    zeta(3)  = %s  (Apery 1979: irrational)" % mp.nstr(mp.zeta(3), 15))
print("    2 pi^4/(45 zeta(3)) = %s  - photon-entropy coefficient (matches the framework's 3.6016)."
      % mp.nstr(2*mp.pi**4/(45*mp.zeta(3)), 12))
print("    zeta(3) enters because Bose-Einstein integrals evaluate to Gamma*zeta products; standard physics")
print("    (Planck 1900), PROVEN-BY-ALGEBRA; borrowing a standard result is not a framework result.")

banner("TASK 5 - THE HONEST VERDICT (SAID LOUDLY)")
print("""
THE FRAMEWORK HAS NO GENUINE RH HANDLE.  IT IS A POETIC READING ONLY.

  * What it HAS: Riemann's functional equation and its axis Re(s)=1/2 - proven by Riemann (1859),
    re-verified here to 60 digits.  Calling it 'the geometry lever' relabels; it adds nothing.
  * What it ASSERTS: 'the zeros are not true zeros but equilibrium points.'  The literal reading is
    numerically DEAD: |zeta| at the known zeros is rounding noise down to 10^-78 - exact zeros.
    The charitable reading ('all equilibrium points sit on the line') is RH itself, reworded.
  * What it LACKS: an operator, a spectral measure, a zero-free-region bound, or any mechanism
    linking P_amb / Omega_amb / phi / 19 / 27 / delta / {1,5} / N=16 to the zeta function.
  * Dimensionful constants (Pa, s^-1) cannot constrain an analytic function without an invented
    bridge; no bridge is defined anywhere in the framework.
  * The one real 18/19 arithmetic fact (19 | denom(B_18), von Staudt-Clausen 1840) is a theorem the
    framework never invokes and cannot derive; as evidence it is a retrofit coincidence.
  * Recall: RH <=> pi(x) = li(x) + O(sqrt(x) log x) (von Koch 1901).  Any 'reading' that does not
    yield either a proof, an operator, or a zero-free region changes none of that.

NO NUMBER THEORIST IS OBLIGED TO ENGAGE ANY OF THIS AS PROPOSED.
""")

banner("RESULT TABLE")
rows = [
 ("xi(s)=xi(1-s); axis Re(s)=1/2 ('geometry lever')",
  "PROVEN-BY-ALGEBRA",
  "none needed; classical since Riemann 1859",
  "nothing - framework only relabels a known theorem"),
 ("'Zeros are not true zeros but equilibrium points'",
  "CLAIMED; literal reading FALSIFIED",
  "|zeta(rho_1)| is 10^-80-level noise = exact zero; any floor > 1e-78 dies",
  "proof that every equilibrium point lies on Re(s)=1/2 - that IS RH"),
 ("'The floor forbids any off-line zero'",
  "CLAIMED; no mechanism; = RH in disguise",
  "exhibit an off-line zero, or derive |zeta(s)| >= c(Re s) > 0 off-line from framework axioms",
  "a quantitative zero-free-region bound derived WITHOUT assuming RH"),
 ("{1,5} / N=16 as a Hilbert-Polya operator candidate",
  "OPEN - not yet a candidate",
  "exhibit self-adjoint H with spec(H) = {t_n}; first-16 residues show no {1,5} structure",
  "the operator H, the Hilbert space, the spectral measure, the eigenvalue map"),
 ("phi / 19 / 27 / delta / 18-19 echoes in zeta land",
  "COINCIDENCE (von Staudt 19|denom(B_18) real but mechanismless)",
  "every canonical match fails (printed above); retrofit, not derivation",
  "a derivation from framework axioms to any zeta quantity"),
 ("delta != 0, transcendental (Lindemann-Weierstrass)",
  "PROVEN-BY-ALGEBRA (trivial)",
  "-",
  "a link from delta to the zeros; none exists"),
]
print("%-44s | %-42s | %-46s | %s" % ("CANDIDATE", "STATUS", "KILL CONDITION", "WHAT A NUMBER THEORIST DEMANDS"))
print("-" * 205)
for r in rows:
    print("%-44s | %-42s | %-46s | %s" % r)
print("-" * 205)

banner("5-LINE SUMMARY")
print(" 1. Strongest checkable echo: von Staudt-Clausen gives 19 | denom(B_18) = 798 - the one real (18,19)")
print("    fact in zeta land; but the framework neither derives nor invokes it, so as an echo it is coincidence.")
print(" 2. Honest gap: no operator, no spectral measure, no zero-free-region bound; the 'No-Zeros' floor is")
print("    numerically falsified (|zeta| < 1e-78 at rho_1), and 'equilibrium points on the line' IS RH reworded.")
print(" 3. Next step: define a self-adjoint operator with spectrum {t_n}, or derive an off-line lower bound for")
print("    |zeta| from the framework's own axioms; anything short of that has zero RH content.")
print(" 4. The only PROVEN content the framework touches (functional equation, zeta(2), zeta(3) entropy) is")
print("    standard mathematics and physics it borrows, not results it produces.")
print(" 5. VERDICT: POETIC READING ONLY - no genuine RH handle; a number theorist must engage nothing here.")
print()
print("probe_riemann.py: exit 0")
sys.exit(0)
