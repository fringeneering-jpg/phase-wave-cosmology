# quantify_solar_system.py
# Score the PWC solar-system ladders against the measured bodies.
# RULES: ZERO fitted parameters. Provenance per number (DERIVED/MEASURED/
# VERIFIED/BACK-SOLVED/CLAIMED/OPEN). Misses reported, never hidden.
# Kill condition per candidate. Exits 0, prints clean tables.
# Laws re-implemented from the framework's own stage3 scripts
# (stage3_consumption_ladder.py, stage3_distance_ladder.py,
#  stage3_phonon_ladder.py, stage3_thermal_balance.py, stage3_photon_wind.py).
import math

# ---------------- LOCKED constants (task) ----------------
C0        = 2.99792458e8      # LOCKED
G         = 6.67430e-11       # LOCKED
HBAR      = 1.054571817e-34   # LOCKED
KB        = 1.380649e-23      # LOCKED
M_SUN     = 1.989e30          # LOCKED
L_SUN     = 3.828e26          # LOCKED (measured)
AU        = 1.495978707e11    # LOCKED
MDOT_DEEP = 4.357e9           # LOCKED via Gamma_sun = 2.1906e-21 s^-1
GAMMA_SUN = MDOT_DEEP / M_SUN # = 2.1906e-21 s^-1  (task value)

# Stefan-Boltzmann constant, DERIVED from locked hbar, kB, c0 (zero fitted)
SIGMA = math.pi**2 * KB**4 / (60.0 * HBAR**3 * C0**2)
L_EFF = MDOT_DEEP * C0**2    # full-conversion power of the deep channel (W)

# ---------------- MEASURED planetary data (NASA fact sheets / literature)
# name, M (kg), R (m), d (AU), Bond albedo, T_eff (K), internal heat (W or None)
PLANETS = [
    ("Mercury", 3.301e23,  2.4397e6, 0.387098, 0.068, 440.0, None),
    ("Venus",   4.8675e24, 6.0518e6, 0.723332, 0.77,  230.0, None),
    ("Earth",   5.9722e24, 6.371e6,  1.000000, 0.306, 255.0, 4.4e13),
    ("Mars",    6.4171e23, 3.3895e6, 1.523679, 0.25,  209.8, None),
    ("Jupiter", 1.8982e27, 6.9911e7, 5.20260,  0.343, 124.4, 3.35e17),
    ("Saturn",  5.6834e26, 5.8232e7, 9.55490,  0.342, 95.0,  1.99e17),
    ("Uranus",  8.6810e25, 2.5362e7, 19.2184,  0.30,  59.1,  0.0),
    ("Neptune", 1.02413e26, 2.4622e7, 30.1100,  0.29,  59.3,  2.1e15),
]
# task-provided internal heat: Earth 4.4e13, Jupiter 3.35e17, Saturn 1.99e17,
# Neptune 2.1e15, Uranus ~0.

def flux(d_AU):
    return L_SUN / (4.0 * math.pi * (d_AU * AU) ** 2)

def P_burn(M, d_AU):
    # consumption ladder own-burn: mdot(M,d) = mdot_deep (M/Ms)^(5/3) d^-2,
    # full mass-energy conversion
    return L_EFF * (M / M_SUN) ** (5.0 / 3.0) * d_AU ** -2.0

def gamma_law(M, d_AU):
    return GAMMA_SUN * (M / M_SUN) ** (2.0 / 3.0) * d_AU ** -2.0

def fmt_ratio(pred, meas):
    if meas is None:
        return "OPEN (no published value)"
    if meas <= 0:
        return "inf (meas=0)"
    r = pred / meas
    d = math.log10(r)
    return "%8.3g x  (%+.2f dex)" % (r, d)

def line(ch="="):
    print(ch * 74)

# sigma check: derived from locked constants only
print("sigma (derived from hbar,kB,c0) = %.6e   [standard 5.670374e-8]" % SIGMA)
print("Gamma_sun = %.6e s^-1 ; L_eff = mdot_deep*c0^2 = %.4e W" % (GAMMA_SUN, L_EFF))
print("fitted parameters: 0 (all formulas fixed; inputs = locked constants + published measurements)")

# ============================ TABLE 1 ============================
line()
print("1) CONSUMPTION LADDER  Gamma(M,d)=Gamma_sun (M/Ms)^(2/3) (d/1AU)^-2,")
print("   scored as own-burn power P = mdot_deep*c0^2 (M/Ms)^(5/3) d^-2 vs the")
print("   body's measured INTERNAL HEAT FLUX (framework claim: the thermal-")
print("   balance excess IS the consumption ladder's own-burn term).")
line()
print("%-9s %13s %12s %11s %17s %-11s" %
      ("body", "P_pred (W)", "P_meas (W)", "residual", "provenance", "verdict"))
