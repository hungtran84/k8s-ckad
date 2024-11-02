# Lab d1.1.3: Exploring Pod Lifecycle and Restart Policies in Kubernetes

## Objective
In this lab, we will examine the lifecycle of a pod in Kubernetes, focusing on how different restart policies (Always, OnFailure, and Never) influence pod behavior. We will simulate failures and observe how Kubernetes manages pod restarts based on the specified restart policy.

## Steps

## Section 1: Always Restart Policy

### Step 1: Monitor Events in Real-Time
Start by watching events in real-time to observe actions taken by Kubernetes during the pod’s lifecycle:

```bash
kubectl get events --watch &
```

### Step 2: Create the Pod with Always Restart Policy
Using the manifest file `pod-always.yaml`, create a pod with the default restart policy (`Always`). This will allow us to observe how Kubernetes manages a pod when the main container fails and restarts automatically.

```yaml
# pod-always.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world-always-pod
spec:
  containers:
  - name: hello-world
    image: ghcr.io/hungtran84/hello-app:1.0
    ports:
    - containerPort: 80
```

Apply the configuration:

```bash
kubectl apply -f pod-always.yaml
```

**Example output:**

```plaintext
pod/hello-world-always-pod created
```

### Step 3: Simulate a Failure in the Container
To simulate a failure, kill the main process inside the container. Kubernetes should detect this failure and attempt to restart the container.

```bash
kubectl exec -it hello-world-always-pod -- /usr/bin/killall hello-app
```

Check the pod’s status to confirm the restart:

```bash
kubectl get pods
```

**Example output showing a restart:**

```plaintext
NAME                          READY   STATUS    RESTARTS   AGE
hello-world-always-pod       1/1     Running   1          1m
```

### Step 4: Describe the Pod to View Restart Details
Use `kubectl describe` to see detailed information, including the restart count, which indicates the number of times Kubernetes restarted the container.

```bash
kubectl describe pod hello-world-always-pod
```

## Section 2: Batch Job with OnFailure Restart Policy

### Step 5: Create a Batch Job to Test Exit Codes
We will create 2 Pods to simulate both a successful completion (exit code 0) and a failure (exit code 1) case. The Job will run a simple command in two different pods: one will exit with code 0, and the other will exit with code 1.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world-success-pod
spec:
  containers:
  - name: hello-world-success
    image: busybox
    command: ['sh', '-c', 'echo "This job succeeded"; exit 0']
  restartPolicy: OnFailure

--- 
apiVersion: v1
kind: Pod
metadata:
  name: hello-world-failure-pod
spec:
  containers:
  - name: hello-world-failure
    image: busybox
    command: ['sh', '-c', 'echo "This job succeeded"; exit 1']
  restartPolicy: OnFailure
```

Apply the configuration:

```bash
kubectl apply -f pod-restart-onfailure.yaml
```

### Step 6: Monitor the pods
Check the status of the pod to see how they completed:

```bash
kubectl get pod
```

You should see both jobs listed, with the `hello-world-pod-success` job completing successfully and the `hello-world-pod-failure` job failing.

### Step 7: Describe the Jobs for Exit Codes
Use `kubectl describe` to check the details of each job, including their completion status and exit codes.

```bash
kubectl describe pod hello-world-pod-success
kubectl describe pod hello-world-pod-failure
```

In the output, check for:

- **Completion Status**: The successful job should indicate completion, while the failed job should show an error state.
- **Exit Code**: The successful job should have an exit code of 0, while the failed job should have an exit code of 1.

### OnFailure Restart Policy Behavior
1. **Initial Pod Creation**: 
When a pod is created with the `OnFailure` restart policy, Kubernetes will attempt to run the container specified in the pod definition.

2. **Container Exit and Failure**: 
If the container exits with a failure status code (e.g., exit code 1), Kubernetes recognizes this as a failure. Under the `OnFailure` policy, the pod is marked as failed, and Kubernetes initiates a restart attempt.

3. **Backoff Mechanism**:

- **Backoff Delay**: Kubernetes employs an exponential backoff strategy for restarting the pod. This means that after a failure, Kubernetes will wait for a brief period before trying to restart the pod. If the pod fails again, the wait time will increase exponentially, up to a maximum limit. This is done to prevent rapid, continuous restarts that can overwhelm the system or lead to resource exhaustion.

- **Retry Limit**: Kubernetes has a configurable limit on the number of retries (or backoff attempts) it will make to restart the pod. If the container continues to fail and reaches this limit, Kubernetes will stop attempting to restart it, and the pod will be marked as failed permanently.

4. **Pod Status Updates**: After each failure and restart attempt, the pod's status will be updated accordingly. You can monitor the pod's status using commands like kubectl get pods or kubectl describe pod <pod-name>. You'll see a status indicating the number of restarts, as well as the reason for the failure (in the event of a permanent failure).
During this process, the RESTARTS count for the pod will increment each time the container fails and Kubernetes attempts to restart it.

## Section 3: Never Restart Policy

### Step 8: Create the Pod with Never Restart Policy
Finally, create a pod with the `Never` restart policy to observe its behavior when the container fails.

```yaml
# pod-never.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world-never-pod
spec:
  containers:
  - name: hello-world
    image: ghcr.io/hungtran84/hello-app:1.0
  restartPolicy: Never
```

Apply the configuration:

```bash
kubectl apply -f pod-never.yaml
```

### Step 9: Test the Never Restart Policy
Simulate a failure in the `hello-world-never-pod` by killing the main process. Observe that the pod enters an Error state without restarting.

```bash
kubectl exec -it hello-world-never-pod -- /usr/bin/killall hello-app
kubectl get pod hello-world-never-pod
```

The pod status should remain `Error`, as the restart policy prevents any restart.

### Step 10: Clean Up
Delete all pods and jobs created during the lab:

```bash
kubectl delete pod hello-world-always-pod hello-world-failure-pod hello-world-success-pod hello-world-never-pod
```

Stop the watch command:

1. Bring the background process to the foreground:

   ```bash
   fg
   ```

2. Terminate it with `Ctrl + C`.

## Summary

In this lab, we explored the lifecycle of a Kubernetes pod and observed how different restart policies affect pod behavior following a failure. By using `Always`, `OnFailure`, and `Never`, we can control whether a container restarts after a failure, helping optimize resource management and troubleshoot specific container behaviors in Kubernetes deployments.

### Use Cases

- **Always**: For services that need high availability and should be running continuously, e.g., web servers, microservices.
- **OnFailure**: For batch jobs or processes that should restart only when they fail, e.g., data processing jobs that should retry on error but not on success.
- **Never**: For tasks that only need to run once, e.g., initialization jobs, database migrations, or clean-up tasks that don’t need to restart.

### Additional Considerations

- **Job and CronJob Resources**: When using Kubernetes Jobs or CronJobs, the `restartPolicy` is set to `OnFailure` by default for Jobs and can be set to `Never` for CronJobs to control task execution behavior.
- **Pod Lifecycle**: The `restartPolicy` only applies to containers in a pod and not the pod itself. If a pod is terminated, it must be recreated, typically through a higher-level controller like a Deployment, StatefulSet, or DaemonSet.
- **Monitoring and Alerts**: Depending on the `restartPolicy`, it's essential to monitor pod statuses and set up alerts to handle unexpected behavior, especially with the `Always` policy, to avoid resource wastage from constant restarts.

In conclusion, understanding and choosing the right `restartPolicy` is crucial for designing resilient applications in Kubernetes, as it directly impacts how your applications handle failures and recover from errors.
