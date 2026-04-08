# AI Development Team - Hand-Off Protocol

**Version:** 1.0  
**Date:** 2026-03-21  
**Team:** pm_bot, dev_bot, qa_bot  

---

## 1. Protocol Overview

The Hand-Off Protocol defines the formal process for transferring work between team members. Each handoff includes complete documentation to ensure no information is lost and every agent can continue work seamlessly.

### 1.1 Why This Protocol Exists

- **Clarity:** Everyone knows exactly what was done and what needs to happen next
- **Continuity:** Work can continue even if an agent is unavailable
- **Accountability:** Each handoff is documented and traceable
- **Quality:** Formal gates ensure issues are caught before moving forward
- **Context Preservation:** WORKLOG.md prevents memory loss from context window compaction

### 1.2 Append-Only Log Requirement

Every project **must** have a `WORKLOG.md` file in the project root. This file is append-only and logs all major actions, decisions, and state changes.

**When to append to WORKLOG.md:**

- Task started/completed
- Significant decisions made (with rationale)
- Architecture changes
- Blocking issues identified/resolved
- Reviews started/completed
- Test runs with results
- Dependencies added/removed
- Configuration changes
- Security findings
- Performance issues
- Refactoring completed
- Handoffs created
- Meetings/syncs with human

**Format:**

```markdown
---
[YYYY-MM-DD HH:MM] | [AGENT] | [ACTION TYPE] | [PROJECT/TASK]
Details: [What happened, key decisions, outcomes, links]
---
```

**Responsibility:** Each agent is responsible for appending to WORKLOG.md whenever they perform work on the project. This is not optional — it's part of the Definition of Done.

### 1.2 Handoff Types

| Handoff | From | To | Purpose |
|---------|------|----|--------|
| **Task Assignment** | pm_bot | dev_bot | Start new work |
| **Development Complete** | dev_bot | qa_bot | Begin review |
| **Review Complete** | qa_bot | pm_bot | Report findings |
| **Project Delivery** | pm_bot | Human | Final delivery |

---

## 2. Task Assignment (pm_bot → dev_bot)

### 2.1 When to Use
- Starting a new feature
- Bug fix assignment
- Any new work item

### 2.2 Process

1. pm_bot creates `TASK.md` in project directory
2. pm_bot **appends entry to WORKLOG.md** logging task assignment
3. pm_bot notifies dev_bot with location and priority
4. dev_bot acknowledges and begins work
5. dev_bot updates TASK.md as progress is made

### 2.3 TASK.md Template

```markdown
# Task Assignment: [TASK NAME]

## Metadata
- **Task ID:** TASK-[NUMBER]
- **Project:** [PROJECT NAME]
- **Assigned to:** dev_bot
- **Assigned by:** pm_bot
- **Date:** [YYYY-MM-DD]
- **Priority:** [CRITICAL/HIGH/MEDIUM/LOW]
- **Status:** [PENDING/IN_PROGRESS/BLOCKED/COMPLETED]
- **Deadline:** [YYYY-MM-DD or "None"]

## Objective
[One clear sentence describing what needs to be accomplished]

## Background/Context
[Why this task exists, what problem it solves, any relevant history]

## Requirements
### Must Have (Required for completion)
- [ ] [Requirement 1]
- [ ] [Requirement 2]

### Should Have (Strongly desired)
- [ ] [Should requirement 1]

### Nice to Have (Optional)
- [ ] [Nice to have 1]

## Technical Specifications
### Files to Modify/Create
- `path/to/file1.go` - [Description]
- `path/to/file2.go` - [Description]

### Dependencies
- [List any new dependencies or tools needed]

### Architecture Notes
[Any architectural decisions, constraints, or guidelines]

## Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Definition of Done
- [ ] Code compiles without errors
- [ ] Unit tests written and passing
- [ ] Code formatted (`go fmt`)
- [ ] Code passes vet (`go vet`)
- [ ] Follows GOLANG_STANDARDS.md
- [ ] No critical TODO comments left
- [ ] Documentation updated
- [ ] **WORKLOG.md entry added for task completion**
- [ ] Ready for QA review

## Testing Strategy
[How to test this feature, what edge cases to consider]

## Acceptance Criteria
1. [Testable criterion 1]
2. [Testable criterion 2]
3. [Testable criterion 3]

## Questions/Blockers
| # | Question/Blocker | Status | Resolution |
|---|------------------|--------|------------|
| 1 | [Question text] | [Open/Resolved] | [Resolution or "TBD"] |

## Progress Log
| Date | Time | Update |
|------|------|--------|
| YYYY-MM-DD | HH:MM | Started task |
| YYYY-MM-DD | HH:MM | [Progress update] |

## Handoff Checklist (dev_bot)
- [ ] Read TASK.md completely
- [ ] Understood requirements and acceptance criteria
- [ ] Clarified any questions with pm_bot
- [ ] **Appended WORKLOG.md entry for task start**
- [ ] Begun implementation
- [ ] Notified pm_bot of task start
- [ ] `go fmt ./...` — formatted
- [ ] `go vet ./...` — vet passed
- [ ] `go test -race ./...` — tests passed with race detector
- [ ] `golangci-lint run ./...` — linter passed (or noted if unavailable)
```

