"""
PWC pairing derivation -- epsilon_0 and mu_0 from the medium's paired-wave
structure, and the cohesion channel of the holding-yield anchor (the last
2.93%).

Locked inputs only:  {rho_0, rho_max, c0, G, m_p, R_p, hbar}  (+ locked targets
eps0_SI, mu0_SI, a_yield, Y_cav, s = 0.053 -- used as TARGETS to compare
against, never as inputs to a coefficient).

Targets:
  T1.  c0 = 1/sqrt(mu0 eps0) = 2.99792458e8 EXACTLY, with eps0 = 8.8541878128e-12
       F/m and mu0 = 1.25663706212e-6 N/A^2 individually matched.
  T2.  a_coh(rho_max) = sqrt(3.23^2 - 3.1352^2) e11 = 7.77e10 N/kg from the yank.
  T3.  Y_cav(rho_0) = s rho_0 c0^2/3 = 1.3781e-11 Pa with s = 0.053.

No fitted parameters. No GR, no dark matter. Failures are named precisely.
"""
import numpy as np

print("=" * 78)
print("SECTION 0 -- locked inputs and targets")
print("=" * 78)

c0      = 2.99792458e8          # m/s   (locked: the medium's own speed)
eps0_SI = 8.8541878128e-12      # F/m   (SI target, T1)
mu0_SI  = 1.25663706212e-6      # N/A^2 (SI target, T1)
G       = 6.6743e-11            # m^3 kg^-1 s^-2
rho0    = 8.74e-27              # kg/m^3  resting density of the medium
rhomax  = 1.304e15              # kg/m^3  locked ceiling
mp      = 1.6726e-27            # kg   proton / wave mass (locked window m_p/3 .. m_p)
Rp      = 0.8414e-15            # m    proton radius (720-degree knot, m_p R_p c0 = 4 hbar)
hbar    = 1.054571817e-34       # J s
s0      = 0.053                 # 5.3% remaining stretch (locked, loose end)
a_yield = 3.23e11               # N/kg sealed holding yield at rho_max (locked target)
Y_cav_T = 1.3781e-11            # Pa   locked tensile-limit target at rho_0 (T3)

for k, v in [("c0", c0), ("eps0_SI", eps0_SI), ("mu0_SI", mu0_SI), ("G", G),
             ("rho0", rho0), ("rhomax", rhomax), ("mp", mp), ("Rp", Rp),
             ("hbar", hbar), ("s0", s0), ("a_yield", a_yield), ("Y_cav_T", Y_cav_T)]:
    print(f"  {k:>9s} = {v:.10e}")

print()
print("locked holding-threshold law (solid-angle channel alone):")
a_hold = c0 * np.sqrt(4.0 * np.pi * G * rhomax)
print(f"  a_hold(rho_max) = c0 sqrt(4 pi G rho_max) = {a_hold:.6e} N/kg")
a_coh = np.sqrt(a_yield ** 2 - a_hold ** 2)
print(f"  sealed yield    = {a_yield:.4e} N/kg  ->  cohesion channel must supply")
print(f"  a_coh(rho_max)  = sqrt(3.23^2 - {a_hold/1e11:.4f}^2) e11 = {a_coh:.6e} N/kg")
print(f"  a_coh / a_hold  = {a_coh/a_hold:.6f}")
Omega_sealed = (a_yield / c0) ** 2 / (G * rhomax)
print(f"  [diagnostic] sealed yield as solid angle: Omega = {Omega_sealed:.4f} sr "
      f"(> 4 pi = {4*np.pi:.4f} sr, geometrically impossible)")
print(f"  extra solid angle the cohesion must supply: dOmega = {Omega_sealed - 4*np.pi:.4f} sr")

# =====================================================================
print()
print("=" * 78)
print("SECTION 1 -- the pairing model (Route A: lattice elasticity; Route B: energy)")
print("=" * 78)

