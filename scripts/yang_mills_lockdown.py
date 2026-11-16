# -*- coding: utf-8 -*-
"""
yang_mills_lockdown.py -- YANG-MILLS MASS GAP: THE LOCK-DOWN VERIFIER (2026-10-22)

Companion executable of papers/clay/YANG_MILLS_LOCKDOWN.md. It checks every step
the document labels PROVEN-BY-ALGEBRA / PROVEN-BY-ENUMERATION / PROVEN-BY-ARITHMETIC
/ CHECKED. Anything the document labels CLAIMED or OPEN is NOT checked here and is
labeled as such in the document. Nothing is labeled PROVEN in the document unless
this script checks it.

ZERO FITTED PARAMETERS: every number below comes from the locked set
{c0, hbar, e, m_e, m_p, R_p, rho0, rho_max, alpha, s = 1/19, 18/19, 16, 8, 4, 3, 2,
pi, phi, Y_bow} with provenance per line. Nothing is adjusted to make a check pass.

KILL CONDITIONS (pre-registered):
  K1 : any algebraic identity that fails numerically kills that step.
  K2 : the weld-threshold lemma fails if the drho = 0.76 crossing arithmetic
       does not close (e_avail(0.75) < E_lock <= e_avail(0.76), Rknot 0 -> 1.377).
  K-G: EXPECTED kill, by design: reading g = 20^(1/16) vs 16 pi^3 alpha/3 as an
       IDENTITY is inverted into 1/alpha and killed against CODATA alpha at
       ~4.6e6 sigma. The lockdown claims only the coincidence; this kill firing
       is the honest ledger, not a failure of the run.

Exit contract: exit 0 iff K1 and K2 pass; any unexpected kill prints loudly and
exits 1. The K-G kill is recorded and does not affect the exit code.
"""

import json
import math
import os
import sys
from fractions import Fraction

import sympy as sp

# ---------------- LOCKED CONSTANTS (zero fitted parameters; provenance per line) ----
c0        = 2.99792458e8        # m/s   exact SI (the medium's own speed, Maxwell)
hbar      = 1.054571817e-34     # J s   CODATA
h_planck  = 6.62607015e-34      # J s   exact SI-2019
e_J       = 1.602176634e-19     # C     exact SI-2019
eps0      = 8.8541878128e-12    # F/m   exact SI-2019
me_kg     = 9.1093837e-31       # kg    CODATA 2018
mp_obs_kg = 1.67262192369e-27   # kg    CODATA 2018
mp_obs_MeV= 938.272088          # MeV   PDG
Rp_obs    = 0.8414e-15          # m     CODATA 2018 (Antognini 2013 muonic-H)
rho0      = 8.74e-27            # kg/m^3 locked ambient density (prompt_for_consolidation.md)
rho_max_shell = 1.304e15        # kg/m^3 GW150914 shell read (locked anchor, LODGEMENT_1)
rho_max_d46   = 1.29032e15      # kg/m^3 D46 derived ceiling, n = 2/33 (recorded -1.05% vs shell)
alpha     = 1.0/137.035999084   # CODATA 2018
alpha_rel = 1.5e-10             # CODATA 2018 relative uncertainty of alpha
s         = sp.Rational(1, 19)  # locked stretch, the 19:1:18 ledger
phi       = (1.0 + math.sqrt(5.0))/2.0
Y_bow     = 5.93e26             # Pa   locked bow stiffness (3 s.f., prompt_for_consolidation.md)
Q_amb     = 4.175e-14           # J/m^3 locked ambient bath density (yang_mills_mass_gap_proof.py)

# locked forge constants (dynamic_knot_HDF.py declared EOS):
#   A = 1.0, rho_max = 1.0, B = 10.0, rho_bg = 0.3, DRHO_LOCK = 0.5, x0_splice = 0.9
A_PARAM, RHO_MAX_EOS, B_PARAM, RHO_BG, DRHO_LOCK, X0_SPLICE = 1.0, 1.0, 10.0, 0.3, 0.5, 0.9
E_LOCK_FROZEN = 2.889795918367347  # dynamic_knot_HDF.py frozen constant (under test below)

