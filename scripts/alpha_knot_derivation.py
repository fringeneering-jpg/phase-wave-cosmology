# -*- coding: utf-8 -*-
"""
PWC — attempt to derive alpha = e^2/(4 pi eps0 hbar c0) from the locked
720-degree toroidal double-loop knot topology alone.

Locked inputs (contract for this attempt):
  m_e R_e c0 = hbar/2,  R_e = hbar/(2 m_e c0) = 193.07 fm = lambda_C/(4 pi)
  double loop of total circumference lambda_C = h/(m_e c0)
  m_p R_p c0 = 4 hbar,  R_p = 0.8414 fm (charge radius)
  m_p/m_e = 8 R_e/R_p
  r_e = alpha * lambda_bar_C  (classical radius = alpha-compression of loop scale)
  the wave returns to itself after 4 pi (Dirac belt / double cover)

Honest-failure discipline: every near-miss is rejected unless a locked
mechanism produces it. Arithmetic on the locked numbers only, no fitted
parameters, no manufactured matches.
"""
import numpy as np

print("=" * 78)
print("PART 0 — CONSTANTS (CODATA 2022) AND LOCKED-GEOMETRY VERIFICATION")
print("=" * 78)

c0  = 299792458.0
h   = 6.62607015e-34
hbar = h / (2 * np.pi)
me  = 9.1093837139e-31
mp  = 1.67262192595e-27
mn  = 1.67492750056e-27
e   = 1.602176634e-19
alpha = 7.2973525643e-3          # CODATA 2022
eps0 = e * e / (2 * alpha * h * c0)
mu0  = 2 * alpha * h / (e * e * c0)

alpha_calc = e * e / (4 * np.pi * eps0 * hbar * c0)
inv_alpha  = 1.0 / alpha_calc

lamC   = h / (me * c0)
lambar = hbar / (me * c0)
Re     = hbar / (2 * me * c0)
Rp     = 0.8414e-15
Rp_calc = 4 * hbar / (mp * c0)
re_cl  = alpha * lambar

print(f"alpha (CODATA 2022)          = {alpha:.12e}")
print(f"alpha (computed from e,eps0)  = {alpha_calc:.12e}")
print(f"1/alpha                      = {inv_alpha:.12f}")
print(f"eps0, mu0 from {{e, alpha}}    : eps0 = {eps0:.12e}  mu0 = {mu0:.12e}")
print(f"  (1/sqrt(mu0 eps0) = {1/np.sqrt(mu0*eps0):.12e}  vs c0 = {c0:.9e})")
print()
print(f"lambda_C        = {lamC:.12e} m  ({lamC*1e12:.8f} pm)")
print(f"lambda_bar_C    = {lambar:.12e} m  ({lambar*1e15:.8f} fm)")
print(f"R_e             = {Re:.12e} m  ({Re*1e15:.8f} fm)   [locked 193.07 fm]")
print(f"R_p (locked)    = {Rp:.12e} m  ({Rp*1e15:.8f} fm)")
print(f"R_p = 4 hbar/(m_p c0) = {Rp_calc*1e15:.8f} fm")
print(f"r_e = alpha*lambar      = {re_cl*1e15:.8f} fm   [locked 2.818 fm]")

print()
print("locked-relation checks:")
print(f"  2*pi*R_e            = {2*np.pi*Re:.12e}  vs lamC/2 = {lamC/2:.12e}  "
      f"(ratio {2*np.pi*Re/(lamC/2):.12f})")
print(f"  4*pi*R_e            = {4*np.pi*Re:.12e}  vs lamC   = {lamC:.12e}  "
      f"(ratio {4*np.pi*Re/lamC:.12f})")
print(f"  R_e/(lamC/4pi)      = {Re/(lamC/(4*np.pi)):.12f}")
print(f"  m_p/m_e             = {mp/me:.9f}   [CODATA 1836.15267343]")
print(f"  8 R_e/R_p           = {8*Re/Rp:.6f}   [locked ~1834-1836]")
print(f"  R_e/R_p             = {Re/Rp:.6f}")
print(f"  m_e c0 R_e / hbar   = {me*c0*Re/hbar:.12f}   [locked 1/2]")
print(f"  m_p c0 R_p / hbar   = {mp*c0*Rp/hbar:.6f}   [locked 4]")
print(f"  2*pi*R_p / lam_p    = {2*np.pi*Rp/(h/(mp*c0)):.6f}   [locked 4]")
print(f"  r_e/(2 alpha R_e)   = {re_cl/(2*alpha*Re):.12f}   [locked 1]")
print(f"  R_e/r_e             = {Re/re_cl:.9f}  = 1/(2 alpha) = {1/(2*alpha):.9f}")

