import os
import time
import random
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from common.tracing import setup_tracing
from common.metrics import record_request, record_error, observe_latency

app = FastAPI()
setup_tracing(app)

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "payments-service")


@app.get("/charge")
def charge():
    start = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.4))

        if random.random() < 0.1:
            raise RuntimeError("Payment failed")

        record_request(SERVICE_NAME, "GET", "/charge", "200")

        return {"status": "charged"}

    except Exception:
        record_error(SERVICE_NAME, "/charge")
        record_request(SERVICE_NAME, "GET", "/charge", "500")
        raise

    finally:
        observe_latency(SERVICE_NAME, "GET", "/charge", start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
