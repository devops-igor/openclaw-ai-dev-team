# AI Development Team Model Configuration

## Overview
This document specifies the language model usage for each agent in the AI development team.

## Model Assignments

### 👥 **Project Manager (pm_bot)**
- **Model**: Default/OpenRouter (flexible for planning and coordination)
- **Purpose**: Task decomposition, planning, coordination, and reporting
- **Reasoning**: Benefits from broad knowledge for understanding requirements and breaking them down

### 👨‍💻 **Lead Golang Developer (dev_bot)**
- **Model**: **ollama/qwen3-coder (local)** ✅ **SPECIFICALLY REQUESTED**
- **Purpose**: Golang development, code generation, implementation
- **Reasoning**: 
  - Specifically optimized for coding tasks
  - Strong performance on development workloads
  - Local execution for privacy and reduced latency
  - Cost-effective for intensive coding tasks
  - Excellent Golang language understanding

### 🔍 **Quality Gatekeeper (qa_bot)**
- **Model**: Default/OpenRouter (flexible for analysis and review)
- **Purpose**: Code review, security analysis, quality assessment
- **Reasoning**: Benefits from broad knowledge for identifying diverse issues and best practices

## Local Model Specification

### ollama/qwen3-coder Details
- **Provider**: Ollama (local execution)
- **Model Family**: Qwen3 series
- **Specialization**: Coding and development tasks
- **Advantages**:
  - Local execution (data privacy)
  - No API costs for intensive usage
  - Reduced latency
  - Optimized for code understanding and generation
  - Strong performance on programming benchmarks

## Usage Instructions

### For dev_bot Tasks:
All Golang development work should utilize the local ollama/qwen3-coder model including:
- Feature implementation
- Test generation
- Code refactoring
- Bug fixes
- Technical documentation
- Performance optimization

### Verification:
To confirm the model is available locally:
```bash
ollama list
# Should show: qwen3-coder
```

### Troubleshooting:
If model is not available:
1. Install with: `ollama pull qwen3-coder`
2. Ensure Ollama service is running
3. Check system resources (RAM/VRAM requirements)
4. Escalate to pm_bot if persistent issues

## Benefits of Local Model for dev_bot

### Performance Advantages:
- Faster iteration cycles (no network latency)
- Consistent availability (no service downtime)
- Predictable performance characteristics

### Cost Advantages:
- No per-token API costs
- Unlimited usage for development tasks
- Fixed infrastructure cost only

### Privacy Advantages:
- Code remains local
- No external API exposure
- Intellectual property protection
- Compliance with data locality requirements

## Team Coordination Notes

While dev_bot uses a specialized local model, effective team collaboration requires:
- Clear communication of requirements and expectations
- Standardized output formats regardless of model used
- Consistent quality standards across all agents
- Shared understanding of Golang best practices

The mixed-model approach (local specialized + general flexible) optimizes both performance and collaboration effectiveness.