print("""
Pairing model.  The medium is EM(+)/EM(-) waves paired at spacing
    a(rho) = (m_w / rho)^(1/3)                  (m_w in [m_p/3, m_p])
Neighbouring pairs attract via the EM yank; heat holds them apart at the
resting spacing.  The yank spring constant per bond is k = |dF_yank/da|.

Route A (lattice elasticity -- Maxwell 1861-62 reading):
    c = sqrt(E/rho),   E = k/a (1D elastic modulus),  rho = m_w/a^3
  -> c = sqrt(k a^2 / m_w)  =  a sqrt(k/m_w)          (1D chain sound speed)
  locked ruling: c = c0  ->  k(rho) = m_w c0^2 / a^2 = rho a c0^2      (1)
  Maxwell identifications (OPEN_WORK.md:121):
      1/eps0 = k/a  ->  eps0_mech = a/k = 1/(rho c0^2)                  (2)
      mu0 = density of paired waves = rho_pair = m_w/a^3                (3)
  -> mu0_mech eps0_mech = 1/c0^2  EXACTLY (identity, m_w-independent).

Route B (interaction energy density):
    u = (1/2) k (s a)^2 / a^3 = (1/2) rho c0^2 s(rho)^2                (4)
    cohesion pressure  Y = rho du/drho - u = (1/2) rho^2 c0^2 d(s^2)/drho
    -> at FIXED stretch s, Route B gives Y = 0; Route A gives
       Y = k s/(3a) = s rho c0^2/3  (force per bond, one axis of three). (5)
""")

a0  = (mp / rho0) ** (1.0 / 3.0)          # m_w = m_p
a0b = (mp / 3.0 / rho0) ** (1.0 / 3.0)    # m_w = m_p/3
k0  = mp * c0 ** 2 / a0 ** 2
k0b = (mp / 3.0) * c0 ** 2 / a0b ** 2
print("pair spacing at rest (locked window m_w in [m_p/3, m_p]):")
print(f"  m_w = m_p   : a0  = (m_p/rho0)^(1/3)   = {a0:.4f} m")
print(f"  m_w = m_p/3 : a0  = (m_p/3/rho0)^(1/3) = {a0b:.4f} m")
print("  [locked window 0.400-0.576 m reproduced]")
print()
print("yank spring constant k = m_w c0^2/a^2  (eq. 1):")
print(f"  k(m_p)   = {k0:.6e} N/m     k(m_p/3) = {k0b:.6e} N/m")
print(f"  k/a = rho0 c0^2 = {k0/a0:.6e} Pa  (= {rho0*c0**2:.6e} Pa, m_w-independent)")
print()
print("eps0_mech = a/k = 1/(rho0 c0^2):")
eps_mech = 1.0 / (rho0 * c0 ** 2)
print(f"  eps0_mech = {eps_mech:.6e}   vs   eps0_SI = {eps0_SI:.6e}")
print(f"  ratio  eps0_mech/eps0_SI = {eps_mech/eps0_SI:.6e}")
print("mu0_mech = rho_pair = rho0:")
mu_mech = rho0
print(f"  mu0_mech  = {mu_mech:.6e}   vs   mu0_SI  = {mu0_SI:.6e}")
print(f"  ratio  mu0_SI/mu0_mech   = {mu0_SI/mu_mech:.6e}")
chi = mu0_SI / rho0
print(f"  -> ONE dimensionless deficit factor chi = {chi:.6e} splits the two constants.")
print()
print("c0 from the lattice (must equal 2.99792458e8 EXACTLY):")
for lab, mw, a, k in [("m_w = m_p", mp, a0, k0), ("m_w = m_p/3", mp/3.0, a0b, k0b)]:
    c_chk = a * np.sqrt(k / mw)
    p_chk = 1.0 / np.sqrt(mu_mech * eps_mech)
    print(f"  {lab:>11s}: sqrt(k a^2/m_w) = {c_chk:.12e}  1/sqrt(mu0 eps0) = {p_chk:.12e}")

# =====================================================================
print()
print("=" * 78)
print("SECTION 2 -- T1:  c0 = 1/sqrt(mu0 eps0), and the individual constants")
print("=" * 78)

