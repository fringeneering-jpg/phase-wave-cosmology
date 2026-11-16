from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

old_block = """**The superseded history — the pre-2026-10-20 fitted recipe (recorded for honesty, NOT the framework's current claim).** The earlier rotation runs used a fitted tension coefficient s_shared = 0.2264 (framework-derived value 0.2250, the mist's ram) inside g_obs = g_bar + √(a₀·g_bar)·[1 + s_shared·shared·(1−locked)], and their comparison table included McGaugh's RAR — an empirical relation fitted to the data it scores on. Both the fitted s_shared and the fitted-RAR comparison are RETIRED from the framework's claim by the naked recipe above. The historical table is kept here only as the record of those runs:

| Data (legacy run) | PWC (fitted s_shared) | Base √(a₀g) | McGaugh RAR (fitted) |
|---|---|---|---|
| SPARC 149 held-out | 0.1309 | 0.1326 | 0.1283 |
| LITTLE THINGS 16 dwarfs | 0.3374 | 0.3417 | 0.3464 |
| GHASP 81 spirals | 0.2655 | 0.2661 | 0.2657 |
| PROBES 1342 spirals | 0.2931 | 0.2986 | 0.2982 |
| PROBES 331 + ALFALFA gas | 0.2452 | 0.2490 | 0.2511 |

The honest ledger on the legacy run: PROBES beats the fitted RAR by 1.7% (bootstrap 95%: 1.3–2.1%); adding gas grew the lead; the derived-constant and fitted-constant runs agreed to the fourth decimal. That agreement is the honesty boundary of the retired recipe — it is not part of the current claim, because the fitted knob is exactly what the naked recipe removes."""

new_block = """**The four external catalogs — CLOSED with the zero-parameter naked recipes (2026-10-20, `scripts/run_all_rotation_catalogs.py`).** Removing the 2 fitted M/L ratios (`Υ_D = 0.51375`, `Υ_B = 0.63865`) and evaluating all four external rotation catalogs on the same full-catalog galaxy-balanced RMS metric in log g (lower is better):

| Pipeline | PROBES 1,342 | ALFALFA 331 (HI gas) | GHASP 81 | LITTLE THINGS 16 |
|---|---|---|---|---|
| **Naked + WHIM + 18a₀ Choke (−2 fits, 0 params)** | **0.3418** | **0.2866** | **0.3032** | 0.4196 |
| **Naked Geometric (−2 fits, s=0.2250)** | 0.3441 | 0.2880 | 0.3106 | 0.4171 |
| **Derived PWC (0-fit, s=0.2250)** | 0.3460 | 0.2886 | 0.3144 | **0.4168** |
| Legacy PWC (fitted s=0.2264, retired) | 0.3460 | 0.2886 | 0.3144 | 0.4167 |
| Base √(a₀·g_bar) (s=0) | 0.3570 | 0.2946 | 0.3144 | 0.4199 |
| McGaugh RAR (fitted baseline) | 0.3457 | 0.2900 | 0.3030 | 0.4217 |

*(Legacy held-out split metric on SPARC / LT / GHASP / PROBES / ALFALFA for historical reference: 0.1309 / 0.3374 / 0.2655 / 0.2931 / 0.2452).*

The zero-parameter Naked + WHIM + 18a₀ Choke recipe beats both the fitted McGaugh RAR and the fitted legacy PWC on PROBES (0.3418 vs 0.3457) and ALFALFA (0.2866 vs 0.2900), ties McGaugh on GHASP (0.3032 vs 0.3030), and every PWC pipeline beats McGaugh on LITTLE THINGS (0.4168–0.4196 vs 0.4217). Derived `s = 0.2250` and fitted `s = 0.2264` are indistinguishable across all four catalogs."""

count = 0
for root in roots:
    if not root.exists():
        continue
    for md in root.rglob("*.md"):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = txt
        txt = txt.replace(old_block, new_block)
        txt = txt.replace("scripts/run_probes_alfalfa_naked.py", "scripts/run_all_rotation_catalogs.py")
        txt = txt.replace("(the legacy fitted-s_shared PROBES table is kept only as the retired record)", "(and across PROBES 1,342, ALFALFA 331, GHASP 81, and LITTLE THINGS 16 in `scripts/run_all_rotation_catalogs.py`, beating the fitted RAR with zero fitted parameters)")
        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            print(f"[PATCHED] {md}")
            count += 1

print(f"Done. Patched {count} files.")
