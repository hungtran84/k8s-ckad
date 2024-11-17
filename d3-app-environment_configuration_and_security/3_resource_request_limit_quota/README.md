# Lab: Demonstrating Resource Control in Kubernetes

## Objectives

- Understand and configure **resource requests** and **limits** for pods in Kubernetes.
- Implement a **ResourceQuota** to enforce limits on resource consumption within a namespace.
- Verify resource controls in action.

---

## Steps

### Step 1: Create a Namespace Manifest
1. Create a namespace manifest to define the namespace for resource control:
   ```yaml
   # namespace.yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: resource-lab
   ```
   
2. Apply the namespace manifest:
   ```bash
   kubectl apply -f namespace.yaml
   ```

---

### Step 2: Configure Resource Requests and Limits
1. Create a deployment manifest that includes resource requests and limits within the `resource-lab` namespace:
   ```yaml
   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: resource-demo
     namespace: resource-lab
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: demo
     template:
       metadata:
         labels:
           app: demo
       spec:
         containers:
         - name: demo-container
           image: nginx
           resources:
             requests:
               memory: "128Mi"
               cpu: "250m"
             limits:
               memory: "256Mi"
               cpu: "500m"
   ```

2. Apply the deployment manifest:
   ```bash
   kubectl apply -f deployment.yaml
   ```

3. Check the pod's resource configuration:
   ```bash
   kubectl get pods -n resource-lab -o jsonpath='{.items[*].spec.containers[*].resources}'
   ```

---

### Step 3: Define a ResourceQuota
1. Create a `ResourceQuota` manifest that specifies limits for the `resource-lab` namespace:
   ```yaml
   # resourcequota.yaml
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: resource-lab-quota
     namespace: resource-lab
   spec:
     hard:
       requests.cpu: "1"
       requests.memory: "512Mi"
       limits.cpu: "2"
       limits.memory: "1Gi"
   ```

2. Apply the resource quota manifest:
   ```bash
   kubectl apply -f resourcequota.yaml
   ```

3. View the applied quota:
   ```bash
   kubectl get resourcequota resource-lab-quota -n resource-lab -o yaml
   ```

---

### Step 4: Verify Resource Quota Enforcement
1. Try scaling the deployment to exceed the quota:
   ```bash
   kubectl scale deployment resource-demo --replicas=5 -n resource-lab
   ```

2. Observe the error message when exceeding the quota:
   ```bash
   kubectl describe resourcequota resource-lab-quota -n resource-lab
   ```

3. Correct the deployment scale to fit within the quota:
   ```bash
   kubectl scale deployment resource-demo --replicas=3 -n resource-lab
   ```

---

## Summary

In this lab, you:
- Learned how to configure **resource requests** and **limits** for containers within a specific namespace.
- Defined and enforced a **ResourceQuota** scoped to the `resource-lab` namespace.
- Verified the enforcement of resource quotas to control resource consumption.

By specifying the namespace in the manifests, you ensure the resources are directly created in the appropriate scope.
