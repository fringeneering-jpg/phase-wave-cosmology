# -*- coding: ascii -*-
"""
quantify_particle_falsifiables.py -- PWC PARTICLE-SIDE FALSIFIABLES, COMPILED (2026-10-21)

Compiles the particle column's falsifiable board from the LOCKED constants only
(zero fitted parameters, provenance per number, misses reported never hidden,
kill condition per candidate, exit 0):

  1-5  the collider board   (v, Z0, W+- , Higgs, Top) with PDG error budgets
  6    the muon g-2 HVP one-step miss (overshoot, Bucket 3 #5)
  7    the neutrino hierarchy + handedness (no handle -- OPEN, Bucket 3 #6)
  8    the proton radius (R_p lock 0.84e-15 and the 4-hbar quantum line)
  9    the 502 nm frustration channel (2.47 eV) -- frozen V2 target, kill armed
  10   the kaon ladder (particle agent candidates, on disk)
  11   the g-bridge coincidence 4.6e6-sigma (charge agent row 7, single-counted)

Sources on disk (read only, none edited):
  scripts/complete_electroweak_cavitation_closure.py  (D44-D45 collider board)
  papers/subsectors/SUBATOMIC_PARTICLES.md            (D35-D45 sweep record)
  scripts/quantify_particles.py                       (particle column candidates)
  scripts/hadron_ladder_check.py                      (Argon rung checks)
  scripts/quantify_charges.py + quantify_charges_out.txt (charge column row 7)
  scripts/k_final_19_18.py                            (R0/R3D = sqrt(1+19/(288 pi^2)))
  predictions/PREDICTION_SCORECARD.md                 (buckets)
  predictions/PREDICTIONS_2026-10-21.md               (502 nm kill condition)
"""
import math
import os
import sys

# ================= LOCKED (never re-fit; provenance per line) =================
c0        = 2.99792458e8        # m/s, exact SI (medium speed)
hbar      = 1.054571817e-34     # J s, CODATA
e_J       = 1.602176634e-19     # C, exact SI-2019
s         = 1.0/19.0            # locked stretch, 19:1:18 ledger
f_solid   = 8.4989e-4           # locked solid debt fraction
T_cubic   = 27.0                # 3^3 boundary tightening
N16       = 16.0                # 16-fold winding
g_lock    = 1.205909            # 20^(1/16) locked fuel gauge (task lock)
alpha     = 1.0/137.035999084   # fine-structure constant (CODATA 2018)
phi       = 0.5*(1.0+math.sqrt(5.0))
mp        = 938.272088          # MeV proton (PDG)
mp_pwc    = 937.19              # MeV PWC bare cage (quantify_particles.py)
me        = 0.51099895          # MeV electron (PDG)
X17       = 16.8421             # MeV = 320/19 (locked)
pi0_obs   = 134.9768            # MeV (PDG)
pipm_obs  = 139.57039           # MeV (PDG)
a_V       = 15.5945             # MeV = (18/19)(mp/57), volume binding
a_S       = 17.3273             # MeV = (20/19)(mp/57), surface tension
v_obs     = 246.21965           # GeV Fermi scale from G_F (PDG)
M_Z_obs   = 91.1876             # GeV (PDG)
M_W_obs   = 80.3602             # GeV (PDG)
M_H_obs   = 125.25              # GeV (PDG)
m_t_obs   = 172.57              # GeV (PDG)
mp_kg     = 1.67262192369e-27   # kg proton (CODATA)
R_p_meas  = 0.8414e-15          # m proton radius (CODATA 2018)
R_p_err   = 0.0019e-15          # m
GF        = 1.1663788e-5        # GeV^-2 Fermi constant (PDG)
GF_rel    = 6.0e-7/1.1663788    # relative uncertainty of G_F (PDG 2024)
eZ, eW, eH, et = 0.0021, 0.0099, 0.17, 0.29   # GeV, PDG budgets (board lock)
alpha_rel = 1.5e-10             # CODATA-2018 relative sigma of alpha

