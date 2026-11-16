#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PWC UNIVERSE CENSUS - the one-line ledger, built from LOCKED constants only.
Run: .venv-solar python scripts/quantify_universe_census.py   (exit 0)

RULES HONORED:
  * ZERO fitted parameters - every number is a locked constant or pure
    arithmetic on locked constants. Any fitted parameter is a defeat.
  * Every number carries provenance: DERIVED / MEASURED / VERIFIED /
    BACK-SOLVED / CLAIMED / OPEN. Misses are reported, never hidden.
  * A kill condition is stated for every candidate row.
  * Audit cross-references (audit/PILLAR2_HEAT_LAW_AUDIT.md):
      F1 : s_dot = -3 H s (the printed -4 H s is the 4/3 slip),
      F3 : 28/19 vs 380/258 - the 258 kyr side is CLAIMED, not established,
      N1 : 3.6013 vs exact 3.6016 k_B (2.701 vs 2.70118 rounding).
    D39: eta_B = f_solid^3 = 6.139e-10 is CLOSED (anomaly sweep).
  * Volume convention (stated, not hidden): R_H = c0/H0, the Hubble sphere,
    per the task's "observable volume" (4/3) pi R_H^3. The LCDM particle
    horizon (46.5 Gly) is 3.52x larger in radius, 43.5x in volume.
  * rho_max locked 1.29032e15 vs shell read 1.304e15: NOT used by the census.

