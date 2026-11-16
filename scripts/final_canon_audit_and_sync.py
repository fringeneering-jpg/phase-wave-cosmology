"""
final_canon_audit_and_sync.py
1. Wires Leg 4 (Submarine Hull clock rate vs Exposed Neutron Thread drag clock) into S13 / IV.4.
2. Wires the '-2 fits: why GR and MOND owe the rotation data two parameters' callout into III.1 / Section 1.
3. Replaces any 'time dilation' wording with 'clock rate'.
4. Prints the final Honest Open Items list from PHASE_WAVE_COSMOLOGY_DERIVATIONS.md.
"""
from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

minus_two_callout = """**The −2 fits: why GR and MOND owe the rotation data two parameters.** For decades, both standard dark-matter halo models (GR) and empirical modified-gravity baselines (MOND / McGaugh's RAR) have quietly started their galaxy rotation fits with two built-in empirical knobs already turned: the assumed 3.6 μm stellar mass-to-light ratios Υ_disk = 0.50 and Υ_bulge = 0.70. Calling two hand-tuned constants "stellar-population priors" does not make them zero-parameter physics; they are two global fits baked into the baryonic data before the gravitational law is ever tested. Phase Wave Cosmology removes both fits from first principles: the extra weight in the disk and bulge is the 10-Gyr accumulated exhaust of Channel-2 phonons deposited into the interstitial medium as knots untie, and integrating the 3D particle-to-wave decompression bloom gives Δρ_geom = [(3/2)Γ(1/3) − 3]/(4π/3) = +24.313%, which locks Υ_D = 1 − 2·Δρ_geom = 0.51375 and Υ_B = Υ_D·(1 + Δρ_geom) = 0.63865 from pure geometry with zero fitted parameters. GR and MOND are welcome to take Υ_D = 0.51375 and Υ_B = 0.63865 into their own pipelines now — and retire the two built-in fits they have been leaning on."""

leg4_block = """**Leg 4 — The submarine hull vs. the bare neutron's exposed thread (clock rate vs. drag clock, `scripts/t6_lorentz_legs_closed.py`, `papers/NEUTRON_LIFETIME.md`).** There is no "time dilation" in PWC — only physical clock rates. Optical cavities and atomic clocks show zero sign of the ~370 km/s motion through the medium because their closed proton–electron envelopes act as a pressurized submarine hull: the bound electromagnetic spacer lattice and internal standing-wave clock rate co-contract by γ⁻¹, cancelling the frame to < 10⁻¹⁷. A bare neutron has no proton–electron shield — its 14:38 thread sits exposed to the medium, and its lifetime is the drag's clock. At the NIST cold-beam speed (v_eff = 791 m/s), the pure wave-equation clock-rate shift τ₀(γ − 1) is 3.06×10⁻⁹ s — nine orders of magnitude short of the observed ~9 s beam-vs-bottle gap. Instead, motion through the medium presses the exposed phase-lock into its channel at first order in v/c₀ with the derived 19:1:18 axial-pitch tariff k = 3069.87 (`scripts/k_final_19_18.py`), shifting the drag clock by +7.17 s to τ_beam = 886.17 s vs. NIST's 887.7 ± 2.2 s (0.7σ). Shielded matter hides the frame by co-contraction; unshielded matter measures the frame directly."""

target_anchor = "**Where the argument bites.** The two mass-to-light ratios are no longer fitted anywhere — geometry sets them."

for root in roots:
    if not root.exists():
        continue
    for md in root.rglob("*.md"):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = txt

        # 1. Scrub any 'time dilation' phrasing -> 'clock-rate shift'
        txt = txt.replace("time dilation", "clock-rate shift")
        txt = txt.replace("Time dilation", "Clock-rate shift")

        # 2. Insert the -2 fits GR/MOND callout if not yet present
        if "why GR and MOND owe the rotation data two parameters" not in txt and target_anchor in txt:
            txt = txt.replace(target_anchor, minus_two_callout + "\n\n" + target_anchor)

        # 3. Append Leg 4 to S13 / IV.4 if t6_lorentz_legs_closed.py is mentioned and Leg 4 isn't yet
        if "t6_lorentz_legs_closed.py" in txt and "Leg 4 — The submarine hull" not in txt:
            txt = txt.replace(
                "scripts/t6_lorentz_legs_closed.py",
                "scripts/t6_lorentz_legs_closed.py\n\n" + leg4_block,
                1
            )

        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            print(f"[POLISHED] {md}")

deriv_path = Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC\papers\PHASE_WAVE_COSMOLOGY_DERIVATIONS.md")
if deriv_path.exists():
    dtxt = deriv_path.read_text(encoding="utf-8")
    if "# THE HONEST OPEN ITEMS" in dtxt:
        sec = dtxt.split("# THE HONEST OPEN ITEMS")[1].split("# THE SCOREBOARD")[0]
        print("\n" + "=" * 78)
        print("CURRENT HONEST OPEN ITEMS SECTION IN PHASE_WAVE_COSMOLOGY_DERIVATIONS.md:")
        print("=" * 78)
        print(sec.strip())
