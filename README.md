# otel-distributed-demo
Opentelemetry distributed microservice tracing with LGTM.

## From repo root:
docker build -f services/orders/Dockerfile -t orders:latest .
docker build -f services/payments/Dockerfile -t payments:latest .
docker build -f services/frontend/Dockerfile -t frontend:latest .