#!/usr/bin/env python3
"""
PWC GW150914 settling time: tau = 4.68 ms from released-medium geometry.
Scratch analysis (not part of the PWC clone). All inputs locked by the task/parent.
Routes: 1 decompression front, 2 inventory dilution, 3 k-rule surface relaxation,
4 two-choke crossing, 5 fight drag (parent msg 1), 6 figure-8 vent (parent msg 2).
Plus: withdrawn 232/272 Hz check and an expression sweep for c0*tau = 1403 km.
"""
import math, itertools
import numpy as np

G    = 6.674e-11
C0   = 2.99792458e8
MSUN = 1.98892e30
RHO_MAX  = 1.304e15
RHO_CORE = 2.3e17
RHO_0    = 8.74e-27          # CLAUDE.md section 4 (locked): resting medium density
A_MAX    = 3.23e11           # yield N/kg
K        = 0.8525            # task-locked k
M1, M2   = 28.118, 22.255    # Msun cores
MCORE    = M1 + M2           # 50.373
HELD_B, HELD_A = 14.627, 11.627
MREL     = 3.0               # Msun released
M_TOT    = 62.0
T1, T2   = 82.9, 73.4        # km layer thicknesses
T_MERGED = 112.6             # km
EDGE     = 159.6             # km
TAU_MEAS = 4.68e-3           # s (H1/L1 within 2%)

def msun(m): return m*MSUN

R_c1 = (3*msun(M1)/(4*math.pi*RHO_CORE))**(1/3)
R_c2 = (3*msun(M2)/(4*math.pi*RHO_CORE))**(1/3)
R_cf = (3*msun(MCORE)/(4*math.pi*RHO_CORE))**(1/3)

print("="*100)
print("LOCKED GEOMETRY REPRODUCTION / CONSISTENCY")
print("="*100)
print(f"core radii: R1={R_c1/1e3:.2f} km  R2={R_c2/1e3:.2f} km  fused={R_cf/1e3:.2f} km  (locked 47.3)")
R1s, R2s = R_c1/1e3 + T1, R_c2/1e3 + T2
print(f"shell outer radii: R1s={R1s:.2f} km  R2s={R2s:.2f} km  (core + layer)")
print(f"layers touch at separation {R1s+R2s:.1f} km; cores touch at {R_c1/1e3+R_c2/1e3:.1f} km")
print(f"fight length = {R1s+R2s-(R_c1/1e3+R_c2/1e3):.1f} km (locked t1+t2 = {T1+T2})")

# k-rule check with k=0.8525
A1, A2, Af = M1**(2/3), M2**(2/3), MCORE**(2/3)
hb, ha = K*(A1+A2), K*Af
print(f"\nk-rule held: before {hb:.3f} Msun (locked 14.627), after {ha:.3f} (locked 11.627), "
      f"released {hb-ha:.3f} (locked 3)")
f = 1 - Af/(A1+A2)
print(f"released fraction f = 1 - Cf^(2/3)/(C1^(2/3)+C2^(2/3)) = {f:.4f}  (k cancels)")
A_sep_km2 = 4*math.pi*(R_c1**2 + R_c2**2)/1e6
A_f_km2   = 4*math.pi*R_cf**2/1e6
print(f"core surface areas: separate {A_sep_km2:.0f} km2, fused {A_f_km2:.0f} km2, "
      f"ratio {A_f_km2/A_sep_km2:.4f} (parent: 27759/34923 = {27759/34923:.4f})")
print(f"held-after/held-before = {HELD_A/HELD_B:.4f}  -> identity {abs(HELD_A/HELD_B - A_f_km2/A_sep_km2)<1e-3}")

# shell mass consistency (locked 11.627 Msun between 47.3 and 159.6 km at rho_max)
Vsh = (4/3)*math.pi*(EDGE*1e3)**3 - (4/3)*math.pi*(R_cf)**3
print(f"\nshell 47.3->159.6 km at rho_max holds {Vsh*RHO_MAX/MSUN:.3f} Msun  "
      f"(locked 11.627 -> INCONSISTENT, factor {11.627/(Vsh*RHO_MAX/MSUN):.1f}); "
      f"edge for 11.627 Msun at rho_max = {((R_cf)**3 + 3*msun(HELD_A)/(4*math.pi*RHO_MAX))**(1/3)/1e3:.1f} km")

