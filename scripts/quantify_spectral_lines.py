# quantify_spectral_lines.py -- the spectral line ladder of Phase Wave Cosmology (PWC),
# quantified from LOCKED constants only.
#
# RULES (task brief 2026-10-21):
#   * ZERO fitted parameters -- every number is a locked constant, an exact SI
#     definition, a mathematical root, or a named literature measurement, with
#     provenance stated per number.
#   * Provenance per number.  Misses reported, never hidden -- candidates that
#     fail are printed, not suppressed.  OPEN is a report, not a crash.
#   * Kill condition per candidate.
#   * Exit code 0 always.
#
# TARGETS:
#   1. 502 nm frustration channel: delta = (6phi^2 - 5pi)/(5pi), dU = delta*U = 2.47 eV
#   2. 18.8 um proton line, 0.0658 eV (papers' V2 target: prediction-shaped, not claimed)
#   3. 21 cm hydrogen line (hyperfine spin-flip; try alpha^4 m_e^2/m_p and the fold pieces)
#   4. CMB peak wavelength from T_CMB = 2.7255 K (Wien)
#   5. Lyman-alpha 121.567 nm (try 13.606 eV = alpha^2 m_e c0^2/2)
import math

# ----------------------------------------------------------------------
# LOCKED CONSTANTS (provenance per number)
# ----------------------------------------------------------------------
c0      = 2.99792458e8       # exact, SI definition (CGPM 1983)
s       = 1.0/19.0           # PWC locked debt share, F_EM/F_debt = 19 (D3)
f_solid = 8.4989e-4          # PWC locked solid sieve fraction (back-solved to G; D39)
T_t     = 27.0               # PWC locked tightening coefficient T = 3^3 (D14/D31)
T7b     = 1.0/57.0           # PWC locked bound T7 shear = s/3 (lepton T7 spread)
T7d     = 20.0/1083.0        # PWC locked decay T7 shear = (20/19)(1/57)
N       = 16.0               # PWC locked 16-fold clock
alpha   = 1.0/137.035999084  # CODATA 2018 fine-structure constant
m_p     = 938.272088         # CODATA 2018 proton mass [MeV]
m_e     = 0.51099895         # CODATA 2018 electron mass [MeV]
m_n     = 939.5654205        # CODATA 2018 neutron mass [MeV]
X17     = 16.8421            # PWC locked X17 = N*(20/19) = 320/19 [MeV]
pi0     = 134.9768           # PDG 2020 neutral pion mass [MeV]
dU      = 2.470              # PWC locked frustration energy [eV] (D12)
hbar    = 1.054571817e-34    # CODATA 2018 reduced Planck constant [J s]
kB      = 1.380649e-23       # exact, SI definition (CGPM 2019) [J/K]
T_CMB   = 2.7255             # COBE/FIRAS 2009 (Fixsen) CMB temperature [K]
phi     = (1.0 + math.sqrt(5.0))/2.0   # golden ratio
pi      = math.pi

# derived exact (no free parameters)
h       = 2.0*pi*hbar                 # Planck constant, exact from locked hbar
eV      = 1.602176634e-19             # exact, SI definition (CGPM 2019)
hc_eVnm = h*c0/eV*1.0e9               # 1239.841984... eV nm, exact from locked
me_mp   = m_e/m_p                     # mass ratio from locked CODATA masses

print('='*78)
print('PWC SPECTRAL LINE LADDER -- locked constants only, zero fitted parameters')
print('='*78)
print(f'hc = {hc_eVnm:.6f} eV nm   (h = 2*pi*hbar, exact)')

# ----------------------------------------------------------------------
# 1. THE 502 nm FRUSTRATION CHANNEL
# ----------------------------------------------------------------------
print()
print('#1  THE 502 nm FRUSTRATION CHANNEL  (D12)')
print('-'*78)
delta  = (6.0*phi**2 - 5.0*pi)/(5.0*pi)
U_imp  = dU/delta
lam502 = hc_eVnm/dU
print(f'golden bridge: 6 phi^2 = {6*phi**2:.10f}  vs  5 pi = {5*pi:.10f}  '
      f'(bridge holds to {100*(6*phi**2/(5*pi)-1):+.4f}%)')
