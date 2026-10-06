# IQ AI Tutor — Codex Oracle Micro Handoff v0.1

This temporary branch is based on:
- repository: Xoxo7997/Ch3-math2
- baseline branch: m0/execution-control-plane
- baseline commit: 5b2aa831a351f43ab3fa4fcedf5180d44fad881b

Purpose: transfer the minimal read-only inputs needed for Oracle Evaluation Harness v0.1 without using the mobile file picker.

## Reconstruct

Run:

```bash
python codex_handoff/reconstruct_handoff.py
```

Expected SHA-256:

`224c503ba637bb7744807a6a1540907890456323ed90df7b2c6b9770b7334dde`

Then extract the resulting ZIP into a NEW working/input directory. Treat all extracted artifacts as read-only references.

The micro handoff contains:
- key Evidence Semantics v0.2.1 engine sources,
- four-skill contracts and canonical items,
- Golden Slice four-skill contracts/items,
- eight representative SDE-01 frozen responses,
- their reviewed representations,
- current projections,
- development failure matrix and summary.

The eight SDE cases are:
SDE01-R001, R002, R018, R019, R025, R026, R029, R030.

## Guardrails

Do NOT modify:
- scorer,
- Gold,
- ontology,
- contracts,
- projector,
- Golden Slice baselines,
- Production,
- Staging.

Do not fix bugs while building Oracle Evaluation Harness v0.1.
Do not create Holdout or Student Zero.
Do not merge this temporary handoff branch.

After reconstructing and verifying the archive, use the invoked IQ AI Tutor conversation for the Oracle Harness task context.