print("""
T1a (the product).  mu0_mech eps0_mech = rho0 * 1/(rho0 c0^2) = 1/c0^2 is an
IDENTITY of the pairing model -- it holds for every m_w in the locked window
and every rho.  So
      c0 = 1/sqrt(mu0 eps0) = 2.99792458e8 m/s      [EXACT -- closed]
T1b (the individual SI values).  Dimensional analysis (unit-exponent matrix):
""")
# unit exponents (kg, m, s, A)
locked = {"rho0": (1, -3, 0, 0), "rhomax": (1, -3, 0, 0), "c0": (0, 1, -1, 0),
          "G": (-1, 3, -2, 0), "mp": (1, 0, 0, 0), "Rp": (0, 1, 0, 0),
          "hbar": (1, 2, -1, 0)}
epsu = (-1, -3, 4, 2)     # F/m = A^2 s^4 kg^-1 m^-3
muu  = (1, 1, -2, -2)     # N/A^2 = kg m A^-2 s^-2
print("  locked inputs: unit exponents (kg, m, s, A):")
for kk, v in locked.items():
    print(f"    {kk:>7s}: {v}")
print(f"  eps0: {epsu}      mu0: {muu}")
print("  every locked input has A-exponent 0;  eps0 needs A^2, mu0 needs A^-2.")
print("  => eps0 and mu0 INDIVIDUALLY cannot be formed from the locked set.")
print("     Only the charge-free product [mu0 eps0] = (0,-2,2,0) = [c0^-2] exists")
print("     in its span.  (This is a proof, not a search failure.)")
print()
print("  What WOULD close the split: the charge scale.  With e = elementary charge")
e  = 1.602176634e-19          # C (exact in the 2019 SI; NOT in the locked set)
alpha = 7.2973525693e-3       # fine-structure constant (measured; NOT in the locked set)
eps_from_ae = e ** 2 / (4.0 * np.pi * alpha * hbar * c0)
mu_from_ae  = 4.0 * np.pi * alpha * hbar / (e ** 2 * c0)
print("  and alpha = e^2/(4 pi eps0 hbar c0) granted as inputs:")
print(f"    eps0 = e^2/(4 pi alpha hbar c0) = {eps_from_ae:.10e}   (SI {eps0_SI:.10e})")
print(f"    mu0  = 4 pi alpha hbar/(e^2 c0) = {mu_from_ae:.10e}   (SI {mu0_SI:.10e})")
print(f"    product = {eps_from_ae*mu_from_ae:.12e} = 1/c0^2 = {1/c0**2:.12e}  [exact]")
print(f"    deficit factor chi = mu0_SI/rho0 = {chi:.6e} = 4 pi alpha hbar/(e^2 c0 rho0) "
      f"= {4*np.pi*alpha*hbar/(e**2*c0*rho0):.6e}")
print("  => the single missing input for T1b is the charge scale {e, alpha}; in pair")
print("     language: the pair's charge magnitude and/or charge separation d.")
print()
print("  Internal-consistency realizations of the yank (each fails the locked premises):")
Q1 = a0 ** 2 * np.sqrt(2.0 * np.pi)        # monopole yank, 1/eps0 = k/a at a = a0
Q2 = a0b ** 2 * np.sqrt(2.0 * np.pi)
print(f"    monopole pair-pair yank: each pair would need net charge Q = a^2 sqrt(2 pi)")
print(f"      Q(m_p)   = {Q1:.4f} C = {Q1/e:.3e} e ;   Q(m_p/3) = {Q2:.4f} C = {Q2/e:.3e} e")
print("      -> but the pair is EM(+)/EM(-) PAIRED (neutral). Contradiction.")
p_dip  = a0 ** 3 * np.sqrt(np.pi / 6.0)    # aligned dipole-dipole, k = 24 p^2/(4 pi eps0 a^5)
p_dipb = a0b ** 3 * np.sqrt(np.pi / 6.0)
print(f"    dipole pair-pair yank: required pair dipole moment p = a^3 sqrt(pi/6)")
print(f"      p(m_p) = {p_dip:.4f} C m -> charge separation d = p/e = {p_dip/e:.3e} m")
print(f"      p(m_p/3) = {p_dipb:.4f} C m -> d = {p_dipb/e:.3e} m   (pair spacing is ~0.5 m)")
print("      -> the charges would sit ~18 orders beyond the pair spacing. Contradiction.")
a_req = k0 * eps0_SI
print(f"    '1/eps0 = k/a' with the locked lattice spring k0 = {k0:.3e} N/m forces")
print(f"      a = k0 eps0 = {a_req:.3e} m = {a_req/Rp:.3e} R_p   (sub-proton; no locked length).")
print()
print("  T1 VERDICT:")
print("    c0 = 1/sqrt(mu0 eps0)                      [EXACT CLOSURE -- identity]")
print("    eps0, mu0 individually from the locked set  [IMPOSSIBLE -- proven]")
print("    missing input: the pair charge scale (e, alpha; equivalently the pair")
print("    charge separation d).  Granting {e, alpha} reproduces both SI values")

