"""
quantify_astro_falsifiables.py -- the eight astrophysical falsifiables of Phase Wave Cosmology.
Compiled 2026-10-21 from the frozen record on disk: the prediction scorecard, the frozen
predictions file, the PROMPT-F ruling capture, and the verified scripts. Nothing here edits papers.

RULES (enforced by construction):
  - ZERO fitted parameters: every number is a LOCKED constant or a composition of the locked set.
  - Provenance per number: each LOCKED/DERIVED label below names its origin.
  - Misses reported, never hidden: the MISSES block prints every on-record miss/caveat.
  - Kill condition per candidate: one per table row, pre-stated in the frozen record.
  - Exit 0 (this script only reports; it never raises).

Reads (row counts only): scripts/gwtc4_blind_results.csv, scripts/gwtc5_blind_results.csv.
"""
import csv, math, os, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# LOCKED SET (provenance per number; the task's locked list)
# ----------------------------------------------------------------------
c0      = 2.99792458e8      # LOCKED  CODATA exact
G       = 6.67430e-11       # LOCKED  CODATA 2018
hbar    = 1.054571817e-34   # LOCKED  CODATA 2018
kB      = 1.380649e-23      # LOCKED  SI exact
rho0    = 8.74e-27          # LOCKED  MEASURED cosmic census (Ruling #9 relabel: rho0 is the observed input)
rho_max_shell   = 1.304e15  # LOCKED  BACK-SOLVED from GW150914's 47.3->159.6 km shell read (Ruling #9)
rho_max_derived = 1.29032e15# LOCKED  DERIVED fold closure (2Y_bow/c0^2)^(33/29)*rho0^(-4/29),
                            #         DERIVATIONS.md L868; -1.05% vs the shell read (VERIFIED there)
rho_core = 2.3e17           # LOCKED  neutron-density merger core (Step 2 of the chain)
s        = 1.0/19.0         # LOCKED  the 19:1:18 partition
Y_bow    = 5.9307e26        # LOCKED  RBH-1 bow anchor: Y = 0.5*rho_max*v_bow^2
n_locked = 2.0/33.0         # LOCKED  closure exponent
f_solid  = 8.4989e-4        # LOCKED  solid share
a_max    = 3.23e11          # LOCKED  BACK-SOLVED shell edge (62 Msun at 159.6 km, GW150914)
N16      = 16               # LOCKED  4 quanta x 4 spinor states (the 16 harmonic modes)
T27      = 27               # LOCKED  3^3 boundary tightening
H0       = 73.935           # LOCKED  k-bridge value
Msun     = 1.989e30         # LOCKED  solar mass

phi = (1.0 + math.sqrt(5.0)) / 2.0          # the golden ratio (geometry)

# DERIVED (recomputed here from the locked set, never assigned):
a0_bare = (c0/math.sqrt(3.0))*math.sqrt(G*rho0/4.0)   # DERIVED  -> 6.6110e-11 (locked table)
a0_knee = phi*a0_bare                                  # DERIVED  -> 1.0695e-10 (one named choice: phi)
drho_geom = (1.5*math.gamma(1.0/3.0) - 3.0)/(4.0*math.pi/3.0)  # DERIVED Gamma(1/3) geometry -> +0.24313
a_max_neck = a_max*math.sqrt(2.0/3.0)                  # DERIVED  sqrt(2/3)*3.23e11 -> 2.6373e11

def v_cap(rho):
    """the cap ladder: v = sqrt(2 Y_bow / rho), capped at c0 (less dense = more speed up to c0)."""
    return min(c0, math.sqrt(2.0*Y_bow/rho))

def pct(a, b):
    return 100.0*(a/b - 1.0)

