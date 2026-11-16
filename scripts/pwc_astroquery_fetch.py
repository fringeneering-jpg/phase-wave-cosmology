import os
from astroquery.vizier import Vizier

# Force VizieR to use the US-Smithsonian mirror instead of Strasbourg
Vizier.MAIN_ROW_LIMIT = -1
Vizier.ROW_LIMIT = -1
Vizier.TIMEOUT = 120

# Switch site to Harvard mirror
Vizier.VIZIER_SERVER = "vizier.cfa.harvard.edu"

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

print("--- FLUSHING ATLAS³D VIA HARVARD MIRROR (J/MNRAS/413/813) ---")
try:
    atlas_result = Vizier.get_catalogs("J/MNRAS/413/813")
    if atlas_result:
        atlas_table = atlas_result[0]
        out_path = os.path.join(output_dir, "atlas3d_cappellari.csv")
        atlas_table.write(out_path, format="csv", overwrite=True)
        print(f"[SUCCESS] ATLAS³D saved to {out_path} ({len(atlas_table)} rows)")
    else:
        print("[WARNING] ATLAS³D query returned empty.")
except Exception as e:
    print(f"[ERROR] ATLAS³D pull failed: {e}")

print("\n--- FLUSHING COMA MAGNITUDES VIA HARVARD MIRROR (J/A+A/490/923) ---")
try:
    coma_result = Vizier.get_catalogs("J/A+A/490/923")
    if coma_result:
        coma_table = coma_result[0]
        out_path = os.path.join(output_dir, "coma_michard_andreon.csv")
        coma_table.write(out_path, format="csv", overwrite=True)
        print(f"[SUCCESS] Coma catalog saved to {out_path} ({len(coma_table)} rows)")
    else:
        print("[WARNING] Coma catalog query returned empty.")
except Exception as e:
    print(f"[ERROR] Coma catalog pull failed: {e}")

print("\n--- MIRROR FLUSH COMPLETE ---")