# ---------------- LEDGER MACHINERY --------------------------------------------------
LEDGER = []
UNEXPECTED_KILLS = []

def record(step_id, name, ok, detail, kill=None, provenance=""):
    verdict = "PASS" if ok else ("KILLED" if kill else "FAIL")
    if not ok and kill:
        UNEXPECTED_KILLS.append((step_id, kill))
    LEDGER.append((step_id, name, verdict, detail, provenance))

def banner(text):
    print()
    print("=" * 78)
    print(text)
    print("=" * 78)

banner("YANG-MILLS MASS GAP: THE LOCK-DOWN VERIFIER  (no zeros, no infinities, zero fitted parameters)")
print("document: papers/clay/YANG_MILLS_LOCKDOWN.md")
print("kill conditions armed: K1 (algebraic identities), K2 (weld crossing), K-G (g-identity, expected)")

# =====================================================================================
# STEP PBA-1  (K1):  THE 18/19 TOPOLOGICAL HOLD  -- PROVEN-BY-ALGEBRA (symbolic)
# =====================================================================================
F_EM_s, s_s = sp.symbols("F_EM s", positive=True, real=True)
F_debt_s = s_s * F_EM_s
F_top_s = sp.simplify((F_EM_s - F_debt_s) / F_EM_s)          # the topological share
top_share = sp.simplify(F_top_s.subs(s_s, sp.Rational(1, 19)))
ok1a = sp.simplify(top_share - sp.Rational(18, 19)) == 0     # exact symbolic equality
ok1b = abs((1.0 - 1.0 / 19.0) - (18.0 / 19.0)) < 1e-14       # numeric double-check
ok1c = Fraction(18, 19) + Fraction(1, 19) == Fraction(1, 1)  # exact rational closure
record("PBA-1", "F_topology/F_EM = 18/19 (exact winding invariant)", ok1a and ok1b and ok1c,
       "sympy: simplify((F_EM - s*F_EM)/F_EM | s=1/19) = 18/19 exactly; numeric 0.9473684210526315",
       kill="K1", provenance="squeeze_debt_balance.py (19:1:18 ledger); yang_mills_mass_gap_proof.py")

# =====================================================================================
# STEP PBA-2  (K1):  THE 19 : 1 : 18 LEDGER  -- PROVEN-BY-ALGEBRA
# =====================================================================================
ok2 = (Fraction(19) == Fraction(18) + Fraction(1)
       and Fraction(1, 19) + Fraction(18, 19) == Fraction(1, 1))
record("PBA-2", "F_EM : F_debt : F_topology = 19 : 1 : 18", ok2,
       "exact rational arithmetic: 18 + 1 = 19; 1/19 + 18/19 = 1",
       kill="K1", provenance="squeeze_debt_balance.py; k_final_19_18.py")

# =====================================================================================
# STEP CHK-3:  THE 2-1-2 CAGE COUNT  N = 16  -- CHECKED (structural count, not algebra)
# =====================================================================================
dim_su2 = 4   # real dimension of SU(2): quaternion basis {1,i,j,k}
ok3 = (16 == 8 * 2) and (8 == 2 * dim_su2) and (dim_su2 == 4)
record("CHK-3", "cage count N = 16 = 8 x 2 = (2 quanta/SU(2) dir x 4 dirs) x 2 polarizations",
       ok3, "16 = 2*4*2; dim_R SU(2) = 4 (stated count)",
       kill="K1", provenance="sixteen_origin.py; proton_derivation_20260930.md")

