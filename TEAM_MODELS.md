# AI Development Team Model Configuration

## Overview
This document specifies the language model usage for each agent in the AI development team.

## Model Assignments

### 👥 **Project Manager (pm_bot)**
- **Model**: ollama/minimax-m2.7:cloud (flexible for planning and coordination)
- **Purpose**: Task decomposition, planning, coordination, and reporting
- **Reasoning**: Benefits from broad knowledge for understanding requirements and breaking them down

### 👨‍💻 **Lead Golang Developer (dev_bot)**
- **Model**: **openrouter/xiaomi/mimo-v2-pro** ✅
- **Purpose**: Golang development, code generation, implementation
- **Reasoning**:
  - Advanced reasoning and coding capabilities
  - Cloud-based inference (no local GPU required)
  - Reliable availability
  - Strong performance on Golang patterns

### 🔍 **Quality Gatekeeper (qa_bot)**
- **Model**: **openrouter/xiaomi/mimo-v2-pro** ✅
- **Purpose**: Code review, security analysis, quality assessment
- **Reasoning**: Advanced reasoning capabilities for thorough code analysis and security scanning

## Model Specifications

### xiaomi/mimo-v2-pro (dev_bot & qa_bot)
- **Provider**: OpenRouter
- **Model Family**: Xiaomi Mimo V2 series
- **Specialization**: General purpose with strong coding and reasoning capabilities
- **Context Window**: 32768 tokens (estimated)
- **Advantages**:
  - Advanced reasoning for complex tasks
  - Strong code generation and review capabilities
  - Cloud-based inference (no local GPU required)
  - Reliable availability through OpenRouter
  - Good balance of performance and cost

## Usage Instructions

### For dev_bot Tasks:
All Golang development work should utilize xiaomi/mimo-v2-pro:
- Feature implementation
- Test generation
- Code refactoring
- Bug fixes
- Technical documentation
- Performance optimization

### For qa_bot Tasks:
All code review and QA work should utilize xiaomi/mimo-v2-pro:
- Security scanning
- Bug detection
- Code quality assessment
- Test coverage evaluation
- Performance review

### Verification:
To confirm the model is properly configured:
```bash
# Check OpenClaw config has the model registered
cat ~/.openclaw/openclaw.json | grep -A2 "xiaomi/mimo-v2-pro"
# Should show the model in the openrouter provider models list
```

### Model Switching:
If you need to change the model:
1. Update `dev_bot/AGENTS.md` or `qa_bot/AGENTS.md` with new model name
2. Update `openclaw.json` models array if adding new provider
3. Restart OpenClaw gateway to apply changes

## Benefits of Cloud Model for dev_bot & qa_bot

### Performance Advantages:
- Fast inference without local GPU requirements
- Consistent availability (cloud redundancy)
- Scalable compute resources on demand
- Advanced reasoning capabilities for complex tasks

### Cost Advantages:
- Pay-per-use model (no idle resource costs)
- No hardware investment required
- Predictable operational expenses based on usage

### Practical Advantages:
- No local GPU/RAM constraints
- Easy model updates and switching
- Access to advanced models with latest improvements
- Reliable availability for production use

## Team Coordination Notes

While both dev_bot and qa_bot use the same advanced cloud model, effective team collaboration requires:
- Clear communication of requirements and expectations
- Standardized output formats regardless of task
- Consistent quality standards across all agents
- Shared understanding of Golang best practices

Using the same model for both development and review ensures consistency in reasoning patterns and code understanding, leading to smoother handoffs and fewer misunderstandings.

## Configuration Files

| File | Purpose |
|------|---------|
| `openclaw.json` | Global model registry and provider configuration |
| `dev_bot/AGENTS.md` | dev_bot role definition with model specification |
| `dev_bot/SETTINGS.md` | Detailed model configuration and usage guidelines |
| `qa_bot/AGENTS.md` | qa_bot role definition with model specification |
| `qa_bot/SETTINGS.md` | Detailed model configuration and usage guidelines |
| `shared/TEAM_MODELS.md` | This document - team-wide model strategy |