# released medium at rho_max as a sphere / skin
Vrel = msun(MREL)/RHO_MAX
Rrel = (3*Vrel/(4*math.pi))**(1/3)
print(f"released 3 Msun at rho_max: volume {Vrel:.3e} m3, sphere radius {Rrel/1e3:.1f} km; "
      f"skin on fused core = {Vrel/(4*math.pi*R_cf**2)/1e3:.1f} km thick")

# chokes
r_tc = 2*G*msun(M_TOT)/C0**2
r_cc = 6*G*msun(M_TOT)/C0**2
r_y  = math.sqrt(G*msun(M_TOT)/A_MAX)
print(f"\nchokes: transverse 2GM/c0^2 = {r_tc/1e3:.1f} km, compression 6GM/c0^2 = {r_cc/1e3:.1f} km, "
      f"yield reach sqrt(GM/a_max) = {r_y/1e3:.1f} km")
print(f"c0*tau = {C0*TAU_MEAS/1e3:.1f} km   (naive 43.7 km/c0 = {43.7e3/C0*1e3:.3f} ms -> factor "
      f"{C0*TAU_MEAS/(43.7e3):.1f})")

print("\n" + "="*100)
print("ROUTE 1 -- DECOMPRESSION FRONT ACROSS THE FULL HELD SHELL (156.3 km region)")
print("="*100)
for cs_name, cs in [("c0 (locked)", C0), ("c0/sqrt3 (loose)", C0/math.sqrt(3)),
                    ("ramp c0->c0/sqrt3 (harmonic mean)", 2/(1/C0+1/(C0/math.sqrt(3))))]:
    t = (T1+T2)*1e3/cs
    print(f"  {cs_name:38s} crossing {T1+T2} km: {t*1e3:.3f} ms   (factor off 4.68: {4.68/t:.1f}x)")
print(f"  also: released-sphere diameter 2*{Rrel/1e3:.0f} km at c0: {2*Rrel/C0*1e3:.3f} ms")
print("  VERDICT: FAILS by 5-9x. No single light-crossing of the locked shell lands 4.68 ms.")

print("\n" + "="*100)
print("ROUTE 2 -- INVENTORY DILUTION: radius where 3 Msun at rho_0 fills a sphere/annulus")
print("="*100)
R_dil = (3*msun(MREL)/(4*math.pi*RHO_0))**(1/3)
print(f"  rho_0 = {RHO_0:.2e} kg/m3 (locked, CLAUDE.md sec 4)")
print(f"  sphere radius = {R_dil:.3e} m = {R_dil/9.4607e15:.0f} light-years   (vs 1403 km)")
ann_km = msun(MREL)/(RHO_0*4*math.pi*43.7e3)
print(f"  annulus of 43.7 km thickness reaches rho_0 at radius {math.sqrt(ann_km):.3e} m")
rho_at_1403 = msun(MREL)/((4/3)*math.pi*(1403e3)**3)
print(f"  density of 3 Msun spread over 1403 km sphere = {rho_at_1403:.3e} kg/m3 "
      f"= rho_max/{RHO_MAX/rho_at_1403:.0f}; not a locked density")
print("  VERDICT: FAILS. Settling time is NOT a dilution-to-ambient time (off by ~15 orders).")

print("\n" + "="*100)
print("ROUTE 3 -- K-RULE SURFACE-AREA RELAXATION: R_eff from the four radii")
print("="*100)
R4 = {"core": R_cf/1e3, "t1": T1, "t2": T2, "edge": EDGE}
print("  naive surface-area timescales:")
for n, v in R4.items():
    print(f"    {n:5s} {v:6.1f} km : {v*1e3/C0*1e3:.3f} ms   circumference 2pi*R: {2*math.pi*v*1e3/C0*1e3:.3f} ms")
print(f"  released mass / (k-rule deficit) consistency: released = k*[C1^(2/3)+C2^(2/3)-Cf^(2/3)] "
      f"= {K*(A1+A2-Af):.3f} Msun")
print("  sweep of clean combinations of the four radii vs 1403.03 km (see sweep section below).")
print("  VERDICT: no surface-area relaxation R_eff/c0 with a locked coefficient lands 1403 km "
      "(closest: 9*(t1+t2) = 1406.7, 4*pi*t_merged = 1414.9, 32*43.7 = 1398.4 - all unmechanised).")

