from fastapi import FastAPI
import random
import time
from common.tracing import setup_tracing

app = FastAPI()
setup_tracing(app, "payments-service")

@app.get("/charge")
def charge():
    time.sleep(random.uniform(0.1, 0.4))
    if random.random() < 0.1:
        raise RuntimeError("Payment failed")
    return {"status": "charged"}
