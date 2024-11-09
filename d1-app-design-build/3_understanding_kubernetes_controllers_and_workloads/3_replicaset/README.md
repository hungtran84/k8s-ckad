# Kubernetes ReplicaSet Lab Guide

## Objectives

In this lab, you will:
- Deploy a Deployment that automatically creates a ReplicaSet.
- Explore how ReplicaSets manage and maintain the desired state of Pods.
- Learn about ReplicaSet selectors, labels, and self-healing.
- Modify and isolate Pods within a ReplicaSet.
- Test ReplicaSet behavior under node failures to understand fault tolerance in Kubernetes.

This lab provides a hands-on opportunity to understand how Kubernetes ensures application availability through ReplicaSets. By the end, you'll be familiar with deployment strategies, the role of labels in managing replicas, and Kubernetes' resilience in handling node and pod failures.

## Steps

### Step 1: Deploy a Deployment and Observe the ReplicaSet

1. Apply the deployment manifest to create a Deployment and its associated ReplicaSet:
   ```bash
   kubectl apply -f deployment.yaml
   ```
   Expected output:
   ```plaintext
   deployment.apps/hello-world created
   service/hello-world created
   ```

2. Verify that a ReplicaSet has been created and inspect its status:
   ```bash
   kubectl get replicaset
   ```
   Example output:
   ```plaintext
   NAME                     DESIRED   CURRENT   READY   AGE
   hello-world-5c7b5b8dfd   5         5         5       2s
   ```

### Step 2: Examine ReplicaSet Selectors and Labels

1. View details of the ReplicaSet, including selectors, labels, and pod template:
   ```bash
   kubectl describe replicaset hello-world
   ```
   Key information includes:
   - `Selector`: Controls the labels used to match Pods for this ReplicaSet.
   - `Labels`: Applied to Pods created by the ReplicaSet.
   - `Pods Status`: Confirms if the ReplicaSet maintains the desired number of Pods running.

### Step 3: Delete the Deployment and Observe the ReplicaSet

1. Delete the Deployment, which will also remove the ReplicaSet and its Pods:
   ```bash
   kubectl delete deployment hello-world
   ```
2. Confirm the ReplicaSet has been deleted:
   ```bash
   kubectl get replicaset
   ```
   Expected output:
   ```plaintext
   No resources found in default namespace.
   ```

### Step 4: Deploy a ReplicaSet with Match Expressions

1. Apply a new deployment using `matchExpressions` to specify complex matching conditions:
   ```bash
   kubectl apply -f deployment-me.yaml
   ```
   Example output:
   ```plaintext
   deployment.apps/hello-world created
   service/hello-world-pod created
   ```

2. Verify the status of the new ReplicaSet:
   ```bash
   kubectl get replicaset
   ```
3. Inspect the selectors and labels for the new ReplicaSet:
   ```bash
   kubectl describe replicaset hello-world
   ```

### Step 5: Test Self-Healing by Deleting a Pod

1. View the list of Pods managed by the ReplicaSet:
   ```bash
   kubectl get pods
   ```
2. Delete one of the Pods and observe Kubernetes’ self-healing behavior:
   ```bash
   kubectl delete pods <pod-name>
   ```
3. Verify a new Pod is created to maintain the desired replica count:
   ```bash
   kubectl get pods
   ```

### Step 6: Isolate a Pod from the ReplicaSet

1. Check the labels for all Pods:
   ```bash
   kubectl get pods --show-labels
   ```
2. Modify the label on a Pod to isolate it from the ReplicaSet’s scope:
   ```bash
   kubectl label pod <pod-name> app=DEBUG --overwrite
   ```
3. Observe the ReplicaSet creating a new Pod to meet the replica requirement:
   ```bash
   kubectl get pods --show-labels
   ```

### Step 7: Re-integrate an Isolated Pod into the ReplicaSet

1. Reapply the original label to the isolated Pod:
   ```bash
   kubectl label pod <pod-name> app=hello-world-pod-me --overwrite
   ```
2. Observe that the ReplicaSet terminates the extra Pod to maintain the desired replica count:
   ```bash
   kubectl get pods --show-labels
   ```

### Step 8: Simulate Node Failure and Observe ReplicaSet Resilience

1. Shut down one of the nodes:
   ```bash
   sudo shutdown -h now
   ```
2. Wait a minute and then check node status:
   ```bash
   kubectl get nodes
   ```
3. Verify if the ReplicaSet relocates the affected Pod to maintain availability.

## Summary

In this lab, you deployed and managed Kubernetes ReplicaSets to maintain application availability, learned about label selectors and pod templates, and observed the self-healing and resilience features of Kubernetes. By isolating, re-integrating, and managing node failures, you demonstrated how Kubernetes ensures a stable, reliable application state, adapting to changes in real-time. These concepts are foundational for managing distributed, resilient applications in a production environment.
