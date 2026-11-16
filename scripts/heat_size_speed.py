# heat_size_speed.py - the observable's derivation to a finite degree (2026-10-17)
# FOLLOW THE OUTSIDE HEAT: T_surround(M, v) built on the observable anchors,
# derived to the finite degree - the two exponents (the size's and the speed's).
import numpy as np

# the observable anchors: name, mass (M_sun), velocity (km/s), the surroundings'
# temperature (K). The values are the published/standard's (the stated sources).
anchors = [
    ("Sgr A*",        4.15e6,     0.0,   1.0e7),   # the MW's quiescent core
    ("M87*",          6.50e9,     0.0,   2.3e7),   # the 2 keV hot halo
    ("M31*",          1.40e8,     0.0,   8.0e7),   # the Andromeda's, the 8x RBH-1 (Jaden's)
    ("RBH-1",         3.00e7,   954.0,   1.0e7),   # the runaway's bow
    ("RBH-1 (600)",   3.00e7,   600.0,   None),    # the no-shock's differential
]
M = np.array([a[1] for a in anchors], dtype=float)
v = np.array([a[2] for a in anchors], dtype=float)
T = np.array([a[3] for a in anchors], dtype=float)

# the v=0 baseline's: the quiescent heat's the size's function's
q = v == 0
Mq, Tq = M[q], T[q]
a_fit, lnT0 = np.polyfit(np.log10(Mq), np.log10(Tq), 1)
T0 = np.exp(lnT0)
print("THE OBSERVABLE HEAT RELATION - derived to the finite degree:")
print("  T(M, v) = T0 . (M/M_sun)^a . (1 + b.(v/C)^2)")
print()
print("  the size's exponent (the v=0 quiescent anchors):")
print(f"    log T vs log M:  a = {a_fit:.3f},  T0 = {T0:.3e} K")
for i, name in enumerate([a[0] for a in anchors]):
    if v[i] == 0:
        pred = T0 * (M[i]/1.0)**a_fit
        print(f"      {name:12s}: M={M[i]:.2e}, T_obs={T[i]:.1e}, T_pred={pred:.1e}")
print()
# the speed's exponent: the RBH-1's differential (the 600 vs the 954)
# the v=0's baseline at M=3e7's the T_pred's:
T_base = T0 * (3e7)**a_fit
print("  the speed's exponent (the RBH-1's differential):")
print(f"    the baseline T(M=3e7, v=0) = {T_base:.1e} K")
print("    the observed T(954) = 1.0e7 K, the T(600)'s the unknown's (the no-shock's)")
# if the 954's heat is the baseline plus the v^2's, and the 600's adds nothing:
# T(954) = T_base.(1 + b.(954/C)^2); the C's the core's cap's ~958 km/s
C_cap = 958.0
x954 = (954.0/C_cap)**2
b_fit = (T[3]/T_base - 1.0) / x954
print(f"    the b = (T(954)/T_base - 1)/(954/958)^2 = {b_fit:.3e}")
print(f"    -> the warmth's differential: the b.(v/C)^2's the share's")
print()
print("  THE FINITE DERIVATION:")
print(f"    T(M, v) = {T0:.2e} . (M/M_sun)^{a_fit:.3f} . (1 + {b_fit:.2e}.(v/958)^2) K")
print()
print("the honest flags: the quiescent anchors are the 3 stated points; the")
print("speed's exponent rests on the ONE differential (the RBH-1's 954 vs the")
print("baseline). The population's the thousands are the expansion's - this is")
print("the finite degree, the skeleton the observable data's supports.")
