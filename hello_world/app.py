"""
Production-grade AWS Lambda function using AWS Lambda Powertools.

This module implements a serverless API with multiple endpoints for health checking,
file upload, and basic greeting functionality.
"""

from typing import Dict, Any
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

# Initialize Powertools components
app = APIGatewayRestResolver()
tracer = Tracer(service="HelloWorldAPI")
logger = Logger(service="HelloWorldAPI")
metrics = Metrics(namespace="HelloWorldAPI", service="HelloWorldAPI")


@app.get("/")
@tracer.capture_method
def root() -> Dict[str, Any]:
    """
    Root endpoint that returns a basic greeting.
    
    Returns:
        Dict[str, Any]: Response containing message and status
    """
    logger.info("Root endpoint called")
    metrics.add_metric(name="RootEndpointInvocations", unit=MetricUnit.Count, value=1)
    return {"message": "Hello World", "status": "ok"}


@app.get("/hello")
@tracer.capture_method
def hello() -> Dict[str, str]:
    """
    Hello endpoint that returns a simple greeting message.
    
    Returns:
        Dict[str, str]: Response containing hello world message
    """
    logger.info("Hello endpoint called")
    metrics.add_metric(name="HelloEndpointInvocations", unit=MetricUnit.Count, value=1)
    return {"message": "hello world"}


@app.post("/upload")
@tracer.capture_method
def upload() -> Dict[str, str]:
    """
    Upload endpoint placeholder for file upload functionality.
    
    Returns:
        Dict[str, str]: Response indicating upload API status
        
    Raises:
        BadRequestError: If request body is invalid
    """
    try:
        # Get the request body for processing
        request_body = app.current_event.body
        logger.info("Upload endpoint called", extra={"body_length": len(request_body) if request_body else 0})
        
        metrics.add_metric(name="UploadEndpointInvocations", unit=MetricUnit.Count, value=1)
        
        # Add basic validation
        if request_body and len(request_body) > 10 * 1024 * 1024:  # 10MB limit
            raise BadRequestError("Request body too large")
            
        return {"message": "Upload API - HTTP 200"}
        
    except Exception as e:
        logger.error("Upload endpoint error", extra={"error": str(e)})
        metrics.add_metric(name="UploadEndpointErrors", unit=MetricUnit.Count, value=1)
        raise


@app.get("/healthcheck")
@tracer.capture_method
def healthcheck() -> Dict[str, str]:
    """
    Health check endpoint for monitoring application status.
    
    Returns:
        Dict[str, str]: Response indicating service health status
    """
    # Add custom metrics
    metrics.add_metric(name="HealthcheckInvocations", unit=MetricUnit.Count, value=1)

    # Structured logging
    logger.info("Healthcheck API - HTTP 200")
    
    return {"message": "healthcheck", "status": "healthy"}


# Main Lambda handler with all Powertools decorators
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Args:
        event (Dict[str, Any]): API Gateway event
        context (LambdaContext): Lambda context object
        
    Returns:
        Dict[str, Any]: API Gateway response
    """
    try:
        logger.info("Lambda invocation started", extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name
        })
        
        response = app.resolve(event, context)
        
        logger.info("Lambda invocation completed successfully")
        return response
        
    except Exception as e:
        logger.error("Lambda handler error", extra={
            "error": str(e),
            "error_type": type(e).__name__,
            "request_id": context.aws_request_id
        })
        metrics.add_metric(name="LambdaHandlerErrors", unit=MetricUnit.Count, value=1)
        raise
