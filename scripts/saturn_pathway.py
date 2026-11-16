import numpy as np
from scipy.integrate import solve_ivp

# --- CONSTANTS ---
C = 299792458.0
AU = 149597870697.0
GM_SUN = 1.32712440018e20
R_SUN = 6.957e8
OMEGA_SUN_SPIN = 2.8653e-6  # 25.38 days
A_ENTROPY = 8.9297e-10      # m/s^2

# PWC specific parameters
K_SUN = (2.0 * OMEGA_SUN_SPIN * R_SUN) / C
WELD_SQUARE = 1.0 / 361.0

# Shell Frequencies (Hz)
f_sun = (1.0/(2.0*np.pi)) * np.sqrt(GM_SUN / R_SUN**3)
f_sat = (1.0/(2.0*np.pi)) * np.sqrt(3.794e16 / (5.8232e7)**3)
f_jup = (1.0/(2.0*np.pi)) * np.sqrt(1.267e17 / (6.9911e7)**3)

def pwc_acceleration(t, state):
    """
    Computes the 3D acceleration for Jupiter and Saturn under PWC mechanics.
    State vector: [x_J, y_J, z_J, vx_J, vy_J, vz_J, x_S, y_S, z_S, vx_S, vy_S, vz_S]
    """
    r_J = state[0:3]
    v_J = state[3:6]
    r_S = state[6:9]
    v_S = state[9:12]
    
    dist_J = np.linalg.norm(r_J)
    dist_S = np.linalg.norm(r_S)
    
    # Unit vectors
    r_hat_S = r_S / dist_S
    h_vec_S = np.cross(r_S, v_S)
    theta_hat_S = np.cross(h_vec_S, r_S)
    theta_hat_S /= np.linalg.norm(theta_hat_S)
    
    # 1. Standard Newtonian Base (Sun point mass)
    a_newt_S = - (GM_SUN / dist_S**2) * r_hat_S
    
    # 2. PWC Radial (Tautness Area Drop + Entropic Floor)
    term_taut_S = (GM_SUN / (C**2 * R_SUN)) * (f_sat / f_sun) * (R_SUN / dist_S)**2
    term_ent_S = A_ENTROPY * (1.0 + (2.0 * GM_SUN) / (C**2 * dist_S))
    a_rad_S = - ((GM_SUN / dist_S**2) * term_taut_S + term_ent_S) * r_hat_S
    
    # 3. PWC Transverse (Rotational Spiral Shear)
    a_trans_S = - ((GM_SUN / dist_S**2) * K_SUN * (f_sat / f_sun)) * theta_hat_S
    
    # 4. PWC Synodic Bridge (Jupiter stealing from Saturn)
    r_JS = r_J - r_S
    dist_JS = np.linalg.norm(r_JS)
    bridge_mag = WELD_SQUARE * (np.sqrt(1.267e17 * A_ENTROPY) / dist_JS) * (5.8232e7 / (dist_S * np.sqrt(3.794e16/GM_SUN)))
    a_bridge_S = bridge_mag * (r_JS / dist_JS)
    
    # Total PWC Acceleration on Saturn
    a_tot_S = a_newt_S + a_rad_S + a_trans_S + a_bridge_S
    
    # (Simplified Jupiter acceleration - base Keplerian for driving the bridge)
    a_newt_J = - (GM_SUN / dist_J**2) * (r_J / dist_J)
    
    return np.concatenate([v_J, a_newt_J, v_S, a_tot_S])

# --- INITIALIZATION (Locking t_0) ---
# Example: Epoch Sept 2004 (Use JPL Horizons exact vectors here for actual run)
# Values below are arbitrary placeholders for structure
state_0 = np.array([
    # Jupiter [x,y,z, vx,vy,vz]
    5.2*AU, 0, 0, 0, 13000, 0,
    # Saturn [x,y,z, vx,vy,vz]
    9.5*AU, 0, 0, 0, 9600, 0
])

print("Integrating PWC exact vector law (No parameter fitting)...")
sol = solve_ivp(pwc_acceleration, [0, 6.5 * 365.25 * 86400], state_0, method='RK45', t_eval=np.linspace(0, 6.5 * 365.25 * 86400, 1000))

print("Integration complete. PWC orbital path generated.")