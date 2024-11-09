# Working with Kubernetes Labels and Selectors

## Objectives
In this lab, you will:
- Create and manage a collection of pods with labels.
- Query and manipulate labels to filter and display pods.
- Apply labels to Kubernetes resources, including Deployments, ReplicaSets, and Services.

## Steps

### 1. Create a Collection of Pods with Labels
To begin, we will create multiple pods and assign labels to each.

```yaml
# CreatePodsWithLabels.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-1
  labels: 
    app: MyWebApp
    deployment: v1
    tier: prod
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-2
  labels: 
    app: MyWebApp
    deployment: v1.1
    tier: prod
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-3
  labels: 
    app: MyWebApp
    deployment: v1.1
    tier: qa
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-4
  labels: 
    app: MyAdminApp
    deployment: v1
    tier: prod
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
```

```shell
kubectl apply -f CreatePodsWithLabels.yaml
```

Expected output:
```plaintext
pod/nginx-pod-1 created
pod/nginx-pod-2 created
pod/nginx-pod-3 created
pod/nginx-pod-4 created
```

### 2. View All Pod Labels in the Cluster
Use the following command to see all pod labels:

```shell
kubectl get pods --show-labels
```

Expected output:
```plaintext
NAME          READY   STATUS    RESTARTS   AGE   LABELS
nginx-pod-1   1/1     Running   0          32s   app=MyWebApp,deployment=v1,tier=prod
nginx-pod-2   1/1     Running   0          32s   app=MyWebApp,deployment=v1.1,tier=prod
nginx-pod-3   1/1     Running   0          32s   app=MyWebApp,deployment=v1.1,tier=qa
nginx-pod-4   1/1     Running   0          32s   app=MyAdminApp,deployment=v1,tier=prod
```

### 3. View Labels of a Specific Pod
To see detailed labels for a single pod:

```shell
kubectl describe pod nginx-pod-1 | head
```

### 4. Query Pods by Labels and Selectors
List pods with specific labels:

```shell
kubectl get pods --selector tier=prod
kubectl get pods --selector tier=qa
kubectl get pods -l tier=prod --show-labels
```

Use multiple label filters with `--show-labels`:

```shell
kubectl get pods -l 'tier=prod,app=MyWebApp' --show-labels
```

### 5. Display Labels in Column Format
Output a particular label in column format:

```shell
kubectl get pods -L tier
kubectl get pods -L tier,app
```

### 6. Modify Pod Labels
Edit an existing label:

```shell
kubectl label pod nginx-pod-1 tier=non-prod --overwrite
kubectl get pod nginx-pod-1 --show-labels
```

Add a new label:

```shell
kubectl label pod nginx-pod-1 another=Label
```

Remove an existing label:

```shell
kubectl label pod nginx-pod-1 another-
```

### 7. Apply Label to Multiple Pods
Apply a label to all pods in the default namespace:

```shell
kubectl label pod --all tier=non-prod --overwrite
kubectl get pod --show-labels
```

### 8. Delete Pods Based on Label
Delete all pods matching a specific label:

```shell
kubectl delete pod -l tier=non-prod
kubectl get pods --show-labels
```

### 9. Kubernetes Resource Management
Create a Deployment with labels:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
  labels:
    app: hello-world
spec:
  replicas: 4
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
```

```shell
kubectl apply -f deployment-label.yaml
```

Expose the Deployment as a Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: hello-world
```

```shell
kubectl apply -f service.yaml
```

Verify labels on Deployment, ReplicaSet, and Pods:

```shell
kubectl describe deployment hello-world
kubectl describe replicaset hello-world
kubectl get pods --show-labels
```

- Look at the `Labels` and `Selectors` on each resource, the `Deployment`, `ReplicaSet` and `Pod`
The deployment has a selector for `app=hello-world`
```
kubectl describe deployment hello-world

Name:                   hello-world
Namespace:              default
CreationTimestamp:      Sun, 13 Aug 2023 14:52:28 +0700
Labels:                 app=hello-world
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=hello-world
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=hello-world
  Containers:
   hello-world:
    Image:        ghcr.io/hungtran84/hello-app:1.0
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   hello-world-6d59dfc665 (4/4 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  88s   deployment-controller  Scaled up replica set hello-world-6d59dfc665 to 4
```

