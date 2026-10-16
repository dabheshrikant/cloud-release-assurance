# Kubernetes notes

This manifest is intended for a local learning cluster. If you use an existing multi-node cluster, ensure the image is available to every node or publish it to a registry and update `image` in `deployment.yaml`.

Apply:
```bash
kubectl apply -f k8s/
kubectl rollout status deployment/orders-api
kubectl port-forward svc/orders-api 8000:80
```
