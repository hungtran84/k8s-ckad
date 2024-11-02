# D1.1.1.2b - Sidecar Pattern

The Sidecar Pattern is an additional container that extends the functionality of the main container. An example frequently cited is when you want to send logs to an external system. Without altering the business logic of the main container, you can deploy a logging agent as a sidecar container. This pattern is particularly useful for tasks such as logging and monitoring, where sidecars can collect logs or metrics from the primary application and forward them to an external system without modifying the primary application.

## Example Configuration

This section demonstrates how to set up a simple sidecar pattern using Kubernetes.

### 1. Creating the Multi-Container Pod

Create a file named `multicontainer-pod.yaml` to define a pod with both a producer and a consumer container.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multicontainer-pod
spec:
  containers:
  - name: producer
    image: ubuntu
    command: ["/bin/bash"]
    args: ["-c", "while true; do echo $(hostname) $(date) >> /var/log/index.html; sleep 10; done"]
    volumeMounts:
    - name: webcontent
      mountPath: /var/log
  - name: consumer
    image: nginx
    ports:
      - containerPort: 80
    volumeMounts:
    - name: webcontent
      mountPath: /usr/share/nginx/html
  volumes:
  - name: webcontent 
    emptyDir: {}
```

#### Explanation

- **Producer Container**: The `producer` container runs an Ubuntu image and continuously writes the hostname and the current date to a file located at `/var/log/index.html` every 10 seconds.
- **Consumer Container**: The `consumer` container runs an Nginx web server that serves the content of the `index.html` file located in the mounted directory.
- **Volume Configuration**: The `webcontent` volume is defined as an `emptyDir`, which means it is a temporary file system that is shared between the two containers in the pod. Data written by the producer is immediately visible to the consumer.

### 2. Apply the Configuration

To create the multi-container pod, execute the following command:

```bash
kubectl apply -f multicontainer-pod.yaml
```

### 3. Accessing the Pod's Shell

Connect to the pod using `kubectl exec` to explore the contents of the log file:

```bash
kubectl exec -it multicontainer-pod -- /bin/sh
```

You will be connected to the `producer` container by default. To check the contents of the log directory:

```bash
# ls -la /var/log
```

This command will display the contents of the `/var/log` directory, showing the `index.html` file that the producer has been updating.

To view the latest entries in the `index.html` file, use:

```bash
# tail /var/log/index.html
```

This will output the most recent lines added by the producer, confirming that data is being written correctly.

### 4. Accessing the Consumer Container

Specify the container name to access the consumer container:

```bash
kubectl exec -it multicontainer-pod --container consumer -- /bin/sh
```

Check the contents served by Nginx:

```bash
# ls -la /usr/share/nginx/html
```

You should see the `index.html` file there as well.

To view the contents being served by the consumer:

```bash
# tail /usr/share/nginx/html/index.html
```

This should display the same lines that were logged by the producer, showing that both containers share data via the mounted volume.

### 5. Port Forwarding

To access the web server running in the consumer container, set up port forwarding from your local machine:

```bash
kubectl port-forward multicontainer-pod 8080:80 &
```

Now, you can send a request to the Nginx server:

```bash
curl http://localhost:8080
```

This command will retrieve the content from `index.html`, demonstrating that the consumer container is serving data from the shared volume.

### 6. Cleanup Resources

After testing, you can clean up the resources by deleting the pod:

```bash
kubectl delete pod multicontainer-pod
```

## Conclusion

This setup effectively demonstrates how to implement the sidecar pattern in Kubernetes, allowing for enhanced data sharing and functionality between containers. By using a shared volume, the producer and consumer containers can communicate efficiently, showcasing the flexibility and power of multi-container pods in Kubernetes.
