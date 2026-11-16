import zstandard, json, os
sessions = [
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check--\session-e0f8aec9-8cf8-4e78-828f-9c85a40b1983\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check--\session-b528db0d-9c17-4d54-86d5-784ede6f1ab4\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-106cf6e1-52ae-4461-8215-87809b2f7a56\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-8d00c7d7-2fa0-4db2-9fca-1eda20a7fdd1\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-df343153-0082-4f90-9f4f-3615cb2672d5\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-5aee0e0b-1376-497b-80a8-93a9e5fab01e\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-5f034167-0501-419d-abe5-921ca8574e26\session.v4.jsonl.zstd",
  r"C:\Users\jaden\.dsh\sessions\--C-Users-jaden-Downloads-PWC-Check-PWC--\session-b8c9c4da-b4f6-4243-9e93-0ab194f3a362\session.v4.jsonl.zstd",
]
for p in sessions:
    if not os.path.exists(p):
        print("MISSING", p); continue
    with open(p, "rb") as f:
        dctx = zstandard.ZstdDecompressor()
        reader = dctx.stream_reader(f)
        raw = reader.read()
    lines = raw.decode("utf-8", errors="replace").splitlines()
    print("="*90)
    print("FILE:", p.split("sessions\\")[1])
    print("lines:", len(lines))
    for ln in lines[:60]:
        try:
            obj = json.loads(ln)
            s = json.dumps(obj, ensure_ascii=False)
        except Exception:
            s = "RAW: " + ln[:200]
        if len(s) > 700: s = s[:700] + "..."
        print(" ", s)
