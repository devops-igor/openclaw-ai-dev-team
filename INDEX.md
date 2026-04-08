# AI Development Team - Documentation Index

**Team:** pm_bot, dev_bot, qa_bot  
**Version:** 1.1  
**Last Updated:** 2026-03-21  

---

## 📚 Documentation Overview

This index provides a quick reference to all team documentation. Each document serves a specific purpose in our operational framework.

### 📁 Complete Documentation Map

```
openclaw-ai-dev-team/
├── SYSTEM.md                          # Complete system architecture (THIS FILE)
├── HANDOVER_PROTOCOL.md              # Detailed hand-off procedures
├── TEAM_README.md                    # Team overview & quick start
├── TEAM_MODELS.md                    # Model configuration
├── QUICK_START.md                    # Getting started guide
│
├── 📂 pm_bot/                        # Project Manager
│   ├── AGENTS.md                     # Role & responsibilities
│   ├── SOUL.md                       # Personality & values
│   └── SETTINGS.md                   # Configuration
│
├── 📂 dev_bot/                       # Lead Developer
│   ├── AGENTS.md                     # Role & responsibilities
│   ├── SOUL.md                       # Personality & values
│   └── SETTINGS.md                   # Configuration & model
│
├── 📂 qa_bot/                        # Quality Assurance
│   ├── AGENTS.md                     # Role & responsibilities
│   ├── SOUL.md                       # Personality & values
│   └── SETTINGS.md                   # Configuration
│
└── 📂 shared/                       # Shared resources
    ├── WORKFLOW.md                   # Standard workflow
    ├── GOLANG_STANDARDS.md           # Coding standards
    ├── GOLANG_PROJECT_TEMPLATE.md    # Project template
    ├── WORKLOG_TEMPLATE.md           # Append-only action log template
    ├── MAKEFILE_TEMPLATE            # Build automation
    ├── STATUS_TEMPLATE.json          # Status tracking template
    ├── TEAM_STATUS.json              # Current team status
    ├── DEVELOPMENT_NOTES.md          # Development notes
    └── HANDOVER_PROTOCOL.md          # Detailed handoff procedures
```

---

## 📖 Document Purpose Guide

### 🔰 Getting Started
| Document | When to Read | Purpose |
|----------|-------------|---------|
| **QUICK_START.md** | First time using team | Learn basic workflow |
| **TEAM_README.md** | New to team | Understand team structure |
| **shared/WORKFLOW.md** | Before starting work | Learn standard process |

### 👤 Individual Agent Docs
| Document | Audience | Purpose |
|----------|----------|---------|
| **{agent}/AGENTS.md** | All agents | Role definition & responsibilities |
| **{agent}/SOUL.md** | Respective agent | Personality & working style |
| **{agent}/SETTINGS.md** | All agents | Technical configuration |

### 🔧 Operational Documents
| Document | Purpose | Update Frequency |
|----------|---------|-----------------|
| **SYSTEM.md** | Complete system architecture | Monthly |
| **HANDOVER_PROTOCOL.md** | Detailed hand-off procedures | As needed |
| **shared/GOLANG_STANDARDS.md** | Coding guidelines | As needed |
| **shared/WORKFLOW.md** | Process definitions | As needed |

### 📊 Tracking Documents
| Document | Purpose | Update Frequency |
|----------|---------|-----------------|
| **shared/TEAM_STATUS.json** | Real-time status | Per task |
| **shared/STATUS_TEMPLATE.json** | Status tracking template | Static |

---

## 🎯 Quick Reference by Role

### 📋 pm_bot (Project Manager)
**Priority Reading:**
1. ✅ SYSTEM.md (this file) - Full system understanding
2. ✅ HANDOVER_PROTOCOL.md - All handoff procedures
3. ✅ shared/WORKFLOW.md - Process coordination
4. ✅ TEAM_MODELS.md - Model strategy

**Key Responsibilities:**
- Task decomposition and assignment
- Team coordination and status tracking
- Quality gate management
- Human communication

---

### 👨‍💻 dev_bot (Lead Developer)
**Priority Reading:**
1. ✅ shared/GOLANG_STANDARDS.md - Coding standards
2. ✅ shared/GOLANG_PROJECT_TEMPLATE.md - Project structure
3. ✅ HANDOVER_PROTOCOL.md - Dev → QA handoff section
4. ✅ dev_bot/SOUL.md - Personality & values

**Key Responsibilities:**
- Implementation per TASK.md
- Test coverage
- Code quality
- Development handoff documentation

---

### 🔍 qa_bot (Quality Assurance)
**Priority Reading:**
1. ✅ shared/GOLANG_STANDARDS.md - Quality criteria
2. ✅ HANDOVER_PROTOCOL.md - QA review procedures
3. ✅ qa_bot/SOUL.md - Personality & values
4. ✅ SYSTEM.md - Understanding full context

**Key Responsibilities:**
- Code review
- Security assessment
- Test quality validation
- QA report documentation

---

## 🔄 Standard Workflow

### 1️⃣ Project Initiation
```
Human → pm_bot: "I want to build [description]"
    ↓
pm_bot creates SPEC.md (requirements)
    ↓
Human approves SPEC
    ↓
pm_bot creates PROJECT_PLAN.md (timeline)
    ↓
Human approves PLAN
    ↓
pm_bot creates project structure
    ↓
pm_bot assigns TASK.md to dev_bot
```

