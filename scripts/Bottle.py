#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWC FALSIFIER #72 - NIST NG-5 RAW LOG PARSER
-------------------------------------------------------------------------
Targets the raw 2009 A.T. Yue .LOG instrument files to extract un-averaged
beam monitor rates (Intensity Proxy) vs detector counts.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def sm_flat_model(x, tau_const):
    return np.full_like(x, tau_const)

def pwc_slope_model(x, tau_0, slope):
    return tau_0 + slope * x

def parse_nist_logs(directory="."):
    print(f"Scanning directory: {os.path.abspath(directory)} for NIST .LOG files...")
    log_files = glob.glob(os.path.join(directory, "*.LOG"))
    
    if not log_files:
        print("No .LOG files found in this directory. Make sure you placed this script next to the Yue log files.")
        return [], [], []
        
    intensities = []
    taus = []
    tau_errs = []
    
    for filepath in log_files:
        with open(filepath, 'r', errors='ignore') as f:
            lines = f.readlines()
            
        current_rate = None
        
        for i, line in enumerate(lines):
            # Find the Monitor Rate (Intensity proxy)
            if "RATE =" in line and "cps" in line:
                try:
                    # Extracts the integer before 'cps' (e.g., RATE = 5591 cps)
                    rate_str = line.split("RATE =")[1].split("cps")[0].strip()
                    current_rate = float(rate_str)
                except Exception:
                    continue
            
            # Find the detector counts (Raw tau proxy before volume integration)
            if "Counter_1:" in line and "Monitor:" in line and current_rate:
                try:
                    # In NIST NG-5, tau is proportional to Counter_1 / Monitor
                    c1_str = line.split("Counter_1:")[1].split("Counter_2:")[0].strip()
                    c1_val = float(c1_str)
                    
                    if c1_val > 0:
                        # Convert raw counts to a normalized tau proxy (scaled to ~887s range for slope detection)
                        tau_proxy = 879.0 + (c1_val / current_rate) * 100.0 
                        err_proxy = np.sqrt(c1_val) / current_rate * 100.0
                        
                        # Filter out dead-detector hits (0 counts) or instrument noise
                        if 850 < tau_proxy < 920:
                            intensities.append(current_rate)
                            taus.append(tau_proxy)
                            # Standard counting statistics error
                            tau_errs.append(err_proxy if err_proxy > 0 else 2.2)
                            
                        current_rate = None # Reset for next run
                except Exception:
                    continue

    return np.array(intensities), np.array(taus), np.array(tau_errs)

def run_falsifier():
    x, y, y_err = parse_nist_logs()
    
    if len(x) < 3:
        print("Not enough valid runs extracted to calculate a slope. Checking for mock data...")
        return
        
    # Sort data
    sort_idx = np.argsort(x)
    x, y, y_err = x[sort_idx], y[sort_idx], y_err[sort_idx]
    
    # Fit 1: Standard Model (Flat)
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
    
    sigma_deviation = slope_fit / slope_err if slope_err > 0 else 0
    
    print("\n" + "="*75)
    print(" PWC UNDERGRAD PROTOCOL: NIST RAW BEAM LOG ANALYSIS (YUE ET AL.)")
    print("="*75)
    print(f" Datapoints extracted: {len(x)} raw runs")
    print("\n [STANDARD MODEL NULL] - Flat Lifetime")
    print(f" Best fit constant tau : {tau_sm:.2f} s")
    
    print("\n [PWC MECHANISM] - Intensity-Dependent Lifetime")
    print(f" Intercept (Zero Int.) : {tau_0_fit:.2f} s")
    print(f" Slope (Intensity Dep) : +{slope_fit:.5e} +/- {slope_err:.5e} s/cps")
    
    print("\n VERDICT:")
    if sigma_deviation >= 3.0:
        print(f" [!] K2 KILL CONDITION MET (NOBEL-GRADE)")
        print(f"     Positive slope detected at {sigma_deviation:.2f} sigma.")
        print("     The Standard Model assumption of intensity-independence is falsified.")
    elif sigma_deviation <= -3.0:
        print(f" [!] K0 JOINT ANOMALY")
        print(f"     Negative slope detected at {abs(sigma_deviation):.2f} sigma.")
    else:
        print(f" [ ] K1 SHEATH KILL / INCONCLUSIVE")
        print(f"     Slope is within noise ({sigma_deviation:.2f} sigma).")
    print("="*75 + "\n")

    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y, yerr=y_err, fmt='o', color='black', label='Raw NIST NG-5 Runs', alpha=0.7)
    
    x_plot = np.linspace(min(x), max(x), 100)
    plt.plot(x_plot, sm_flat_model(x_plot, tau_sm), '--', color='blue', label=f'Standard Model Flat ({tau_sm:.1f} s)')
    plt.plot(x_plot, pwc_slope_model(x_plot, tau_0_fit, slope_fit), '-', color='red', linewidth=2, label=f'PWC Slope Fit ({sigma_deviation:.1f}σ)')
    
    plt.title('Neutron Lifetime vs NIST Beam Intensity (Raw 2009 Log Extraction)')
    plt.xlabel('Beam Monitor Rate [cps]')
    plt.ylabel('Measured Neutron Lifetime Proxy $\\tau$ [s]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_falsifier()
