# dev_bot Configuration

## Model Specification
- **Primary Model**: ollama/qwen3-coder (local)
- **Purpose**: Golang development, code generation, and implementation tasks
- **Reasoning**: Optimized for coding tasks, strong performance on development workloads

## Usage Guidelines
When dev_bot performs development tasks:
1. Use ollama/qwen3-coder for all code generation and implementation
2. Leverage model's strengths in understanding Golang syntax and patterns
3. Apply model's coding capabilities for:
   - Feature implementation
   - Test generation
   - Code refactoring
   - Bug fixes
   - Documentation generation

## Fallback Strategy
If local ollama/qwen3-coder is unavailable:
1. Check if model is properly installed and running
2. Verify Ollama service status
3. Escalate to pm_bot for manual intervention if needed

## Performance Considerations
- Token limits: Optimize prompts for efficiency
- Context window: Leverage for understanding larger code contexts
- Temperature: Use balanced settings for creativity vs consistency
- Stop sequences: Implement appropriate stopping conditions for code generation