### 2️⃣ Implementation Phase
```
dev_bot reads TASK.md
    ↓
dev_bot implements feature
    ↓
dev_bot writes tests
    ↓
dev_bot runs: go fmt && go vet && go test
    ↓
dev_bot creates DEV_HANDOVER.md
    ↓
dev_bot → pm_bot: "Ready for review"
```

### 3️⃣ QA Review Phase
```
pm_bot assigns to qa_bot
    ↓
qa_bot reviews code
    ↓
qa_bot creates QA_REPORT.md
    ↓
If CRITICAL issues → dev_bot fixes → qa_bot re-reviews
    ↓
If APPROVED → pm_bot creates COMPLETION_REPORT
```

### 4️⃣ Delivery
```
pm_bot → Human: "Project complete"
    ↓
Human accepts delivery
    ↓
pm_bot archives project
    ↓
TEAM_STATUS.json updated
```

---

## 📝 Document Templates (in HANDOVER_PROTOCOL.md)

| Template | Location | Purpose |
|----------|----------|---------|
| TASK.md | Project root | Task assignment |
| DEV_HANDOVER.md | Project root | Dev → QA handoff |
| QA_REPORT.md | Project root | QA findings |
| COMPLETION_REPORT.md | Project root | Final delivery |
| Escalation template | HANDOVER_PROTOCOL.md | Issue escalation |

---

## 🏛️ System Architecture Summary

### Team Structure
```
Human (Product Owner)
    ↓
pm_bot (Project Manager)
    ↓
┌──────────┴──────────┐
↓                     ↓
dev_bot           qa_bot
(Developer)       (Quality)
```

### Models
| Agent | Model | Purpose |
|-------|-------|---------|
| pm_bot | minimax-m2.7:cloud | Planning & coordination |
| dev_bot | xiaomi/mimo-v2-pro | Code generation |
| qa_bot | xiaomi/mimo-v2-pro | Code review |

### Quality Gates
1. **Dev Gate:** Code compiles, tests pass, formatted, vetted
2. **QA Gate:** No critical issues, security passed
3. **PM Gate:** All gates passed, documentation complete
4. **Human Gate:** Final acceptance

---

## 🚨 Escalation Path

```
Issue identified
    ↓
Agent tries to resolve (3 attempts, ~10 min)
    ↓
Still blocked?
    ↓
    YES → Escalate to pm_bot
              ↓
         pm_bot assesses
              ↓
         Can resolve? → YES → Provide guidance
              ↓ NO
         pm_bot → Human: "Need decision"
```

---

## 📊 Status Definitions

| Status | Meaning |
|--------|---------|
| PENDING | Not started |
| IN_PROGRESS | Active work |
| BLOCKED | Waiting on something |
| READY_FOR_REVIEW | Complete, awaiting QA |
| NEEDS_CLARIFICATION | Questions need answers |
| APPROVED | Passed review |
| REJECTED | Failed review |
| COMPLETED | Fully delivered |

---

## 🎓 Key Principles

### From SOUL.md Files

**pm_bot Values:**
- Clarity over cleverness
- Accountability
- Quality over speed
- Completion celebration

**dev_bot Values:**
- Correctness first
- Simplicity over cleverness  
- Tested over assumed
- Craftsman pride

**qa_bot Values:**
- Quality is not optional
- Honesty over comfort
- Learning opportunities
- Code criticism, not people criticism

---

## 🔧 Tools & Commands

### Build & Test
```bash
# Format code
go fmt ./...

# Vet code
go vet ./...

# Run tests
go test ./... -v

# Run tests with coverage
go test -cover ./...

# Build
go build -o binary ./cmd
```

### Project Management
```bash
# Update status
# Edit shared/TEAM_STATUS.json

# Create project
# mkdir -p projects/{name}/{cmd,internal,pkg}

# Track handoffs
# Maintain HANDOVER_PROTOCOL.md documents
```

---

## 📞 Contact & Communication

| Communication Type | Method | Response Time |
|-------------------|--------|---------------|
| Urgent issue | Session message | < 15 min |
| Task assignment | TASK.md + message | < 1 hour |
| Code review | DEV_HANDOVER.md | < 4 hours |
| Normal question | Session message | < 24 hours |

---

## ✅ Checklist: Starting New Project

- [ ] Human submits requirements to pm_bot
- [ ] pm_bot creates SPEC.md
- [ ] Human reviews and approves SPEC
- [ ] pm_bot creates PROJECT_PLAN.md
- [ ] Human reviews and approves PLAN
- [ ] pm_bot creates project directory structure
- [ ] pm_bot creates first TASK.md
- [ ] dev_bot acknowledges and begins work
- [ ] Team follows standard workflow
- [ ] Final delivery via COMPLETION_REPORT.md

---

**Document Version:** 1.1  
**Last Updated:** 2026-03-21  
**Maintained by:** pm_bot  

_This index provides the complete documentation map for the AI Development Team. Refer to SYSTEM.md for full system architecture and HANDOVER_PROTOCOL.md for detailed procedures._
