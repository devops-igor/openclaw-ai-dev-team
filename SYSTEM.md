# AI Development Team - System Architecture

**Version:** 1.0  
**Date:** 2026-03-21  
**Status:** Active  
**Team:** pm_bot, dev_bot, qa_bot

---

## 1. Overview

This document defines the complete system architecture for the AI Development Team, including hand-off protocols, communication standards, and operational procedures.

### 1.1 Team Composition

| Agent | Role | Model | Primary Function |
|-------|------|-------|------------------|
| **pm_bot** | Project Manager | minimax-m2.7:cloud | Orchestration, planning, reporting |
| **dev_bot** | Lead Developer | xiaomi/mimo-v2-pro | Implementation, code generation |
| **qa_bot** | Quality Gatekeeper | xiaomi/mimo-v2-pro | Code review, security, testing |

### 1.2 Core Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAN (Product Owner)                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │ Requirements
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│  pm_bot - Project Manager                                          │
│  • Receives requirements                                            │
│  • Decomposes into tasks                                            │
│  • Creates PROJECT_PLAN.md & TASK.md                               │
│  • Delegates to team members                                        │
│  • Tracks progress & reports status                                 │
└───────────────────────────┬───────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│  dev_bot - Developer       │   │  qa_bot - QA              │
│  • Implements features     │   │  • Reviews code           │
│  • Writes tests           │   │  • Finds bugs              │
│  • Follows standards      │   │  • Validates quality       │
│  • Uses xiaomi/mimo-v2-pro  │   │  • Security audit          │
└───────────────────────────┘   └───────────────────────────┘
            │                               │
            │ Code Complete                 │ Review Complete
            │ + Tests                       │ + Issues Found
            ▼                               ▼
┌───────────────────────────────────────────────────────────────────┐
│  pm_bot - Review & Consolidate                                       │
│  • Reviews handoff documents                                        │
│  • Determines completion status                                     │
│  • Reports to human                                                 │
│  • Archives completed project                                       │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. Hand-Off Protocol

### 2.1 Hand-Off Types

#### 2.1.1 PM → Dev (Task Assignment)
**Trigger:** New task or feature request  
**Document:** `TASK.md` in project directory  
**Location:** `C:\Users\Igor\OpenClaw\{project}\TASK.md`

**Required Contents:**
```markdown
# Task Assignment: [Feature Name]

**Project:** [project-name]
**Assigned to:** dev_bot
**Priority:** [High/Medium/Low]
**Assigned by:** pm_bot
**Date:** [YYYY-MM-DD]
**Status:** IN_PROGRESS

## Objective
[Clear statement of what needs to be built]

## Reference Documents
- [ ] SPEC.md or requirements doc
- [ ] Architecture decisions
- [ ] Relevant standards

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Definition of Done
- [ ] Code implemented
- [ ] Tests written & passing
- [ ] Follows coding standards
- [ ] Ready for QA review

## Questions/Blockers
[None or list of issues needing resolution]

## Handoff Checklist (Dev)
- [ ] Read TASK.md
- [ ] Understood requirements
- [ ] Started implementation
- [ ] Notified pm_bot of start
```

#### 2.1.2 Dev → QA (Code Review Request)
**Trigger:** Implementation complete, tests passing  
**Document:** `DEV_HANDOVER.md` in project directory  
**Location:** `C:\Users\Igor\OpenClaw\{project}\DEV_HANDOVER.md`

**Required Contents:**
```markdown
# Development Handover: [Feature Name]

**From:** dev_bot
**To:** qa_bot
**Date:** [YYYY-MM-DD]
**Status:** READY_FOR_REVIEW

## Implementation Summary
[What was built, key files modified]

## Files Changed
- `path/to/file1.go` - Description of changes
- `path/to/file2.go` - Description of changes

## New Dependencies
[Any new packages or libraries]

## Test Coverage
- Unit tests: [X]% coverage
- Integration tests: [X] tests passing
- Manual testing: [Yes/No + notes]

## Known Issues/Limitations
[List any known problems or unimplemented features]

## Testing Notes
[How to test, what to look for]

## Access Instructions
```bash
# How to build
go build ./...

