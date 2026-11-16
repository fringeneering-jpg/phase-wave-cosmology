# -*- coding: utf-8 -*-
"""
PWC yield anchor — cohesion channel re-derived WITH HEAT as the driver.
Corrected caloric law (parent correction, framework-owner endorsed):
  gas branch : H(rho) = H0 - (c0^2/3) ln(rho/rho0),  rho0 <= rho <= rho_fold = rho_max/2
               drop = (c0^2/3) ln(rho_max / (2 rho0)) = 31.371 c0^2 per kg
  plateau    : P = P* = rho_max c0^2 pinned, dv = 1/rho_max,
               phase-change heat P* dv = c0^2 exactly (the latent L)
  TOTAL      : Q_tot = 32.371 c0^2 = 2.910e18 J/kg ;  H0 >= Q_tot
Zero fitted parameters. No GR. All numbers from locked inputs (repo-quoted).
"""
import numpy as np

# ---------------- locked constants (repo) ----------------
c0    = 299792458.0          # c0 = 1/sqrt(mu0 eps0)
c0sq  = c0**2
G     = 6.67430e-11
s     = 0.052632             # 5.3% remaining stretch (1/0.95 = 1.053, OPEN_WORK L125)
rho0  = 8.74e-27             # resting medium density (CLOSURE_SHEET L26)
rho_max = 1.304e15           # locked ceiling (DERIVATION_BRIEF L35)
a_yield = 3.23e11            # holding yield at rho_max (DERIVATION_BRIEF L36)
gamma   = 3.36e31            # P*R/2, sonic-point pressure scale (CLOSURE_SHEET L44)
m_n   = 1.67492749804e-27    # neutron mass, CODATA
eV    = 1.602176634e-19
E_line= 43.2e9 * eV          # Fan et al. arXiv:2407.11737 line (OPEN_WORK L89)
Y_bow = 5.93e26              # RBH-1 bow-wave anchor (DERIVATIONS.md row 15)
v_bow = 9.54e5               # 954 km/s at rho_max

# locked TARGETS (parent's T1/T2)
Y_cav_t  = 1.3781e-11
a_geo_t  = 3.1352e11
a_coh_t  = 7.7674e10
Y_coh_t  = 7.1935e30
P_locked_t = 1.1720e32
kappa_t  = 0.061379

print("="*92)
print("0) LOCKED-INPUT REPRODUCTION (residual vs target)")
print("="*92)

Y_cav   = s*rho0*c0sq/3.0
P_locked= rho_max*c0sq
a_geo   = c0*np.sqrt(4*np.pi*G*rho_max)
a_coh   = np.sqrt(a_yield**2 - a_geo**2)
Y_coh   = a_coh**2/(4*np.pi*G)
kappa   = Y_coh/P_locked

rows = [
 ("Y_cav = s rho0 c0^2/3",  Y_cav,  Y_cav_t),
 ("P_locked = rho_max c0^2",P_locked,P_locked_t),
 ("a_geo = c0 sqrt(4pi G rho_max)",a_geo,a_geo_t),
 ("a_coh = sqrt(a_yield^2 - a_geo^2)",a_coh,a_coh_t),
 ("Y_coh = a_coh^2/(4pi G)",Y_coh,Y_coh_t),
 ("kappa = Y_coh/P_locked", kappa, kappa_t),
]
for name,val,tgt in rows:
    print(f"  {name:38s} {val: .6e}   target {tgt: .6e}   rel.res {(val/tgt-1):+.3e}")

print(f"  channel closure a_geo^2 + a_coh^2 - a_yield^2 = {a_geo**2+a_coh**2-a_yield**2: .3e}")

print()
print("="*92)
print("1) H(rho) — THE CORRECTED CALORIC LAW")
print("="*92)
rho_fold = rho_max/2.0
ln_fold  = np.log(rho_max/(2*rho0))
Q_gas    = ln_fold/3.0          # units of c0^2
Q_plat   = 1.0
Q_tot    = Q_gas + Q_plat
Q_tot_J  = Q_tot*c0sq

print(f"  rho_fold = rho_max/2                 = {rho_fold:.6e} kg/m^3")
print(f"  ln(rho_max/(2 rho0))                = {ln_fold:.6f}   (e-folds of gas branch)")
print(f"  gas-branch drop (c0^2/3)*ln(fold/rho0) = {Q_gas:.6f} c0^2  per kg")
print(f"  plateau phase-change heat P* dv       = {Q_plat:.6f} c0^2  per kg  (P*=rho_max c0^2, dv=1/rho_max)")
print(f"  TOTAL caloric inventory Q_tot         = {Q_tot:.6f} c0^2 = {Q_tot_J:.6e} J/kg")
print(f"  constraint on rest heat:  H0 >= {Q_tot:.6f} c0^2 = {Q_tot_J:.6e} J/kg")
print(f"  H(pho): gas H=H0-(c0^2/3)ln(rho/rho0); plateau H=H0-{Q_gas:.4f} c0^2 - c0^2(2 - rho_max/rho)")
print(f"  H(rho_fold) = H0 - {Q_gas:.6f} c0^2 ;  H(rho_max) = H0 - {Q_tot:.6f} c0^2")
print(f"  (H0 symbolic; H0=Q_tot  =>  neutron rung 'no heat' exactly at the locked end)")

