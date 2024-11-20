# Lab: Passing Configuration into Containers using Environment Variables

## Objectives

- Understand how environment variables are passed into containers in Kubernetes.
- Observe how services dynamically update environment variables in Pods.
- Learn the effect of recreating Pods and services on environment variables.

## Steps

### Step 1: Create Deployments and Services
1. Apply the deployment manifests to create two deployments: one for a database system and another for the application.

   ```bash
   kubectl apply -f deployment-alpha.yaml
   # Output:
   # deployment.apps/hello-world-alpha created
   # service/hello-world-alpha created

   kubectl apply -f deployment-beta.yaml
   # Output:
   # deployment.apps/hello-world-beta created
   # service/hello-world-beta created
   ```

### Step 2: Verify Services
2. List the services to verify they were created:

   ```bash
   kubectl get service
   # Output:
   # NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
   # hello-world-alpha   ClusterIP   10.32.12.208   <none>        80/TCP    85s
   # hello-world-beta    ClusterIP   10.32.10.122   <none>        80/TCP    60s
   # kubernetes          ClusterIP   10.32.0.1      <none>        443/TCP   6d16h
   ```

### Step 3: Retrieve Pod Name
3. Get the name of one of the Pods in the `hello-world-alpha` deployment:

   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-alpha | awk '{print $1}' | head -n 1)
   echo $PODNAME
   # Example Output: hello-world-alpha-757d4b95c4-2khvs
   ```

### Step 4: Examine Environment Variables
4. Inside the Pod, check the environment variables. Note that only the `alpha` service information is present:

   ```bash
   kubectl exec -it $PODNAME -- printenv | sort
   ```

   Example Output (abbreviated):

   ```text
   HELLO_WORLD_ALPHA_SERVICE_HOST=10.32.15.46
   HELLO_WORLD_ALPHA_SERVICE_PORT=80
   ```

### Step 5: Recreate the Pod
5. Delete the existing Pod and let it be recreated:

   ```bash
   kubectl delete pod $PODNAME
   ```

6. Get the new Pod name and check its environment variables. Notice that both `alpha` and `beta` service information are now present:

   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-alpha | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- printenv | sort
   ```

   Example Output (abbreviated):

   ```text
   HELLO_WORLD_ALPHA_SERVICE_HOST=10.32.15.46
   HELLO_WORLD_BETA_SERVICE_HOST=10.32.2.164
   ```

### Step 6: Delete a Service and Deployment
7. Delete the `hello-world-beta` deployment and service:

   ```bash
   kubectl delete deployment hello-world-beta
   kubectl delete service hello-world-beta
   ```

8. Check the environment variables again. The `beta` service variables remain until the Pod is recreated:

   ```bash
   kubectl exec -it $PODNAME -- printenv | sort
   ```

   Example Output (abbreviated):

   ```text
   HELLO_WORLD_BETA_SERVICE_HOST=10.32.2.164
   ```

### Step 7: Cleanup
9. Clean up resources by deleting the `hello-world-alpha` deployment:

   ```bash
   kubectl delete -f deployment-alpha.yaml
   ```

## Summary

- Environment variables for services are injected at Pod creation.
- Changes in services (e.g., deletion) do not immediately reflect in existing Pods.
- Recreating Pods ensures they have the most up-to-date environment variables.
