# WORKLOG.md - Append-Only Action Log

**Important:** This file is append-only. Never edit or delete previous entries. Only append new entries at the bottom with a timestamp.

## Purpose

WORKLOG.md prevents "memory loss" caused by context window compaction. By logging every major action, decision, and state change, the team maintains continuity even when previous context becomes unavailable.

## When to Log

Append an entry for each of these events:

- [ ] Task started (with task ID and brief description)
- [ ] Task completed (with results/outcome)
- [ ] Significant decision made (with rationale)
- [ ] Architecture change (with reason)
- [ ] Blocking issue identified
- [ ] Blocking issue resolved
- [ ] Review started/completed
- [ ] Test run completed (with results)
- [ ] Deployment or release
- [ ] Handoff created
- [ ] Meeting or sync with human
- [ ] Dependencies added/removed/updated
- [ ] Configuration changes
- [ ] Security findings
- [ ] Performance issues discovered/addressed
- [ ] Refactoring completed
- [ ] Bug discovered and fixed
- [ ] Any event that future-you would need to know about

## Format

Each entry should follow this pattern:

```markdown
---
[YYYY-MM-DD HH:MM] | [AGENT] | [ACTION TYPE] | [PROJECT/TASK]
Details: [What happened, key decisions, outcomes, links to related docs]
---
```

### Examples

```markdown
---
2026-03-20 14:30 | pm_bot | TASK_ASSIGNMENT | btc-price-cli
Details: Assigned TASK-001 to dev_bot. Task: Implement Bitcoin price fetcher using CoinGecko API. Priority: HIGH.
---

2026-03-20 14:45 | dev_bot | TASK_STARTED | btc-price-cli
Details: Started TASK-001. Plan: Create price fetcher service with caching. Will use stdlib net/http.
---

2026-03-20 15:30 | dev_bot | DECISION | btc-price-cli
Details: Chose 30-second cache TTL after researching CoinGecko rate limits (10-30 calls/min free tier). Rationale: Stay within free tier while providing fresh data.
---

2026-03-20 16:00 | dev_bot | TESTS_COMPLETED | btc-price-cli
Details: Unit tests passing (12/12). Coverage: 87%. Integration tests: 4/4 passing. go vet: clean. go fmt: clean.
---

2026-03-20 16:15 | dev_bot | HANDOFF_CREATED | btc-price-cli
Details: Created DEV_HANDOVER.md. Notified pm_bot for QA review. Files changed: 5 .go files, 3 test files. Ready for qa_bot.
---

2026-03-20 16:30 | qa_bot | REVIEW_STARTED | btc-price-cli
Details: Received DEV_HANDOVER.md. Starting code review. Focus areas: error handling, API client reuse, test quality.
---

2026-03-20 17:00 | qa_bot | REVIEW_COMPLETED | btc-price-cli
Details: Review APPROVED with 2 minor comments (naming improvement). No critical issues. Security: clean. Test coverage adequate (87%).
---

2026-03-20 17:15 | pm_bot | PROJECT_COMPLETED | btc-price-cli
Details: All gates passed. Created COMPLETION_REPORT.md. Notified human. Project archived.
```

## Maintenance

- **Every team member** must append entries when they perform work
- **Entries must be timestamped** in ISO 8601 format (YYYY-MM-DD HH:MM)
- **Be concise but complete** — include enough detail to understand later
- **Reference related documents** (TASK.md, QA_REPORT.md, etc.)
- **Don't delete or edit** old entries, even if they contain errors. Correct in a new entry if needed.

## Template

When starting a new project, copy this WORKLOG.md template to the project root.

## Benefits

- **Continuity:** You can restart work after context window compaction and catch up by reading WORKLOG.md
- **Auditability:** Complete history of decisions and actions
- **Onboarding:** New team members can read WORKLOG to understand project evolution
- **Blame-free debugging:** When something breaks, the worklog shows what changed and when
- **Handoff support:** Complements formal handoff documents with chronological context

## Integration with Handoffs

Formal handoff documents (TASK.md, DEV_HANDOVER.md, QA_REPORT.md) contain the official record. WORKLOG.md provides the chronological narrative. Use both:

- **Formal handoffs** for structured information, acceptance criteria, and sign-offs
- **WORKLOG** for the day-to-day story of how the work unfolded

---

**Last Updated:** 2026-03-21  
**Maintained by:** pm_bot  