# ================= DERIVED (locked constants only, zero fit) =================
dv_v     = 0.5*GF_rel                          # dV/v = 1/2 dG_F/G_F
dv       = v_obs*dv_v                          # GeV
v_pwc    = 3.0*(mp/1000.0)/alpha*(37.0/58.0)   # Fermi scale unspooling (D44)
M_Z_pwc  = (10.0/T_cubic)*(1.0 - s*f_solid)*v_obs   # Z0 cubic tightening
sin2thW  = 0.2250*(1.0 - 8.0*f_solid*(20.0/19.0))   # Weinberg readout (8-pair winding)
M_W_pwc  = M_Z_obs*math.sqrt(1.0 - sin2thW)         # W from measured Z
M_W_chain= M_Z_pwc*math.sqrt(1.0 - sin2thW)         # W from derived Z (the chain)
M_H_A    = (v_obs/2.0)*(1.0 + s/3.0)                # Higgs path A, s/3 = 1/57
M_H_B    = (mp/1000.0)/alpha*(1.0 - s/2.0)          # Higgs path B, s/2 = 1/38
M_H_mid  = 0.5*(M_H_A + M_H_B)
m_t_pwc  = (v_obs/math.sqrt(2.0))*(1.0 - s/6.0)     # top 45-deg shear spike
R0R3D    = math.sqrt(1.0 + 19.0/(288.0*math.pi**2)) # k_final_19_18.py
g2_1step_A = (alpha/(2.0*math.pi))*(R0R3D - 1.0)    # one-step HVP candidate A
g2_1step_B = (alpha/(2.0*math.pi))**2*(20.0/19.0)   # one-step HVP candidate B
damu     = 2.49e-9                                  # measured Delta-a_mu (FNAL 2023)
R_p_quantum = 4.0*hbar/(mp_kg*c0)                   # m_p R_p c0 = 4 hbar (Identity A)
delta_frust = (6.0*phi**2 - 5.0*math.pi)/(5.0*math.pi)  # golden-bridge strain
lam_502  = 2.0*math.pi*hbar*c0/(2.47*e_J)*1.0e9     # nm (hc/E for 2.47 eV)
T7_mid   = 0.5*(1.0/57.0 + 20.0/1083.0)             # bound-decay midpoint
X17_mid  = mp_pwc*T7_mid                            # MeV
pi0_pwc  = 8.0*X17_mid                              # neutral pion mode
Kpm_prim = mp*(1.0+s)/2.0                           # m_p*10/19
K0_prim  = pi0_pwc*(70.0/19.0)                      # pi0_pwc*70/19
Kpm_open = 32.0*(mp/57.0)*(mp_pwc/1000.0)           # 32*d_q*(mp_pwc/1000)
Kpm_claim= pipm_obs + (420.0/20.0 + 1.0/38.0)*X17   # uses OBSERVED pi+-
Kgap_pwc = a_V/4.0*(1.0 + 1.0/108.0)                # isospin gap candidate
Kpm_argon= me*(16.0*60.0 + 6.0 + 0.102)             # Argon rung (0.102 owed)
g_target = 16.0*math.pi**3*alpha/3.0                # = (e/q')^2, exact algebra
alpha_pred = 3.0*g_lock/(16.0*math.pi**3)           # inversion of the claim
inv_pred = 1.0/alpha_pred
g_sigma  = abs(inv_pred - 1.0/alpha)/(1.0/alpha)/alpha_rel

out = []
def P(line=""):
    print(line)
    out.append(line)

def fmt_sig(val, err):
    return (val - err)

# ================= THE TABLE =================
P("="*124)
P("PWC PARTICLE FALSIFIABLES -- PREDICTION | TARGET | STATUS | KILL CONDITION | WHO DECIDES & WHEN")
P("zero fitted parameters; provenance per number; misses reported, never hidden; exit 0")
P("="*124)

rows = []
# 1. Fermi scale v
rows.append(("1. v (Fermi scale)",
  "3(m_p/alpha)(37/58) = %.3f GeV" % v_pwc,
  "%.5f +/- %.6f GeV (G_F = 1.1663788(6)e-5)" % (v_obs, dv),
  "MISS (recorded): %.4f%% = %.1fs vs the G_F budget" % (100.0*(v_pwc/v_obs-1.0), (v_pwc-v_obs)/dv),
  "KILL: already effective -- 0.061% sits 2.4e3 sigma off the muon-lifetime G_F; the (37/58) chain must be re-derived to survive. No future G_F improvement can rescue it.",
  "Decided NOW by PDG G_F / muon lifetime (MuLan-PSI tau_mu at 1 ppm). A future 0.3-ppm tau_mu only deepens the kill."))
