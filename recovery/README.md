# IQ AI Tutor — Canonical Recovery Branch

This branch is an **isolated recovery/audit surface** based on `95c4a92ea98b42f354372b1e21779b81e19d1d24` from `main`.

It does **not** modify the student app in `index.html`, does not merge anything, and does not claim production readiness.

## What is transported

Two byte-preserving recovery bundles are stored as Base64 chunks under `recovery/transport/`:

- Golden Slice v0.1.1 — text/source/schema/test/report/provenance surface.
- Evidence Semantics v0.2.1 Surgical Patch — core executable implementation, schemas, tests, locks/manifests, report, math vendor, and compact source inputs.

The original artifact ZIP SHA-256 values are recorded in `recovery/manifest.json`.
The transport bundles have their own SHA-256 values and are verified before extraction.

## Reconstruct safely

Run:

```bash
python recovery/transport/unpack_recovery.py
```

By default this extracts to:

`/tmp/iq-ai-tutor-canonical-recovery`

so the Git working tree stays untouched.

## Important limitation

This first recovery commit intentionally does **not** transport several binary/nested baseline archives, the synthetic SQLite ledger, and large generated regression datasets. Those omissions are enumerated exactly in `recovery/manifest.json`.

Therefore Codex should:

1. audit the reconstructed source trees and provenance;
2. verify transport hashes;
3. inspect executable logic and test definitions;
4. run only tests whose declared dependencies are present;
5. report missing-dependency blockers rather than editing canonical files or fabricating replacements.

Do not merge this branch into `main` until recovery audit and provenance checks are complete.
