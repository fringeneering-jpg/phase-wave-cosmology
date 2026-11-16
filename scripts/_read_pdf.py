import sys
try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("NO_PYPDF"); sys.exit(0)
r = PdfReader(r"C:\Users\jaden\Downloads\Stellar Scaling Derivation Audit.pdf")
print("PAGES:", len(r.pages))
txt = ""
for i, pg in enumerate(r.pages):
    txt += "\n=== PAGE %d ===\n" % (i+1)
    txt += pg.extract_text() or ""
print(txt[:20000])