# ----------------------------------------------------------------------
# 1. THE PULSAR SPEED CENSUS (B1508+55 vs the cap ladder; K1-K3)
# ----------------------------------------------------------------------
def section1():
    vp, up, dn = 1083.0, 103.0, 90.0          # PSR B1508+55 transverse speed km/s (VLBA parallax;
                                              # scripts/cavitation_speed_limit.py L22; the frozen census)
    cap_shell   = v_cap(rho_max_shell)/1e3    # 953.7 km/s (printed "954" in the papers)
    cap_derived = v_cap(rho_max_derived)/1e3  # 958.8 km/s (the DERIVED ceiling)
    cap_loose_raw = math.sqrt(2.0*Y_bow/rho0)/1e3  # raw formula ~3.7e23 km/s = 1.2e15 c0
    cap_loose   = v_cap(rho0)/1e3             # -> capped at c0
    rho_x       = 2.0*Y_bow/c0**2             # crossover density: below this, v_cap = c0
    sig_up      = (vp - 954.0)/up             # +1.25 sigma over the shell cap (the papers' "954")
    sig_up_der  = (vp - cap_derived)/up       # +1.21 sigma over the derived ceiling
    sig_req     = (vp - 954.0)/5.0            # K1 needs v - 5sig > 954 -> sig_v <= 25.8 km/s
    print("== 1. PULSAR SPEED CENSUS: B1508+55 vs the cap ladder ==")
    print("   cap ladder v_cap = sqrt(2 Y_bow / rho), capped at c0 (less dense = more speed, up to c0):")
    print("     shell ceiling  rho_max 1.304e15  -> %.2f km/s   (papers print 954; C_yield on record)" % cap_shell)
    print("     derived ceiling rho_max 1.29032e15 -> %.2f km/s  (the DERIVED value)" % cap_derived)
    print("     loose medium  rho0 8.74e-27 -> raw %.2e km/s (%.1e c0) -> capped at c0; crossover rho_x = 2Y_bow/c0^2 = %.4e kg/m^3" % (cap_loose_raw, cap_loose_raw/c0, rho_x))
    print("   B1508+55: 1083 (+103/-90) km/s  ->  +%.2f sigma over 954;  +%.2f sigma over %.1f" % (sig_up, sig_up_der, cap_derived))
    print("   K1 decisive read needs v - 5sig > 954  ->  sig_v <= %.1f km/s (ruling: ~26 km/s); current +103/-90 is too coarse" % sig_req)
    for name, v, expect in (("B1508+55", 1083e3, 0.775), ("CID-42", 1770e3, 0.290), ("3C 186", 2100e3, 0.206)):
        r_eff = 2.0*Y_bow/v**2
        print("   K3 check %-9s rho_eff = 2Y_bow/v^2 = %.4e = %.3f rho_max(shell)  (record %.3f; all <= rho_max -> no kill)"
              % (name, r_eff, r_eff/rho_max_shell, expect))
    print("   K2 check: no confirmed medium bow below 0.9 C_own in the census -> no kill (ruling TEST 2).")
    print("   VERDICT: INCONCLUSIVE (not failed, not passed) - K1 pending astrometry, K2/K3 clean.\n")

# ----------------------------------------------------------------------
# 2. GAIA WIDE BINARIES: G_eff/G midpoint vs 1.43 +/- 0.06 (CLOSED)
# ----------------------------------------------------------------------
def section2():
    band_lo = 1.0 + drho_geom                       # 1.2431  (the Gamma(1/3) geometry share)
    band_hi = phi                                   # 1.6180  (the same phi as a0 = phi*a0_bare)
    mid     = 0.5*(band_lo + band_hi)               # 1.4306 -> printed 1.431
    tgt, err = 1.43, 0.06
    dev = (mid - tgt)/err
    print("== 2. GAIA WIDE BINARIES: G_eff/G ==")
    print("   band  = [1 + drho_geom, phi] = [%.4f, %.4f]  (drho_geom = (1.5*Gamma(1/3) - 3)/(4*pi/3) = %+.5f)" % (band_lo, band_hi, drho_geom))
    print("   midpoint = %.5f -> printed 1.431  vs target 1.43 +/- 0.06  ->  %+.2f sigma" % (mid, dev))
    print("   VERDICT: CLOSED (scorecard TRUE #8, the 2026-10-21 sweep). Caveat on record: the published")
    print("   '1.43 +/- 0.06' source is unnamed in the papers - pin it before the >=3sigma re-test.\n")

