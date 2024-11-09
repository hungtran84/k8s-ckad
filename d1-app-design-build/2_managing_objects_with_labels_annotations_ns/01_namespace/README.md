Here's the updated markdown with headers structured as requested:

# Lab d1.2.1: Exploring Kubernetes Namespaces

## Objective  
In this lab, we will explore how namespaces in Kubernetes help in organizing resources, managing permissions, and isolating workloads. We will create multiple namespaces, deploy resources within these namespaces, and examine how they affect resource visibility, access, and isolation.

## Steps

### Section 1: Creating and Exploring Namespaces  

#### Step 1: List Existing Namespaces  
Start by listing all the existing namespaces to see the default namespaces created by Kubernetes.

```bash
kubectl get namespaces
```

You should see namespaces such as `default`, `kube-system`, `kube-public`, and others depending on your Kubernetes setup.

#### Step 2: Create New Namespaces  
Create two new namespaces to use in this lab: `dev` and `prod`. Namespaces are defined directly through `kubectl`.

```bash
kubectl create namespace dev
kubectl create namespace prod
```

Verify their creation by listing the namespaces again:

```bash
kubectl get namespaces
```

Example output:

```
NAME              STATUS   AGE
default           Active   10d
kube-system       Active   10d
kube-public       Active   10d
dev               Active   1m
prod              Active   1m
```

### Section 2: Deploying Resources within Namespaces  

#### Step 3: Deploy a Pod in the `dev` Namespace  
Create a simple pod in the `dev` namespace using the following manifest file:

```yaml
# dev-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: dev-hello-world-pod
  namespace: dev
spec:
  containers:
  - name: hello-world
    image: ghcr.io/hungtran84/hello-app:1.0
    ports:
    - containerPort: 80
```

Apply the configuration:

```bash
kubectl apply -f dev-pod.yaml
```

#### Step 4: Verify the Pod in the `dev` Namespace  
List all pods in the `dev` namespace to confirm that the pod has been created successfully.

```bash
kubectl get pods -n dev
```

#### Step 5: Deploy a Pod in the `prod` Namespace  
Similarly, create a pod in the `prod` namespace using the following manifest:

```yaml
# prod-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: prod-hello-world-pod
  namespace: prod
spec:
  containers:
  - name: hello-world
    image: ghcr.io/hungtran84/hello-app:1.0
    ports:
    - containerPort: 80
```

Apply the configuration:

```bash
kubectl apply -f prod-pod.yaml
```

#### Step 6: Verify the Pod in the `prod` Namespace  
List all pods in the `prod` namespace to confirm that the pod has been created successfully.

```bash
kubectl get pods -n prod
```

### Section 3: Accessing Resources Across Namespaces  

#### Step 7: Attempt Cross-Namespace Pod Access  
Try accessing the `prod-hello-world-pod` from a pod in the `dev` namespace. By default, Kubernetes does not allow pods from different namespaces to interact unless configured explicitly. 

```bash
kubectl exec -it dev-hello-world-pod -n dev -- curl prod-hello-world-pod.prod.svc.cluster.local
```

This command might fail if network policies or DNS settings prevent inter-namespace communication, highlighting the isolation provided by namespaces.

### Section 4: Cleaning Up

#### Step 8: Delete Resources and Namespaces  
After completing the lab, delete the pods and namespaces to clean up your environment.

```bash
kubectl delete pod dev-hello-world-pod -n dev
kubectl delete pod prod-hello-world-pod -n prod
kubectl delete namespace dev
kubectl delete namespace prod
```

## Summary  
In this lab, we explored how namespaces in Kubernetes provide a way to organize, isolate, and manage resources within a cluster. By creating separate `dev` and `prod` namespaces, we demonstrated the deployment of isolated resources and observed namespace-based resource visibility and access control.

## Use Cases  
- **Development and Testing**: Separate environments for dev, staging, and production help maintain configuration consistency while isolating resources.
- **Multi-Tenant Clusters**: For organizations hosting multiple applications or users, namespaces can provide logical separation within a single cluster.
- **Resource Quotas and Limits**: Namespaces can help allocate resources to specific teams or applications, enforcing limits to avoid resource contention.

## Additional Considerations  
- **Network Policies**: Kubernetes supports network policies to control traffic between pods, allowing further customization of inter-namespace access.
- **Role-Based Access Control (RBAC)**: By combining namespaces with RBAC, administrators can enforce fine-grained permissions, ensuring users and services only access designated namespaces.
- **Resource Quotas**: Namespaces can be configured with resource quotas, which prevent resource overuse by limiting CPU, memory, and storage allocations within a namespace.

## Conclusion
Kubernetes namespaces are a fundamental tool for structuring resources, managing access, and enabling multi-tenant applications within a single cluster.