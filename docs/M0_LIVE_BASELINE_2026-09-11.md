# IQ AI Tutor — M0 Live Baseline Audit

Date: 2026-09-11
Branch: `m0/execution-control-plane`

## Purpose
Freeze the observable live state before any integrity migration or production write. This document is a read-only baseline, not a statement that the current design is production-ready.

## Canonical GitHub repository state
- Repository: `Xoxo7997/Ch3-math2`
- Default branch: `main`
- Root contains only `README.md` and a single large `index.html` (~215 KB).
- Latest commit on `main` is from 2026-09-01.
- No Next.js/TypeScript project structure, package manifest, CI workflow, Supabase migrations, or live Edge Function source is currently version-controlled in this repository.

### M0 conclusion
There is material drift between GitHub and the live Supabase project. The live backend is newer than the repository. This must be resolved before production migrations continue.

## Live Supabase project baseline
- Project ref: `lcaqnjuktsbrhljwynec`
- Region: `ap-southeast-1`
- PostgreSQL: 17.6.1
- Status: active / healthy
- Auth users: 0
- Development branches: 0

### Row counts at audit time
- `skills`: 29
- `questions`: 226
- `attempts`: 271
- `quiz_runs`: 29
- `student_devices`: 8
- `student_review_state`: 5

### Public schema tables
- `7997`
- `skills`
- `questions`
- `attempts`
- `student_devices`
- `quiz_runs`
- `student_review_state`

All listed public tables currently have RLS enabled.

## RLS and grants
Current explicit public policies observed:
- `questions`: public SELECT (`qual = true`)
- `skills`: public SELECT (`qual = true`)
- `attempts`: anon INSERT when `user_id IS NULL`
- `attempts`: authenticated INSERT when `auth.uid() = user_id`

Tables `7997`, `quiz_runs`, `student_devices`, and `student_review_state` have RLS enabled with no client-facing policies.

Database grants for `anon` and `authenticated` are broad at the table/column privilege layer. RLS still controls row access, but the current public SELECT policy on `questions` means the raw `options` and `solution` columns are client-readable through the Data API. The anon INSERT policy on `attempts` also means client-supplied `is_correct`, `trap_code`, and related fields can still be inserted on the legacy path when `user_id` is null.

### Integrity implication
The new `quiz-engine` performs server-side scoring, but the legacy direct Data API paths remain open. Therefore server-only scoring is not yet an enforced system invariant.

## Edge Function
Live function:
- name: `quiz-engine`
- deployed version: 2
- `verify_jwt`: false
- uses a per-device secret scheme for the current phone prototype
- uses server-side service-role access for scoring and persistence
- function comments explicitly state that this is device-scoped prototype proof, not user identity/authentication

The function is materially newer than the GitHub repository and is not currently version-controlled there.

## Migrations
Supabase currently reports only two migrations:
- `20260910095446_v011_verified_mastery_foundation`
- `20260910095509_v011_seed_chapter3_review_forms`

The live schema contains more structure than is represented by the available migration history. A complete reproducible baseline therefore does not yet exist in Git.

## Supabase advisor findings
Security advisor:
- RLS enabled with no policy on `7997`, `quiz_runs`, `student_devices`, `student_review_state` (informational; these may intentionally be service-only tables).

Performance advisor:
- missing covering indexes for foreign keys on:
  - `attempts.question_id`
  - `questions.skill_code`
  - `quiz_runs.question_id`
  - `student_review_state.skill_code`
- `quiz_runs_device_active_index` currently reported unused.

## Highest-risk M0 findings
1. **Repository/live drift — BLOCKER.** The backend cannot yet be recreated confidently from Git.
2. **No staging branch — BLOCKER.** Production is currently the only database environment.
3. **Legacy answer exposure — CRITICAL.** Public SELECT on `questions` exposes raw `options` and `solution` columns.
4. **Legacy attempt forgery path — CRITICAL.** Anonymous direct inserts into `attempts` remain possible with caller-supplied truth fields.
5. **No authenticated student identity — CRITICAL for durable student state.** `auth.users = 0`.
6. **Edge Function auth is prototype-only.** `verify_jwt=false` is deliberate today, but cannot be the final production identity boundary.
7. **Migration history is incomplete as a rebuild source.** Current schema must be baselined before further DDL.

## M0 no-write rule
Until a staging environment exists and the baseline is captured:
- no destructive DDL on production;
- no direct production schema edits in the dashboard;
- no attempt to "clean up" historical rows in place;
- no reliance on client-provided correctness or trap values for new production evidence.

## Next execution sequence
1. Create a Supabase development/staging branch from the current project.
2. Capture/reconstruct the current schema as a reproducible baseline in Git.
3. Snapshot/version-control the live `quiz-engine` source.
4. Define environment boundaries (`local`, `staging`, `production`) and secret ownership.
5. Test migration apply/rollback and backup/restore on staging.
6. Only then start M1 Integrity Kernel migrations: authenticated ownership, immutable question/version truth, server-only scoring, append-only attempts, and closure of legacy direct-write/read paths.

## Exit condition for M0
M0 is complete only when a clean environment can be recreated from version-controlled migrations/functions, staging exists, secrets are environment-scoped, rollback/restore is tested, and production is no longer the place where schema design is experimented on.