# ==========================================================================
print()
print("=" * 78)
print("PART 1 — KNOT GEOMETRIC INVARIANTS (the double loop / Moebius band)")
print("=" * 78)

circ_loop  = 2 * np.pi * Re
path_total = 2 * circ_loop
A_loop   = np.pi * Re**2
A_double = 2 * np.pi * Re**2
print(f"one-loop circumference 2 pi R_e = {circ_loop:.12e} m = lamC/2 ({circ_loop/(lamC/2):.12f})")
print(f"total path length = {path_total:.12e} m = lamC ({path_total/lamC:.12f})")
print("phase advance per traversal of lamC = 2 pi (one full wave cycle)")
print("phase advance for return-to-identity = 4 pi  (double cover, spin-1/2)")
print(f"enclosed area, one loop    pi R_e^2   = {A_loop:.6e} m^2")
print(f"enclosed area, double loop 2 pi R_e^2 = {A_double:.6e} m^2")
print(f"  A_loop/lamC^2   = {A_loop/lamC**2:.9f}  = 1/(16 pi) = {1/(16*np.pi):.9f}")
print(f"  A_double/lamC^2 = {A_double/lamC**2:.9f}  = 1/(8 pi)  = {1/(8*np.pi):.9f}")
print(f"  A_double/lambar^2 = {A_double/lambar**2:.9f}  = pi/2 = {np.pi/2:.9f}")

# --- Gauss linking / writhing numerics -----------------------------------
def link_integral(r1, t1, r2, t2, dt1, dt2):
    """Gauss linking integral (1/4pi) SS (r1-r2).(dr1 x dr2)/|r1-r2|^3 dt1 dt2."""
    L = 0.0
    for i in range(len(t1)):
        x1, y1, z1 = r1[i]
        v1 = (r1[(i+1) % len(t1)] - r1[(i-1) % len(t1)]) / (2*dt1)
        dx1, dy1, dz1 = v1
        for j in range(len(t2)):
            x2, y2, z2 = r2[j]
            v2 = (r2[(j+1) % len(t2)] - r2[(j-1) % len(t2)]) / (2*dt2)
            dx2, dy2, dz2 = v2
            rx, ry, rz = x1-x2, y1-y2, z1-z2
            r3 = (rx*rx + ry*ry + rz*rz)**1.5
            if r3 == 0: continue
            L += (rx*(dy1*dz2 - dz1*dy2) + ry*(dz1*dx2 - dx1*dz2)
                  + rz*(dx1*dy2 - dy1*dx2)) / r3
    return L * dt1 * dt2 / (4 * np.pi)

def writhe_self(r, t, dt, exclude, T):
    """Writhing number of one closed curve of period T, excluding near-coincident pairs."""
    n = len(t)
    W = 0.0
    for i in range(n):
        x1, y1, z1 = r[i]
        v1 = (r[(i+1) % n] - r[(i-1) % n]) / (2*dt)
        dx1, dy1, dz1 = v1
        for j in range(n):
            d = abs(t[i] - t[j])
            if d < exclude or abs(d - T) < exclude or i == j:
                continue
            x2, y2, z2 = r[j]
            v2 = (r[(j+1) % n] - r[(j-1) % n]) / (2*dt)
            dx2, dy2, dz2 = v2
            rx, ry, rz = x1-x2, y1-y2, z1-z2
            r3 = (rx*rx + ry*ry + rz*rz)**1.5
            if r3 == 0: continue
            W += (rx*(dy1*dz2 - dz1*dy2) + ry*(dz1*dx2 - dx1*dz2)
                  + rz*(dx1*dy2 - dy1*dx2)) / r3
    return W * dt * dt / (4 * np.pi)

R = 1.0
n  = 400
t1 = np.linspace(0, 2*np.pi, n, endpoint=False)
cA  = np.stack([R*np.cos(t1), R*np.sin(t1), np.zeros_like(t1)], axis=1)
cB_side = np.stack([R*np.cos(t1), R*np.sin(t1), 0.1*R*np.ones_like(t1)], axis=1)
# Hopf-linked: circle in the xz-plane centered at (R,0,0) — pierces the xy-disk once
cB_hopf = np.stack([R + R*np.cos(t1), np.zeros_like(t1), R*np.sin(t1)], axis=1)

