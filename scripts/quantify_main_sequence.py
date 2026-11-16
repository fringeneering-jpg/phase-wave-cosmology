# quantify_main_sequence.py
# Phase Wave Cosmology - the stellar main-sequence ladder from the locked set only.
# Task: the M^(2/3) consumption ladder across the main sequence, sample
#   (0.1, 0.25, 0.5, 1.0, 1.5, 3, 5, 10, 20, 40) Msun.
# Rules: ZERO fitted parameters; provenance per number; misses reported, never
# hidden; kill condition per candidate; OPEN marked where the locked set gives
# no route. Exit 0.
# 2026-10-21 - quantifier run.

import math, sys, os

# =====================================================================
# LOCKED SET (as given in the task; provenance labels per the frozen ledger)
# =====================================================================
C0     = 2.99792458e8    # LOCKED  (Maxwell: 1/sqrt(mu0 eps0); measured)
RHO0   = 8.74e-27        # LOCKED  (the medium's ambient density)
RHO_MAX= 1.29032e15      # DERIVED (the electron Max-P: (2Y_bow/c0^2)^(33/29) rho0^(-4/29))
RHO_CORE=2.3e17          # LOCKED  (the bare neutron core)
S      = 1.0/19.0        # LOCKED  (the 19:1:18 fold balance)
Y_BOW  = 5.9307e26       # LOCKED  (the one yield, Pa)
N_LAD  = 2.0/33.0        # LOCKED  (the EOS shape exponent)
F_SOLID= 8.4989e-4       # DERIVED (the solid debt fraction - the one datum)
A_MAX  = 3.23e11         # LOCKED  (the medium's acceleration ceiling, N/kg)
G      = 6.67430e-11     # LOCKED  (in-framework: f_solid^12 (4s/81) Rp^2 c0^3/hbar)
MSUN   = 1.989e30        # LOCKED  (solar mass)
LSUN   = 3.828e26        # LOCKED  (solar luminosity)
RSUN   = 6.957e8         # LOCKED  (solar radius)
TEFF_SUN=5772.0          # LOCKED  (solar effective temperature)
SIGMA  = 5.670374e-8     # LOCKED  (Stefan-Boltzmann)
HBAR   = 1.054571817e-34 # LOCKED  (unused in this ladder)
KB     = 1.380649e-23    # LOCKED  (unused in this ladder)
T27    = 27.0            # LOCKED  (unused in this ladder)
T7B    = 1.0/57.0        # LOCKED  (unused in this ladder)
T7D    = 20.0/1083.0     # LOCKED  (unused in this ladder)
N16    = 16.0            # LOCKED  (unused in this ladder)

# anchors carried by the paper / solar program - NOT in this task's locked list
F_CHOKE_SUN = 0.07       # the 7% restricted share; solar frozen gate (stage3_outside_in_ladder.py)
SIGMA_K     = 8.48e20    # the k-rule held column kg/m^2 (FITTED column; BH branch only)
T_SKIN      = 650.0e3    # 650 km canonical skin (Sigma_k / shell-read rho_max 1.304e15)
T_CMB       = 2.7255     # CMB temperature K (MEASURED; used only for the r_lum anchor)
A_RAD       = 7.5657e-16 # radiation constant (4 sigma/c0)

MASSES = [0.1, 0.25, 0.5, 1.0, 1.5, 3.0, 5.0, 10.0, 20.0, 40.0]
AU  = 1.495978707e11
LY  = 9.4607304725808e15
DEX_KILL = 0.30   # convention used here: |residual| > 0.30 dex (factor ~2) kills a point

# ZAMS effective temperatures, Pecaut & Mamajek 2013 (ApJS 208, 9), +/-5% spread.
ZAMS_T = {0.1:2900, 0.25:3380, 0.5:3800, 1.0:5772, 1.5:6950,
          3.0:10600, 5.0:15700, 10.0:23900, 20.0:32000, 40.0:44300}

lines = []
def out(s=""):
    lines.append(s); print(s)

