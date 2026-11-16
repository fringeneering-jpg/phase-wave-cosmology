import fitz
doc = fitz.open(r"C:\Users\jaden\Downloads\Stellar Scaling Derivation Audit.pdf")
print("pages:", len(doc))
out = r"C:\Users\jaden\Downloads\PWC-Check\_pdf_pages"
import os
os.makedirs(out, exist_ok=True)
for i in range(len(doc)):
    page = doc[i]
    # check text layer first
    t = page.get_text().strip()
    if t:
        print("PAGE", i+1, "HAS TEXT:", len(t), "chars:", t[:200].replace(chr(10), " | "))
    pix = page.get_pixmap(dpi=110)
    pix.save(os.path.join(out, "page_%03d.png" % (i+1)))
print("rendered to", out)