dt1 = t1[1] - t1[0]
lk_side = link_integral(cA, t1, cB_side, t1, dt1, dt1)
lk_hopf = link_integral(cA, t1, cB_hopf, t1, dt1, dt1)
print()
print("linking-number numerics (Gauss integral, n = %d):" % n)
print(f"  Lk(two loops side-by-side, parallel)   = {lk_side:+.6f}   (expect 0)")
print(f"  Lk(two loops interlinked, Hopf)        = {lk_hopf:+.6f}   (expect +-1)")
wr_circle = writhe_self(cA, t1, dt1, exclude=0.05, T=2*np.pi)
print(f"  Wr(single planar circle)               = {wr_circle:+.6f}   (expect 0)")

# Moebius band boundary = the 720-degree double loop:
# r(theta) = ((R + a cos(theta/2)) cos theta, (R + a cos(theta/2)) sin theta, a sin(theta/2)),
# theta in [0, 4 pi); a = band half-width (torus minor radius).
def mobius_boundary(a_band, th):
    u = th/2
    return np.stack([(R + a_band*np.cos(u))*np.cos(th),
                     (R + a_band*np.cos(u))*np.sin(th),
                     a_band*np.sin(u)], axis=1)
def mobius_tangent(a_band, th):
    u = th/2
    su, cu = np.sin(u), np.cos(u)
    st, ct = np.sin(th), np.cos(th)
    return np.stack([-(R + a_band*cu)*st - (a_band/2)*su*ct,
                      (R + a_band*cu)*ct - (a_band/2)*su*st,
                      (a_band/2)*cu], axis=1)
def mobius_normal(a_band, th):
    u = th/2
    return np.stack([-np.cos(u)*np.cos(th), -np.cos(u)*np.sin(th), -np.sin(u)], axis=1)

def link_analytic(r1, dr1, r2, dr2, dt):
    """Gauss linking integral with analytic tangents."""
    L = 0.0
    n = len(r1)
    for i in range(n):
        x1, y1, z1 = r1[i]; dx1, dy1, dz1 = dr1[i]
        for j in range(n):
            x2, y2, z2 = r2[j]; dx2, dy2, dz2 = dr2[j]
            rx, ry, rz = x1-x2, y1-y2, z1-z2
            r3 = (rx*rx + ry*ry + rz*rz)**1.5
            if r3 == 0: continue
            L += (rx*(dy1*dz2 - dz1*dy2) + ry*(dz1*dx2 - dx1*dz2)
                  + rz*(dx1*dy2 - dy1*dx2)) / r3
    return L * dt * dt / (4 * np.pi)

for a_band, nM, eps_p in [(0.1, 500, 0.02), (0.05, 700, 0.01)]:
    th = np.linspace(0, 4*np.pi, nM, endpoint=False)
    dth = th[1] - th[0]
    cM = mobius_boundary(a_band, th)
    wr_mob = writhe_self(cM, th, dth, exclude=0.05, T=4*np.pi)
    cM_push = cM + eps_p*mobius_normal(a_band, th)
    lk_mob = link_analytic(cM, mobius_tangent(a_band, th),
                           cM_push,
                           mobius_tangent(a_band, th)
                           + eps_p*np.stack([0.5*np.sin(th/2)*np.cos(th) + np.cos(th/2)*np.sin(th),
                                             0.5*np.sin(th/2)*np.sin(th) - np.cos(th/2)*np.cos(th),
                                             -0.5*np.cos(th/2)], axis=1),
                           dth)
    print(f"  Moebius boundary (a/R = {a_band}, push eps = {eps_p}):")
    print(f"    Wr(boundary) = {wr_mob:+.6f}   (expect +-1: one clasp crossing)")
    print(f"    Lk(boundary, band-normal push-off) = {lk_mob:+.6f}   (expect +-2)")
print("  => invariants of the 720-degree knot:  Wr = +-1,  Tw = Lk - Wr = +-1")
print("     (one full turn of the framing over the double loop = half-twist 1/2")
print("     per loop),  Lk = +-2  — the Seifert framing of a Moebius band is")
print("     +-2, i.e. 2 x 2 pi = 4 pi = the 720-degree double cover, in units")
print("     of 2 pi.  Holonomy per loop = -1 (Z2).  All O(1) integers/halves.")