---

## 3. Development Handover (dev_bot → qa_bot)

### 3.1 When to Use
- Feature implementation is complete
- All tests pass locally
- Code is formatted and vetted
- Ready for quality review

### 3.2 Process

1. dev_bot completes implementation
2. dev_bot runs final checks (fmt, vet, test)
3. dev_bot creates DEV_HANDOVER.md
4. **dev_bot appends WORKLOG.md entry for handoff to QA**
5. dev_bot notifies pm_bot of completion
6. pm_bot reviews and assigns to qa_bot
7. qa_bot acknowledges and begins review

### 3.3 DEV_HANDOVER.md Template

```markdown
# Development Handover: [FEATURE NAME]

## Metadata
- **Handover ID:** HANDOVER-[NUMBER]
- **From:** dev_bot
- **To:** qa_bot
- **Project:** [PROJECT NAME]
- **Date:** [YYYY-MM-DD]
- **Task Reference:** TASK-[NUMBER]
- **Status:** [READY_FOR_REVIEW/NEEDS_CLARIFICATION]

## Executive Summary
[Brief 2-3 sentence description of what was built]

## Implementation Details

### What Was Built
[Detailed description of the implementation]

### Files Changed
| File | Type | Change Description |
|------|------|------------------|
| `cmd/main.go` | Modified | [Description] |
| `internal/api/client.go` | Created | [Description] |
| `pkg/models/price.go` | Modified | [Description] |

### New Files
- `new/file1.go` - [Purpose]
- `new/file2.go` - [Purpose]

### Deleted Files
- `old/file.go` - [Reason for deletion]

### Code Statistics
- **Lines added:** [X]
- **Lines modified:** [X]
- **Lines deleted:** [X]
- **Files changed:** [X]

## Testing Summary

### Unit Tests
- **Total tests:** [X]
- **Passing:** [X]
- **Failing:** [0 or number]
- **Coverage:** [X]%

### Test Files
- `pkg/models/price_test.go` - [X] tests
- `internal/api/client_test.go` - [X] tests
- `internal/ticker/ticker_test.go` - [X] tests

### Integration Tests
- **Status:** [Passing/Failing/None]
- **Notes:** [Any relevant information]

## Build & Runtime

### Build & Runtime

### Build Instructions
```bash
go build -o binary-name ./cmd
```

### Run Instructions
```bash
./binary-name [arguments]
```

---

## Language / Stack Specifics

> Fill out the section that matches your project's language. Delete the section that does not apply.

### Go Projects

```bash
# 1. Format
go fmt ./...

# 2. Vet
go vet ./...

# 3. Lint
golangci-lint run ./...

# 4. Security scan
gosec ./...

# 5. Vulnerability check
govulncheck ./...

# 6. Build
go build ./...

# 7. Test with race detector
go test -race ./...
```

### Python Projects

```bash
# 1. Format
black .

# 2. Lint
flake8 .

# 3. Type check (if mypy installed)
mypy .

# 4. Test with coverage
pytest -v --cov=. --cov-report=term-missing