- The `ReplicaSet` has labels and selectors for app and the current pod-template-hash
Look at the `Pod Template` and the labels on the Pods created
```
kubectl describe replicaset hello-world

Name:           hello-world-6d59dfc665
Namespace:      default
Selector:       app=hello-world,pod-template-hash=6d59dfc665
Labels:         app=hello-world
                pod-template-hash=6d59dfc665
Annotations:    deployment.kubernetes.io/desired-replicas: 4
                deployment.kubernetes.io/max-replicas: 5
                deployment.kubernetes.io/revision: 1
Controlled By:  Deployment/hello-world
Replicas:       4 current / 4 desired
Pods Status:    4 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=hello-world
           pod-template-hash=6d59dfc665
  Containers:
   hello-world:
    Image:        ghcr.io/hungtran84/hello-app:1.0
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  2m8s  replicaset-controller  Created pod: hello-world-6d59dfc665-k8lth
  Normal  SuccessfulCreate  2m8s  replicaset-controller  Created pod: hello-world-6d59dfc665-tx8g2
  Normal  SuccessfulCreate  2m8s  replicaset-controller  Created pod: hello-world-6d59dfc665-rcr2r
  Normal  SuccessfulCreate  2m8s  replicaset-controller  Created pod: hello-world-6d59dfc665-pmjmc
```
- The Pods have labels for `app=hello-world` and for the `pod-temlpate-hash` of the current `ReplicaSet`
```
kubectl get pods --show-labels

NAME                           READY   STATUS    RESTARTS   AGE     LABELS
hello-world-6d59dfc665-k8lth   1/1     Running   0          3m21s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-pmjmc   1/1     Running   0          3m21s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-rcr2r   1/1     Running   0          3m21s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-tx8g2   1/1     Running   0          3m21s   app=hello-world,pod-template-hash=6d59dfc665
```
- Edit the label on one of the Pods in the `ReplicaSet`, change the `pod-template-hash`
```
kubectl label pod hello-world-6d59dfc665-k8lth pod-template-hash=DEBUG --overwrite
pod/hello-world-6d59dfc665-k8lth labeled
```

- The ReplicaSet will deploy a new Pod to satisfy the number of replicas. Our relabeled Pod still exists.
```
kubectl get pods --show-labels

NAME                           READY   STATUS    RESTARTS   AGE     LABELS
hello-world-6d59dfc665-k8lth   1/1     Running   0          4m48s   app=hello-world,pod-template-hash=DEBUG
hello-world-6d59dfc665-pmjmc   1/1     Running   0          4m48s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-rcr2r   1/1     Running   0          4m48s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-rk729   1/1     Running   0          28s     app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-tx8g2   1/1     Running   0          4m48s   app=hello-world,pod-template-hash=6d59dfc665
```
- Let's look at how `Services` use `labels` and `selectors`, check out services.yaml
```
kubectl get service

NAME          TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
hello-world   ClusterIP   10.32.6.179   <none>        80/TCP    4m40s
kubernetes    ClusterIP   10.32.0.1     <none>        443/TCP   15h
```

- The `selector` for this serivce is `app=hello-world`, that pod is still being load balanced to!
```
kubectl describe service hello-world 
Name:              hello-world
Namespace:         default
Labels:            <none>
Annotations:       cloud.google.com/neg: {"ingress":true}
Selector:          app=hello-world
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.32.6.179
IPs:               10.32.6.179
Port:              <unset>  80/TCP
TargetPort:        8080/TCP
Endpoints:         10.28.0.15:8080,10.28.0.16:8080,10.28.0.17:8080 + 2 more...
Session Affinity:  None
Events:            <none>
```

