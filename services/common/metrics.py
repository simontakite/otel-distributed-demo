"""
Shared Prometheus RED metrics implementation.
Reusable across all services.
"""

import time
from prometheus_client import Counter, Histogram


# Total request counter
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "endpoint", "status"],
)

# Request duration histogram
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["service", "method", "endpoint"],
)

# Error counter
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["service", "endpoint"],
)


def record_request(service, method, endpoint, status):
    REQUEST_COUNT.labels(service, method, endpoint, status).inc()


def record_error(service, endpoint):
    ERROR_COUNT.labels(service, endpoint).inc()


def observe_latency(service, method, endpoint, start_time):
    REQUEST_LATENCY.labels(service, method, endpoint).observe(
        time.time() - start_time
    )
