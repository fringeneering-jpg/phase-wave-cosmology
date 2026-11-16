import math

# LOCKED CONSTANTS FROM quantify_pt_c.py & quantify_pt_d.py
c0       = 2.99792458e8
hbar     = 1.054571817e-34
MEV_J    = 1.602176634e-13
hbarc    = hbar * c0 / (MEV_J * 1e-15)
alpha    = 1.0 / 137.035999084
R_p_fm   = 0.84
rho_core = 2.3e17
m_p      = 938.272088
m_n      = 939.5654205
m_e      = 0.51099895

E_bound  = m_p / 57.0
a_V      = (18.0 / 19.0) * E_bound               # 15.5945 MeV
a_S      = (20.0 / 19.0) * E_bound               # 17.3273 MeV
a_C_c    = (8.0 / 19.0) * alpha * hbarc / R_p_fm # 0.7218 MeV (quantify_pt_c: 8 chiral pairs / 19 shares)
m_p_kg   = m_p * 1e6 * 1.602176634e-19 / (c0**2)
r0_fm    = (3.0 * m_p_kg / (4.0 * math.pi * rho_core))**(1.0/3.0) * 1e15
a_C_d    = 0.6 * alpha * hbarc / r0_fm           # 0.7189 MeV (quantify_pt_d: r0 from rho_core)

a_A_b    = a_V * (28.0 / 19.0)                   # 22.9814 MeV (quantify_pt_b)
a_A_c    = 18.0 * (m_n - m_p)                    # 23.2800 MeV (quantify_pt_c)
a_A_d    = (27.0 / 20.0) * a_S                   # 23.3919 MeV (quantify_pt_d)
a_p      = 12.0                                  # 3*N/4 = 12.0 MeV

# Heavy shell stabilization from relativistic 1/2-spin hold: 2*(a_S - a_V)*(17/19) = 3.1006 MeV
E_scale  = 2.0 * (a_S - a_V)                     # 3.4654 MeV
E_sh_50_82_126 = E_scale * (17.0 / 19.0)         # 3.1006 MeV

def delta(A, Z):
    if Z % 2 == 0 and (A - Z) % 2 == 0:
        return a_p / math.sqrt(A)
    if Z % 2 == 1 and (A - Z) % 2 == 1:
        return -a_p / math.sqrt(A)
    return 0.0

def heavy_shell(Z, N):
    # Proximity to 50, 82, 126 magic closures (within +/-2 nucleons)
    sh = 0.0
    for m in (50, 82, 126):
        if abs(Z - m) <= 2:
            sh += E_sh_50_82_126 * (1.0 - 0.4 * abs(Z - m))
        if abs(N - m) <= 2:
            sh += E_sh_50_82_126 * (1.0 - 0.4 * abs(N - m))
    return sh

# Embedded AME2020 anchors from quantify_pt_d.py (using AME2020 column)
PT_D = [
    ("Ba-138", 138, 56, 1158.29),
    ("Nd-142", 142, 60, 1185.14),
    ("Sm-152", 152, 62, 1251.80),
    ("Gd-158", 158, 64, 1303.20),
    ("Dy-164", 164, 66, 1347.20),
    ("Er-168", 168, 68, 1379.90),
    ("Hf-180", 180, 72, 1447.90),
    ("W-184",  184, 74, 1486.50),
    ("Os-192", 192, 76, 1546.90),
    ("Pt-195", 195, 78, 1545.67),
    ("Hg-202", 202, 80, 1595.18),
    ("Pb-208", 208, 82, 1636.45),
    ("Bi-209", 209, 83, 1640.20),
    ("Th-232", 232, 90, 1766.70),
    ("U-238",  238, 92, 1801.69),
]

print("=" * 94)
print(" PWC PERIODIC TABLE D (Cs..U, Z=55..92): BARE SEMF VS +(N-Z)*m_e HEAVY CLOCK-RATE HOLD")
print("=" * 94)
print(f" {'Isotope':<8} | {'(Z, N)':<9} | {'N-Z':<4} | {'AME2020':<9} | {'Old pt_d Res':<13} | {'+(N-Z)*m_e':<11} | {'With Hold+Shell'}")
print("-" * 94)

old_s2, new_s2 = 0.0, 0.0
old_sum, new_sum = 0.0, 0.0

for name, A, Z, B_ame in PT_D:
    N = A - Z
    B_old = a_V*A - a_S*(A**(2.0/3.0)) - a_C_d*(Z**2)/(A**(1.0/3.0)) - a_A_d*((N-Z)**2)/A + delta(A, Z)
    res_old = B_ame - B_old

    # In the heavy slowed-clock zone, each excess neutron holds its electron mass +(N-Z)*m_e
    # and uses the exposed-thread debt a_A_c = 18*(m_n - m_p) = 23.28 MeV:
    B_new = (a_V*A - a_S*(A**(2.0/3.0)) - a_C_d*(Z**2)/(A**(1.0/3.0))
             - a_A_c*((N-Z)**2)/A + delta(A, Z) + (N - Z)*m_e + heavy_shell(Z, N))
    res_new = B_ame - B_new

    old_s2 += res_old**2; new_s2 += res_new**2
    old_sum += res_old;   new_sum += res_new
    print(f" {name:<8} | ({Z:2d},{N:3d}) | {N-Z:4d} | {B_ame:9.2f} | {res_old:+11.2f}   | {(N-Z)*m_e:+9.2f}   | {res_new:+10.2f} MeV")

n_iso = len(PT_D)
print("-" * 94)
print(f" OLD quantify_pt_d.py (no electron hold) -> Mean bias: {old_sum/n_iso:+.2f} MeV | RMS: {math.sqrt(old_s2/n_iso):.2f} MeV")
print(f" NEW with +(N-Z)*m_e + 50/82/126 shells  -> Mean bias: {new_sum/n_iso:+.2f} MeV | RMS: {math.sqrt(new_s2/n_iso):.2f} MeV")
print("=" * 94)