for name, M, R, d, A, teff, pint in PLANETS:
    p = P_burn(M, d)
    if pint is None:
        print("%-9s %13.4e %12s %s %s" %
              (name, p, "OPEN", fmt_ratio(p, None), "DERIVED/OPEN"))
    else:
        print("%-9s %13.4e %12s %s %s" %
              (name, p, "%.3e" % pint, fmt_ratio(p, pint), "DERIVED/MEASURED"))
print("Sun anchor: P = mdot_deep*c0^2 = %.4e W  vs L_sun = %.4e W -> %s" %
      (L_EFF, L_SUN, fmt_ratio(L_EFF, L_SUN)) + "  (BACK-SOLVED: mdot_deep =")
print("            (L_rad+L_neu)/c0^2 by construction - the anchor is circular.")
print()
print("  kill conditions / notes:")
print("  Mercury : OPEN (dead planet; radiogenic estimate ~1e11 W -> +5.1 dex).")
print("  Venus   : OPEN (radiogenic estimate ~2e13 W -> +4.2 dex).")
print("  Earth   : KILL at 5.6e3 x - a 2.45e17 W furnace would make Earth glow; it puts out 4.4e13 W.")
print("  Mars    : OPEN (InSight-derived ~4e12 W -> +2.8 dex).")
print("  Jupiter : miss, +2.60 dex (398x the measured 3.35e17 W).")
print("  Saturn  : miss, +1.43 dex (26.7x vs task 1.99e17 W). Source spread flagged:")
print("            T_eff=95 K arithmetic gives 9.3e16 W internal (out/in 1.89); miss either way.")
print("  Uranus  : KILL. Ladder predicts 5.77e16 W; measured ~0 (out/in 1.06+/-0.08,")
print("            upper limit ~7e14 W). A body with no furnace is predicted to burn.")
print("  Neptune : miss, +1.17 dex (14.7x vs 2.1e15 W; T_eff arithmetic 3.3e15 W -> 9.3x).")
print("  Ladder survives ONLY as an escape-rate law (Table 5): Earth 1.10x.")

# ============================ TABLE 2 ============================
line()
print("2) THERMAL BALANCE  out/in per body (giants put off more than they take in)")
line()
print("%-9s %12s %12s %12s %17s %-12s" %
      ("body", "P_abs (W)", "P_out (W)", "out/in meas", "out/in ladder", "verdict"))
lit = {"Jupiter": 1.67, "Saturn": 1.78, "Uranus": 1.06, "Neptune": 2.61}
for name, M, R, d, A, teff, pint in PLANETS:
    pabs = (1.0 - A) * math.pi * R ** 2 * flux(d)
    pout = 4.0 * math.pi * R ** 2 * SIGMA * teff ** 4
    meas = pout / pabs
    plad = 1.0 + P_burn(M, d) / pabs
    v = "miss" if (plad - meas) / meas > 0.3 else "holds"
    ln = ("lit %.2f" % lit[name]) if name in lit else ""
    print("%-9s %12.4e %12.4e %12.4f %17.3f %-12s %s" %
          (name, pabs, pout, meas, plad, v, ln))
print()
print("  measured out/in from MEASURED T_eff, R, Bond albedo; literature check:")
print("  Jupiter 1.67, Saturn 1.78, Uranus 1.06, Neptune 2.61 -> J/U/N VERIFIED");
print("  within a few %; Saturn 1.89 vs 1.78 (~6%, albedo convention). Earth row");
print("  is 1.015 here (T_eff=255 K is the A=0.30 balance temp) vs 1.00037 from");
print("  1+P_int/P_abs with the 4.4e13 W internal flux.");
print("  FRAMEWORK's own printout (2.16/2.35/1.53/3.17) used geometric albedos");
print("  as Bond -> 20-30% inflation; Uranus 1.53 collapses to 1.07 with Bond");
print("  0.30 (its own comment says 1.06 - the script contradicts its printout).");
print("  QUALITATIVE CLAIM VERIFIED: J/S/N out/in > 1 (1.66 / 1.89 / 2.63),");
print("  Uranus ~1.06 (no internal heat) - the giants really do put off more.");
print("  LADDER-QUANTIFIED EXCESS MISSES: predicted out/in sits 0.8-2.2 dex above");
print("  measured at the giants; KILL at Uranus (predicts 12.1x, measured 1.07).");

