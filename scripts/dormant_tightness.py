# dormant_tightness.py - the non-eating split (2026-10-17)
# The eating adds the accretion's heat; the NON-eating are the pure friction.
# The prediction: the dormant's collapse to a tight relation (the T from the
# size/shell/speed alone); the active's scatter above it.
import numpy as np

T_MAX = 5.51e7
C_BOW = 958e3
c0 = 2.9979e8
G = 6.674e-11
M_sun = 1.989e30
a0 = 6.611e-11

def reach(M):
    # the framework's shell scale: r_t = sqrt(GM/a0) (the papers' own)
    return np.sqrt(G * M / a0)

def T_predict(M, v, f_vent, x_factor=10.0):
    # the friction-only temperature at X = 10 . r_t
    R = reach(M)
    R_shell = R
    mu_bow = (v / C_BOW)**2
    mu_amb = (v / c0)**2
    T_surf = T_MAX * f_vent * (1.0 + mu_bow + mu_amb)
    x = x_factor * R_shell
    return T_surf * (R_shell / x) ** 0.5, R

# the dormant anchors: the quiet ones (no significant accretion)
dormant = [
    ("Sgr A*",      4.15e6, 0.0,  1.0e7),
    ("M87*",        6.50e9, 0.0,  2.3e7),
    ("M31*",        1.40e8, 0.0,  8.0e7),
]
# the active ones: the eaters (the accretion's extra heat)
active = [
    ("3C 273",      1.0e9,  0.0,  1.0e8),   # the quasar's the hot's
    ("NGC 4258",    3.9e7,  0.0,  1.0e7),
]

print("THE DORMANT SPLIT - the non-eating tightness test:")
print(f"  {'name':12s} {'M':>8s} {'r_t (pc)':>10s} {'T_obs':>10s} {'T_friction':>12s} {'ratio':>8s}")
rows = []
for name, M, v, T_obs in dormant:
    T_f, R = T_predict(M * M_sun, v, 0.5)   # the f_vent = 0.5's the stated's
    rows.append((name, M, R/3.0857e16, T_obs, T_f, T_obs/T_f))
    print(f"  {name:12s} {M:8.1e} {R/3.0857e16:10.1f} {T_obs:10.1e} {T_f:12.2e} {T_obs/T_f:8.2f}")
print()
for name, M, v, T_obs in active:
    T_f, R = T_predict(M * M_sun, v, 0.5)
    print(f"  {name:12s} {M:8.1e} {R/3.0857e16:10.1f} {T_obs:10.1e} {T_f:12.2e} {T_obs/T_f:8.2f}  <- EATING")
print()
# the tightness: the dormant's ratio spread
ratios = [r[5] for r in rows]
print(f"  the dormant's T_obs/T_friction ratios: {[f'{x:.2f}' for x in ratios]}")
print(f"  the spread: {max(ratios)/min(ratios):.2f}x")
print()
print("the honest frame: the dormant's ratios should cluster (the tight's); the")
print("eater's ratio should sit ABOVE (the accretion's extra). The f_vent = 0.5")
print("is the stated share; the framework's own shell's the r_t's reach.")
