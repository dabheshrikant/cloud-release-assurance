# Cloud Release Assurance — Starter Project

A small FastAPI Orders service and starter test suite for practicing Cloud Delivery Assurance:
Docker → Kubernetes → CI tests → release gate.

## Prerequisites
- Python 3.11+ (for local development)
- Docker
- kubectl and a local Kubernetes cluster (kind, minikube, or an existing lab)
- Git

## 1. Run locally
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000/docs`.

In another terminal:
```bash
pip install -r requirements-dev.txt
pytest -v
```

## 2. Build and run with Docker
```bash
docker build -t cloud-release-assurance:0.1.0 .
docker run --rm -p 8000:8000 cloud-release-assurance:0.1.0
```
Test:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

## 3. Deploy to local Kubernetes
For a local cluster such as kind, load the image into the cluster if needed:
```bash
kind load docker-image cloud-release-assurance:0.1.0
kubectl apply -f k8s/
kubectl rollout status deployment/orders-api
kubectl get pods,svc
```
Open the service through port-forward:
```bash
kubectl port-forward svc/orders-api 8000:80
```
Then visit `http://localhost:8000/health`.

Note: The manifest uses `imagePullPolicy: IfNotPresent`. For a remote cluster, push the image to a registry and update the image reference.

## 4. Quality gate (starter)
```bash
python scripts/evaluate_gate.py examples/release-results-pass.json
python scripts/evaluate_gate.py examples/release-results-fail.json
```
Exit code is `0` for PASS and `1` for FAIL. The GitHub Actions workflow runs tests and uploads JUnit results; the next project task is to connect deployment validation and gate evaluation into a full promotion pipeline.

## Suggested next steps
1. Add API tests for invalid order payloads and unknown order IDs.
2. Publish the Docker image to GHCR or AWS ECR.
3. Add Helm charts and separate dev/staging values.
4. Make the pipeline deploy to a disposable Kubernetes environment.
5. Add failure evidence (pod description, logs, events) and a controlled rollback rehearsal.

This is a learning starter, not a production-ready release platform. Do not put credentials or secrets in the repository.
