# otel-distributed-demo
Opentelemetry distributed microservice tracing with LGTM.

## From repo root:
docker build -f services/orders/Dockerfile -t absolootly/orders:latest .
docker build -f services/payments/Dockerfile -t absolootly/payments:latest .
docker build -f services/frontend/Dockerfile -t absolootly/frontend:latest .

## Docker push
docker push absolootly/orders:latest 
docker push absolootly/payments:latest 
docker push absolootly/frontend:latest

## K8s deploy

## Load testing
k6 run k6/loadtest.js