# ----------------------------------------------------------------------
# 3. MERGER min(E,S) + NECK YIELD: a_max,neck = sqrt(2/3)*3.23e11 (PENDING)
# ----------------------------------------------------------------------
def section3():
    a_scan = 2.64e11                               # 193-merger empirical scan minimum (bootstrap 2.58-2.80e11)
    n4 = n5 = None
    try:
        with open(os.path.join(HERE, "gwtc4_blind_results.csv")) as fh:
            n4 = sum(1 for _ in csv.reader(fh)) - 1
        with open(os.path.join(HERE, "gwtc5_blind_results.csv")) as fh:
            n5 = sum(1 for _ in csv.reader(fh)) - 1
    except OSError as e:
        print("   [csv read failed: %s - counts reported as claimed 89/104]" % e)
    n4 = 89 if n4 is None else n4
    n5 = 104 if n5 is None else n5
    ntot = n4 + 5 + n5
    print("== 3. MERGER min(E,S) WITH THE NECK YIELD ==")
    print("   a_max,neck = sqrt(2/3) * a_max = %.4e N/kg  (3D shell -> 2D transverse neck projection)" % a_max_neck)
    print("   %d mergers = %d on-disk (gwtc4) + 5 named (GW150914/GW190521/GW170104/GW170814/GW151226) + %d on-disk (gwtc5)" % (ntot, n4, n5))
    print("   vs the %d-merger scan minimum %.2e  ->  %+.2f%%   (bootstrap 2.58-2.80e11)" % (ntot, a_scan, pct(a_max_neck, a_scan)))
    E1 = math.sqrt(G*36.0*Msun/a_max_neck)
    E2 = math.sqrt(G*29.0*Msun/a_max_neck)
    E_neck = G*(36.0*Msun)*(29.0*Msun)/(2.0*c0**2*(E1+E2))/Msun
    print("   GW150914 E-limit at the neck yield = %.3f Msun vs catalog 3.0 Msun -> %+.1f%%" % (E_neck, pct(E_neck, 3.0)))
    print("   VERDICT: PENDING (armed). Kill: the light-event E-limit lands on the 3.23e11 curve, not the neck.")
    print("   Honest boundary on record: the no-edge pair 0.71%/0.88% is CLAIMED-NOT-REPRODUCED (Ruling #12);")
    print("   GW190521 min(E,S) = 5.56 vs catalog 9.0 Msun (38% miss, recorded).\n")

# ----------------------------------------------------------------------
# 4. HAWKING TEMPERATURE: T = hbar c0^3 / (8 pi G M kB) - reproduced exactly
# ----------------------------------------------------------------------
def section4():
    print("== 4. HAWKING TEMPERATURE ==")
    print("   sonic choke: kappa = (1/2)|d(c0^2 - v^2)/dr| at r_s, v^2 = 2GM/r  ->  kappa = c0^4/(4GM)")
    print("   T = hbar*kappa/(2*pi*kB*c0) = hbar*c0^3/(8*pi*G*M*kB).  Zero free parameters.")
    worst = 0.0
    for M_msun in (1.0, 62.0, 4.3e6):
        Mkg = M_msun*Msun
        T_direct = hbar*c0**3/(8.0*math.pi*G*Mkg*kB)
        kappa = c0**4/(4.0*G*Mkg)
        T_kappa = hbar*kappa/(2.0*math.pi*kB*c0)
        rel = abs(T_direct - T_kappa)/T_direct
        worst = max(worst, rel)
        print("   M = %-9g Msun  T = %.4e K   (kappa-route vs direct: rel diff %.1e)" % (M_msun, T_direct, rel))
    print("   the lengthening matters: without the radial lengthening T_flat = 2 x Hawking (static_medium_check.py).")
    print("   VERDICT: CLOSED as an exact reproduction (identity, rel diff %.1e). It is a derivation closure," % worst)
    print("   not an armed observation - no feasible dataset measures a BH temperature; recorded as such.\n")

# ----------------------------------------------------------------------
# 5. RBH-1 AT 0.996 OF THE CAP (the bow; the bow law's anchor)
# ----------------------------------------------------------------------
def section5():
    v_rbh = 950e3
    C_own = v_cap(rho_max_shell)
    ratio = v_rbh/C_own
    thresh = 0.9*C_own
    print("== 5. RBH-1: 950 km/s vs C(rho_max) = %.1f km/s -> %.3f of the cap" % (C_own/1e3, ratio))
    print("   bow law: the medium bow fires iff v >= ~0.9 C_own (%.0f km/s). RBH-1 at 0.996 -> the bow," % (thresh/1e3))
    print("   the star forge.  ONE point: it fixes Y_bow, so it is the ANCHOR, not a test (cavitation_speed_limit.py).")
    print("   'Oumuamua: 26 km/s = %.1e of its C -> no bow, observed none -> PASS." % (2.6e4/c0))
    print("   Open: the recoil-SMBH wake searches (3C 186, CID-42) have NEVER been checked.")
    print("   VERDICT: PASS as anchor; the bow LAW stays armed on the future catalog.\n")