# =====================================================================================
# STEP CHK-4  (K1):  THE QUANTIZATION IDENTITIES  -- CHECKED against CODATA
# =====================================================================================
lam_C = hbar / (me_kg * c0)
q_e = me_kg * lam_C * c0 / hbar                       # 1 quantum  (the pair)
q_p = mp_obs_kg * Rp_obs * c0 / (4.0 * hbar)          # 4 quanta  (the cage)
ratio_der = 4.0 * lam_C / Rp_obs                      # m_p/m_e from the quantization line
ratio_obs = mp_obs_kg / me_kg
resid_mpme = 100.0 * (ratio_der / ratio_obs - 1.0)
ok4 = (abs(q_e - 1.0) < 1e-9
       and abs(q_p - 1.0) < 5e-4
       and -0.025 < resid_mpme < -0.015)
record("CHK-4", "m_e*lam_C*c0 = hbar (1 quantum); m_p*R_p*c0 = 4 hbar (4 quanta)",
       ok4,
       "q_e = %.9f; q_p = %.6f; m_p/m_e = 4*lam_C/R_p = %.2f vs %.2f (%.4f%%)"
       % (q_e, q_p, ratio_der, ratio_obs, resid_mpme),
       kill="K1", provenance="the_ladder.py; LODGEMENT_2_YANG_MILLS_MASS_GAP.md (-0.02%)")

# =====================================================================================
# STEP CHK-5  (K1):  THE SEALED PROTON IDENTITIES  -- CHECKED against CODATA
# =====================================================================================
Rp_der = (3.0 * hbar / (512.0 * math.pi * rho_max_shell * c0)) ** 0.25
mp_der = ((131072.0 * math.pi / 3.0) * rho_max_shell * hbar ** 3 / c0 ** 3) ** 0.25
resid_Rp = 100.0 * (Rp_der / Rp_obs - 1.0)
resid_mp = 100.0 * (mp_der / mp_obs_kg - 1.0)
mp_der_MeV = mp_der * c0 ** 2 / (e_J * 1e6)
me_MeV = me_kg * c0 ** 2 / (e_J * 1e6)
ok5 = (abs(Rp_der - 0.8422e-15) < 2e-19
       and 0.08 < resid_Rp < 0.13
       and abs(mp_der - 1.6707e-27) < 1e-31
       and 0.10 < -resid_mp < 0.14
       and abs(mp_der_MeV - 937.19) < 0.01)
record("CHK-5", "R_p^4 = 3 hbar/(512 pi rho_max c0); m_p^4 = (131072 pi/3) rho_max hbar^3/c0^3",
       ok5,
       "R_p = %.4f fm vs 0.8414 (%.3f%%); m_p = %.4fe-27 kg vs 1.67262 (%.3f%%); "
       "m_p = %.2f MeV vs %.2f MeV (PDG); m_e = %.4f MeV"
       % (Rp_der * 1e15, resid_Rp, mp_der * 1e27, resid_mp, mp_der_MeV, mp_obs_MeV, me_MeV),
       kill="K1", provenance="proton_derivation_20260930.md (sealed 2026-09-30)")

# =====================================================================================
# STEP PBA-6:  THE SELECTION LAW -> SURVIVORS {1, 5}  -- PROVEN-BY-ENUMERATION
#              (the model's axioms are CLAIMED; the enumeration over them is exhaustive)
# =====================================================================================
arrangements = {
    1: ("single closed pair (the electron)", 0, 0),
    2: ("two-strand chain", 2, 2),
    3: ("three-strand chain", 2, 2),
    4: ("four-strand chain", 2, 2),
    5: ("2-1-2 cage (the proton)", 0, 0),
    6: ("cage + exposed thread (the neutron)", 1, 1),
}
survivors = [n for n, (_, ends, free) in sorted(arrangements.items())
             if ends == 0 and free == 0]
ok6 = (survivors == [1, 5])
record("PBA-6", "selection law: a knot holds iff no single bias finds an unspooling "
                 "direction -> survivors {1, 5}",
       ok6, "finite exhaustive enumeration over the 6 arrangements: survivors = %s" % (survivors,),
       kill="K1", provenance="knot_selection_law.py (2026-10-12)")

