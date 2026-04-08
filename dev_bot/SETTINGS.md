# dev_bot Configuration

## Model Specification
- **Provider**: OpenRouter
- **Primary Model**: openrouter/xiaomi/mimo-v2-pro
- **Purpose**: Golang development, code generation, and implementation tasks
- **Reasoning**: Advanced model for higher quality code generation, better reasoning, and comprehensive testing

## Model Details
- **Context Window**: 32768 tokens (estimated)
- **Reasoning**: true (advanced reasoning)
- **Cost**: Check OpenRouter pricing for current rates

## Usage Guidelines
When dev_bot performs development tasks:
1. Use openrouter/xiaomi/mimo-v2-pro for all code generation and implementation
2. Apply capabilities for:
   - Feature implementation
   - Test generation
   - Code refactoring
   - Bug fixes
   - Documentation generation
3. Ensure high-quality output with thorough reasoning

## Model Features
- Cloud-based inference via OpenRouter
- Strong reasoning capabilities
- Best-in-class for code generation and analysis
- Suitable for complex development tasks

## Fallback Strategy
If xiaomi/mimo-v2-pro is unavailable:
1. Check OpenRouter API status
2. Verify API key configuration
3. Fall back to openrouter/stepfun/step-3.5-flash:free if available
4. Escalate to pm_bot for manual intervention if needed
