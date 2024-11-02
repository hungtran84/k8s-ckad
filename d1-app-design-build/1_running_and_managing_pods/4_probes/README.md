#  Implement Container Probes

## Objective
To configure and implement container probes (`liveness`, `readiness`, and `startup`) in a Kubernetes deployment, monitor their behavior, and resolve issues related to incorrect probe settings.

## Steps

### 1. Start Monitoring Events
Start a watch to observe the events associated with our probes.
```bash
kubectl get events --watch &
clear
```

### 2. Create a Deployment with Probes
We have a single container pod app in a `Deployment` that has both a `liveness` probe and a `readiness` probe.

```yaml
# container-probes.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
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
        livenessProbe:
          tcpSocket:
            port: 8081
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 8081
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 3. Apply the Deployment
Deploy the configuration. After 10 seconds, our liveness and readiness probes will fail. The liveness probe will kill the current pod and recreate one.
```bash
kubectl apply -f container-probes.yaml
```

### 4. Monitor Pod Status
Check the pod status to observe readiness and restarts.
```bash
kubectl get pods
```

### 5. Investigate Issues
Describe the pod to understand the failures.
```bash
kubectl describe pods
```
- Check the events for probe failures.
- Review the current configuration of liveness and readiness probes.
- Confirm the container's readiness status.

### 6. Update Probe Configuration
Change the probes to the correct container port (8080).
```yaml
# Update container-probes.yaml
livenessProbe:
  tcpSocket:
    port: 8080
readinessProbe:
  httpGet:
    path: /
    port: 8080
```

### 7. Reapply the Configuration
Send the updated configuration to the API server.
```bash
kubectl apply -f container-probes.yaml
```

### 8. Verify Changes
Check the pod status and confirm the probes are correctly pointing to port `8080`.
```bash
kubectl describe pods
kubectl get pods
```

### 9. Clean Up
Delete the deployment to clean up resources.
```bash
kubectl delete deployment hello-world
```

### 10. Create Deployment with Faulty Startup Probe
Start monitoring events again.
```bash
kubectl get events --watch &
clear
```

### 11. Define Startup Probe
Create a deployment with a faulty startup probe.
```yaml
# container-probes-startup.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
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
        startupProbe:
          tcpSocket:
            port: 8081
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 1
        livenessProbe:
          tcpSocket:
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 12. Deploy and Monitor
Apply the deployment and monitor for container restarts.
```bash
kubectl apply -f container-probes-startup.yaml
kubectl get pods
```

### 13. Correct Startup Probe
Change the startup probe port from `8081` to `8080`.
```bash
kubectl apply -f container-probes-startup.yaml
```

### 14. Confirm Pod Status
Check that the pod is now up and ready.
```bash
kubectl get pods
```

### 15. Close Monitoring
Close the watch on events.
```bash
fg
ctrl+c
```

### 16. Final Cleanup
Remove the deployment with the faulty startup probe.
```bash
kubectl delete -f container-probes-startup.yaml
```

## Summary
In this implementation, we configured and tested liveness, readiness, and startup probes in a Kubernetes deployment. We monitored their behavior through event logs, diagnosed issues related to incorrect probe settings, and successfully resolved them by updating the configuration.

### Probe Handlers
There are three available handlers that can cover almost any scenario:

#### Exec Action
Executes a command inside the container; this can handle various tasks since any executable can be run, such as a script that performs multiple curl requests to determine the status or an executable that connects to an external dependency. Ensure that the executable does not create zombie processes.

#### TCP Socket Action
Connects to a defined port to check if the port is open, mostly used for endpoints that do not communicate over HTTP.

#### HTTP Get Action
Sends an HTTP GET request as a probe to the defined path; the HTTP response code determines whether the probe is successful.

### Common Probe Parameters
Each type of probe has common configurable fields:

- **initialDelaySeconds**: Seconds after the container started and before probes start. (default: 0)
- **periodSeconds**: Frequency of the pod checks. (default: 10)
- **timeoutSeconds**: Timeout for the expected response. (default: 1)
- **successThreshold**: How many successful results are needed to transition from failure to a healthy state. (default: 1)
- **failureThreshold**: How many failed results are needed to transition from a healthy to a failure state. (default: 3)

For successful probe configuration, analyzing the requirements and dependencies of our application/microservice is essential.

### Startup Probes
If your process requires time to get ready, such as reading a file, parsing a large configuration, or preparing data, you should use startup probes. If the probe fails and the threshold is exceeded, it will trigger a restart, allowing the operation to start over. Adjust **initialDelaySeconds** and **periodSeconds** accordingly to ensure the process has sufficient time to complete; otherwise, your pod may enter a loop of restarts.

### Readiness Probes
Readiness probes control the traffic sent to the pod. They modify Pod Conditions, indicating whether the pod should be included in the service and load balancers. When the probe succeeds enough times (based on the threshold), the pod is marked as ready to receive traffic. If the process can signal that it needs to be temporarily removed from service, readiness probes facilitate this.

### Liveness Probes
Liveness probes are useful when a container cannot crash by itself due to unexpected errors. Using liveness probes allows Kubernetes to restart the pod when the probe fails, thus addressing some bugs in the process. If the process can handle errors by exiting, you may not need liveness probes; however, they are advantageous for accommodating unknown bugs until fixed.
