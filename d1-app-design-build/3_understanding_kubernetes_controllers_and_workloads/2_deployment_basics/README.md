# Lab: Creating a Deployment Imperatively

## Objectives
In this lab, you will learn how to create a Kubernetes deployment imperatively using `kubectl create`. This method allows you to specify important parameters such as the image, container ports, and replica count directly in the command line. By the end of the lab, you'll understand how to:
- Create a deployment with specified container images and replicas.
- Scale deployments.
- Combine commands for more efficient workflow.
- Check the status of deployments and clean up resources.

## Steps

### Step 1: Create a Deployment
Use the `kubectl create deployment` command to create a deployment with a specified container image.

```bash
kubectl create deployment hello-world --image=ghcr.io/hungtran84/hello-app:1.0
```

Expected output:
```
deployment.apps/hello-world created
```

### Step 2: Scale the Deployment
After creating the deployment, you can scale it to run multiple replicas.

```bash
kubectl scale deployment hello-world --replicas=5
```

Expected output:
```
deployment.apps/hello-world scaled
```

### Step 3: Create a Deployment with Combined Parameters
You can combine deployment creation and scaling into a single command by specifying the replica count when creating the deployment.

```bash
kubectl create deployment hello-world1 --image=ghcr.io/hungtran84/hello-app:1.0 --replicas=5
```

Expected output:
```
deployment.apps/hello-world1 created
```

### Step 4: Verify the Deployment Status
Check the status of your deployments to confirm they are running the specified number of replicas.

```bash
kubectl get deployment
```

Expected output:
```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
hello-world    5/5     5            5           2m22s
hello-world1   5/5     5            5           55s
```

### Step 5: Clean Up Resources
To remove the deployments, use the `kubectl delete deployment` command.

```bash
kubectl delete deployment hello-world hello-world1
```

Expected output:
```
deployment.apps "hello-world" deleted
deployment.apps "hello-world1" deleted
```

## Summary
In this lab, you learned how to create and manage Kubernetes deployments using imperative commands. You created a deployment, scaled it, and combined options for efficient command usage. Additionally, you verified the deployment status and performed a cleanup of the resources created. This approach is helpful for quick deployments without needing YAML configuration files, especially for testing and prototyping in Kubernetes environments.