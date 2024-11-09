# Lab: Updating a Deployment and Checking Rollout Status

## Objectives
- Learn how to update a deployment in Kubernetes.
- Monitor the rollout status during an update.
- Understand how `maxUnavailable` and `maxSurge` parameters affect rolling updates.

## Prerequisites
Ensure you have both `deployment.yaml` and `deployment-v2.yaml` ready for this lab. These files define the initial version (v1) and updated version (v2) of the deployment.

### `deployment.yaml`
This file defines the initial version of the deployment with image `ghcr.io/hungtran84/hello-app:1.0` and an accompanying service.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 10
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

### `deployment-v2.yaml`
This file defines the updated version of the deployment with image `ghcr.io/hungtran84/hello-app:2.0` and the same service.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 10
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
        image: ghcr.io/hungtran84/hello-app:2.0
        ports:
        - containerPort: 8080
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

## Understanding `maxUnavailable` and `maxSurge`

Kubernetes provides two key parameters, `maxUnavailable` and `maxSurge`, to control how deployments are updated:

- **`maxUnavailable`**: This parameter specifies the maximum number of pods that can be unavailable during the update process. By default, this is set to 25% of the replicas. For a deployment of 10 replicas, 25% of 10 is 2.5, which is rounded **down** to 2. This means that up to 2 pods can be unavailable at any time during the update.
  
- **`maxSurge`**: This parameter specifies the maximum number of extra pods that can be created during the update. The default value is also 25%. For a deployment of 10 replicas, 25% of 10 is 2.5, which is rounded **up** to 3. This means that up to 3 additional pods can be created during the update.

These settings determine how many pods can be in a "waiting" or "excess" state during a rolling update, ensuring minimal downtime and allowing the deployment to maintain availability.

To better understand these parameters, let's use `kubectl explain`:

1. **`maxUnavailable`**:
   ```bash
   kubectl explain deployment.spec.strategy.rollingUpdate.maxUnavailable
   ```

2. **`maxSurge`**:
   ```bash
   kubectl explain deployment.spec.strategy.rollingUpdate.maxSurge
   ```

For a deployment with 10 replicas:
- **Max Unavailable**: 25% of 10 = 2.5 → Rounded down to 2. This means up to 2 pods can be unavailable during the update.
- **Max Surge**: 25% of 10 = 2.5 → Rounded up to 3. This means up to 3 additional pods can be created during the update.

### Step 1: Deploy the Initial Version (v1)

1. Roll out the initial version of the deployment:
   ```bash
   kubectl apply -f deployment.yaml
   ```

   **Expected Output:**
   ```plaintext
   deployment.apps/hello-world created
   service/hello-world created
   ```

2. Check the status of the deployment:
   ```bash
   kubectl get deployment hello-world
   ```

   **Expected Output:**
   ```plaintext
   NAME           READY   UP-TO-DATE   AVAILABLE   AGE
   hello-world    10/10   10           10          40s
   ```

### Step 2: Update the Deployment to v2

1. Apply the new version of the deployment:
   ```bash
   kubectl apply -f deployment-v2.yaml
   ```

   **Expected Output:**
   ```plaintext
   deployment.apps/hello-world configured
   ```

2. Check the status of the rollout, which will show the update process in progress:
   ```bash
   kubectl rollout status deployment hello-world
   ```

   **Expected Output:**
   ```plaintext
   Waiting for deployment "hello-world" rollout to finish: 5 out of 10 new replicas have been updated...
   Waiting for deployment "hello-world" rollout to finish: 9 of 10 updated replicas are available...
   deployment "hello-world" successfully rolled out
   ```

3. Verify the rollout completion status with the exit code:
   ```bash
   echo $?
   ```

   **Expected Output:**
   ```plaintext
   0
   ```

### Step 3: Examine the Deployment Details

1. Describe the deployment to see details, including `Replicas`, `Conditions`, `Events`, `OldReplicaSet`, and `NewReplicaSet`:
   ```bash
   kubectl describe deployments hello-world
   ```

   **Expected Output (example):**
   ```plaintext
   Name:                   hello-world
   Namespace:              default
   CreationTimestamp:      Wed, 16 Aug 2023 22:53:38 +0700
   Labels:                 <none>
   Annotations:            deployment.kubernetes.io/revision: 2
   Selector:               app=hello-world
   Replicas:               10 desired | 10 updated | 10 total | 10 available | 0 unavailable
   StrategyType:           RollingUpdate
   ...
   ```

### Step 4: Review Replicasets for Rollback

1. Check existing replicasets:
   ```bash
   kubectl get replicaset
   ```

   **Expected Output:**
   ```plaintext
   NAME                     DESIRED   CURRENT   READY   AGE
   hello-world-66d45dfbcd   10        10        10      5m19s
   hello-world-6d59dfc665   0         0         0       9m52s
   ```

2. Describe the `NewReplicaSet` to inspect `labels`, `replicas`, `status`, and `pod-template-hash`:
   ```bash
   kubectl describe replicaset hello-world-66d45dfbcd
   ```

   **Expected Output (example):**
   ```plaintext
   Name:           hello-world-66d45dfbcd
   Namespace:      default
   Selector:       app=hello-world,pod-template-hash=66d45dfbcd
   Labels:         app=hello-world
                   pod-template-hash=66d45dfbcd
   ...
   ```

3. Describe the `OldReplicaSet` for comparison:
   ```bash
   kubectl describe replicaset hello-world-6d59dfc665
   ```

   **Expected Output (example):**
   ```plaintext
   Name:           hello-world-6d59dfc665
   Namespace:      default
   Selector:       app=hello-world,pod-template-hash=6d59dfc665
   Labels:         app=hello-world
                   pod-template-hash=6d59dfc665
   ...
   ```

### Step 5: Clean Up Resources

To avoid incurring unnecessary resource usage, delete the resources created during this lab:

1. Delete the deployment and service:
   ```bash
   kubectl delete -f deployment-v2.yaml
   ```

   **Expected Output:**
   ```plaintext
   deployment.apps "hello-world" deleted
   service "hello-world" deleted
   ```

## Summary
In this lab, you learned to:
- Deploy a new version of an application using Kubernetes deployments.
- Check the rollout status and ensure the deployment completes successfully.
- Inspect deployment details and understand the usage of `replicasets` for rolling updates and rollbacks.