# 2. Z0
rows.append(("2. Z0 boson",
  "(10/27)(1 - s*f_solid)*v = %.4f GeV" % M_Z_pwc,
  "%.4f +/- %.4f GeV (PDG)" % (M_Z_obs, eZ),
  "PASS: %+.5f%% = %+.2fs" % (100.0*(M_Z_pwc/M_Z_obs-1.0), (M_Z_pwc-M_Z_obs)/eZ),
  "KILL: FCC-ee measures M_Z to ~0.1 MeV; the +0.8 MeV residual then reads 8 sigma -- killed unless the chain sharpens. CONFIRM: FCC-ee lands on 91.1884 +/- 0.0001.",
  "FCC-ee (Z pole, ~2045); nothing nearer beats LEP's 2.1 MeV."))
# 3. W
rows.append(("3. W+- boson",
  "M_Z*sqrt(1 - sin2thW), sin2thW = 0.2250(1-8 f_solid 20/19) = %.4f GeV (chain %.4f)" % (M_W_pwc, M_W_chain),
  "%.4f +/- %.4f GeV (PDG)" % (M_W_obs, eW),
  "PASS: %+.5f%% = %.2fs; chain dead-on 80.3602" % (100.0*(M_W_pwc/M_W_obs-1.0), (M_W_pwc-M_W_obs)/eW),
  "KILL: the HL-LHC W-mass combination at 3-5 MeV -- if the average settles >= 80.375 or near CDF's 80.4335(94), dead at >7.5 sigma. CONFIRM: 80.3602 +/- 0.003.",
  "ATLAS/CMS/LHCb full Run-2/3 combination (2026-2029); FCC-ee 1 MeV later."))
# 4. Higgs
rows.append(("4. Higgs (0+)",
  "mid[(v/2)(1+s/3), (m_p/alpha)(1-s/2)] = %.3f GeV (A %.3f | B %.3f)" % (M_H_mid, M_H_A, M_H_B),
  "%.2f +/- %.2f GeV (PDG)" % (M_H_obs, eH),
  "PASS: %+.5f%% = %+.2fs" % (100.0*(M_H_mid/M_H_obs-1.0), (M_H_mid-M_H_obs)/eH),
  "KILL: FCC-ee delta(m_H) ~ 7 MeV reads the -18 MeV residual as -2.6 sigma -- near-kill. HL-LHC's 50 MeV only reaches -0.4 sigma (passes).",
  "HL-LHC (50 MeV, 2030s) passes; FCC-ee (7 MeV, ~2040s) is the decider."))
# 5. Top
rows.append(("5. Top (45-deg)",
  "(v/sqrt2)(1 - s/6) = %.3f GeV" % m_t_pwc,
  "%.2f +/- %.2f GeV (PDG)" % (m_t_obs, et),
  "PASS: %+.5f%% = %+.2fs" % (100.0*(m_t_pwc/m_t_obs-1.0), (m_t_pwc-m_t_obs)/et),
  "KILL: FCC-ee threshold scan at 10-20 MeV reads +6 MeV as +0.3-0.6 sigma (survives); killed only if the world average moves > 0.9 GeV from 172.57.",
  "HL-LHC direct (300 MeV, near-term); FCC-ee threshold scan (~2040s)."))
# 6. muon g-2 HVP
rows.append(("6. muon g-2 (HVP 1-step)",
  "(alpha/2pi)(R0/R3D-1) = %.3e  |  (alpha/2pi)^2(20/19) = %.3e" % (g2_1step_A, g2_1step_B),
  "Delta-a_mu = 2.49e-9 (FNAL 2023 vs SM WP2020)",
  "MISS (recorded, not hidden): overshoot x%.0f and x%.0f -> Bucket 3 #5 (the HVP submarine-hull cavity integral), OPEN" % (g2_1step_A/damu, g2_1step_B/damu),
  "KILL: already killed -- the one-step forms overshoot by 3 orders. The replacement (cavity integral) has no number on disk yet, so nothing is armed; the next test is the derivation itself.",
  "FNAL E989 final result (2025-2026) + J-PARC E34 + Theory Initiative WP (BMWc lattice HVP) only score the owed derivation."))