- Get a list of all IPs in the service, there's 5,why?
```
kubectl describe endpoints hello-world
Name:         hello-world
Namespace:    default
Labels:       <none>
Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2023-08-13T07:56:49Z
Subsets:
  Addresses:          10.28.0.15,10.28.0.16,10.28.0.17,10.28.1.9,10.28.2.16
  NotReadyAddresses:  <none>
  Ports:
    Name     Port  Protocol
    ----     ----  --------
    <unset>  8080  TCP

Events:  <none>
```

- Get a list of pods and their IPs
```
kubectl get pod -o wide

NAME                           READY   STATUS    RESTARTS   AGE     IP           NODE                                      NOMINATED NODE   READINESS GATES
hello-world-6d59dfc665-k8lth   1/1     Running   0          7m19s   10.28.0.15   gke-gke-test-default-pool-03d0c6b2-sv8f   <none>           <none>
hello-world-6d59dfc665-pmjmc   1/1     Running   0          7m19s   10.28.0.16   gke-gke-test-default-pool-03d0c6b2-sv8f   <none>           <none>
hello-world-6d59dfc665-rcr2r   1/1     Running   0          7m19s   10.28.2.16   gke-gke-test-default-pool-03d0c6b2-bfk0   <none>           <none>
hello-world-6d59dfc665-rk729   1/1     Running   0          2m59s   10.28.0.17   gke-gke-test-default-pool-03d0c6b2-sv8f   <none>           <none>
hello-world-6d59dfc665-tx8g2   1/1     Running   0          7m19s   10.28.1.9    gke-gke-test-default-pool-03d0c6b2-n7l2   <none>           <none>
```

- To remove a pod from load balancing, change the label used by the service's selector.
The ReplicaSet will respond by placing another pod in the ReplicaSet
```
kubectl get pods --show-labels
NAME                           READY   STATUS    RESTARTS   AGE     LABELS
hello-world-6d59dfc665-k8lth   1/1     Running   0          7m47s   app=hello-world,pod-template-hash=DEBUG
hello-world-6d59dfc665-pmjmc   1/1     Running   0          7m47s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-rcr2r   1/1     Running   0          7m47s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-rk729   1/1     Running   0          3m27s   app=hello-world,pod-template-hash=6d59dfc665
hello-world-6d59dfc665-tx8g2   1/1     Running   0          7m47s   app=hello-world,pod-template-hash=6d59dfc665

kubectl label pod hello-world-6d59dfc665-k8lth app=DEBUG --overwrite
pod/hello-world-6d59dfc665-k8lth labeled
```

- Look at the registered endpoint addresses. Now there's 4
```
kubectl describe endpoints hello-world
```

- To clean up, delete the deployment, service and the Pod removed from the replicaset
```
kubectl delete deployment hello-world
kubectl delete service hello-world
kubectl delete pod hello-world-6d59dfc665-k8lth
```

### 10. Scheduling Pods

Scheduling is a deeper topic in Kubernetes, but here we will focus on how labels can be used to influence it.

1. **Check Current Node Labels:**
   To see the current labels on your nodes, you can use:
   ```bash
   kubectl get nodes --show-labels
   ```

2. **Label Your Nodes:**
   You can label your nodes with descriptive tags to help with scheduling:
   ```bash
   kubectl label node <node1> disk=local_ssd
   kubectl label node <node2> hardware=local_gpu
   ```

3. **Confirm Your Labels:**
   Query the nodes again to confirm that the labels have been applied:
   ```bash
   kubectl get node -L disk,hardware
   ```

   Example output:
   ```
   NAME                                      STATUS   ROLES    AGE   VERSION           DISK        HARDWARE
   gke-gke-test-default-pool-03d0c6b2-bfk0   Ready    <none>   15h   v1.27.3-gke.100   local_ssd   
   gke-gke-test-default-pool-03d0c6b2-n7l2   Ready    <none>   15h   v1.27.3-gke.100               local_gpu
   gke-gke-test-default-pool-03d0c6b2-sv8f   Ready    <none>   15h   v1.27.3-gke.100               
   ```

