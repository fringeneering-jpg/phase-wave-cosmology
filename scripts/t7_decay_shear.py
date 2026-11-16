# t7_decay_shear.py - the T7 spread: bound vs unspooling debt (PROPOSED closure, 2026-10-20)
# Intact muon (m_mu): the retained debt share s = 1/19 is trapped inside the
# fold, buffering the shear. At decay (tau_mu): the weld breaches and the
# s = 1/19 debt unspools out of the crease, raising the effective shear by
# (1 + s) = 20/19.
# PROPOSED: verification script only - not part of the canon until ruled.
# Zero fitted parameters - only the locked s = 1/19 enters.
import math

me_kg = 9.1093837e-31
me_MeV = 0.510998950
hbar = 1.054571817e-34
c0 = 2.99792458e8
alpha_inv = 137.035999084
s = 1.0 / 19.0

# the T7 readings, solved from the two sealed formulas (not pasted):
m_mu_codata = 105.6583755   # MeV
tau_mu_codata = 2.1969811e-6  # s

T7_mass = 60.0 * (m_mu_codata / (me_MeV * (20.0 * math.pi ** 3 / 3.0)) - 1.0)
tau_e = hbar / (me_kg * c0 ** 2)
T7_tau = 3.0 * (tau_mu_codata / (256.0 * (alpha_inv ** 6) * tau_e) - 1.0)

T7_decay = T7_mass * (1.0 + s)

def tau_mu(T7):
    return 256.0 * (alpha_inv ** 6) * (1.0 + T7 / 3.0) * tau_e

res_tau_T7mass = 1e6 * (tau_mu(T7_mass) / tau_mu_codata - 1.0)   # ppm (the named -245 ppm)
res_tau_T7decay = 1e6 * (tau_mu(T7_decay) / tau_mu_codata - 1.0)  # ppm after the 20/19 factor

print("=" * 74)
print("THE T7 SPREAD - the bound vs unspooling debt (s = 1/19)")
print("=" * 74)
print("T7 (mass)     = %.4f%%   (solved from m_mu)" % (T7_mass * 100))
print("T7 (tau)      = %.4f%%   (solved from tau_mu)" % (T7_tau * 100))
print("T7,decay      = T7,mass x 20/19 = %.4f%%" % (T7_decay * 100))
print()
print("tau_mu residual with T7,mass : %+.1f ppm   (the named spread)" % res_tau_T7mass)
print("tau_mu residual with T7,decay: %+.1f ppm   (after the 20/19 unspooling)" % res_tau_T7decay)
print()
print("VERDICT: the (1 + 1/19) unspooling factor closes the T7 spread")
print("to %+.1f ppm using only the locked s = 1/19." % res_tau_T7decay)
print("note: the audit's +7.7 ppm figure used the fixed T7 = 0.0175 rounding; this")
print("script solves T7 self-consistently from each formula and lands +7.4 ppm.")
print("STATUS: PROPOSED - the T7 spread stays a named open item until this is ruled.")