print()
print("="*92)
print("2) Y(H) = Y0 * f(H/H0)  —  anchors and the forced family")
print("="*92)
Y0   = Y_cav
RY   = Y_coh/Y_cav                # endpoint ratio forced by T2
A_tot= np.log(RY)
a    = A_tot/Q_tot                # exponent per unit c0^2 of expelled heat
lam  = c0sq/a                     # heat scale: tension e-folds per lam J/kg

print(f"  Y0 = s rho0 c0^2/3                    = {Y0:.6e} Pa  (T1 anchor preserved: f(1)=1)")
print(f"  R_Y = Y_coh/Y_cav                     = {RY:.6e}")
print(f"  A_tot = ln R_Y                        = {A_tot:.6f}")
print(f"  Delta = (H0-H)/c0^2  in [0, {Q_tot:.4f}] ;  f(0)=1 , f(Delta_end)=R_Y")
print(f"  x_end = H(rho_max)/H0 = 1 - {Q_tot:.4f} c0^2/H0  (H0-dependent, >=0)")
print(f"  exponential closure f(Delta)=exp(a Delta):  a = ln R_Y / Delta_end = {a:.6f}")
print(f"  heat scale lambda = c0^2/a             = {lam:.6e} J/kg = {lam/c0sq:.6f} c0^2")
print(f"  yank law:  dY/dH = -Y/lambda  (yank proportional to tension, stiffens as pairs close)")
print()
print(f"  Y(H) = Y0 exp[ ln R_Y * (H0 - H)/Q_tot ]   (H0 symbolic)")
print(f"  gas-branch tension:  Y(rho) = Y0 (rho/rho0)^(a/3),   a/3 = {a/3.0:.6f}  (~ linear in rho)")
Y_fold  = Y0*np.exp(a*Q_gas)
Y_end   = Y0*np.exp(a*Q_tot)
print(f"  Y(rho_fold) = {Y_fold:.6e} Pa   (={kappa*np.exp(-a):.6f} * P_locked)")
print(f"  plateau multiplier e^a = {np.exp(a):.6f}")
print(f"  Y(H(rho_max)) = Y0 e^(a Delta_end) = {Y_end:.6e} Pa   target {Y_coh_t:.6e}   rel.res {(Y_end/Y_coh_t-1):+.3e}")
print(f"  T2 cohesion channel CLOSED: Y_coh = kappa * P_locked, kappa = {kappa:.6f} (target {kappa_t})")
yank_end = a*Y_coh/c0sq
print(f"  yank -dY/dH at locked end = a Y_coh/c0^2 = {yank_end:.6e} kg/m^3 = {yank_end/rho_max:.6f} rho_max")
print(f"  max tension-per-unit-heat (stress form) a Y_coh = {a*Y_coh:.6e} Pa = {a*kappa:.6f} P_locked")

print()
print("="*92)
print("3) T3 — the gamma anchor P*R/2 = 3.36e31 Pa on the heat ladder")
print("="*92)
g_over_P = gamma/P_locked
g_over_Y = gamma/Y_coh
Delta_sonic = np.log(gamma/Y0)/a
print(f"  gamma/P_locked = {g_over_P:.6f}   (repo: ~0.29, CLOSURE_SHEET L44)")
print(f"  gamma/Y_coh    = {g_over_Y:.6f}   (cohesion supplies {1/g_over_Y*100:.2f}% of the sonic-point stress)")
print(f"  Delta_sonic = ln(gamma/Y0)/a = {Delta_sonic:.6f}   vs Delta_end = {Q_tot:.6f}")
print(f"  Delta_sonic/Delta_end = {Delta_sonic/Q_tot:.6f}   (sonic point sits {100*(Delta_sonic/Q_tot-1):.2f}% past the locked end)")
print(f"  place for 0.287: f(Delta_sonic) = gamma/Y0 = {gamma/Y0:.6e}, reached just beyond the channel's max")