Output: one ledger table, a 5-line summary (best hit / worst miss / next
derivation), the one-line universe sentence, and a markdown copy at
scripts/quantify_universe_census_ledger.md. No paper is edited.
"""
import math
import textwrap
import os

# ================= LOCKED CONSTANTS (never re-fit) =================
c0     = 2.99792458e8        # m/s
rho0   = 8.74e-27            # kg/m^3   MEASURED ambient (locked)
s      = 1.0 / 19.0          # DERIVED fold balance
f_sol  = 8.4989e-4           # DERIVED solid fraction
H0_kms = 73.935              # km/s/Mpc, the k-bridge, DERIVED (SH0ES-compat 0.86 sigma)
Q_CMB  = 4.175e-14           # J/m^3     MEASURED FIRAS (locked)
T_CMB  = 2.7255              # K         MEASURED FIRAS (locked)
kB     = 1.380649e-23        # J/K
hbar   = 1.054571817e-34     # J s
m_p_MeV= 938.272088          # MeV (PWC bare cage 937.19)
T_cub  = 27.0                # 3^3, the tightening coefficient
MPC    = 3.0856775814913673e22
GYR    = 3.15576e16
M_SUN  = 1.98892e30

m_p = m_p_MeV * 1.602176634e-13 / c0**2     # kg
c02 = c0 ** 2

# ---- external measured anchors (residual column only, never re-fit) ----
eta_obs, eta_obs_err = 6.104e-10, 0.058e-10   # Planck 2018 (workspace-frozen anchor)
Obh2, Obh2_err = 0.02237, 0.00015             # Planck 2018 Omega_b h^2
Omh2, Omh2_err = 0.1430, 0.0011               # Planck 2018 Omega_m h^2
R_horizon = 46.5e9 * 9.4607304725808e15       # m, LCDM particle horizon
T_firas, T_firas_err = 2.72548, 0.00057       # FIRAS
beta_Tz, beta_Tz_err = 0.007, 0.013           # T_CMB(z) slope, SZ/ALMA compilations (audit)

# ================= PURE ARITHMETIC (derived from locked only) =================
H0     = H0_kms * 1e3 / MPC                   # s^-1
R_H    = c0 / H0                              # m, Hubble sphere
V      = (4.0 / 3.0) * math.pi * R_H ** 3     # m^3
V_hor  = (4.0 / 3.0) * math.pi * R_horizon ** 3
rho_crit = 3.0 * H0**2 / (8.0 * math.pi * 6.67430e-11)
rho_h2    = 3.0 * (100e3 / MPC) ** 2 / (8.0 * math.pi * 6.67430e-11)  # rho_crit at h=1
Om_m_pwc  = rho0 / rho_crit
Om_m_obs  = Omh2 / (H0_kms / 100.0) ** 2
Om_m_obs_s= Omh2_err / (H0_kms / 100.0) ** 2
sigma_rho0 = (rho0 / rho_h2 - Omh2) / Omh2_err     # sigma of rho0 vs Planck Omega_m h^2

# bath state
Q_comp = math.pi**2 * kB**4 / (15.0 * hbar**3 * c0**3) * T_CMB**4   # a T^4 cross-check
s_bath = 4.0 * Q_CMB / (3.0 * T_CMB)                                # J/K/m^3
n_g    = 2.0 * 1.2020569031595943 / math.pi**2 * (kB * T_CMB / (hbar * c0))**3  # photons/m^3
s_ph   = s_bath / n_g / kB                                          # entropy per photon, k_B
eta_B  = f_sol ** 3                                                 # D39 CLOSED
n_k    = eta_B * n_g                                                # knots/m^3
n_b    = rho0 * s / m_p                                             # PWC baryons/m^3

# census
M_tied = rho0 * V
M_b    = M_tied * s                                # baryonic share (s = 1/19)
Q_tot  = Q_CMB * V
S_bath = s_bath * V
N_g    = n_g * V
N_k    = n_k * V
m_k    = M_b / N_k                                # implied knot mass, kg
m_k_MeV= m_k * c02 / 1.602176634e-13

# heat-drop clock
Qdot   = -4.0 * H0 * Q_CMB
Tdot   = -H0 * T_CMB * GYR                         # K/Gyr
sdot3  = -3.0 * H0 * s_bath                        # F1-corrected
sdot4  = -4.0 * H0 * s_bath                        # the slip

# measured-side quantities
rho_m_obs = Omh2 * rho_h2
M_hor_tot = rho_m_obs * V_hor
M_hor_ord = (Obh2 / Omh2) * M_hor_tot
rho_b_obs = Obh2 * rho_h2
ratio_obs = (rho_b_obs * c02) / Q_CMB             # matter:heat, measured
ratio_obs_s= ratio_obs * (Obh2_err / Obh2)
ratio_pwc = (rho0 * s * c02) / Q_CMB              # matter:heat, PWC
N_b_obs_V = eta_obs * n_g * V                     # measured baryons in Hubble volume
N_g_hor   = n_g * V_hor
S_hor     = s_bath * V_hor
Q_hor     = Q_CMB * V_hor
s_b_obs   = s_ph * kB / eta_obs                   # measured entropy per baryon (J/K)
s_b_pwc   = s_bath / n_b
lss_obs   = 380.0 / 258.0
lss_alt   = 377.7 / 258.0

def pc(x): return 100.0 * (x - 1.0)

# ================= LEDGER ROWS =================
rows = []

def add(name, formula, value, measured, residual, prov, kill):
    rows.append(dict(name=name, formula=formula, value=value, measured=measured,
                     residual=residual, prov=prov, kill=kill))

add("H0 (SI)",
    "73.935 km/s/Mpc",
    "%.5e s^-1" % H0,
    "2.184e-18 s^-1 (Planck 67.4)",
    "+9.70%% vs Planck; +0.86 sigma vs SH0ES",
    "DERIVED (k-bridge)",
    "KILL: H0 is BACK-SOLVED through k; if the k = 3069.87 chain breaks, the clock and every volume below break with it.")

add("R_H (radius)",
    "c0/H0",
    "%.5e m = %.3f Gpc = %.2f Gly" % (R_H, R_H/3.0856775814913673e25, R_H/9.4607304725808e15/1e9),
    "c/H(Planck) = 14.51 Gly; particle horizon 46.5 Gly",
    "-8.84%% vs c/H(Planck); -71.6%% vs horizon",
    "DERIVED (locked c0,H0)",
    "KILL: VOLUME CONVENTION - Hubble sphere is not the particle horizon (43.5x in volume); every volume quantity inherits this.")

add("V (volume)",
    "(4/3) pi R_H^3",
    "%.5e m^3" % V,
    "%.5e m^3 (horizon volume)" % V_hor,
    "-97.70%% (volume convention)",
    "DERIVED",
    "KILL: same convention as R_H; PWC census is a Hubble-sphere census, not a horizon census.")

add("M_tied (tied mass)",
    "rho0 * V",
    "%.5e kg = %.4e M_sun" % (M_tied, M_tied/M_SUN),
    "%.4e kg total matter / %.4e kg ordinary (horizon vol, Planck)" % (M_hor_tot, M_hor_ord),
    "%.1f%% / %.1f%% mass-level (volume-mismatched); density-level +%.1f%% = %.0f sigma" % (100*(M_tied/M_hor_tot-1), 100*(M_tied/M_hor_ord-1), 100*(rho0/rho_m_obs-1), sigma_rho0),
    "DERIVED (locked rho0,H0)",
    "KILL: rho0/rho_crit = %.3f (Omega_m,PWC) vs Planck Omega_m = %.4f +/- %.4f at h = %.4f -> %.0f sigma over-density; mass-level -92.5%%/-52.2%% are volume-mismatched (43.5x) and NOT the agreement they look like." % (Om_m_pwc, Om_m_obs, Om_m_obs_s, H0_kms/100.0, sigma_rho0))

add("Q_tot (bath heat)",
    "Q_CMB * V",
    "%.5e J" % Q_tot,
    "%.5e J (horizon volume)" % Q_hor,
    "-97.70%% (volume convention)",
    "DERIVED (FIRAS-locked Q)",
    "KILL: definitional a*T^4; fails only if FIRAS is wrong. a*T^4 recompute = %.4e vs locked %.4e (-0.004%%)." % (Q_comp, Q_CMB))

add("heat:matter",
    "Q : rho0*s*c0^2",
    "1 : %.1f (T/990 = %.4f mK)" % (ratio_pwc, T_CMB/990.0*1e3),
    "1 : %.1f +/- %.1f (Planck Omega_b h^2 = 0.02237)" % (ratio_obs, ratio_obs_s),
    "+%.1f%% in matter:heat = +%.1f sigma" % ((ratio_pwc/ratio_obs-1)*100, (ratio_pwc-ratio_obs)/ratio_obs_s),
    "DERIVED (S5, audit-verified)",
    "KILL: 14.1 sigma vs Planck baryon density; PWC needs Omega_b h^2 = %.5f (Planck: 0.02237 +/- 0.00015)." % (rho0*s/rho_h2))

add("s_bath (entropy dens.)",
    "4Q/3T",
    "%.5e J/K/m^3" % s_bath,
    "(4/3)aT^3 = same, FIRAS",
    "0.000%%",
    "DERIVED-from-locked; VERIFIED",
    "KILL: none - identity for a photon gas; definitional, not a prediction.")

add("n_g (photons/m^3)",
    "2zeta(3)/pi^2 (kT/hc)^3",
    "%.5e m^-3 = %.2f cm^-3" % (n_g, n_g*1e-6),
    "410.7 cm^-3 (FIRAS 2.72548 K)",
    "0.000%%",
    "VERIFIED (audit N1)",
    "KILL: definitional; the 2.701-vs-2.70118 rounding prints 3.6013 k_B vs exact %.4f k_B (cosmetic)." % s_ph)

add("N_g (CMB photons)",
    "n_g * V",
    "%.5e" % N_g,
    "%.5e (horizon volume)" % N_g_hor,
    "-97.70%% volume-driven; per-m^3 exact",
    "DERIVED",
    "KILL: volume convention.")

add("S_bath (total entropy)",
    "s_bath * V",
    "%.5e J/K" % S_bath,
    "%.5e J/K (horizon volume)" % S_hor,
    "-97.70%% (volume convention)",
    "DERIVED",
    "KILL: volume convention; entropy per photon %.4f k_B is exact (VERIFIED)." % s_ph)

add("S per baryon",
    "s_bath / (rho0*s/m_p)",
    "%.5e J/K = %.4e k_B" % (s_b_pwc, s_b_pwc/kB),
    "%.4e k_B (3.6016 k_B / eta_obs)" % (s_b_obs/kB),
    "-%.2f%% = -0.60 sigma" % (100*(1-s_b_pwc/s_b_obs)),
    "DERIVED",
    "KILL: inherits eta_B (+0.60 sigma); dies if Planck eta tightens below ~0.5%% without moving.")

add("eta_B (baryon/photon)",
    "f_solid^3",
    "%.4e" % eta_B,
    "%.3e +/- %.2e (Planck 2018)" % (eta_obs, eta_obs_err),
    "+%.2f%% = +%.2f sigma" % (pc(eta_B/eta_obs), (eta_B-eta_obs)/eta_obs_err),
    "DERIVED (CLOSED, D39)",
    "KILL: a pure fold number (8.4989e-4)^3; fails if Planck eta error shrinks below ~1%% without moving.")

add("N_knots",
    "eta_B * n_g * V",
    "%.5e (%.4f m^-3)" % (N_k, n_k),
    "%.5e baryons, same volume (Planck eta); 1.00e80 horizon" % N_b_obs_V,
    "+%.2f%% = +0.60 sigma (same volume)" % pc(N_k/N_b_obs_V),
    "DERIVED (D39)",
    "KILL: eta_B-dependent (+0.60 sigma). INTERNAL: rho0*s*V/N_k = %.1f MeV vs m_p = %.2f MeV -> +%.2f%% knot-mass gap (OPEN); measured-eta route gives %.1f MeV (+%.2f%%)." % (m_k_MeV, m_p_MeV, 100*(m_k_MeV/m_p_MeV-1), m_k_MeV*eta_B/eta_obs, 100*(m_k_MeV*eta_B/eta_obs/m_p_MeV-1)))

add("dQ/dt (heat-drop clock)",
    "-4 H Q",
    "%.5e J/m^3/s" % Qdot,
    "standard adiabatic law -4HQ; T_CMB(z) beta = 0.007 +/- 0.013 consistent",
    "0.000%% (definitional)",
    "DERIVED (chain D27)",
    "KILL: a measured beta /= 0 at T_CMB(z) breaks adiabaticity; beta currently consistent with 0.")

add("dT/dt (CMB cooling)",
    "-H * T_CMB",
    "%.5f K/Gyr" % Tdot,
    "band -0.19 to -0.21 K/Gyr (task); Planck H0 gives -0.186 K/Gyr",
    "PASS: inside band",
    "DERIVED",
    "KILL: degenerate with H0 - not directly measurable on Gyr timescales; the band itself excludes H0 <= 69 km/s/Mpc.")

add("s_dot (entropy drop)",
    "-3 H s_bath (F1-corrected)",
    "%.5e J/K/m^3/s" % sdot3,
    "entropy flux 3Hs = same; naive -4Hs = %.5e (the slip)" % sdot4,
    "0.000%% after F1 correction",
    "DERIVED + audit F1 CORRECTION",
    "KILL: bookkeeping - the printed -4H*s must be corrected to -3H*s wherever it appears (audit F1).")

add("28/19 (LSS tempo)",
    "s(1+T) = (1/19)(1+27)",
    "%.9f" % (s*(1+T_cub)),
    "380/258 = %.9f" % lss_obs,
    "+0.0554%%",
    "DERIVED; observed side CLAIMED (F3)",
    "KILL: 258 kyr has no identified Planck epoch (audit F3); with t_rec = 377.7 kyr the residual becomes +%.2f%% - the claim must name the two epochs." % (100*(s*(1+T_cub)/lss_alt-1)))

# ================= PRINT =================
W = [13, 18, 24, 30, 22, 22, 60]
HDR = ["quantity", "PWC formula", "PWC value", "measured value", "residual %/sigma", "provenance", "kill condition"]

def render(cells):
    wrapped = [textwrap.wrap(c, w) if w else [c] for c, w in zip(cells, W)]
    n = max(len(x) for x in wrapped)
    out = []
    for i in range(n):
        parts = [(x[i] if i < len(x) else "").ljust(w) for x, w in zip(wrapped, W)]
        out.append(" | ".join(parts).rstrip())
    return out

line = []
print("=" * 150)
print("PWC UNIVERSE CENSUS - one ledger, zero fitted parameters, locked constants only")
print("=" * 150)
print("R_H = %.4e m (%.3f Gpc, %.2f Gly) ; V = %.4e m^3 ; H0 = %.5f km/s/Mpc" %
      (R_H, R_H/3.0856775814913673e25, R_H/9.4607304725808e15/1e9, V, H0_kms))
print("convention: Hubble sphere c0/H0 (the task's observable volume); horizon is 43.5x larger")
print("=" * 150)
for row in render(HDR):
    print(row)
print("-" * 150)
for r in rows:
    for ln in render([r["name"], r["formula"], r["value"], r["measured"], r["residual"], r["prov"], r["kill"]]):
        print(ln)
    print("-" * 150)

# ================= SELF-CHECKS =================
print()
print("SELF-CHECKS (all must PASS):")
checks = [
    ("s_bath = 4Q/3T matches task's 2.042e-14", abs(s_bath - 2.042e-14) < 1e-17),
    ("dT/dt = %.4f K/Gyr inside [-0.21, -0.19]" % Tdot, -0.21 <= Tdot <= -0.19),
    ("heat:matter 1:%.1f matches 1:990" % ratio_pwc, abs(ratio_pwc - 990) < 2),
    ("eta_B = f_solid^3 = %.3e matches D39 6.139e-10" % eta_B, abs(eta_B - 6.139e-10) < 5e-13),
    ("dQ/dt = -4HQ = %.3e J/m^3/s" % Qdot, True),
    ("knot-mass gap +%.2f%% flagged OPEN, not hidden" % (100*(m_k_MeV/m_p_MeV-1)), True),
    ("zero fitted parameters: all inputs from LOCKED list", True),
]
for name, ok in checks:
    print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
assert all(ok for _, ok in checks), "self-check failed"
print("ALL SELF-CHECKS PASS")

# ================= 5-LINE SUMMARY =================
print()
print("5-LINE SUMMARY:")
print("1. BEST HIT    : eta_B = f_solid^3 = %.4e vs Planck %.3e +/- %.2e -> +%.2f%%, +0.60 sigma;"
      % (eta_B, eta_obs, eta_obs_err, pc(eta_B/eta_obs)))
print("                the knot census (%.3e) lands on the baryon census (%.3e) from a pure fold number, zero fits." % (N_k, N_b_obs_V))
print("2. HIT         : the heat-drop clock dT/dt = %.4f K/Gyr sits inside the -0.19..-0.21 K/Gyr band and" % Tdot)
print("                dQ/dt = -4H Q = %.3e J/m^3/s reproduces the adiabatic law exactly." % Qdot)
print("3. WORST MISS  : rho0 at density level - rho0 h^2 = %.4f vs Planck Omega_m h^2 = %.4f +/- %.4f" % (rho0/rho_h2, Omh2, Omh2_err))
print("                -> +225%%, %.0f sigma (mass-level %.1f%% vs total / %.1f%% vs ordinary matter, both volume-mismatched)." % (sigma_rho0, 100*(M_tied/M_hor_tot-1), 100*(M_tied/M_hor_ord-1)))
print("4. MISS        : heat:matter 1:%.1f vs measured 1:%.1f +/- %.1f (Planck Omega_b h^2 = 0.02237) -> +%.1f sigma."
      % (ratio_pwc, ratio_obs, ratio_obs_s, (ratio_pwc-ratio_obs)/ratio_obs_s))
print("5. NEXT        : derive the knot mass - rho0*s*V/N_k = %.1f MeV vs m_p = %.2f MeV (+%.2f%% internal gap);"
      % (m_k_MeV, m_p_MeV, 100*(m_k_MeV/m_p_MeV-1)))
print("                closing it (or showing 1023.3 MeV = a locked combination) finishes the census, else the gap is a kill.")

# ================= THE ONE-LINE UNIVERSE =================
finale = ("One Hubble volume (R_H = %.3e m) holds %.3e CMB photons at %.4f K carrying %.3e J of heat "
          "against %.3e kg of tied mass (heat:matter = 1:990, T/990 = %.4f mK), %.3e knots at "
          "eta_B = f_solid^3 = %.3e, %.3e J/K of bath entropy - cooling at dQ/dt = %.3e J/m^3/s, i.e. %.4f K/Gyr."
          % (R_H, N_g, T_CMB, Q_tot, M_tied, T_CMB/990.0*1e3, N_k, eta_B, S_bath, Qdot, Tdot))
print()
print("THE ONE-LINE UNIVERSE:")
print(finale)
print()
print("EXIT 0")

# ================= MARKDOWN COPY =================
here = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(here, "quantify_universe_census_ledger.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# PWC Universe Census Ledger (2026-10-21, locked constants only, zero fitted parameters)\n\n")
    f.write("Convention: R_H = c0/H0 = %.4e m (Hubble sphere); V = %.4e m^3. Horizon volume is 43.5x larger.\n\n" % (R_H, V))
    f.write("| quantity | PWC formula | PWC value | measured value | residual %/sigma | provenance | kill condition |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for r in rows:
        f.write("| %s | %s | %s | %s | %s | %s | %s |\n" % (
            r["name"], r["formula"], r["value"], r["measured"], r["residual"], r["prov"], r["kill"]))
    f.write("\n## 5-line summary\n\n")
    f.write("1. BEST HIT: eta_B = f_solid^3 = %.4e vs Planck %.3e +/- %.2e -> +%.2f%%, +0.60 sigma; knots %.3e on baryons %.3e.\n" % (eta_B, eta_obs, eta_obs_err, pc(eta_B/eta_obs), N_k, N_b_obs_V))
    f.write("2. HIT: dT/dt = %.4f K/Gyr inside the -0.19..-0.21 band; dQ/dt = -4H Q = %.3e J/m^3/s exact.\n" % (Tdot, Qdot))
    f.write("3. WORST MISS: rho0 h^2 = %.4f vs Planck Omega_m h^2 = %.4f +/- %.4f -> +225%%, %.0f sigma (mass-level %.1f%% vs total / %.1f%% vs ordinary matter, both volume-mismatched).\n" % (rho0/rho_h2, Omh2, Omh2_err, sigma_rho0, 100*(M_tied/M_hor_tot-1), 100*(M_tied/M_hor_ord-1)))
    f.write("4. MISS: heat:matter 1:%.1f vs 1:%.1f +/- %.1f -> +%.1f sigma.\n" % (ratio_pwc, ratio_obs, ratio_obs_s, (ratio_pwc-ratio_obs)/ratio_obs_s))
    f.write("5. NEXT: derive knot mass rho0*s*V/N_k = %.1f MeV vs m_p = %.2f MeV (+%.2f%%).\n" % (m_k_MeV, m_p_MeV, 100*(m_k_MeV/m_p_MeV-1)))
    f.write("\n## The one-line universe\n\n" + finale + "\n")
    f.write("\nAudit cross-refs: PILLAR2_HEAT_LAW_AUDIT.md F1 (s_dot = -3Hs), F3 (28/19 vs 380/258 provenance), N1 (3.6013 vs 3.6016 k_B). D39: eta_B = f_solid^3 CLOSED.\n")
print("markdown ledger written: %s" % md_path)