# =====================================================================
# DERIVED BRIDGES (each with provenance)
# =====================================================================
a0_bare = (C0/math.sqrt(3.0))*math.sqrt(G*RHO0/4.0)              # 6.6110e-11 m/s^2
rho_max_chk = (2.0*Y_BOW/C0**2)**(33.0/29.0)*RHO0**(-4.0/29.0)
t_skin_locked = SIGMA_K/RHO_MAX
sigma_sheet  = A_MAX/(2.0*math.pi*G)
rcore_sun = (3.0*MSUN/(4.0*math.pi*RHO_CORE))**(1.0/3.0)
g_sun   = G*MSUN/RSUN**2
mdot_sun= LSUN/C0**2
eps_sun = mdot_sun/MSUN
t_eff_chk = (LSUN/(4.0*math.pi*SIGMA*RSUN**2))**0.25
u_cmb   = A_RAD*T_CMB**4
r_lum_sun_AU = math.sqrt(LSUN/(4.0*math.pi*C0*u_cmb))/AU

out("="*96)
out("PWC - THE STELLAR MAIN-SEQUENCE LADDER - the M^(2/3) consumption board")
out("quantify_main_sequence.py | zero fitted parameters | provenance per number |")
out("misses reported | kill condition per candidate | OPEN marked | exit 0")
out("="*96)
out()
out("DERIVED BRIDGES (checked against the locked table)")
out("  a0_bare = (c0/sqrt3) sqrt(G rho0/4)          = %.4e m/s^2  [DERIVED; locked 6.6110e-11]" % a0_bare)
out("  rho_max = (2Y_bow/c0^2)^(33/29) rho0^(-4/29) = %.5e kg/m^3 [DERIVED; locked 1.29032e15; residual %+.3f%%]" % (rho_max_chk, 100*(rho_max_chk/RHO_MAX-1)))
out("  t_skin  = Sigma_k/rho_max = 657 km with the locked rho_max (650 km canonical with the")
out("            shell-read 1.304e15); Sigma_k = 8.48e20 kg/m^2 is the FITTED k-rule column;")
out("            the zero-fit sheet candidate a_max/(2 pi G) = %.3e kg/m^2 misses it by %+.1f%%" % (sigma_sheet, 100*(SIGMA_K/sigma_sheet-1)))
out("  R_core(M) = (3M/4pi rho_core)^(1/3) = %.3f km x m^(1/3)  [DERIVED; 5.3 Msun -> %.2f km, the paper's 22.2 km BH core]" % (rcore_sun/1e3, rcore_sun*5.3**(1/3)/1e3))
out("  g_sun    = G Msun/Rsun^2 = %.2f m/s^2" % g_sun)
out("  f_choke_solar = 0.07 (the 7% restricted share, solar frozen gate)  [ANCHOR, not in this locked list]")
out("  T_eff self-check: (L_sun/4pi sigma R_sun^2)^(1/4) = %.1f K vs locked 5772  [IDENTITY]" % t_eff_chk)
out("  mdot_sun = L_sun/c0^2 = %.4e kg/s (deep channel 4.3572e9 incl 2.3%% neutrinos)" % mdot_sun)
out("  eps_sun  = mdot_sun/M_sun = %.4e 1/s  (consumption_ladder.json: 2.1906e-21 deep)" % eps_sun)
out("  r_lum_sun = sqrt(L_sun/(4 pi c0 u_cmb)) = %.1f AU, u_cmb = a T_cmb^4, T_cmb = 2.7255 K" % r_lum_sun_AU)
out("            [ANCHOR: luminous_reach.json 10428.5 AU; T_cmb MEASURED, not in this locked list]")
out("  UNUSED locked here: hbar, kB, T=27, T7b=1/57, T7d=20/1083, N=16, s=1/19, n=2/33,")
out("            f_solid (a_max enters only the rejected sheet-column check above)")
out()

# =====================================================================
# empirical comparison laws (literature; used strictly as the target, no fit)
# =====================================================================
def emp_L(m):
    if m > 1.0:  return m**3.5   # standard empirical MLR, upper main sequence
    if m < 1.0:  return m**2.3   # standard empirical MLR, low mass
    return 1.0
def emp_R(m):
    if m > 1.66: return m**0.57  # Demircan & Kahraman 1991 (Ap&SS 181, 313)
    return m**0.8
def emp_T_chain(m):
    return TEFF_SUN*(emp_L(m)/emp_R(m)**2)**0.25