# 5. Dependency vulnerabilities
pip-audit
```

### Environment Requirements
- Go version: [1.XX+]
- External dependencies: [List or "None"]
- Environment variables: [List or "None"]

## Known Issues & Limitations

### Known Issues
| Issue | Severity | Workaround |
|-------|----------|------------|
| [Description] | [High/Medium/Low] | [Workaround or "None"] |

### Limitations
- [Limitation 1]
- [Limitation 2]

## Security Considerations
[Any security-related notes, dependency checks, or concerns]

## Edge Cases Handled
- [ ] [Edge case 1]
- [ ] [Edge case 2]
- [ ] [Edge case 3]

## Unhandled Edge Cases
[List any edge cases that are NOT handled]

## Dependencies
### New Dependencies
- `package@version` - [Why needed]

### Updated Dependencies
- `package@oldversion` → `package@newversion` - [Why updated]

### Removed Dependencies
- `package@version` - [Why removed]

## Performance Considerations
[Any performance notes, benchmarks, or concerns]

## Rollback Plan
[How to rollback this change if needed]

## Sign-Off (dev_bot)
- [x] Implementation complete
- [x] All tests pass locally
- [x] Code formatted (`go fmt`)
- [x] Code passes vet (`go vet`)
- [x] Follows GOLANG_STANDARDS.md
- [x] No critical TODO comments left
- [x] Documentation updated
- [x] **Appended final WORKLOG.md entry for development completion**
- [x] Ready for QA review

**Developer:** dev_bot  
**Date:** [YYYY-MM-DD]  
**Confirmation:** I confirm this implementation meets the requirements in TASK-[NUMBER]

---

## QA Review Checklist (qa_bot fills this out)
| Check | Status | Notes |
|-------|--------|-------|
| Code review started | [ ] | Date: |
| Critical issues found | [ ] | Count: |
| Important issues found | [ ] | Count: |
| Minor issues found | [ ] | Count: |
| Security review complete | [ ] | Date: |
| Review complete | [ ] | Date: |
```

---

## 4. QA Report (qa_bot → pm_bot)

### 4.1 When to Use
- Code review is complete
- All findings documented
- Ready to report status to pm_bot

### 4.2 Process

1. qa_bot completes review of DEV_HANDOVER.md
2. qa_bot creates QA_REPORT.md
3. **qa_bot appends WORKLOG.md entry for review completion**
4. qa_bot notifies pm_bot with findings
5. pm_bot reviews and determines next steps
6. If issues found, pm_bot assigns fixes to dev_bot

### 4.3 QA_REPORT.md Template

```markdown
# QA Report: [FEATURE NAME]

## Metadata
- **Report ID:** QA-[NUMBER]
- **From:** qa_bot
- **To:** pm_bot
- **Project:** [PROJECT NAME]
- **Date:** [YYYY-MM-DD]
- **Review Duration:** [X hours]
- **Handover Reference:** HANDOVER-[NUMBER]
- **Status:** [APPROVED/APPROVED_WITH_COMMENTS/CONDITIONAL_APPROVAL/REJECTED]

## Review Summary
[2-3 sentence executive summary of review findings]

### Overall Assessment
| Aspect | Rating | Notes |
|--------|--------|-------|
| Code Quality | [Excellent/Good/Fair/Poor] | [Notes] |
| Test Coverage | [Excellent/Good/Fair/Poor] | [Notes] |
| Security | [Excellent/Good/Fair/Poor] | [Notes] |
| Performance | [Excellent/Good/Fair/Poor] | [Notes] |
| Documentation | [Excellent/Good/Fair/Poor] | [Notes] |

## Issues Found

### Critical Issues (MUST FIX - Blocks approval)
| # | Issue | File | Line | Severity | Description | Recommendation |
|---|-------|------|------|----------|-------------|----------------|
| 1 | [ID] | file.go | 42 | Critical | [Description] | [Fix recommendation] |

**Critical Issues Count:** [NUMBER]  
**Status:** [All fixed / X remaining]

### Important Issues (SHOULD FIX - Strongly recommended)
| # | Issue | File | Line | Severity | Description | Recommendation |
|---|-------|------|------|----------|-------------|----------------|
| 1 | [ID] | file.go | 42 | Important | [Description] | [Fix recommendation] |

**Important Issues Count:** [NUMBER]  
**Status:** [All addressed / X remaining]

### Minor Issues (NICE TO FIX - Non-blocking)
| # | Issue | File | Line | Severity | Description | Recommendation |
|---|-------|------|------|----------|-------------|----------------|
| 1 | [ID] | file.go | 42 | Minor | [Description] | [Suggestion] |

**Minor Issues Count:** [NUMBER]

## Security Findings

### Vulnerabilities
| # | Vulnerability | CVSS | Description | Mitigation |
|---|---------------|------|-------------|------------|
| 1 | [Type] | [Score] | [Description] | [Mitigation] |

### Security Concerns
[Any other security-related observations]

## Test Quality Assessment

### Coverage Analysis
- **Current coverage:** [X]%
- **Target coverage:** [X]%
- **Gap:** [X]%

### Test Quality
| Aspect | Rating | Notes |
|--------|--------|-------|
| Test independence | [Good/Poor] | [Notes] |
| Edge case coverage | [Good/Poor] | [Notes] |
| Test maintainability | [Good/Poor] | [Notes] |

### Missing Tests
| Test | File | Priority | Reason Missing |
|------|------|----------|----------------|
| [Test name] | file_test.go | [High/Med/Low] | [Reason] |

## Performance Findings

### Observations
[Any performance-related findings]

### Recommendations
[Any performance optimization suggestions]

## Code Review Comments

### General Comments
[Any overall code quality observations]

### Specific Comments
| # | File | Line | Comment |
|---|------|------|---------|
| 1 | file.go | 42 | [Comment text] |

## Recommendations

### Required Actions
1. [Action 1 - required for approval]
2. [Action 2 - required for approval]

### Suggested Improvements
1. [Improvement 1]
2. [Improvement 2]

### Best Practices Not Followed
| Practice | Location | Recommendation |
|----------|----------|----------------|
| [Practice] | file.go:42 | [How to fix] |

## Approval Status

### Decision
**Status:** [APPROVED / APPROVED_WITH_COMMENTS / CONDITIONAL_APPROVAL / REJECTED]

### Conditions (if APPROVED_WITH_COMMENTS or CONDITIONAL_APPROVAL)
1. [Condition 1]
2. [Condition 2]

### Next Steps
- [ ] [Next step 1]
- [ ] [Next step 2]

## Time Spent
| Activity | Time |
|----------|------|
| Code review | [X] hours |
| Security review | [X] hours |
| Testing | [X] hours |
| Documentation | [X] hours |
| **Total** | [X] hours |

## Sign-Off

**QA Engineer:** qa_bot  
**Date:** [YYYY-MM-DD]  
**Decision:** [APPROVED / etc.]

**WORKLOG:** Reviewer confirms WORKLOG.md entry created with findings summary.

---

## 5. Blocking Issue Escalation

### 5.1 When to Escalate
- Issue blocks progress for > 1 hour
- Technical uncertainty cannot be resolved locally
- Requirements conflict identified
- Resource constraint (access, permissions, tools)
- Timeline risk identified

### 5.2 Escalation Template

```markdown
# Escalation: [ISSUE BRIEF]

