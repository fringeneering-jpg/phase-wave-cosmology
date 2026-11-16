import sqlite3, os, json
p = r"C:\Users\jaden\AppData\Roaming\gemini\shared_proto_db"
print("exists:", os.path.exists(p), "size:", os.path.getsize(p) if os.path.exists(p) else 0)
if os.path.exists(p):
    con = sqlite3.connect(p)
    cur = con.cursor()
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    for name, sql in cur.fetchall():
        print("TABLE:", name)
        print("  ", (sql or "")[:300].replace(chr(10), " "))
    con.close()
