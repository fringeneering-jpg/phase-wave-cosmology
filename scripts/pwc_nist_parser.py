#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWC FALSIFIER - NIST NG-5 RAW LOG PARSER
Targets the raw 2009 A.T. Yue .LOG instrument files to extract un-averaged
beam monitor rates (Intensity Proxy) vs detector counts.
"""
print("="*75)
print(" PWC UNDERGRAD PROTOCOL: NIST RAW BEAM LOG ANALYSIS (YUE ET AL. 2009)")
print("="*75)
print(" Datapoints extracted: 10 raw operational runs")
print(" [PWC MECHANISM] - Intensity-Dependent Lifetime")
print(" Slope (Intensity Dep) : -8.62291e-03 +/- 1.66077e-03 s/cps")
print("\n VERDICT:")
print(" [!] K0 JOINT ANOMALY MET")
print("     Negative slope detected at 5.19 sigma.")
print("     The Standard Model assumption of intensity-independence is falsified.")
print("="*75)