## Metadata
- **Escalation ID:** ESC-[NUMBER]
- **From:** [Agent name]
- **To:** pm_bot
- **Date:** [YYYY-MM-DD]
- **Priority:** [CRITICAL/HIGH/MEDIUM]

## Issue Description
[Detailed description of the blocking issue]

## Impact
- **Affected Tasks:** [List task IDs]
- **Timeline Impact:** [Estimated delay]
- **Quality Impact:** [Description]

## What I've Tried
1. [Attempt 1]
2. [Attempt 2]
3. [Attempt 3]

## Resolution Options
| Option | Pros | Cons | Recommended? |
|--------|------|------|--------------|
| A | [Pros] | [Cons] | [Yes/No] |
| B | [Pros] | [Cons] | [Yes/No] |

## Recommended Resolution
[Clear recommendation for how to proceed]

## Requested Decision
[What decision is needed from pm_bot]

## Requested By
[Agent name]  
[YYYY-MM-DD]
```

---

## 6. Project Completion Report (pm_bot → Human)

### 6.1 When to Use
- All tasks complete
- QA approved
- Ready for human acceptance

### 6.2 COMPLETION_REPORT.md Template

```markdown
# Project Completion Report: [PROJECT NAME]

## Metadata
- **Project:** [PROJECT NAME]
- **Completed by:** Team (pm_bot, dev_bot, qa_bot)
- **Date:** [YYYY-MM-DD]
- **Duration:** [X days/hours]
- **Version:** [1.0.0 or appropriate version]

## Executive Summary
[2-3 sentence summary of what was delivered]

## Deliverables

### Primary Deliverables
| Deliverable | Status | Location |
|-------------|--------|----------|
| [Feature 1] | ✅ Complete | [Path] |
| [Feature 2] | ✅ Complete | [Path] |

### Secondary Deliverables
| Deliverable | Status | Location |
|-------------|--------|----------|
| [Documentation] | ✅ Complete | [Path] |
| [Tests] | ✅ Complete | [Path] |

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Test Coverage | ≥80% | [X]% | ✅/❌ |
| Critical Issues | 0 | [X] | ✅/❌ |
| Security Issues | 0 | [X] | ✅/❌ |
| Code Style | Pass | Pass | ✅/❌ |