# ============================ TABLE 3 ============================
line()
print("3) PHONON LADDER  day side carries d^-1/2; differential carries the wrap")
line()
print("  (a) day-side drive  T_day(d) = T_Earth_day * d^-1/2  (anchor Earth 288 K)")
print("%-9s %10s %12s %12s %s" % ("body", "d (AU)", "pred (K)", "meas (K)", "residual"))
day = {"Mercury": 700.0, "Venus": 737.0, "Earth": 288.0, "Mars": 293.0, "Moon": 390.0}
d_au = {"Mercury": 0.387098, "Venus": 0.723332, "Earth": 1.0, "Mars": 1.523679, "Moon": 1.0}
for b in ["Mercury", "Venus", "Earth", "Mars", "Moon"]:
    p = 288.0 * d_au[b] ** -0.5
    print("%-9s %10.4f %12.1f %12.0f %s" %
          (b, d_au[b], p, day[b], fmt_ratio(day[b], p) + " (meas/pred)"))
print("  Venus/Earth: measured 737/288 = 2.559; drive predicts 1.176 -> 2.18x short.")
print("  KILL: if the d^-1/2 drive alone sets surface T, Venus kills it. The 92-bar");
print("  phonon wrap carries the remaining 2.18x, but W_eff is built from MEASURED");
print("  P, rho, gamma, R, P_rot plus a hand-set 1-bar scale - no locked-constant");
print("  derivation (CLAIMED, not DERIVED).");
print()
print("  (b) day/night swing vs wrap  W_eff = (c_s*P_rot/2*pi*R)*(P/1 bar),");
print("      c_s = sqrt(gamma*P/rho)   [framework stage3_phonon_ladder.py]");
print("%-9s %12s %12s %9s %9s" % ("body", "c_s (m/s)", "travel (m)", "W_eff", "swing (K)"))
swing = {"Mercury": 600.0, "Venus": 0.0, "Earth": 10.0, "Mars": 110.0, "Moon": 280.0}
atm = {"Mercury": None, "Venus": (1.3, 9.2e6, 65.0, 243.0 * 86400.0, 6.052e6),
       "Earth": (1.4, 1.013e5, 1.225, 86400.0, 6.371e6),
       "Mars": (1.3, 636.0, 0.02, 88642.0, 3.390e6), "Moon": None}
for b in ["Mercury", "Venus", "Earth", "Mars", "Moon"]:
    if atm[b] is None:
        print("%-9s %12s %12s %9s %9.0f" % (b, "-", "-", "0", swing[b]))
    else:
        gam, P, rho, prot, R = atm[b]
        cs = math.sqrt(gam * P / rho)
        trav = cs * prot
        weff = trav / (2 * math.pi * R) * (P / 1.013e5)
        print("%-9s %12.1f %12.4e %9.4g %9.0f" % (b, cs, trav, weff, swing[b]))
print("  swing is monotone non-increasing in W_eff (0/10/110/280/600 K vs");
print("  21509/0.73/0.0053/0/0) -> qualitative hit (VERIFIED ordering), but no");
print("  closed quantitative law and no locked constants anywhere in it.");
print("  KILL: none for the ordering; the surface-T reading is killed at Venus.")

# ============================ TABLE 4 ============================
line()
print("4) PHOTON WIND  R_crit: beta = F_sail/F_grav = 1, rock dust at 1 AU")
line()
F1 = L_SUN / (4 * math.pi * AU ** 2)
A_DUST, RHO_ROCK, RHO_ICE = 0.1, 2500.0, 1000.0
rc = (1 + A_DUST) * 3 * F1 * AU ** 2 / (4 * C0 * G * M_SUN * RHO_ROCK)
rc_qpr = 3 * F1 * AU ** 2 / (4 * C0 * G * M_SUN * RHO_ROCK)   # standard Q_pr=1
rc_ice = (1 + A_DUST) * 3 * F1 * AU ** 2 / (4 * C0 * G * M_SUN * RHO_ICE)
print("  framework formula (1+A)*3*F1*AU^2/(4 c0 G Ms rho), A=0.1, rho=2500:")
print("     R_crit(rock) = %.4f um   vs target 0.25 um -> %s" %
      (rc * 1e6, fmt_ratio(rc * 1e6, 0.25)))
print("  standard Q_pr=1 (drop the (1+A) factor): %.4f um -> %s" %
      (rc_qpr * 1e6, fmt_ratio(rc_qpr * 1e6, 0.25)))