# ----------------------------------------------------------------------
# 6. THE 16-FOLD CLOCK RINGDOWN: 4.68 ms (CLOSED on GW150914)
# ----------------------------------------------------------------------
def section6():
    tau_obs = 0.00468
    t_sep_sum = 82.9 + 73.4                     # 156.3 km (the two separate Max-P shells)
    t_merged = 0.5*(112.6 + 112.3)              # 112.45 km (k-rule / shell doc reads)
    dt_shed = t_sep_sum - t_merged              # 43.85 km
    d_stage = 2.0*dt_shed                       # 87.70 km (two-shell pass per stage)
    L_chord = math.sqrt(2.0)*d_stage            # 124.03 km
    tau_pred = N16*d_stage*1e3/c0               # 16 stages / c0
    tau_form = N16*L_chord*1e3/(math.sqrt(2.0)*c0)  # 16L/(sqrt(2) c0), same thing
    print("== 6. THE 16-FOLD CLOCK RINGDOWN ==")
    print("   dt_shed = 156.3 - 112.45 = %.2f km; d_stage = 2*dt_shed = %.2f km; L = sqrt(2)*d_stage = %.2f km" % (dt_shed, d_stage, L_chord))
    print("   tau_loop = 16L/(sqrt(2)*c0) = %.4f ms  (== 16*d_stage/c0 = %.4f ms)  vs GW150914 settling 4.68 ms -> %+.3f%%" % (tau_form*1e3, tau_pred*1e3, pct(tau_pred, tau_obs)))
    print("   c0*tau/16 = %.3f km matches d_stage (the crossing geometry)." % (c0*tau_obs/N16/1e3))
    print("   VERDICT: CLOSED on GW150914 (+0.012%, Ruling #5; the 4.6796 ms value is the pre-grind reading).")
    print("   The next light-merger ringdown is the armed timing check, not a waveform claim.\n")

# ----------------------------------------------------------------------
# 7. THE BLAZE STAR PLAYBOOK (4 kill conditions, overdue)
# ----------------------------------------------------------------------
def section7():
    yrs = 2026 - 1946
    print("== 7. BLAZE STAR (T CrB) PLAYBOOK ==")
    print("   ~80-yr recurrent nova, last erupted 1946 -> %d yrs elapsed -> OVERDUE (literature flagged" % yrs)
    print("   'days away' through 2026: Forbes 2026-06-02; MNRAS 2026, arXiv:2607.15245).")
    kills = [
        "the decline exactly matches the standard TNR/nucleosynthesis radioactive tail, no re-hold plateau",
        "E_total/m_drop != c0^2 within measurement (the heat ledger does not close on the shed mass)",
        "a clean monotonic accretion rise into the eruption, no pre-flash choked stall signature",
        "no 502 nm frustration-channel excess during the eruption",
    ]
    for i, k in enumerate(kills, 1):
        print("   KILL %d: %s." % (i, k))
    print("   VERDICT: PENDING - overdue, any day. Nothing to score until it fires.\n")

# ----------------------------------------------------------------------
# 8. V SGE STALL STRUCTURE
# ----------------------------------------------------------------------
def section8():
    print("== 8. V SGE STALL STRUCTURE ==")
    print("   the extreme mass-transfer binary; the literature's own endpoint is merge/collapse at saturation (~2083).")
    print("   the framework's contribution is the mechanism: the saturation IS the stall - the transfer feeds the choke")
    print("   until the medium refuses at its own rate; the endpoint is the same relief-runaway chain as every eruption.")
    print("   the stall structure is scoreable NOW from the archival light curve; no date is claimed beyond ~2083.")
    print("   Kill: the long-term brightening shows no stall/plateau structure - a smooth monotonic ramp all the way in.")
    print("   VERDICT: PENDING - scoreable now; endpoint ~2083. NOTE: no frozen quantitative prediction (weakest cell).\n")

