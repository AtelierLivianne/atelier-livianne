import os
import sqlite3

p = os.path.expandvars(
    r"%APPDATA%\Cursor\User\workspaceStorage\4c9cd7f7832f2e9769e77ed9cbca8a55\state.vscdb"
)
if not os.path.isfile(p):
    print("missing", p)
    raise SystemExit(1)

con = sqlite3.connect(p)
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("tables", tables)
for t in tables[:5]:
    try:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(t, n)
    except Exception as e:
        print(t, "err", e)

hits = []
for key, ln in con.execute("SELECT key, length(value) FROM ItemTable").fetchall():
    blob = con.execute("SELECT value FROM ItemTable WHERE key=?", (key,)).fetchone()[0]
    if not isinstance(blob, (bytes, memoryview)):
        continue
    b = bytes(blob)
    if b"heroVideo" in b or b"appShell" in b:
        hits.append((ln, key))
hits.sort(reverse=True)
print("hits", hits[:10])
if hits:
    key = hits[0][1]
    blob = con.execute("SELECT value FROM ItemTable WHERE key=?", (key,)).fetchone()[0]
    s = bytes(blob).decode("utf-8", errors="ignore")
    open(r"d:\Desktop\atelier-livianne-hero-demo\_db_blob.txt", "w", encoding="utf-8", errors="ignore").write(s)
    print("wrote _db_blob.txt from", key, "len", len(s))
