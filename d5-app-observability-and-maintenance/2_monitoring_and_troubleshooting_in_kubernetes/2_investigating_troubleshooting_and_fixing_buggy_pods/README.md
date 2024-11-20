# Lab: Troubleshooting and debugging in Kubernets

## Objectives
In this lab, you will:
- Create a simple NGINX deployment and generate access logs with error codes (`4xx` and `5xx`).
- Create a Deployment that produces error logs (e.g., "DB connection failed").
- Debug scenarios involving:
  - A Deployment with an invalid container command.
  - A GPU Deployment that cannot start due to missing GPU nodes.
- Use `kubectl logs` and related commands to investigate and resolve issues.
- Perform a rollout restart of a Deployment and retrieve logs from a deleted pod.

## Steps

### 1. Prerequisites
- A running Kubernetes cluster.
- `kubectl` installed and configured.

---

### 2. Create a Simple NGINX Deployment and Generate Logs

#### 2.1 Create an NGINX Deployment
1. Deploy NGINX:
   ```bash
   kubectl create deployment nginx --image=nginx
   ```

2. Expose the deployment as a ClusterIP service:
   ```bash
   kubectl expose deployment nginx --port=80 --target-port=80
   ```

3. Check the service details:
   ```bash
   kubectl get service nginx
   ```
   Note the service name, such as `nginx`.

#### 2.2 Send Requests to Generate Logs
1. Use a temporary `nginx:alpine` pod to send requests:
   ```bash
   kubectl run curl-pod --image=nginx:alpine --restart=Never -it --rm -- sh
   ```

2. Inside the pod shell, use `curl` to access the service by its name:
   ```bash
   curl http://nginx
   ```

3. Introduce error codes:
   - Send a request to a non-existent path to generate a `404` error:
     ```bash
     curl http://nginx/nonexistent
     ```

4. Exit the pod shell by typing `exit`.

5. Retrieve NGINX pod logs:
   ```bash
   kubectl logs -l app=nginx
   ```

---

### 3. Debugging a Buggy Pod/Deployment

#### 3.1 Deployment with an Invalid Container Command
1. Apply a Deployment with an invalid command:
   <details>
   <summary>Reveal Manifest</summary>

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: invalid-command
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: invalid-command
     template:
       metadata:
         labels:
           app: invalid-command
       spec:
         containers:
         - name: invalid-container
           image: nginx
           command: ["invalid-command"] # Invalid command
   ```
   </details>

2. Apply the manifest:
   ```bash
   kubectl apply -f <manifest-file>
   ```

3. Debug the issue:
   - Check pod status:
     ```bash
     kubectl get pods -l app=invalid-command
     ```
   - View events:
     ```bash
     kubectl describe pod -l app=invalid-command
     ```
   - Check logs (if applicable):
     ```bash
     kubectl logs -l app=invalid-command
     ```

4. Fix the issue:
   - Patch the deployment to remove the invalid command:
     ```bash
     kubectl patch deployment invalid-command --type=json -p '[{"op":"remove","path":"/spec/template/spec/containers/0/command"}]'
     ```

5. Verify the pod is running:
   ```bash
   kubectl get pods -l app=invalid-command
   ```

---

#### 3.2 GPU Deployment Pending Due to Missing GPU Nodes
1. Apply a GPU Deployment manifest:
   <details>
   <summary>Reveal Manifest</summary>

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: gpu-app
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: gpu-app
     template:
       metadata:
         labels:
           app: gpu-app
       spec:
         containers:
         - name: gpu-container
           image: nvidia/cuda:11.0-base
           resources:
             limits:
               nvidia.com/gpu: 1
   ```
   </details>

2. Apply the manifest:
   ```bash
   kubectl apply -f <manifest-file>
   ```

3. Debug the issue:
   - Check pod status:
     ```bash
     kubectl get pods -l app=gpu-app
     ```
   - Describe the pod to find the cause:
     ```bash
     kubectl describe pod -l app=gpu-app
     ```
     Observe the message indicating no GPU nodes are available.

4. Resolve the issue:
   - Add GPU nodes to your cluster, or remove the GPU resource limits from the deployment if GPU is not required.

---

### 4. Rollout Restart the Deployment and Retrieve Logs from Deleted Pod

#### 4.1 Rollout Restart the Deployment
1. Perform a rollout restart for the `nginx` Deployment:
   ```bash
   kubectl rollout restart deployment nginx
   ```

2. Verify the new pod is created:
   ```bash
   kubectl get pods -l app=nginx
   ```

#### 4.2 Retrieve Logs from the Deleted Pod
1. Use the `--previous` flag to get logs from the deleted pod:
   ```bash
   kubectl logs <new-nginx-pod-name> --previous
   ```
   Replace `<new-nginx-pod-name>` with the name of the new NGINX pod.

2. Observe logs from the terminated container, including previous requests and errors.

---

### 5. Clean Up
1. Delete the deployments and resources:
   ```bash
   kubectl delete deployment nginx invalid-command gpu-app error-app
   kubectl delete service nginx
   ```

---

## Summary
In this lab, you:
- Created an NGINX deployment, sent requests, and analyzed logs to generate access and error logs (`4xx` and `5xx`).
- Debugged:
  - A Deployment with an invalid container command.
  - A GPU Deployment pending due to missing GPU nodes.
- Performed a rollout restart of the NGINX Deployment and retrieved logs from a deleted pod.
- Used `kubectl logs` and related commands for effective troubleshooting in Kubernetes workloads.
