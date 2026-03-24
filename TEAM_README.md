# AI Development Team for Golang

This workspace contains a specialized AI-assisted development team focused on Golang projects, featuring cloud-based model utilization for development tasks.

## Team Members

### 📋 Project Manager (pm_bot)
- **Role**: Orchestrator and coordinator
- **Model**: minimax-m2.7:cloud (flexible for planning and coordination)
- **Responsibilities**: Task decomposition, delegation, progress tracking, reporting
- **Focus**: Ensuring smooth workflow between team members

### 💻 Lead Golang Developer (dev_bot)
- **Role**: Primary implementation engineer
- **Model**: **openrouter/xiaomi/mimo-v2-pro** ✅ **CONFIGURED**
- **Specialization**: Golang backend development, APIs, concurrency, advanced reasoning
- **Focus**: Writing clean, idiomatic, well-tested Go code using xiaomi/mimo-v2-pro
- **Advantage**: Cloud-based advanced AI with strong coding capabilities, no local GPU required

### 🔍 Quality Gatekeeper & Bug Hunter (qa_bot)
- **Role**: Code auditor and quality assurance
- **Model**: **openrouter/xiaomi/mimo-v2-pro** ✅ **CONFIGURED**
- **Specialization**: Security, correctness, best practices
- **Focus**: Finding bugs, ensuring quality, maintaining standards

## Workflow

1. **Planning** - PM breaks down requests into actionable tasks
2. **Development** - **Dev implements features using xiaomi/mimo-v2-pro** following Go standards
3. **Review** - QA audits for quality, security, and correctness
4. **Iteration** - Feedback loop until approval
5. **Completion** - PM confirms "done-done" work

## Cloud Model Advantages for Development

The dev_bot's utilization of xiaomi/mimo-v2-pro via OpenRouter provides:

### ⚡ **Performance Benefits**
- Advanced reasoning capabilities for complex code
- No local GPU requirements
- Scalable compute resources on demand
- Reliable availability through cloud infrastructure

### 💰 **Cost Efficiency**
- Pay-per-use pricing (no idle resource costs)
- No hardware investment required
- Access to state-of-the-art models without maintenance

### 🎯 **Advanced Capabilities**
- Strong code generation and understanding
- Excellent handling of Go idioms and patterns
- Large context window for complex codebases
- Continuous model improvements from provider

### 🔧 **Ease of Use**
- No local installation or configuration
- Automatic updates and improvements
- Simple API integration through OpenRouter
- Consistent performance across environments

## Getting Started

The team follows these principles:
- Clear communication through defined channels
- Golang best practices and idioms (enforced by xiaomi/mimo-v2-pro + qa_bot)
- Security-first mindset
- Comprehensive testing
- Continuous improvement

## Model Verification

To confirm the model is properly configured:
```bash
# Check OpenClaw config has the model registered
cat ~/.openclaw/openclaw.json | grep -A2 "xiaomi/mimo-v2-pro"
# Should show the model in the openrouter provider models list
```

Check the individual agent folders (pm_bot/, dev_bot/, qa_bot/) for specific roles, responsibilities, and model configurations.
Shared configurations are in the shared/ directory.
