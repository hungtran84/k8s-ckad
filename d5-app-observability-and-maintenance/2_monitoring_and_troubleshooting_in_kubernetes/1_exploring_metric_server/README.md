# Lab: Installing Metrics Server in Kubernetes and Exploring Metrics

## Objectives
In this lab, you will:
- Install the Metrics Server in a Kubernetes cluster.
- Explore the Metrics Server to understand its functionality.
- Use `kubectl top` to view CPU and memory usage for nodes and pods.

## Steps

### 1. Prerequisites
- A running Kubernetes cluster (e.g., Minikube, GKE, or kubeadm-based cluster).
- `kubectl` installed and configured to communicate with the cluster.

### 2. Install the Metrics Server
1. Apply the Metrics Server manifest:
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   ```
2. Verify that the Metrics Server pods are running:
   ```bash
   kubectl get pods -n kube-system
   ```
   Look for a pod named `metrics-server` and ensure its status is `Running`.

### 3. Explore Metrics Server
1. Check if the Metrics Server is working correctly:
   ```bash
   kubectl get apiservices | grep metrics
   ```
   Ensure that the status of the `v1beta1.metrics.k8s.io` service is `True`.

2. Confirm metrics are being served:
   ```bash
   kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes" | jq .
   ```
   *(Optional)* Install `jq` if not available, or read the raw JSON response.

### 4. Use `kubectl top` to View Metrics
1. View node-level resource usage:
   ```bash
   kubectl top nodes
   ```
   Example output:
   ```
   NAME          CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
   node-1        250m         12%    1024Mi          50%
   ```

2. View pod-level resource usage in a namespace:
   ```bash
   kubectl top pods -n <namespace>
   ```
   Replace `<namespace>` with the desired namespace (e.g., `default`).

   Example output:
   ```
   NAME            CPU(cores)   MEMORY(bytes)
   my-app-pod      150m         256Mi
   ```

3. (Optional) View resource usage for all namespaces:
   ```bash
   kubectl top pods --all-namespaces
   ```

### 5. Troubleshooting
- If `kubectl top` commands show no data, ensure:
  - Metrics Server is running (`kubectl get pods -n kube-system`).
  - Cluster nodes are appropriately labeled and ready.

### 6. Clean Up
If you want to remove the Metrics Server:
```bash
kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Summary
In this lab, you installed the Metrics Server to enable resource monitoring in your Kubernetes cluster. You used the `kubectl top` command to view CPU and memory usage for nodes and pods. This setup is essential for monitoring and scaling workloads effectively.
