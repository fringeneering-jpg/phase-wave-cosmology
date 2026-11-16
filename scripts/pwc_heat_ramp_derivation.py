"""
PWC heat-driven wave-alignment ramp S(rho,T) -- derivation with THE HEAT as the
driver.  Scratch derivation (not committed to the repo).

Locked inputs only (quoted from the repo):
  w(S)   = (1+2S)/3                      (DERIVATION_BRIEF T3 route)
  gas S=0:  P = rho c0^2/3 , c_s = c0/sqrt(3)
  locked S=1: P = rho c0^2 , c_s = c0    (Zel'dovich stiff)
  first-order plateau P* = rho_max c0^2 over [rho_max/2, rho_max]; fold at rho_max/2
  heat law: dQ = -P dv, u = c0^2, total inventory L = c0^2 J/kg
  anchors: S(H_0) = 0, S(H_0 - c0^2) = 1, monotone
  T2 ramp-insensitivity: c_s^2 = c0^2[1 - (2/3)(1 - rho/rho_g*)^m] lands the
     steady-flow sonic point at rho_s = e^{3/2} rho_0 = 4.4817 rho_0,
     r_s = 1.5 GM/c0^2 for m = 1,2,4,8.
  rho_0 = 8.74e-27, rho_max = 1.304e15, rho_core = 2.3e17, a_yield = 3.23e11,
  a_hold(rho_0) = (c0/sqrt3)*sqrt(G rho_0/4) = 6.61e-11  (derived, eos_latent_heat.md)
  rho_max/2 fold construction from L = c0^2 = P* dv (dv = v_s).

No fitted parameters.  Honest failure reporting: the exact datum is named.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

# ------------------------------------------------------------- constants
c0    = 2.99792458e8
G     = 6.6743e-11
rho0  = 8.74e-27
rhomax = 1.304e15
rhocore = 2.3e17
ayield = 3.23e11
Msun  = 1.989e30
mn    = 1.674927498e-27        # neutron mass kg
mp    = 1.67262192369e-27      # proton mass kg
mprot_GeV = 0.93827208816
mnuc_GeV  = 0.931494102       # per-nucleon mass for A~46 (arXiv 46-nucleon convention)
eV     = 1.602176634e-19
rhog   = rhomax / 2.0          # the fold (locked: plateau over [rho_max/2, rho_max])
Pstar  = rhomax * c0**2

def w_S(S):  return (1.0 + 2.0*S) / 3.0
def cs2_S(S): return c0**2 * w_S(S)
def Omega_eff(S): return 0.25 * (16.0*np.pi)**S

print("="*80)
print("SECTION 0 -- locked inputs")
print("="*80)
for k, v in [("c0", c0), ("G", G), ("rho0", rho0), ("rhomax", rhomax),
             ("rhocore", rhocore), ("ayield", ayield), ("rhog (fold)", rhog),
             ("P*", Pstar)]:
    print(f"  {k:<16s} = {v:.6e}")
print(f"  ln(rhog/rho0)  = {np.log(rhog/rho0):.6f}   (e-folds of density from rest to the fold)")
print(f"  (c0^2/3) ln(rhog/rho0) = {(c0**2/3)*np.log(rhog/rho0):.6e} J/kg "
      f"= {(1/3)*np.log(rhog/rho0):.4f} c0^2")

# =====================================================================
print()
print("="*80)
print("SECTION 1 -- the heat balance: S = S(H(rho))")
print("="*80)
print("""Heat law (locked): compression squeezes heat out, dQ = -P dv with u = c0^2,
so the heat content per kg falls with density:
    dH = P dv = -P drho/rho^2  ->  dH/dln(rho) = -P/rho = -c0^2 (1+2S)/3