print("\n" + "="*100)
print("ROUTE 4 -- TWO-CHOKE CROSSING (transverse 2GM/c0^2 .. compression 6GM/c0^2)")
print("="*100)
for cs_name, cs in [("c0", C0), ("c0/sqrt3", C0/math.sqrt(3))]:
    print(f"  {r_tc/1e3:.1f}->{r_cc/1e3:.1f} km at {cs_name:8s}: {(r_cc-r_tc)/cs*1e3:.3f} ms")
    print(f"  core->{r_cc/1e3:.1f} km at {cs_name:8s}: {(r_cc-R_cf)/cs*1e3:.3f} ms")
print(f"  6GM/c0^2 / (c0/sqrt3) = {(r_cc/(C0/math.sqrt(3)))*1e3:.3f} ms  (closest, still {4.68/(r_cc/(C0/math.sqrt(3))*1e3):.2f}x short)")
print("  VERDICT: FAILS by 1.5-3.8x. The choke region is too small to clock 4.68 ms.")

print("\n" + "="*100)
print("ROUTE 5 -- FIGHT DRAG (parent msg 1): cores plowing through each other's rho_max shells")
print("="*100)
A_l1, A_l2 = math.pi*(T1*1e3)**2, math.pi*(T2*1e3)**2
taud1 = msun(M1)/(RHO_MAX*A_l1*C0)
taud2 = msun(M2)/(RHO_MAX*A_l2*C0)
taudc = msun(MCORE)/(RHO_MAX*(A_l1+A_l2)*C0)
print(f"  tau_d1 = M1/(rho_max pi t1^2 c0) = {taud1*1e3:.3f} ms")
print(f"  tau_d2 = M2/(rho_max pi t2^2 c0) = {taud2*1e3:.3f} ms")
print(f"  combined = {taudc*1e3:.3f} ms")
print(f"  note: M1/t1^2 = {msun(M1)/(T1*1e3)**2:.3e}, M2/t2^2 = {msun(M2)/(T2*1e3)**2:.3e} kg/m2 -> "
      f"ratio {msun(M1)/(T1*1e3)**2/(msun(M2)/(T2*1e3)**2):.4f} (layer faces scale with core mass)")
v0a = math.sqrt(G*msun(M_TOT)/((T1+T2)*1e3))     # v^2 = GM/r, r = 156.3 km
E1r = math.sqrt(G*msun(M1)/A_MAX); E2r = math.sqrt(G*msun(M2)/A_MAX)
v0b = math.sqrt(G*msun(M_TOT)/(E1r+E2r))
print(f"\n  closing speeds: v0(156.3 km) = {v0a/C0:.3f} c0   v0(E1+E2 = {((E1r+E2r)/1e3):.1f} km) = {v0b/C0:.3f} c0")
print(f"  stopping distances: v0*tau_d1: {v0a*taud1/1e3:.0f} km (v0a), {v0b*taud1/1e3:.0f} km (v0b)  vs c0*tau = {C0*TAU_MEAS/1e3:.0f} km")
print(f"  v that makes stopping distance = 1403 km exactly: {C0*TAU_MEAS/taud1/C0:.4f} c0 = c0/sqrt2 x {C0*TAU_MEAS/taud1/C0*math.sqrt(2):.4f}")
print(f"\n  sqrt2 test:")
print(f"    tau_d1/sqrt2 = {taud1/math.sqrt(2)*1e3:.4f} ms   (measured 4.68 -> {100*(taud1/math.sqrt(2)/TAU_MEAS-1):+.2f}%)")
print(f"    tau_d2/sqrt2 = {taud2/math.sqrt(2)*1e3:.4f} ms   ({100*(taud2/math.sqrt(2)/TAU_MEAS-1):+.2f}%)")
print(f"    combined/sqrt2 = {taudc/math.sqrt(2)*1e3:.4f} ms   ({100*(taudc/math.sqrt(2)/TAU_MEAS-1):+.2f}%)")
print(f"  sqrt2 = two cores sharing? each core decays at 1/tau_d, so u = v1+v2 also decays at "
      f"~1/tau_d (rates 1/taud1,1/taud2): shared drag gives tau_d, NOT tau_d/sqrt2.  FAILS as sqrt2 origin.")
print(f"  sqrt2 = 203 vs 156 km approach? v0 ratio = {v0b/v0a:.3f} = sqrt(156.3/203.1) = {math.sqrt((T1+T2)*1e3/(E1r+E2r)):.3f}; "
      f"not sqrt2.  FAILS as sqrt2 origin.")
