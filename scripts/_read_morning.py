import zstandard, json, os, re
p = r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check--\session-bf3791cf-ecb6-4737-98b9-73929d937cb2\session.v4.jsonl.zstd"
with open(p, "rb") as f:
    dctx = zstandard.ZstdDecompressor()
    reader = dctx.stream_reader(f)
    raw = reader.read()
lines = raw.decode("utf-8", errors="replace").splitlines()
print("TOTAL LINES:", len(lines))
user_msgs = []
bhp = []
for ln in lines:
    try: obj = json.loads(ln)
    except: continue
    t = obj.get("type")
    if t == "user/message":
        for c in obj.get("data", {}).get("content", []):
            txt = c.get("text", "")
            if txt:
                user_msgs.append(txt)
    s = ln
    if re.search(r"Max-P|max-p|cold-weld|14:38|terminal melt", s, re.I):
        bhp.append(ln[:400])
print("USER MESSAGES:", len(user_msgs))
for i, m in enumerate(user_msgs[:12]):
    print("---USER[%d]---" % i)
    print(m[:500])
print()
print("BH-TEXT HITS IN TRANSCRIPT:", len(bhp))
for h in bhp[:5]:
    print(" *", h)
