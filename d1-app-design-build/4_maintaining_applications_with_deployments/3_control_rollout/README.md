# Lab: Controlling the Rate and Update Strategy of a Deployment Update

## Objectives
- Deploy a Kubernetes `Deployment` with Readiness probes.
- Update the deployment using `RollingUpdate` strategy with specific control over the rollout speed and max surge/unavailable pods.
- Troubleshoot deployment issues such as pods not becoming ready due to incorrect configuration.
- Use `kubectl` commands to inspect deployment status, progress, and troubleshoot.
- Perform a deployment rollback to a previous revision.

## Steps

### 1. Deploy the Initial Deployment with Readiness Probes
We will start by deploying a `Deployment` resource with Readiness Probes to ensure the pods are ready before they are considered available.

Let review the manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 20
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 10%
      maxSurge: 2
  revisionHistoryLimit: 20
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello-world
        image: ghcr.io/hungtran84/hello-app:1.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /index.html
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  selector:
    app: hello-world
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
```


```bash
kubectl apply -f deployment.probes-1.yaml
```
**Output:**
```plaintext
deployment.apps/hello-world created
service/hello-world created
```

Next, check the `Replicas` and `Conditions` to ensure all pods are online and ready:

```bash
kubectl describe deployment hello-world
```

Look for:
- **Replicas:** All 20 pods should be in the available state.
- **Conditions:** Pods should be marked as `Available` and `Progressing`.

### 2. Update the Deployment from v1 to v2
Now, update the deployment to use a new version (`v2`) of the container image with the updated readiness probe settings.

```bash
diff deployment.probes-1.yaml deployment.probes-2.yaml
```

**Output:**
```plaintext
23c23
<         image: ghcr.io/hungtran84/hello-app:1.0
---
>         image: ghcr.io/hungtran84/hello-app:2.0
```

Apply the update:
```bash
kubectl apply -f deployment.probes-2.yaml
```

**Output:**
```plaintext
deployment.apps/hello-world configured
service/hello-world configured
```

Check the status of the replicas and ensure the rollout is in progress:
```bash
kubectl get replicaset
```
**Output:**
```plaintext
NAME                     DESIRED   CURRENT   READY   AGE
hello-world-55574f5d66   14        14        14      6m44s
hello-world-57db99fb49   8         8         4       28s
...
...
hello-world-68b85d479f   0         0         0       7m9s
hello-world-7f8558c654   20        20        20      2m46s
```

Inspect the deployment again:
```bash
kubectl describe deployment hello-world
```

### 3. Update Again Without Checking `diff` (Troubleshooting Scenario)
This time, we will update without checking the `diff` first, and later troubleshoot why some replicas are not updating.

```bash
kubectl apply -f deployment.probes-3.yaml
```

Check the deployment status:
```bash
kubectl rollout status deployment hello-world
```

If the deployment is stuck at a certain point, such as `4 out of 20 new replicas have been updated`, investigate using:

```bash
kubectl describe deployment hello-world
```

Inspect the status:
- **Replicas:** You may see discrepancies with `total` and `updated`.
- **Conditions:** Check for the `ReplicaSetUpdated` status, indicating that updates are progressing.

### 4. Troubleshoot the Issue (Readiness Probe Misconfiguration)
If the deployment is stuck and not progressing, the issue might be related to the `Readiness Probe`. Let's check the `ReplicaSets`:

```bash
kubectl get replicaset
```

You may find that no pods in the new ReplicaSet (`hello-world-5c5cf688f8`) are ready, while pods in the old ReplicaSet (`hello-world-55574f5d66`) are ready.

```bash
kubectl describe deployment hello-world
```

Look for the `Readiness` probe configuration, and verify if the port is correct. In this case, the port might have been misconfigured during the update:
- Port `8080` was updated to `8081`, which could cause the readiness probe to fail if the application doesn't respond on the new port.

### 5. Rollback to a Previous Revision
Once you've identified the issue (e.g., incorrect readiness probe configuration), you can rollback to a previous revision.

```bash
kubectl rollout undo deployment hello-world --to-revision=2
```

Check the status of the deployment to verify the rollback:
```bash
kubectl describe deployment hello-world
```

Ensure the `Replicas` are back to 20, and all pods are available.

### 6. Clean Up the Deployment
After completing the tasks, delete the deployment and service:

```bash
kubectl delete deployment hello-world
kubectl delete service hello-world
```

### 7. Restarting a Deployment
For a fresh start, create a new deployment with a simple image:

```bash
kubectl create deployment hello-world --image=ghcr.io/hungtran84/hello-app:1.0 --replicas=5
```

Check the status of the deployment and its pods:

```bash
kubectl get deployment
```

```bash
kubectl get pods
```

Restart the deployment to trigger a new rollout:

```bash
kubectl rollout restart deployment hello-world
```

Check the deployment status again to see the new ReplicaSet being created:

```bash
kubectl describe deployment hello-world
```

### Summary
- We successfully created and updated a deployment using the `RollingUpdate` strategy.
- We managed the update rollout speed with `maxUnavailable` and `maxSurge` settings.
- Troubleshot issues with readiness probes and used `kubectl describe` to inspect deployment states.
- Rolled back to a previous deployment revision to resolve issues.
- Cleaned up by deleting the deployment and service, and restarted a deployment to test further.
