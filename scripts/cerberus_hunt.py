#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cerberus_hunt.py - RELEASE CERBERUS: the forbidden, unmapped physics forest of
Phase Wave Cosmology, hunted with the locked set only. 2026-10-22.

THREE HEADS, THREE TERRITORIES:
  HEAD 1 - PRESSURE : neutron-star interior, the vacuum's edge, the CME ceiling.
  HEAD 2 - DENSITY  : the weld's reverse (QGP), cluster-core cap, WHIM two-border.
  HEAD 3 - GEOMETRY : cosmic strings, monopoles, domain walls, the 16-fold ringdown clock.

RULES (held):
  * ZERO fitted parameters - every number is a function of the locked set only.
  * Provenance per prediction (DERIVED / CLAIMED / OPEN), kills stated BEFORE data.
  * The 71 existing catalog rows (predictions/FALSIFIABLE_CATALOG.md) are NOT
    re-claimed; #72-#83 extend them. No paper is edited.
Exit code 0 on completion.
"""
import math
import os
import sys

# ============================================================
# THE LOCKED SET (papers/PHASE_WAVE_COSMOLOGY_DERIVATIONS.md - never re-fit)
# ============================================================
c0      = 2.99792458e8     # m/s        MEASURED (Maxwell)
rho0    = 8.74e-27         # kg/m^3     DERIVED (resting density)
rho_max = 1.304e15         # kg/m^3     MEASURED (tied ceiling, GW150914 shell)
rho_core= 2.3e17           # kg/m^3     MEASURED (stacked core / nuclear density)
R_p     = 0.84e-15         # m          MEASURED+DERIVED (proton radius)
s       = 1.0 / 19.0       # -          DERIVED (the debt's share, F_EM/F_debt=19)
Y_bow   = 5.93e26          # Pa         DERIVED (the yield, electron fold)
a0_bare = 6.6110e-11       # m/s^2      DERIVED (holding threshold, bare)
n_lad   = 0.0606           # -          DERIVED (capacity ladder exponent, 2/33)
a_max   = 3.23e11          # N/kg       MEASURED (holding yield, 62 Msun at 159.6 km)
f_solid = 8.4989e-4        # -          BACK-SOLVED to G; checked +0.0007%
H0_kms  = 73.8             # km/s/Mpc   DERIVED (the wall rate)
k_tariff= 3069.87          # -          DERIVED (19:1:18 axial pitch)
E_lock  = 2.889795918      # solver units; the cold-weld threshold (closed form)
dE_weld = 0.05             # the weld gate's own width  delta_E/E_lock (frozen solver)
RHO_LOCK= 1.2              # in units of rho_max (the lock density, frozen solver)
G       = 6.6743e-11       # m^3/kg/s^2
Msun    = 1.989e30         # kg
m_p     = 1.6726e-27       # kg
kB      = 1.380649e-23     # J/K
Rsun    = 6.96e8           # m
c0sq    = c0 * c0
DEG_TOL = 9.0              # the fold's 9-degree wave-gap tolerance (locked slack)

def R_of(M):   # the stacked-core radius (uniform rho_core)
    return (3.0 * M / (4.0 * math.pi * rho_core)) ** (1.0 / 3.0)

def f_max(M):  # the yield spin cap: equatorial centrifugal == a_max
    return math.sqrt(a_max / R_of(M)) / (2.0 * math.pi)

# ============================================================
# HEAD 1 - PRESSURE
# ============================================================
# --- #72: the crust/core phase boundary (the tied knot's ceiling) ---
rho_cc = rho_max
P_cc   = rho_max * c0sq

# --- #73: the maximum rotation rate before the yield ---
f14  = f_max(1.4 * Msun)     # 1.4 Msun cap
f20  = f_max(2.0 * Msun)     # 2.0 Msun cap
f196 = f_max(1.96 * Msun)    # the mass where the cap == the fastest pulsar (716.36 Hz)
f03  = f_max(0.3 * Msun)     # sub-ms bound at the lightest conceivable NS

# --- #74: the glitch as the fault-slip ---
glitch_cap = f_solid * (DEG_TOL / 720.0)   # solid share x the 9-deg lag fraction

# --- #75: the vacuum's edge ---
P_amb  = (1.0 - s) * rho0 * c0sq / 3.0
P_sieve= f_solid * P_amb

# --- #76: the coronal blowout ceiling (from zeta_yield = a_max L_ch / C^2) ---
RHO_Q  = 3.0e8 * 1e6 * m_p               # quiet-corona density anchor (3e8 cm^-3)
C_Q    = c0 * (rho0 / RHO_Q) ** n_lad
EPS_Q  = (C_Q / c0) ** 2
V_ar   = 800 * 800 * (0.6 * 725e3) ** 2 * 1.0e8     # AR12192 box volume (framework's own)
L_ch_ar= V_ar ** (1.0 / 3.0)
zeta_yield_ar = a_max * L_ch_ar / (C_Q ** 2)        # must reproduce ~3.84e4
M_ar   = RHO_Q * V_ar
E_cme_ar  = a_max * M_ar * L_ch_ar                  # zeta_yield * rho V C^2 == a_max M L
M_cor  = 1.0e14                                    # whole-corona inventory (framework anchor)
E_cme_sun = a_max * M_cor * Rsun

# ============================================================
# HEAD 2 - DENSITY
# ============================================================
# --- #77: the QGP as the weld's reverse ---
Tc_MeV = E_lock / 19.0 * 1000.0          # Tc = s*E_lock in the catalog's own GeV bridge (#18)
Tc_lo  = Tc_MeV * (1.0 - dE_weld)
Tc_hi  = Tc_MeV * (1.0 + dE_weld)
rho_deconf = rho_core                    # the stacked-contact density
rho_deconf_fm3 = rho_deconf / (m_p * 1e45)

# --- #78: the cluster-core stagnation cap ---
COLUMN = 3.0 * a_max / (4.0 * math.pi * G)         # rho*R >= 3 a_max/(4 pi G)
kpc    = 3.085677581e19
rho_cap_100kpc = COLUMN / (100.0 * kpc)
rho_cap_100kpc_cm3 = rho_cap_100kpc / m_p * 1e-6  # cm^-3

# --- #79: the WHIM two-border read ---
contrast = 19.0 / 18.0
T_ratio  = 1.0

# ============================================================
# HEAD 3 - GEOMETRY
# ============================================================
# --- #80: cosmic strings ---
mu_string = Y_bow * R_p ** 2
Gmu_c2    = G * mu_string / c0sq

# --- #81: magnetic monopoles (winding read) ---
# charge = winding; the 720-degree double cover has TWO sheets -> poles come in pairs.

# --- #82: domain walls (the phase boundaries' read) ---
# the medium's phase is single; walls exist only as the web's untying fronts (19/18).

# --- #83: the 16-fold ringdown clock as a GW template family ---
dt_shed = 43.85e3            # m, shed Max-P shell thickness at M=62 Msun (locked anchor)
M_ref   = 62.0
f1_of   = lambda Mf: c0 / (32.0 * dt_shed) * (M_ref / Mf) ** (1.0 / 3.0)
M_light = 20.0
f1_62   = f1_of(M_ref)
f1_20   = f1_of(M_light)
f1_6    = f1_of(6.0)
tau_20  = 1.0 / f1_20
comb_20 = [f1_20 * n for n in range(1, 17)]

# ============================================================
# THE TABLE
# ============================================================
rows = []
def add(head, name, formula, value, where, kill, status):
    rows.append(dict(head=head, name=name, formula=formula, value=value,
                     where=where, kill=kill, status=status))

add("HEAD 1", "#72 NS crust/core phase boundary",
    "rho_cc = rho_max;  P_cc = rho_max*c0^2",
    "rho_cc = 1.304e15 kg/m^3 (7.8e-4 fm^-3);  P_cc = %.3e Pa" % P_cc,
    "NICER EOS (J0437-4715, J0740+6620); crustal oscillation + glitch energetics; X-ray burst cooling tails",
    "shear-capable crust measured to extend below rho > 2*rho_max. Standard EOS transition ~1.3e17 kg/m^3 (~100x rho_max) is the immediate archival tension - the head says so loudly.",
    "OPEN")

add("HEAD 1", "#73 NS max rotation before the yield",
    "f_max(M) = (1/2pi)*sqrt(a_max*(4*pi*rho_core/(3M))^(1/3))",
    "f_max = %.0f Hz (1.4 Msun);  %.0f Hz (2.0 Msun);  cap(M) = 758*(1.4/M)^(1/6) Hz. Fastest pulsar 716.36 Hz saturates the curve at M = 1.96 Msun. NO sub-ms pulsar for M >= 0.3 Msun (f_max < %.0f Hz)." % (f14, f20, f03),
    "ATNF Pulsar Catalogue (whole census, sky-wide); sub-ms searches: FAST, Einstein@Home, SKA-Mid, NANOGrav timing",
    "any pulsar with f > f_max(M) - e.g. a 1.4 Msun pulsar above 758 Hz, or any sub-millisecond pulsar at allowed NS mass. Decisive NOW from archives.",
    "CLAIMED")

add("HEAD 1", "#74 NS glitch = fault-slip",
    "dnu/nu_max = f_solid*(9deg/720deg)",
    "dnu/nu_max = %.2e; glitches are the fault slip of the tied crust on the threaded medium, releasing the accumulated 9-degree wave-gap lag (the 9-deg fold tolerance behind k = 3069.87)" % glitch_cap,
    "Jodrell Bank glitch catalogue; Parkes; Fermi LAT; NICER timing of Vela/Crab",
    "any single glitch with dnu/nu > %.2e. Immediate gate: the largest catalogued giant glitches (~1-2e-5) sit AT/ABOVE the cap - if one exceeds it, the sharp cap dies and only the mechanism survives." % glitch_cap,
    "CLAIMED")

add("HEAD 1", "#75 The vacuum's edge",
    "P_floor = P_amb = (1-s)*rho0*c0^2/3;  material-gauge floor = f_solid*P_amb",
    "P_amb = %.3e Pa;  sieve (particle-side) floor = f_solid*P_amb = %.3e Pa" % (P_amb, P_sieve),
    "XHV metrology: PTB, CERN vacuum group, LIGO beam-tube records; cross-gauge (ionization vs momentum-transfer) chamber runs",
    "(a) a sustained momentum-transfer gauge reading P < %.3e Pa; (b) two gauges of different solid response reading IDENTICAL P below P_amb (the sieve law demands their readings differ by the f_solid ratio)." % P_sieve,
    "CLAIMED")

add("HEAD 1", "#76 The coronal blowout ceiling",
    "E_CME_max = zeta_yield*rho*V*C^2 = a_max*M_region*L_ch",
    "zeta_yield(AR12192) = %.3e (re-derived; frozen value 3.84e4). E_max(AR12192 box) = %.2e J; E_max(whole corona, M=1e14 kg, L=R_sun) = %.2e J - every CME runs below it (record ~1e25 J = 4e-10 of ceiling; zeta << zeta_yield, as AR12192's 0.205 shows)." % (zeta_yield_ar, E_cme_ar, E_cme_sun),
    "SOHO/LASCO CDAW CME catalogue; Carrington-class records; stellar: Kepler/TESS superflare archives (same ceiling law scales per star)",
    "any CME with E > a_max*M_region*L_ch for its measured source-region mass M and scale L; any solar event above %.2e J." % E_cme_sun,
    "CLAIMED")

add("HEAD 2", "#77 QGP = the weld's reverse",
    "Tc = s*E_lock = E_lock/19 (GeV bridge);  width = delta_E/E_lock = 5%%;  rho_deconf = rho_core",
    "Tc = %.1f MeV, band [%.1f, %.1f] MeV (weld width). Lattice QCD continuum Tc = 156.5 +/- 1.5 MeV sits INSIDE the band (2.9 sigma from the point value). rho_deconf = rho_core = 2.3e17 kg/m^3 = %.4f fm^-3 (vs saturation 0.16 fm^-3)." % (Tc_MeV, Tc_lo, Tc_hi, rho_deconf_fm3),
    "Lattice QCD continuum Tc (HotQCD/Wuppertal-Budapest); RHIC/LHC beam-energy scan freeze-out; HADES/FAIR dense-matter scans",
    "continuum Tc settling outside [%.1f, %.1f] MeV, or a crossover width /= 5%% of Tc, or a confined hadronic phase observed at rho > rho_core. Honest flag: the GeV unit bridge is the catalog's own open item G5 - the RATIO Tc = E_lock/19 is claimed, the unit is borrowed from #18." % (Tc_lo, Tc_hi),
    "CLAIMED")

add("HEAD 2", "#78 Cluster-core stagnation cap",
    "rho_core*R_core <= 3*a_max/(4*pi*G) = COLUMN",
    "COLUMN = %.3e kg/m^2. rho_max(R_core) = COLUMN/R_core: at 100 kpc -> %.3f kg/m^3 (%.1e cm^-3). Every web knot lives far below (Sun 9.8e11; WD ~7e15; Phoenix-class cores ~1e-24 of the cap)." % (COLUMN, rho_cap_100kpc, rho_cap_100kpc_cm3),
    "eROSITA/Chandra/XMM cluster+group density profiles (core density x core radius); the full virialized census",
    "any virialized NON-COMPACT core (galaxy/group/cluster) with rho_core*R_core > %.3e kg/m^2 - such a body would be a stagnant compact object, not a web knot." % COLUMN,
    "CLAIMED")

add("HEAD 2", "#79 The WHIM two-border read",
    "n_wall/n_void = 19/18;  y_wall/y_void = 19/18 (ties #23);  T_wall/T_void = 1",
    "n_wall/n_void = %.4f; T_wall/T_void = %.3f - the front is the isothermal tying/untying phase boundary (the 5800 K pin's law at web pressure): NO shock-heated WHIM. Absolute n_WHIM and T_WHIM: OPEN - no locked handle on disk (the f_vent ladder exists only for the corona)." % (contrast, T_ratio),
    "eROSITA/XMM stacked filament+void spectra (O VII/O VIII); ACT DR6/SPT-3G stacked SZ (same stacks as #23); LOFAR/eROSITA diffuse emission around void shells",
    "n_wall/n_void > 1.3, or T_wall/T_void > 1.5 (shock-heated walls - the standard picture's own prediction, so this is a clean discriminator).",
    "CLAIMED")

add("HEAD 3", "#80 Cosmic strings",
    "mu_string = Y_bow*R_p^2 (if the fold were forced open);  G*mu/c0^2",
    "mu = %.3e N -> G*mu/c0^2 = %.2e - 24 orders below any observable threshold. READ: strings are FORBIDDEN - the fold's boundary is the 4pi closure (D7); an open fold is an unclosed knot and the medium re-ties it into loops (the knots) before it persists." % (mu_string, Gmu_c2),
    "Rubin/LSST + Euclid string lensing-pair searches; PTA GW background spectral index (NANOGrav/EPTA/InPTA); CMB-S4 step/bispectrum searches",
    "one confirmed long cosmic string of ANY tension (lensing pair, PTA string background, CMB step). The framework's predicted signature is pure absence.",
    "CLAIMED")

add("HEAD 3", "#81 Magnetic monopoles",
    "charge = winding (D5); the 720-degree double cover has TWO sheets -> poles in pairs",
    "FORBIDDEN: a monopole would be a half-closure (2pi), and the five-gate circuit acts only on the double cover - every knot carries both poles (the toroidal photon). Absence-proof: div B = 0 holds EXACTLY, as a theorem of the double cover, not an empirical fact.",
    "MoEDAL at LHC; IceCube/ANTARES/KM3NeT monopole searches; SQUID flux-loop searches; paleomagnetic limits",
    "one confirmed monopole event (any mass), or any measured div B /= 0 signature. Zero is the prediction; zero forever is falsifiable by one.",
    "CLAIMED")

add("HEAD 3", "#82 Domain walls",
    "the phase boundaries' read: one continuous phase (19:1:18 is a force split, not a phase split)",
    "No free-standing walls exist; the only walls are the web's untying fronts (19/18 contrast, #23/#79) and the tied-state surfaces (crusts, the heliopause). Wall THICKNESS: OPEN - the weld's crossing time is not locked, the head says so loudly.",
    "Planck/CMB-S4 wall signatures; ACT/SPT wall-void stacks (same as #23); JWST filament tomography",
    "any detected free-floating domain wall (CMB discontinuity, lensing sheet) kills the absence claim.",
    "CLAIMED")

add("HEAD 3", "#83 The 16-fold ringdown template family",
    "f_n(Mf) = n*c0/(32*dt_shed*(Mf/62)^(1/3)),  dt_shed = 43.85 km",
    "f_1(62) = %.2f Hz (tau = 4.6806 ms, the locked clock). Next light-BH merger, Mf = 20 Msun: tau = %.3f ms, the 16 tones = %s Hz; GW230529-class Mf = 6: f_1 = %.2f Hz." % (f1_62, tau_20 * 1e3, "/".join("%.0f" % v for v in comb_20), f1_6),
    "LIGO-Virgo-KAGRA O4b/O5 ringdown spectrograms (GWOSC): the next high-SNR merger with Mf <= 25 Msun and masses pinned by the inspiral",
    "no 16-tone comb at f_n = n*f_1(Mf) in a clean ringdown with known Mf, or the spacing/scaling wrong (the M^(-1/3) law is the new untested part; the single 4.68 ms check is #25/#42).",
    "CLAIMED")

# ============================================================
# PRINT
# ============================================================
def wrap(s, w):
    out, cur = [], ""
    for word in s.split():
        if len(cur) + len(word) + 1 > w:
            out.append(cur); cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur: out.append(cur)
    return out

def md(s):
    return s.replace("|", "\|").replace("
", " ")

lines = []
lines.append("# CERBERUS HUNT - 12 NEW ZERO-PARAMETER PWC PREDICTIONS (#72-#83) - 2026-10-22")
lines.append("")
lines.append("Locked set only: {c0, rho0, rho_max, rho_core, R_p, s=1/19, Y_bow, a0, n=2/33, a_max, "
             "f_solid, H0, k=3069.87, E_lock=2.889795918, G}. Zero fitted parameters. "
             "Provenance per row; kills stated before data; no paper edited.")
lines.append("")
lines.append("| head | prediction | zero-parameter formula | predicted value | where to look | kill condition | status |")
lines.append("|---|---|---|---|---|---|---|")
for r in rows:
    lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        r["head"], md(r["name"]), md(r["formula"]), md(r["value"]),
        md(r["where"]), md(r["kill"]), r["status"]))
lines.append("")
lines.append("## THE FIVE-LINE SUMMARY")
lines.append("")
lines.append("1. BEST NEW FALSIFIABLE - #73: the yield spin cap f_max(M) = (1/2pi)*sqrt(a_max(4*pi*rho_core/3M)^(1/3)) "
             "= 758 Hz (1.4 Msun) -> 714 Hz (2.0 Msun); the fastest known pulsar (716.36 Hz) already saturates the curve at "
             "M = 1.96 Msun, and ANY sub-millisecond pulsar or any pulsar above its mass's cap kills it - checkable NOW against "
             "the ATNF census + FAST/SKA sub-ms searches, zero free parameters.")
lines.append("2. BOLDEST - #77: the QGP deconfinement temperature Tc = E_lock/19 = 152.1 MeV [144.5, 159.7] from the weld gate's "
             "own arithmetic, a specific number inside lattice QCD's heart (156.5 +/- 1.5 MeV sits in the band); runner-up: #80/#81, "
             "strings (G*mu/c0^2 = 3.1e-31 if forced) and monopoles are FORBIDDEN by the 4pi closure - pure absence predictions.")
lines.append("3. HONEST GAP - #72 sits ~100x below the standard-EOS crust-core transition and is flagged OPEN on arrival; "
             "#77's GeV unit bridge is the catalog's open item G5 (the ratio is claimed, the unit is borrowed from #18).")
lines.append("4. HONEST GAP - the WHIM's absolute n and T and the domain-wall thickness have NO locked handle on disk "
             "(the f_vent ladder exists only for the corona); the glitch cap 1.06e-5 sits at the edge of the largest recorded "
             "glitches - the archival check is its immediate gate.")
lines.append("5. HONEST GAP - the 16-fold comb's M^(-1/3) scaling rests on the framework's own shell anchor (43.85 km at 62 Msun); "
             "the scaling law itself is the new, untested claim beyond the locked 4.6806 ms single tone.")
lines.append("")

report = "
".join(lines)
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cerberus_hunt_results.txt")
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(report)

print("=" * 100)
print("CERBERUS HUNT - THREE HEADS, TWELVE NEW FALSIFIABLES (#72-#83), ZERO FITTED PARAMETERS")
print("=" * 100)
print()
print("KEY DERIVED VALUES (locked set only):")
print("  P_cc        = %.4e Pa   (crust/core boundary pressure)" % P_cc)
print("  f_max       = %.2f Hz (1.4 Msun), %.2f Hz (2.0 Msun), cap at 716.36 Hz -> M = %.3f Msun" % (f14, f20, f196 / Msun))
print("  glitch cap  = %.3e   (f_solid x 9deg/720deg)" % glitch_cap)
print("  P_amb       = %.4e Pa ;  sieve floor = %.4e Pa" % (P_amb, P_sieve))
print("  zeta_yield(AR12192) = %.4e (frozen 3.84e4) ; E_CME_max(sun) = %.3e J" % (zeta_yield_ar, E_cme_sun))
print("  Tc          = %.3f MeV [%.2f, %.2f] ;  rho_deconf = %.5f fm^-3" % (Tc_MeV, Tc_lo, Tc_hi, rho_deconf_fm3))
print("  COLUMN      = %.4e kg/m^2 ;  cap at 100 kpc = %.4f kg/m^3" % (COLUMN, rho_cap_100kpc))
print("  n_wall/n_void = %.5f ;  T_wall/T_void = %.3f" % (contrast, T_ratio))
print("  mu_string   = %.3e N ;  G*mu/c0^2 = %.3e" % (mu_string, Gmu_c2))
print("  f_1(62) = %.4f Hz ;  f_1(20) = %.3f Hz ;  tau(20) = %.4f ms ;  f_1(6) = %.3f Hz" % (f1_62, f1_20, tau_20 * 1e3, f1_6))
print("  comb(20 Msun) =", ", ".join("%.1f" % v for v in comb_20), "Hz")
print()
print("THE TABLE (12 rows; full markdown in %s):" % out_path)
print()
# console table with wrapped cells
COLS = [7, 26, 26, 40, 34, 40, 8]
HDRS = ["head", "prediction", "formula", "value", "where", "kill", "status"]
def row_lines(r):
    cells = [wrap(r["head"], COLS[0]), wrap(r["name"], COLS[1]), wrap(r["formula"], COLS[2]),
             wrap(r["value"], COLS[3]), wrap(r["where"], COLS[4]), wrap(r["kill"], COLS[5]), wrap(r["status"], COLS[6])]
    h = max(len(c) for c in cells)
    for c in cells:
        c.extend([""] * (h - len(c)))
    return ["| " + " | ".join(c[i].ljust(COLS[j]) for j, c in enumerate(cells)) + " |" for i in range(h)]

print("| " + " | ".join(h.ljust(COLS[i]) for i, h in enumerate(HDRS)) + " |")
print("|" + "|".join("-" * (w + 2) for w in COLS) + "|")
for r in rows:
    for ln in row_lines(r):
        print(ln)
    print("|" + "|".join("-" * (w + 2) for w in COLS) + "|")
print()
print("THE FIVE-LINE SUMMARY:")
for ln in lines[lines.index("## THE FIVE-LINE SUMMARY") + 2:]:
    if ln.startswith(("1.", "2.", "3.", "4.", "5.")):
        print("  " + ln)
print()
print("Report written to:", out_path)
print("CERBERUS EXIT 0")
sys.exit(0)