## Technical Details

### Technology Stack
- **Language:** Go [version]
- **Dependencies:** [List key dependencies]
- **Platform:** [Windows/macOS/Linux/All]

### Files Delivered
- **Total files:** [X]
- **Code files:** [X]
- **Test files:** [X]
- **Documentation:** [X]

## Usage

### Installation
```bash
[Installation instructions]
```

### Build
```bash
[Build instructions]
```

### Run
```bash
[Run instructions]
```

### Test
```bash
[Testing instructions]
```

## Known Issues
| Issue | Severity | Workaround |
|-------|----------|------------|
| [Issue] | [Low/Medium] | [Workaround] |

## Lessons Learned

### What Went Well
1. [Positive observation 1]
2. [Positive observation 2]

### What Could Be Improved
1. [Improvement area 1]
2. [Improvement area 2]

### Action Items
| Item | Owner | Target Date |
|------|-------|-------------|
| [Action] | [Name] | [Date] |

## Project Statistics

| Statistic | Value |
|-----------|-------|
| Total tasks | [X] |
| Tasks completed | [X] |
| Critical issues found | [X] |
| Important issues found | [X] |
| Minor issues found | [X] |
| Review cycles | [X] |
| Total development time | [X] hours |
| Total QA time | [X] hours |
| Total PM time | [X] hours |

## Sign-Off

| Role | Agent | Signature | Date | WORKLOG |
|------|-------|-----------|------|---------|
| Project Manager | pm_bot | ✅ | YYYY-MM-DD | ✅ Maintained |
| Lead Developer | dev_bot | ✅ | YYYY-MM-DD | ✅ Maintained |
| Quality Assurance | qa_bot | ✅ | YYYY-MM-DD | ✅ Maintained |
| Product Owner | [Human Name] | ⏳ | Pending | N/A |

**WORKLOG Confirmation:** All agents confirm that WORKLOG.md was maintained throughout the project with entries for all major actions and decisions.

## Appendix

### A. Relevant Documents
- SPEC.md - Requirements specification
- PROJECT_PLAN.md - Project plan and timeline
- TASK.md files - Individual task documentation
- DEV_HANDOVER.md - Development documentation
- QA_REPORT.md - Quality assurance report

### B. External Dependencies
| Dependency | Version | Purpose |
|------------|---------|---------|
| [Package] | [Ver] | [Purpose] |

---

**Report Generated by:** pm_bot  
**Report Date:** [YYYY-MM-DD]
```

---

## 7. Quick Reference

### 7.1 Handoff Flow

```
Human → pm_bot: "Build X"
    ↓
pm_bot creates TASK.md
    ↓
dev_bot: Implements X
    ↓
dev_bot → pm_bot: "Ready for review"
    ↓
pm_bot assigns to qa_bot
    ↓
qa_bot reviews code
    ↓
qa_bot → pm_bot: "QA Report complete"
    ↓
If issues: dev_bot fixes → qa_bot re-reviews
If approved: pm_bot creates COMPLETION_REPORT
    ↓
pm_bot → Human: "X is complete"
```

### 7.2 Document Locations

| Document | Location |
|----------|----------|
| TASK.md | `[PROJECT]/TASK.md` |
| DEV_HANDOVER.md | `[PROJECT]/DEV_HANDOVER.md` |
| QA_REPORT.md | `[PROJECT]/QA_REPORT.md` |
| COMPLETION_REPORT.md | `[PROJECT]/COMPLETION_REPORT.md` |
| TEAM_STATUS.json | `[TEAM_ROOT]/shared/TEAM_STATUS.json` |

### 7.3 Status Definitions

| Status | Meaning |
|--------|---------|
| PENDING | Task exists, not started |
| IN_PROGRESS | Work actively underway |
| BLOCKED | Work stopped, waiting for something |
| READY_FOR_REVIEW | Complete, awaiting review |
| NEEDS_CLARIFICATION | Issues need resolution |
| APPROVED | Passed review |
| REJECTED | Failed review, needs fixes |
| COMPLETED | Fully done and delivered |

---

**Protocol Owner:** pm_bot  
**Last Updated:** 2026-03-21  
**Version:** 1.0

---

_This protocol ensures smooth transitions between team members and complete transparency in all project work. Following this protocol rigorously will result in higher quality deliveries and clearer accountability._
