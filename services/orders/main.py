import os
import time
import random
import requests
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from common.tracing import setup_tracing
from common.metrics import record_request, record_error, observe_latency

app = FastAPI()
setup_tracing(app)

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "orders-service")

PAYMENTS_SERVICE_URL = os.getenv(
    "PAYMENTS_SERVICE_URL",
    "http://payments-service"
)


@app.get("/create-order")
def create_order():
    start = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.3))

        response = requests.get(f"{PAYMENTS_SERVICE_URL}/charge")

        record_request(SERVICE_NAME, "GET", "/create-order", "200")

        return {
            "order": "created",
            "payment": response.json(),
        }

    except Exception:
        record_error(SERVICE_NAME, "/create-order")
        record_request(SERVICE_NAME, "GET", "/create-order", "500")
        raise

    finally:
        observe_latency(SERVICE_NAME, "GET", "/create-order", start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