# ==========================================================================
print()
print("=" * 78)
print("PART 2 — CHARGE FROM CIRCULATION (far field, flux, moment)")
print("=" * 78)

I   = e * c0 / lamC
B1  = mu0 * I / (2 * Re)
B2  = 2 * B1
Phi1 = B1 * A_loop
Phi2 = B2 * A_loop
Phi0 = h / e
print(f"circulating current I = e c0/lamC = {I:.6e} A")
print(f"B(center), one loop  = {B1:.6e} T")
print(f"flux through one loop's own disk, Phi1 = {Phi1:.6e} Wb")
print(f"self-flux, double loop, Phi2 = {Phi2:.6e} Wb")
print(f"  Phi2/Phi0 = {Phi2/Phi0:.9f}   = alpha/2 = {alpha/2:.9f}")
print(f"  e*Phi2/hbar = {e*Phi2/hbar:.9f}   = pi*alpha = {np.pi*alpha:.9f}")
print("  (EXACT but circular: e appears on both sides (current and phase), so")
print("   this re-expresses alpha; it does not derive it.)")

muB   = e * hbar / (2 * me)
mu_dl = 2 * I * A_loop          # two loops, each carrying current I = e c0/lamC
print()
print(f"magnetic moment of the double loop, mu = 2 * I * A_loop = {mu_dl:.6e} J/T")
print(f"Bohr magneton muB = e hbar/(2 m_e) = {muB:.6e} J/T")
print(f"  mu/muB = {mu_dl/muB:.9f}   (= 1/2)")
print(f"  with the 4-pi double-cover phase counted (effective winding 2):")
print(f"  mu_eff/muB = {2*mu_dl/muB:.9f}   -> g = 2 emerges from the 720-degree")
print("  structure, NOT from a fitted factor.  This is the one clean topological")
print("  output: spin hbar/2 (locked m_e R_e c0 = hbar/2) + double circulation")
print("  -> mu_B.  alpha does not appear anywhere in it.")
print()
print("Angular momentum: L = m_e c0 R_e = %.3f hbar  [locked 1/2]" % (me*c0*Re/hbar))
print("Phase circulation quantum: winding number n = 1 (electron), n = 8 (proton)")
print("  -> dimensionless circulation numbers available: {1/2, 1, 2, 4, 8, ...}.")
print("  137.036 is none of them: the MAGNITUDE of e is not a winding number.")
print()
print("Far field of the double loop:")
print("  E_monopole = q/(4 pi eps0 r^2) with q ASSIGNED = e  (no derivation)")
print("  B_dipole   ~ mu/r^3 with mu = muB (derived above, g = 2)")
print("  electric dipole moment = 0 (symmetric loop).  The winding produces")
print("  no charge; it fixes only integer circulations and the g-factor.")

A_Phi0 = Phi0 / B2
print()
print(f"area enclosing one flux quantum at the double loop's central field:")
print(f"  A_Phi0 = Phi0/B(center) = {A_Phi0:.6e} m^2")
print(f"  A_Phi0/A_double = {A_Phi0/A_double:.9f}   = 1/alpha = {1/alpha:.9f}")
print("  (EXACT but circular: Phi0 = h/e and B ~ e -> the e^2 cancels into alpha.)")

# ==========================================================================
print()
print("=" * 78)
print("PART 3 — SELF-ENERGY ROUTE: the aspect ratio is the missing datum")
print("=" * 78)

def f_ring(R_over_a, npts=400000):
    """Dimensionless self-energy coefficient of a uniformly charged thin ring,
    line-regularized:  U = q^2/(4 pi eps0 R) * f,  f = (R/2) * mean(1/den),
    den = sqrt(4 R^2 sin^2(phi/2) + a^2).  Thin-ring textbook asymptote
    (surface charge on the wire): f -> [ln(8R/a) - 2]/(2 pi); the O(1)
    constant depends on the (unlocked) charge distribution on the wire."""
    ph = np.linspace(0, 2*np.pi, npts, endpoint=False)
    den = np.sqrt(4*R_over_a**2*np.sin(ph/2)**2 + 1.0)
    return (R_over_a/2) * np.mean(1.0/den)

