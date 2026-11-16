#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWC FALSIFIER #72 - DATA EXTRACTION & ANALYSIS ("THE UNDERGRAD PROTOCOL")
-------------------------------------------------------------------------
Analyzes raw, un-averaged neutron lifetime run data (beam or bottle) 
against intensity/power parameters.

Standard Model Null: tau(I) is perfectly flat.
PWC Sheath Ruling: tau(I) slopes upward with intensity.

Usage: 
  python pwc_undergrad_protocol.py [path_to_data.json]
"""

import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -------------------------------------------------------------------
# 1. MODEL DEFINITIONS
# -------------------------------------------------------------------

def sm_flat_model(x, tau_const):
    """Standard Model: Lifetime is absolutely flat regardless of intensity."""
    return np.full_like(x, tau_const)

def pwc_slope_model(x, tau_0, slope):
    """PWC: Lifetime shifts upward with intensity (un-corrected systematics)."""
    return tau_0 + slope * x

# -------------------------------------------------------------------
# 2. DATA PARSING
# -------------------------------------------------------------------

def load_and_parse_json(filepath):
    """
    Update the dictionary keys here to match the exact schema of the 
    archival JSON you are targeting.
    """
    print(f"Loading archival run data from: {filepath}")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    intensities = []
    taus = []
    tau_errs = []
    
    # Adjust these keys based on the actual JSON structure
    for run in data.get('runs', []):
        try:
            # Look for the raw intensity proxy (reactor power, monitor counts, beam flux)
            i_val = float(run['intensity_proxy'])
            # Look for the raw measured lifetime before algorithmic averaging
            t_val = float(run['raw_tau_measured'])
            t_err = float(run['tau_uncertainty'])
            
            intensities.append(i_val)
            taus.append(t_val)
            tau_errs.append(t_err)
        except KeyError as e:
            continue
            
    return np.array(intensities), np.array(taus), np.array(tau_errs)

# -------------------------------------------------------------------
# 3. STATISTICAL FIT & VERDICT
# -------------------------------------------------------------------

def analyze_and_plot(x, y, y_err):
    # Sort data for clean plotting
    sort_idx = np.argsort(x)
    x, y, y_err = x[sort_idx], y[sort_idx], y_err[sort_idx]
    
    # Fit 1: Standard Model (Flat)
    # Weighted average using inverse variance
    w = 1.0 / (y_err ** 2)
    tau_sm = np.sum(w * y) / np.sum(w)
    sm_chi2 = np.sum(((y - tau_sm) / y_err) ** 2)
    sm_dof = len(x) - 1
    
    # Fit 2: PWC (Slope)
    popt_pwc, pcov_pwc = curve_fit(pwc_slope_model, x, y, sigma=y_err, absolute_sigma=True)
    tau_0_fit, slope_fit = popt_pwc
    slope_err = np.sqrt(pcov_pwc[1, 1])
    pwc_chi2 = np.sum(((y - pwc_slope_model(x, tau_0_fit, slope_fit)) / y_err) ** 2)
    pwc_dof = len(x) - 2
    
    # Verdict Calculation
    sigma_deviation = slope_fit / slope_err if slope_err > 0 else 0
    
    print("\n" + "="*70)
    print(" PWC UNDERGRAD PROTOCOL: RAW DATA ANALYSIS")
    print("="*70)
    print(f" Datapoints analyzed: {len(x)} raw runs")
    print("\n [STANDARD MODEL NULL] - Flat Lifetime")
    print(f" Best fit constant tau : {tau_sm:.2f} s")
    print(f" Chi-squared / dof     : {sm_chi2:.2f} / {sm_dof}")
    
    print("\n [PWC MECHANISM] - Intensity-Dependent Lifetime")
    print(f" Intercept (Zero Int.) : {tau_0_fit:.2f} s")
    print(f" Slope (Intensity Dep) : +{slope_fit:.5e} +/- {slope_err:.5e} s/unit")
    print(f" Chi-squared / dof     : {pwc_chi2:.2f} / {pwc_dof}")
    
    print("\n VERDICT:")
    if sigma_deviation >= 3.0:
        print(f" [!] K2 KILL CONDITION MET (NOBEL-GRADE)")
        print(f"     Positive slope detected at {sigma_deviation:.2f} sigma.")
        print("     The Standard Model assumption of intensity-independence is falsified.")
    elif sigma_deviation <= -3.0:
        print(f" [!] K0 JOINT ANOMALY")
        print(f"     Negative slope detected at {abs(sigma_deviation):.2f} sigma.")
        print("     SM falsified, but PWC sheath direction reversed. Review theory.")
    else:
        print(f" [ ] K1 SHEATH KILL / INCONCLUSIVE")
        print(f"     Slope is within noise ({sigma_deviation:.2f} sigma).")
        print("     Sheath effect dead down to current statistical floor.")
    print("="*70 + "\n")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y, yerr=y_err, fmt='o', color='black', label='Raw Run Data ("Systematics")', alpha=0.7)
    
    x_plot = np.linspace(min(x), max(x), 100)
    plt.plot(x_plot, sm_flat_model(x_plot, tau_sm), '--', color='blue', label=f'Standard Model Flat ({tau_sm:.1f} s)')
    plt.plot(x_plot, pwc_slope_model(x_plot, tau_0_fit, slope_fit), '-', color='red', linewidth=2, label=f'PWC Slope Fit ({sigma_deviation:.1f}σ significance)')
    
    plt.title('Neutron Lifetime vs Beam/Trap Intensity (Raw Archival Data)')
    plt.xlabel('Intensity Proxy (Reactor Power / Trap Fill Count)')
    plt.ylabel('Measured Neutron Lifetime $\\tau$ [s]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# 4. TEST DATA GENERATOR (For dry runs)
# -------------------------------------------------------------------
def generate_mock_json():
    """Generates a test JSON simulating the 'hidden' slope in archival data."""
    np.random.seed(42)
    intensities = np.linspace(10, 100, 30)
    # Simulate an actual 4-second shift hidden in the noise across the power range
    true_tau = 880 + (4.0 * (intensities / 100)) 
    errors = np.random.uniform(1.5, 3.5, size=30)
    measured_taus = np.random.normal(true_tau, errors)
    
    data = {"runs": []}
    for i, t, e in zip(intensities, measured_taus, errors):
        data["runs"].append({
            "run_id": f"run_{int(i*1000)}",
            "intensity_proxy": round(i, 2),
            "raw_tau_measured": round(t, 2),
            "tau_uncertainty": round(e, 2)
        })
    
    test_file = "test_archival_data.json"
    with open(test_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated mock archival data: {test_file}")
    return test_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        print("No JSON file provided. Running mock data generator to demonstrate protocol.")
        filepath = generate_mock_json()
        
    x, y, y_err = load_and_parse_json(filepath)
    if len(x) < 3:
        print("Error: Not enough valid data points found in JSON. Check your dictionary keys in 'load_and_parse_json()'.")
    else:
        analyze_and_plot(x, y, y_err)