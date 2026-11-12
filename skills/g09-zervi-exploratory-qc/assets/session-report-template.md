# Exploratory QC Session: <Mission>

## Metadata

| Field | Value |
|---|---|
| Session | `<YYYY-MM-DD-HHmm-scope>` |
| Charter authorization | `<explicitly authorized session or charter>` |
| Date | `<YYYY-MM-DD>` |
| Branch / commit | `<branch>` / `<commit>` |
| Environment | `<local, staging, or other>` |
| Approved origins | `<origins>` |
| Browser tools | `<available or unavailable; name tools>` |
| Evidence policy | `<sanitization or capture constraints>` |
| Output base / register | `<explicitly authorized OUTPUT_BASE>` / `<OUTPUT_BASE/findings.md, or chat-only proposal>` |

## Mission

**Scope:** <Narrow journey, module, or product risk explored>

**Question:** <What this session tried to learn>

**Out of scope:** <What this session deliberately did not cover>

## Environment And Actors

| Actor | Account or data type | Authorization boundary |
|---|---|---|
| `<guest/client/provider/owner/non-owner>` | `<synthetic or none>` | `<read-only or authorized mutations>` |

## Budget

| Item | Value |
|---|---|
| Maximum duration | `20 minutes absolute; no override` |
| Start / deadline | `<HH:mm>` / `<HH:mm>` |
| Exploration cutoff | `<deadline minus 3 minutes when possible>` |
| Actual duration | `<minutes>` |
| Stop reason | `<maximum reached, mission complete, or safety/tool blocker>` |

## Paths Explored

| Route or module | Actor | Goal or hypothesis | Status | Result | Evidence |
|---|---|---|---|---|---|
| `<path>` | `<actor>` | `<goal>` | `<EXECUTED or NOT TESTED>` | `<observed outcome, or planned probe when not tested>` | `<sanitized reference or N/A>` |

If browser tools are unavailable, do not record observed findings. Keep probes `NOT TESTED`, describe the execution-ready charter/plan here, and record the tooling blocker below.

## Findings

### Clear Defects

| Candidate or ID | Severity | Trigger | Observed behavior | Impact | Evidence |
|---|---|---|---|---|---|
| `<NEW or ZQC-###>` | `<P0-P3 by impact>` | `<steps>` | `<observation>` | `<user/business impact>` | `<reference>` |

### Improvement Opportunities

| Candidate or ID | Severity | Observation | Opportunity | Evidence |
|---|---|---|---|---|
| `<NEW or ZQC-###>` | `<P0-P3 by impact>` | `<current behavior>` | `<improvement>` | `<reference>` |

### Product Questions

| Candidate or ID | Severity | Decision needed | Why it matters | Evidence |
|---|---|---|---|---|
| `<NEW or ZQC-###>` | `<P0-P3 by impact>` | `<question>` | `<impact>` | `<reference>` |

### Environment/Tooling Blockers

| Candidate or ID | Severity | Blocker | Impact on session | Evidence |
|---|---|---|---|---|
| `<NEW or ZQC-###>` | `<P0-P3 by impact>` | `<constraint>` | `<coverage lost>` | `<reference>` |

## Evidence Notes

- `<Sanitized screenshots, console observations, API responses, or reproduction notes. Never include secrets or browser storage contents.>`

## Blocked And Untested Areas

| Area | Reason | Confidence impact | Suggested next probe |
|---|---|---|---|
| `<area>` | `<budget, access, environment, data, or authorization>` | `<impact>` | `<next action>` |

## Cumulative Register Changes

| Action | ID | Category | Detail |
|---|---|---|---|
| `<added/updated/moved/none>` | `<ZQC-### or N/A>` | `<category>` | `<occurrence, evidence, status, or move>` |

Record category-specific closure evidence: explicit retest for defects; recorded product/maintainer decision for Product Questions; recorded product decision or verified implementation for Improvement Opportunities; evidence that access, tooling, or environment was restored for Environment/Tooling Blockers. Preserve prior history.

Closing a blocker does not change probe outcomes. Keep every unexecuted probe `NOT TESTED`, schedule it only in a later separately authorized session, and never imply it passed.

## Session Summary

<Concise statement of product coherence, highest risk, and remaining uncertainty.>
