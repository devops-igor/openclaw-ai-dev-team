# Example CLI

A simple command-line interface built by the AI development team to demonstrate the workflow.

## Usage

```bash
# Build the CLI
go build -o example-cli ./cmd/example-cli

# Run commands
./example-cli hello
./example-cli version
```

## Project Structure

This project follows the standard Golang structure recommended for AI dev team projects:
- `cmd/` - Contains the main application entry points
- `go.mod` - Go module definition
- The team would extend this with additional packages in `internal/` and `pkg/` as needed

## AI Development Team Notes

This serves as a starting point for demonstrating how the team collaborates:
1. **PM_bot** would receive feature requests and break them into tasks
2. **Dev_bot** would implement new features (adding commands, improving functionality)
3. **QA_bot** would review code for quality, security, and adherence to Go standards
4. The team would iterate until QA approves, then PM confirms completion