print(f'delta = (6 phi^2 - 5 pi)/(5 pi) = {delta:.6e}   (paper claims 1.532e-5; '
      f'match at 4 sig figs: {delta/1.532e-5*100:.4f}%)')
print('NOTE: delta IS the golden bridge residual -- frustration strain and bridge')
print('      mismatch are the same number.')
print(f'U implied = dU/delta = {dU:.4f}/{delta:.6e} = {U_imp:.1f} eV = {U_imp/1e3:.3f} keV')
print('      -> U has NO numerical value anywhere in the papers (only dU = delta x U is')
print(f'         locked). U = {U_imp/1e3:.2f} keV is implied but UNANCHORED -> provenance OPEN.')
print(f'lambda = h c0 / dU = {hc_eVnm:.6f}/{dU} = {lam502:.4f} nm   vs the paper 502.0 nm')
print(f'      residual = {lam502-502.0:+.4f} nm = {100*(lam502/502.0-1):+.4f}%')
print(f'round trip: 502.0 nm -> {hc_eVnm/502.0:.5f} eV   (the locked 2.47 eV is 3-sig-fig)')
print('VERDICT: arithmetic VERIFIED at the lock own precision (2.47 eV, 3 sig figs).')
print('CONTENT: the wavelength adds nothing beyond the locked dU (same number converted);')
print('         the independent content is delta (phi/pi bridge) only.')

# ----------------------------------------------------------------------
# 2. THE 18.8 um PROTON LINE (0.0658 eV)
# ----------------------------------------------------------------------
print()
print('#2  THE 18.8 um PROTON LINE, 0.0658 eV  (V2 target)')
print('-'*78)
E18   = hc_eVnm/18.8e3    # energy of 18.8 um in eV (18.8 um = 18800 nm)
lam65 = hc_eVnm/0.0658    # wavelength of 0.0658 eV in nm
print('round trip check of the paper pair:')
print(f'  0.0658 eV -> {lam65:.3f} um ;  18.8 um -> {E18:.6f} eV')
print('  the pair is internally consistent at 2 sig figs only; at 3 sig figs they are')
print(f'  {100*(lam65/18.8e3-1):+.2f}% apart (energy-primary) / {100*(E18/0.0658-1):+.2f}% (wavelength-primary).')
print('zero-parameter probes from LOCKED pieces only (none claim, all reported):')
probes2 = [
    ('dU * T7b',                     dU*T7b),
    ('dU * T7d',                     dU*T7d),
    ('dU * T7b * (3/2)  [3/2 UNLOCKED, flag]', dU*T7b*1.5),
    ('dU * T7d * (3/2)  [3/2 UNLOCKED, flag]', dU*T7d*1.5),
    ('alpha^3 m_e c^2 / 3  [structure UNLOCKED, flag]', alpha**3*m_e*1e6/3.0),
    ('pi0 * f_solid^3',              pi0*f_solid**3*1e6),
    ('kB * T_CMB',                   kB*T_CMB/eV),
    ('m_p c^2 * f_solid^3',          m_p*f_solid**3*1e6),
]
for name, E in probes2:
    print(f'  {name:46s} -> {E:.6e} eV  ({hc_eVnm/E:8.2f} um)   '
          f'vs 0.0658 eV: {100*(E/0.0658-1):+.2f}%')