# ----------------------------------------------------------------------
# THE TABLE
# ----------------------------------------------------------------------
def table():
    rows = [
        ("1. Pulsar speed cap ladder",
         "B1508+55 1083 vs 954/958.8",
         "INCONCLUSIVE (K1 pending; K2/K3 clean)",
         "K1 v-5sig>954 km/s + literature no-signature (needs sig_v<=25.8); K2 medium bow at v<0.9 C_own; K3 unslammed rho_eff>rho_max",
         "VLBA/Gaia astrometry of B1508+55 (sig_v<=26 km/s) + ATNF PSRCAT census - NOW, runnable; decisive when published"),
        ("2. Gaia wide binaries G_eff/G",
         "mid 1.431 vs 1.43 +/- 0.06",
         "CLOSED (scorecard TRUE #8)",
         "independent pre-registered sample: G_eff/G outside 1.243-1.618 at >=3sigma (the 1.43+/-0.06 source pinned first)",
         "published Gaia wide-binary sample (CLOSED); next independent pre-registered sample / Gaia DR4 - on publication"),
        ("3. Merger neck yield",
         "2.6373e11 vs 2.64e11 (-0.10%)",
         "PENDING (armed)",
         "light-event E-limit mass drop lands on the 3.23e11 curve, not the 2.6373e11 neck curve",
         "LIGO-Virgo-KAGRA GWOSC stream + GWTC catalogs - months (O4b running, O5 ~2027)"),
        ("4. Hawking temperature",
         "hbar c0^3/8piGMkB (exact)",
         "CLOSED (exact reproduction)",
         "derived T deviates from the formula (equality re-verified here); observational kill: measured BH T != formula (no feasible data)",
         "no feasible dataset decides an identity; recorded as a derivation closure, not an armed observation"),
        ("5. RBH-1 bow law",
         "950 km/s = 0.996 of C",
         "PASS - anchor; law armed",
         "one medium bow at <0.9 of its C_own, or one cap-runner without a bow",
         "HST/JWST deep imaging, wake search of 3C 186 & CID-42 (never checked) - archival, now"),
        ("6. 16-fold clock ringdown",
         "4.6806 ms vs 4.68 ms",
         "CLOSED on GW150914 (+0.012%)",
         "light-BH ringdown resolved at testable SNR shows no 4.68 ms family",
         "LVK ringdown of the next high-SNR light merger - months (O4b/O5)"),
        ("7. Blaze Star playbook",
         "4 kills; ~80-yr overdue",
         "PENDING - overdue, any day",
         "4 kills: (1) exact radioactive-tail decline, no re-hold; (2) E_tot/m_drop != c0^2; (3) monotonic rise, no pre-flash stall; (4) no 502 nm excess",
         "AAVSO light curves + ARAS spectra (502 nm channel) - any day; last eruption 1946"),
        ("8. V Sge stall structure",
         "stall plateau; endpoint ~2083",
         "PENDING - scoreable now",
         "long-term brightening shows no stall/plateau structure - a smooth monotonic ramp all the way in",
         "AAVSO/ASAS-SN public archives + archival plates - NOW for the stall; endpoint ~2083 (literature)"),
    ]
    w = [22, 24, 22, 44, 44]
    def wrap(t, width):
        return textwrap.wrap(t, width) or [""]
    cells = [[wrap(r[i], w[i]) for i in range(5)] for r in rows]
    def line(parts):
        s = ""
        for i, p in enumerate(parts):
            s += p + " " * (w[i] - len(p)) + "|"
        return s
    print("=" * 168)
    print("THE ASTRO FALSIFIABLES TABLE  (prediction | target | status | kill condition | who/when decides)")
    print("=" * 168)
    print(line(["prediction", "target", "status", "kill condition", "deciding observatory/dataset, when"]))
    print("-" * 168)
    for c in cells:
        n = max(len(x) for x in c)
        for j in range(n):
            parts = [c[i][j] if j < len(c[i]) else "" for i in range(5)]
            print(line(parts))
        print("-" * 168)

