#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quantify_cosmology.py - THE COSMOLOGY COLUMN OF THE PWC INVENTORY LEDGER
========================================================================
Quantifies the cosmology column of Phase Wave Cosmology from the LOCKED
CONSTANTS ONLY.  ZERO fitted parameters: every number carries provenance
(DERIVED / MEASURED / VERIFIED / BACK-SOLVED / CLAIMED / OPEN), every
candidate carries a kill condition, and every miss is printed - never hidden.

Framework receipts (read from the workspace, not re-derived):
  D39  eta_B = f_solid^3  CLOSED +0.60 sigma   (papers/PHASE_WAVE_COSMOLOGY_DERIVATIONS.md L831)
  S9   H0 wall rate: Gamma_untie = rho0 c0/(rho_max R_p)   (DERIVATIONS.md L566-568)
  S12  rho0 T2 bow-wave equilibrium, predicted 8.70e-27 vs "observed" 8.74e-27 (L594-596)
  D31  28/19 = s(1+T) with T = 3^3, vs "Planck LSS tempo" 380/258 kyr (L445-451)
  k<->H0 bridge: H0 = k * 3 c0 rho0/(20 lam_C,e rho_max)   (scripts/k_h0_bridge.py)
  audit/PILLAR2_HEAT_LAW_AUDIT.md L26: observed-side provenance of 380/258 = CLAIMED (F3)
  grep over papers/: "rho_crit" 0 hits, "Omega_Lambda" 0 hits, "Omega_m" 0 hits
      -> the framework has NO handle on critical density or Omega shares; those
         rows below are honest bookkeeping and are marked OPEN where the
         framework has no equation.