# energy closure
E_156 = G*msun(M1)*msun(M2)/(2*C0**2*(T1+T2)*1e3*MSUN)
E_203 = G*msun(M1)*msun(M2)/(2*C0**2*(E1r+E2r)*MSUN)
r_exact = G*msun(M1)*msun(M2)/(2*C0**2*msun(MREL))
print(f"\n  ENERGY CLOSURE: G M1 M2/(2 c0^2 r) = 3 Msun at r = {r_exact/1e3:.1f} km (locked fight length = {T1+T2})")
print(f"    at r = t1+t2 = 156.3 km: {E_156:.3f} Msun  ({100*(E_156/MREL-1):+.1f}% of the 3-Msun dump)")
print(f"    at r = E1+E2 = 203.1 km: {E_203:.3f} Msun  ({100*(E_203/MREL-1):+.1f}% of the dump)")

print("\n" + "="*100)
print("ROUTE 6 -- FIGURE-8 VENT (parent msg 2): overlap squeezed laterally through the pinch ring")
print("="*100)
A_ring_req = msun(MREL)/(RHO_MAX*C0*TAU_MEAS)
print(f"  ring that drains 3 Msun in tau=4.68 ms: A_ring = M_rel/(rho_max c0 tau) = {A_ring_req:.3e} m2")
for rr in (50.0, 60.0, 70.0):
    print(f"    at ring radius {rr:.0f} km: width w = {A_ring_req/(2*math.pi*rr*1e3)/1e3:.2f} km")
print(f"    (parent: 7-10 km at 50-70 km radius)")

def lens(x, R1, R2):
    """two-sphere intersection geometry at separation x (R1>=R2)."""
    if x >= R1 + R2: return 0.0, 0.0, 0.0, 0.0
    a  = (x*x + R1*R1 - R2*R2)/(2*x)
    rr = math.sqrt(max(R1*R1 - a*a, 0.0))
    h1 = R1 - a; h2 = R2 - (x - a)
    V  = math.pi*h1*h1*(3*R1-h1)/3 + math.pi*h2*h2*(3*R2-h2)/3
    S  = 2*math.pi*(R1*h1 + R2*h2)
    return rr, V, S, (h1, h2)

x_touch = R1s*1e3 + R2s*1e3
x_cont  = (R_c1 + R_c2)
print(f"\n  fight: x from {x_touch/1e3:.1f} km (layer touch) to {x_cont/1e3:.1f} km (core touch); "
      f"rim radius and lens:")
for x_km in (230.8, 217.4, 203.1, 190.0, 156.3, 112.6, 74.5):
    rr, V, S, (h1, h2) = lens(x_km*1e3, R1s*1e3, R2s*1e3)
    print(f"    x={x_km:6.1f} km: r_rim={rr/1e3:6.1f} km  V_lens={V*RHO_MAX/MSUN:5.3f} Msun  "
          f"caps=({h1/1e3:.1f},{h2/1e3:.1f}) km  lens surface={S/1e6:.0f} km2  "
          f"w for tau={A_ring_req/(2*math.pi*rr)/1e3:5.2f} km" if rr > 0 else
          f"    x={x_km:6.1f} km: just touching (r_rim=0)")
rr_c, V_c, S_c, _ = lens(x_cont, R1s*1e3, R2s*1e3)
print(f"\n  lens at CORE CONTACT holds {V_c*RHO_MAX/MSUN:.2f} Msun at rho_max (locked release 3 Msun; "
      f"k-rule area bookkeeping vs literal lens volume)")
print(f"  lens surface at contact {S_c/1e6:.0f} km2 -> full-surface drain at c0 = {msun(MREL)/(RHO_MAX*C0*S_c)*1e3:.3f} ms (too fast)")

# ring area profile across the fight for candidate widths
print("\n  ring area profile A_ring(x) = 2pi r_rim(x) * w :")
xs = np.linspace(x_cont, x_touch, 200)
rrs = np.array([lens(x, R1s*1e3, R2s*1e3)[0] for x in xs])
mean_rr = np.trapezoid(rrs, xs)/(x_touch - x_cont)
print(f"    mean rim radius over the fight = {mean_rr/1e3:.1f} km")
for wname, w in [("w = f*R_cf = 9.71 km", 0.2051*R_cf/1e3*1e3), ("w = R_f/5 = 9.46 km", R_cf/1e3/5*1e3),
                 ("w = f*R_c1 = 7.94 km", 0.2051*R_c1/1e3*1e3), ("w = 8.0 km", 8.0e3)]:
    w_req = msun(MREL)/(RHO_MAX*C0*TAU_MEAS*2*math.pi*mean_rr)
    A_mean = 2*math.pi*mean_rr*w
    print(f"    {wname:22s}: mean A_ring = {A_mean/1e6:.0f} km2 -> tau = M/(rho c0 A) = "
          f"{msun(MREL)/(RHO_MAX*C0*A_mean)*1e3:.3f} ms")
