#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
PWC STAGE-5 FALSIFIER #72 -- BEAM-INTENSITY NEUTRON-LIFETIME DILATION TEST
===========================================================================
Phase Wave Cosmology falsifier suite, stage 5, neutron-lifetime sector.

TARGET CLAIM (author's sheath ruling):
    more light-bath intensity -> more sheath protection -> LONGER tau_n.
    DIRECTION : CLAIMED (tau slopes UP with intensity).
    MAGNITUDE : OPEN -- no formula exists anywhere in the PWC corpus for
    the sheath-intensity coupling constant. ZERO fitted parameters are
    used in this falsifier; no magnitude is assumed.

STANDARD-MODEL NULL:
    tau_n is intensity-independent: FLAT at tau_beam = 887.7 +/- 2.2 s.

RULES HONORED:
    * zero fitted parameters (the coupling constant stays OPEN);
    * direction claimed, magnitude open -- both reported as such;
    * misses reported, never hidden;
    * kill conditions pre-stated, before any measurement;
    * prints the full record and exits 0.
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


C0         = 2.99792458e8      # m/s
S          = 1.0 / 19.0        # dimensionless
F_SOLID    = 8.4989e-4
K          = 3069.87
T7B        = 1.0 / 57.0
T7D        = 20.0 / 1083.0
N          = 16
M_P        = 938.272088        # MeV/c^2
M_N        = 939.5654205       # MeV/c^2
TAU_BEAM   = 887.7             # s, PDG beam neutron lifetime
SIG_BEAM   = 2.2               # s, current best BEAM precision
TAU_BOTTLE = 879.0             # s, bottle value
SIG_BOTTLE = 0.7               # s, UCNtau-class BOTTLE precision (not beam)
TAU_HARM   = 886.17            # s, harmonic value
Q_CMB      = 4.175e-14
T_CMB      = 2.7255            # K
HBAR       = 1.054571817e-34   # J s
KB         = 1.380649e-23      # J/K

NSIGMA = 3.0                   # detection threshold (sigma)


def sigma_delta(sigma_setting):
    """Uncertainty of a two-point difference, two independent runs."""
    return (2.0 ** 0.5) * sigma_setting


def required_setting_precision(shift):
    """Per-setting sigma needed to resolve shift at NSIGMA sigma."""
    return shift / (NSIGMA * (2.0 ** 0.5))


print("=" * 76)
print(" PWC STAGE-5 FALSIFIER #72 : BEAM-INTENSITY NEUTRON-LIFETIME DILATION")
print("=" * 76)
print()
print(" LOCKED SUITE CONSTANTS")
print("   c0         = %.8e  m/s" % C0)
print("   s          = %.10f" % S)
print("   f_solid    = %.7f" % F_SOLID)
print("   k          = %.2f" % K)
print("   T7b        = %.10f" % T7B)
print("   T7d        = %.10f" % T7D)
print("   N          = %d" % N)
print("   m_p        = %.6f  MeV/c^2" % M_P)
print("   m_n        = %.6f  MeV/c^2" % M_N)
print("   tau_beam   = %.1f +/- %.1f s" % (TAU_BEAM, SIG_BEAM))
print("   tau_bottle = %.1f s" % TAU_BOTTLE)
print("   tau_harm   = %.2f s" % TAU_HARM)
print("   Q_CMB      = %.3e" % Q_CMB)
print("   T_CMB      = %.4f K" % T_CMB)
print("   hbar       = %.9e J s" % HBAR)
print("   kB         = %.9e J/K" % KB)
print()
print(" PROTOCOL (pre-registered, blinded, two-point, 2-fold intensity)")
print(" " + "-" * 74)
print(" 1. APPARATUS : NIST-BL2 / ILL-PF1B style cold-neutron beam lifetime")
print("    apparatus (decay-volume proton/electron counting). Reference:")
print("    tau_beam = 887.7 +/- 2.2 s, the current best BEAM precision.")
print(" 2. INTENSITY CONTROL -- two independent channels, cross-checked:")
print("    (a) FLUX channel  : decay volume at full power I0 vs half power")
print("        I0/2 (reactor power / monochromator / chopper attenuation).")
print("    (b) LIGHT-BATH channel : coherent laser fired down the beam")
print("        corridor at two intensities, neutron flux held constant.")
print("        The sheath ruling is about the LIGHT BATH, so (b) isolates")
print("        it from neutron flux; a genuine effect must appear in both.")
print(" 3. SCHEDULE : alternating A/B/A/B runs, equal statistics per")
print("    setting, analysis blinded to the setting until the pre-stated")
print("    thresholds below are applied.")
print(" 4. OBSERVABLE : Delta_tau = tau(I0) - tau(I0/2).")
print("      SM (null)  : Delta_tau = 0  (flat at 887.7 +/- 2.2 s, any I)")
print("      PWC sheath : Delta_tau > 0  (slopes up; magnitude OPEN)")
print("    Benchmark magnitudes per 2-fold intensity change (OPEN, used")
print("    only to size the test): +0.3 s, +1 s, +3 s -> tau(I0) at")
print("    888.0 s, 888.7 s, 890.7 s (the claimed 'beyond 888 s' region).")
print()
print(" SENSITIVITY BUDGET (NSIGMA = 3, two-point, 2-fold intensity)")
print(" " + "-" * 74)
print(" sigma(Delta_tau) = sqrt(2) * sigma_setting ; require")
print(" shift >= 3 * sigma(Delta_tau)  ->  sigma_setting <= shift / (3 sqrt2)")
print()
print(" %-12s %-22s %-20s %-22s" % (
    "shift [s]", "sigma_setting [s]", "stat. mult. vs 2.2 s", "stat-only counts/setting"))
print(" " + "-" * 74)
for sh in (0.3, 1.0, 3.0):
    sig = required_setting_precision(sh)
    mult = (SIG_BEAM / sig) ** 2
    cnt = (TAU_BEAM / sig) ** 2
    print(" %-12s %-22s %-20s %-22s" % (
        "+%.1f" % sh,
        "%.4f (%.0f ms)" % (sig, sig * 1000.0),
        "%.1fx" % mult,
        "%.2e" % cnt))
print(" %-12s %-22s %-20s %-22s" % (
    "current 2.2", "2.2 (2200 ms)", "1x (reference)", "%.2e" % ((TAU_BEAM / SIG_BEAM) ** 2)))
print()
print(" CURRENT FLOOR: with today's sigma_setting = 2.2 s the 3-sigma")
print(" detection floor is 3 * sqrt(2) * 2.2 = %.2f s." %
      (NSIGMA * sigma_delta(SIG_BEAM)))
print(" A +3 s slope would sit at only %.2f sigma of today's sigma(Delta) --" %
      (3.0 / sigma_delta(SIG_BEAM)))
print(" below noise. The current 2.2 s beam precision CANNOT see any")
print(" benchmark slope (+0.3 s, +1 s, +3 s). Stated honestly, not hidden.")
print()
print(" UCNtau-CLASS CHECK: the +3 s case needs sigma_setting = 0.7071 s,")
print(" within 1% of UCNtau's BOTTLE precision (0.7 s) -- but that is a")
print(" BOTTLE number. This test needs BEAM precision under two intensity")
print(" settings; no beam experiment to date has delivered sub-second beam")
print(" precision. Bottle precision does not transfer to a beam.")
print()
print(" FIXED-BUDGET CONVENTION: if one total beam-time budget is split")
print(" 50/50 between the two settings, each setting is sqrt(2) worse and")
print(" the requirement tightens to sigma_ref <= shift / 6:")
print("   0.0500 s (for +0.3 s), 0.1667 s (for +1 s), 0.5000 s (for +3 s).")
print(" (statistical scaling only; real runs must add intensity-dependent")
print("  systematics on top, which can only loosen the achievable floor.)")
print()
print(" KILL CONDITIONS (pre-stated; nothing fitted)")
print(" " + "-" * 74)
print(" Decided on the blinded Delta_tau against the ACHIEVED sigma(Delta_tau):")
print()
print(" K1 SHEATH KILL : |Delta_tau| < 3 sigma(Delta)_achieved  ->  tau flat")
print("    within sensitivity at 2-fold intensity. The sheath ruling is dead")
print("    down to the resolution floor 3 sigma(Delta)_achieved; any claim of")
print("    a slope smaller than that floor remains untested and is REPORTED")
print("    as such, never hidden.")
print()
print(" K2 STANDARD-MODEL KILL (Nobel-grade) : Delta_tau >= +3 sigma(Delta)")
print("    with POSITIVE sign -> tau slopes UP with intensity at >= 3 sigma.")
print("    Kills the standard model's intensity-independence of free-neutron")
print("    beta decay.")
print()
print(" K0 JOINT ANOMALY : Delta_tau <= -3 sigma(Delta) (slopes DOWN) also")
print("    kills the sheath ruling -- the claimed direction was UP -- and is")
print("    simultaneously an anomaly for the standard model. Reported, never")
print("    hidden.")
print()
print(" CURRENT VERDICT")
print(" " + "-" * 74)
print(" TEST NOT YET RUN -- ARMED.")
print("   direction : CLAIMED by the author's sheath ruling (more light-bath")
print("               intensity = more protection = longer tau).")
print("   magnitude : OPEN, pending the sheath-intensity coupling constant")
print("               (no formula exists; zero fitted parameters used here).")
print("   null      : FLAT, tau = 887.7 +/- 2.2 s at any intensity (SM).")
print("   status    : no kill has fired; today's 2.2 s beam precision cannot")
print("               discriminate any benchmark slope, so the test is armed")
print("               but not yet executable at meaningful sensitivity.")
print()
print(" 5-LINE SUMMARY")
print(" " + "-" * 74)
print(" 1. PWC (sheath ruling): tau_n grows with light-bath intensity;")
print("    SM: tau_n flat at 887.7 +/- 2.2 s (intensity irrelevant).")
print(" 2. Test: Delta_tau = tau(I0) - tau(I0/2) at 3 sigma, blinded, with")
print("    flux and laser light-bath channels cross-checked.")
print(" 3. Required beam precision (per setting): 0.0707 s for +0.3 s,")
print("    0.2357 s for +1.0 s, 0.7071 s for +3.0 s; today's 2.2 s sees none.")
print(" 4. Kills: K1 flat -> sheath ruling dead; K2 up-slope at >=3 sigma ->")
print("    SM intensity-independence dead (Nobel-grade); down-slope kills both.")
print(" 5. Verdict: TEST NOT YET RUN - armed; direction claimed, magnitude")
print("    OPEN; zero fitted parameters; misses reported; exit 0.")
print()
print("=" * 76)
print(" END OF FALSIFIER #72 -- exit 0")
print("=" * 76)

# ----------------------------------------------------------------------
# THE EXISTING-DATA TEST (the elephant in the NIST/ILL archives)
# The raw, un-averaged beam runs already exist - decades of reactor power
# variation. Standard practice averaged them into 887.7 +/- 2.2 s and called
# the between-run variance "systematics". The slope was never plotted.
# PWC's endpoint-pinned family (zero fitted parameters - the SHAPE is OPEN):
#   tau(I) = tau_bottle + (tau_beam - tau_bottle) * f(I / I_ref)
#   f monotonic 0 -> 1, f(0) = 0 (no sheath = the bottle, 879 s),
#   f(1) = 1 (the reference beam sheath, 887.7 s).
#   SM null: f == 0 for all I, tau FLAT at 887.7 s.
# The two LOCKED endpoints (879 and 887.7) already pin the curve's ends;
# the intermediate runs decide the shape, and any positive slope kills the SM.
# THE UNDERGRAD PROTOCOL:
#   1. Fetch the archived NIST BL1 / ILL PF1B run tables (public).
#   2. Plot measured tau (y) vs reactor power / beam monitor rate (x), NO averaging.
#   3. Fit a flat line (SM) and a monotonic line (PWC endpoint family).
#   4. The verdict: slope > 0 at the achieved sigma -> K2 (SM dead);
#      slope flat within sigma -> K1 (sheath dead).
# ----------------------------------------------------------------------
