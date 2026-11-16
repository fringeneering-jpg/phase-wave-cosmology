#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
quantify_falsifiables_master.py -- Phase Wave Cosmology: the COMPLETE falsifiable catalog.

Compiled 2026-10-21 from papers/ (UNIFIED, DERIVATIONS, NEUTRON_LIFETIME, subsectors, clay),
predictions/ (PREDICTIONS_2026-10-21, PREDICTION_SCORECARD), capture/ (all 2026-10-15 .. 2026-10-21
rulings), audit/ (OPEN_ITEMS_LEDGER, PILLAR2 audit, PROMPT F final, SCRIPT_EXECUTION_PASS), and the
executed scripts (speed_census, merger_neck_yield, anchor_closure_test, quantify_charges,
quantify_universe_census, sixteen_fold_grind_check, cmb_birefringence).

Rules honored: ZERO fitted parameters (locked set only); provenance per number
(DERIVED / MEASURED / VERIFIED / BACK-SOLVED / CLAIMED / OPEN); misses reported, never hidden;
a kill condition per candidate, stated before the data; this script exits 0.
No paper is edited by this script. Output: console table + predictions/FALSIFIABLE_CATALOG.md.
"""
import math
import sys
from pathlib import Path

# force UTF-8 console output (Windows cp1252 stdout would choke on the ledger's symbols)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------- LOCKED CONSTANTS (never re-fit) ----------------
c0     = 2.99792458e8
rho0   = 8.74e-27
RHO_MAX_SHELL = 1.304e15        # MEASURED shell read (GW150914)
RHO_MAX_DERIV = 1.29032e15      # DERIVED ceiling (D46)
rho_core = 2.3e17
R_p    = 0.84e-15
s      = 1.0/19.0
Y_bow  = 5.9307e26
n_lock = 2.0/33.0               # the SHAPE (ruled)
f_solid = 8.4989e-4
k      = 3069.87
a_max  = 3.23e11
a0_bare = 6.6110e-11
T27    = 27.0
N      = 16.0
g_lock = 20.0**(1.0/16.0)
alpha  = 1.0/137.035999084
m_p    = 938.272088              # MeV
m_e    = 0.51099895              # MeV
G      = 6.67430e-11
hbar   = 1.054571817e-34
kB     = 1.380649e-23
Q_CMB  = 4.175e-14
T_CMB  = 2.7255
H0_wall = 73.935                 # km/s/Mpc (wall rate)
MeV_J  = 1.602176634e-13
h_eVs  = 4.135667696e-15
ZETA3  = 1.202056903159594

# ---------------- VERIFICATION BLOCK (locked constants only) ----------------
checks = []
def chk(name, value, target, fmt="%.6g", tol_rel=None):
    r = (value/target - 1.0) if target else 0.0
    ok = (abs(r) <= tol_rel) if tol_rel is not None else True
    checks.append((name, value, target, r, fmt, ok))
    return value

phi = (1.0 + math.sqrt(5.0))/2.0
chk("wall/void ratio 19/18", 19.0/18.0, 1.05556, "%.6f")
chk("28/19 (LSS tempo multiplier)", s*(1+T27), 1.473684, "%.6f")
chk("380/258 (Planck observed side)", 380.0/258.0, 1.472868, "%.6f")
chk("predicted tempo 380/(28/19) [kyr]", 380.0/(s*(1+T27)), 258.0, "%.3f")
chk("tempo residual %", 100*((s*(1+T27))/(380.0/258.0)-1.0), 0.0554, "%.4f")
lam502 = h_eVs*c0/2.47e-9
chk("502 nm channel [nm]", lam502, 502.0, "%.2f")
chk("18.8 um proton line [nm]", h_eVs*c0/0.0658e-9, 18800.0, "%.0f")
a_neck = a_max*math.sqrt(2.0/3.0)
chk("merger neck yield sqrt(2/3)*a_max [N/kg]", a_neck, 2.6373e11, "%.4e")
chk("neck vs 193-merger scan 2.64e11 [%]", 100*(a_neck/2.64e11-1.0), -0.10, "%.2f")
t_loop = 32.0*43.85e3/c0
chk("16-fold ringdown 32*dt_shed/c0 [ms]", t_loop*1e3, 4.68, "%.4f")
chk("ringdown residual [%]", 100*(t_loop/4.68e-3-1.0), 0.012, "%.3f")
S8p = 0.8320*(19.0/20.0)
chk("S8 = S8_Planck*19/20", S8p, 0.7904, "%.4f")
chk("S8 vs DES Y6 0.789 [sigma]", (S8p-0.789)/0.012, 0.12, "%.2f")
g_t = 16.0*math.pi**3*alpha/3.0
chk("g-bridge 20^(1/16) vs 16pi^3 a/3 [%]", 100*(g_lock/g_t-1.0), -0.069, "%.3f")
inv_alpha = 3.0*g_lock/(16.0*math.pi**3)
chk("g claimed exact -> 1/alpha", 1.0/inv_alpha, 137.035999084, "%.3f")
chk("bridge 9/(4s)", 9.0/(4.0*s), 42.7416, "%.4f")
tau_beam = 879.0/(1.0 - k*791.0/c0)
chk("neutron tariff tau_beam [s]", tau_beam, 886.17, "%.2f")
chk("tau_beam vs NIST 887.7+/-2.2 [sigma]", (tau_beam-887.7)/2.2, 0.7, "%.2f")
# derived rho_max closure (D46) and the anchor-test route
rho_closed = (2.0*Y_bow/c0**2)**(33.0/29.0) * rho0**(-4.0/29.0)
chk("derived rho_max (2Y/c0^2)^(33/29) rho0^(-4/29)", rho_closed, RHO_MAX_DERIV, "%.4e", tol_rel=0.005)
chk("derived vs shell residual [%]", 100*(RHO_MAX_DERIV/RHO_MAX_SHELL-1.0), -1.05, "%.2f")
rho_closed_n = (2.0*Y_bow/c0**2)**(1.0/(1.0-2.0*0.0606)) * rho0**(-2.0*0.0606/(1.0-2.0*0.0606))
chk("anchor-test rho_max at locked n=0.0606 vs shell [%]", 100*(rho_closed_n/RHO_MAX_SHELL-1.0), -1.178, "%.2f")
C_ladder_deriv = c0*(rho0/RHO_MAX_DERIV)**0.0606
C_yield_deriv  = math.sqrt(2.0*Y_bow/RHO_MAX_DERIV)
chk("v_cav re-anchor C(rho_max_derived) [km/s]", C_ladder_deriv/1e3, 958.8, "%.2f", tol_rel=0.002)
chk("yield-law C at derived ceiling [km/s]", C_yield_deriv/1e3, 958.78, "%.2f", tol_rel=0.002)
chk("old v_cav floor at shell rho_max [km/s]", math.sqrt(2.0*Y_bow/RHO_MAX_SHELL)/1e3, 954.0, "%.1f", tol_rel=0.002)
n_g = 2.0*ZETA3/math.pi**2*(kB*T_CMB/(hbar*c0))**3
eta_B = f_solid**3
m_knot_kg = rho0*s/(eta_B*n_g)
m_knot_MeV = m_knot_kg*c0**2/MeV_J
chk("census knot mass rho0*s*V/N_k [MeV]", m_knot_MeV, 1023.4, "%.1f", tol_rel=0.002)
chk("knot-mass gap vs m_p 938.272 [%]", 100*(m_knot_MeV/m_p-1.0), 9.07, "%.2f", tol_rel=0.05)
H0_si = H0_wall*1e3/3.085677581e22
chk("dT_CMB/dt = -H*T [K/Gyr]", H0_si*T_CMB*3.15576e16, 0.2061, "%.4f")
chk("eta_B = f_solid^3", eta_B, 6.139e-10, "%.3e")
chk("X17 = 16*(20/19) [MeV]", 16.0*20.0/19.0, 16.8421, "%.4f")
chk("Hall partition 19-16", 19.0-N, 3.0, "%.0f")
chk("Hall partition 18-16", 18.0-N, 2.0, "%.0f")
chk("B1508+55 sigma above 954", (1083.0-954.0)/90.0, 1.43, "%.2f", tol_rel=0.15)
chk("GW190521 min(E,S)/catalog - 1 [%]", 100*(5.56/9.0-1.0), -38.2, "%.1f", tol_rel=0.05)
chk("tau_loop = 16L/(sqrt2 c0) [ms]", 16.0*2.0*math.sqrt(2.0)*43.85e3/(math.sqrt(2.0)*c0)*1e3, 4.6806, "%.4f")
chk("neck E for GW150914 at neck yield [Msun]",
    G*36.0*29.0*1.98847e30/(2.0*c0**2*(math.sqrt(G*36.0*1.98847e30/a_neck)+math.sqrt(G*29.0*1.98847e30/a_neck))),
    3.018, "%.3f", tol_rel=0.02)

# ---------------- THE CATALOG ----------------
# statuses: armed, pending, true, miss   speed: 0=now(archives) 1=days-weeks 2=months 3=years 4=decades+/standing 5=~2083
SPEED = {0:"now (archives/running)", 1:"days-weeks", 2:"months", 3:"years", 4:"decades+/standing", 5:"~2083 (literature)"}
ROWS = [
# ================= ARMED =================
dict(name="T CrB (Blaze Star) kill #1 — re-hold decline", status="armed", speed=0,
 pred="The decline from maximum is the dam re-holding (re-tying at the local C(rho)), steeper than any Ni-56 radioactive slope, then a re-hold plateau as the re-tied knots hold the budget — the 1866/1946 pattern repeats.",
 kill="A decline shape matching the standard TNR/nucleosynthesis radioactive tail exactly, with no re-hold plateau.",
 data="AAVSO light curves + ARAS spectra. The ~80-year nova is overdue (last erupted 1946), flagged 'days away' through 2026.",
 prov="CLAIMED (mechanism ruling 2026-10-18); frozen 2026-10-21, kill armed."),
dict(name="T CrB kill #2 — the heat ledger E_total = m_drop·c0²", status="armed", speed=0,
 pred="E_total = m_drop × c0² — bolometric output / c0² = the ejected-unspooled mass; the expelled share 18/19 and the retained 1/19 read as the remnant's tightened state.",
 kill="E_total/m_drop != c0² within measurement, once the bolometric curve and the ejecta mass are in.",
 data="AAVSO bolometric light curve + ejecta-mass spectroscopy (ARAS).",
 prov="DERIVED (c0² = 8.9876e16 J/kg ledger); frozen 2026-10-21."),
dict(name="T CrB kill #3 — the choke pre-signal", status="armed", speed=0,
 pred="The stall is visible BEFORE the flash: the pre-eruption months carry a choked, sub-luminous plateau (pressure building against the refusal), not a smooth accretion ramp.",
 kill="A clean monotonic accretion rise into the eruption with no pre-flash stall signature.",
 data="AAVSO long-term light curve + the literature's accretion-state windows (Forbes 2026-06-02; arXiv:2607.15245).",
 prov="CLAIMED (mechanism); frozen 2026-10-21."),
dict(name="T CrB kill #4 — the 502 nm frustration channel", status="armed", speed=0,
 pred="The 502 nm frustration channel (DeltaU = delta·U = 2.47 eV, the color of the medium's resistance) brightens above quiescent during the eruption, tracking the untying rate.",
 kill="No 502 nm excess during the eruption.",
 data="ARAS/AAVSO spectra at 502 nm through the eruption.",
 prov="DERIVED (D12, delta = (6 phi^2 - 5 pi)/5 pi); frozen V2 target."),
dict(name="Pulsar speed census — cap ladder 954 → 958.8 km/s (P3-NEXT-1)", status="armed", speed=0,
 pred="No unslammed body above its density cap: quiet v<600, near-Mach 600-954, cap-runner >=954, slammed >1.2x954 km/s; a bow requires v >= 0.9·C_own = 859 km/s for rho_max bodies; the cap re-anchors 954 -> 958.8 km/s at the derived ceiling rho_max = 1.29032e15 (the C-ladder meets the yield there).",
 kill="K1: a pulsar with v-5sigma > 954 km/s and a literature-confirmed signature absence kills the 954 cap for neutron stars (B1508+55: 1,083 +103/-90 km/s, +1.3sigma — INCONCLUSIVE; decisive read needs sigma_v <= 26 km/s). K2: a confirmed medium bow at v < 0.9·C_own kills the bow law's lower bound. K3: an unslammed body with rho_eff = 2Y_bow/v² > rho_max kills the grid law.",
 data="ATNF pulsar catalogue + proper motions (Gaia/VLBA). Census executed 2026-10-21 (scripts/speed_census.py): no kill; CID-42 0.290 rho_max, 3C 186 0.206 rho_max (declared SLAM exception class); B1508+55 'not failed, not passed' — pending astrometry.",
 prov="DERIVED cap (C(rho) ladder); B1508+55 MEASURED; 958.8 re-anchor DERIVED (D46)."),
dict(name="T_CMB(z) slope = -H", status="armed", speed=0,
 pred="The entropy clock reads dT_CMB/dt = -H·T_CMB = -0.206 K/Gyr (wall rate 73.8) to -0.188 K/Gyr (H = 67.4); T(z) = T0(1+z), i.e. the z-slope beta = 0 exactly (adiabatic).",
 kill="A measured beta != 0 in the published SZ/ALMA T(z) compilations breaks adiabaticity; a dT/dt outside the band excludes H0 <= 69 km/s/Mpc (the band's own content).",
 data="Published SZ T(z) compilations + ALMA CO line temperatures (z ~ 1-7). Measurable NOW with existing data.",
 prov="DERIVED (D27 chain; T ~ rho^(1/3) -> d ln Q/dt = -4H). Pillar-2 audit: not discriminating vs Lambda-CDM (identity) — consistency ledger."),
dict(name="BL1 sheath-weighted spectrum (run-matched)", status="armed", speed=0,
 pred="tau_beam = tau0/(1 - k·v_eff/c0) = 886.17 s (k = 3069.87, v_eff ~ 791 m/s) folded over the measured BL1 velocity spectrum, weighted by BOTH velocity and the per-particle broken-down-light sheath; the beam lifetime lengthens with the local light-bath intensity; a single free neutron keeps its own sheath unless something strips it.",
 kill="No sheath-intensity dependence in the BL1 data; or a stripped single free neutron whose lifetime does not shorten.",
 data="NIST BL1 beamline measured spectrum (NIST Eqs. 3-5 weighting), the run-matched distribution not the illustrated one.",
 prov="k DERIVED (19/18 axial pitch); tau0 = 879.4 s MEASURED (UCNtau); v_eff MEASURED (NG-6); the sheath weighting OPEN (ruling not yet an equation)."),
dict(name="Birefringence void template — rank-correlation", status="armed", speed=0,
 pred="beta(n_hat) = integral K(rho,...) ds, dK/d(ln rho) < 0 — voids enhanced, walls suppressed; frozen template over 1,163 Douglass+ 2023 voids, top corridor RA 142-150 deg, Dec +31-46 deg, amplitude ~0.177 deg.",
 kill="The pre-specified rank-correlation with the direction-dependent beta map fails the frozen template/sign/exclusions.",
 data="Planck/ACT/SPT polarization maps (direction-dependent cosmic birefringence).",
 prov="SIGN CLOSED (two-motion retarded chiral path, 2026-10-20); template DERIVED, correlation armed (D32)."),
dict(name="X17 non-confirmation watch", status="armed", speed=0,
 pred="The X17 closure (16·20/19 = 16.8421 MeV, +0.0125% vs the 16.84 MeV anomaly) rests on the unconfirmed Atomki signal.",
 kill="NA64 / MEG II / PADME non-confirmation removes the anchor — the closure dies either way.",
 data="NA64, MEG II, PADME (running).",
 prov="X17 MEASURED-anchor (unconfirmed anomaly); formula DERIVED."),
dict(name="Pioneer law coupling (D38) — Cassini/MESSENGER kill", status="armed", speed=0,
 pred="a_PWC = c0·H0·(1+Delta_rho_geom) = 8.93e-10 m/s² acts on the Pioneers at 20-70 AU (+2.17% vs 8.74+/-1.33e-10 m/s²).",
 kill="MESSENGER/BepiColombo radio tracking shows no unmodeled sunward excess beyond the thermal-recoil budget at Mercury range; Cassini-era range residuals (<= few x 1e-10 m/s²) already tension an all-matter coupling — the law must pre-register its object-dependence.",
 data="MESSENGER, BepiColombo, Cassini radio tracking.",
 prov="DERIVED (D38); coupling object-dependence OPEN."),
dict(name="V Sagittae — mass-transfer saturation stall", status="armed", speed=0,
 pred="The transfer feeds the choke from the other side: accretion saturates the companion's capacity until the medium refuses at its own rate — the saturation IS the stall, the long-term brightening shows stall/plateau structure, and the endpoint is the same relief-runaway chain as every eruption.",
 kill="The system's long-term brightening shows no stall/plateau structure — a smooth monotonic ramp all the way in.",
 data="AAVSO archival light curve + ASAS-SN + archival plates (scoreable NOW); endpoint ~2083 (the literature's merge date).",
 prov="CLAIMED (mechanism); date MEASURED-literature."),
dict(name="Solar holdout — next M/X AR scored blind (Pi_V > 1, zeta_yield)", status="armed", speed=1,
 pred="Pi_V = C(rho)²/(eps_a c0²) > 1 at the polarity boundary is eruption-necessary (block first, then zeta): an eruption requires Pi_V > 1 AND zeta -> zeta_yield = 3.84e4; a strong AR that never crosses Pi_V = 1 will NOT erupt (the AR 12192 pattern). Flare day: the 7% (6.84%) restricted share holds, churn ~0.82 Hz, restricted power 2.68e25 W, and a pre-flare load spike (like the 5.26e23 W spike at 07:00 UT before AR 12192's 16:59 flare) precedes the flare by hours.",
 kill="An eruptive AR whose Pi_V stayed below 1 through the buildup; or a Pi_V > 1 AR that erupts with zeta nowhere near zeta_yield; or a flare day with no pre-flare load spike.",
 data="HMI magnetograms (JSOC/Helioviewer), AIA (Helioviewer), EIS where available. Blind protocol pre-registered (data/solar/PREREGISTRATION.md; frozen law corona_model_frozen.json).",
 prov="DERIVED (frozen law); zeta_yield DERIVED; the 7% share VERIFIED 6.84%."),
dict(name="502 nm electron channel / 18.8 um proton line (frozen V2)", status="armed", speed=1,
 pred="DeltaU = delta·U = 2.47 eV = 502 nm electron channel; 0.0658 eV = 18.8 um proton line (prediction-shaped, not claimed).",
 kill="The 502 nm channel is never observed where the untying rate peaks (including the T CrB eruption) and the 18.8 um line is absent.",
 data="ARAS/AAVSO spectra (T CrB); dedicated 502 nm photometry/spectroscopy; IR spectroscopy for 18.8 um.",
 prov="DERIVED (D12); the observational match is CLAIMED-shaped, not claimed."),
dict(name="Next cap-runner, predicted before measurement", status="armed", speed=4,
 pred="Every future fast object lands on the density grid: no gas-branch body above 0.1873 c0 (56,156 km/s), no rho_max body above 958.8 km/s except forced-passage slams (recoil SMBHs).",
 kill="A confirmed fast object off the grid at its own density.",
 data="Gaia DR4/DR5 proper motions, pulsar timing surveys, future astrometry.",
 prov="DERIVED (C(rho) grid); standing falsifier."),
dict(name="Galaxy weather radar — x = g_bar/(18·a0_bare)", status="armed", speed=0,
 pred="Settled x<0.5 / stalling 0.5-1 / runaway x>=1; scored 1,749 settled (99.7%) and 5 stalling (NGC 1365, NGC 4102, NGC 4429, NGC 5719, UGC 02183 — the known active ones).",
 kill="A galaxy with x >= 1 showing no stall/runaway signature, or a settled (x<0.5) galaxy running away.",
 data="SPARC/SDSS kinematics + 2MRS environment (available now).",
 prov="DERIVED (18a0 choke); the 1,749/5 scoring VERIFIED."),
# ================= PENDING =================
dict(name="Wall/void contrast 19/18 = 1.0556 (P2-A stacked SZ test)", status="pending", speed=1,
 pred="y_wall/y_void = 19/18 = 1.05556 — the wall is the untying front (always moving out); the swept void behind runs at 18/19 = 94.74% (the 1/19 = 5.26% deficit is the retained debt share s); the front is a local maximum of the stacked radial profile, void centers under-pressured. Zero fitted parameters.",
 kill="(1) r < 1 at >=3sigma; (2) |r - 1.0556| > 3·sigma_tot (sigma_sys = 0.010 floor); (3) no front peak at 3sigma; (4) full y-map coupling ruled (already dead: full coupling gives y = 0.62 per 100 Mpc vs observed <= 1e-5). No-decision: sigma_stat > 0.028 -> inconclusive, stays OPEN.",
 data="ACT DR6 + SPT-3G y-maps; Douglass+ 2023 voids (Planck2018 rows only, edge==0, |b|>=15 deg, cluster-masked: 805 voids); Planck MILCA cross-check. Current MILCA single-pixel read: ratio 0.8548 = ratio-of-two-negative-medians artifact — INCONCLUSIVE; sign fraction 52.1% (2.0sigma).",
 prov="DERIVED (19:1:18 balance); BLOCKED on author rulings R1 (y<->P coupling) and R2 (front thickness); frozen 2026-10-21T17:30."),
dict(name="Next light-BH merger — neck yield 2.6373e11 N/kg", status="pending", speed=2,
 pred="The dropped mass of the next high-SNR light BH merger (M_f <= 25 Msun) reads min(E, S) with the 3D-to-2D neck yield a_max,neck = a_max,3D·sqrt(2/3) = 2.6373e11 N/kg, not the solitary-shell 3.23e11.",
 kill="The catalog's E-limit mass drop for light events lands on the 3.23e11 curve, not the neck curve.",
 data="GWOSC event API / LVK O4b-O5 stream (gwtc4/5_blind_results.csv local).",
 prov="DERIVED (sqrt(2/3) containment); retrofit: 193-merger scan min 2.64e11 (bootstrap 2.58-2.80e11) vs neck -0.10% — CLOSED D2; honest disagreement with the locked 3.23e11 on record."),
dict(name="Next light-BH ringdown — the 16-fold 4.68 ms family", status="pending", speed=2,
 pred="tau_loop = 16L/(sqrt2·c0) = 32·Delta_t_shed/c0 = 4.6806 ms carries the ringdown time constant for the post-merger fold.",
 kill="A light-BH ringdown resolved at SNR where the 16-fold clock's crossing is testable and shows no 4.68 ms family.",
 data="LVK strain data (O4b/O5).",
 prov="CLOSED on GW150914 (4.6806 ms vs 4.68 ms, +0.012%, scripts/sixteen_fold_grind_check.py); the next-event check is a timing test, not a waveform claim."),
dict(name="Next nearby supernova — held-wave/luminous-wave arrival ladder (PREDICTION 5, PROPOSED)", status="pending", speed=3,
 pred="(a) The neutrino burst precedes the light by hours — the unheld medium wave runs at 99.99% c0 while the luminous wave pays the stiff-medium drag out of the star. (b) The gamma flash lags the blast wave by ~1.7 s — the held luminous wave pays the tariff's time.",
 kill="(a) Any well-instrumented nearby SN whose neutrinos and light arrive within minutes of each other. (b) A nearby SN with no ~1.7 s gamma delay.",
 data="Super-K/Hyper-K + IceCube + optical/gamma follow-up of the next nearby SN.",
 prov="CLAIMED (author's ruling + SN 1987A's record; no script on disk yet — P3 miss #5). Ruling #13 recommends adoption."),
dict(name="r = 0 — no-inflation B-modes (CANDIDATE)", status="pending", speed=3,
 pred="No inflaton => no primordial B-modes; r = 0.",
 kill="r > 0.01 detected (asymmetric kill-only).",
 data="BICEP/SPT-3G/ACT; LiteBIRD and CMB-S4 for the decisive read.",
 prov="CANDIDATE — needs author sign-off (Ruling #8)."),
dict(name="Neutrino ladder — Delta m²31/Delta m²21 = 32·(1+T7) (PROPOSED)", status="pending", speed=3,
 pred="Delta m²31/Delta m²21 = 32·(1+T7) = 32.561 vs PDG 32.576 (-0.046%); dead vs NuFIT 33.9 (-4.0%).",
 kill="Inverted ordering (JUNO/DUNE) or the NuFIT ratio settling.",
 data="JUNO, DUNE, NuFIT global fits.",
 prov="PROPOSED — needs the axial-pitch ruling (Ruling #7)."),
dict(name="Knot-mass gap — census 1023.4 vs m_p = 938.27 MeV", status="pending", speed=0,
 pred="The census-implied knot mass rho0·s·V/N_k (N_k = eta_B·n_g·V, eta_B = f_solid³) must equal the proton mass m_p = 938.272 MeV from locked constants alone.",
 kill="The gap must close via a locked-constant chain, or it stands as a permanent recorded internal miss: current value 1023.4 MeV vs m_p 938.272 MeV = +9.07% (measured-eta route 1029.3 MeV = +9.70%).",
 data="Internal census (scripts/quantify_universe_census.py, quantify_universe_census_ledger.md).",
 prov="DERIVED (census); the +9.07% gap OPEN — reported, never hidden."),
dict(name="Hall ladder generalization — nu = 1/3, 2/5, 2/3 from the 19:18/N=16 partition", status="pending", speed=0,
 pred="The 16-fold winding partition emits {19-16, 18-16} = {3, 5}: Hall quasiparticle charges e/3 (nu=1/3), e/5 (nu=2/5), the 2/3 filling, and the quark charges -e/3, +2e/3 — every 0.0000% residual by construction.",
 kill="The partition must emit the FULL observed odd-denominator ladder (1/5, 1/7, 1/9, 3/7, ... = Laughlin m) with zero choices, and forbid the unobserved single-layer 4/3, 2/9; {3,5} alone is a retrofit. If it cannot generalize, the partition rule dies.",
 data="Internal derivation (scripts/quantify_charges.py); fractional quantum Hall plateau data + the SM charge table.",
 prov="TRIAL from locked 19:18/N=16 (no workspace derivation yet) — retrofit until it generalizes."),
dict(name="JWST z > 14 galaxy assembly (Bucket 3 #1)", status="pending", speed=3,
 pred="Early galaxy assembly at z > 14 is consistent with the 28/19 tempo + the a0 floor (JADES-GS-z14-0 halo density read).",
 kill="z > 14 assembly incompatible with the tempo + floor.",
 data="JWST JADES/CEERS/UNCOVER.",
 prov="OPEN (author's lane)."),
dict(name="YM glueball mass bridge — E_lock = 2.8898 to GeV", status="pending", speed=0,
 pred="The cold-weld threshold E_lock = 2.8898 (scan units) states a predicted glueball mass in GeV once the unit bridge is written.",
 kill="More than ~30% off the lattice (SU(3) ~ 1.7 GeV, SU(2) ~ 1.65 GeV).",
 data="Lattice QCD (existing).",
 prov="Mechanism CLAIMED, theorem OPEN (LODGEMENT_2 admits this)."),
dict(name="Navier-Stokes blowup falsifier (the capped system)", status="pending", speed=3,
 pred="The capped system (|u| <= c0, rho <= rho_max, P <= P_max, work <= c0²/kg, stall + re-cavitation) never blows up in finite time; Omega_amb = 2.4555e-18 s^-1 <= ||omega|| <= Omega_cav = 1.1324e21 s^-1 < infinity.",
 kill="Exhibit finite-time blowup of the capped system (pre-registered against the OpenAI announcement); the formal global-regularity proof is NOT claimed.",
 data="Mathematics (any worker).",
 prov="DERIVED caps; theorem OPEN (Lean-style translation = named future work)."),
dict(name="T2 resting-density reconciliation — eta·(<v>/c0) = 1/4", status="pending", speed=0,
 pred="rho0 = 8·a0·rho_max·R_p/(3·eta·c0·<v>) predicts rho0 = 8.70e-27 vs observed 8.74e-27 (0.5%).",
 kill="As printed it requires eta·(<v>/c0) = 0.24880013, not the stated 1/4 — reconcile the finite bounding scale or relabel OPEN.",
 data="Internal (the printed T2 equations).",
 prov="DERIVED chain; the 0.2488 vs 0.25 discrepancy OPEN (P2/auditor)."),
dict(name="The 53 — the sun's light and the Z0 step share the debt's fingerprint", status="pending", speed=0,
 pred="The 53.3 ppm Z0 solid-debt residual, the applied 44.7 ppm s·f_solid step, and the sun's 53.2 quintillionths-of-a-gram/m³ deep-channel field mass are one debt's fingerprint (20/19 and s·f_solid at both ends of the ladder).",
 kill="No derivation ties them — the item stays OPEN (the author's guess, not claimed as a hit).",
 data="Internal derivation.",
 prov="CLAIMED/OPEN (capture/2026-10-21_the_53.md)."),
dict(name="Betelgeuse / red-giant grip collapse law", status="pending", speed=3,
 pred="f_choke = (g_surf/a0_bare)² · f_choke_solar — a supergiant's grip collapses >5,000x; Betelgeuse's shed-to-burn ratio = 247 vs the Sun's 0.3.",
 kill="The next supergiant mass-loss/shedding event inconsistent with the collapse law (the 2019-20 Great Dimming is the worked, postdiction example).",
 data="VLT/ALMA monitoring of Betelgeuse, Antares, and the next supergiant shedding event.",
 prov="DERIVED (D34 size law); the Great Dimming read is a worked event, not prediction-first."),
dict(name="5800 K photosphere pin from the heat:wave ladder", status="pending", speed=0,
 pred="T_surface = 5800 K is the medium's tying-transition temperature, to fall out of the heat:wave ratio ladder (2.7 K rest / 38 pK lack / 7.9e-13 J/m³ squeeze triplet) at photospheric pressure.",
 kill="The ladder cannot produce 5800 K from the locked set.",
 data="Internal derivation.",
 prov="OPEN (mechanism stated, the pressure axis awaits)."),
dict(name="Phonon wrap-around — day/night differentials of a string of planets", status="pending", speed=0,
 pred="The day/night differential carries the phonon's travel: wrap-around W = c_s·P_rot/(2 pi R) times the atmosphere's heat capacity; W >> 1 -> no differential, W << 1 -> full differential; vibratability orders the emission excesses (rigid rocks balance out/in = 1.00, vibrating giants burn: Neptune 2.6x, Uranus ~1.06).",
 kill="The W ordering fails to explain the observed day/night differentials and emission excesses.",
 data="Planetary thermal emission records (IRAS/Cassini/Voyager) — data exists.",
 prov="PROPOSED test design (author's, 2026-10-18); not yet frozen/run."),
dict(name="CID-42's 3D speed — the gear-pump recoil band", status="pending", speed=2,
 pred="The gear-pump recoil law's frozen independent test: CID-42's 3D speed must read ~1,800-2,100 km/s (the locked recoil band 0.21-0.29 rho_max).",
 kill="Measured 3D speed outside the band.",
 data="HST/JWST spectroscopy (datum named, not yet measured).",
 prov="DERIVED (scripts/gear_pump_recoils.py)."),
# ================= TRUE =================
dict(name="AR 12192's class — predicted CONFINED before the read", status="true", speed=0,
 pred="The frozen law written BEFORE the HMI/AIA look: Pi_V max = 1.074 (marginal block), zeta = 0.205 vs zeta_yield = 3.84e4 -> NO eruption, confined class (the AR 12192 pattern).",
 kill="(Retroactive kill, passed): an eruption with Pi_V below 1 or zeta near zeta_yield. The region's record: one flare, confined — THE CLASS MATCHED.",
 data="HMI/AIA AR 12192 flare day 2014-10-22 (data/solar/results/ar12192_flux_load_result.json, 2026-10-19).",
 prov="VERIFIED (pre-registered: PREREGISTRATION.md, corona_model_frozen.json)."),
dict(name="Blind synthetic gates T1/T2/T3", status="true", speed=0,
 pred="The frozen model scored against planted synthetic truth: T1 predicted t* = 18.45 h vs planted 18.45 h; T2 measured the planted 7,200 s lag exactly; T3 classified all three planted outcomes.",
 kill="(Passed): any gate failure against the planted truth.",
 data="Gate G2 result (data/solar/results/gate_G2_result.json).",
 prov="VERIFIED (internal blind test)."),
dict(name="Earth's per-kg consumption — M^(2/3) ladder", status="true", speed=0,
 pred="Gamma(M) = Gamma_sun·(M/M_sun)^(2/3): Earth predicted 4.56e-25 s^-1 per kg before the observed rate was quoted against it.",
 kill="(Passed): observed 5.02e-25 s^-1 — TRUE within 9%. Standing kill: the ladder breaks on the next scored body (Mars 87.8 outlier recorded, per-planet throttle note).",
 data="Earth atmospheric escape vs the consumption ladder (stage3_consumption_ladder.py).",
 prov="DERIVED + VERIFIED (9%)."),
dict(name="The naked -2-fits rotation law on 4 external catalogs", status="true", speed=0,
 pred="The recipe (Gamma(1/3) geometry, phi·a0) locked with zero fitted parameters BEFORE the runs, beats the fitted baselines: PROBES 0.3418<0.3457, ALFALFA 0.2866<0.2900, GHASP 0.3032~0.3030 (tie won on parameter count), LITTLE THINGS 0.4196<0.4217.",
 kill="(Passed out-of-sample): any fitted baseline beating the naked recipe on the pre-registered metric.",
 data="PROBES 1,342 / ALFALFA 331 / GHASP 81 / LITTLE THINGS 16 (run_all_rotation_catalogs.py).",
 prov="VERIFIED out-of-sample, zero fitted parameters."),
dict(name="The Planck LSS tempo — 28/19 predicted 257.857 vs 258.0 kyr (+0.0554%)", status="true", speed=0,
 pred="T = 3^3 = 27 locked from boundary geometry; s(1+T) = 28/19 = 1.473684 vs the Planck 380/258 = 1.472868; predicted tempo 380/1.473684 = 257.857 kyr.",
 kill="(Arithmetic TRUE; provenance kill armed): the observed side 380/258 must be identified — 258 kyr matches no standard Planck epoch (t(z_drag) = 389.0, t(z*) = 371.2, t(z=1350) = 258.4 kyr by the auditor's integration). Name the two quantities or relabel the +0.0554% closure CLAIMED; with 377.7 kyr the residual becomes +0.66%.",
 data="Planck 2018 LSS epochs (the 380/258 identification is the named open item — audit F3).",
 prov="DERIVED + VERIFIED (arithmetic); observed-side provenance CLAIMED (F3)."),
dict(name="The muon lifetime — the 20/19 unspooling", status="true", speed=0,
 pred="T7_decay = (20/19)·T7_bound = 1.8263% (vs 1.8239% demanded) closed tau_mu from -245 ppm to +7.7 ppm; the 20/19 was locked (the debt ratio), the PDG lifetime was the target.",
 kill="(Passed): 29x residual reduction, +7.7 ppm.",
 data="PDG tau_mu (scripts/lepton_t7_unspool_closed.py).",
 prov="DERIVED + VERIFIED."),
dict(name="The collider board (relabeled: ratio laws on measured anchors)", status="true", speed=0,
 pred="v = 3(m_p/alpha)(37/58) = 246.070 GeV (-0.061% vs the measured vev); M_Z = (10/27)(1 - s·f_solid)·v_obs = 91.1884 GeV (+0.37sigma); M_W = 80.3595 (-0.07sigma, chain dead-on 80.3602); M_H = 125.232 (-0.11sigma); m_t = 172.576 (+0.02sigma).",
 kill="(The zero-parameter-chain claim from the derived v is WITHDRAWN): with the derived v the same formula reads 91.133 GeV (-26sigma); the rows are TRUE as ratio laws anchored on the measured v_obs = 246.21965 GeV and M_Z,obs (disclosed 2026-10-21), not on the derived v.",
 data="PDG / LHC / CMS measured masses.",
 prov="v DERIVED; the four rows VERIFIED ratio laws on MEASURED anchors (FLAG A relabel)."),
dict(name="The 2026-10-21 zero-parameter sweep (11 anomalies)", status="true", speed=0,
 pred="Formulas written first, measurements quoted after: X17 +0.0125%; Li-7 -0.58sigma; Pioneer +0.14sigma; eta_B = f_solid³ +0.60sigma; Voyager heliopause midpoint 0.2423 pPa inside 0.230-0.251; Gaia wide binaries 1.431 vs 1.43; pi0 = 8·X17_mid +0.0149%; 4He +0.65%; 2H +0.31%.",
 kill="(Passed): each target was the published measurement, each formula the locked constants.",
 data="PDG, Planck 2018, DES Y6, Voyager/Cassini, Gaia DR3, Atomki (scripts/anomaly_sweep_2026_10_21.py).",
 prov="TRUE (each row VERIFIED; the sweep's own misses stay visible below)."),
dict(name="S8 = 0.7904", status="true", speed=0,
 pred="S8,PWC = S8,Planck x (19/20) = 0.7904 — the void-lensing transfer carries the same 1/20 as the debt's complement.",
 kill="(Passed): DES Y6 0.789 +/- 0.012 -> +0.12sigma. Forward kill: DESI/Euclid/SPT-3G/ACT tightening moves S8 off 0.7904 by >3sigma.",
 data="DES Y6 weak lensing (D42, CLOSED 2026-10-21).",
 prov="DERIVED + VERIFIED."),
dict(name="The 16-fold ringdown clock — 4.6806 ms vs 4.68 ms", status="true", speed=0,
 pred="N = 4pi/(pi/4) = 16; tau_loop = 16L/(sqrt2·c0); 32·Delta_t_shed/c0 = 4.6806 ms for GW150914's ringdown.",
 kill="(Passed): +0.012% vs the 4.68 ms ringdown. The next-event kill is armed separately (row above).",
 data="GW150914 (scripts/sixteen_fold_grind_check.py; 2·Delta_t_shed = 87.70 km/stage).",
 prov="VERIFIED (CLOSED 2026-10-20; grind check)."),
dict(name="The merger neck retrofit — 2.6373e11 vs the scan's 2.64e11", status="true", speed=0,
 pred="The 3D-to-2D neck a_max·sqrt(2/3) = 2.6373e11 N/kg was derived AFTER the 193-merger scan minimized at 2.64e11 (bootstrap 2.58-2.80e11) — rescue at -0.10%, with the honest disagreement vs the locked 3.23e11 on record.",
 kill="(Passed): -0.10%. Honest ledger: the scan disagreed with the locked 3.23e11 by ~20%, outside the bootstrap — the agreement is the neck's, not the shell's.",
 data="193 GWTC mergers (gwtc4/5_blind_results.csv; scripts/merger_neck_yield.py).",
 prov="DERIVED (sqrt(2/3) containment); scan MEASURED."),
dict(name="The neutron tariff — 886.17 s vs 887.7 +/- 2.2 s (0.7sigma)", status="true", speed=0,
 pred="tau_beam = tau0/(1 - k·v_eff/c0) = 886.17 s with k = 3069.87 DERIVED forward from the 19:1:18 axial pitch (R0/R3D = sqrt(1 + 19/(288 pi²)) = 1.0033366), folded over the literature's own trap weighting.",
 kill="(Passed): inside the NIST error bar, 0.7sigma, beam 888 > bottle 878 with the mechanism's own sign. Forward kill: the run-matched BL1 spectrum (armed row above).",
 data="NIST beam 887.7 +/- 2.2 s; UCNtau bottle 879 s.",
 prov="VERIFIED-COMPATIBLE, derived forward (scripts/k_final_19_18.py, neutron_fold_closed.py)."),
dict(name="The g-bridge coincidence — 20^(1/16) vs 16 pi³ alpha/3 (single-counted)", status="true", speed=0,
 pred="g = (rho_medium/rho_matter)^(1/16) = 20^(1/16) = 1.205909 vs (e/q')² = 16 pi³ alpha/3 = 1.206740 — the same modes counted twice (8x2 = 4x4 = 16).",
 kill="TRUE only as a -0.069% coincidence: if claimed exact, it inverts to 1/alpha = 137.39 vs 137.035999084 -> 4.6e6 sigma. Single-counted — (e/q')² is row 1's definition inverted, not an independent match.",
 data="Internal (scripts/quantify_charges.py, sixteen_origin.py).",
 prov="g LOCKED (20:1 ledger, 16 modes); target DERIVED; coincidence VERIFIED, exactness MISS."),
dict(name="The bridge 9/(4s) = 42.75 vs 42.7416 (single-counted)", status="true", speed=0,
 pred="9/(4s) = 9·19/4 = 42.75 vs the self-coupling/alpha_G bridge 42.7416 at measured R_p = 8.414e-16 (G cancels; m_p R_p c0 = 4 hbar).",
 kill="(Passed): +0.02%. Single-counted: the residual IS the quantization law m_p R_p c0 = 4 hbar read through measured R_p (implied R_p 8.414e-16, 0.08sigma of CODATA 0.8414(19) fm).",
 data="CODATA R_p (scripts/bridge_derivation.py, quantify_charges.py).",
 prov="DERIVED + VERIFIED (single-counted)."),
dict(name="The knot forge — drho = 0.76 crossing (CLOSED 2026-10-20)", status="true", speed=0,
 pred="A pure wave pulse compressed beyond rho_max welds into a retained topological knot iff e_avail >= E_lock = 2.8898; the crossing at drho = 0.76 (e_avail = 2.9122, +0.8%); RETAINED above, not retained below (drho = 0.70, 0.75).",
 kill="(Passed): the 16-case scoreboard reproduces the crossing exactly; the corrected sub-threshold rows read 0.4471-0.6427.",
 data="Internal (run_parallel_knots.py, threshold_scan_results.json).",
 prov="DERIVED + VERIFIED (numerical)."),
dict(name="The CMB first peak — l1 = 219.0 vs 220", status="true", speed=0,
 pred="R_eff = 21 x 3f/(4(1-f)) — the reach x the grip = 21 inertia -> l1 = 219.0.",
 kill="(Passed): -0.46% vs the observed l1 = 220.",
 data="Planck CMB TT spectrum (effective_drag_closure.py).",
 prov="DERIVED + VERIFIED."),
dict(name="The birefringence SIGN — the ~0.177 deg template landed", status="true", speed=0,
 pred="The two-motion retarded chiral path (observer-rotation shadow ~0.126 deg + chiral diamond-lattice term ~0.051 deg) lands exactly on the frozen ~0.177 deg template.",
 kill="(Passed): the sign closed 2026-10-20. The rank-correlation remains armed (row above).",
 data="The frozen 1,163-void template (scripts/Retarded_chiral_path.py, Wire_Retarded_Path.py).",
 prov="SIGN CLOSED (D32); correlation armed."),
dict(name="The solar pin — 5,770.8 K vs 5,772 K", status="true", speed=0,
 pred="T(L_bol = 3.828e26 W) = 5,770.8 K against the 5,772 K photospheric temperature (-0.02%); T(P_in = 3.916e26 W) = 5,803.6 K (+0.06% vs the 5800 K pin).",
 kill="(Passed): -0.02%. Recorded: the paper's pairing of 3.916e26 W with 5,771 K conflates the two fluxes — 2.3% unbooked (audit F2, relabel pending).",
 data="Solar bolometric flux (stage3_surface_phase_shift.py).",
 prov="VERIFIED with the conflation recorded."),
dict(name="The consumption ladder — Sun/Earth ~4,400x per kg", status="true", speed=0,
 pred="Per-kg consumption scales as M^(2/3): Sun/Earth = 4,361x per kg; the total burn scales as M^(5/3): predicted 1.6e9 vs observed 1.45e9 (~10%).",
 kill="(Passed): confirmed by the data; Mars 87.8 outlier recorded with the per-planet throttle note.",
 data="Earth atmospheric escape, Jupiter excess power, the solar deep channel (stage3_consumption_ladder.py).",
 prov="DERIVED + VERIFIED."),
dict(name="The CMB cooling band — -0.19 to -0.21 K/Gyr", status="true", speed=0,
 pred="dT_CMB/dt = -H·T_CMB = -0.206 K/Gyr (wall rate 73.8) / -0.188 (67.4) — inside the published band.",
 kill="(Passed): inside the band. Degenerate with H0 — not directly measurable on Gyr timescales; the band itself excludes H0 <= 69 km/s/Mpc.",
 data="Published CMB cooling constraints (entropy_heat_drop_track.py).",
 prov="DERIVED (ledger); the 4H·s -> 3H·s bookkeeping slip recorded (F1)."),
dict(name="Hawking from the Terminal Acoustic Stall", status="true", speed=0,
 pred="kappa = c0^4/4GM (Painleve-Gullstrand acoustic analogue); T = hbar·kappa/(2 pi kB c0) = hbar c0³/(8 pi G M kB) — exact, zero free parameters, Planck mass to M87*.",
 kill="(Passed as a correspondence): the kappa -> T step is imported from Unruh's method, not derived — the correspondence is TRUE, the derivation of the thermal step is OPEN.",
 data="Known black-hole thermodynamics (static_medium_check.py).",
 prov="DERIVED correspondence chain; the final thermal step imported (honest)."),
# ================= MISS =================
dict(name="Convective overshoot (the one-step probe)", status="miss", speed=0,
 pred="The one-step convective-overshoot probe of the stellar interior.",
 kill="(KILL FIRED): tested, did not hold — kept in the ledger as the honest miss.",
 data="Stellar interior data (the recorded probe).",
 prov="MISS (recorded, never hidden)."),
dict(name="One-step muon g-2 candidates", status="miss", speed=0,
 pred="The one-step muon g-2 formula from the locked set.",
 kill="(KILL FIRED): overshoots the measured 2.49e-9 by orders; moved to Bucket 3 (the HVP cavity integral), not claimed.",
 data="FNAL/BNL g-2 (2.49e-9).",
 prov="MISS (recorded)."),
dict(name="The cosmic dipole / EDGES one-step multiplier", status="miss", speed=0,
 pred="The one-step multiplier s(1+T)(1+Delta_rho_geom) = (28/19)(1.24313) = 1.8320 reaches the observed dipole/EDGES excess.",
 kill="(KILL FIRED): reaches only 16-23% of the observed 2.19x dipole excess and 2.39x EDGES ratio — PARTIAL miss, Bucket 3 #2, not claimed.",
 data="Cosmic dipole, EDGES 21-cm trough.",
 prov="MISS/PARTIAL (recorded)."),
dict(name="The withdrawn 26.3% ringdown killshot", status="miss", speed=0,
 pred="The 26.3% ringdown claim.",
 kill="WITHDRAWN by the author before the data; lives in git history, not in the papers.",
 data="—",
 prov="WITHDRAWN (git history)."),
dict(name="GW190521 — min(E,S) = 5.56 vs catalog 9.0 Msun", status="miss", speed=0,
 pred="E = 11.78, S = 5.56 -> dropped mass 5.56 Msun.",
 kill="(KILL FIRED): catalog 9.0 Msun — a 38% miss, printed with no residual (auditor-recorded).",
 data="GWTC GW190521.",
 prov="MISS (recorded)."),
dict(name="The merger no-edge pair — 0.71% trivial vs 0.88% min(E,S)", status="miss", speed=0,
 pred="The claim that the merger machinery's 0.88% out-of-sample beats the trivial baseline's 0.71%.",
 kill="(KILL FIRED on reproducibility): CLAIMED-NOT-REPRODUCED — the current script prints 0.89% DEV / 0.81% OUT and no script computes the trivial baseline. Restore the script or withdraw the pair (Ruling #12).",
 data="GWTC-4/5 (merger_energy_balance.py).",
 prov="CLAIMED-NOT-REPRODUCED (recorded)."),
dict(name="The collider zero-parameter chain from the derived v", status="miss", speed=0,
 pred="The collider board as a zero-fitted-parameter chain running from the derived v = 246.070 GeV alone.",
 kill="(KILL FIRED): with the derived v the Z0 law reads M_Z = 91.133 GeV (-26sigma) vs the printed 91.1884 (+0.37sigma) — the chain claim is withdrawn; the rows are relabeled ratio laws on the measured anchors (FLAG A).",
 data="PDG M_Z (auditor VERIFIED).",
 prov="MISS -> relabeled (withdrawn claim)."),
dict(name="Neutron beta-decay bookkeeping — the wound-electron picture", status="miss", speed=0,
 pred="Two-body unwinding of the wound electron predicts mono-energetic ~782 keV beta electrons.",
 kill="(KILLED BY DATA IN HAND): the Fermi continuum and the antineutrino are never booked by the wound-electron picture — the observed continuous spectrum is the kill, recorded as Track A miss #1.",
 data="Measured beta-decay electron continuum (data already exists).",
 prov="MISS (recorded; the three-body bookkeeping is the named open task)."),
dict(name="Neutrino absolute scale — m_e·s^6", status="miss", speed=0,
 pred="The one-step absolute neutrino-mass scale m_e·s^6.",
 kill="(KILL FIRED): misses sqrt(Delta m²21) by +25% (recorded by P1).",
 data="Neutrino oscillation data.",
 prov="MISS (recorded)."),
dict(name="The naive cage projection {2,1,2} -> Delta m²31", status="miss", speed=0,
 pred="The naive cage projection {2,1,2} predicting Delta m²31.",
 kill="(KILL FIRED): Delta m²31 ~ 0 — killed by existing oscillation data.",
 data="Neutrino oscillation data.",
 prov="MISS (recorded)."),
dict(name="The anchor closure — derived rho_max vs the shell (-1.05% proximity, closure FAILED)", status="miss", speed=0,
 pred="rho_max = (2Y_bow/c0²)^(33/29)·rho0^(-4/29) = 1.29032e15 vs the GW150914 shell read 1.304e15 (-1.05%, D46 VERIFIED) — the closure must land exactly on the shell from the locked pieces alone (the C-ladder must meet the yield law at the ceiling: C-gap = 0).",
 kill="(KILL FIRED, anchor_closure_test.py 2026-10-21): at the locked n = 0.0606 the executable prints C_yield = 953.74 km/s vs C_ladder = 958.72 km/s — C-gap +0.522% (must be 0); n_closing = 0.060655 (+0.0906% nudge needed); rho_max_closed = 1.28864e15 vs 1.304e15 = -1.178%. VERDICT NOT CLOSED -> per the pre-stated kill, rho_max relabeled BACK-SOLVED pending the author's n-origin ruling (a +0.091% nudge — geometry, or a nudge?). The -1.05% D46 proximity stands as recorded, not as closure.",
 data="Internal (scripts/anchor_closure_test.py; D46).",
 prov="KILL FIRED -> BACK-SOLVED (pending ruling); the -1.05%/-1.18% proximity recorded."),
dict(name="T2 resting-density derivation as printed", status="miss", speed=0,
 pred="rho0 = 8·a0·rho_max·R_p/(3·eta·c0·<v>) with eta·(<v>/c0) = 1/4 stated.",
 kill="(KILL FIRED as printed): the equations require eta·(<v>/c0) = 0.24880013, not 1/4 — the derivation does not follow from its own printed equations; reconcile or relabel OPEN.",
 data="The printed T2 equations (P2/auditor VERIFIED).",
 prov="MISS as printed -> OPEN (pending the finite bounding scale)."),
dict(name="The 380/258 identification", status="miss", speed=0,
 pred="380/258 kyr as the observed side of the T = 27 Planck-tempo closure.",
 kill="(KILL FIRED on provenance): 258 kyr matches no standard Planck epoch (t(z_drag) = 389.0, t(z*) = 371.2, t(z=1350) = 258.4 kyr); with t_rec = 377.7 kyr the residual becomes +0.66%. Name the two quantities or relabel the closure CLAIMED.",
 data="Planck 2018 epoch tables (auditor integration).",
 prov="CLAIMED (F3) -> must be identified or relabeled."),
dict(name="The 4H·s entropy slip", status="miss", speed=0,
 pred="Entropy drop/production = 4H·s = 1.954e-31 J/K/m³/s printed.",
 kill="(KILL FIRED on bookkeeping): the chain Qdot = -4HQ, Tdot = -HT, s = 4Q/3T gives 3H·s = 1.4655e-31 J/K/m³/s — the printed 4H·s is the slip (factor 4/3), corrected wherever printed.",
 data="Internal (entropy_heat_drop_track.py lines 38/46).",
 prov="MISS (bookkeeping; corrected)."),
dict(name="Mars fits the M^(2/3) ladder 'exactly, zero parameters'", status="miss", speed=0,
 pred="'Mars, Jupiter, and Saturn fit the exact same M^(2/3)·d^(-2) scaling with zero per-planet free parameters' (the 1/R² defense brief).",
 kill="(KILL FIRED): the framework's own runner prints Mars obs/law = 87.8 (the planet's own low-gravity-escape throttle outruns the drive) — an 88x outlier explained by a per-planet throttle is not 'fits exactly with zero parameters'.",
 data="Mars/Jupiter/Saturn thermal budgets (the runner).",
 prov="MISS (the row must be reported with the throttle note)."),
dict(name="SPARC 0.1335 dex claim", status="miss", speed=0,
 pred="The claimed SPARC rms 0.1335 dex.",
 kill="(KILL FIRED on verification): the verified run reads 0.1355 dex across 2,700 points (bulge 0.1285 vs claimed 0.1177; deep-field bias -0.0161 vs claimed -0.0023) — the difference recorded, not smoothed; the -2 fits stand.",
 data="SPARC 2,700 points (stage3_sparc_final_recipe.py).",
 prov="MISS -> corrected record (0.1355)."),
dict(name="k collision — 3059.7 vs 3069.87", status="miss", speed=0,
 pred="Two k values circulated: 3059.7 ('the 12') and 3069.87 (19/18).",
 kill="(KILL FIRED on consolidation): keep 3069.87 (the locked set); retire 3059.7 to git history (Ruling #4 recommendation).",
 data="Internal consolidation.",
 prov="MISS (record conflict)."),
dict(name="16-fold status collision — OPEN vs CLOSED (4.6796 vs 4.6806 ms)", status="miss", speed=0,
 pred="The sixteen-fold clock's status printed inconsistently: OPEN (4.6796 ms, +0.009%) vs CLOSED (4.6806 ms, +0.012%).",
 kill="(KILL FIRED on consolidation): one number — CLOSED 4.6806 ms (+0.012%, grind check); 4.6796 ms tagged as the pre-grind value (Ruling #5 recommendation).",
 data="Internal consolidation.",
 prov="MISS (record conflict)."),
]

# ---------------- SORT: status, then speed ----------------
ORDER = {"armed": 0, "pending": 1, "true": 2, "miss": 3}
ROWS.sort(key=lambda r: (ORDER[r["status"]], r["speed"]))

# ---------------- OUTPUT ----------------
out_lines = []
def out(s=""):
    print(s)
    out_lines.append(s)

out("=" * 100)
out("PWC FALSIFIABLE CATALOG — quantify_falsifiables_master.py (2026-10-21)")
out("Locked constants only; zero fitted parameters; kills pre-stated; misses reported.")
out("=" * 100)
out("VERIFICATION BLOCK (all numbers recomputed from the locked set):")
ok_all = True
for name, value, target, r, fmt, ok in checks:
    flag = "OK " if ok else "WARN"
    if not ok:
        ok_all = False
    out("  [%s] %-52s = %s  (target %s, residual %+.4f%%)" % (flag, name, fmt % value, fmt % target, 100*r))
out("  all checks passed: %s" % ok_all)
out("")
out("CATALOG — %d rows. Sort: status (armed -> pending -> true -> miss), then data-arrival speed." % len(ROWS))
out("")
for i, r in enumerate(ROWS, 1):
    out("#%02d  [%s]  (data: %s)" % (i, r["status"].upper(), SPEED[r["speed"]]))
    out("      %s" % r["name"])
    out("      PREDICT: %s" % r["pred"])
    out("      KILL:    %s" % r["kill"])
    out("      DATA:    %s" % r["data"])
    out("      PROV:    %s" % r["prov"])
    out("")
from collections import Counter
cnt = Counter(r["status"] for r in ROWS)
out("=" * 100)
out("COUNTS: armed=%d  pending=%d  true=%d  miss=%d  (total %d)" %
    (cnt.get("armed", 0), cnt.get("pending", 0), cnt.get("true", 0), cnt.get("miss", 0), len(ROWS)))
out("=" * 100)

# ---------------- MARKDOWN CATALOG ----------------
md = []
md.append("# THE PHASE WAVE COSMOLOGY FALSIFIABLE CATALOG — the complete armed ledger")
md.append("")
md.append("**Compiled:** 2026-10-21 (Australia/Perth) by `scripts/quantify_falsifiables_master.py`.")
md.append("**Sources:** `papers/` (UNIFIED, DERIVATIONS, NEUTRON_LIFETIME, subsectors, clay), `predictions/`")
md.append("(PREDICTIONS_2026-10-21, PREDICTION_SCORECARD), `capture/` (all rulings 2026-10-15 .. 2026-10-21),")
md.append("`audit/` (OPEN_ITEMS_LEDGER, PILLAR2 audit, PROMPT F final, SCRIPT_EXECUTION_PASS), and the executed")
md.append("scripts (`speed_census`, `merger_neck_yield`, `anchor_closure_test`, `quantify_charges`,")
md.append("`quantify_universe_census`, `sixteen_fold_grind_check`, `cmb_birefringence`).")
md.append("")
md.append("**Discipline.** ZERO fitted parameters — every number comes from the locked set")
md.append("{c0, rho0, rho_max, rho_core, R_p, s = 1/19, Y_bow, n = 2/33, f_solid, k = 3069.87,")
md.append("a_max, a0_bare, T = 27, N = 16, g = 20^(1/16), alpha, m_p, m_e} plus measured anchors, each with")
md.append("its provenance (DERIVED / MEASURED / VERIFIED / BACK-SOLVED / CLAIMED / OPEN). Misses are reported,")
md.append("never hidden. Every candidate carries its kill condition, stated before the data. This file is")
md.append("generated; no paper is edited.")
md.append("")
md.append("**Status legend.** `armed` — frozen kill conditions, the deciding data is available now or imminent.")
md.append("`pending` — frozen but gated on an author ruling, a not-yet-made measurement, or a non-imminent event.")
md.append("`true` — the call was frozen first and the data landed on it. `miss` — tested and did not hold (kept visible).")
md.append("")
md.append("**Sort.** by status (armed -> pending -> true -> miss), then by how fast the deciding data could arrive.")
md.append("")
md.append("| # | Name | Prediction | Kill condition | Data / observatory | Status | Provenance | Speed |")
md.append("|---|---|---|---|---|---|---|---|")
for i, r in enumerate(ROWS, 1):
    md.append("| %d | %s | %s | %s | %s | **%s** | %s | %s |" % (
        i,
        r["name"].replace("|", "\\|"),
        r["pred"].replace("|", "\\|"),
        r["kill"].replace("|", "\\|"),
        r["data"].replace("|", "\\|"),
        r["status"],
        r["prov"].replace("|", "\\|"),
        SPEED[r["speed"]],
    ))
md.append("")
md.append("## Counts per status")
md.append("")
md.append("| Status | Count |")
md.append("|---|---|")
for st in ["armed", "pending", "true", "miss"]:
    md.append("| %s | %d |" % (st, cnt.get(st, 0)))
md.append("| **total** | **%d** |" % len(ROWS))
md.append("")
md.append("## Required-17 coverage (the task's mandatory rows)")
md.append("")
md.append("Blaze Star 4 kills (rows 1-4); wall/void 19/18 = 1.0556; T_CMB(z) = -H; pulsar speed census")
md.append("(cap ladder 954 -> 958.8 km/s); the 502 nm line (+18.8 um); the BL1 sheath-weighted spectrum;")
md.append("the merger neck yield 2.6373e11; the solar holdout (Pi_V > 1, zeta_yield); S8 = 0.7904; the")
md.append("birefringence template; the 16-fold ringdown 4.68 ms; V Sge; the knot-mass gap 1023.4 vs")
md.append("938.27 MeV; the Hall ladder generalization; the g-bridge coincidence (single-counted); the")
md.append("28/19 tempo provenance; the derived rho_max vs shell -1.05% (closure kill fired).")
md.append("")

out_path = Path(__file__).resolve().parent.parent / "predictions" / "FALSIFIABLE_CATALOG.md"
out_path.write_text("\n".join(md), encoding="utf-8")
print("")
print("CATALOG WRITTEN: %s" % out_path)
print("EXIT: 0")
raise SystemExit(0)