print(f"    w that lands 4.68 ms with the mean rim radius: {msun(MREL)/(RHO_MAX*C0*TAU_MEAS*2*math.pi*mean_rr)/1e3:.2f} km")
# rim radius at reach-contact
rr_203 = lens((E1r+E2r), R1s*1e3, R2s*1e3)[0]
print(f"\n    at the reach-contact x=E1+E2={((E1r+E2r)/1e3):.1f} km: r_rim = {rr_203/1e3:.2f} km; "
      f"width needed = {A_ring_req/(2*math.pi*rr_203)/1e3:.2f} km  (R_f/5 = {R_cf/1e3/5:.2f}, f*R_f = {0.2051*R_cf/1e3:.2f})")
rr_fus = rr_c
print(f"    at the fused state (core contact): r_rim = {rr_fus/1e3:.2f} km; "
      f"width needed = {A_ring_req/(2*math.pi*rr_fus)/1e3:.2f} km")

# vent-limited closing simulation
print("\n  vent-limited closing simulation (gravity + face drag, throttle u <= c0*A_ring/(pi r_rim^2)):")
def simulate(w, x0, u0, label, cap="ring"):
    x = x0; u = u0; t = 0.0; dt0 = 1e-6
    ts, xs_, us, fl = [], [], [], []
    tau_eff = msun(MCORE)/(RHO_MAX*(A_l1+A_l2)*C0)   # relative drag rate ~1/tau_d
    while x > x_cont and t < 0.02:
        rr, V, S, _ = lens(x, R1s*1e3, R2s*1e3)
        Aring = 2*math.pi*rr*w if cap == "ring" else A_ring_req
        u_free = u + dt0*(G*msun(M_TOT)/x**2 - u/tau_eff)
        u_thr  = C0*Aring/(math.pi*rr**2) if rr > 0 else 1e9
        u = min(u_free, u_thr)
        flux = min(RHO_MAX*math.pi*rr**2*u, RHO_MAX*C0*Aring) if rr > 0 else 0.0
        ts.append(t); xs_.append(x); us.append(u); fl.append(flux)
        x -= u*dt0; t += dt0
    ts = np.array(ts); fl = np.array(fl); us = np.array(us)
    pk = np.argmax(fl)
    # e-fold of the tail
    tail = fl[pk:]
    t_tail = ts[pk:] - ts[pk]
    if len(tail) > 5 and tail[0] > 0:
        m = np.where(tail <= tail[0]/math.e)[0]
        efold = t_tail[m[0]] if len(m) else float("nan")
    else:
        efold = float("nan")
    # post-contact drainage tail: remaining released medium through the fused-state ring
    V_fin = lens(x_cont, R1s*1e3, R2s*1e3)[1]
    M_vented = RHO_MAX*V_fin/MSUN
    A_fin = 2*math.pi*lens(x_cont, R1s*1e3, R2s*1e3)[0]*w if cap == "ring" else A_ring_req
    M_rem = max(MREL - M_vented, 0.0)
    t_tail_ms = msun(M_rem)/(RHO_MAX*C0*A_fin)*1e3
    print(f"    {label:34s} fight time {ts[-1]*1e3:6.3f} ms  peak flux at {ts[pk]*1e3:5.2f} ms  "
          f"min u {us.min()/C0:.3f} c0  vented-in-fight {M_vented:.2f} Msun  "
          f"post-contact drain of {M_rem:.2f} Msun: {t_tail_ms:.3f} ms")
    return ts, fl

