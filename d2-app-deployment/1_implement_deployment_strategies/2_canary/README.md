# Lab: Canary Deployment Strategy in Kubernetes

## Objectives
- Implement a Canary deployment strategy in Kubernetes.
- Deploy two versions of a sample application (`stable` and `canary`).
- Use replica management to gradually shift traffic from the stable to the canary version.
- Understand how to manage a gradual rollout for low-risk application upgrades.

## Prerequisites
- A Kubernetes cluster (GKE recommended).
- `kubectl` and `ghcr.io` configured for container registry access.

## Steps

### Step 1: Create Stable and Canary Deployments

1. **Create Stable Deployment**  
   Deploy version 1.0 of the application in the `stable` environment with 4 replicas.

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: stable
     labels:
       app: helloworld
       role: stable
   spec:
     replicas: 4
     selector:
       matchLabels:
         app: helloworld
     template:
       metadata:
         labels:
           app: helloworld
           role: stable
       spec:
         containers:
           - name: hello-app
             image: ghcr.io/hungtran84/hello-app:1.0
             ports:
               - containerPort: 8080
   ```

   Apply the `stable` deployment:

   ```bash
   kubectl apply -f stable-deployment.yaml
   ```

2. **Create Canary Deployment**  
   Deploy version 2.0 of the application in the `canary` environment, starting with 1 replica (20% of total traffic).

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: canary
     labels:
       app: helloworld
       role: canary
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: helloworld
     template:
       metadata:
         labels:
           app: helloworld
           role: canary
       spec:
         containers:
           - name: hello-app
             image: ghcr.io/hungtran84/hello-app:2.0
             ports:
               - containerPort: 8080
   ```

   Apply the `canary` deployment:

   ```bash
   kubectl apply -f canary-deployment.yaml
   ```

### Step 2: Create LoadBalancer Service

Create a LoadBalancer service that will direct traffic to both the `stable` and `canary` deployments based on their shared `app` label.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: helloworld
spec:
  selector:
    app: helloworld
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

Apply the `helloworld` service:

```bash
kubectl apply -f helloworld-service.yaml
```

### Step 3: Verify Initial Traffic Split

1. **Get the External IP**  
   Wait for the `helloworld` service to obtain an external IP, then retrieve it:

   ```bash
   kubectl get svc helloworld
   ```

2. **Test Initial Traffic**  
   Use `curl` or a browser to access the external IP. Initially, about 80% of requests should reach the `stable` deployment, while 20% should reach the `canary` deployment.

   ```bash
   curl http://<EXTERNAL-IP>
   ```

3. **Observe Replica Distribution**  
   To confirm traffic distribution, you can scale up and down the `stable` and `canary` deployments and monitor their response rates.

### Step 4: Gradually Increase Canary Deployment

1. **Increase Canary Replicas to 40% Traffic (2 Replicas)**  
   Scale the `canary` deployment up by 1 replica and reduce the `stable` deployment by 1 replica to keep the total count at 5.

   ```bash
   kubectl scale deployment canary --replicas=2
   kubectl scale deployment stable --replicas=3
   ```

   Verify the new traffic distribution by making requests to the `helloworld` service:

   ```bash
   curl http://<EXTERNAL-IP>
   ```

   With 2 replicas for `canary` and 3 for `stable`, the canary version should now handle approximately 40% of the traffic.

2. **Increase Canary to 60% Traffic (3 Replicas)**  
   Continue increasing canary’s share by adjusting the replicas:

   ```bash
   kubectl scale deployment canary --replicas=3
   kubectl scale deployment stable --replicas=2
   ```

3. **Increase Canary to 80% Traffic (4 Replicas)**  
   When confident in the canary version, scale the deployments again:

   ```bash
   kubectl scale deployment canary --replicas=4
   kubectl scale deployment stable --replicas=1
   ```

4. **Complete the Rollout (100% Canary)**  
   Finally, scale down the `stable` deployment to zero, directing all traffic to the `canary` version.

   ```bash
   kubectl scale deployment canary --replicas=5
   kubectl scale deployment stable --replicas=0
   ```

### Step 5: Clean Up Resources

To remove all resources created during this lab:

```bash
kubectl delete deployment stable
kubectl delete deployment canary
kubectl delete svc helloworld
```

## Summary

In this lab, you implemented a Canary deployment strategy in Kubernetes, allowing you to gradually shift traffic from a stable deployment to a canary deployment. By using replica scaling, you were able to control traffic distribution and incrementally route users to the new version, ensuring a low-risk deployment with the option to roll back if needed.