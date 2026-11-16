import fitz, re
doc = fitz.open(r"C:\Users\jaden\Downloads\Austin Powers Black Hole Pun.pdf")
full = ""
for i in range(len(doc)):
    full += doc[i].get_text() + "\n"
p = r"C:\Users\jaden\Downloads\PWC-Check\_argon_sweep.txt"
with open(p, "w", encoding="utf-8") as f:
    f.write(full)
print("chars:", len(full))
for m in re.finditer(r"## (D\d+[^\n]{0,80})", full):
    print(m.group(1)[:100])
for m in re.finditer(r"([A-Z][a-z][A-Za-z /-]{3,60} (?:CLOSED|HIT|Miss))", full):
    print("STATUS:", m.group(1)[:110])
