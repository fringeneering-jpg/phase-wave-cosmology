import os, math

p_dir = "C:/Users/jaden/Downloads/PWC-Check/PWC/scripts"
for fn in sorted(os.listdir(p_dir)):
    if fn.startswith("quantify_"):
        print(">>> FOUND SCRIPT:", fn)

# Locked Constants from quantify_pt_b.py
c0 = 2.99792458e8
hbar = 1.054571817e-34
alpha = 1.0 / 137.035999084
J_per_MeV = 1.602176634e-13
hbar_c = hbar * c0 * 1.0e15 / J_per_MeV  # 197.32698 MeV*fm

m_p = 938.272088
m_e = 0.51099895
R_p_fm = 0.84
rho_core = 2.3e17

# 1. Locked SEMF from quantify_pt_b.py
E_bound = m_p / 57.0                     # 16.4609 MeV
a_V = (18.0 / 19.0) * E_bound            # 15.5945 MeV
a_S = (20.0 / 19.0) * E_bound            # 17.3273 MeV
a_A = a_V * (28.0 / 19.0)                # 22.9814 MeV (from quantify_pt_b.py!)

# 2. The Two Locked Zero-Parameter Coulomb Routes (Eliminating the back-solved 6/5 in quantify_elements.py)
m_p_kg = m_p * 1.78266192e-30
r0_core_fm = (3.0 * m_p_kg / (4.0 * math.pi * rho_core)) ** (1.0 / 3.0) * 1.0e15  # 1.2019 fm
r0_cage_fm = R_p_fm * (57.0 / 40.0)                                               # 1.1970 fm

a_C_core = (3.0 / 5.0) * alpha * hbar_c / r0_core_fm                              # 0.7188 MeV
a_C_cage = (3.0 / 5.0) * alpha * hbar_c / r0_cage_fm                              # 0.7218 MeV

print("=" * 88)
print(" 1. CLOSING THE COULOMB 6/5: LATTICE 57/40 VS CORE DENSITY r0 (ZERO BACK-SOLVING)")
print("=" * 88)
print(f" r0 from rho_core (2.3e17 kg/m^3) : {r0_core_fm:.4f} fm -> a_C = {a_C_core:.4f} MeV")
print(f" r0 from Cage Lattice R_p*(57/40) : {r0_cage_fm:.4f} fm -> a_C = {a_C_cage:.4f} MeV (Diff: {100*(a_C_cage/a_C_core - 1):+.2f}%)")
print(f" Why quantify_elements needed 6/5 : (57/40)*(q'/e)^2 = {(57.0/40.0)*(0.9103**2):.4f} vs 6/5 = 1.2000!")
print(f" Fission Limit Z^2/A = 2*a_S/a_C  : {2.0*a_S/a_C_core:.2f} (core) | {2.0*a_S/a_C_cage:.2f} (cage) [Empirical: 47-50]")

# 3. Test quantify_pt_b.py + Excess-Neutron Electron Hold (N - Z)*m_e across Na -> U
print("\n" + "=" * 88)
print(" 2. TESTING YOUR (N - Z)*m_e EXCESS-ELECTRON HOLD ON HEAVY NUCLEI (Cs -> U)")
print("=" * 88)
print(f" {'Isotope':<8} | {'(Z, N)':<9} | {'N-Z':<4} | {'AME2020 BE':<11} | {'Bare PWC d':<12} | {'+(N-Z)*m_e':<11} | {'New Residual'}")
print("-" * 88)

heavy_test = [
    ("Ar-40",  18,  22,  343.8108),
    ("Fe-56",  26,  30,  492.2539),
    ("Ge-74",  32,  42,  645.6649),
    ("Sn-120", 50,  70, 1020.5460),
    ("Cs-133", 55,  78, 1118.5320),
    ("Nd-142", 60,  82, 1185.1450),
    ("W-184",  74, 110, 1472.9340),
    ("Au-197", 79, 118, 1559.4000),
    ("Pb-208", 82, 126, 1636.4300),
    ("Th-232", 90, 142, 1766.6900),
    ("U-238",  92, 146, 1801.6940),
]

for name, Z, N, B_obs in heavy_test:
    A = Z + N
    # Exact bare SEMF from quantify_pt_b.py
    B_pwc = a_V * A - a_S * (A ** (2.0/3.0)) - a_C_core * (Z ** 2) / (A ** (1.0/3.0)) - a_A * ((N - Z) ** 2) / A
    d_bare = B_obs - B_pwc
    e_hold = (N - Z) * m_e
    d_new = B_obs - (B_pwc + e_hold)
    print(f" {name:<8} | ({Z:2d},{N:3d}) | {N-Z:4d} | {B_obs:11.2f} | {d_bare:+10.2f}   | {e_hold:+9.2f}   | {d_new:+10.2f} MeV")
print("=" * 88)