print(f"    (start: layer touch x0={x_touch/1e3:.1f} km, u0={math.sqrt(G*msun(M_TOT)/x_touch)/C0:.3f} c0)")
simulate(8.0e3, x_touch, math.sqrt(G*msun(M_TOT)/x_touch), "w=8 km const (parent scale)")
simulate(0.2051*R_cf, x_touch, math.sqrt(G*msun(M_TOT)/x_touch), "w=f*R_cf const")
simulate(R_cf/5, x_touch, math.sqrt(G*msun(M_TOT)/x_touch), "w=R_f/5 const")
simulate(None, x_touch, math.sqrt(G*msun(M_TOT)/x_touch), "constant A_ring=3.26e9 m2 (by tau)", cap="const")
print(f"    (parent start: x0=156.3 km, u0=0.765 c0)")
simulate(8.0e3, (T1+T2)*1e3, v0a, "w=8 km const, x0=156.3")
simulate(R_cf/5, (T1+T2)*1e3, v0a, "w=R_f/5 const, x0=156.3")

print("\n" + "="*100)
print("SWEEP: clean expressions from locked geometry vs 1403.03 km")
print("="*100)
target = C0*TAU_MEAS
gm  = G*msun(M_TOT)/C0**2        # GM/c0^2 = 91.55 km
cands = {
 "9*(t1+t2)": 9*(T1+T2), "32*43.7": 32*43.7, "2.8pi*edge": 2.8*math.pi*EDGE,
 "18*sqrt(t1*t2)": 18*math.sqrt(T1*T2), "3pi^2*core": 3*math.pi**2*R_cf/1e3,
 "4pi*t_merged": 4*math.pi*T_MERGED, "(2pi+1/2)*(edge+core)": (2*math.pi+0.5)*(EDGE+R_cf/1e3),
 "8/pi*6GM/c0^2": 8/math.pi*r_cc/1e3, "(23/3)*2GM/c0^2": (23/3)*r_tc/1e3,
 "sqrt3*(6GM/c0^2 - 2GM/c0^2)+2GM/c0^2": math.sqrt(3)*(r_cc-r_tc)/1e3 + r_tc/1e3,
 "2*sqrt3*GM/c0^2 (3.46 GM)": 2*math.sqrt(3)*gm/1e3,
 "6GM/c0^2/sqrt3 + 2GM/c0^2": r_cc/1e3/math.sqrt(3) + r_tc/1e3,
 "M1/(rho pi t1^2 c0)*c0 /1e3 (tau_d1*c0)": taud1*C0/1e3,
 "tau_d1*c0/sqrt2": taud1*C0/1e3/math.sqrt(2),
 "M_rel/(rho A_ring) with A=3.26e9": msun(MREL)/(RHO_MAX*3.26e9)/1e3,
 "pi*t1^2*sqrt2*M_rel/M1": math.pi*(T1*1e3)**2*math.sqrt(2)*msun(MREL)/msun(M1)/1e6,
 "(edge^2-core^2)/(edge+core) = edge-core": (EDGE**2-(R_cf/1e3)**2)/(EDGE+R_cf/1e3),
 "43.7*(rho_core/rho_max)^(2/3)": 43.7*(RHO_CORE/RHO_MAX)**(2/3),
 "sqrt(2GM/c0^2 * M_rel/(rho_max*A_ring))": math.sqrt(r_tc*msun(MREL)/(RHO_MAX*3.26e9))/1e3,
}
print(f"{'expression':55s} {'km':>9s} {'dev from 1403.03':>14s} {'f=c0/L':>9s} {'f=c0/(2piL)':>10s}")
tgt_km = target/1e3
for name, L in cands.items():
    L = L if isinstance(L, float) else L
    f1 = C0/(L*1e3); f2 = C0/(2*math.pi*L*1e3)
    flag = " <-- 232/272 Hz?" if (abs(f1-232)<6 or abs(f1-272)<6 or abs(f2-232)<6 or abs(f2-272)<6) else ""
    print(f"  {name:53s} {L:9.1f} {100*(L/tgt_km-1):+13.2f}% {f1:8.1f} {f2:9.1f}{flag}")

# ---- exhaustive combination sweep of the four locked radii ----
print("\n  exhaustive combination sweep (four radii, +-*/, powers 1/3..3, coeffs 1/4..4, pi, sqrt2, sqrt3):")
qs = {"Rc": R_cf/1e3, "t1": T1, "t2": T2, "Re": EDGE, "d": T1+T2, "m": T_MERGED,
      "ov": T1+T2-T_MERGED, "gm": gm/1e3, "2gm": r_tc/1e3, "6gm": r_cc/1e3}