# =====================================================================
# CANDIDATE 1 - THE LUMINOSITY LAW (the M^(2/3) consumption ladder)
#   per-kg consumption eps(M) = eps_sun m^(2/3);  L = c0^2 eps M = L_sun m^(5/3)
#   ladder exponent 5/3 = 1.667  vs  data demand 3.5 (m>1) / 2.3 (m<1)
# =====================================================================
out("="*96)
out("CANDIDATE 1 - THE LUMINOSITY LAW  L = L_sun (M/M_sun)^(5/3)")
out("  per-kg consumption eps = eps_sun m^(2/3) -> L = c0^2 eps M = L_sun m^(5/3)")
out("  ladder forces exponent 5/3 = 1.667 | data demand 3.5 (M>1) and 2.3 (M<1)")
out("  kill convention: |residual| > 0.30 dex kills the candidate at that mass")
out("="*96)
out("%-6s %-22s %-16s %-10s %-34s %-30s" % ("m", "law prediction", "empirical", "residual", "provenance", "kill condition / verdict"))
out("%-6s %-22s %-16s %-10s %-34s %-30s" % ("(Msun)", "(L_sun; eps 1/s)", "(L_sun)", "(dex)", "", ""))
out("-"*96)
for m in MASSES:
    Lp  = LSUN*m**(5.0/3.0)
    eps = eps_sun*m**(2.0/3.0)
    Le  = LSUN*emp_L(m)
    res = math.log10(Lp/Le)
    verdict = "SURVIVES" if abs(res) <= DEX_KILL else "KILLED"
    out("%-6.2f %-22s %-16s %-10s %-34s %-30s" % (m,
        "%.4g (%.2e)" % (Lp/LSUN, eps),
        "%.4g" % (Le/LSUN),
        "%+.3f" % res,
        "m^(5/3) consumption ladder (locked)",
        "%s (%+.2f dex vs 0.30)" % (verdict, res)))
out()
out("VERDICT 1: KILLED as a complete bolometric luminosity law - residuals run +0.63 dex (0.1)")
out("  to -2.94 dex (40 Msun); the ladder forces 5/3, the data demands 3.5 / 2.3. It SURVIVES")
out("  only at 0.5-1.0 Msun, and survives everywhere as the CONSUMPTION (untying) rate, which is")
out("  not the observable bolometric L: the gap is the fusion throttle (the temperature")
out("  sensitivity of the p-p/CNO chains) - OPEN, no route from the locked set.")
out()

# =====================================================================
# CANDIDATE 2 - THE RADIUS LADDER (the shell law)
#   route A (grip collapse, D34): f_choke = (g_surf/a0_bare)^2 f_choke_solar; the
#     main sequence is the fixed-hold line f_choke = f_choke_solar = 7% ->
#     g_surf = const -> R = R_sun m^(1/2).  The surface-area column law
#     M = Sigma_star 4 pi R^2 gives the same exponent 1/2 (Sigma_star OPEN).
#   route B (650-km skin, compact branch): R = R_core + t_skin, R_core ~ m^(1/3)
#     at rho_core - the black-hole branch.
#   data demand: 0.57 (M>1.66) / 0.8 (M<1.66)
# =====================================================================
out("="*96)
out("CANDIDATE 2 - THE RADIUS LADDER  (the shell law: 650-km skin / D34 grip collapse)")
out("  route A: f_choke = (g_surf/a0_bare)^2 f_choke_solar (D34); MS = fixed hold f_choke = 7%")
out("           -> g_surf = const -> R = R_sun m^(1/2)   [ladder forces 1/2]")
out("  route B: R = R_core + t_skin, R_core = (3M/4pi rho_core)^(1/3) + 650 km  [forces 1/3 + const; BH branch]")
out("  data demand: 0.57 (M>1.66), 0.8 (M<1.66)  [Demircan & Kahraman 1991]")
out("="*96)
out("%-6s %-14s %-14s %-12s %-12s %-12s %-26s %-28s" % ("m","route A","route B","empirical","resid A","resid B","provenance","kill condition / verdict"))
out("%-6s %-14s %-14s %-12s %-12s %-12s %-26s %-28s" % ("(Msun)","(R_sun)","(km)","(R_sun)","(dex)","(dex)","",""))
out("-"*96)
for m in MASSES:
    RA  = RSUN*m**0.5
    RB  = rcore_sun*m**(1.0/3.0) + T_SKIN
    Re  = RSUN*emp_R(m)
    rA  = math.log10(RA/Re)
    rB  = math.log10(RB/Re)
    vA  = "SURVIVES" if abs(rA) <= DEX_KILL else "KILLED"
    vB  = "SURVIVES" if abs(rB) <= DEX_KILL else "KILLED"
    out("%-6.2f %-14s %-14s %-12s %-12s %-12s %-26s %-28s" % (m,
        "%.4f" % (RA/RSUN),
        "%.1f" % (RB/1e3),
        "%.4f" % (Re/RSUN),
        "%+.3f" % rA,
        "%+.3f" % rB,
        "A: grip 7% / B: core+skin",
        "A: %s (%+.2f) / B: %s (%+.2f)" % (vA, rA, vB, rB)))