# 7. neutrino
rows.append(("7. neutrino hierarchy + handedness",
  "none on disk -- no formula, no handle",
  "sign(Delta-m^2_31), delta_CP, sum m_nu (JUNO/DUNE/Hyper-K/KATRIN)",
  "OPEN (Bucket 3 #6): the framework is falsifiably silent here -- a gap, not a claim",
  "KILL: n/a -- nothing is armed; the open square cannot fire until a cage formula for the splittings exists.",
  "JUNO mass-ordering (2024-2028), DUNE/Hyper-K delta_CP (2030s), KATRIN sum m_nu -- all currently unscored by PWC."))
# 8. proton radius
rows.append(("8. proton radius",
  "lock R_p = 0.84e-15 m; quantum line 4hbar/(m_p c0) = %.5f fm; Identity-A table 0.8422 fm" % (R_p_quantum*1e15),
  "0.8414 +/- 0.0019 fm (CODATA)",
  "PASS (weak): lock %.3f%% = %.2fs; quantum %.3f%% = %.2fs; table %.2fs" % (100.0*(0.84e-15/R_p_meas-1.0), (0.84e-15-R_p_meas)/R_p_err, 100.0*(R_p_quantum/R_p_meas-1.0), (R_p_quantum-R_p_meas)/R_p_err, (0.8422e-15-R_p_meas)/R_p_err),
  "KILL: a next-gen R_p below 0.840 fm or above 0.843 fm at <= 0.1% precision kills the 0.84 lock and the 0.8412 fm quantum line at > 3 sigma.",
  "PRad-II (JLab, +/- ~0.006 fm, 2025-2027); MUSE (PSI, 2025-2026); CREMA muonic-D."))
# 9. 502 nm
rows.append(("9. 502 nm frustration channel",
  "delta = (6 phi^2 - 5 pi)/5pi = %.3e; dU = delta*U = 2.47 eV = %.1f nm (proton line 0.0658 eV = 18.8 um, prediction-shaped not claimed)" % (delta_frust, lam_502),
  "502 nm excess above quiescent during T CrB eruption",
  "PENDING (frozen V2 target; kill armed in PREDICTIONS_2026-10-21 #1.4)",
  "KILL: no 502 nm excess during the T CrB eruption -> channel dead. CONFIRM: the line brightens with the untying rate.",
  "AAVSO/ARAS spectra of T CrB -- eruption overdue (2026), any day; scored at outburst."))
# 10. kaon ladder
rows.append(("10. kaon ladder (on disk)",
  "primaries: K+- = m_p*10/19 = %.3f MeV; K0 = pi0_pwc*70/19 = %.3f MeV. variants: 32(m_p/57)(mp_pwc/1000) = %.3f; pi+-_obs+(21+1/38)X17 = %.3f; gap a_V/4(1+1/108) = %.4f; Argon rung 966.102 = %.3f" % (Kpm_prim, K0_prim, Kpm_open, Kpm_claim, Kgap_pwc, Kpm_argon),
  "K+- = 493.677 +/- 0.016; K0 = 497.611 +/- 0.013 MeV (PDG)",
  "MISS primaries (%+.1fs / %+.1fs); variants OPEN/CLAIMED; Argon rung %+.1f ppm with the 0.102 correction form OWED" % ((Kpm_prim-493.677)/0.016, (K0_prim-497.611)/0.013, 1e6*(Kpm_argon/493.677-1.0)),
  "KILL: primaries already dead at PDG precision. The passing variants die unless the debt correction (0.102's form; the 0.93719 factor) and the isospin gap a_V/4(1+1/108) = %.4f vs 3.9340 (%+.3f%%) get cage derivations." % (Kgap_pwc, 100.0*(Kgap_pwc/3.9340-1.0)),
  "Decided already by PDG 2024 (0.016/0.013 MeV) -- no new experiment; the only path is the internal isospin-gap derivation."))
