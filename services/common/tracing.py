from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

ALLOY_ENDPOINT = "http://monitoring-grafana-alloy.monitoring.svc.cluster.local:4318/v1/traces"

def setup_tracing(app, service_name: str):
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0"
    })

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=ALLOY_ENDPOINT)
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