hits = []
coefs = [0.25, 1/3, 0.5, 2/3, 0.75, 1.0, 4/3, 1.5, 2.0, 2.5, 3.0, 4.0,
         math.pi, 2*math.pi, math.pi/2, math.pi/3, 4*math.pi/3, 8/math.pi,
         math.sqrt(2), 1/math.sqrt(2), math.sqrt(3), 2/math.sqrt(3), math.e, 9.0, 32.0]
names = list(qs.keys()); vals = list(qs.values())
for i, (a, va) in enumerate(zip(names, vals)):
    for b, vb in zip(names[i:], vals[i:]):
        for c in coefs:
            for L, tag in [(c*(va+vb), f"{c:g}*({a}+{b})"), (c*va*vb, f"{c:g}*{a}*{b}"),
                           (c*va*vb/max(va+vb,1e-9), f"{c:g}*{a}*{b}/({a}+{b})"),
                           (c*math.sqrt(va*vb), f"{c:g}*sqrt({a}*{b})")]:
                if abs(L-tgt_km)/tgt_km < 0.01:
                    hits.append((abs(L-tgt_km)/tgt_km, L, tag))
hits.sort()
print("    top combinations within 1% of 1403.03 km:")
for dev, L, tag in hits[:14]:
    print(f"      {tag:42s} {L:9.1f} km  ({100*(L/tgt_km-1):+.2f}%)")

print("\n" + "="*100)
print("WITHDRAWN 232/272 Hz CHECK")
print("="*100)
f_272_R = C0/(272.0*2*math.pi)
print(f"  withdrawn-predicted 272 Hz <-> R = c0/(2pi f) = {f_272_R/1e3:.1f} km; "
      f"as a yield radius: a = GM/R^2 = {G*msun(M_TOT)/f_272_R**2:.2e} N/kg "
      f"(round-3 refit yield = 2.64e11 -> the withdrawn route was the yield-radius frequency)")
f_232_R = C0/(232.0*2*math.pi)
print(f"  withdrawn-extracted 232 Hz <-> R = {f_232_R/1e3:.1f} km; E1+E2 = {((E1r+E2r)/1e3):.1f} km gives "
      f"{C0/(2*math.pi*(E1r+E2r)):.1f} Hz (within {100*(C0/(2*math.pi*(E1r+E2r))/232-1):+.1f}% - flag, do not use)")
for name, tau in [("this route tau=4.68 ms -> 1/tau", TAU_MEAS), ("fight drag tau_d1 (6.62 ms)", taud1),
                  ("stopping distance 1330 km as wavelength", 1330e3/C0), ("stopping 1520 km", v0a*taud1/C0)]:
    print(f"  {name:42s}: f = {1/tau if tau>1e-3 else C0/(tau):.1f} Hz  (232? 272?  NO)")
print("  VERDICT: none of the fight/vent candidates reproduces 232 or 272 Hz; the withdrawn")
print("  yield-radius frequency route (272 Hz at the refit yield) is not revived by any candidate.")

print("\n" + "="*100)
print("BEST CANDIDATE EQUATIONS")
print("="*100)
print(f"  A) tau = M_core1/(sqrt2 * rho_max * pi * t1^2 * c0) = {taud1/math.sqrt(2)*1e3:.4f} ms "
      f"({100*(taud1/math.sqrt(2)/TAU_MEAS-1):+.2f}% vs 4.68)")
print(f"  B) tau = M_rel/(rho_max * c0 * A_ring), A_ring = sqrt2*pi*t1^2*M_rel/M_core1 = "
      f"{math.pi*(T1*1e3)**2*math.sqrt(2)*msun(MREL)/msun(M1):.3e} m2 = a ring of width "
      f"{math.pi*(T1*1e3)**2*math.sqrt(2)*msun(MREL)/msun(M1)/(2*math.pi*54.7e3)/1e3:.2f} km at radius 54.7 km")
print(f"  both need ONE unnamed factor (the sqrt2 = the pinch-drainage geometry factor):")
print(f"    -> with it: 4.6845 ms (0.1%); without it: 6.62 ms (41% high).")
print(f"  the pinch-ring width w = 4.8-9.5 km over the fight is NOT derivable from the locked")
print(f"  geometry alone -> missing input: the medium's gap-pressure / vena-contracta law P(rho,s)")
print(f"  (the repo's already-listed decompression law rho(r),P(r),c_s(r) - OPEN_WORK line 41).")