out()
out("f_choke diagnostic (grip share along the ladder): route A holds f_choke = 7% BY CONSTRUCTION;")
out("  empirical radii give 110.9% at 0.1 Msun (over-retained), 2.49% at 40 Msun, and the giants")
out("  collapse (Betelgeuse: f_choke = 5.6e-11, a >1e9-fold grip collapse - D34's shedding).")
out()
out("VERDICT 2: route A SURVIVES 0.25-40 Msun (|resid| <= 0.18 dex) and sits ON the kill line")
out("  at 0.1 Msun (+0.30 dex, reported boundary); the shell law forces 1/2, the data demand")
out("  0.57/0.8, and 1/2 splits the empirical pair. Route B is KILLED for the main sequence")
out("  (~-3.0 dex at the Sun: 663 km vs 6.957e8 m) - it is the compact/BH branch, not the photosphere.")
out("  OPEN: a star column Sigma_star for a zero-fit normalization (the BH Sigma_k is FITTED),")
out("  and the 0.8 <-> 0.57 bend (the convective/radiative split) - no route in the locked set.")
out()

# =====================================================================
# CANDIDATE 3 - T_eff FROM L = 4 pi R^2 sigma T^4
#   T = T_sun m^((5/3 - 2*(1/2))/4) = T_sun m^(1/6)   [ladder forces 1/6]
#   data demand (chain): (3.5-2*0.57)/4 = 0.59 (m>1.66); (2.3-2*0.8)/4 = 0.175 (m<1.66)
# =====================================================================
out("="*96)
out("CANDIDATE 3 - THE EFFECTIVE TEMPERATURE  L = 4 pi R^2 sigma T^4")
out("  ladder: T = 5772 K m^(1/6)   [forces 1/6 = 0.167]")
out("  data demand via the empirical chain (p-2q)/4: 0.59 (m>1.66, 3.5 & 0.57);")
out("  0.475 (1<m<1.66, 3.5 & 0.8); 0.175 (m<1, 2.3 & 0.8);")
out("  measured ZAMS anchors (Pecaut & Mamajek 2013, +/-5%) for the verdict")
out("="*96)
out("%-6s %-12s %-12s %-12s %-12s %-28s %-30s" % ("m","law T_eff","chain T_eff","ZAMS T_eff","resid (ZAMS)","provenance","kill condition / verdict"))
out("%-6s %-12s %-12s %-12s %-12s %-28s %-30s" % ("(Msun)","(K)","(K)","(K)","(dex)","",""))
out("-"*96)
for m in MASSES:
    Tl = TEFF_SUN*m**(1.0/6.0)
    Tc = emp_T_chain(m)
    Tz = ZAMS_T[m]
    rz = math.log10(Tl/Tz)
    rc = math.log10(Tl/Tc)
    v  = "SURVIVES" if abs(rz) <= DEX_KILL else "KILLED"
    out("%-6.2f %-12s %-12s %-12s %-12s %-28s %-30s" % (m,
        "%.0f" % Tl, "%.0f" % Tc, "%.0f" % Tz,
        "%+.3f" % rz,
        "m^(1/6) = (5/3 - 2*1/2)/4 (locked)",
        "%s vs ZAMS (%+.2f dex vs 0.30)" % (v, rz)))
out()
out("chain check (secondary): below 1 Msun the ladder's 1/6 vs the chain's 0.175 nearly")
out("  cancel (|resid| <= 0.008 dex at 0.1-0.5; at 1.5 the chain's mixed 0.475 sits between) -")
out("  recorded, but it does NOT survive the measured anchors:")
out("  +0.13 dex at 0.1-0.5 (3,900-5,100 K predicted for 2,900-3,800 K M/K dwarfs).")
out()
out("VERDICT 3: SURVIVES 0.1-3 Msun (worst -0.19 dex at 3); KILLED for M >= 5 (10,674 K vs")
out("  44,000 K at 40 Msun, -0.62 dex). The ladder cannot produce O/B photospheres.")
out()