# =====================================================================
print()
print("=" * 78)
print("SECTION 3 -- T3: the tensile limit at the loose end")
print("=" * 78)
print("""
Route A cohesion pressure (eq. 5):  Y(rho) = k s /(3 a)  -- the yank stiffness
times the failure stretch, per bond area, one tension axis of the three (the
same 1/3 as the untied EoS P = rho c0^2/3).  With k = rho a c0^2 (eq. 1):
      Y_cav(rho_0) = s rho_0 c0^2 / 3                                     (6)
Note: independent of m_w (a cancels) -- the same law for the whole window.
""")
Y_cav = s0 * rho0 * c0 ** 2 / 3.0
print(f"  k0(m_p)   = {k0:.6e} N/m ;  k0(m_p/3) = {k0b:.6e} N/m")
print(f"  Y_cav = k s/(3a):  {k0*s0/(3*a0):.6e} Pa (m_p) ;  {k0b*s0/(3*a0b):.6e} Pa (m_p/3)")
print(f"  Y_cav = s rho0 c0^2/3 = {Y_cav:.6e} Pa")
print(f"  locked T3 target     = {Y_cav_T:.6e} Pa   ->  {100*(Y_cav/Y_cav_T-1):+.2f}%")
s_implied = 3.0 * Y_cav_T / (rho0 * c0 ** 2)
print(f"  [bookkeeping] the locked target 1.3781e-11 implies s = {s_implied:.6f},")
print(f"  not 0.053 -- the locked inputs are internally rounded by {100*(s0/s_implied-1):+.2f}%.")
print(f"  Using s = {s_implied:.6f}: Y_cav = {s_implied*rho0*c0**2/3:.6e} Pa  [exact]")
print()
print("  Route B at fixed s gives Y = 0 (u ~ rho, Y = rho du/drho - u). To reach")
print(f"  Y = s rho c0^2/3 via Route B the stretch must obey d(s^2)/d ln rho = 2/(3s) "
      f"= {2.0/(3.0*s0):.4f} at rho_0 -- i.e. the same missing input: the heat-balance")
print("  relation s(rho).  Route A (force per bond) is the one consistent with T3.")
print()
print("  v_cav benchmark (locked law v_cav ~ sqrt(2Y/rho)):")
print(f"    v_cav(rho_0) = sqrt(2 Y_cav/rho0) = {np.sqrt(2*Y_cav/rho0):.6e} m/s "
      f"= {np.sqrt(2*Y_cav/rho0)/c0:.6e} c0")
print("  water benchmark (locked): (-140 MPa)/(2.2 GPa) = 6.36% vs the medium's")
print(f"  Y_cav/(rho0 c0^2/3) = s = {100*s0:.2f}%   [same order, as the framework states]")
print()
print("  T3 VERDICT: CLOSED from the pairing law (eq. 6), up to the locked inputs'")
print("  own 0.7% internal rounding of s.  The yank spring constant k = rho a c0^2")
print("  (locked by T1's product identity) + the 1/3 EoS factor reproduce Y_cav.")