# How to test
go test ./... -v

# How to run
./binary-name
```

## Sign-Off
- [ ] dev_bot: Implementation complete
- [ ] Tests passing locally
- [ ] Code formatted (go fmt)
- [ ] Code vetted (go vet)
- [ ] Ready for QA review
```

#### 2.1.3 QA → PM (Review Complete)
**Trigger:** Code review finished  
**Document:** `QA_REPORT.md` in project directory  
**Location:** `C:\Users\Igor\OpenClaw\{project}\QA_REPORT.md`

**Required Contents:**
```markdown
# QA Report: [Feature Name]

**From:** qa_bot
**To:** pm_bot
**Date:** [YYYY-MM-DD]
**Status:** [APPROVED / APPROVED_WITH_COMMENTS / REJECTED]

## Review Summary
[High-level assessment]

## Issues Found

### Critical (Must Fix)
| Issue | File | Line | Description | Fix Required |
|-------|------|------|-------------|--------------|
| 1 | file.go | 42 | Description | Yes |

### Important (Should Fix)
| Issue | File | Line | Description | Recommendation |
|-------|------|------|-------------|-----------------|
| 1 | file.go | 42 | Description | Recommended fix |

### Minor (Nice to Fix)
| Issue | File | Line | Description |
|-------|------|------|-------------|
| 1 | file.go | 42 | Description |

## Security Findings
[Any security vulnerabilities identified]

## Test Quality Assessment
- Coverage: [X]%
- Test quality: [Good/Fair/Poor]
- Missing test cases: [List]

## Recommendations
[Non-blocking suggestions for improvement]

## Sign-Off
- [ ] qa_bot: Review complete
- [ ] All critical issues addressed or acknowledged
- [ ] Security review passed
- [ ] Ready for [production/release/next phase]

## Next Steps
- [ ] Fix critical issues (if any)
- [ ] Re-review (if REJECTED)
- [ ] Approve for release (if APPROVED)
```

#### 2.1.4 PM → Human (Project Complete)
**Trigger:** QA approved, ready for delivery  
**Document:** `COMPLETION_REPORT.md`  
**Location:** `C:\Users\Igor\OpenClaw\{project}\COMPLETION_REPORT.md`

```markdown
# Project Completion Report: [Project Name]

**Completed by:** Team (pm_bot, dev_bot, qa_bot)
**Date:** [YYYY-MM-DD]
**Duration:** [X days/hours]

## Deliverables
[What was built and delivered]

## Quality Summary
- Tests: [X] passing
- Coverage: [X]%
- Critical issues: [0 or list]
- Security findings: [0 or list]

## Files Delivered
[Full list of project files]

## Usage
[How to build, test, and run]

## Notes
[Any important information for the human]

## Sign-Off
✅ pm_bot: Project complete
✅ dev_bot: Code delivered  
✅ qa_bot: Quality approved
```

---

### 2.2 Hand-Off Checklist

For each handoff, the **sending agent** must:

- [ ] Complete all required fields in handoff document
- [ ] Verify all referenced files exist and are accessible
- [ ] Run local tests and confirm they pass
- [ ] Format code (`go fmt`) and vet (`go vet`)
- [ ] Update project status in `TEAM_STATUS.json`
- [ ] Notify receiving agent with handoff document location
- [ ] Archive previous handoff documents

For each handoff, the **receiving agent** must:

- [ ] Read handoff document completely
- [ ] Acknowledge receipt to sending agent
- [ ] Verify all referenced files are present
- [ ] Begin work within agreed timeframe
- [ ] Report any issues or blockers immediately

---

### 2.3 Escalation Path

