import fitz, re
doc = fitz.open(r"C:\Users\jaden\Downloads\Stellar Scaling Derivation Audit.pdf")
out = []
for i in range(len(doc)):
    t = doc[i].get_text()
    out.append("=== PAGE %d ===\n" % (i+1) + t)
full = "\n".join(out)
p = r"C:\Users\jaden\Downloads\PWC-Check\_gemini_audit_chat.txt"
with open(p, "w", encoding="utf-8") as f:
    f.write(full)
print("total chars:", len(full))
# extract all user prompts for an outline of the conversation
prompts = re.findall(r"User prompt: ([^\n]+)", full)
for i, pr in enumerate(prompts):
    print("USER[%d]: %s" % (i, pr[:220]))