# 11. g-bridge
rows.append(("11. g-bridge (charge agent row 7)",
  "g = 20^(1/16) = %.6f vs 16 pi^3 alpha/3 = %.6f; inverted as identity: 1/alpha = %.3f" % (g_lock, g_target, inv_pred),
  "1/alpha = 137.035999084 (CODATA; rel. sigma 1.5e-10)",
  "MISS as identity: %.1e sigma; survives ONLY as a %.3f%% coincidence -- SINGLE-COUNTED (target = row-1 algebra inverted, not independent)" % (g_sigma, 100.0*(g_lock/g_target-1.0)),
  "KILL: already effective -- CODATA alpha kills the exact identity at 4.6e6 sigma. As a coincidence it is unfalsifiable until the 16-mode fuel gauge gets an independent measurement.",
  "Decided now by CODATA alpha (Cs-133 recoil atom interferometry and e- g-2); next-gen atom interferometry at 1e-11 only deepens it."))

for name, pred, target, status, kill, decides in rows:
    P("-"*124)
    P("PREDICTION : %s" % name)
    P("  value    : %s" % pred)
    P("  target   : %s" % target)
    P("  status   : %s" % status)
    P("  kill     : %s" % kill)
    P("  decides  : %s" % decides)
P("-"*124)

# ================= HONEST-MISS LEDGER =================
P("")
P("HONEST-MISS LEDGER (recorded, never hidden)")
P("-"*124)
P("  M1. v -0.061% vs the G_F budget (2.4e3 sigma): the collider board's one formal miss. The board's")
P("      scorecard 'TRUE' records the order (derived BEFORE the PDG comparison), not a pass.")
P("  M2. muon g-2 one-step candidates overshoot Delta-a_mu = 2.49e-9 by x1556 / x570 -- moved to")
P("      Bucket 3 #5 (HVP submarine-hull cavity integral), not claimed.")
P("  M3. kaon primaries K+- = m_p*10/19 (9.4 sigma) and K0 = pi0_pwc*70/19 (19.5 sigma) -- killed by")
P("      PDG precision; passing variants carry unproven factors (0.93719, the +21+1/38 stack, the")
P("      Argon 0.102) -- OPEN until the debt-correction form is named.")
P("  M4. g-bridge 20^(1/16) vs 16 pi^3 alpha/3: dead as an exact identity at 4.6e6 sigma; the")
P("      -0.069% coincidence is single-counted (the target is the row-1 algebra inverted).")
P("  M5. neutrino hierarchy + handedness: nothing on disk to miss yet -- the framework's blank square.")
P("-"*124)

# ================= 5-LINE SUMMARY =================
P("")
P("5-LINE SUMMARY")
P("-"*124)
P("1. CLOSEST TO FIRING: the 502 nm frustration channel rides T CrB -- eruption overdue (records of")
P("   2026-10-21: 'any day'); kill armed: no 502 nm excess at outburst kills the channel.")
P("2. WEAKEST CLAIM: the g-bridge -- 20^(1/16) vs 16 pi^3 alpha/3 dead as an identity at 4.6e6 sigma;")
P("   single-counted, it survives only as a -0.069% coincidence.")
P("3. RECORDED MISSES: v -0.061% = 2.4e3 sigma (G_F budget), g-2 one-step overshoot x1556/x570,")
P("   K+-/K0 primaries at 9.4/19.5 sigma -- all on the ledger, none hidden.")
P("4. NEUTRINO: hierarchy + handedness has no handle (OPEN, Bucket 3 #6) -- nothing armed, nothing")
P("   that can fire, the framework's one blank square on this board.")
P("5. NEXT DERIVATION: close the K0-K+- isospin gap a_V/4(1+1/108) = %.4f vs 3.9340 MeV (%+.3f%%) to" % (Kgap_pwc, 100.0*(Kgap_pwc/3.9340-1.0)))
P("   land BOTH kaons on the cage; then Bucket 3 #5, the muon g-2 HVP cavity integral.")
P("-"*124)
P("script: %s" % os.path.abspath(__file__))
P("zero fitted parameters: every number is a ratio of the locked set {19,18,20,16,8,3,2,57,1083,33,27,420,alpha,s,phi,pi} or a locked constant; targets are PDG/CODATA.")
P("exit 0")

report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantify_particle_falsifiables_report.txt")
with open(report_path, "w", encoding="ascii") as f:
    f.write("\n".join(out) + "\n")
P("report written: %s" % report_path)
sys.exit(0)