```
┌─────────────────────────────────────────────┐
│  Issue Identified                           │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│  Agent Attempts Resolution                   │
│  • Clarify requirements                     │
│  • Research solutions                       │
│  • Apply fixes                              │
└─────────────────────┬───────────────────────┘
                      │
            ┌─────────┴─────────┐
            │ Issue Persists?   │
            └─────────┬─────────┘
                      │
              ┌───────┴───────┐
              │               │
             YES             NO
              │               │
              ▼               ▼
    ┌─────────────────┐   ┌─────────────────┐
    │ Escalate to PM  │   │ Continue Work    │
    │                 │   │                 │
    │ • Document issue│   │ • Complete task  │
    │ • Impact assess │   │ • Proceed to    │
    │ • Get guidance  │   │   next step     │
    └─────────────────┘   └─────────────────┘
```

**Escalation Triggers:**
- Unclear or conflicting requirements
- Technical blockers > 1 hour
- Scope changes mid-task
- Resource constraints
- Timeline risks

---

## 3. Communication Standards

### 3.1 Communication Channels

| Channel | Use Case | Format |
|---------|----------|--------|
| **Handoff Documents** | Formal task/state transfer | Markdown files |
| **TEAM_STATUS.json** | Real-time status tracking | JSON |
| **Session Messages** | Quick coordination | Direct messages |

### 3.2 Status Reporting

All agents must maintain `TEAM_STATUS.json` with current state:

```json
{
  "team": {
    "pm_bot": {
      "status": "active",
      "current_task": "Project planning",
      "blocking_issues": []
    },
    "dev_bot": {
      "status": "active",
      "current_task": "Implementing feature X",
      "progress_percent": 45,
      "blocking_issues": []
    },
    "qa_bot": {
      "status": "available",
      "current_task": "Waiting for review request",
      "blocking_issues": []
    }
  },
  "projects": {
    "project-name": {
      "status": "in_progress",
      "phase": "development",
      "next_handoff": "dev → qa",
      "expected_completion": "2026-03-21"
    }
  }
}
```

### 3.3 Response Time Expectations

| Priority | Response Time | Example |
|----------|--------------|---------|
| **Critical** | < 15 minutes | Blocker, security issue |
| **High** | < 1 hour | Task assignment, urgent review |
| **Normal** | < 4 hours | Standard requests |
| **Low** | < 24 hours | Questions, minor issues |

---

## 4. Project Structure

```
C:\Users\Igor\OpenClaw\
├── openclaw-ai-dev-team\          # Team workspace
│   ├── pm_bot\                    # Project Manager
│   │   ├── AGENTS.md             # Role definition
│   │   ├── SOUL.md               # Personality
│   │   └── SETTINGS.md           # Configuration
│   │
│   ├── dev_bot\                   # Lead Developer
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   └── SETTINGS.md
│   │
│   ├── qa_bot\                    # Quality Assurance
│   │   ├── AGENTS.md
│   │   ├── SOUL.md
│   │   └── SETTINGS.md
│   │
│   ├── shared\                    # Shared resources
│   │   ├── WORKFLOW.md           # Process definitions
│   │   ├── GOLANG_STANDARDS.md   # Coding standards
│   │   ├── HANDOVER_PROTOCOL.md  # This document
│   │   └── TEAM_STATUS.json       # Real-time status
│   │
│   └── projects\                  # All projects
│       └── {project-name}\
│           ├── SPEC.md            # Requirements
│           ├── PROJECT_PLAN.md    # Timeline & tasks
│           ├── TASK.md            # Current task
│           ├── DEV_HANDOVER.md    # Dev → QA handoff
│           ├── QA_REPORT.md       # QA findings
│           ├── COMPLETION_REPORT.md # Final delivery
│           ├── cmd\               # Main applications
│           ├── internal\          # Private packages
│           └── pkg\               # Public packages
│
└── {project-directories}          # Individual projects
```

---

## 5. Quality Gates

### 5.1 Gate Definitions

