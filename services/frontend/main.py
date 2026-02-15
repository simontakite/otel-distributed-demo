"""
Frontend Service

Responsibilities:
- Entry point of system
- Calls orders-service
- Emits traces
- Emits RED metrics
"""

import os
import time
import random
import requests
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from common.tracing import setup_tracing
from common.metrics import (
    record_request,
    record_error,
    observe_latency,
)

app = FastAPI()
setup_tracing(app)

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "frontend-service")

ORDERS_SERVICE_URL = os.getenv(
    "ORDERS_SERVICE_URL",
    "http://orders-service"
)


@app.get("/checkout")
def checkout():
    start = time.time()

    try:
        time.sleep(random.uniform(0.05, 0.2))

        response = requests.get(f"{ORDERS_SERVICE_URL}/create-order")

        record_request(SERVICE_NAME, "GET", "/checkout", "200")

        return {
            "checkout": "complete",
            "order": response.json(),
        }

    except Exception:
        record_error(SERVICE_NAME, "/checkout")
        record_request(SERVICE_NAME, "GET", "/checkout", "500")
        raise

    finally:
        observe_latency(SERVICE_NAME, "GET", "/checkout", start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
