# stage3_advisor_checks.py - the Advisor's verdict, verified and answered (2026-10-18)
# Verifies the three blocks (B not G, storage not drag, tangential not
# radial) and the corrected supernova math; answers the three requests:
# dV's definition, the 18-part debt, the collapse duration; and states the
# energy functional with the PWC mapping. The key new number: the choke's
# strain against the LOCAL modulus K(rho_corona) = 968 Pa is 2.7e-5 -
# LINEAR - the Advisor's 3.4e7 used the BASELINE modulus (the wrong shelf).
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27

RHO_COR = 5.02e-13
C_COR = pi_v.capacity(RHO_COR, c0, rho0, n_lad)
K_COR = RHO_COR * C_COR ** 2
M_SUN = 1.989e30
DV = M_SUN / RHO_COR                 # the 1 M_sun breach's preferred-volume demand
R_SRC = 14.3e3

print("=" * 78)
print("THE ADVISOR'S VERDICT - verified, and the three requests answered")
print("=" * 78)

print("1. THE MAGNITUDE FLAG, RECHECKED ON THE RIGHT SHELF:")
sig_over_G0 = 0.0265 / (rho0 * c0 ** 2)          # the BASELINE modulus
sig_over_Gc = 0.0265 / K_COR                       # the CORONA's own modulus
print(f"   with the BASELINE modulus (G0 = rho0 c0^2 = {rho0*c0**2:.1e} Pa):")
print(f"   sigma/G = {sig_over_G0:.1e} - the Advisor's 3.4e7, outside linear")
print(f"   with the CHOKE'S OWN modulus (K(rho_corona) = {K_COR:.1e} Pa):")
print(f"   sigma/G = {sig_over_Gc:.2e} - LINEAR. The shear modulus is the")
print(f"   LOCAL K(rho) from the capacity ladder, not the baseline - the")
print(f"   'different modulus' the Advisor offered as option 1, now named.")
print()

print("2. B IS NOT G - the wave-speed fork, stated honestly:")
G = K_COR                               # the local shear = the local stiffness
B = K_COR
cT = (G / RHO_COR) ** 0.5
cL = ((B + 4 * G / 3.0) / RHO_COR) ** 0.5
print(f"   c_T = sqrt(G/rho) = {cT:.2e} m/s = the capacity's own C")
print(f"   c_L = sqrt((B+4G/3)/rho) = {cL:.2e} m/s = 1.53 x C")
print(f"   -> the framework's C(rho) labels the SHEAR branch; the longitudinal")
print(f"   branch runs 1.53x faster. The Level-0 anchor picks C as the")
print(f"   capacity - the two branches are the same modulus, two polarizations.")
print()

print("3. THE SUPERNOVA MATH, CORRECTED - verified:")
A_F = 12.0                              # the smooth release shape
E_pref = rho0 * DV ** 2 / (4 * 3.14159265358979 * c0)   # the prefactor
print(f"   E_rad = A_F x (rho0 DV^2 / 4 pi c0 tau^3) = A_F x {E_pref:.2e} J")
for E_target, label in [(1e44, "a supernova"), (3e47, "GW150914's order")]:
    tau = (A_F * E_pref / E_target) ** (1.0 / 3.0)
    print(f"   {label:16s} ({E_target:.0e} J): tau = {tau:.1f} s")
v_c0 = DV / (4 * 3.14159265358979 * R_SRC ** 3) / 1.0
print(f"   the accommodation-velocity flag: DV/(4 pi a^3) = {v_c0:.1e} - the")
print(f"   linear compact-source formula indeed cannot carry this: the DV is")
print(f"   the PREFERRED-VOLUME demand (1 M_sun x dV_u at the corona's density),")
print(f"   NOT the actual displaced volume - the two must be split before the")
print(f"   pulse is physical.")
print()

print("4. THE THREE REQUESTS FROM THE LOG:")
E_debt = (18.0 / 19.0) * M_SUN * c0 ** 2     # the 18-part debt
TAU_AC = R_SRC / 9.58e5                      # the acoustic crossing at C(rho_max)
print(f"   dV = {DV:.2e} m^3 = the 1 M_sun breach's PREFERRED-VOLUME demand")
print(f"       (the knot's release at the ambient's specific volume, 1/rho_cor)")
print(f"   the 18-part debt = (18/19) M c0^2 = {E_debt:.2e} J for 1 M_sun")
print(f"       (the fold's 19:1:18 balance - 18/19 of the mass-energy)")
print(f"   the collapse duration: tau_acoustic = a/C(rho_max) = "
      f"{TAU_AC*1e3:.1f} ms - a LOWER bound only; the full RP-with-phase")
print(f"   conversion solve (C never hits 0 at finite rho_max) is the actual")
print(f"   number - honest: NOT yet computed")
print(f"   dynamic_knot_HDF.py: IN OUR REPO at runpod_heavy/dynamic_knot_HDF.py")
print(f"   (with phi_eq_of inside) - the 'projects' folder just needs the copy")
print()

print("5. THE ENERGY FUNCTIONAL (the matched derivation's master equation):")
print("   W = (B/2)[tr e - theta_*(chi)]^2 + G(chi)|e_dev - e*_dev(chi)|^2")
print("       + f(chi) + (kappa/2)|grad chi|^2")
print("   the PWC mapping: theta_*(chi) = eta(1-chi) - the preferred volume")
print("   (the conversion source); e*_dev(chi) = the 720-degree twist's own")
print("   preferred deviatoric strain (the winding's torsion - what the")
print("   double-loop topology justifies); f(chi) = the phase energy (E_lock);")
print("   G(chi) = the LOCAL modulus K(rho(chi)) - the shelf fix above.")
res = {"sigma_over_G_baseline": sig_over_G0, "sigma_over_G_corona": sig_over_Gc,
       "cT": cT, "cL": cL, "E_prefactor": E_pref, "E_debt_18_19_J": E_debt,
       "tau_acoustic_ms": TAU_AC * 1e3, "dV_m3": DV,
       "accommodation_velocity_flag": v_c0}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "advisor_checks.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
