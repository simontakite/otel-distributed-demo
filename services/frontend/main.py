from fastapi import FastAPI
import requests
import random
import time
from common.tracing import setup_tracing

app = FastAPI()
setup_tracing(app, "frontend-service")

ORDERS_URL = "http://orders-service/create-order"

@app.get("/checkout")
def checkout():
    time.sleep(random.uniform(0.05, 0.2))
    response = requests.get(ORDERS_URL)
    return {
        "checkout": "complete",
        "order": response.json()
    }
