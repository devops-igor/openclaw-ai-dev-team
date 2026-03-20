# AI Development Team for Golang

This workspace contains a specialized AI-assisted development team focused on Golang projects, featuring local model optimization for development tasks.

## Team Members

### 📋 Project Manager (pm_bot)
- **Role**: Orchestrator and coordinator
- **Model**: Flexible/OpenRouter (planning and coordination)
- **Responsibilities**: Task decomposition, delegation, progress tracking, reporting
- **Focus**: Ensuring smooth workflow between team members

### 💻 Lead Golang Developer (dev_bot)  
- **Role**: Primary implementation engineer
- **Model**: **ollama/qwen3-coder (local)** ✅ **SPECIFICALLY CONFIGURED**
- **Specialization**: Golang backend development, APIs, concurrency, local model utilization
- **Focus**: Writing clean, idiomatic, well-tested Go code using qwen3-coder
- **Advantage**: Local execution ensures privacy, reduces latency, and eliminates API costs for intensive coding tasks

### 🔍 Quality Gatekeeper & Bug Hunter (qa_bot)
- **Role**: Code auditor and quality assurance
- **Model**: Flexible/OpenRouter (analysis and review)
- **Specialization**: Security, correctness, best practices
- **Focus**: Finding bugs, ensuring quality, maintaining standards

## Workflow

1. **Planning** - PM breaks down requests into actionable tasks
2. **Development** - **Dev implements features using ollama/qwen3-coder** following Go standards
3. **Review** - QA audits for quality, security, and correctness  
4. **Iteration** - Feedback loop until approval
5. **Completion** - PM confirms "done-done" work

## Local Model Advantages for Development

The dev_bot's utilization of ollama/qwen3-coder provides:

### 🔒 **Privacy & Security**
- Code and prompts remain local
- No external API exposure
- Intellectual property protection

### ⚡ **Performance Benefits**
- Reduced latency (no network roundtrips)
- Consistent availability
- Faster iteration cycles

### 💰 **Cost Efficiency**
- Zero per-token API costs for development
- Unlimited usage for coding tasks
- Predictable operational expenses

### 🎯 **Task-Specific Optimization**
- Model specifically trained for code understanding and generation
- Strong performance on Golang development patterns
- Context awareness for complex implementations

## Getting Started

The team follows these principles:
- Clear communication through defined channels
- Golang best practices and idioms (enforced by qwen3-coder + qa_bot)
- Security-first mindset
- Comprehensive testing
- Continuous improvement

## Model Verification

To confirm the local model is available:
```bash
ollama list
# Should include: qwen3-coder
```

Check the individual agent folders (pm_bot/, dev_bot/, qa_bot/) for specific roles, responsibilities, and model configurations.
Shared configurations are in the shared/ directory.