print("  VERIFIED within ~10% either way - a real hit, DERIVED from locked c0, G,");
print("  Ms, L_sun + MEASURED dust density rho=2500 kg/m3.");
print("  KILL: none (would trigger if R_crit left ~0.1-1 um for rock dust).");
print("  BUG (reported, not hidden): photon_wind.json 'rock: 0.6315 um' is the");
print("  rho=1000 ICE value (%.4f um), saved by a loop-variable bug; rock with" % (rc_ice * 1e6))
print("  rho=2500 is %.4f um." % (rc * 1e6))

# ============================ TABLE 5 ============================
line()
print("5) DISTANCE LADDER  d^-2 drive, and Mars' 87.8x throttle")
line()
print("  (a) the arriving drive itself: F(d) = L_sun/4*pi*d^2 ->");
print("      F(Mars)/F(Earth) = %.5f vs (1/1.523679)^2 = %.5f  (exact identity," %
      (flux(1.523679) / flux(1.0), 1.0 / 1.523679 ** 2))
print("      VERIFIED - but trivial: it IS the definition of insolation).");
print()
print("  (b) does the body's consumption follow it? Gamma = Gamma_sun (M/Ms)^(2/3) d^-2");
print("%-9s %14s %14s %17s %s" % ("body", "law (1/s)", "observed (1/s)", "ratio obs/law", "verdict"))
obs = {"Earth": ("3 kg/s escape", 3.0 / 5.9722e24),
       "Mars": ("MAVEN ~2.5 kg/s", 2.5 / 6.4171e23),
       "Jupiter": ("plasma ~1e3 kg/s", 1.0e3 / 1.8982e27)}
for name, M, R, d, A, teff, pint in PLANETS:
    law = gamma_law(M, d)
    if name in obs:
        tag, o = obs[name]
        r = o / law
        v = "HIT (anchor)" if 0.9 <= r <= 1.15 else ("order-level (noisy)" if 0.3 < r < 3.0 else "MISS")
        print("%-9s %14.4e %14.4e %12.2f x (%+.2f dex) %s [%s]" %
              (name, law, o, r, math.log10(r), v, tag))
    else:
        print("%-9s %14.4e %14s %17s %s" % (name, law, "OPEN", "-", "no published total loss"))
print()
print("  Mars: law %.4e /s -> %.4g kg/s; MAVEN sees ~2.5 kg/s = %.1fx the d^-2" %
      (gamma_law(6.4171e23, 1.523679), gamma_law(6.4171e23, 1.523679) * 6.4171e23,
       2.5 / 6.4171e23 / gamma_law(6.4171e23, 1.523679)))
print("  drive (framework printed 87.81 with d=1.524). KILL: the d^-2 radiation");
print("  drive does NOT set Mars' consumption; the body's own throttle (low-");
print("  gravity escape, photochemistry) outruns it - the framework's own script");
print("  concedes this. Residual +1.94 dex. Honest MISS.");
print("  Earth: 1.10x - the ladder's own anchor (holds to 10%). Jupiter: 0.67x -");
print("  within an order (noisiest anchor, plasma outflow). Mercury/Venus/Saturn/");
print("  Uranus/Neptune: OPEN (no published total-loss rates).");

# ============================ SUMMARY ============================
line()
print("HONEST MISSES: consumption ladder as internal heat (Earth x5.6e3, Uranus");
print("5.8e16 W vs ~0); thermal-balance quantities (giants +0.8..+2.2 dex);");
print("phonon surface-T at Venus (2.18x short); distance ladder at Mars (87.8x);");
print("framework's own printed out/in use geometric-as-Bond albedo (+20-30%);");
print("photon_wind.json rock/ice mislabel; Saturn and Neptune internal-heat source");
print("spread (task value vs T_eff arithmetic) reported, verdicts unaffected.");
print()
print("SUMMARY (5 lines)");
print("1. BEST HIT   : photon wind R_crit = 0.253 um (0.230 um with Q_pr=1) vs");
print("               rock-dust blowout at 0.25 um / 1 AU - within +1%/-8%,");
print("               DERIVED from locked constants alone (VERIFIED).");
print("2. WORST MISS : consumption ladder as own-furnace - Earth +3.75 dex, and");
print("               Uranus KILLED (predicts 5.77e16 W where ~0 is measured).");
print("3. SURVIVES   : ladder as escape-rate law: Earth 1.10x; thermal-balance");
print("               qualitative claim (giants out/in 1.66/1.89/1.07/2.63) VERIFIED.");
print("4. NEXT DERIVATION: derive the 87.8x Mars throttle term (gravity/photochem)");
print("               from locked constants instead of importing it measured.");
print("5. FITTED PARAMETERS: 0. Every formula fixed; inputs are locked constants");
print("               + published measurements; nothing tuned, nothing hidden.");
print()
print("exit 0")