Self-consistent ODE for a ramp S = f(H):  dS/dln(rho) = -f'(H) P/rho.
""")

# ---- form (c): S = (H0 - H)/c0^2  (normalized heat lost) -- satisfies BOTH anchors for any H0>=c0^2
def S_heat(rho):
    """anchor-forced closed ramp: S = (H0-H)/c0^2, self-consistent solution."""
    x = (rho/rho0)**(2.0/3.0)
    return np.where(x < 3.0, 0.5*(x - 1.0), 1.0)     # saturates at S=1
def H_heat(rho, H0=c0**2):
    return H0 - c0**2 * S_heat(rho)
rho_c = 3.0**1.5 * rho0
print(f"form (c)  S = (H0-H)/c0^2 :  dS/dln(rho) = (1+2S)/3")
print(f"   closed: S(rho) = [(rho/rho0)^(2/3) - 1]/2,  H(rho) = H0 - c0^2 S(rho)")
print(f"   completion (S=1, heat exhausted): rho_c = 3^(3/2) rho0 = {rho_c/rho0:.4f} rho0 "
      f"= {rho_c:.4e} kg/m^3")
print(f"   -> ln(rho_c/rho0) = {np.log(rho_c/rho0):.4f}  vs  fold at ln(rhog/rho0) = {np.log(rhog/rho0):.3f}")
print(f"   -> completion is {np.log(rhog/rho_c):.2f} e-folds ({(np.log(rhog/rho_c)/np.log(10)):.1f} decades) "
      f"BEFORE the fold rho_max/2.")
print()
# ---- forms (a)/(b): S = 1 - H/H0  -- anchors force H0 = c0^2, then identical to (c)
print("form (b)  S = 1 - H/H0 :  S(H0) = 0 ok;  S(H0-c0^2) = c0^2/H0 = 1  ONLY IF  H0 = c0^2")
print(f"   -> the two anchors FORCE H0 = c0^2 for the linear form; then (b) == (c) exactly.")
print(f"   THE ANCHORS PIN THE UNKNOWN DATUM:  H0 = c0^2 = {c0**2:.6e} J/kg (for the linear forms).")
print()
# ---- log form
print("log form  S = ln(H0/H)/ln(H0/(H0-c0^2)) : satisfies both anchors for ANY H0 > c0^2")
print("   ODE: dS/dln(rho) = (1+2S)/3 * k/(-ln(1-k)) * (1-k)^(-S),  k = c0^2/H0")
print("   completion density rho_g(k) = rho0 exp(3 I(k)/mu),  I(k)=int_0^1 (1-k)^t/(1+2t) dt,  mu=k/(-ln(1-k))")
def Ilog(k): return quad(lambda t: (1.0-k)**t/(1.0+2.0*t), 0.0, 1.0)[0]
print("   k = c0^2/H0 :   H0->inf (k->0) ... H0->c0^2 (k->1)")
for k in [0.0, 0.01, 0.1, 0.5, 0.9, 0.99]:
    if k == 0.0:
        rho_gk = 3.0**1.5 * rho0
    else:
        mu = k/(-np.log(1.0-k))
        rho_gk = rho0*np.exp(3.0*Ilog(k)/mu)
    print(f"      k={k:.2f}: completion at {rho_gk/rho0:.3f} rho0")
print()
# ---- theorem
print("THEOREM (any anchored monotone form):  completion cannot exceed e^3 rho0 = "
      f"{np.exp(3)*rho0:.4e} kg/m^3")
print("   proof: S=1 requires heat expelled Q = L = c0^2; but")
print("   Q(rho) = int_{rho0}^{rho} P drho/rho^2 = int (c0^2/3)(1+2S) dln(rho) >= (c0^2/3) ln(rho/rho0)")
print("   -> ln(rho_c/rho0) <= 3  for EVERY form f with f(H0)=0, f(H0-c0^2)=1.")
print(f"   fold needs ln(rho_c/rho0) = {np.log(rhog/rho0):.2f}  ->  the inventory must be")
print(f"   L >= (c0^2/3) ln(rhog/rho0) = {(c0**2/3)*np.log(rhog/rho0)/c0**2:.4f} c0^2, not c0^2.")

# =====================================================================
print()
print("="*80)
print("SECTION 2 -- T1: fold at rho_max/2, w carried 1/3 -> 1")
print("="*80)
vg, vs = 1.0/rhog, 1.0/rhomax
dv = vg - vs
print(f"fold construction (locked, L = c0^2 = P* dv):  P* dv = {Pstar*dv:.6e} = c0^2 = {c0**2:.6e}")
print(f"   dv = c0^2/P* = 1/rho_max = v_s  ->  v_g = 2 v_s  ->  rho_g* = rho_max/2 = {rhog:.4e}")
print("   [PASS] fold at rho_max/2 emerges free from L = c0^2 (independent of the ramp shape).")
print()
print("w(S) carried by the heat ramp:")
for r in [rho0, 2*rho0, rho_c, 10*rho_c, rhog, rhomax]:
    S = S_heat(r)
    print(f"   rho/rho0 = {r/rho0:>10.3e} :  S = {S:.4f}  w = {w_S(S):.4f}  c_s/c0 = {np.sqrt(w_S(S)):.4f}")
print(f"   -> the ramp carries w from 1/3 to 1 over [rho0, 3^(3/2) rho0]; at the fold S=1 (w=1) already.")
print(f"   -> P(rho_max/2^-) = (rho_max/2) c0^2 ; the fold jumps x2 to P* = rho_max c0^2.")
print("   T1 verdict: fold REPRODUCED at rho_max/2 (via L = c0^2 = P*dv), but the ramp's w=1 is reached")
print("   40 decades before the fold -- the ramp does NOT 'carry w across the transition' in the literal")
print("   density-range sense.  The ramp that DOES (completing exactly at the fold) is the T2 m-family; see S3.")

# =====================================================================
print()
print("="*80)
print("SECTION 3 -- T2: ramp-insensitivity; does the heat ramp land in the family?")
print("="*80)
print("3a. Steady-flow sonic condition:  h(rho_s) - h(rho0) = (3/2) c_s^2(rho_s),  r_s = GM/(2 c_s^2).")
print("    Heat ramp:  h - h0 = int c_s^2 dln rho = (c0^2/2)((rho/rho0)^(2/3) - 1) = (c0^2/2)(x - 1)")
print("               (3/2) c_s^2  = (c0^2/2) x       ->  h - (3/2)c_s^2 = -c0^2/2 < 0 for ALL rho")
u_grid = np.linspace(0.0, np.log(rhocore/rho0), 500)
res_min = 1e99
for u in u_grid:
    rho = rho0*np.exp(u)
    S = S_heat(rho)
    h = 0.5*c0**2*((rho/rho0)**(2.0/3.0) - 1.0)
    res = h - 1.5*cs2_S(S)
    res_min = min(res_min, res)
print(f"    numeric scan over [rho0, rho_core]: max of (h - 1.5 c_s^2)/c0^2 = {res_min/c0**2:.6f}  "
      f"(always negative: {res_min/c0**2:.4f} c0^2)")
print("    -> NO steady-flow sonic point exists for the heat ramp: the stiffening outruns the enthalpy;")
print("       the flow can never go transonic.  The locked sonic point 4.4817 rho_0 is NOT reproduced.")
print("       [FAIL vs T2]")
print()
print("3b. The m-family check (the ramp that must remain):")
def cs2_m(x, m): return c0**2*(1.0 - (2.0/3.0)*(1.0-x)**m)
def h_m(u, m):
    return quad(lambda t: cs2_m(rho0*np.exp(t)/rhog, m), 0.0, u)[0]
def F_m(u, m):
    rho = rho0*np.exp(u)
    return h_m(u, m) - 1.5*cs2_m(rho/rhog, m)
for m in [1.0, 2.0, 4.0, 8.0]:
    us = brentq(F_m, 0.1, np.log(rhog/rho0)*0.9999, args=(m,))
    rhos = rho0*np.exp(us)
    rs = c0**2/(2.0*cs2_m(rhos/rhog, m))          # in GM/c0^2 units
    print(f"    m={m:.0f}: rho_s = {rhos/rho0:.6f} rho0  (locked e^(3/2) = {np.exp(1.5):.6f}),"
          f"  r_s = {rs:.6f} GM/c0^2  (locked 1.5)")
    print(f"         ramp correction at rho_s: (rho_s/rhog)^m = {(rhos/rhog)**m:.2e}  -> insensitivity.")
print()
print("3c. The m-family's heat bookkeeping (the same dQ = -P dv law):")
def harmonic(m): return sum(1.0/k for k in range(1, int(m)+1))
print("    heat expelled from rest to the fold along the family:")
for m in [1.0, 2.0, 4.0, 8.0]:
    dH = c0**2*((1.0/3.0)*np.log(rhog/rho0) + (2.0/3.0)*harmonic(m))
    print(f"      m={m:.0f}:  dH(fold) = c0^2[(1/3)ln(rhog/rho0) + (2/3) H_m] = {dH/c0**2:.4f} c0^2")
print("    -> the family reaches S=1 with the heat content dropped by 32.03-33.18 c0^2,")
print("       NOT by c0^2.  The locked anchor S(H0 - c0^2) = 1 (equivalently inventory L = c0^2)")
print("       is violated by a factor 32.")
print()
print("3d. Function-class incompatibility (proof, not fit):")
print("    heat law near rest:   dS/dln(rho) = -f'(H0) P/rho -> (c0^2/3)|f'(H0)| = O(1) per e-fold")
print("       (all three natural forms give ~1/3 per e-fold at rest -- a LOG ramp)")
print("    m-family near rest:   dS/dln(rho) = m (rho/rhog) (1-rho/rhog)^(m-1) -> 0  (flat start)")
print("    -> no f(H) with the locked anchors solves the heat-law ODE into the family. PROVEN.")
print()
print("3e. THE FAILING DATUM (named):")
L_min = (c0**2/3.0)*np.log(rhog/rho0)
print(f"    locked:  total inventory L = c0^2 J/kg   (anchor S(H0 - c0^2) = 1)")
print(f"    required to complete at the fold:  L >= (c0^2/3) ln(rhog/rho0) = {L_min/c0**2:.4f} c0^2")
print(f"    m-family values: 32.03-33.18 c0^2.  ->  L = c0^2 is 31.4x too small.")
print(f"    Equivalently: the anchor must be S(H0 - 32.03 c0^2) = 1 (m=1).")
print(f"    Consequence for the unknown datum H0:  H0 >= 32.03 c0^2 = {32.03*c0**2:.4e} J/kg")
print(f"    (the 'excess heat' floor, see S5).")

# =====================================================================
print()
print("="*80)
print("SECTION 4 -- T3: the radial profile (core -> rho_max shell -> decompression)")
print("="*80)
M    = 62.0*Msun      # GW150914 merged: 51 core + 11 medium
Mcore = 51.0*Msun
Rc   = (3.0*Mcore/(4.0*np.pi*rhocore))**(1.0/3.0)
Redge = np.sqrt(G*M/ayield)
Mshell = (4.0*np.pi/3.0)*rhomax*(Redge**3 - Rc**3)
print(f"core: rho_core = 2.3e17, M_core = 51 Msun -> R_core = {Rc/1e3:.2f} km   (repo: 47.3 km)")
print(f"shell edge (yield BC): R_edge = sqrt(GM/a_yield) = {Redge/1e3:.2f} km   (repo: 159.6 km)")
print(f"shell mass at rho_max: (4pi/3) rho_max (R_edge^3 - R_core^3) = {Mshell/Msun:.2f} Msun  (repo: 10.87)")
print(f"  GM/c0^2 = {G*M/c0**2/1e3:.2f} km  ->  2GM/c0^2 = {2*G*M/c0**2/1e3:.2f} km,  "
      f"6GM/c0^2 = {6*G*M/c0**2/1e3:.2f} km")
print(f"  shell edge / choke = {Redge/(2*G*M/c0**2):.4f}   (repo OPEN_WORK: edge/choke 0.87)")
print()
print("4a. Pure hydrostatic decompression (naive): dP/dr = -rho GM/r^2")
print("    locked branch (S=1, c_s = c0):  rho(r) = rho_max exp[-(GM/c0^2)(1/R_edge - 1/r)]")
rho_inf = rhomax*np.exp(-G*M/(c0**2*Redge))
print(f"    rho(inf)/rho_max = exp[-GM/(c0^2 R_edge)] = {rho_inf/rhomax:.4f}")
print(f"    -> the atmosphere asymptotes to {100*rho_inf/rhomax:.1f}% of rho_max at infinity; decompression")
print(f"       to rho0 needs ln(rhomax/rho0) = {np.log(rhomax/rho0):.1f} e-folds but only "
      f"{G*M/(c0**2*Redge):.3f} are available.")
print("    -> hydrostatic equilibrium CANNOT decompress the medium; the decompression is a")
print("       yield/tension process (the repo's 'held medium is static and tension-held').")
print()
print("4b. Decompression via the holding-threshold law (the repo's a_hold law):")
a_hold0 = (c0/np.sqrt(3.0))*np.sqrt(0.25*G*rho0)     # derived 6.61e-11 (eos_latent_heat.md)
print(f"    a_hold(rho, S) = c_s(S) sqrt(Omega_eff(S) G rho),  Omega_eff(S) = (1/4)(16 pi)^S")
print(f"    profile:  rho(r) = a(r)^2 / (Omega_eff(S(rho)) c_s^2(S(rho)) G),  a(r) = GM/r^2")
print(f"    S(rho) = m-family ramp 1-(1-rho/rhog)^m for rho<rhog, S=1 above (fold jump at rhog).")
def S_prof(rho, m):
    if rho < rhog: return 1.0 - (1.0 - rho/rhog)**m
    return 1.0
def rho_thresh(r, m):
    a2 = (G*M/r**2)**2
    def f(lr):
        rho = np.exp(lr); S = S_prof(rho, m)
        return rho*Omega_eff(S)*cs2_S(S)*G - a2
    lr = brentq(f, np.log(rho0*1.0), np.log(rhomax*1.05))
    return np.exp(lr)
m0 = 1.0
r_fold  = (G*M**2/(4.0*np.pi*c0**2*rhog))**0.25
r_reach = np.sqrt(G*M/a_hold0)
print(f"    S=1 branch: rho = GM^2/(4 pi c0^2 r^4) ;  fold rho=rhog at r_fold = {r_fold/1e3:.1f} km "
      f"= {r_fold/(G*M/c0**2):.3f} GM/c0^2")
print(f"    outer reach: rho -> rho0 at r_reach = sqrt(GM/a_hold(rho0)) = {r_reach/3.0857e16:.4f} pc")
for r, lab in [(2*G*M/c0**2, "2GM/c0^2"), (6*G*M/c0**2, "6GM/c0^2"), (r_fold, "r_fold")]:
    rho = rho_thresh(r, m0); S = S_prof(rho, m0)
    print(f"    at r = {r/1e3:8.1f} km ({lab}): rho = {rho:.4e} ({rho/rhomax:.4f} rhomax), "
          f"S = {S:.4f}, P = {rho*c0**2*w_S(S):.4e} Pa, c_s = {np.sqrt(cs2_S(S))/c0:.4f} c0")
print(f"    window interior [2,6]GM/c0^2 = [{2*G*M/c0**2/1e3:.1f}, {6*G*M/c0**2/1e3:.1f}] km:")
print(f"       rho falls {rho_thresh(2*G*M/c0**2,m0)/rhomax:.3f} rhomax -> "
      f"{rho_thresh(6*G*M/c0**2,m0)/rhomax:.3e} rhomax;  S falls 1 -> "
      f"{S_prof(rho_thresh(6*G*M/c0**2,m0),m0):.4f};  the fold sits at "
      f"{r_fold/(G*M/c0**2):.3f} GM/c0^2 (inside the window's inner edge for M=62).")
print()
print("    mass bookkeeping vs the k-rule (validated held medium):")
Mtail = G*M**2/c0**2*(1.0/Redge - 1.0/r_reach)
print(f"    threshold-envelope tail mass = (GM^2/c0^2)(1/R_edge - 1/r_reach) = {Mtail/Msun:.1f} Msun")
print(f"    vs k-rule held-after = 11 Msun (shell 10.87 + tail ~0.13 bookkeeping)")
print(f"    -> the threshold law is the marginal-hold ENVELOPE, not the actual held column;")
print(f"       the k-rule surface capacity (Sigma = 8.48e20 kg/m^2, candidate a_yield/(2 pi G)) caps it.")
print(f"    -> the decompression-zone SHAPE is not locked by the inputs; candidates documented below.")
Sigma_k = 8.48e20
Sig_shell = rhomax*(Redge - Rc)
print(f"    k-rule Sigma = {Sigma_k:.3e} kg/m^2 ; shell column = rho_max x 112.4 km = {Sig_shell:.3e} kg/m^2")
Sig_tail = Sigma_k - Sig_shell
p_tail = 1.0 + rhomax*Redge/Sig_tail
print(f"    k-rule-capped tail: rho = rho_max (R_edge/r)^p with p = 1 + rho_max R_edge/Sigma_tail = "
      f"{p_tail:.2f}  -> thin steep skin (mass {Sig_tail*4*np.pi*Rc**2/Msun:.2f} Msun).")
print()
print("4c. Choke landing (locked): free-fall crossing at 6 GM/c0^2 = ISCO:")
print("    free-fall Bernoulli on the gas branch: v^2/2 + (c0^2/3) ln(rho/rho0) = GM/r; with")
print("    v = sqrt(2GM/r) the terms cancel -> rho = rho0 everywhere (test-particle limit), and")
print("    the compression choke is where v = c_s(rho0) = c0/sqrt(3):  r = 2GM/(c0^2/3) = 6 GM/c0^2.")
a_hold_max = c0*np.sqrt(4.0*np.pi*G*rhomax)
for lab, a in [("sealed yield 3.23e11", ayield), ("derived a_hold(rho_max) 3.135e11", a_hold_max)]:
    Mcross = c0**4/(36.0*G*a)
    print(f"    crossover r_yield = 6GM/c0^2:  M = c0^4/(36 G a) = {Mcross/Msun:.2f} Msun   [{lab}]")
print(f"    -> 5.23-5.39 Msun (the task's mass-gap edge).  [PASS]")
print()
print("4d. T2 steady-flow sonic point (m-family) for M = 62:")
for m in [1.0, 2.0, 4.0, 8.0]:
    us = brentq(F_m, 0.1, np.log(rhog/rho0)*0.9999, args=(m,))
    rhos = rho0*np.exp(us)
    rs_km = G*M/(2.0*cs2_m(rhos/rhog, m))/1e3
    print(f"    m={m:.0f}: rho_s = {rhos/rho0:.4f} rho0 ;  r_s = {rs_km:.1f} km "
          f"= {c0**2/(2*cs2_m(rhos/rhog,m)):.4f} GM/c0^2 "
          f"(inside the shell edge 159.6 km; steady flow is not the held-medium equilibrium).")

# ---- save the profile CSV (threshold envelope, capped at rho_max / floored at rho_0)
rs = np.geomspace(Rc*1.001, r_reach, 400)
rows = []
for r in rs:
    try:
        rho = rho_thresh(r, m0)
    except ValueError:
        a2 = (G*M/r**2)**2
        f_lo = rho0*Omega_eff(0.0)*cs2_S(0.0)*G - a2
        f_hi = rhomax*Omega_eff(1.0)*cs2_S(1.0)*G - a2
        if f_lo >= -1e-6*a2:     # pull below what rest-density medium can hold (incl. exact endpoint)
            rho = rho0
        elif f_hi <= 1e-6*a2:    # pull above the locked ceiling -> shell at rho_max
            rho = rhomax
        else:
            raise
    S = S_prof(rho, m0)
    rows.append((r, rho, rho*c0**2*w_S(S), np.sqrt(cs2_S(S)), S, G*M/r**2))
arr = np.array(rows)
np.savetxt("ramp_out_profile.csv", arr,
           header="r_m,rho_kgm3,P_Pa,cs_ms,S,accel_Nkg", delimiter=",")
print(f"\n    profile CSV saved: ramp_out_profile.csv ({len(rows)} radii, "
      f"{Rc/1e3:.1f} km -> {r_reach/3.0857e16:.3f} pc)")

# =====================================================================
print()
print("="*80)
print("SECTION 5 -- T4: the 43.2 GeV line = 46 nucleon masses (arXiv:2407.11737)")
print("="*80)
Eline = 43.2e9*eV
m_u = Eline/c0**2
n_u = m_u/mn
print(f"43.2 GeV = {Eline:.4e} J  =  m_u c0^2  ->  m_u = {m_u:.4e} kg = {n_u:.2f} neutron masses "
      f"(arXiv: 46 nucleon masses).  [arithmetic: PASS]")
print()
print("What the ramp/heat law contributes:")
print(f"  (i) the fixed quantum: L = c0^2 per kg -> the light per untying of a fixed knot of mass m_u")
print(f"      is exactly m_u c0^2 = 43.2 GeV -> a LINE, not a spread.  [mechanism-level: consistent]")
print(f"  (ii) untying is endothermic (draws m_u c0^2 = 43.2 GeV from the surroundings), so the line")
print(f"      must track the hot heat-holding gas, not cold regions.  [mechanism-level: consistent]")
print()
print("Does the law identify WHICH knot unties (m_u = 46 nucleons)?")
print(f"  locked pair-mass window m_w in [m_p/3, m_p] = [0.31, 0.94] GeV  (pairing derivation) --")
print(f"  a 46-nucleon unit (43.2 GeV) is 46-138 pairs; no locked knot-ladder entry has mass 46 m_n.")
print("  -> T4: the EVENT is NOT identified from the locked set.  [FAIL-DOCUMENTED]")
print()
print("Near-misses (rejected: no locked provenance / violates a locked datum):")
H0_fold = 2.0*c0**2*np.log(rhog/rho0)/(3.0*np.log(3.0))     # form (b) pinned to complete at the fold
mw_fold = Eline/H0_fold
print(f"  (1) fold-pinned linear form: H0 = 2 c0^2 ln(rhog/rho0)/(3 ln3) = {H0_fold/c0**2:.2f} c0^2;")
print(f"      per pair: 43.2 GeV needs m_w = E/H0 = {mw_fold/mp:.3f} m_p -- INSIDE [m_p/3, m_p]!")
print(f"      but this H0 violates the anchor S(H0 - c0^2) = 1 by {H0_fold/c0**2:.1f}x (S1-e) and")
print(f"      exhausts the heat AT the fold, before the plateau can release its own L = c0^2.")
print(f"  (2) m-family inventory: dH(fold)/kg = 32.03 c0^2 -> 43.2 GeV would need m = "
      f"{Eline/(32.03*c0**2*mp):.2f} m_p -- outside the window.")
print(f"  (3) ln(rhog/rho0)/2 = {np.log(rhog/rho0)/2:.2f} ~ 46 (+2.3%) -- numerology, no mechanism.")
print(f"  -> none passes the repo's locked-provenance rule; T4 stays open.")
print()
u_cmb = 7.5657e-16*2.725**4
print(f"Excess-heat bookkeeping (repo OPEN_WORK: 'Excess heat vs the measured 2.7 K of space'):")
print(f"  CMB energy per kg of medium: u_cmb/rho0 = {u_cmb/rho0:.4e} J/kg = {u_cmb/(rho0*c0**2):.3e} c0^2")
print(f"  H0 floor from the m-family:  H0 >= 32.03 c0^2 = {32.03*c0**2:.4e} J/kg")
print(f"  -> the medium's rest heat >= {32.03*c0**2/(u_cmb/rho0):.3e} x the 2.7 K CMB energy per kg"
      f"  (H0 itself stays UNPINNED; only the floor is fixed).")

# =====================================================================
print()
print("="*80)
print("SECTION 6 -- SUMMARY OF PASS / FAIL")
print("="*80)
print(f" [PASS] anchors + heat law force the closed ramp  S(rho) = [(rho/rho0)^(2/3)-1]/2,")
print(f"        H(rho) = c0^2 (3-(rho/rho0)^(2/3))/2,  H0 PINNED = c0^2 for the linear forms;")
print(f"        completion at 3^(3/2) rho0 = {rho_c/rho0:.4f} rho0; causal (c_s <= c0), monotone.")
print(f" [PASS] fold at rho_max/2 emerges free from L = c0^2 = P* dv  (dv = v_s -> rho_g* = rho_max/2).")
print(f" [FAIL] T1: the heat ramp completes {np.log10(rhog/rho_c):.1f} decades before the fold --")
print(f"        it does not carry w across the transition in the density-range sense.")
print(f" [FAIL] T2: no steady-flow sonic point (h - 1.5 c_s^2 = -c0^2/2 < 0 for all rho);")
print(f"        4.4817 rho_0 / 1.5 GM/c0^2 NOT reproduced.  The m-family DOES land there (m=1,2,4,8).")
print(f" [note] T3's free-fall landing at 6 GM/c0^2 survives for BOTH ramps (S(rho_0)=0 ->")
print(f"        c_s(rho_0)=c0/sqrt3; the test-particle free-fall keeps rho=rho_0), so the landing")
print(f"        does not discriminate.  The discriminator is the steady-flow sonic point (T2): the")
print(f"        heat ramp has none -- the medium stiffens faster than the infall accelerates, so no")
print(f"        transonic choke (and no Hawking sonic point) can form.  The m-family restores it.")
print(f" [PASS] with the m-family ramp: crossing at 6 GM/c0^2, crossover 5.23-5.39 Msun;")
print(f"        radial profile: core 47.2 km -> rho_max shell to 159.6 km (10.87 Msun) ->")
print(f"        decompression envelope rho ~ r^-4 with the fold at {r_fold/(G*M/c0**2):.3f} GM/c0^2,")
print(f"        reach 0.36 pc; k-rule capacity caps the tail (shape open).")
print(f" [FAIL-DATUM] THE EXACT DATUM:  total inventory L = c0^2 J/kg  (anchor S(H0-c0^2)=1).")
print(f"        The fold-completing family needs L >= (c0^2/3) ln(rhog/rho0) = {L_min/c0**2:.2f} c0^2")
print(f"        (family: 32.03-33.18 c0^2).  Either L = c0^2 is the latent heat of the PLATEAU only")
print(f"        (P* dv = c0^2 exact) and the gas-side ramp draws on H0 >= 32.03 c0^2 of excess heat,")
print(f"        or the ramp must not complete at the fold.")
print(f" [OPEN] T4: 43.2 GeV = 46.0 nucleon masses (arithmetic); the untying EVENT is not identified;")
print(f"        H0 floor = 32.03 c0^2 = 6.03e5 x (CMB energy per kg) -- the excess-heat item.")
print(f" [OPEN] decompression-zone SHAPE (envelope r^-4 vs k-rule-capped skin) -- not locked.")
