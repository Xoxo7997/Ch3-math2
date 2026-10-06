from pathlib import Path
import base64, hashlib

ROOT = Path(__file__).resolve().parent
parts = []
for i in range(7):
    p = ROOT / f"part_{i:02d}.b64"
    if not p.exists():
        raise SystemExit(f"missing {p.name}")
    parts.append(p.read_text(encoding="ascii").strip())

last = ROOT / "part_07.double.b64"
if not last.exists():
    raise SystemExit("missing part_07.double.b64")
parts.append(base64.b64decode(last.read_text(encoding="ascii").strip()).decode("ascii"))

encoded = "".join(parts)
data = base64.b64decode(encoded, validate=True)
expected = "224c503ba637bb7744807a6a1540907890456323ed90df7b2c6b9770b7334dde"
actual = hashlib.sha256(data).hexdigest()
out = ROOT / "IQ_AI_Tutor_Codex_Oracle_Micro_Handoff_v0_1.zip"
out.write_bytes(data)

print("output:", out)
print("bytes:", len(data))
print("sha256:", actual)
if actual != expected:
    raise SystemExit("SHA256 mismatch")
print("OK: handoff reconstructed and verified")