# ----------------------------------------------------------------------
# MISSES / CAVEATS (reported, never hidden)
# ----------------------------------------------------------------------
def misses():
    print("MISSES & CAVEATS ON RECORD (reported, never hidden):")
    for m in [
        "C(rho_max) gap: C_yield 953.7 vs C_ladder 958.8 km/s = +0.53% here (+0.522% in the PROMPT-F executable) - 'must be 0'; rho_max carries BACK-SOLVED pending the n-origin ruling (geometry or nudge?).",
        "n = 2/33 appears in no paper as the closure exponent's origin - an unused locked constant until the fold closure (ruling #1).",
        "Merger no-edge pair 0.71% vs 0.88% is CLAIMED-NOT-REPRODUCED (Ruling #12); GW190521 min(E,S) = 5.56 vs catalog 9.0 Msun (38% miss).",
        "B1508+55 astrometry +103/-90 km/s is too coarse for K1; the decisive read needs sigma_v <= 25.8 km/s (published: none yet).",
        "Wide binaries: the '1.43 +/- 0.06' target source is unnamed in the papers (pin required); the predicted band 1.243-1.618 is wide - only the midpoint test has closed.",
        "Hawking: an exact reproduction is an identity, not a prediction - no feasible observation can falsify it near-term (recorded as closure, not as a score).",
        "RBH-1 is ONE anchor point (it fixes Y_bow) - the bow law's kills are what is armed; the 3C 186 / CID-42 wake searches have never been run.",
        "16-fold: the 4.6796 ms (+0.009%) pre-grind vs 4.6806 ms (+0.012%) status collision was consolidated by Ruling #5 (CLOSED = 4.6806).",
        "Blaze Star: AAVSO/ARAS downloads sit behind a Cloudflare check from this machine (pull in a browser); the 502 nm channel rides ARAS/AAVSO spectra.",
        "V Sge: no frozen quantitative prediction - the stall claim is shape-only (the weakest of the eight).",
    ]:
        print("  - " + m)
    print()

# ----------------------------------------------------------------------
# THE 5-LINE SUMMARY
# ----------------------------------------------------------------------
def summary():
    print("5-LINE SUMMARY:")
    lines = [
        "CLOSEST TO FIRING: Blaze Star T CrB - eruption overdue (80-yr recurrence, last 1946; literature flagged 'days away' through 2026); 4 kill conditions armed, AAVSO/ARAS decide any day.",
        "NEXT: pulsar census K1 - B1508+55 at 1,083 km/s sits +1.3sigma over the 954 cap, decisive once VLBA/Gaia proper motion reaches sigma_v <= 26 km/s; the merger-neck + 16-fold pair await the next light BH merger (O4b/O5).",
        "WEAKEST CLAIM: V Sge stall structure - no frozen quantitative prediction (mechanism restatement with a shape-only kill); runner-up weak: the Hawking item, an exact identity rather than an armed observation.",
        "NEXT DERIVATION: the n-origin ruling - derive n = 2/33 from the fold geometry to close the on-record C(rho_max) gap (953.7 yield-law vs 958.8 ladder, +0.53%) and settle rho_max DERIVED vs BACK-SOLVED.",
        "RUNNER-UP DERIVATION: the bow-law wake searches for 3C 186 / CID-42 (never checked, archival data in hand) and pinning the unnamed 1.43 +/- 0.06 wide-binary source for the pre-registered >=3sigma re-test.",
    ]
    for i, l in enumerate(lines, 1):
        print("  %d. %s" % (i, l))

def main():
    print("PHASE WAVE COSMOLOGY - THE EIGHT ASTROPHYSICAL FALSIFIABLES (compiled 2026-10-21)")
    print("locked set: c0, rho0, rho_max (shell/derived), rho_core, s=1/19, Y_bow, n=2/33, f_solid, a_max,")
    print("a0_bare, a0, T=27, N=16, G, hbar, kB, H0, Msun.  Zero fitted parameters; provenance per number.\n")
    print("derived self-checks: a0_bare = %.4e (locked 6.6110e-11); a0 = phi*a0_bare = %.4e (locked 1.0695e-10);" % (a0_bare, a0_knee))
    rho_closed = (2.0*Y_bow/c0**2)**(33.0/29.0)*rho0**(-4.0/29.0)
    print("fold closure (2Y_bow/c0^2)^(33/29)*rho0^(-4/29) = %.5e vs locked rho_max_derived 1.29032e15 (%+.3f%%); the locked table value is used." % (rho_closed, pct(rho_closed, rho_max_derived)))
    print()
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section7()
    section8()
    table()
    print()
    misses()
    summary()
    print()
    print("exit 0")

if __name__ == "__main__":
    main()
    sys.exit(0)