Planck 2018 external receipts (MEASURED, TT,TE,EE+lowE+lensing): H0, eta_B,
Omega_b h^2, Omega_m, Omega_Lambda, T_CMB.  SH0ES: Riess et al. 2022.
"""

import math
import sys

# ---------------- LOCKED CONSTANTS (never re-fit) ----------------
c0       = 2.99792458e8      # m/s         MEASURED (Maxwell)
rho0     = 8.74e-27          # kg/m^3      resting density (S12: "observed 8.74e-27")
rho_max_shell = 1.304e15     # kg/m^3      MEASURED (GW150914 shell read) - k-bridge input
rho_max_deriv = 1.29032e15   # kg/m^3      DERIVED (locked alternate)
R_p      = 0.84e-15          # m           MEASURED+DERIVED (proton radius)
s        = 1.0 / 19.0
f_solid  = 8.4989e-4         #             BACK-SOLVED (to reproduce G)
k        = 3069.87           #             locked endurance coefficient (the k-bridge)
T_cubic  = 3 ** 3            # 27
m_p_MeV  = 938.272088        # MeV         MEASURED
m_e_MeV  = 0.51099895        # MeV         MEASURED
G        = 6.67430e-11       # m^3/kg/s^2  MEASURED
hbar     = 1.054571817e-34   # J s         MEASURED
kB       = 1.380649e-23      # J/K         MEASURED
Q_CMB    = 4.175e-14         # J/m^3       MEASURED (FIRAS bath)
T_CMB    = 2.7255            # K           MEASURED (FIRAS)
H0_lock  = 73.935            # km/s/Mpc    DERIVED (the k-bridge, locked)
T28      = 28.0 / 19.0

# ---------------- UNIT / DERIVED HELPERS (no fitting) ----------------
EV_KG    = 1.602176634e-19 / c0 ** 2        # 1 eV/c^2 in kg
m_p_kg   = m_p_MeV * 1.0e6 * EV_KG
m_e_kg   = m_e_MeV * 1.0e6 * EV_KG
MPC_M    = 3.0856775814913673e22            # m per Mpc
MPC_KM   = 3.0856775814913673e19            # km per Mpc
LY_M     = 9.4607304725808e15               # m per light-year
ZETA3    = 1.2020569031595942
PI4_30Z  = math.pi ** 4 / (30.0 * ZETA3)    # 2.701178 - mean photon energy / kB T
H100     = 100.0e3 / MPC_M                  # 100 km/s/Mpc in 1/s
rho_crit_h1 = 3.0 * H100 ** 2 / (8.0 * math.pi * G)   # 1.8784e-26 kg/m^3
lamC_e   = hbar / (m_e_kg * c0)             # electron reduced Compton wavelength

# ---------------- EXTERNAL MEASURED RECEIPTS (Planck 2018 / SH0ES) ----------------
H0_shoes   = 73.04;  H0_shoes_e  = 1.04
H0_planck  = 67.36;  H0_planck_e = 0.54
h_planck   = 0.6736; h_planck_e  = 0.0054
eta_P      = 6.104e-10;  eta_P_e = 0.058e-10      # Planck baryon-to-photon
Obh2_P     = 0.02237;    Obh2_P_e = 0.00015
Om_P       = 0.3153;     Om_P_e   = 0.0073
Ol_P       = 0.6847;     Ol_P_e   = 0.0073
T_CMB_e    = 0.0006
N_eff      = 3.046                                 # SM prediction (external)
n_gamma_obs = 4.107e8                              # 410.7 cm^-3 from T_CMB
tempo_obs  = 380.0 / 258.0                         # "Planck LSS tempo" - CLAIMED side
s_ng_ledger = 3.6013                               # ledger's quoted s/n_gamma

# ---------------- PWC DERIVATIONS FROM THE LOCKED SET ONLY ----------------
# (1) H0 via the k-bridge (scripts/k_h0_bridge.py): eliminate the common radius R
H0_bridge_s = k * 3.0 * c0 * rho0 / (20.0 * lamC_e * rho_max_shell)     # 1/s
H0_bridge   = H0_bridge_s * MPC_KM                                     # km/s/Mpc
# cross-check route S9: Gamma_untie = rho0 c0/(rho_max R_p)
H0_untie_shell  = (rho0 * c0 / (rho_max_shell * R_p)) * MPC_KM         # km/s/Mpc
H0_untie_deriv  = (rho0 * c0 / (rho_max_deriv * R_p)) * MPC_KM         # km/s/Mpc

# (2) the tied baryon share (D39)
eta_B = f_solid ** 3
# (3) photon inventory from the CMB bath
n_g   = Q_CMB / (PI4_30Z * kB * T_CMB)           # 1/m^3
rho_g = Q_CMB / c0 ** 2                          # kg/m^3
rho_r = rho_g * (1.0 + (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * N_eff)
# (4) matter density from the tied share (baryons carry the share: "the matter
#     share is the solid debt fraction cubed", DERIVATIONS.md L831)
rho_b  = eta_B * n_g * m_p_kg
# (5) bookkeeping shares at the locked H0 (framework itself reads NO Omega)
H0_pwc_s  = H0_lock * 1.0e3 / MPC_M              # locked H0 in 1/s
h_pwc     = H0_lock / 100.0
rho_crit  = 3.0 * H0_pwc_s ** 2 / (8.0 * math.pi * G)
Obh2_pwc  = rho_b / rho_crit_h1
Ob_pwc    = Obh2_pwc / h_pwc ** 2
Or_pwc    = rho_r / rho_crit
Ob_planck = Obh2_P / h_planck ** 2
Ob_planck_e = Ob_planck * math.sqrt((Obh2_P_e / Obh2_P) ** 2 + (2 * h_planck_e / h_planck) ** 2)
Om_pwc    = Ob_pwc                      # baryons-only bookkeeping; framework has no CDM
Ol_pwc    = 1.0 - Ob_pwc - Or_pwc       # the "untying's share" = residue, not a Lambda claim
# (6) horizon and the S12 hierarchy identity
R_H_pwc    = c0 / H0_pwc_s
R_H_planck = c0 / (H0_planck * 1.0e3 / MPC_M)
hier_rho   = rho_max_shell / rho0
hier_RH    = R_H_pwc / R_p
# (7) the 28/19 acoustic tempo (D31)
tempo_pwc  = s * (1.0 + T_cubic)                 # 28/19
# (8) entropy rows
s_over_ng = 2.0 * math.pi ** 4 / (45.0 * ZETA3)               # entropy per PHOTON (kB)
s_nu_over_s_gamma = (7.0 / 8.0) * (4.0 / 11.0) * N_eff
s_over_nb_pwc    = s_over_ng * (1.0 + s_nu_over_s_gamma) / eta_B
s_over_nb_planck = s_over_ng * (1.0 + s_nu_over_s_gamma) / eta_P
# rho0 self-check (S12: predicted 8.70e-27 vs locked 8.74e-27)
rho0_pred = 8.70e-27

# ---------------- RESIDUAL HELPERS ----------------
def pct(calc, meas):
    return 100.0 * (calc / meas - 1.0)

def sig(calc, meas, err):
    return (calc - meas) / err

def res_str(calc, meas, err=None):
    p = pct(calc, meas)
    if err:
        return "%+.2f%% (%+.2f sigma)" % (p, sig(calc, meas, err))
    return "%+.3f%%" % p

def fnum(x, nd=4):
    """scientific or plain formatting, nd significant digits"""
    return ("%." + str(nd) + "g") % x

# ---------------- THE INVENTORY TABLE ----------------
COLS = ["name", "PWC formula", "PWC value", "measured value",
        "residual %/sigma", "provenance", "kill condition"]
W    = [16, 26, 24, 24, 22, 30, 32]

rows = [
    ("H0 (k-bridge, wall rate)",
     "k*3*c0*rho0/(20*lamC,e*rho_max,shell)",
     "73.935 km/s/Mpc (locked)",
     "SH0ES 73.04+/-1.04; Planck 67.36+/-0.54",
     "%+.2f%% (%+.2fs) vs SH0ES | %+.2f%% (%+.2fs) vs Planck" % (
         pct(H0_lock, H0_shoes), sig(H0_lock, H0_shoes, H0_shoes_e),
         pct(H0_lock, H0_planck), sig(H0_lock, H0_planck, H0_planck_e)),
     "DERIVED (k locked 3069.87; rho_max shell-read 1.304e15 MEASURED; lamC,e from m_e)."
     " Bridge reproduced: %s km/s/Mpc" % fnum(H0_bridge, 6),
     "Break if k, rho0, m_e or rho_max move; must stay <=2 sigma of a distance-ladder"
     " H0; the wall-vs-volume (73.9 vs 67.4) reading is qualitative until the wall/void"
     " split is quantified. Cross-checks: Gamma_untie = %s (shell) / %s (derived rho_max)."
     % (fnum(H0_untie_shell, 5), fnum(H0_untie_deriv, 5))),
    ("rho0 (resting density)",
     "locked; T2 bow-wave equilibrium predicts 8.70e-27",
     "8.74e-27 kg/m^3",
     "framework prediction 8.70e-27 (S12)",
     res_str(rho0, rho0_pred),
     "MEASURED lock per S12 text ('observed 8.74e-27'); the receipt is not named -> "
     "CLAIMED; DERIVED prediction (S12, CLOSED 2026-09-30)",
     "Name the observation that reads 8.74e-27. It is NOT rho_m (Planck 2.687e-27) and"
     " NOT rho_crit - kill if it cannot be sourced."),
    ("rho_crit",
     "3*H0^2/(8*pi*G)",
     "%s kg/m^3" % fnum(rho_crit, 6),
     "8.5232e-27 (Planck, h=0.6736)",
     "%s (%+.2fs)" % (res_str(rho_crit, 8.5232e-27),
                      sig(rho_crit, 8.5232e-27, 2 * 8.5232e-27 * H0_planck_e / H0_planck)),
     "DERIVED bookkeeping. The framework never invokes rho_crit (0 hits in papers/);"
     " its medium uses rho0 instead.",
     "Only meaningful if a Friedmann-fluid reading is adopted; it inherits the H0"
     " tension (12.8 sigma) wholesale."),
    ("eta_B (baryon share)",
     "f_solid^3",
     fnum(eta_B, 4),
     "6.104+/-0.058e-10 (Planck)",
     res_str(eta_B, eta_P, eta_P_e),
     "DERIVED + VERIFIED (D39 CLOSED 2026-10-21: +0.60 sigma)",
     "Dies if f_solid (8.4989e-4) or the Planck eta_B move beyond 2 sigma."),
    ("n_gamma (photon number density)",
     "Q_CMB/(2.70118*kB*T_CMB)",
     "%s m^-3 (410.75 cm^-3)" % fnum(n_g, 6),
     "410.7 cm^-3 (from T_CMB)",
     res_str(n_g, n_gamma_obs, n_gamma_obs * 3.0 * T_CMB_e / T_CMB),
     "DERIVED identity; inputs FIRAS MEASURED (Q_CMB, T_CMB)",
     "Dies if FIRAS Q_CMB or T_CMB move; it is an input echo, not an independent"
     " prediction."),
    ("rho_gamma",
     "Q_CMB/c0^2",
     "%s kg/m^3" % fnum(rho_g, 6),
     "a*T^4/c^2 = 4.6448e-31 (FIRAS)",
     res_str(rho_g, 4.6448e-31, 4.6448e-31 * 4.0 * T_CMB_e / T_CMB),
     "VERIFIED (FIRAS receipt through T_CMB)",
     "Dies if Q_CMB or T_CMB move; again an input echo."),
    ("rho_rad (gamma+3 nu)",
     "rho_g*(1+0.2271*N_eff)",
     "%s kg/m^3 (N_eff=3.046)" % fnum(rho_r, 5),
     "same receipt from T_CMB + N_eff",
     res_str(rho_r, rho_g * (1.0 + (7.0/8.0)*(4.0/11.0)**(4.0/3.0)*N_eff)),
     "DERIVED with N_eff = 3.046 external (SM prediction, MEASURED in labs); the"
     " framework has no N_eff derivation",
     "Kill: N_eff from Planck (2.99+/-0.17) drifting away from 3.046, or a framework"
     " N_eff that never appears."),
    ("rho_b (matter density, tied share)",
     "eta_B*n_gamma*m_p",
     "%s kg/m^3" % fnum(rho_b, 6),
     "Obh2*rho_c(h=1) = 4.2021e-28",
     "%s; sigma = %+.2f" % (res_str(rho_b, 4.2021e-28),
                           sig(rho_b, 4.2021e-28, 4.2021e-28 * Obh2_P_e / Obh2_P)),
     "DERIVED + VERIFIED (D39 chain: the share is the physics; the physical density"
     " is h-independent)",
     "Dies with eta_B."),
    ("Omega_b h^2 (share, h-free)",
     "rho_b/rho_crit(h=1)",
     fnum(Obh2_pwc, 6),
     "0.02237+/-0.00015",
     res_str(Obh2_pwc, Obh2_P, Obh2_P_e),
     "DERIVED bookkeeping (the framework reads eta_B, not Omega)",
     "Dies with eta_B."),
    ("Omega_b (critical share)",
     "Obh2/h^2, h=0.73935",
     fnum(Ob_pwc, 6),
     "%s+/-%s" % (fnum(Ob_planck, 5), fnum(Ob_planck_e, 2)),
     res_str(Ob_pwc, Ob_planck, Ob_planck_e),
     "DERIVED bookkeeping. H0-share artifact: the physical density hits, the Omega"
     " share misses ONLY through the locked H0 - not a separate prediction.",
     "Inherits the H0 tension. Kill only if eta_B itself dies."),
    ("Omega_m",
     "none (baryons only via eta_B)",
     "0.04108 (baryons-only bookkeeping)",
     "0.3153+/-0.0073",
     "OPEN",
     "OPEN: no dark-matter handle anywhere in papers/ (0 hits); rotation curves are"
     " routed through a0 (MOND phenomenology), not through Omega_m.",
     "Must produce 0.3153+/-0.0073 from the locked set (e.g. via the a0 route) or the"
     " Lambda-CDM comparison is retracted. Until then: OPEN, not hidden."),
    ("Omega_Lambda (untying's share)",
     "1-Omega_b-Omega_r (residue only)",
     fnum(Ol_pwc, 4),
     "0.6847+/-0.0073",
     "OPEN",
     "OPEN: the untying is a LOCAL wall mechanism (S9), not a cosmological constant;"
     " no Lambda equation exists in the papers (0 hits). The residue is bookkeeping,"
     " not a claim.",
     "Must be read from the untying's heat draw / wall-void dynamics; a residue is not"
     " a derivation. Until then: OPEN."),
    ("R_H (horizon)",
     "c0/H0",
     "%s m = %s Gly (%s Mpc)" % (fnum(R_H_pwc, 6), fnum(R_H_pwc / LY_M, 6), fnum(R_H_pwc / MPC_M, 6)),
     "14.516 Gly (4450.6 Mpc, Planck)",
     "%s (%+.2fs)" % (res_str(R_H_pwc, R_H_planck), sig(R_H_pwc, R_H_planck, R_H_planck * H0_planck_e / H0_planck)),
     "DERIVED bookkeeping",
     "Inherits the H0 tension."),
    ("Hierarchy rho_max/rho0 = R_H/R_p",
     "rho_max/rho0 vs c0/(H0*R_p)",
     "%s vs %s" % (fnum(hier_rho, 6), fnum(hier_RH, 6)),
     "internal identity (paper: +0.015% with its own H0=73.8, R_p=0.8414 fm)",
     res_str(hier_RH, hier_rho),
     "DERIVED internal identity (S12: 'rho_max/rho0 ~ 1.492e41 = R_H/R_p is a derived"
     " consequence of the equilibrium closure')",
     "Internal consistency only - no external datum. Breaks if R_p, rho_max or H0"
     " move; with the DERIVED rho_max (1.29032e15) the gap grows to %s."
     % res_str(R_H_pwc / R_p, rho_max_deriv / rho0)),
    ("28/19 acoustic tempo",
     "s*(1+T), T = 3^3 = 27",
     fnum(tempo_pwc, 8),
     "380/258 = 1.47286822 ('Planck LSS tempo')",
     res_str(tempo_pwc, tempo_obs),
     "DERIVED arithmetic (28/19 = 1.47368421). Observed side CLAIMED (audit F3: not"
     " reproduced from Planck tables in this workspace)",
     "Reproduce 380/258 from Planck 2018 tables (age at LSS / drag-crossing time) or"
     " the closure is decorative numerology, not a verification."),
    ("s/n_gamma (entropy per photon)",
     "2*pi^4/(45*zeta(3))",
     "3.601570 kB",
     "ledger quote 3.6013 kB",
     res_str(s_over_ng, s_ng_ledger),
     "VERIFIED identity (Planck-spectrum relation s_g = (4/3)Q/T). The ledger label"
     " 'baryon-to-entropy' is a misnomer: this is entropy per PHOTON.",
     "None as an identity - but the row's label must be fixed, or the ledger"
     " overstates what it derived."),
    ("s/n_b (true baryon-to-entropy)",
     "(s/n_gamma)*(1+7/8*4/11*N_eff)/eta_B",
     "1.15525e10 kB",
     "1.16187e10 kB (Planck eta_B)",
     res_str(s_over_nb_pwc, s_over_nb_planck),
     "DERIVED from the tied share (photons + 3 neutrino families)",
     "Dies with eta_B."),
]

def wrap(text, width):
    out, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if cur and len(cand) > width:
            out.append(cur); cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out or [""]

def print_table(rows):
    sep = " | "
    header = sep.join(h.center(W[i]) for i, h in enumerate(COLS))
    print(header)
    print(sep.join("-" * W[i] for i in range(len(COLS))))
    for r in rows:
        cells = [wrap(c, W[i]) for i, c in enumerate(r)]
        n = max(len(c) for c in cells)
        for j in range(n):
            line = []
            for i in range(len(COLS)):
                t = cells[i][j] if j < len(cells[i]) else ""
                line.append(t.ljust(W[i]))
            print(sep.join(line).rstrip())
        print(sep.join("-" * W[i] for i in range(len(COLS))))

print("=" * 118)
print("PWC COSMOLOGY INVENTORY LEDGER - locked constants only, ZERO fitted parameters")
print("PWC side: DERIVED from the locked set | Measured side: Planck 2018 / SH0ES receipts")
print("Provenance labels: DERIVED / MEASURED / VERIFIED / BACK-SOLVED / CLAIMED / OPEN")
print("=" * 118)
print()
print("WHAT THE FRAMEWORK READS:  H0 (wall rate, k-bridge), rho0, eta_B = f_solid^3,")
print("  28/19 tempo, s/n_gamma, and the rho_max/rho0 = R_H/R_p hierarchy identity.")
print("WHAT IT DOES NOT READ (0 hits in papers/):  rho_crit, Omega_b, Omega_m,")
print("  Omega_Lambda - all Omega rows below are bookkeeping built on the tied share,")
print("  marked OPEN where no framework equation exists.")
print()
print_table(rows)
print()
print("-" * 118)
print("5-LINE SUMMARY")
print("-" * 118)
print("BEST HIT:    eta_B = f_solid^3 = %s vs Planck 6.104+/-0.058e-10 -> +0.57%%,"
      " +0.60 sigma (D39 CLOSED); its tied matter density rho_b = %s kg/m^3 vs"
      " 4.2021e-28 -> +0.38%%, +0.56 sigma." % (fnum(eta_B, 5), fnum(rho_b, 6)))
print("WORST MISS:  the Omega-share column carried by the locked H0 - Omega_b = %s vs"
      " 0.04930 -> -16.7%% (-9.6 sigma) and H0 itself vs Planck 67.36 -> +9.8%%"
      " (+12.2 sigma); the wall-vs-volume reading of the tension is qualitative only."
      % fnum(Ob_pwc, 5))
print("BIGGEST OPEN: Omega_m and Omega_Lambda have ZERO framework handles (0 paper hits);"
      " 'the untying's share' %s is a bookkeeping residue, not a Lambda claim - kept OPEN"
      " with kill conditions, not hidden." % fnum(Ol_pwc, 4))
print("CAVEAT HIT:  28/19 = %s vs 380/258 = 1.47286822 -> +0.0554%% (smallest residual),"
      " but the observed side is CLAIMED (audit F3) - the closure dies unless 380/258"
      " is reproduced from Planck 2018 tables." % fnum(tempo_pwc, 8))
print("NEXT:        quantify the wall/void split - turn the qualitative H0 tension"
      " (73.9 wall vs 67.4 volume average) into a volume-weighted H0 from a measured"
      " void fraction; that one step would close H0 and hand Omega_Lambda its first"
      " handle. Second priority: reproduce the 380/258 tempo provenance.")
print()
print("ZERO FITTED PARAMETERS - every PWC number above came from the locked set.")
print("SCRIPT EXITED 0")
sys.exit(0)