print("ring self-energy coefficient f(R/a) — numeric (line regularization):")
for ratio in [100, 1000, 10000]:
    fnum = f_ring(ratio)
    print(f"  R/a = {ratio:7d}:  f = {fnum:.6f}   2 pi f = {2*np.pi*fnum:.4f}   "
          f"ln(8R/a) = {np.log(8*ratio):.4f}   "
          f"(textbook surface-charge const: {2*np.pi*fnum - np.log(8*ratio):+.4f} vs -2)")
print("  -> f = [ln(8R/a) + O(1)]/(2 pi): log-running; the O(1) constant is")
print("     regularization-dependent (it depends on how the wave's charge sits")
print("     on the wire — an UNLOCKED datum in itself).")

# Electrostatic self-energy, single loop (charge q on one circle):
#   U = q^2/(4 pi eps0 R_e) f ;  U = m_e c^2 = hbar c0/(2 R_e)
#   -> alpha = 1/(2 f)
# Coincident double loop (two strands, total charge e): U = (3/2) U_single(q=e)
#   -> alpha = 1/(3 f)
f_need_single = 1/(2*alpha)
f_need_double = 1/(3*alpha)
print()
print("demand U_electrostatic = m_e c^2:")
print(f"  single loop:   alpha = 1/(2 f)  ->  f = {f_need_single:.6f}")
print(f"  double loop:   alpha = 1/(3 f)  ->  f = {f_need_double:.6f}")
ln_s = 2*np.pi*f_need_single          # ln(8R/a) - 2  (textbook const)
ln_d = 2*np.pi*f_need_double
ln_m = 4*np.pi/alpha                  # magnetic version: alpha = 4 pi/[ln(8R/a)-2]
def p10(x):
    return (x + 2 - np.log(8)) / np.log(10)
print("  with f = [ln(8R/a)-2]/(2 pi):")
print(f"    single: ln(8R_e/a) - 2 = pi/alpha      = {ln_s:.6f}")
print(f"            ->  R_e/a = e^{ln_s+2:.3f}/8 = 10^{p10(ln_s):.3f}   (absurd)")
print(f"    double: ln(8R_e/a) - 2 = 2 pi/(3 alpha) = {ln_d:.6f}")
print(f"            ->  R_e/a = e^{ln_d+2:.3f}/8 = 10^{p10(ln_d):.3f}   (absurd)")
print(f"    magnetic self-energy (1/2 L I^2): alpha = 4 pi/[ln(8R/a)-2]")
print(f"            ln(8R_e/a) - 2 = 4 pi/alpha   = {ln_m:.6f}")
print(f"            ->  R_e/a = e^{ln_m+2:.3f}/8 = 10^{p10(ln_m):.3f}   (absurd)")
print("  Any value of alpha can be matched by moving a: the aspect ratio is a")
print("  FREE parameter, and 1/137.036 only fixes log(8R/a). Nothing in the")
print("  locked knot fixes a -> alpha is not derived by self-energy.")

print()
print("aspect ratio a/R_e that alpha = 1/137.036 WOULD demand under simple laws")
print("(a = torus minor radius = wave transverse extent):")
variants = [
    ("alpha = (a/R)/(4 pi)",          4*np.pi*alpha),
    ("alpha = (a/R)^2/(4 pi)",        np.sqrt(4*np.pi*alpha)),
    ("alpha = (a/R)^2/(2 pi)",        np.sqrt(2*np.pi*alpha)),
    ("alpha = (a/R)^3/(4 pi)",        (4*np.pi*alpha)**(1/3)),
    ("alpha = (a/R)^2",               np.sqrt(alpha)),
]
for name, aR in variants:
    print(f"  {name:26s} -> a/R_e = {aR:.6f}   a = {aR*Re*1e15:8.4f} fm   a/R_p = {aR*Re/Rp:8.3f}")
print("  None of these a values is locked; each is a NEW datum the model would")
print("  have to supply (e.g. a confinement eigenvalue). Closest accidental hit:")
print(f"  a = 4 pi alpha R_e = {4*np.pi*alpha*Re*1e15:.4f} fm = {4*np.pi*alpha*Re/Rp:.3f} R_p"
      "  (~21, but no locked mechanism).")

# ==========================================================================
print()
print("=" * 78)
print("PART 4 — CANDIDATE IDENTIFICATIONS, TESTED WITH NUMBERS")
print("=" * 78)

print("Target: alpha = {:.12e}, 1/alpha = {:.12f}".format(alpha, 1/alpha))
print("Precision demanded: alpha known to ~1.5e-10 relative; a candidate must")
print("match to ~1e-9.  Anything at 1e-2..1e-6 is a decisive failure.")
print()