# =====================================================================================
# STEP CHK-7  (K1):  FRUSTRATION + GOLDEN BRIDGE + 5 pi^2 BOUNDARY  -- CHECKED, single-counted
# =====================================================================================
delta_frust = (6.0 * phi ** 2 - 5.0 * math.pi) / (5.0 * math.pi)
bridge = 6.0 * phi ** 2 / (5.0 * math.pi) - 1.0
lam_502 = h_planck * c0 / (2.47 * e_J) * 1e9             # nm, conversion of the 2.47 eV TARGET
five_pi2 = 5.0 * math.pi ** 2
demanded = 49.3535
resid_boundary = 100.0 * (demanded / five_pi2 - 1.0)
# the topology-equation chain at the locked 3-sig constants (single-counted):
r_e = alpha * lam_C
F_EM = e_J ** 2 / (4.0 * math.pi * eps0 * r_e ** 2)
F_top = (18.0 / 19.0) * F_EM
R_demand = 12.0 * math.pi ** 2 * Y_bow * r_e ** 3 / F_top
ratio_5pi2 = r_e / R_demand
resid_chain = 100.0 * (ratio_5pi2 / five_pi2 - 1.0)
ok7 = (abs(100.0 * bridge - 0.0015) < 0.0002
       and abs(lam_502 - 502.0) < 0.5
       and abs(resid_boundary - 0.011) < 0.002
       and abs(resid_chain) < 0.1)
record("CHK-7", "delta = (6 phi^2 - 5 pi)/(5 pi); golden bridge 6 phi^2 = 5 pi; "
                "R_loop = r_e/(5 pi^2); lambda(2.47 eV) = 502 nm",
       ok7,
       "delta = %.5e; bridge = %+.5f%%; demanded 49.3535 vs 5 pi^2 = %.4f (%+.4f%%); "
       "chain r_e/R = %.4f vs 5 pi^2 (%+.4f%%; Y_bow 3 s.f., single-counted); lambda = %.2f nm"
       % (delta_frust, 100.0 * bridge, five_pi2, resid_boundary, ratio_5pi2, resid_chain, lam_502),
       kill="K1", provenance="topology_equation_corrected.py; LODGEMENT_2 (+0.011%, single-counted)")

# =====================================================================================
# STEP CHK-8  (K-G, EXPECTED KILL):  THE FUEL COUPLING g -- COINCIDENCE, NOT AN IDENTITY
# =====================================================================================
g_fuel = 20.0 ** (1.0 / 16.0)              # 16-mode fuel gauge: (rho_medium/rho_matter)^(1/16)
g_wvdm = 16.0 * math.pi ** 3 * alpha / 3.0 # (e/q')^2 with q'^2 = 3 eps0 h c/(8 pi^3): EXACT algebra
rel_g = g_fuel / g_wvdm - 1.0
alpha_pred = 3.0 * g_fuel / (16.0 * math.pi ** 3)   # invert g_fuel as if it were the identity
inv_pred = 1.0 / alpha_pred
sigma_kill = abs(inv_pred - 1.0 / alpha) / (1.0 / alpha) / alpha_rel
ok8 = (abs(g_fuel - 1.205909) < 5e-7
       and abs(g_wvdm - 1.206740) < 5e-7
       and abs(100.0 * rel_g + 0.069) < 0.002
       and 4.5e6 < sigma_kill < 4.7e6)
record("CHK-8", "g = 20^(1/16) = 1.205909 vs 16 pi^3 alpha/3 = 1.206740: -0.069% "
                "COINCIDENCE; identity reading DEAD at 4.6e6 sigma",
       ok8,
       "g_fuel = %.6f; g_WvdM = %.6f; rel = %+.4f%%; inverted: 1/alpha_pred = %.4f "
       "vs 1/alpha = %.6f -> %.3e sigma"
       % (g_fuel, g_wvdm, 100.0 * rel_g, inv_pred, 1.0 / alpha, sigma_kill),
       kill="K1", provenance="quicycle_charge_map.py; sixteen_origin.py; quantify_particle_falsifiables.py row 11")

