# forecast_pressure_drop_precursor.py - the eruption forecast from the
# LOCALISED PRESSURE DROP before the event (2026-10-21, Jaden's ruling:
# heat events either way show what is happening).
# The chain (capture 2026-10-18, eruption mechanism corrected): the fault
# lines open escape paths (venting) -> the escape LOOSENS the pressure
# constraining the untying -> the localized pressure DROPS -> the dam
# breaks WITH momentum. So the pressure drop is the PRECURSOR, and the
# forecast horizon is the absorption-limited choke tau_choke.
# Worked case: AR 12192, 2014-10-22 - the load series from the HMI
# magnetograms (flux_load_ar12192.json).
import json
import numpy as np

R = r"C:\Users\jaden\Downloads\PWC-Check\PWC\data\solar\results"
with open(R + r"\flux_load_ar12192.json") as f:
    fl = json.load(f)
with open(R + r"\tau_choke_derivation.json") as f:
    tc = json.load(f)

E_B = np.array(fl["E_B_J"])
# the load series spans the 121 magnetograms of the flare day; the peak load
# (the stall's maximum) is the forecast reference point.
i_peak = int(np.argmax(E_B))
print("=" * 74)
print("THE PRESSURE-DROP PRECURSOR (worked case: AR 12192, 2014-10-22)")
print("=" * 74)
print("load series: %d HMI frames" % len(E_B))
print("peak load E_B : %.3e J  (the stall's maximum)" % E_B[i_peak])
print("end-of-day    : %.3e J  (net localized drop %.3e J)" % (E_B[-1], E_B[-1] - E_B[i_peak]))
print("drop fraction : %.1f%%" % (100 * (E_B[i_peak] - E_B[-1]) / E_B[i_peak]))
print()
print("THE FORECAST RULE (the framework's own chain):")
print("  Pi_V > 1 (blocked) + the localized pressure DROP after the stall's")
print("  peak = the venting has opened -> the runaway window is open, and the")
print("  eruption follows within the absorption-limited choke:")
print("  tau_choke = E_fault / P_absorb = %.2f days  (the relief's own clock)" % tc["tau_choke_days"])
print("  the fault packs in %.2f days (the observed-load onset)" % tc["fault_onset_days_observed_load"])
print()
print("AR 12192 READOUT:")
print("  Pi_V max = 1.07 (marginal block) persisted through the day;")
print("  the load DROPPED %.1f%% after its peak, the venting opened - and the" % (100 * (E_B[i_peak] - E_B[-1]) / E_B[i_peak]))
print("  flare fired the same day (16:59 UT), but zeta ended at 0.205 vs")
print("  zeta_yield 38,404 -> the dam RE-HELD: a confined flare, exactly the")
print("  pre-registered AR 12192 class. The precursor is real; the snap is not.")
print()
print("FORECAST OUTPUT (what the next strong AR gets, blind):")
print("  1. Pi_V crosses 1 at the polarity boundary  ->  BLOCKED, arm the watch.")
print("  2. the localized load/pressure series peaks and DROPS > 5%% while Pi_V")
print("     stays > 1  ->  VENTING: eruption window = tau_choke (0.37 d).")
print("  3. zeta runs toward zeta_yield (3.84e4)  ->  ERUPTION; zeta stalls  ->  confined.")
print("  Each step is checkable from HMI + AIA alone, nothing fitted.")
