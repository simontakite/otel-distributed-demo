"""
Manual OpenTelemetry SDK setup.
Fully environment-driven.
No hardcoded configuration.
"""

import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Function to set up tracing for the application
def setup_tracing(app):
    """
    Configure tracing for the service.
    All configuration is environment-driven (12-factor).
    """

    # Fetch the service name from the environment variable, default to "unknown-service"
    service_name = os.getenv("OTEL_SERVICE_NAME", "unknown-service")

    # Fetch the OTLP endpoint for exporting traces, default to "http://localhost:4318"
    otlp_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://localhost:4318"
    )

    # Fetch the sampling ratio for traces, default to 1.0 (always sample)
    sample_ratio = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0"))

    # Define the resource attributes for the service
    resource = Resource.create({
        "service.name": service_name,
        "service.version": os.getenv("SERVICE_VERSION", "1.0.0"),
        "deployment.environment": os.getenv("DEPLOYMENT_ENV", "dev"),
    })

    # Set up the sampler with a parent-based strategy and trace ID ratio-based sampling
    sampler = ParentBased(TraceIdRatioBased(sample_ratio))

    # Create a TracerProvider with the defined resource and sampler
    provider = TracerProvider(
        resource=resource,
        sampler=sampler,
    )

    # Set up the OTLP exporter with the endpoint for sending traces
    exporter = OTLPSpanExporter(
        endpoint=f"{otlp_endpoint}/v1/traces"
    )

    # Add a span processor to the provider for batch processing of spans
    provider.add_span_processor(BatchSpanProcessor(exporter))

    # Set the global tracer provider to the configured provider
    trace.set_tracer_provider(provider)

    # Automatically instrument FastAPI and Requests for tracing
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
