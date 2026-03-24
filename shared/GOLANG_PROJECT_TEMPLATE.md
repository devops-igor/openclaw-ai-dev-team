# Standard Golang Project Template

This template defines the recommended structure for Golang projects that the AI development team will work on.

## Directory Structure
```
project-name/
├── cmd/                    # Main applications
│   └── app-name/           # Each app gets its own directory
│       └── main.go
├── internal/               # Private application and library code
│   ├── handlers/           # HTTP handlers
│   ├── services/           # Business logic
│   ├── repositories/       # Data access layer
│   └── middleware/         # Custom middleware
├── pkg/                    # Library code that's ok to export to external applications
├── api/                    # API definitions (OpenAPI/Swagger, protobuf, etc.)
├── configs/                # Configuration files
├── scripts/                # Automation scripts
├── test/                   # External test applications and test data
├── docs/                   # Documentation
├── configs/                # Configuration templates
├── deployments/            # Deployment manifests (K8s, Docker compose, etc.)
├── Makefile                # Build automation
├── go.mod                  # Go module definition
├── go.sum                  # Dependency checksums
├── main.go                 # Application entry point (for simple apps)
├── README.md               # Project documentation
└── WORKLOG.md              # Append-only action log (prevents context loss)
```

## Recommended Practices

### 1. Module Organization
- Use meaningful module paths (e.g., github.com/username/project)
- Keep main package minimal - delegate to internal packages
- Separate concerns clearly between layers

### 2. Dependency Management
- Go modules for versioning
- Regular dependency updates (`go get -u ./...`)
- Vendoring only when necessary

### 3. Build System
- Makefile for common tasks (build, test, lint, fmt)
- Dockerfile for containerization
- CI/CD pipeline integration points

### 4. Testing Strategy
- Unit tests in *_test.go files alongside code
- Integration tests in test/ directory
- Table-driven tests for complex logic
- Mock interfaces for external dependencies

### 5. Documentation
- Godoc comments for all exported functions
- README with setup and usage instructions
- API documentation where applicable
- Architecture decision records (ADRs) for significant choices

## Team Usage Guidelines

When the team creates a new Golang project:
1. PM_bot creates initial project structure based on this template
2. Dev_bot implements features following the structure
3. QA_bot reviews adherence to standards and identifies gaps
4. All agents maintain consistency with established patterns