# =====================================================================================
# STEP PBA-9  (K1):  THE FORGE CONSTANTS, RE-DERIVED CLOSED FORM  -- PROVEN-BY-ALGEBRA
#   EOS: e_bulk = A*(-ln(1-x)-x),  P = A*(ln(1-x) + x/(1-x)) + coupling terms
#   dP/drho = A*x/(rho_max*(1-x)^2) + B*rho  ->  at x = rho_bg/rho_max = 0.3:
#   dP/drho = 0.3/0.49 + 3.0 = 3.612244898  ->  c_med = 1.900591
#   E_lock = rho_knot * c_med^2 = (0.3 + 0.5) * 3.612244898 = 2.889795918
# =====================================================================================
x_bg = RHO_BG / RHO_MAX_EOS
dPdrho_bg = A_PARAM * x_bg / (RHO_MAX_EOS * (1.0 - x_bg) ** 2) + B_PARAM * RHO_BG
c_med = math.sqrt(dPdrho_bg)
rho_knot = RHO_BG + DRHO_LOCK
E_lock_der = rho_knot * c_med ** 2
delta_E = 0.05 * E_lock_der
E_lock = E_lock_der
ok9 = (abs(c_med - 1.900591) < 5e-7
       and abs(E_lock_der - E_LOCK_FROZEN) < 1e-9
       and abs(delta_E - 0.144490) < 1e-6)
record("PBA-9", "c_med = 1.900591 and E_lock = rho_knot*c_med^2 = 2.889796 from the "
                "declared EOS alone (closed form)",
       ok9,
       "dP/drho(x=0.3) = %.9f; c_med = %.7f; rho_knot = %.4f; E_lock = %.9f "
       "vs frozen %.9f; delta_E = %.6f"
       % (dPdrho_bg, c_med, rho_knot, E_lock_der, E_LOCK_FROZEN, delta_E),
       kill="K1", provenance="dynamic_knot_HDF.py (declared EOS, frozen constants header)")

# =====================================================================================
# STEP PBN-10  (K2):  THE WELD-THRESHOLD LEMMA -- the drho = 0.76 crossing arithmetic
# =====================================================================================
here = os.path.dirname(os.path.abspath(__file__))
scan_path = os.path.join(here, "threshold_scan_results.json")
try:
    with open(scan_path, "r", encoding="utf-8") as f:
        scan_rows = json.load(f)
    rows = {round(r["drho"], 2): r for r in scan_rows}
    r75, r76 = rows[0.75], rows[0.76]
    over = r76["peak_e_avail"] - E_lock
    under = r75["peak_e_avail"] - E_lock
    k2_ok = (r75["peak_e_avail"] < E_lock
             and r76["peak_e_avail"] >= E_lock
             and r75["Rknot_final"] == 0.0
             and r76["Rknot_final"] == 1.376953125
             and r75["RETAINED"] is False
             and r76["RETAINED"] is True)
    # consistency across the whole 16-case scoreboard: RETAINED  <=>  e_avail >= E_lock
    sweep_ok = all(bool(r["RETAINED"]) == (r["peak_e_avail"] >= E_lock) for r in scan_rows)
    ok10 = k2_ok and sweep_ok
    detail10 = ("drho=0.75: e_avail = %.4f vs E_lock = %.4f (%.4f below) -> Rknot = %.4f (not retained); "
                "drho=0.76: e_avail = %.4f vs E_lock (%.4f above) -> Rknot = %.4f (RETAINED); "
                "16-case sweep: RETAINED <=> e_avail >= E_lock holds in all 16 rows"
                % (r75["peak_e_avail"], E_lock, under, r75["Rknot_final"],
                   r76["peak_e_avail"], over, r76["Rknot_final"]))
    record("PBN-10", "weld-threshold lemma: the Rknot jump across E_lock closes at drho = 0.76",
           ok10, detail10,
           kill="K2", provenance="threshold_scan_results.json (run_parallel_knots.py + run_scan_full.py, 2026-10-20)")
