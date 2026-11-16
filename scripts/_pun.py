import fitz
doc = fitz.open(r"C:\Users\jaden\Downloads\Austin Powers Black Hole Pun.pdf")
print("pages:", len(doc))
for i in range(len(doc)):
    t = doc[i].get_text().strip()
    print("=== PAGE", i+1, "===")
    print(t[:600] if t else "(no text layer - image page)")