print('VERDICT: OPEN.  The papers themselves label it prediction-shaped, not claimed')
print('(D12/A6); no locked route on disk reproduces 0.0658 eV. Nearest probes need')
print('unlocked factors (3/2, alpha^3 m_e/3); none within 0.5% except flagged forms.')
# ----------------------------------------------------------------------
# 3. THE 21 cm HYDROGEN LINE (electron spin-flip in the cage)
# ----------------------------------------------------------------------
print()
print('#3  THE 21 cm HYDROGEN LINE  (hyperfine, electron spin-flip)')
print('-'*78)
nu_obs   = 1420.405751786e6   # Hz, Hellwig et al. 1970 hydrogen maser standard (the measurement, not locked)
E_obs    = h*nu_obs/eV
E_skel   = (4.0/3.0)*alpha**4*m_e*1e6*me_mp   # Fermi skeleton, locked route only
g_p_ext  = 5.5856946893                     # CODATA 2018 proton g-factor (EXTERNAL -- NOT in locked set)
E_fermi  = E_skel*g_p_ext
g_need   = E_obs/E_skel
print(f'observed: 1420.40575 MHz = {E_obs:.6e} eV   (task 5.874e-6 eV -> match at 4 sig figs)')
print('locked route (Fermi contact skeleton; the 4/3 spin-sum drops out of the 1s derivation):')
print(f'  E = (4/3) alpha^4 m_e c0^2 (m_e/m_p) = {E_skel:.6e} eV  = {E_skel/(h/eV)/1e6:.2f} MHz')
print(f'  -> MISS by a factor {E_obs/E_skel:.4f} (residual {100*(E_skel/E_obs-1):+.2f}%).')
print(f'  The missing factor IS the proton magnetic moment: g_p needed = {g_need:.5f}')
print(f'  vs CODATA g_p = {g_p_ext:.10f} (EXTERNAL, not in the locked set).')
print(f'with the external g_p: (4/3) g_p alpha^4 m_e c^2 (m_e/m_p) = {E_fermi:.6e} eV')
print(f'  vs observed {E_obs:.6e} eV -> residual {1e6*(E_fermi/E_obs-1):+.1f} ppm')
print('  (the remaining +531 ppm is the unlocked correction content -- reduced mass, the')
print('   electron g-2 anomaly, proton structure, QED -- none of it in the locked set).')
print(f'fold-piece probes for the needed g_p ~ {g_need:.5f} (all UNLOCKED, reported not claimed):')
probes3 = [
    ('16 pi / 9  (= N pi / 9; via golden bridge phi^2 = 5pi/6 -> phi^2 + pi/2 = 4pi/3)',
     16.0*pi/9.0),
    ('(4/3)(phi^2 + pi/2)  [4/3 = the spin-sum; phi^2+pi/2 UNLOCKED]', (4.0/3.0)*(phi**2+pi/2)),
    ('320/57 = X17/3',    X17/3.0),
    ('57/pi^2',           57.0/pi**2),
    ('27/phi^3',          T_t/phi**3),
]
for name, g in probes3:
    print(f'  {name:62s} = {g:.6f}   vs g_p {g_p_ext:.6f}: {100*(g/g_p_ext-1):+.4f}%')
print('VERDICT: OPEN.  The alpha^4 m_e^2/m_p route reproduces the correct skeleton but lands')
print('5.583x short: the proton g-factor is not derivable from any locked piece (papers contain')
print('no g_p derivation; nearest probe 16pi/9 is -115 ppm off at g_p own precision).')

# ----------------------------------------------------------------------
# 4. CMB PEAK WAVELENGTH (Wien from T_CMB = 2.7255 K)
# ----------------------------------------------------------------------
print()
print('#4  THE CMB PEAK WAVELENGTH  (Wien, T_CMB = 2.7255 K)')
print('-'*78)
def wien_root_x():
    lo, hi = 1e-9, 20.0
    for _ in range(200):                       # bisection: exact root of x = 5(1 - e^-x)
        mid = 0.5*(lo+hi)
        if mid - 5.0*(1.0-math.exp(-mid)) > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)