# =====================================================================
print()
print("=" * 78)
print("SECTION 4 -- T2: the cohesion channel of the holding yield at rho_max")
print("=" * 78)
a_max = (mp / rhomax) ** (1.0 / 3.0)
print(f"  pair spacing at rho_max: a_max = (m_p/rho_max)^(1/3) = {a_max:.6e} m")
print(f"  (a0/a_max = {a0/a_max:.6e};  rho_max/rho0 = {rhomax/rho0:.6e})")
print()

print("4a. Route A spring, fixed stretch s = 0.053 (the T3 law extended to rho_max):")
a_coh_spring = c0 ** 2 * s0 / (3.0 * a_max)
print(f"    Y(rho_max)  = s rho_max c0^2/3 = {s0*rhomax*c0**2/3:.6e} Pa")
print(f"    a_coh = Y/(rho a) = c0^2 s/(3 a_max) = {a_coh_spring:.6e} N/kg")
print(f"    target 7.77e10 -> overshoot factor {a_coh_spring/a_coh:.3e}x")
s_req = 3.0 * a_max * a_coh / c0 ** 2
print(f"    hitting 7.77e10 with this law needs s(rho_max) = {s_req:.3e} "
      f"(= {s_req/s0:.3e} x s(rho_0));")
print(f"    as a power law s ~ rho^-p between the two locked ends: p = "
      f"{np.log(s0/s_req)/np.log(rhomax/rho0):.4f}  (not derivable from the locked set).")
print()

print("4b. Holding-threshold reading a^2 = 4 pi G (net push), P_net = P - Y:  ")
print("    a_hold^2 = 4 pi G * rho_max c0^2 is an identity of the locked law,")
print("    so the sealed yield reads a_sealed^2 = 4 pi G (P_locked + Y_coh) with")
Y_req = a_coh ** 2 / (4.0 * np.pi * G)
P_lock = rhomax * c0 ** 2
print(f"    Y_coh(rho_max) = a_coh^2/(4 pi G) = {Y_req:.6e} Pa")
print(f"    Y_coh / P_locked = {Y_req/P_lock:.6f}   (the extra 0.7703 sr = 4 pi x this)")
print(f"    via Y = s rho c0^2/3 this demands s_eff(rho_max) = {3*Y_req/P_lock:.4f}")
print(f"    vs s(rho_0) = {s0} -- the stretch would have to GROW 3.47x under compression.")
print()

print("4c. van der Waals route, P_net = kinetic push - a_van rho^2 (locked analogy):")
a_van_T3 = Y_cav_T / rho0 ** 2
a_van_T2 = Y_req / rhomax ** 2
print(f"    a_van from T3 (Y_cav/rho0^2)  = {a_van_T3:.6e} m^5 kg^-1 s^-2")
print(f"    a_van from T2 (Y_req/rhomax^2)= {a_van_T2:.6e} m^5 kg^-1 s^-2")
print(f"    ratio {a_van_T3/a_van_T2:.3e}x  -> ONE rho^2 law cannot carry the yank from")
print(f"    rho_0 to rho_max.  With a_van(T3): Y(rho_max) = {a_van_T3*rhomax**2:.3e} Pa,")
a_coh_vdw = np.sqrt(4.0 * np.pi * G * a_van_T3 * rhomax ** 2)
print(f"    a_coh = sqrt(4 pi G Y) = {a_coh_vdw:.3e} N/kg vs target 7.77e10 "
      f"({a_coh_vdw/a_coh:.3e}x off).")
print(f"    Required exponent between the two locked ends: Y ~ rho^n with")
print(f"    n = ln(Y_req/Y_cav_T)/ln(rho_max/rho0) = "
      f"{np.log(Y_req/Y_cav_T)/np.log(rhomax/rho0):.4f}  (~rho^1, not rho^2).")
print()

