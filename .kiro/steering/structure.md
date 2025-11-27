# Project Structure & Organization

## Directory Layout

```
├── .github/workflows/          # CI/CD pipeline configuration
│   └── deploy.yml             # GitHub Actions deployment workflow
├── .kiro/steering/            # AI assistant steering rules
├── events/                    # SAM local test events
│   ├── default.json          # Default API Gateway event
│   ├── healthcheck.json      # Health check endpoint test
│   ├── hello.json           # Hello endpoint test
│   └── upload.json          # Upload endpoint test
├── hello_world/              # Main application code
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Lambda handler and API endpoints
│   └── requirements.txt     # Runtime dependencies
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   │   ├── __init__.py     # Test package initialization
│   │   └── test_handler.py # Comprehensive endpoint tests
│   └── requirements.txt     # Test dependencies
├── template.yaml            # SAM infrastructure template
├── samconfig.toml          # SAM deployment configuration
├── pytest.ini             # Test configuration
├── mypy.ini               # Type checking configuration
├── renovate.json          # Dependency update automation
└── README.md             # Project documentation
```

## Code Organization Patterns

### Lambda Function Structure
- **Single handler file**: `hello_world/app.py` contains all endpoint logic
- **Powertools integration**: Standard decorators for logging, tracing, and metrics
- **API Gateway REST resolver**: Route-based endpoint handling
- **Type hints**: All functions must include proper type annotations

### Test Organization
- **Unit tests only**: Located in `tests/unit/`
- **Comprehensive coverage**: Minimum 95% code coverage required
- **Test classes**: Organized by functionality (endpoints, error handling, integration, performance)
- **Mock fixtures**: Reusable Lambda context and API Gateway event fixtures

### Configuration Files
- **Infrastructure**: `template.yaml` defines all AWS resources
- **Deployment**: `samconfig.toml` manages deployment parameters
- **Testing**: `pytest.ini` enforces coverage and test standards
- **Code quality**: `mypy.ini` enables strict type checking

## Naming Conventions

### Files and Directories
- **Snake case**: All Python files use snake_case naming
- **Descriptive names**: Files clearly indicate their purpose
- **Test prefixes**: Test files start with `test_`

### Python Code
- **Functions**: snake_case for all function names
- **Classes**: PascalCase for class names (e.g., `MockLambdaContext`)
- **Constants**: UPPER_CASE for constants and environment variables
- **Type hints**: Required for all function parameters and return values

### AWS Resources
- **Stack naming**: Uses stack name prefix for uniqueness
- **Resource tags**: All resources tagged with Service and Environment
- **Logical IDs**: PascalCase CloudFormation logical IDs

## Import Organization

Standard import order in Python files:
```python
# 1. Standard library imports
from typing import Dict, Any, Union, cast

# 2. Third-party imports
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
# ... other powertools imports

# 3. Local imports (if any)
# from .utils import helper_function
```

## Event Test Files

Test events in `events/` directory follow API Gateway event structure:
- **Consistent format**: All events use standard API Gateway REST format
- **Realistic data**: Events contain realistic headers and request context
- **Endpoint specific**: Each endpoint has its own test event file

## Documentation Standards

- **Docstrings**: All functions require comprehensive docstrings
- **Type documentation**: Parameters and return types documented
- **README**: Comprehensive project documentation with examples
- **Comments**: Inline comments for complex business logic only

## File Size Guidelines

- **Single responsibility**: Each file should have a clear, single purpose
- **Reasonable size**: Lambda handler file should remain under 500 lines
- **Test organization**: Test files can be larger but should be well-organized with clear class structure

## Dependencies Management

- **Separate requirements**: Runtime (`hello_world/`) and test (`tests/`) dependencies separated
- **Version pinning**: All dependencies use minimum version constraints
- **Security updates**: Renovate.json configured for automated security updates
- **Minimal dependencies**: Only include necessary packages to reduce cold start time