x_wien  = wien_root_x()
b_wien  = h*c0/(x_wien*kB)
lam_max = b_wien/T_CMB
nu_Bnu  = 2.8214393721*kB*T_CMB/h    # B_nu peak constant (a mathematical root, not fitted)
print(f'x = {x_wien:.9f}  (exact root of x = 5(1-e^-x), the Planck B_lambda extremum; no free parameter)')
print(f'b = h c0/(x kB) = {b_wien:.9e} m K   (CODATA value 2.897771955e-3 m K)')
print(f'lambda_max = b / T_CMB = {lam_max*1e3:.4f} mm   vs observed CMB peak 1.063 mm')
print(f'      residual = {100*(lam_max*1e3/1.063-1):+.3f}%  (rounding of the quoted 1.063 mm)')
print(f'FIRAS T_CMB = 2.72548 +/- 0.00057 K -> lambda_max uncertainty = +/- {b_wien/T_CMB**2*0.00057*1e3:.4f} mm')
print(f'convention caution: B_nu peaks at {nu_Bnu/1e9:.1f} GHz (1.871 mm); B_lambda peaks at {lam_max*1e3:.3f} mm.')
print('VERDICT: CONSISTENT BY CONSTRUCTION.  Wien + locked T_CMB is an identity -- zero')
print('predictive content beyond T_CMB itself, so no kill condition can be armed.')

# ----------------------------------------------------------------------
# 5. LYMAN-ALPHA 121.567 nm
# ----------------------------------------------------------------------
print()
print('#5  LYMAN-ALPHA 121.567 nm  (the cage 13.606 eV route)')
print('-'*78)
E_H     = alpha**2*m_e*1e6/2.0          # Rydberg energy from locked alpha, m_e, c0
lam_lim = hc_eVnm/E_H
E_lya   = (3.0/4.0)*E_H/(1.0+me_mp)     # 1s -> 2p with reduced-mass correction (locked m_p)
lam_lya = hc_eVnm/E_lya
print(f'E_H = alpha^2 m_e c0^2 / 2 = {E_H:.6f} eV')
print(f'the task stated route: lambda = hc/13.606 eV = {lam_lim:.3f} nm')
print('  -> that is the LYMAN LIMIT (ionization edge), NOT Lyman-alpha. The route as stated')
print(f'     lands 25% short of 121.567 nm: residual {100*(lam_lim/121.567-1):+.1f}%.')
print('correct locked route (1s -> 2p, Bohr + reduced mass):')
print(f'  E = (3/4) E_H / (1 + m_e/m_p) = {E_lya:.6f} eV')
print(f'  lambda = hc/E = {lam_lya:.4f} nm   vs observed 121.567 nm (vacuum)')
print(f'  residual = {lam_lya-121.567:+.4f} nm = {1e6*(lam_lya/121.567-1):+.1f} ppm')
print('  the +11 ppm is the fine-structure doublet + Lamb-shift content of the 2p level --')
print('  none of it reachable from the locked set (pure Bohr value).')
print('VERDICT: the cage route PASSES at Bohr level (+11 ppm) with the (3/4) Balmer factor')
print('and the locked m_p reduced-mass correction; it is OPEN for the QED content.')
print('The task 13.606 eV -> 121.567 nm pairing is a conflation of the Lyman limit with')
print('Lyman-alpha: arithmetically DEAD as stated (91.127 nm, not 121.567 nm).')
# ----------------------------------------------------------------------
# THE TABLE
# ----------------------------------------------------------------------
print()
print('='*78)
print('SUMMARY TABLE')
print('='*78)
rows = [
 ('1. 502 nm frustration channel',
  'delta=(6phi^2-5pi)/(5pi)=1.5321e-5; lam=hc0/dU (dU=2.47 eV locked)',
  f'delta {delta:.4e}; lam {lam502:.2f} nm',
  '502.0 nm (paper claim); T CrB eruption pending',
  f'delta match at 4 s.f.; lam residual {100*(lam502/502.0-1):+.3f}%',
  'delta: phi, pi (locked). dU: locked D12. U=161.2 keV implied, unanchored (OPEN)',
  'KILL: no 502 nm excess during T CrB eruption (PREDICTIONS_2026-10-21 #1.4, frozen). Also: U has no locked provenance.'),
 ('2. 18.8 um proton line',
  'no locked route (paper pair round-trips at 2 s.f. only)',
  'OPEN (best flagged probe dU*T7b*3/2 = 0.06500 eV)',
  '0.0658 eV = 18.8 um (paper V2 target)',
  'no unlocked-free candidate within 0.5%',
  'paper: prediction-shaped, not claimed (D12/A6)',
  'KILL: n/a -- nothing armed (framework itself does not claim it). OPEN.'),
 ('3. 21 cm hydrogen line',
  '(4/3) alpha^4 m_e c0^2 (m_e/m_p) [Fermi skeleton]',
  f'{E_skel:.4e} eV (254.4 MHz)',
  f'{E_obs:.4e} eV (1420.40575 MHz)',
  f'MISS x{g_need:.4f}; needs g_p (unlocked). With external g_p: +{1e6*(E_fermi/E_obs-1):.0f} ppm',
  'alpha, m_e, m_p, c0, hbar locked; spin-sum 4/3 from the 1s contact term',
  'KILL: armed only if a locked derivation of g_p appears; papers have none -> OPEN. Nearest fold probe 16pi/9 = 5.58505 (-115 ppm).'),
 ('4. CMB peak wavelength',
  'lambda_max = h c0/(x kB T_CMB), x = root of x=5(1-e^-x)',
  f'{lam_max*1e3:.4f} mm',
  '1.063 mm (COBE/FIRAS)',
  f'{100*(lam_max*1e3/1.063-1):+.3f}% (rounding)',
  'hbar->h, c0, kB, T_CMB locked; x a mathematical root',
  'KILL: none possible -- identity with locked T_CMB, zero predictive content.'),
 ('5. Lyman-alpha 121.567 nm',
  '(3/4) alpha^2 m_e c0^2/2 / (1+m_e/m_p)',
  f'{lam_lya:.3f} nm',
  '121.567 nm (vacuum)',
  f'{lam_lya-121.567:+.3f} nm = +{1e6*(lam_lya/121.567-1):.0f} ppm',
  'alpha, m_e, m_p, c0 locked; 3/4 Balmer factor; reduced mass from locked m_p',
  'KILL: the task 13.606 eV -> 121.567 nm route is DEAD as stated (gives the Lyman limit 91.127 nm); corrected route passes at Bohr level, OPEN for fine structure + Lamb.'),
]
print(f"{'target':26s} | {'formula (locked route)':42s} | {'predicted':22s} | {'observed':22s} | residual")
print('-'*78)
for t, f, p, o, r, prov, kill in rows:
    print(f'{t:26s} | {f:42s} | {p:22s} | {o:22s} | {r}')
    print(f'{"":26s}   provenance: {prov}')
    print(f'{"":26s}   {kill}')
