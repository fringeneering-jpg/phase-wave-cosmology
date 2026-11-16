"""
PWC keystone derivation -- continuous EoS bridging untied (w=1/3) and
locked (w=1) branches, the holding-threshold law, the 95% stretch chain,
and the two-choke landing.

Locked inputs only:
  rho_0   = 8.74e-27 kg/m^3   (resting)
  rho_max = 1.304e15 kg/m^3   (ceiling)
  c0      = 2.99792458e8 m/s
  G       = 6.6743e-11
  L       = c0^2 J/kg  (latent heat; gas->solid exothermic)
  u       = c0^2 J/kg  in EVERY phase
  P_g = rho c0^2/3 (c_s = c0/sqrt(3)),  P_k = rho c0^2 (c_s = c0)
  first-order transition; coexistence rho_g* = rho_max/2, P* = rho_max c0^2;
  enthalpy jump P* dv = c0^2; plateau c_s = 0; fold at rho_gap = rho_max/2.
No fitted parameters. No GR, no dark matter.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants
c0    = 2.99792458e8
G     = 6.6743e-11
rho0  = 8.74e-27
rhomax = 1.304e15
a0_meas   = 6.68e-11          # SPARC/PROBES shared-tension value (sealed)
a_yield   = 3.23e11           # sealed holding yield at rho_max
Msun  = 1.989e30
mn    = 1.674927498e-27
me    = 9.1093837015e-31
Rp    = 0.8414e-15            # proton charge radius (muonic H)
Mpc   = 3.0857e22
def H0_of(km_s_Mpc): return km_s_Mpc*1e3/Mpc     # s^-1

print("="*78)
print("SECTION 0 -- constants and branch endpoints")
print("="*78)
c_sg = c0/np.sqrt(3.0)
print(f"c_s(gas)   = c0/sqrt(3) = {c_sg:.6e} m/s   (w=1/3)")
print(f"c_s(locked)= c0         = {c0:.6e} m/s   (w=1)")
print(f"P*(coexistence) = rho_max c0^2 = {rhomax*c0**2:.6e} Pa")

# =====================================================================
print("="*78)
print("SECTION 1 -- TASK 1: the holding-threshold law and Omega_eff(S)")
print("="*78)

def w_S(S):    return (1.0 + 2.0*S)/3.0            # rigidity w = P/(rho c0^2)
def cs_S(S):   return c0*np.sqrt(w_S(S))           # branch sound speed
def Omega_eff(S): return 0.25*(16.0*np.pi)**S     # solid-angle prefactor
def a_hold(rho, S):
    return cs_S(S)*np.sqrt(Omega_eff(S)*G*rho)

S0, S1 = 0.0, 1.0
ah0 = a_hold(rho0,   S0)
ah1 = a_hold(rhomax, S1)
print("a_hold(rho, S) = c_s(S) * sqrt(Omega_eff(S) * G * rho)")
print("  c_s(S)^2 = c0^2 (1+2S)/3  ;  Omega_eff(S) = (1/4) * (16 pi)^S")
print(f"  Omega_eff(0) = {Omega_eff(S0):.6g}   (isotropic flux: 1/2 hemisphere x 1/2 cosine)")
print(f"  Omega_eff(1) = {Omega_eff(S1):.6f}   (Gauss-law sphere)")
print(f"  sqrt[Omega_eff(1)/Omega_eff(0)] = sqrt(16 pi) = {np.sqrt(16*np.pi):.6f}")
print()
print(f"ANCHOR 1: a_hold(rho_0, S=0)   = (c0/sqrt3) sqrt(G rho_0/4)")
print(f"        = {ah0:.6e} m/s^2   vs measured a0 = {a0_meas:.4e}  ->  {100*(ah0/a0_meas-1):+.2f}%")
print(f"ANCHOR 2: a_hold(rho_max, S=1) = c0 sqrt(4 pi G rho_max)")
print(f"        = {ah1:.6e} N/kg  vs sealed yield {a_yield:.4e}  ->  {100*(ah1/a_yield-1):+.2f}%")
print()
# the comparison legs quoted in the task
same_pref_at_max = cs_S(S1)*np.sqrt(0.25*G*rhomax)     # sqrt(G rho/4) prefactor
same_pref_at_0   = cs_S(S0)*np.sqrt(4*np.pi*G*rho0)    # 4 pi prefactor
print(f"[comparison] same sqrt(G/4) prefactor at rho_max: {same_pref_at_max:.4e} N/kg "
      f"({a_yield/same_pref_at_max:.2f}x low)")
print(f"[comparison] same 4-pi prefactor at rho_0:      {same_pref_at_0:.4e} m/s^2 "
      f"({same_pref_at_0/a0_meas:.2f}x high)")
sqrt403 = np.sqrt(40.0/3.0)
print(f"[numerology] sqrt(40/3) c0 sqrt(G rho_max) = {sqrt403*c0*np.sqrt(G*rhomax):.6e} "
      f"(matches sealed yield to {100*(sqrt403*c0*np.sqrt(G*rhomax)/a_yield-1):+.3f}%; "
      f"no mechanism -- rejected in repo, DERIVATION_BRIEF.md:188)")
print()
# What Omega_eff(1) WOULD be needed to hit 3.23e11 exactly with the same law:
need = (a_yield/(cs_S(S1)*np.sqrt(G*rhomax)))**2
print(f"[diagnostic] hitting {a_yield:.3e} at rho_max needs Omega_eff(1) = {need:.4f} sr "
      f"> 4 pi = {4*np.pi:.4f} sr (geometrically impossible) -> the 2.93% residual cannot "
      f"be a solid-angle effect; it needs the cohesion channel Y(rho_max) (missing input, see failures).")

# =====================================================================
print()
print("="*78)
print("SECTION 2 -- TASK 2: the transition shape; plateau/fold at rho_max/2")
print("="*78)

Pstar = rhomax*c0**2
rhog  = rhomax/2.0
vg, vs = 1.0/rhog, 1.0/rhomax
dv    = vg - vs
print("2a. Plateau EMERGES from the locked inputs (not asserted):")
print(f"    locked edge: (rho_max, P = rho_max c0^2) -> P* = {Pstar:.6e} Pa, v_s = {vs:.6e} m^3/kg")
print(f"    enthalpy jump (locked): P* dv = L = c0^2  ->  dv = c0^2/P* = {dv:.6e} m^3/kg")
print(f"    dv == v_s exactly ({np.isclose(dv, vs)}) because L = c0^2 = P_s v_s = "
      f"rho_max c0^2 * (1/rho_max).")
print(f"    -> v_g = v_s + dv = 2 v_s = {vg:.6e} m^3/kg  ->  rho_g* = rho_max/2 = {rhog:.6e} kg/m^3")
print(f"    -> the fold sits at rho_max/2 = {rhog:.3e} BY CONSTRUCTION of L = c0^2; no free parameter.")
print()
print("2b. Causality forbids any continuous bridge (mean-value theorem):")
slope_bridge = (Pstar - rhog*c0**2/3.0)/(rhomax - rhog)   # gas edge -> locked edge
slope_fold   = Pstar/rhog                                  # origin -> fold at P*
print(f"    bridge gas-edge -> locked-edge: avg slope = {slope_bridge/c0**2:.4f} c0^2 > c0^2  (FORBIDDEN)")
print(f"    bridge deep-space -> fold (rho_max/2, P*): avg slope = {slope_fold/c0**2:.4f} c0^2 > c0^2  (FORBIDDEN)")
print(f"    -> the plateau is forced first-order; it cannot be smoothed into a causal P(rho).")
print()
print("2c. Maxwell equal-area rule cannot be satisfied by ANY causal loop:")
# required equal-area integral: int_{rhog}^{rhomax} P d(rho)/rho^2 = P* dv = c0^2
I_req = Pstar*dv
def I_loop_max():   # causal envelope P <= rho c0^2 (eta <= 1) maximizes the integral
    return quad(lambda r: r*c0**2/r**2, rhog, rhomax)[0]
I_max = I_loop_max()
print(f"    required:  int P drho/rho^2 over [rho_max/2, rho_max] = P* dv = {I_req:.6e} = c0^2")
print(f"    causal max (P <= rho c0^2 everywhere): {I_max:.6e} = ln(2) c0^2 = {np.log(2):.4f} c0^2  <  c0^2")
print(f"    -> no barotropic bridge with w <= 1 satisfies the Maxwell rule; the transition is a")
print(f"       genuine discontinuity regularized only by surface tension (gradient term, not in inputs).")
print()
print("2d. The plateau and the order parameter:")
def eta_phase(rho):  return 2.0 - rhomax/rho    # lever rule, 0 -> 1 across the plateau
for r in [rhog, 1.25*rhog, 1.5*rhog, 0.9*rhomax, rhomax]:
    print(f"    rho={r:.3e}: phase fraction eta={eta_phase(r):.4f}, w_mix = P*/(rho c0^2) = {Pstar/(r*c0**2):.4f}, "
          f"c_s = sqrt(dP/drho) = 0 (plateau)")
print("    fold at rho_gap = rho_max/2: pressure jumps P*/6 -> P*,  jump = (5/6) P* = "
      f"{Pstar-Pstar/6:.6e} Pa")
print()
print("2e. c_s(rho) through the whole transition (must never exceed c0):")
print(f"    gas branch rho<rho_max/2 : c_s = c0/sqrt(3) = {c_sg:.6e} m/s")
print(f"    fold   rho = rho_max/2   : c_s -> 0 (spinodal of the idealized loop)")
print(f"    plateau rho in (rm/2, rm) : c_s = 0 (kappa = infinity)")
print(f"    locked edge rho = rho_max: c_s = c0 = {c0:.6e} m/s")
print(f"    max c_s = c0 exactly -> causal everywhere.  [pass]")
print()
print("2f. Metastable stiffening attempt: eta(rho) = (rho/rho_g*)^n always breaks causality at the fold:")
for n in [0.25, 0.5, 1.0, 2.0]:
    cs2_at_fold = c0**2*(1.0/3.0 + (2.0/3.0)*(n+1.0))
    print(f"    n={n}: c_s^2(rho_g*) = c0^2 [1/3 + 2(n+1)/3] = {cs2_at_fold/c0**2:.4f} c0^2  "
          f"({'> c0^2  FORBIDDEN' if cs2_at_fold > c0**2 else 'ok'})")
print("    the only causal approach to the fold is the slope->c0^2 asymptote P -> rho c0^2,")
print("    which still fails the equal-area rule (2c) -> plateau stands as the only shape.")

# =====================================================================
print()
print("="*78)
print("SECTION 3 -- TASK 3: the 95% / 5.3% stretch chain and Y_cav")
print("="*78)

print("3a. Volume-release arithmetic (locked rho_0):")
print(f"    volume released per untied mass = 1/rho_0 = {1/rho0:.6e} m^3/kg")
print(f"    per neutron: m_n/rho_0 = {mn/rho0:.5f} m^3   (repo says 0.207 m^3 -> implies rho_0 = "
      f"{mn/0.207:.3e}, the stale 8.1e-27 value; see failures)")
print(f"    per electron: m_e/rho_0 = {me/rho0*1e6:.1f} cm^3   (repo says 112 cm^3 -> implies "
      f"rho_0 = {me/1.12e-4:.3e}; same stale value)")
print()
print("3b. The 95% = rho_0/rho_crit, and the remaining stretch:")
for Hk in [("H0 = 70 km/s/Mpc (used by the repo's 0.95 claim)", 70.0),
           ("H0 = 67.4 (Planck/CMB)", 67.4),
           ("H0 = 73.8 (repo's own T7 SH0ES wall value)", 73.8)]:
    H = H0_of(Hk[1])
    rhoc = 3.0*H**2/(8.0*np.pi*G)
    print(f"    {Hk[0]:<52}: rho_crit = {rhoc:.5e}, rho_0/rho_crit = {rho0/rhoc:.4f}, "
          f"remaining stretch = {1.0/(rho0/rhoc)-1:.4f} ({100*(1.0/(rho0/rhoc)-1):.2f}%)")
print()
print("3c. The cohesion limit: medium fails at P = -Y_cav:")
s_target = 1.0/0.95 - 1.0
K0   = rho0*c0**2/3.0                      # bulk modulus of the untied branch
Ycav = s_target*K0
print(f"    K(rho_0) = rho_0 c_s^2 = rho_0 c0^2/3 = {K0:.6e} Pa")
print(f"    Y_cav = s * K = (1/0.95 - 1) * rho_0 c0^2/3 = {Ycav:.6e} Pa")
vcav = np.sqrt(2.0*Ycav/rho0)
print(f"    v_cav(rho_0) = sqrt(2 Y_cav/rho_0) = {vcav:.6e} m/s = {vcav/c0:.4f} c0   [speed-limit law 1/2 rho v^2 = Y]")
print(f"    cavitation length  lambda_cav = Y_cav/(rho_0 a_hold(rho_0)) = {Ycav/(rho0*ah0):.6e} m")
print(f"    = s x holding length  [holding length c_s/omega_hold = {cs_S(S0)/np.sqrt(Omega_eff(S0)*G*rho0):.6e} m]")
print(f"    -> the chain is CONSISTENT but s itself enters as the observed rho_0/rho_crit ratio;")
print(f"       a first-principles Y(rho_0) needs the pairing yank (missing input, see failures).")
print(f"    water benchmark: (-140 MPa)/(2.2 GPa) = {140e6/2.2e9:.4f} = {100*140e6/2.2e9:.2f}% "
      f"vs the medium's {100*s_target:.2f}% (same order, not exact).")
print()
print("3d. rho_0 chain (T2, checked): rho_0 = 8 a_hold rho_max R_p / (3 eta <v>) with eta=1/4, <v>=c0")
for lab, a in [("derived a_hold(rho_0) = 6.6094e-11", ah0), ("measured a0 = 6.68e-11", a0_meas)]:
    rho_pred = 8.0*a*rhomax*Rp/(3.0*0.25*c0*c0)
    print(f"    {lab:<38}: rho_0_pred = {rho_pred:.4e} kg/m^3 vs observed {rho0:.3e}  ->  "
          f"{100*(rho_pred/rho0-1):+.2f}%")
print("    -> rho_0 = 8.74e-27 comes out of the T2 chain near the observed vacuum density. [pass, -1.5%/+0.5%]")

# =====================================================================
print()
print("="*78)
print("SECTION 4 -- TASK 5: the two-choke statement; where the compression choke lands")
print("="*78)

print("4a. Free-fall crossing (repo framing, v = sqrt(2GM/r) = c_s):  r = 2GM/c_s^2")
print(f"    untied branch (c_s = c0/sqrt3): r = 2GM/(c0^2/3) = 6 GM/c0^2")
print(f"    locked branch (c_s = c0)      : r = 2GM/c0^2")
print()
print("4b. WHERE IT LANDS with the derived two-phase EoS:")
print("    Bernoulli on the gas branch:  v^2/2 + (c0^2/3) ln(rho/rho_0) = GM/r.")
print("    With v = sqrt(2GM/r) the two terms cancel identically -> rho = rho_0 everywhere:")
print("    the free-fall profile never compresses the gas branch (test-particle limit),")
print("    so the compression choke lands exactly where v = c_s(rho_0) = c0/sqrt(3):")
print(f"        r_choke = 6 GM/c0^2   (the untied endpoint of the window).")
rfold = 3.0/(np.log(rhomax/(2.0*rho0)))     # in GM/c0^2 units, where rho = rho_max/2
vfold = np.sqrt(2.0*3.0/np.log(rhomax/(2*rho0)))*1.0  # v at the fold, units c0  (recompute cleanly below)
print(f"    were the flow to reach the fold density rho_max/2 on this branch: "
      f"r = {rfold:.5f} GM/c0^2,")
v_at_fold = np.sqrt(2.0*G*(1.0)/ (rfold))    # units of (G M)^0 * ... careful, do algebra below
v_at_fold = np.sqrt(2.0/rfold)               # v = sqrt(2GM/r), r = rfold*GM/c0^2 -> v = c0*sqrt(2/rfold)
print(f"    v there = sqrt(2GM/r) = {v_at_fold:.4f} c0  > c0  -> superluminal; the transition cannot be")
print(f"    reached acoustically; the medium locks at the terminal stall (row 24: c_loc^2 + v^2 = c0^2,")
print(f"    c_loc = 0 at 2GM/c0^2).")
print()
print("4c. Steady-flow sonic radius (full momentum equation, cross-check):")
print("    (v^2-c_s^2) v'/v = 2c_s^2/r - GM/r^2  ->  r_s = GM/(2 c_s^2),  h(rho_s) = (3/2) c_s^2")
print(f"    untied branch: rho_s = rho_0 e^(3/2) = {np.exp(1.5):.4f} rho_0,  r_s = 1.5 GM/c0^2")
print(f"    locked branch: r_s = 0.5 GM/c0^2")
print("    (the repo's window uses the free-fall crossing; the steady-flow sonic point is a factor")
print("     4 inward because the pressure gradient carries part of the pull -- repo OPEN_WORK.md:41")
print("     already flags that all choke radii used empty-space infall.)")
print()
print("4d. Locking-rate ramp and the window interior:")
print("    family: c_s^2 = c0^2 [1 - (2/3)(1 - rho/rho_g*)^m]  (m = locking rate; causal for m >= 1)")
print("    (sonic condition solved in log density, u = ln rho)")
for m in [1.0, 2.0, 4.0, 8.0]:
    def cs2(x):  return c0**2*(1.0 - (2.0/3.0)*(1.0-x)**m)
    def H_of(u): # enthalpy increment h(rho0 e^u) = int_0^u c_s^2(rho0 e^t) dt
        return quad(lambda t: cs2(rho0*np.exp(t)/rhog), 0.0, u)[0]
    def F_u(u):  # sonic condition h = (3/2) c_s^2
        rho = rho0*np.exp(u)
        return H_of(u) - 1.5*cs2(rho/rhog)
    us = brentq(F_u, 0.0, np.log(rhomax/rho0)*0.999)
    rhos = rho0*np.exp(us)
    rs   = c0**2/(2.0*cs2(rhos/rhog))          # GM/c0^2 units
    print(f"    m={m}: rho_s = {rhos/rho0:.4f} rho_0,  r_s = {rs:.4f} GM/c0^2   (steady-flow frame)")
print("    -> the steady-flow sonic radius is RAMP-INSENSITIVE (rho_s = e^(3/2) rho_0 = 4.48 rho_0,")
print("       r_s = 1.5 GM/c0^2) for EVERY causal ramp: near rho_s the ramp correction is")
print("       O((rho_s/rho_g*)^m) ~ 1e-41, so the sonic condition reduces to the ideal-branch one.")
print("       The flow goes sonic at near-background density; the ramp acts only deep in the")
print("       supersonic region. The repo's window [2, 6] GM/c0^2 is the free-fall crossing")
print("       r = 2GM/c_s^2: the two-phase EoS lands it at exactly 6 GM/c0^2 (c_s = c0/sqrt3 all")
print("       the way to the fold); populating the window interior requires the ramp S(rho)")
print("       (missing input -- the alignment law).")
print()
print("4e. Yield/choke crossover masses (r_yield = sqrt(GM/a) vs the landed choke 6 GM/c0^2):")
for lab, a in [("derived a_hold(rho_max) = 3.1353e11", ah1), ("sealed yield = 3.23e11", a_yield)]:
    M36 = c0**4/(36.0*G*a)
    M4  = c0**4/(4.0*G*a)
    print(f"    {lab:<36}: M(choke=6GM/c0^2) = c0^4/(36 G a) = {M36/Msun:.2f} Msun ;   "
          f"M(choke=2GM/c0^2) = c0^4/(4 G a) = {M4/Msun:.2f} Msun")
print("    -> landing at 6 GM/c0^2 puts the crossover at ~5.2-5.4 Msun, at the 3-5 Msun mass gap")
print("       (repo OPEN_WORK.md:34 called this a coincidence until derived).")
print()
print("4f. Consistency: derived yield vs the GW150914 shell edge (M=62 Msun, edge 159.6 km):")
M914 = 62.0*Msun
r_edge_derived = np.sqrt(G*M914/ah1)
r_edge_sealed  = np.sqrt(G*M914/a_yield)
print(f"    sqrt(GM/a_hold(derived)) = {r_edge_derived/1e3:.1f} km ;  sqrt(GM/a(sealed)) = "
      f"{r_edge_sealed/1e3:.1f} km  (repo edge = 159.6 km)")

# =====================================================================
print()
print("="*78)
print("SUMMARY OF PASS / FAIL")
print("="*78)
print(f" [PASS] a_hold(rho_0)   = {ah0:.4e}  vs a0 = {a0_meas:.3e}  ({100*(ah0/a0_meas-1):+.2f}%)")
print(f" [FAIL-2.93%] a_hold(rho_max) = {ah1:.4e}  vs sealed {a_yield:.3e}  ({100*(ah1/a_yield-1):+.2f}%)  -- needs cohesion channel Y(rho_max)")
print(f" [PASS] fold at rho_max/2 emerges from L = c0^2 = P_s v_s (dv = v_s).")
print(f" [PASS] c_s(rho) <= c0 everywhere (max = c0 at the locked branch).")
print(f" [PASS] continuous causal bridge forbidden (MVT: 5/3 c0^2 and 2 c0^2 > c0^2); equal-area fails (ln2 < 1).")
print(f" [PASS] 5.3% chain reproduces rho_0 (T2: -1.5% with derived a_hold, -0.5% with measured a0);")
print(f"        Y_cav = {Ycav:.3e} Pa; v_cav = {vcav/c0:.4f} c0; water 6.36% vs 5.26%.")
print(f" [PASS] compression choke lands at 6 GM/c0^2 (derived); crossover {M36/Msun:.2f} Msun.")
print(f" [OPEN] missing inputs: Y(rho) pairing yank (epsilon_0), transition temperature T*,")
print(f"        surface-tension regularization kappa_C, alignment law S(rho,T) (locking ramp),")
print(f"        and H0 for the exact 95% figure.")