print()
print("="*92)
print("4) CAVITATION THRESHOLD from dH/dt = P dv/dt  (Max-P + a touch of speed)")
print("="*92)
v_cav0 = np.sqrt(2*Y_cav/rho0)
v_cavm = np.sqrt(2*Y_coh/rho_max)
v_ambm = c0*np.sqrt(2*(1+kappa))
print(f"  general threshold: (1/2) rho v^2 = P_amb + Y ;  locked form (P_amb=0): (1/2) rho v^2 = Y")
print(f"  v_cav(rho0)   = sqrt(2 Y_cav/rho0) = {v_cav0:.6e} m/s = {v_cav0/c0:.6f} c0  [= sqrt(2s/3) c0 = {np.sqrt(2*s/3):.6f}]")
print(f"  v_cav(rho_max)= sqrt(2 Y_coh/rho_max) = {v_cavm:.6e} m/s = {v_cavm/c0:.6f} c0  [= sqrt(2 kappa) c0 = {np.sqrt(2*kappa):.6f}]")
print(f"  with ambient P_locked: v = sqrt(2(1+kappa)) c0 = {v_ambm/c0:.6f} c0  -> locked phase cannot cavitate")
print(f"  heat paid along the leg: H_inf - H(P) = P^2/(2 rho) ; at Max-P: Y^2/(2 rho)")
print()
v_bow_chk = np.sqrt(2*Y_bow/rho_max)
Delta_bow = np.log(Y_bow/Y0)/a
print(f"  BOW-WAVE CROSS-CHECK (repo row 15): Y=5.93e26 Pa -> v = {v_bow_chk:.6e} m/s = {v_bow_chk/1e3:.1f} km/s (locked 954 km/s)")
print(f"  Delta_bow = ln(Y_bow/Y0)/a = {Delta_bow:.6f}  = {Delta_bow/Q_tot:.6f} of the ladder  (vs 1.000 for Y_coh)")
print(f"  Y_coh/Y_bow = {Y_coh/Y_bow:.6e}   <-- UNRESOLVED: cohesion channel is 1.21e4 x the bow-wave tension at rho_max")

print()
print("="*92)
print("5) T4 — the 43.2 GeV line (arXiv:2407.11737) as the plateau quantum per pair")
print("="*92)
m_line = E_line/c0sq
N_nucl = m_line/m_n
m_pair = m_line
n_pair = rho0/m_pair
d_pair = n_pair**(-1/3)
print(f"  43.2 GeV / c0^2 = {m_line:.6e} kg = {N_nucl:.3f} neutron masses  (locked: 46)")
print(f"  plateau latent per kg = c0^2  =>  per pair: m_pair c0^2 = 43.2 GeV  ->  m_pair = {m_pair:.6e} kg = {m_pair/m_n:.2f} m_n")
print(f"  HEAT-LAW READING: the line is the fold/plateau phase-change quantum of ONE 46-nucleon pair")
print(f"  single energy because every pair has the same mass and the phase-change heat is fixed at c0^2 per kg")
print(f"  full ladder per pair = {Q_tot:.3f} x 43.2 GeV = {Q_tot*E_line/eV/1e12:.4f} TeV (gas branch = spectrum, plateau = line)")
print(f"  pair number density at rest = {n_pair:.6e} m^-3 ;  resting pair spacing = {d_pair:.3f} m")

print()
print("="*92)
print("6) HONEST LEDGER — near-identities (NOT exact) and residual freedom")
print("="*92)
print(f"  kappa vs 7s/6            : kappa/(7s/6) = {kappa/(7*s/6):.6f}  (residual {kappa/(7*s/6)-1:+.2e})")
print(f"  a vs 3                   : a/3 = {a/3:.6f}  (residual {a/3-1:+.2e})")
print(f"  kappa*a + 2s vs gamma/P_locked : {kappa*a+2*s:.6f} vs {g_over_P:.6f}  (residual {kappa*a+2*s-g_over_P:+.2e})")
print(f"  a Y_coh / gamma          : {a*Y_coh/gamma:.6f}   (2/pi = 0.636620)")
print()
print("  FREE DATA REMAINING:")
print("   (a) H0 : unknown, bounded below by Q_tot = 32.371 c0^2 (equations symbolic in H0);")
print("       pinned exactly (no datum left) only if the ladder's neutron rung 'no heat, locked'")
print("       is identified with the locked end -> H0 = Q_tot.")
print("   (b) f's interior shape: the anchors force only f(0)=1 and f(Delta_end)=R_Y; the exponential")
print("       f=exp(a Delta) is the unique ZERO-PARAMETER family under the yank law dY/dH=-Y/lambda.")
print("       Any other monotone family through the two points costs one extra shape datum.")
print("   (c) The bow-wave anchor Y=5.93e26 Pa at rho_max sits at Delta = 0.9022 of the ladder;")
print("       the cohesion channel needs Delta = 1.000. Missing datum to reconcile: the heat state")
print("       at the bow-wave / rho_max boundary.")
