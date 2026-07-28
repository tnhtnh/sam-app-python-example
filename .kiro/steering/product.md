# Product Overview

## Hello World API

A production-grade serverless REST API built with AWS SAM (Serverless Application Model) that demonstrates best practices for serverless architecture, observability, and deployment.

## Core Functionality

The API provides four main endpoints:
- **Root (`/`)**: Basic greeting with status information
- **Hello (`/hello`)**: Simple hello world message
- **Health Check (`/healthcheck`)**: Service health monitoring endpoint
- **Upload (`/upload`)**: File upload placeholder with size validation (10MB limit)

## Key Features

- **Comprehensive Observability**: Structured logging, custom metrics, and distributed tracing using AWS Lambda Powertools
- **Production-Ready Monitoring**: CloudWatch alarms for errors and performance metrics
- **Error Handling**: Global exception handling with proper HTTP status codes
- **Security**: Input validation, request size limits, and principle of least privilege IAM
- **Testing**: 100% test coverage with unit, integration, and performance tests
- **CI/CD**: Automated testing, security scanning, and deployment pipeline

## Architecture

Built on AWS serverless services:
- **AWS Lambda**: Python 3.13 runtime with 256MB memory, 30-second timeout
- **API Gateway**: RESTful API with CORS support
- **CloudWatch**: Logging, metrics, and monitoring
- **X-Ray**: Distributed tracing
- **SQS**: Dead letter queue for failed invocations

## Target Use Cases

This application serves as a reference implementation for:
- Serverless API development best practices
- AWS Lambda Powertools integration
- Production-ready monitoring and observability
- Automated testing and deployment patterns
- Security and performance optimization