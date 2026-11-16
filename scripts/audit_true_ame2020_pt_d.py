import math

# LOCKED CONSTANTS ONLY (ZERO FITTED PARAMETERS, ZERO RAMPS)
c0       = 2.99792458e8
hbar     = 1.054571817e-34
MEV_J    = 1.602176634e-13
hbarc    = hbar * c0 / (MEV_J * 1e-15)
alpha    = 1.0 / 137.035999084
rho_core = 2.3e17
m_p      = 938.272088
m_n      = 939.5654205
m_e      = 0.51099895

E_bound  = m_p / 57.0
a_V      = (18.0 / 19.0) * E_bound
a_S      = (20.0 / 19.0) * E_bound
m_p_kg   = m_p * 1e6 * 1.602176634e-19 / (c0**2)
r0_fm    = (3.0 * m_p_kg / (4.0 * math.pi * rho_core))**(1.0/3.0) * 1e15
a_C      = 0.6 * alpha * hbarc / r0_fm           # 0.7189 MeV
a_A      = (27.0 / 20.0) * a_S                   # 23.3919 MeV (exact locked quantify_pt_d a_A)
a_p      = 12.0                                  # 3*N/4 = 12.0 MeV

# Exact Heavy Shell Closure (strictly at Z or N in {50, 82, 126}, zero smoothing parameters!)
E_scale  = 2.0 * (a_S - a_V)                     # 3.4654 MeV
E_sh_heavy = E_scale * (17.0 / 19.0)             # 3.1006 MeV

def delta(A, Z):
    if Z % 2 == 0 and (A - Z) % 2 == 0:
        return a_p / math.sqrt(A)
    if Z % 2 == 1 and (A - Z) % 2 == 1:
        return -a_p / math.sqrt(A)
    return 0.0

def exact_magic_shell(Z, N):
    sh = 0.0
    if Z in (50, 82, 126): sh += E_sh_heavy
    if N in (50, 82, 126): sh += E_sh_heavy
    return sh

# Verified AME2020 Experimental Total Binding Energies (B/A * A from AME2020 table)
# Showing both the corrupted numbers that were in quantify_pt_d.py and true AME2020:
PT_D_TRUE = [
    ("Ba-138", 138, 56, 1158.29, 1158.29),
    ("Nd-142", 142, 60, 1185.14, 1185.15),
    ("Sm-152", 152, 62, 1251.80, 1253.11),
    ("Gd-158", 158, 64, 1303.20, 1295.90),
    ("Dy-164", 164, 66, 1347.20, 1338.04),
    ("Er-168", 168, 68, 1379.90, 1365.78),
    ("Hf-180", 180, 72, 1447.90, 1446.30),
    ("W-184",  184, 74, 1486.50, 1472.93),
    ("Os-192", 192, 76, 1546.90, 1526.12),
    ("Pt-195", 195, 78, 1579.60, 1545.68),
    ("Hg-202", 202, 80, 1638.80, 1595.16),
    ("Pb-208", 208, 82, 1636.45, 1636.43),
    ("Bi-209", 209, 83, 1640.20, 1640.24),
    ("Th-232", 232, 90, 1766.70, 1766.69),
    ("U-238",  238, 92, 1801.69, 1801.69),
]

print("=" * 98)
print(" TRUE AME2020 AUDIT OF PERIODIC TABLE D (Cs..U): ZERO RAMPS, LOCKED a_A = (27/20)*a_S")
print("=" * 98)
print(f" {'Isotope':<8} | {'(Z, N)':<9} | {'Bad pt_d BE':<11} | {'True AME20':<10} | {'Bare Res':<10} | {'+(N-Z)*m_e + Shell':<18}")
print("-" * 98)

bare_s2, hold_s2 = 0.0, 0.0
bare_sum, hold_sum = 0.0, 0.0

for name, A, Z, B_bad, B_true in PT_D_TRUE:
    N = A - Z
    B_bare = a_V*A - a_S*(A**(2.0/3.0)) - a_C*(Z**2)/(A**(1.0/3.0)) - a_A*((N-Z)**2)/A + delta(A, Z)
    B_hold = B_bare + (N - Z)*m_e + exact_magic_shell(Z, N)

    res_bare = B_true - B_bare
    res_hold = B_true - B_hold

    bare_s2 += res_bare**2; hold_s2 += res_hold**2
    bare_sum += res_bare;   hold_sum += res_hold
    flag = " <-- TYPO FIXED" if abs(B_bad - B_true) > 2.0 else ""
    print(f" {name:<8} | ({Z:2d},{N:3d}) | {B_bad:11.2f} | {B_true:10.2f} | {res_bare:+8.2f}   | {res_hold:+8.2f} MeV{flag}")

n_iso = len(PT_D_TRUE)
print("-" * 98)
print(f" BARE SEMF (True AME2020)                -> Mean bias: {bare_sum/n_iso:+.2f} MeV | RMS: {math.sqrt(bare_s2/n_iso):.2f} MeV")
print(f" WITH +(N-Z)*m_e + EXACT 50/82/126 SHELL -> Mean bias: {hold_sum/n_iso:+.2f} MeV | RMS: {math.sqrt(hold_s2/n_iso):.2f} MeV")
print("=" * 98)
