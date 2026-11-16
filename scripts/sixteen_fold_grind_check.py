"""
sixteen_fold_grind_check.py
Connects the Oct 1 shed Max-P shell thickness (~43.84 km = 156.3 - 112.46 km)
to the Oct 12 sixteen-fold clock (c0 * tau / 16 = 87.689 km = 2 * 43.845 km,
L = 2 * sqrt(2) * dt_shed = 124.01 km).
"""
import math

c0 = 299792.458       # km/s
tau_obs = 0.00468     # s (GW150914 settling time = 4.68 ms)
N_folds = 16          # 4pi / (pi/4) = 16 harmonic stages

# GW150914 shell thicknesses (DERIVATIONS.md / PWC_MASTER_FRAMEWORK)
t1_sep = 82.9         # km (36 Msun separate Max-P shell: 121.6 - 38.7 km)
t2_sep = 73.4         # km (29 Msun separate Max-P shell: 109.2 - 35.8 km)
t_sep_sum = t1_sep + t2_sep  # 156.3 km

# Merged shell thickness: 159.6 - 47.0 = 112.6 km (k-rule core) or 159.6 - 47.3 = 112.3 km (shell doc)
t_merged_k = 112.6
t_merged_shell = 112.3
t_merged_mid = 0.5 * (t_merged_k + t_merged_shell)  # 112.45 km

dt_shed_k = t_sep_sum - t_merged_k         # 43.70 km
dt_shed_shell = t_sep_sum - t_merged_shell # 44.00 km
dt_shed_mid = t_sep_sum - t_merged_mid     # 43.85 km

# Per-stage travel distance (2 shells = round-trip across shed layer per stage)
d_stage = 2.0 * dt_shed_mid                # 87.70 km
L_45_chord = math.sqrt(2.0) * d_stage      # 124.03 km (the 124 km in sixteen_fold_clock.md!)
tau_pred = (N_folds * d_stage) / c0        # s

print("=" * 76)
print("D13 SIXTEEN-FOLD CLOCK: CORE-GRINDING SHED SHELL CONNECTION")
print("=" * 76)
print(f"Separate Max-P shells (t1 + t2)   : {t1_sep:.1f} + {t2_sep:.1f} = {t_sep_sum:.1f} km")
print(f"Merged Max-P shell (k / shell)    : {t_merged_k:.1f} km / {t_merged_shell:.1f} km (mid: {t_merged_mid:.2f} km)")
print(f"Shed Max-P thickness (dt_shed)    : {dt_shed_k:.2f} to {dt_shed_shell:.2f} km (mid: {dt_shed_mid:.2f} km)")
print(f"Single-pass time (dt_shed / c0)   : {1000.0 * dt_shed_mid / c0:.4f} ms (~0.15 ms)")
print(f"Two-shell pass per stage (2*dt)   : {d_stage:.4f} km vs c0*tau/16 = {c0*tau_obs/16.0:.4f} km")
print(f"45-deg crease chord L = 2*sqrt2*dt: {L_45_chord:.2f} km vs L = 124.00 km (+0.02%)")
print(f"16-stage total path (32 * dt_shed): {N_folds * d_stage:.2f} km vs c0*tau = {c0*tau_obs:.2f} km")
print(f"Predicted settling time (32*dt/c0): {1000.0 * tau_pred:.4f} ms vs {1000.0 * tau_obs:.2f} ms ({100*(tau_pred/tau_obs - 1):+.3f}%)")
print("=" * 76)