print('-'*78)

# ----------------------------------------------------------------------
# 5-LINE SUMMARY
# ----------------------------------------------------------------------
print()
print('5-LINE SUMMARY')
print('-'*78)
print('1. 502 nm: delta=(6phi^2-5pi)/5pi=1.5321e-5 VERIFIED; 2.47 eV = 501.96 nm (paper 502.0 is its own 3-s.f. rounding); U=161.22 keV is implied but nowhere locked -> provenance OPEN; T CrB kill armed.')
print('2. 18.8 um/0.0658 eV: OPEN -- papers call it prediction-shaped, not claimed; the pair round-trips only at 2 s.f. (+/-0.2%); no locked-only formula lands within 0.5%.')
print('3. 21 cm: the alpha^4 m_e^2/m_p skeleton lands 5.583x short (1.0521e-6 vs 5.8743e-6 eV): the missing factor is g_p, which no locked fold piece reproduces (best probe 16pi/9 = -115 ppm) -> OPEN.')
print('4. CMB peak: Wien from locked h, c0, kB, T_CMB gives 1.0632 mm vs 1.063 mm -- an identity with the locked temperature, zero predictive content, no kill condition possible.')
print('5. Lyman-alpha: the task 13.606 eV route is DEAD as stated (it gives the Lyman limit, 91.127 nm); the correct locked route (3/4)E_H/(1+m_e/m_p) gives 121.568 nm vs 121.567 nm (+11 ppm, Bohr-level PASS; QED content OPEN).')
print()
print('exit 0: all candidates reported, misses shown, no fitted parameters used.')