# =====================================================================
# CANDIDATE 4 - THE LUMINOUS REACH  r_lum = sqrt(L)
#   r_lum = r_lum_sun sqrt(L/L_sun) = 10,429 AU m^(5/6)  [shape locked; the
#   absolute anchor rides on T_cmb = 2.7255 K, MEASURED, not in the locked list]
# =====================================================================
out("="*96)
out("CANDIDATE 4 - THE LUMINOUS REACH  r_lum = sqrt(L)  (10,429 AU x m^(5/6))")
out("="*96)
out("%-6s %-14s %-16s %-14s %-42s" % ("m","L_law (L_sun)","r_lum (AU)","r_lum (ly)","provenance"))
out("-"*96)
for m in MASSES:
    Lp = LSUN*m**(5.0/3.0)
    rl = r_lum_sun_AU*m**(5.0/6.0)
    out("%-6.2f %-14s %-16s %-14s %-42s" % (m,
        "%.4g" % (Lp/LSUN),
        "%.0f" % rl,
        "%.3f" % (rl*AU/LY),
        "r_lum_sun sqrt(L/L_sun); r_lum_sun = 10,429 AU"))
out()
out("VERDICT 4: a definition, not an independent law - r_lum inherits Candidate 1's kill beyond")
out("  ~1.5 Msun (the reach is sqrt of the consumption luminosity). The M^(5/6) shape is locked;")
out("  the absolute normalization needs T_cmb = 2.7255 K - OPEN in this locked list.")
out()

# =====================================================================
# OPEN ITEMS
# =====================================================================
out("="*96)
out("OPEN - where the locked set gives no route")
out("="*96)
out("  1. The fusion throttle: the term that turns the M^(5/3) untying rate into the")
out("     M^(3.5)/M^(2.3) bolometric output (temperature sensitivity of p-p/CNO).")
out("  2. The star column Sigma_star (zero-fit radius normalization); the BH Sigma_k = 8.48e20")
out("     kg/m^2 is FITTED and the sheet candidate a_max/(2 pi G) misses it by +10.1%.")
out("  3. The empirical radius bend 0.8 <-> 0.57 (convective/radiative split) - no route.")
out("  4. T_cmb = 2.7255 K (r_lum absolute anchor) - MEASURED, not in this locked list.")
out("  5. f_choke_solar = 7% (solar-program frozen gate) - ANCHOR, not in this locked list;")
out("     without it the R normalization is OPEN (the exponent 1/2 stands regardless).")
out()

# =====================================================================
# 5-LINE SUMMARY
# =====================================================================
out("="*96)
out("5-LINE SUMMARY")
out("="*96)
out("1. BEST HIT - radius ladder R = R_sun (M/M_sun)^(1/2) (D34 grip collapse, fixed 7% hold):")
out("   survives 0.25-40 M_sun (worst +0.18 dex); the 0.1 M_sun point sits ON the kill line")
out("   (+0.30 dex, boundary); the shell law forces 1/2, splitting the data's demanded 0.57/0.8 pair.")
out("2. WORST MISS - luminosity ladder L = L_sun (M/M_sun)^(5/3) as total bolometric output:")
out("   KILLED, -2.94 dex at 40 M_sun (468 vs 4.06e5 L_sun) and +0.63 dex at 0.1; forces 5/3,")
out("   data demands 3.5 / 2.3; survives only as the consumption (untying) rate.")
out("3. T_eff ladder T = 5772 K (M/M_sun)^(1/6): survives 0.1-3 M_sun, KILLED for M >= 5")
out("   (-0.62 dex at 40: 10,674 K vs 44,000 K); the chain-level low-mass cancellation (<=0.01 dex)")
out("   is recorded but does not survive measured anchors (+0.13 dex).")
out("4. r_lum = 10,429 AU (M/M_sun)^(5/6) = sqrt(L): 1,530 AU (0.1) -> 225,583 AU (40); the shape")
out("   is locked, the absolute anchor needs T_cmb = 2.7255 K (not locked here).")
out("5. NEXT DERIVATION - the fusion throttle (the missing term between the M^(5/3) untying rate")
out("   and the M^(3.5/2.3) output) and the star column Sigma_star; both OPEN. The 650-km-skin")
out("   compact branch (M^(1/3)) is the BH branch and is KILLED for the main sequence (-3.0 dex).")
out()
out("exit 0")

# mirror the report to the repo's results convention
res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantify_main_sequence_results.txt")
with open(res_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("report written:", res_path)
sys.exit(0)