4. **Create Pods with Node Selectors:**
   Next, create three pods, with two using `nodeSelector` and one without:
   ```yaml
   cat PodsToNodes.yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-pod-ssd
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
     nodeSelector:
       disk: local_ssd
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-pod-gpu
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
     nodeSelector:
       hardware: local_gpu
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-pod
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
   ```

5. **Apply the Pod Configuration:**
   Apply the configurations to create the pods:
   ```bash
   kubectl apply -f PodsToNodes.yaml
   ```

6. **View the Scheduling of the Pods:**
   Check which nodes the pods have been scheduled on:
   ```bash
   kubectl get node -L disk,hardware
   ```

   And to see pod details:
   ```bash
   kubectl get pods -o wide
   ```

   Example output for pods:
   ```
   NAME                           READY   STATUS    RESTARTS   AGE   IP           NODE                                      NOMINATED NODE   READINESS GATES
   hello-world-6d59dfc665-k8lth   1/1     Running   0          20m   10.28.0.15   gke-gke-test-default-pool-03d0c6b2-sv8f   <none>           <none>
   nginx-pod                      1/1     Running   0          39s   10.28.0.18   gke-gke-test-default-pool-03d0c6b2-sv8f   <none>           <none>
   nginx-pod-gpu                  1/1     Running   0          39s   10.28.1.10   gke-gke-test-default-pool-03d0c6b2-n7l2   <none>           <none>
   nginx-pod-ssd                  1/1     Running   0          40s   10.28.2.17   gke-gke-test-default-pool-03d0c6b2-bfk0   <none>           <none>
   ```

7. **Clean Up:**
   Once you're finished, it's good practice to clean up by removing the labels and the pods:
   ```bash
   kubectl label node <node1> disk-
   kubectl label node <node2> hardware-
   kubectl delete pod nginx-pod
   kubectl delete pod nginx-pod-gpu
   kubectl delete pod nginx-pod-ssd
   ```

## Summary
In this lab, you created and managed labels on Kubernetes resources, enabling advanced filtering and querying.

## The Role of Labels in Kubernetes

Labels in Kubernetes are key-value pairs applied to resources to enhance organization, selection, and automation. They are essential for the functioning of controllers, which rely on labels to manage and control associated resources effectively.

### Key Use Cases for Labels

1. **Organizing Resources by Application**
   - Labels group resources under an app (e.g., `app: frontend`), simplifying updates and management of related resources.

2. **Environment-Based Management**
   - Use labels like `environment: production` or `environment: dev` to separate resources across environments, minimizing accidental updates.

3. **Version Control**
   - Labels like `version: v1` allow for easy version management, enabling canary releases, A/B testing, and rolling updates.

4. **Label Selectors for Resource Querying**
   - Label selectors enable filtering of resources based on specific criteria (e.g., `kubectl get pods -l app=frontend`), making it easier to retrieve and manage related resources.

5. **Controller Management**
   - Controllers, such as Deployments and ReplicaSets, use labels to track the Pods they manage. For instance, a Deployment will match Pods with a specific label to ensure the desired state is maintained.

6. **Resource Affinity Rules**
   - Labels enable affinity and anti-affinity rules for pod placement, helping balance loads and reduce latency.

7. **Tracking Ownership**
   - Labels like `owner: teamA` indicate responsibility, improving accountability in shared clusters.

8. **Cost Allocation**
   - Labels with tags such as `cost-center: project123` help track resource costs across projects and teams.

9. **Monitoring and Alerting**
   - Labels integrate with monitoring tools, allowing tailored alerts for resources with tags like `criticality: high`.

### Practical Tips for Label Management

- **Standardize Labeling**: Use consistent labels (e.g., `app`, `env`, `version`) to simplify queries.
- **Avoid Over-Labeling**: Apply labels that provide value without creating excessive tags.
- **Automate with Tools**: Manage labels consistently across environments using tools like Helm or Kustomize.

## Conclusion
Labels are crucial for managing Kubernetes resources, particularly in the context of controllers that depend on labels to maintain the desired state of applications. By leveraging labels effectively, teams can optimize operations and streamline resource management.