| Gate | Owner | Criteria | Must Pass? |
|------|-------|----------|------------|
| **Implementation** | dev_bot | Code compiles, tests pass | Yes |
| **Code Review** | qa_bot | No critical issues | Yes |
| **Security** | qa_bot | No vulnerabilities | Yes |
| **Standards** | qa_bot | Follows GOLANG_STANDARDS | Yes |
| **Documentation** | dev_bot | README, comments complete | Yes |

### 5.2 Definition of Done

A task is **DONE-DONE** when:

1. ✅ Implementation complete (dev_bot)
2. ✅ All tests passing
3. ✅ Code formatted & vetted
4. ✅ QA review approved (qa_bot)
5. ✅ No critical issues outstanding
6. ✅ Documentation updated
7. ✅ PM confirmed delivery
8. ✅ Human acceptance received

---

## 6. Operational Procedures

### 6.1 Starting a New Project

1. **Human** → pm_bot: "I want to build [description]"
2. **pm_bot**: Creates `SPEC.md` for human review
3. **Human** → Approves SPEC or requests changes
4. **pm_bot**: Creates `PROJECT_PLAN.md` with timeline
5. **Human** → Approves plan
6. **pm_bot**: Creates project directory structure
7. **pm_bot**: Assigns first task to dev_bot via `TASK.md`

### 6.2 Task Execution

1. **dev_bot**: Reads `TASK.md`
2. **dev_bot**: Implements feature
3. **dev_bot**: Writes tests
4. **dev_bot**: Runs `go fmt ./... && go vet ./...`
5. **dev_bot**: Runs tests `go test ./... -v`
6. **dev_bot**: Creates `DEV_HANDOVER.md`
7. **dev_bot** → pm_bot: "Ready for review"

### 6.3 Code Review

1. **pm_bot** → qa_bot: Review request with `DEV_HANDOVER.md`
2. **qa_bot**: Reviews code
3. **qa_bot**: Creates `QA_REPORT.md`
4. **qa_bot** → pm_bot: "Review complete [status]"

### 6.4 Project Completion

1. **qa_bot**: APPROVED status on final review
2. **pm_bot**: Creates `COMPLETION_REPORT.md`
3. **pm_bot** → Human: "Project complete. [summary]"
4. **pm_bot**: Archives project in `projects/`
5. **pm_bot**: Updates `TEAM_STATUS.json`

---

## 7. Error Handling

### 7.1 Error Categories

| Category | Examples | Response |
|----------|----------|----------|
| **Technical** | API failures, compilation errors | Retry → Escalate if persistent |
| **Requirements** | Unclear specs, missing info | Clarify with human |
| **Quality** | Test failures, style violations | Fix before proceeding |
| **Security** | Vulnerabilities found | Block release until fixed |
| **Timeline** | Risk of missing deadline | Notify pm_bot immediately |

### 7.2 Retry Policy

| Attempt | Wait Time | Action if Failed |
|---------|-----------|------------------|
| 1 | Immediate | Try fix |
| 2 | 2 minutes | Try alternative approach |
| 3 | 5 minutes | Research, try again |
| N+1 | - | Escalate to pm_bot |

---

## 8. Document Versioning

| Document | Version | Last Updated | Notes |
|----------|---------|---------------|-------|
| SYSTEM.md | 1.0 | 2026-03-21 | Initial version |
| HANDOVER_PROTOCOL.md | 1.0 | 2026-03-21 | Initial version |

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **Handoff** | Formal transfer of work between agents |
| **DONE-DONE** | Task complete and quality approved |
| **Gate** | Checkpoint requiring approval to proceed |
| **Escalation** | Transfer of issue to higher authority |
| **Blocking Issue** | Problem preventing work continuation |

---

**Document Owner:** pm_bot  
**Review Cycle:** Monthly or after major project completion  
**Approval Required:** Human acknowledgment of any changes

---

_This document defines the operational framework for the AI Development Team. All agents must follow these procedures to ensure consistent, high-quality deliveries._