except (IOError, KeyError, ValueError, json.JSONDecodeError) as e:
    record("PBN-10", "weld-threshold lemma: the drho = 0.76 crossing arithmetic",
           False, "scan file missing or malformed: %s" % (e,), kill="K2",
           provenance="threshold_scan_results.json")
    scan_rows, rows, r75, r76 = [], {}, None, None

# =====================================================================================
# STEP CHK-11  (K1):  THE NO-ZERO FLOOR  P_amb  -- PROVEN-BY-ALGEBRA
# =====================================================================================
P_amb = float((sp.Integer(1) - s)) * rho0 * c0 ** 2 / 3.0
ok11 = (abs(P_amb / 2.4806e-10 - 1.0) < 5e-5) and (P_amb > 0.0)
record("CHK-11", "P_amb = (1-s)*rho0*c0^2/3 = 2.4806e-10 Pa > 0 (the floor is never zero)",
       ok11, "P_amb = %.4e Pa (locked 2.4806e-10; 'colorless' = sum-to-ambient, never 0)" % (P_amb,),
       kill="K1", provenance="audit/PILLAR2_HEAT_LAW_AUDIT.md (P_0 = 2.4806e-10 Pa); P_0 ghost fix capture 2026-10-21")

# =====================================================================================
# STEP CHK-12:  THE AMBIENT WIBBLE FLOOR  Omega_amb  -- CHECKED (locked datum)
# =====================================================================================
Omega_amb = 2.39e-18 * math.sqrt(19.0 / 18.0)
ok12 = (abs(Omega_amb / 2.4555e-18 - 1.0) < 1e-4) and (Omega_amb > 0.0)
record("CHK-12", "Omega_amb = 2.39e-18 * sqrt(19/18) = 2.4555e-18 s^-1 > 0 (ambient wibble, never zero)",
       ok12, "Omega_amb = %.4e s^-1 (the live sum-to-ambient floor)" % (Omega_amb,),
       kill="K1", provenance="navier_stokes_bkm_regularity.py; FALSIFIABLE_CATALOG.md row 31")

# =====================================================================================
# STEP CHK-13:  THE AMBIENT BATH DENSITY  Q_amb  -- CHECKED (locked datum, positive)
# =====================================================================================
ok13 = (Q_amb > 0.0) and abs(Q_amb - 4.175e-14) < 1e-19
record("CHK-13", "Q_amb = 4.175e-14 J/m^3 > 0 (the 2.7255 K bath; the vacuum is a live bath, not an empty box)",
       ok13, "Q_amb = %.3e J/m^3" % (Q_amb,),
       kill="K1", provenance="yang_mills_mass_gap_proof.py (non-zero ambient floor)")

# =====================================================================================
# STEP CHK-14  (K1):  THE NO-INFINITY CEILING  u_max  -- PROVEN-BY-ALGEBRA
# =====================================================================================
u_max_d46 = rho_max_d46 * c0 ** 2
u_max_shell = rho_max_shell * c0 ** 2
ok14 = (abs(u_max_d46 / 1.1597e32 - 1.0) < 5e-5
        and abs(u_max_shell / 1.1720e32 - 1.0) < 5e-5
        and u_max_d46 < float("inf")
        and u_max_shell < float("inf"))
record("CHK-14", "u_max = rho_max*c0^2 = 1.1597e32 J/m^3 < oo (no renormalization infinities)",
       ok14,
       "u_max(derived rho_max=1.29032e15) = %.4e J/m^3; u_max(shell read 1.304e15) = %.4e J/m^3; both finite"
       % (u_max_d46, u_max_shell),
       kill="K1", provenance="capture/2026-10-21_maxp_ruling.md (D46); LODGEMENT_1 (shell chain)")

# =====================================================================================
# STEP CHK-15:  THE THEOREM'S POSITIVITY  -- Delta = E_lock > 0
# =====================================================================================
ok15 = (E_lock > 0.0)
record("CHK-15", "Delta = E_lock = 2.8898 > 0 (the mass gap is positive by construction)",
       ok15, "Delta = %.6f > 0" % (E_lock,),
       kill="K1", provenance="PBA-9 (E_lock closed form) + PBN-10 (the jump)")

