Here is the updated lab guide using a `kubectl run` command with an `nginx:alpine` pod to test the services. This approach avoids port-forwarding and instead directly tests each service.

---

# Lab: Blue/Green Deployment Strategy in Kubernetes

## Objectives
- Implement a Blue/Green deployment strategy in Kubernetes.
- Deploy two versions of a sample application (`blue` and `green`).
- Test each deployment using a temporary pod.
- Route traffic to `blue` initially, then switch to `green` for a seamless upgrade.
- Learn how to manage multiple environments and control user traffic flow.

## Prerequisites
- A Kubernetes cluster (GKE recommended).
- `kubectl` and `ghcr.io` configured for container registry access.

## Steps

### Step 1: Create Blue and Green Deployments

1. **Create Blue Deployment**  
   Deploy version 1.0 of the application in the `blue` environment.

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: blue
     labels:
       app: helloworld
       role: blue
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: helloworld
         role: blue
     template:
       metadata:
         labels:
           app: helloworld
           role: blue
       spec:
         containers:
           - name: hello-app
             image: ghcr.io/hungtran84/hello-app:1.0
             ports:
               - containerPort: 8080
   ```

   Apply the `blue` deployment:

   ```bash
   kubectl apply -f blue-deployment.yaml
   ```

2. **Create Green Deployment**  
   Deploy version 2.0 of the application in the `green` environment.

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: green
     labels:
       app: helloworld
       role: green
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: helloworld
         role: green
     template:
       metadata:
         labels:
           app: helloworld
           role: green
       spec:
         containers:
           - name: hello-app
             image: ghcr.io/hungtran84/hello-app:2.0
             ports:
               - containerPort: 8080
   ```

   Apply the `green` deployment:

   ```bash
   kubectl apply -f green-deployment.yaml
   ```

### Step 2: Create Services

1. **Create Blue Service**  
   Expose the `blue` deployment internally within the cluster.

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: blue
   spec:
     selector:
       app: helloworld
       role: blue
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8080
   ```

   Apply the `blue` service:

   ```bash
   kubectl apply -f blue-service.yaml
   ```

2. **Create Green Service**  
   Expose the `green` deployment internally within the cluster.

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: green
   spec:
     selector:
       app: helloworld
       role: green
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8080
   ```

   Apply the `green` service:

   ```bash
   kubectl apply -f green-service.yaml
   ```

3. **Create Public Service**  
   Create a public-facing service that will initially route traffic to the `blue` deployment.

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: public
   spec:
     selector:
       app: helloworld
       role: blue
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8080
     type: LoadBalancer
   ```

   Apply the `public` service:

   ```bash
   kubectl apply -f public-service.yaml
   ```

### Step 3: Test Blue and Green Deployments

1. **Test Blue Deployment using Blue Service**  
   Run a temporary `nginx:alpine` pod to test the `blue` service:

   ```bash
   kubectl run test --image=nginx:alpine -it --rm --restart=Never -- curl blue
   ```

   This should return a response indicating version 1.0 of the application.

2. **Test Green Deployment using Green Service**  
   Run a temporary `nginx:alpine` pod to test the `green` service:

   ```bash
   kubectl run test --image=nginx:alpine -it --rm --restart=Never -- curl green
   ```

   This should return a response indicating version 2.0 of the application.

### Step 4: Verify Blue Deployment via Public Service

1. **Get the External IP**  
   Wait for the `public` service to get an external IP, then retrieve it.

   ```bash
   kubectl get svc public
   ```

2. **Test Public Service pointing to Blue**  
   Access the external IP in your browser or use `curl` to verify that version 1.0 is accessible.

   ```bash
   curl http://<EXTERNAL-IP>
   ```

   You should see output indicating version 1.0 of the application.

### Step 5: Switch Traffic to Green Deployment

1. **Update the Public Service Selector**  
   Modify the `public` service to point to the `green` deployment.

   ```bash
   kubectl label service public role=green --overwrite
   ```

2. **Test Public Service pointing to Green**  
   Access the external IP again to confirm that traffic is now routed to version 2.0.

   ```bash
   curl http://<EXTERNAL-IP>
   ```

   The output should now reflect version 2.0 of the application.

### Step 6: Clean Up Resources

To remove all resources created during this lab:

```bash
kubectl delete deployment blue
kubectl delete deployment green
kubectl delete svc blue
kubectl delete svc green
kubectl delete svc public
```

## Summary

In this lab, you implemented a Blue/Green deployment strategy in Kubernetes. You deployed two separate environments (`blue` and `green`) for the application, initially routing traffic to `blue`. After verifying the `green` deployment, you switched traffic to `green` by updating the `public` service selector, demonstrating how this strategy enables quick, low-risk application upgrades. Finally, you cleaned up all resources created in this lab.