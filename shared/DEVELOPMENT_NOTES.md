# Development Team Notes - Model Usage

## Cloud-Based Model Configuration

The AI development team uses cloud-based models via OpenRouter for flexibility and advanced capabilities:

### 🎯 **Specialized Cloud Model for Development**
- **Agent**: dev_bot (Lead Golang Developer)
- **Model**: openrouter/xiaomi/mimo-v2-pro
- **Purpose**: High-quality Golang implementation, testing, and code generation

### 🔄 **Unified Model for Review**
- **Agent**: qa_bot (Quality Gatekeeper)
- **Model**: openrouter/xiaomi/mimo-v2-pro
- **Purpose**: Code review, security analysis, and quality assessment

### 📋 **Flexible Model for Coordination**
- **Agent**: pm_bot (Project Manager)
- **Model**: openrouter/minimax-m2.7:cloud (or similar flexible model)
- **Purpose**: Planning, coordination, and reporting

## Benefits of This Approach

### For Development and Review (dev_bot + qa_bot):
1. **Advanced Capabilities**: State-of-the-art models with strong reasoning
2. **No Local Hardware**: No need for powerful GPUs or local installations
3. **Scalability**: Cloud resources scale to demand
4. **Consistency**: Same model across development and review ensures shared understanding
5. **Cost Control**: Pay-per-use with no idle resource costs
6. **Always Updated**: Provider maintains models with latest improvements

### For Coordination (pm_bot):
1. **Flexibility**: General-purpose model adapts to various planning tasks
2. **Reliability**: Cloud redundancy ensures availability
3. **Easy Switching**: Can change models without local setup

## Implementation Details

### Model Verification
Before starting work, verify the models are properly configured:
```bash
# For PowerShell:
.\validate_models.ps1

# For Bash:
./validate_models.sh

# Or manually check openclaw.json:
cat ~/.openclaw/openclaw.json | grep -A5 "xiaomi/mimo-v2-pro"
```

### Configuration
Ensure `openclaw.json` includes the model under OpenRouter provider:
```json
{
  "models": {
    "providers": {
      "openrouter": {
        "models": [
          {
            "id": "xiaomi/mimo-v2-pro",
            "name": "Xiaomi Mimo V2 Pro",
            "contextWindow": 32768,
            "input": ["text"]
          }
        ]
      }
    }
  }
}
```

### Usage in Workflows
All Golang development work performed by dev_bot should explicitly utilize xiaomi/mimo-v2-pro for:
- Feature implementation from specifications
- Test generation (unit, integration, table-driven)
- Code refactoring and optimization
- Bug identification and fixing
- Technical documentation generation
- Performance analysis and improvement

All code review work performed by qa_bot should utilize the same model for consistency.

### Fallback Procedures
If the primary model becomes unavailable:
1. Check OpenRouter API status and account balance
2. Verify API key configuration in openclaw.json
3. Fall back to openrouter/stepfun/step-3.5-flash:free if available
4. Escalate to pm_bot for manual intervention if needed
5. Document any workaround in project notes

## Best Practices for Cloud Model Usage

### Prompt Engineering
- Be specific about Golang requirements and constraints
- Reference shared/GOLANG_STANDARDS.md for guidance
- Provide clear context about existing codebase structure
- Specify desired output format (e.g., "complete Go file", "function only")
- Leverage the large context window for broader code understanding

### Context Management
- Use the model's full context window for understanding larger code sections
- Break complex tasks into smaller, manageable pieces when appropriate
- Use iterative refinement for sophisticated implementations
- Include relevant code snippets and documentation in prompts

### Quality Assurance
- All code from dev_bot undergoes review by qa_bot
- Cloud model usage does not bypass quality gates
- Standards compliance verified through shared/GOLANG_STANDARDS.md
- Security review performed regardless of generation source
- Consistency between dev and QA models improves review accuracy

## Cost Optimization

### Token Usage Awareness
- Be mindful of context window usage (32K tokens)
- Use concise but complete prompts
- Avoid unnecessary repetition in conversations

### Monitoring
- Track OpenRouter usage and costs periodically
- Set up alerts for unusual spending
- Consider using smaller/faster models for routine tasks if needed

## Troubleshooting Guide

### Common Issues & Solutions

**Problem**: "model not found" or "invalid model" error
**Solution**:
- Verify the model ID is exactly "openrouter/xiaomi/mimo-v2-pro"
- Check that your OpenRouter account has access to this model
- Ensure openclaw.json is properly formatted and OpenClaw restarted

**Problem**: API rate limits or quota exceeded
**Solution**:
- Check your OpenRouter account balance and limits
- Implement retry logic with exponential backoff
- Consider upgrading your OpenRouter plan if needed

**Problem**: Slow response times
**Solution**:
- Check your network connectivity
- Consider that cloud models may have variable latency
- Use a faster fallback model for time-critical tasks

**Problem**: Poor code quality output
**Solution**:
- Improve prompt specificity
- Provide more context and examples
- Break down complex tasks into smaller steps
- Consider that model may need more detailed requirements

**Problem**: OpenRouter API key invalid
**Solution**:
- Verify the API key in `~/.openclaw/openclaw.json`
- Ensure the key has necessary permissions
- Generate a new key from OpenRouter dashboard if needed

## Team Coordination with Unified Model

Using the same model for both development and review enhances collaboration:

### Shared Understanding
- Both dev_bot and qa_bot are familiar with the model's strengths and weaknesses
- Consistent code style and pattern recognition
- Easier communication about implementation details

### Predictable Output
- Code generation and review use similar reasoning patterns
- Fewer misunderstandings due to model-specific quirks
- Smoother handoffs between development and review

### Efficient Iterations
- Feedback from qa_bot is more likely to be actionable for dev_bot
- Less back-and-forth needed to clarify review comments
- Faster resolution of issues

This approach ensures that while we leverage cloud capabilities, the team maintains cohesive, high-quality collaboration throughout the development lifecycle.
