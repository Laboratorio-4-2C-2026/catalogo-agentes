# Zervi Exploratory QC Findings

Bundled initialization template, not an executed register or evidence of zero defects. Use the full operator-supplied existing register when available. Initialize `OUTPUT_BASE/findings.md` only with explicit output authorization; otherwise propose content in chat. Session reports belong in `OUTPUT_BASE/sessions/`.

This cumulative register preserves distinct exploratory QC findings across sessions for incremental agent updates and fast human review. Session reports provide detailed evidence; this file tracks the latest state without erasing history.

## Update Rules

1. Read the full register before adding or changing an entry.
2. Deduplicate by normalized **route/module + actor + trigger + observed behavior + impact**.
3. If the key matches, update `Last seen`, append sanitized evidence, and increment `Occurrences`.
4. Do not merge findings that are merely similar but have different root behavior.
5. Assign the next sequential stable ID in the form `ZQC-###` only to a distinct finding. Never reuse an ID.
6. Close a Clear Defect only after explicit retest evidence confirms resolution.
7. Close a Product Question only after an explicit product/maintainer decision is recorded as evidence.
8. Close an Improvement Opportunity only after an explicit product decision or verified implementation is recorded as evidence.
9. Close an Environment/Tooling Blocker only after evidence confirms that access, tooling, or environment was restored.
10. Closing a blocker does not resolve its unexecuted probes. Keep them `NOT TESTED`; they require a later separately authorized session and must never be implied to have passed.
11. Never erase history. Move closed entries to **Resolved/closed** and preserve the original category, discovery, evidence, decisions, implementation, restoration, probe outcomes, and retest history.

## Legends

### Severity

| Severity | Meaning |
|---|---|
| P0 | Safety, data, or security failure, or a total product blocker. |
| P1 | Core flow or authorization failure without a viable workaround. |
| P2 | Significant incorrect or degraded behavior with a workaround or limited scope. |
| P3 | Minor visual, copy, or usability issue. |

Assign severity from impact, never from ticket wording or ticket priority.

### Status

| Status | Meaning |
|---|---|
| Open | Confirmed and unresolved. |
| Needs decision | Product intent or desired behavior requires an explicit decision. |
| Blocked | Confirmation or progress is prevented by an environment, tooling, access, or data constraint. |
| Fixed pending verification | A fix is reported but has not passed explicit retest. |
| Closed | Category-specific closure evidence is recorded and the entry has moved to Resolved/closed. |

## Entry Template

```markdown
### ZQC-### - <Concise title>

- **Category:** <Clear Defect | Improvement Opportunity | Product Question | Environment/Tooling Blocker>
- **Severity:** <P0 | P1 | P2 | P3, based on impact>
- **Status:** <Open | Needs decision | Blocked | Fixed pending verification | Closed>
- **Route/module:** <normalized route or module>
- **Actor:** <guest | client | provider | owner | non-owner>
- **Trigger:** <normalized action or state>
- **Observed behavior:** <what happens>
- **Expected/coherent behavior:** <what should happen or question to resolve>
- **Impact:** <user, business, trust, safety, or data impact>
- **First seen:** <YYYY-MM-DD session link>
- **Last seen:** <YYYY-MM-DD session link>
- **Occurrences:** <count>
- **Evidence:** <sanitized evidence links or notes>
- **Closure evidence:** <required category-specific retest, decision, verified implementation, or access/tooling/environment restoration; N/A while open>
- **Unexecuted probes:** <NOT TESTED probes requiring a later separately authorized session; none if fully executed>
- **History:** <dated status, evidence, and decision changes; append only>
```

## Clear Defects

_No entries in template._

## Improvement Opportunities

_No entries in template._

## Product Questions

_No entries in template._

## Environment/Tooling Blockers

_No entries in template._

## Resolved/closed

_No entries in template._