print("4d. Near-miss algebra (candidates for Y/P at rho_max; required 0.06134):")
req = Y_req / P_lock
cands = {
    "s (1 + 1/(2 pi))": s0 * (1.0 + 1.0 / (2.0 * np.pi)),
    "s (1 + 3 s)": s0 * (1.0 + 3.0 * s0),
    "2 s / sqrt(3)": 2.0 * s0 / np.sqrt(3.0),
    "7 pi s^2": 7.0 * np.pi * s0 ** 2,
    "s (1 + 2 s)": s0 * (1.0 + 2.0 * s0),
}
for lab, v in cands.items():
    print(f"    {lab:<16s} = {v:.6f}   residual {100*(v/req-1):+.2f}%")
ah_s  = a_hold * np.sqrt(s0)
ah_3p = a_hold * s0 * 3.0 * np.pi / 2.0
ah_Rp = np.pi * a_hold * Rp / a_max
print(f"    a_hold sqrt(s) = {ah_s:.4e} ({100*(ah_s/a_coh-1):+.2f}%);  "
      f"a_hold s 3pi/2 = {ah_3p:.4e} ({100*(ah_3p/a_coh-1):+.2f}%);  "
      f"pi a_hold Rp/a_max = {ah_Rp:.4e} ({100*(ah_Rp/a_coh-1):+.2f}%)")
print("     none lands exactly and none has a locked provenance -> numerology, rejected.)")
print()

print("4e. What IS derivable for T2 from the yank:")
print(f"    - the cohesion enters through the SAME spring k = rho a c0^2 that T3 locks;")
print(f"    - at fixed s its contribution to the sealed yield is Y/P = s/3 = {s0/3:.4f},")
print(f"      i.e. a_coh = a_hold sqrt(s/3) = {a_hold*np.sqrt(s0/3):.3e} N/kg "
      f"({a_hold*np.sqrt(s0/3)/a_coh:.2f}x short);")
print(f"    - the locked 7.77e10 needs Y/P = {req:.6f}, i.e. an effective stretch of")
print(f"      3 Y/P = {3*req:.4f} at rho_max (3.47x the rest value) -- a law for s(rho)")
print("      that the locked inputs do not contain.")
print()
print("  T2 VERDICT: FAILS from the locked set -- DOCUMENTED.")
print("    Missing input #2: the yank force law F(a) away from equilibrium --")
print("    equivalently the residual-stretch function s(rho) (the heat balance of the")
print("    compressed state), equivalently the pair's charge separation d.  The locked")
print("    spring constant k = rho a c0^2 fixes the equilibrium stiffness only; the")
print("    locked set does not fix how the 5.3% stretch drains as rho -> rho_max, and")
print("    every natural extension misses the target by 3.5x to 2e20x (4a-4c).")

# =====================================================================
print()
print("=" * 78)
print("SUMMARY OF PASS / FAIL")
print("=" * 78)
print(f" [PASS-EXACT] T1 product: 1/sqrt(mu0 eps0) = c0 = {c0:.9e} m/s (lattice identity)")
print(f" [FAIL-PROVEN] T1 individual eps0 = {eps0_SI:.5e}, mu0 = {mu0_SI:.5e}:")
print(f"       unformable from {{rho0, rhomax, c0, G, mp, Rp, hbar}} (no charge dimension).")
print(f"       Missing input: pair charge scale {{e, alpha}} / pair charge separation d.")
print(f"       Mechanical split deficit chi = mu0_SI/rho0 = {chi:.6e}.")
print(f" [PASS] T3: Y_cav = s rho0 c0^2/3 = {Y_cav:.6e} Pa vs locked {Y_cav_T:.6e} "
      f"({100*(Y_cav/Y_cav_T-1):+.2f}%; s rounding {100*(s0/s_implied-1):+.2f}%).")
print(f" [FAIL-DOCUMENTED] T2: a_coh(rho_max) = {a_coh:.6e} N/kg not derivable from the")
print(f"       locked yank (fixed-s spring: {a_coh_spring:.2e}; vdW(T3): {a_coh_vdw:.2e}).")
print(f"       Missing input: F_yank(a) / s(rho) heat balance (needs Y/P = {req:.6f}, "
      f"s_eff = {3*req:.4f} at rho_max).")