print("(a) alpha = (loop radius ratio)^p :")
p = np.log(alpha)/np.log(Rp/Re)
print(f"    (R_p/R_e)^p = alpha  ->  p = ln(alpha)/ln(R_p/R_e) = {p:.6f}")
print(f"    (R_e/R_p)^p = 1/alpha ->  p = {np.log(1/alpha)/np.log(Re/Rp):.6f}")
print(f"    nearest rationals: 19/21 = {19/21:.6f} -> (R_e/R_p)^(19/21) = "
      f"{(Re/Rp)**(19/21):.3f} (off {(Re/Rp)**(19/21)*alpha-1:+.2e});"
      f"  9/10 = 0.9 -> {(Re/Rp)**0.9:.3f}")
print("    -> exponent 0.90515 is NOT locked by anything; REJECT.")

print()
print("(b) alpha = 1/(4 pi * integer) forms:")
print(f"    4 pi * 137.036             = {4*np.pi*inv_alpha:.6f}")
print(f"    137.036/(4 pi)             = {inv_alpha/(4*np.pi):.6f}  (needed 'integer' n)")
print(f"    137.036/(4 pi^2)           = {inv_alpha/(4*np.pi**2):.6f}   "
      f"(cf. 2 sqrt 3 = {2*np.sqrt(3):.6f}, off {inv_alpha/(4*np.pi**2)/(2*np.sqrt(3))-1:+.2e})")
print(f"    best integer form 1/(44 pi) = {1/(44*np.pi):.9f}  -> off by {1/(44*np.pi)/alpha-1:+.3e}")
print(f"    (15/2)*(R_e/R_p) = {7.5*Re/Rp:.4f}  vs 4 pi*137.036, off {7.5*Re/Rp/(4*np.pi*inv_alpha)-1:+.2e}")
print("    -> n = 10.90498 is not an integer and is not a knot invariant; REJECT.")
print(f"    near-misses: 44 pi = {44*np.pi:.6f} (off {44*np.pi/inv_alpha-1:+.3e});  "
      f"16 pi e = {16*np.pi*np.e:.6f} (off {16*np.pi*np.e/inv_alpha-1:+.3e});")
print(f"    2^7+3^2 = 137 (off {137/inv_alpha-1:+.3e});  4 pi^3+pi^2+pi = "
      f"{4*np.pi**3+np.pi**2+np.pi:.6f} (off {(4*np.pi**3+np.pi**2+np.pi)/inv_alpha-1:+.3e})")
print("     — the last one matches to 6 digits but is a 3-term numerology with no")
print("       knot mechanism; REJECT per the framework's own rule.")

print()
print("(c) area / path-length ratios (locked, alpha-free):")
print(f"    A_loop/lamC^2   = 1/(16 pi) = {1/(16*np.pi):.9f}")
print(f"    A_double/lamC^2 = 1/(8 pi)  = {1/(8*np.pi):.9f}")
print(f"    alpha/(A_double/lamC^2) = 8 pi alpha = {8*np.pi*alpha:.9f} = 1/5.45239")
print("    -> the locked area ratio misses alpha by the exact factor 8 pi alpha;")
print("       no locked datum repairs it. REJECT.")

print()
print("(d) other geometric ratios of the locked scales:")
print("   " + "-"*74)
print("   ratio                                  value        note")
print("   " + "-"*74)
rows = [
    ("R_p/R_e",                      Rp/Re,   "alpha-free, no hit"),
    ("R_e/R_p",                      Re/Rp,   "alpha-free, no hit"),
    ("(R_e/R_p)^2",                  (Re/Rp)**2, "alpha-free, no hit"),
    ("R_e/(1.202 fm)",               Re/1.202e-15, "alpha-free, no hit"),
    ("2 pi R_e/lamC (= 1/2)",        2*np.pi*Re/lamC, "alpha-free, no hit"),
    ("alpha*R_e/R_p   (cf. 5/3)",    alpha*Re/Rp, "contains alpha; 5/3 off 0.47%"),
    ("(R_p/R_e)/alpha (cf. 3/5)",    (Rp/Re)/alpha, "contains alpha; 3/5 off 0.47%"),
    ("alpha^2*(R_e/R_p)^2 (cf. 2sqrt2)", alpha**2*(Re/Rp)**2, "contains alpha; off 0.9%"),
    ("r_e/R_e = 2 alpha",            re_cl/Re,  "circular (definition)"),
    ("lambar/r_e = 1/alpha",         lambar/re_cl, "circular (definition)"),
    ("lamC/r_e = 2 pi/alpha",        lamC/re_cl, "circular (definition)"),
    ("2 lamC/r_e = 4 pi/alpha",      2*lamC/re_cl, "circular (definition)"),
]
for name, val, note in rows:
    print(f"   {name:38s} {val:14.6f}   {note}")
