"""
t27_cubic_tempo_closed.py - 3D Cubic Relief Tightening T = 3^3 = 27 (2026-10-20)
Derives T = 27 from the 3-per-proton heat reach compounded across 3 spatial axes
and verifies s*(1 + T) = 28/19 against the Planck LSS acoustic tempo (380/258 kyr).
"""
s = 1.0 / 19.0
reach_factor = 3          # V_reach = 3 * m_p / rho0 (from u_h = rho0 * c0^2 / 3)
dims = 3                  # 3 orthogonal spatial axes of boundary convergence
T_cubic = reach_factor ** dims  # 3^3 = 27

tempo_ratio_pwc = s * (1.0 + T_cubic)      # 28 / 19 = 1.4736842
t_age_kyr = 380.0
t_lss_obs_kyr = 258.0
tempo_ratio_obs = t_age_kyr / t_lss_obs_kyr # 1.4728682
t_lss_pwc_kyr = t_age_kyr / tempo_ratio_pwc

print("=" * 74)
print("T = 3^3 = 27 CUBIC TIGHTENING & PLANCK LSS TEMPO CLOSURE")
print("=" * 74)
print(f"Per-proton heat reach factor : {reach_factor}  (V_reach = 3 m_p / rho0)")
print(f"3D cubic boundary tightening : T = {reach_factor}^{dims} = {T_cubic}")
print(f"PWC speed-up multiplier      : s*(1 + T) = 28/19 = {tempo_ratio_pwc:.6f}")
print(f"Planck LSS tempo ratio       : 380 / 258 kyr     = {tempo_ratio_obs:.6f}")
print(f"Predicted LSS tempo          : {t_lss_pwc_kyr:.3f} kyr vs 258.0 kyr ({100*(tempo_ratio_pwc/tempo_ratio_obs - 1):+.4f}%)")
print("=" * 74)
