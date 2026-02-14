from fastapi import FastAPI
import requests
import random
import time
from common.tracing import setup_tracing

app = FastAPI()
setup_tracing(app, "orders-service")

PAYMENTS_URL = "http://payments-service/charge"

@app.get("/create-order")
def create_order():
    time.sleep(random.uniform(0.1, 0.3))
    response = requests.get(PAYMENTS_URL)
    return {
        "order": "created",
        "payment": response.json()
    }
