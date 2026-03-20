# Development Team Notes - Model Usage

## Local Model Optimization for Development

The AI development team employs a strategic model assignment approach:

### 🎯 **Specialized Local Model for Development**
- **Agent**: dev_bot (Lead Golang Developer)
- **Model**: ollama/qwen3-coder (local execution)
- **Purpose**: Optimized Golang implementation, testing, and code generation

### 🔄 **Flexible Models for Coordination & Review**
- **Agents**: pm_bot (Project Manager), qa_bot (Quality Gatekeeper)
- **Model**: Flexible/OpenRouter (general purpose)
- **Purpose**: Planning, coordination, analysis, and review

## Benefits of This Approach

### For Development Tasks (dev_bot + qwen3-coder):
1. **Privacy**: Code and prompts remain entirely local
2. **Performance**: Low latency, high throughput for coding tasks
3. **Cost**: Eliminates per-token API costs during intensive development
4. **Specialization**: Model specifically trained for code understanding
5. **Reliability**: Independent of external service availability

### For Coordination & Review (pm_bot/qa_bot + flexible models):
1. **Breadth**: Broad knowledge for understanding requirements and identifying issues
2. **Flexibility**: Adaptable to various coordination and analysis tasks
3. **Consistency**: Stable behavior for process-oriented work

## Implementation Details

### Model Verification
Before starting work, verify the local model is available:
```bash
ollama list | findstr qwen3-coder
```

### Model Installation (if needed)
```bash
ollama pull qwen3-coder
```

### Usage in Workflows
All Golang development work performed by dev_bot should explicitly utilize the local ollama/qwen3-coder model for:
- Feature implementation from specifications
- Test generation (unit, integration, table-driven)
- Code refactoring and optimization
- Bug identification and fixing
- Technical documentation generation
- Performance analysis and improvement

### Fallback Procedures
If the local model becomes unavailable:
1. Check Ollama service status: `ollama serve`
2. Verify model installation: `ollama list`
3. Reinstall if necessary: `ollama pull qwen3-coder`
4. Notify pm_bot for coordination of alternatives
5. Document any workaround in project notes

## Best Practices for Local Model Usage

### Prompt Engineering
- Be specific about Golang requirements and constraints
- Reference shared/GOLANG_STANDARDS.md for guidance
- Provide clear context about existing codebase structure
- Specify desired output format (e.g., "complete Go file", "function only")

### Context Management
- Leverage the model's context window for understanding larger code sections
- Break complex tasks into smaller, manageable pieces when needed
- Use iterative refinement for sophisticated implementations

### Quality Assurance
- All code from dev_bot undergoes review by qa_bot
- Local model usage does not bypass quality gates
- Standards compliance verified through shared/GOLANG_STANDARDS.md
- Security review performed regardless of generation source

## Troubleshooting Guide

### Common Issues & Solutions

**Problem**: "model not found" error
**Solution**: 
```powershell
ollama pull qwen3-coder
```

**Problem**: Slow response times
**Solution**:
- Check system resources (RAM/VRAM usage)
- Consider model quantization options
- Verify Ollama is using appropriate hardware acceleration

**Problem**: Poor code quality
**Solution**:
- Review and refine prompts for specificity
- Ensure adequate context is provided
- Verify understanding of Go idioms and best practices
- Leverage qa_bot review for quality assurance

**Problem**: Service not responding
**Solution**:
```powershell
# Restart Ollama service
net stop ollama
net start ollama
# or
ollama serve
```

## Team Coordination with Mixed Models

Despite using different models, effective collaboration requires:

### Consistent Communication
- Clear, specific requirements from human to pm_bot
- Well-defined tasks from pm_bot to dev_bot
- Specific, actionable feedback from qa_bot to dev_bot
- Regular status updates from pm_bot to human

### Shared Standards
All agents reference the same:
- Golang coding standards (shared/GOLANG_STANDARDS.md)
- Project templates (shared/GOLANG_PROJECT_TEMPLATE.md)
- Workflow definitions (shared/WORKFLOW.md)
- Quality criteria (defined in WORKFLOW.md)

### Output Format Consistency
Regardless of model used, agents should produce:
- Well-structured, readable outputs
- Actionable, specific feedback
- Clear indication of completion status
- Proper formatting for easy consumption by other agents

This approach ensures that while dev_bot benefits from local model optimization for development tasks, the team maintains cohesive, high-quality collaboration throughout the development lifecycle.