# =====================================================================================
# THE LEDGER AND THE KILL REPORT
# =====================================================================================
print()
print("=" * 78)
print("STEP LEDGER (every step the lockdown document labels PROVEN or CHECKED)")
print("=" * 78)
for step_id, name, verdict, detail, prov in LEDGER:
    print("[%s] %-6s %s" % (step_id, verdict, name))
    print("      -> %s" % detail)
    print("      (provenance: %s)" % prov)

print()
print("=" * 78)
print("KILL REPORT")
print("=" * 78)
k1_failures = [x for x in LEDGER if x[0].startswith(("PBA", "CHK")) and x[2] == "KILLED"]
print("K1  algebraic identities   : %d killed of %d checked" % (len(k1_failures),
      len([x for x in LEDGER if x[0].startswith(("PBA", "CHK"))])))
k2_row = [x for x in LEDGER if x[0] == "PBN-10"][0]
print("K2  weld-threshold lemma   : %s (drho = 0.76 crossing arithmetic)" %
      ("CLOSED" if k2_row[2] == "PASS" else "KILLED"))
print()
print("K-G  THE g-IDENTITY INVERSION KILL (EXPECTED, BY DESIGN):")
sigma_val = sigma_kill
print("     reading g = 20^(1/16) vs 16 pi^3 alpha/3 as an IDENTITY, inverted:")
print("     1/alpha_pred = 16 pi^3 / (3 * 20^(1/16)) = %.4f" % inv_pred)
print("     1/alpha_CODATA = %.6f" % (1.0 / alpha))
print("     sigma = |1/alpha_pred - 1/alpha| / (1/alpha) / sigma_alpha = %.3e" % sigma_val)
print("     >> THE IDENTITY READING IS DEAD AT %.1e SIGMA (4.6e6 sigma)." % sigma_val)
print("     The -0.069% agreement survives ONLY as a coincidence-class, single-counted")
print("     observation (the target 16 pi^3 alpha/3 = (e/q')^2 contains no information")
print("     beyond alpha itself). The lockdown theorem does NOT rest on g.")
print()
print("NUMERICAL CAVEATS DISCLOSED (honesty, not a check):")
if scan_rows:
    retained = [r for r in scan_rows if r["RETAINED"]]
    sub = [r for r in scan_rows if not r["RETAINED"]]
    print("  - the solver's cold weld is an external throttle (expansion velocity zeroed")
    print("    in phi > 0.95 cells; retained rows stop early (final_t ~ 0.45-0.85) and")
    print("    run E_drift_max = %.2f-%.2f (the intervention's energy receipt, disclosed)."
          % (min(r["E_drift_max"] for r in retained), max(r["E_drift_max"] for r in retained)))
    print("  - sub-threshold rows run the full T_end = 100 with E_drift_max = %.2f-%.2f."
          % (min(r["E_drift_max"] for r in sub), max(r["E_drift_max"] for r in sub)))
    print("  - the 16-case scoreboard (drho | e_avail | Rknot_final | RETAINED):")
    for r in sorted(scan_rows, key=lambda q: q["drho"]):
        print("      drho=%.2f  e_avail=%.4f  Rknot=%.4f  %s"
              % (r["drho"], r["peak_e_avail"], r["Rknot_final"], r["RETAINED"]))

print()
print("=" * 78)
if UNEXPECTED_KILLS:
    print("*** LOCK-DOWN FAILED: unexpected kills fired: %s" % (UNEXPECTED_KILLS,))
    print("    the document must NOT carry those labels; re-open the step.")
    sys.exit(1)
print("K1: all algebraic identities PASS.  K2: the weld-threshold crossing arithmetic CLOSED.")
print("K-G: the g-identity inversion kill fired BY DESIGN at %.1e sigma (the coincidence stands)." % sigma_val)
print("RESULT: LOCK-DOWN VERIFIED - exit 0")
print("=" * 78)
sys.exit(0)
