# t6_lorentz_legs.py - the T6 Lorentz legs, mechanical accounting (PROPOSED, 2026-10-20)
# The medium is static - the knots are a sieve. A moving glass block of
# index n delays the wave only during the knot-trench traversals; the
# interstitial medium is NOT dragged.
#
# Two framework-native readings, computed side by side:
#   (A) the trench-carry accounting: the wave is trapped in the trenches for
#       the fraction (n-1)/n of its transit and is carried at the block's
#       speed v only while trapped -> drag coefficient (1 - 1/n).
#   (B) the speed-budget reading: the framework's own budget c_loc^2 + v_ff^2
#       = c0^2 gives the knots the flow-budget share v_ff^2/c0^2 = (1 - 1/n^2)
#       -> drag coefficient (1 - 1/n^2), which is Fresnel/Fizeau's.
# PROPOSED: verification script only - the T6 legs stay OPEN in the canon
# until the coefficient question is ruled.
import math

c0 = 2.99792458e8

def fizeau(v, n, method):
    if method == "A":
        f = 1.0 - 1.0 / n
    else:
        f = 1.0 - 1.0 / n ** 2
    return c0 / n + v * f

print("=" * 74)
print("THE T6 LORENTZ LEGS - the moving sieve of knots (medium static)")
print("=" * 74)
print("The wave travels c0 in the interstices and is delayed only inside")
print("the knot-trenches of the glass (index n). The medium is never dragged.")
print()
for n in (1.5, 1.33, 1.000293):   # glass, water, air
    v = 10.0  # m/s, the Fizeau-scale block speed
    vA = fizeau(v, n, "A")
    vB = fizeau(v, n, "B")
    print("n = %.6f:" % n)
    print("  (A) trench-carry   v_eff = c0/n + v(1 - 1/n)   = %.9f m/s" % vA)
    print("  (B) speed-budget   v_eff = c0/n + v(1 - 1/n^2) = %.9f m/s  (Fresnel/Fizeau)" % vB)
    print("  measured drag coefficient (Fizeau 1851): 1 - 1/n^2 = %.6f" % (1.0 - 1.0 / n ** 2))
    print()
print("Kennedy-Thorndike cavity null (1e-17):")
print("  the cavity is a bound EM equilibrium lattice - it self-compensates")
print("  and co-contracts with the local tension gradient, so a cavity-length")
print("  anisotropy below 1e-17 is the expected null, not a surprise:")
print("  no medium drag means no preferred-frame signal for the lattice itself.")
print()
print("Aberration: the static-medium reading is the same retarded-path")
print("kinematics as the cosmic sprinkler (the observer moves, the medium")
print("stands) - the apparent angle shift is v/c0 to first order, derived")
print("from kinematics, not from a dragged frame.")
print()
print("STATUS: PROPOSED - the T6 Lorentz legs stay OPEN in the canon until")
print("the (A)/(B) coefficient question is ruled; this script records both")
print("readings honestly without choosing for the framework.")
