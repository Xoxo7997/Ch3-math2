#!/usr/bin/env python3
"""Reconstruct IQ AI Tutor recovery bundles OUTSIDE the tracked repository by default."""
from __future__ import annotations
import argparse, base64, hashlib, io, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLES = {
    "golden_slice": {
        "prefix": "golden_slice_text.tar.gz.b64.part",
        "parts": 4,
        "sha256": "2b182a8a16323aa90879b13c6831302c6495f7be5e552b19b13737b7743f7da3",
    },
    "evidence_semantics": {
        "prefix": "evidence_semantics_core.tar.gz.b64.part",
        "parts": 2,
        "sha256": "b5309af07549e8121fd6fe8099670a5729a8de3ed2145d4e9bbc049ecb04b75f",
    },
}

def safe_extract(tf: tarfile.TarFile, dest: Path) -> None:
    dest = dest.resolve()
    for m in tf.getmembers():
        target = (dest / m.name).resolve()
        if target != dest and dest not in target.parents:
            raise RuntimeError(f"unsafe archive path: {m.name}")
    tf.extractall(dest)

def reconstruct(name: str, dest: Path) -> None:
    spec = BUNDLES[name]
    chunks = []
    for i in range(spec["parts"]):
        p = ROOT / f'{spec["prefix"]}{i:03d}'
        if not p.is_file():
            raise FileNotFoundError(p)
        chunks.append(p.read_text(encoding="ascii"))
    raw = base64.b64decode("".join(chunks), validate=True)
    got = hashlib.sha256(raw).hexdigest()
    if got != spec["sha256"]:
        raise RuntimeError(f"{name}: transport SHA mismatch: {got}")
    out = dest / name
    out.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        safe_extract(tf, out)
    print(f"{name}: OK sha256={got} extracted_to={out}")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="/tmp/iq-ai-tutor-canonical-recovery")
    ap.add_argument("--bundle", choices=["all", *BUNDLES], default="all")
    args = ap.parse_args()
    dest = Path(args.dest)
    names = list(BUNDLES) if args.bundle == "all" else [args.bundle]
    for name in names:
        reconstruct(name, dest)

if __name__ == "__main__":
    main()
