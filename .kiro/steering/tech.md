# Technology Stack & Build System

## Core Technologies

### Runtime & Language
- **Python 3.13**: Latest Python runtime with type hints required
- **AWS Lambda**: Serverless compute platform
- **AWS SAM**: Infrastructure as Code and local development

### Key Dependencies
- **AWS Lambda Powertools**: Observability framework (`aws-lambda-powertools[all]>=2.34.1`)
- **Boto3**: AWS SDK for Python (`boto3>=1.34.0`)
- **Requests**: HTTP library (`requests>=2.31.0`)

### Development Tools
- **pytest**: Testing framework with coverage reporting
- **mypy**: Static type checking (strict mode enabled)
- **black**: Code formatting (88 character line length)
- **flake8**: Linting and style checking
- **bandit**: Security vulnerability scanning

## Build System

### SAM CLI Commands

```bash
# Build application (containerized for consistency)
sam build --use-container --cached

# Local development server
sam local start-api
# API available at http://127.0.0.1:3000

# Invoke specific function with test event
sam local invoke HelloWorldFunction --event events/hello.json

# Deploy to AWS
sam deploy --guided  # First time
sam deploy           # Subsequent deployments

# View logs
sam logs -n HelloWorldFunction --stack-name cursor-sam-app-python-example --tail
```

### Testing Commands

```bash
# Run all tests with coverage (minimum 95% required)
pytest tests/unit --cov=hello_world --cov-report=html --cov-report=term

# Run specific test class
pytest tests/unit/test_handler.py::TestHelloWorldEndpoints -v

# Type checking
mypy hello_world/

# Code formatting
black hello_world/ tests/

# Linting
flake8 hello_world/ tests/ --max-line-length=88

# Security scanning
bandit -r hello_world/ -f json -o bandit-report.json
```

### Development Workflow

```bash
# Install dependencies
pip install -r hello_world/requirements.txt
pip install -r tests/requirements.txt

# Development cycle
sam build --use-container
sam local start-api  # Terminal 1
# Make changes, test endpoints
pytest tests/unit --cov=hello_world  # Terminal 2
```

## Configuration Files

- **template.yaml**: SAM infrastructure template
- **samconfig.toml**: SAM deployment configuration
- **pytest.ini**: Test configuration with coverage requirements
- **mypy.ini**: Type checking configuration (strict mode)
- **renovate.json**: Automated dependency updates

## AWS Lambda Powertools Integration

All functions use the standard Powertools decorators:
```python
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    # Handler implementation
```

## Environment Variables

Standard Powertools environment variables are configured globally:
- `POWERTOOLS_SERVICE_NAME`: HelloWorldAPI
- `POWERTOOLS_METRICS_NAMESPACE`: HelloWorldAPI
- `POWERTOOLS_LOG_LEVEL`: INFO
- `POWERTOOLS_TRACER_CAPTURE_RESPONSE`: true
- `POWERTOOLS_TRACER_CAPTURE_ERROR`: true