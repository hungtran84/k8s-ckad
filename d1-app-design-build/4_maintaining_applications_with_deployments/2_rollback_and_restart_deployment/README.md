# Lab - Rollback and restart deployment

## Objectives
- Learn how Kubernetes handles updates to a non-existent image in a deployment.
- Observe the effects of using an invalid image and how the system behaves under a failed rollout.
- Understand the use of `maxUnavailable`, `maxSurge`, and the `progressDeadlineSeconds` in the rollout process.

## Steps

### Step 1: Delete Existing Deployments
We start by deleting any existing deployments because we're interested in observing state changes during the deployment process.
```bash
kubectl delete deployment hello-world
kubectl delete service hello-world
```

### Step 2: Create v1 Deployment and Update to v2
Create the initial deployment using a `deployment.yaml` file and then update it to v2 using `deployment.v2.yaml`.
```bash
kubectl apply -f deployment.yaml
```

**Output:**
```plaintext
deployment.apps/hello-world created
service/hello-world created
```

```
kubectl apply -f deployment-v2.yaml
```

**Output:**
```plaintext
deployment.apps/hello-world configured
service/hello-world unchanged
```

### Step 3: Apply Broken Deployment
Now, apply a broken deployment configuration (`deployment.broken.yaml`) that references a non-existent image.
```bash
kubectl apply -f deployment.broken.yaml
```

**Output:**
```plaintext
deployment.apps/hello-world configured
service/hello-world unchanged
```

### Step 4: Observe the Rollout Failure
We expect the rollout to fail due to the unavailable image. Check the rollout status:
```bash
kubectl rollout status deployment hello-world
```

**Output:**
```plaintext
Waiting for deployment "hello-world" rollout to finish: 5 out of 10 new replicas have been updated...
error: deployment "hello-world" exceeded its progress deadline
```

You can also check the return code:
```bash
echo $?
# Output: 1
```

### Step 5: Inspect Pods and Error Messages
Next, check the status of the pods to observe the `ImagePullBackoff` or `ErrImagePull` errors.
```bash
kubectl get pods
```

**Output:**
```plaintext
NAME                           READY   STATUS             RESTARTS   AGE
hello-world-556c7c756d-27m2l   0/1     ErrImagePull       0          115s
hello-world-556c7c756d-6bzv8   0/1     ErrImagePull       0          115s
hello-world-556c7c756d-g7lt7   0/1     ErrImagePull       0          115s
hello-world-556c7c756d-r927d   0/1     ErrImagePull       0          115s
hello-world-556c7c756d-rkjfs   0/1     ImagePullBackOff   0          115s
hello-world-647685778-7v6jz    1/1     Running            0          4m
hello-world-647685778-dsmwt    1/1     Running            0          3m57s
hello-world-647685778-jvz8f    1/1     Running            0          3m58s
hello-world-647685778-kmlxz    1/1     Running            0          3m57s
hello-world-647685778-p92v7    1/1     Running            0          4m
hello-world-647685778-pznpm    1/1     Running            0          4m1s
hello-world-647685778-qvxg8    1/1     Running            0          4m1s
hello-world-647685778-xz6qn    1/1     Running            0          3m57s
```

### Step 6: Understand `maxUnavailable` and `maxSurge`
Now, let's look at the concept of `maxUnavailable` and `maxSurge`. In this case:
- `maxUnavailable` is 25% (rounding down to 2), so only 2 pods from the original `ReplicaSet` are offline.
- `maxSurge` is 25% (rounding up to 3), which means we have 13 pods in total, 3 more than the desired 10.

Check the `kubectl describe` output:
```bash
kubectl describe deployments hello-world
```

**Output:**
```plaintext
...
Replicas:               10 desired | 5 updated | 13 total | 8 available | 5 unavailable
RollingUpdateStrategy:  25% max unavailable, 25% max surge
...
```

### Step 7: Review Rollout History
To review the deployment history, check the rollout revisions:
```bash
kubectl rollout history deployment hello-world
```

**Output:**
```plaintext
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
```

### Step 8: Examine Changes in Each Revision
You can check the changes applied in each revision to see the pod templates:
```bash
kubectl rollout history deployment hello-world --revision=2
kubectl rollout history deployment hello-world --revision=3
```

### Step 9: Rollback to Previous Revision
Since revision 2 is the last valid configuration, we will rollback to it:
```bash
kubectl rollout undo deployment hello-world --to-revision=2
```

**Output:**
```plaintext
deployment.apps/hello-world rolled back
```


Check the rollout status:
```bash
kubectl rollout status deployment hello-world
```

**Output:**
```plaintext
deployment "hello-world" successfully rolled out
```

### Step 10: Verify Pod Status
Check the status of the pods after the rollback:
```bash
kubectl get pods
```

**Output:**
```plaintext
NAME                          READY   STATUS    RESTARTS   AGE
hello-world-647685778-6stvg   1/1     Running   0          47s
hello-world-647685778-7v6jz   1/1     Running   0          13h
hello-world-647685778-dsmwt   1/1     Running   0          13h
hello-world-647685778-jvz8f   1/1     Running   0          13h
hello-world-647685778-kmlxz   1/1     Running   0          13h
hello-world-647685778-p92v7   1/1     Running   0          13h
hello-world-647685778-pznpm   1/1     Running   0          13h
hello-world-647685778-qvxg8   1/1     Running   0          13h
hello-world-647685778-xwqhv   1/1     Running   0          47s
hello-world-647685778-xz6qn   1/1     Running   0          13h
```

### Step 11: Clean Up
Finally, delete the deployment and start over with a new deployment:
```bash
kubectl delete deployment hello-world
kubectl delete service hello-world
```

## Summary
In this lab, we demonstrated how Kubernetes handles rollouts when an invalid image is referenced. We observed the use of `maxUnavailable` and `maxSurge` in controlling the rollout process. The lab also covered how to handle failed rollouts, inspect the state of pods, and rollback to a previous working revision.
