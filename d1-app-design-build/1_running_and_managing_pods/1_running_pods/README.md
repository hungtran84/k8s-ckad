# Lab D1.1.1 - Running Pods

In this lab, we will explore how to create and manage pods in a Kubernetes cluster. We will start with basic pod operations, scale a deployment, and finally, create a static pod. This hands-on approach will help solidify the understanding of Kubernetes pod lifecycle events and interactions.

## Prerequisites
- A running Kubernetes cluster
- `kubectl` command-line tool configured to interact with your cluster

## 1. Monitoring Events
Start by monitoring the events in your Kubernetes cluster. This will allow you to see the lifecycle events for pods as they are created and managed.

```bash
kubectl get events --watch &
```

## 2. Creating a Pod
Next, we will create a simple pod by applying a manifest file named `pod.yaml`. This pod will run a container from an image hosted on GitHub Container Registry.

### Create `pod.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world-pod
spec:
  containers:
  - name: hello-world
    image: ghcr.io/hungtran84/hello-app:1.0
    ports:
    - containerPort: 80
```

### Apply the Pod Manifest

```bash
kubectl apply -f pod.yaml
```

You should see events similar to the following:

```
0s          Normal    Scheduled                 pod/hello-world-pod   Successfully assigned default/hello-world-pod to node5
0s          Normal    Pulling                   pod/hello-world-pod   Pulling image "ghcr.io/hungtran84/hello-app:1.0"
0s          Normal    Pulled                    pod/hello-world-pod   Successfully pulled image "ghcr.io/hungtran84/hello-app:1.0" in 3.584474683s (3.584491183s including waiting)
0s          Normal    Created                   pod/hello-world-pod   Created container hello-world
0s          Normal    Started                   pod/hello-world-pod   Started container hello-world
```

## 3. Creating a Deployment
Now, let's create a deployment with one replica. A deployment manages a replica set and can scale the number of replicas.

### Create `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
  selector:
    matchLabels:
      run: hello-world
  template:
    metadata:
      labels:
        run: hello-world
    spec:
      containers:
      - name: hello-world
        image: ghcr.io/hungtran84/hello-app:1.0
        ports:
        - containerPort: 80
```

### Apply the Deployment Manifest

```bash
kubectl apply -f deployment.yaml
```

You should see events indicating the deployment creation and the scaling of the replica set:

```
0s          Normal    ScalingReplicaSet         deployment/hello-world   Scaled up replica set hello-world-6d59dfc665 to 1
0s          Normal    SuccessfulCreate          replicaset/hello-world-6d59dfc665   Created pod: hello-world-6d59dfc665-mzhdq
```

## 4. Scaling the Deployment
Next, we will scale the deployment to 2 replicas.

```bash
kubectl scale deployment hello-world --replicas=2
```

The output will indicate the scaling of the replica set and the creation of the second pod:

```
0s          Normal    ScalingReplicaSet         deployment/hello-world   Scaled up replica set hello-world-6d59dfc665 to 2 from 1
0s          Normal    SuccessfulCreate          replicaset/hello-world-6d59dfc665   Created pod: hello-world-6d59dfc665-v9bbz
```

## 5. Deleting a Pod
Let's scale down the deployment to 1 replica, which will trigger the deletion of the second pod.

```bash
kubectl scale deployment hello-world --replicas=1
```

You will see events related to scaling down and killing the pod:

```
0s          Normal    ScalingReplicaSet         deployment/hello-world   Scaled down replica set hello-world-6d59dfc665 to 1 from 2
0s          Normal    Killing                   pod/hello-world-6d59dfc665-v9bbz   Stopping container hello-world
```

## 6. Executing Commands in a Pod
You can also execute commands within a running container of a pod.

### Get the Running Pods

```bash
kubectl get pods
```

### Execute a Shell in the Pod

```bash
kubectl exec -it hello-world-pod -- /bin/sh
```

Inside the pod, you can run commands like `ps` to check running processes:

```bash
/app # ps
PID   USER     TIME  COMMAND
    1 root      0:00 ./hello-app
   11 root      0:00 /bin/sh
```

### Exit the Pod Shell

```bash
exit
```

## 7. Port Forwarding to Access the Application
To access the application running in the pod directly, you can set up port forwarding.

```bash
kubectl port-forward hello-world-pod 8080:8080 &
```

You can now send requests to your application:

```bash
curl http://localhost:8080
```

You should receive a response similar to:

```
Hello, world!
Version: 1.0.0
hello-world-pod
```

### Terminate Port Forwarding
To stop the port forwarding, use:

```bash
fg
ctrl+c
```

## 8. Cleanup Resources
Finally, clean up the resources created during the lab.

```bash
kubectl delete deployment hello-world
kubectl delete pod hello-world-pod
```

Stop the events monitoring:

```bash
fg
ctrl+c
```

## 9. Creating Static Pods
Now we will create a static pod. This type of pod is managed directly by the kubelet on the node and does not go through the API server.

### Create Static Pod Manifest
Create a pod manifest using `kubectl run` with dry-run and output it in YAML format.

```bash
kubectl run hello-world --image=ghcr.io/hungtran84/hello-app:2.0 --dry-run=client -o yaml --port=8080
```

Expected output:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: hello-world
  name: hello-world
spec:
  containers:
  - image: ghcr.io/hungtran84/hello-app:2.0
    name: hello-world
    ports:
    - containerPort: 8080
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

### Find Static Pod Path
Log into one of the nodes and find the static pod path in the kubelet configuration.

```bash
gcloud compute ssh node2 --zone asia-southeast1-c
```

```bash
[node2 ~]$ cat /var/lib/kubelet/config.yaml
```

You should see an entry for `staticPodPath`, typically set to `/etc/kubernetes/manifests`.

### Create the Static Pod Manifest
Create a new file in the static pod path:

```bash
sudo nano /etc/kubernetes/manifests/mypod.yaml
```

Paste the following pod definition:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: hello-world
  name: hello-world
spec:
  containers:
  - image: ghcr.io/hungtran84/hello-app:2.0
    name: hello-world
    ports:
    - containerPort: 8080
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Press Ctr+E to Exist and hit Y to save the file.

## 10. Verify the Static Pod
Log out of the node and back into the Cloudshell. List the pods to see the static pod created.

```bash
kubectl get pods -o wide
```

You should see the static pod listed with a name that includes the node name:

```
hello-world-node2   1/1     Running   0          99s   10.5.1.4   node2   <none>           <none>
```

### Deleting the Static Pod
Attempt to delete the static pod:

```bash
kubectl delete pod hello-world-node2
```

Check the list of pods again
```sh
kubectl get pods -o wide
```

Notice that it remains running. This is because static pods are managed by the kubelet and cannot be deleted via `kubectl`.

### Remove the Static Pod Manifest
Log into the node where the static pod is running and delete the manifest:

```bash
[node2 ~]$ rm /etc/kubernetes/manifests/mypod.yaml
```

Switch back to the Cloudshell and check the pods again:

```bash
kubectl get pods
```

You should see that the static pod is no longer present.

## Conclusion
In this lab, we have learned how to create, scale, and manage pods in a Kubernetes environment. We also explored the differences between regular deployments and static pods, enhancing our understanding of Kubernetes pod lifecycle and management.