print(f"   1.202 fm / R_p = {1.202e-15/Rp:.8f}  vs 10/7 = {10/7:.8f}  (off {1.202e-15/Rp/(10/7)-1:+.2e})")
print("   -> the only tight coincidence found (1.202 fm = (10/7) R_p to 2e-7),")
print("      but it involves no alpha and has no locked mechanism tying it to the")
print("      charge; it cannot rescue alpha.  All exact 137.036 'hits' above are the")
print("      locked relation r_e = alpha lambar_C restated — circular.")

print()
print("(e) the 43.2 GeV = 46 nucleon masses hint:")
E46 = 46 * (mp + mn) / 2 * c0**2 / (1.602176634e-19 * 1e9)
print(f"    46 nucleons (p/n average) = {E46:.3f} GeV")
print(f"    137.036/pi                = {inv_alpha/np.pi:.4f}   (off {inv_alpha/np.pi/E46-1:+.3e})")
print(f"    137.036/46                = {inv_alpha/46:.5f}      (cf. 3, off {inv_alpha/46/3-1:+.3e})")
print("    -> 1% off, no mechanism; REJECT.")

print()
print("(f) winding/linking integers available in the locked knot:")
print("    {Tw per loop = 1/2,  Wr = 1,  Tw = 1,  Lk = 2,  winding n = 1,  n = 8,")
print("     g = 2,  loops = 2}")
print(f"    none of 137.036, {inv_alpha/(4*np.pi):.4f}, {inv_alpha/np.pi:.4f}, "
      f"{4*np.pi*inv_alpha:.4f} is in the integer span")
print("    {1/2, 1, 2, 4, 8} x {1, pi, 2 pi, 4 pi, 1/(4 pi), 1/(8 pi)}.  REJECT all.")

# ==========================================================================
print()
print("=" * 78)
print("PART 5 — WHAT A SUCCESSFUL DERIVATION WOULD REQUIRE")
print("=" * 78)
print("1. The required 'topological invariant' with value 137.036 does not exist")
print("   in the locked knot. The locked dimensionless set is")
print("   {1/2, 1, 2, 4, 8, 2 pi, 4 pi, 1/(4 pi), 1/(8 pi), 229.47, 1835.7, ...}")
print("   and all are O(1) integers/fractions. 137.036 cannot be a winding,")
print("   linking, writhe or twist number of this knot.")
print("2. The only place 137.036 can live is a LOGARITHM of an aspect ratio,")
print("   i.e. a self-energy: 1/alpha = (3/(2 pi))[ln(8 R_e/a) - 2]  (double-loop")
print(f"   electrostatic), requiring R_e/a = 10^{p10(ln_d):.3f}; the single-loop")
print(f"   form 1/alpha = [ln(8R/a)-2]/pi requires R_e/a = 10^{p10(ln_s):.3f}; the")
print(f"   magnetic form 1/alpha = [ln(8R/a)-2]/(4 pi) requires 10^{p10(ln_m):.3f}.")
print("3. The missing datum is therefore the TORUS ASPECT RATIO R_e/a —")
print("   equivalently the transverse extent a of the wave (the torus minor")
print("   radius). It is NOT in the locked set: the locked inputs fix only R_e,")
print("   R_p and their ratio via the mass ratio. Granting a fixes alpha by")
print("   definition (a/R_e = 4 pi alpha = 0.0917 -> a = 17.7 fm = 21.0 R_p),")
print("   but nothing in the locked topology produces 0.0917.")
print("4. Therefore: alpha is NOT derivable from the locked knot topology alone.")
print("   The derivation chain would need ONE extra physical datum — a locked")
print("   aspect ratio or an equivalent confinement/self-consistency condition")
print("   that fixes ln(8 R_e/a) — and that datum is exactly the charge scale")
print("   {e, alpha} in disguise.")
print("=" * 78)
