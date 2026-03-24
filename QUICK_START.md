# AI Development Team - Quick Start Guide

## 🚀 Getting Started

Your AI-assisted Golang development team is now ready to work! Here's how to use it effectively.

### 📁 **Team Structure Overview**
```
openclaw-ai-dev-team/
├── 👥 pm_bot/          # Project Manager - Orchestrator
├── 👥 dev_bot/         # Lead Golang Developer - Coder
├── 👥 qa_bot/          # Quality Gatekeeper - Reviewer & Security
├── 📁 shared/          # Common standards, templates, workflows
├── 📁 projects/        # Working directory for Golang projects
└── 📄 Documentation    # AGENTS.md, README.md, etc.
```

## 🔧 **How the Team Works**

### The Standard Workflow:
1. **Planning** - You describe what you want to build
2. **Decomposition** - pm_bot breaks it into actionable tasks
3. **Implementation** - dev_bot writes Golang code following standards
4. **Review** - qa_bot checks for quality, security, and correctness
5. **Iteration** - Feedback loop until QA approves
6. **Completion** - pm_bot confirms "done-done" and reports to you

### Communication Flow:
```
You (Human) 
    ↓ (Goals/Requirements)
pm_bot ←→ dev_bot ←→ qa_bot
    ↓              ↑
   Status       Feedback
    ↓              ↑
You ←─────── Reports ←───────
```

## 📋 **Using the Team for a New Project**

### Step 1: Define Your Requirements
Create a simple description of what you want to build:
```
"I need a REST API for managing user profiles with:
- CRUD operations (Create, Read, Update, Delete)
- JWT authentication
- PostgreSQL persistence
- Input validation and error handling
- Unit and integration tests"
```

### Step 2: Let pm_bot Decompose
The Project Manager will:
- Break down requirements into specific, actionable tasks
- Identify dependencies and implementation order
- Create a preliminary timeline
- Assign initial tasks to dev_bot

### Step 3: Watch dev_bot Implement
The Lead Developer will:
- Follow Golang best practices from shared/GOLANG_STANDARDS.md
- Use the project template from shared/GOLANG_PROJECT_TEMPLATE.md
- Write clean, tested, idiomatic Go code
- Implement features incrementally with frequent commits

### Step 4: Observe qa_bot Review
The Quality Gatekeeper will:
- Review code for security vulnerabilities
- Check adherence to Go idioms and conventions
- Validate test coverage and quality
- Identify potential bugs and performance issues
- Provide actionable feedback for improvement

### Step 5: Iterate to Completion
The team will cycle through implement→review→improve until:
- All requirements are met
- Code passes quality and security reviews
- Tests pass successfully
- Documentation is complete
- pm_bot confirms "done-done" work

## 💡 **Best Practices for Working With the Team**

### ✅ **Do:**
- Be specific about requirements and acceptance criteria
- Provide context about the project's purpose and users
- Ask clarifying questions when needed
- Review the team's progress regularly
- Provide feedback on what works well and what could improve

### ❌ **Don't:**
- Expect instant results on complex projects (quality takes time)
- Skip the review process (qa_bot's role is crucial)
- Ignore Golang standards (they exist for good reasons)
- Expect the team to know unspecified details
- Forget that iteration is part of quality development

## 📊 **Tracking Progress**

Check these files for team status:
- `shared/TEAM_STATUS.json` - Overall team capacity and sprint status
- `shared/STATUS_TEMPLATE.json` - Template for sprint/task tracking
- Individual agent folders for their current focus areas

## 📝 **WORKLOG - Preventing Memory Loss**

Every project includes a `WORKLOG.md` (append-only log). This prevents "memory loss" when the context window compacts.

**Why it matters:**
- Agents append entries for every major action, decision, and state change
- You can restart work and catch up by reading WORKLOG.md
- Complete project history is preserved for audits and onboarding

**Agents must log:**
- Task starts/completions
- Significant decisions (with rationale)
- Architecture changes
- Blockers and resolutions
- Reviews and test results
- Handoffs and meetings

**Format:** `YYYY-MM-DD HH:MM | AGENT | ACTION_TYPE | DESCRIPTION`

**Responsibility:** It's part of the Definition of Done for every task. No worklog entry means the work isn't done.

See `shared/WORKLOG_TEMPLATE.md` for full guidelines and examples.

## 🛠️ **Extending the Team**

As you work with the team, you might want to add:

### New Agent Types:
- **docs_bot** - Technical documentation specialist
- **devops_bot** - Deployment and infrastructure expert
- **data_bot** - Database and data engineering specialist
- **ux_bot** - User experience and interface designer

### Enhanced Capabilities:
- Custom workflows for specific project types
- Advanced monitoring and metrics
- Integration with external tools (Jira, GitHub, Slack, etc.)
- Specialized Golang domains (microservices, CLI tools, web services)

## 🎯 **First Project Suggestion**

Try starting with a small, well-defined project to validate the workflow:
- A CLI tool for a specific task
- A simple REST API with one resource
- A library for a common Golang pattern
- A tool that solves a personal productivity problem

This lets you see how the team collaborates before tackling larger, more complex projects.

---

**Ready to start?** Just describe what you'd like to build, and your AI development team will begin working on it using Golang best practices and quality-first development principles!

**Current Working Directory:** `C:\Users\Igor\OpenClaw\openclaw-ai-dev-team`