# Lab: Creating and Managing DaemonSets in Kubernetes

## Objectives
- Create a DaemonSet that runs a Pod on each Node in a cluster.
- Apply a `nodeSelector` to target a subset of Nodes.
- Update an existing DaemonSet and observe its rolling update strategy.

---

## Steps

### 1. Creating a DaemonSet on All Nodes

A DaemonSet ensures that a single Pod is running on each Node in a Kubernetes cluster, useful for network services that need to operate on every Node.

1. **List the Nodes in the cluster:**
   ```shell
   kubectl get nodes
   ```
   Example output:
   ```
   NAME    STATUS   ROLES           AGE     VERSION
   node1   Ready    control-plane   2m39s   v1.27.2
   node2   Ready    <none>          2m11s   v1.27.2
   node3   Ready    <none>          2m7s    v1.27.2
   node4   Ready    <none>          2m5s    v1.27.2
   node5   Ready    <none>          2m2s    v1.27.2
   ```

2. **Check existing DaemonSets in the `kube-system` namespace:**
   ```shell
   kubectl get daemonsets --namespace kube-system kube-proxy
   ```

   **Output:**
   ```plaintext
    NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
    kube-proxy   3         3         3       3            3           kubernetes.io/os=linux   9d
   ```

3. **Create a new DaemonSet for our `hello-world` app:**
   ```shell
   kubectl apply -f DaemonSet.yaml
   ```

4. **Verify that the DaemonSet has deployed a Pod to each worker Node:**
   ```shell
   kubectl get daemonsets
   ```

   **Output:**
   ```plaintext
    NAME             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
    hello-world-ds   2         2         2       2            2           <none>          12s
   ```

   ```shell
   kubectl get pods -o wide
   ```
   **Output:**
   ```plaintext
    NAME                   READY   STATUS    RESTARTS   AGE     IP                NODE    NOMINATED NODE   READINESS GATES
    hello-world-ds-cd7tw   1/1     Running   0          2m23s   192.168.166.152   node1   <none>           <none>
    hello-world-ds-tf4cv   1/1     Running   0          2m23s   192.168.104.2     node2   <none>           <none>
   ```

5. **Describe the DaemonSet to see detailed information:**
   ```shell
   kubectl describe daemonsets hello-world-ds
   ```

6. **View labels assigned to each Pod created by the DaemonSet:**
   ```shell
   kubectl get pods --show-labels
   ```

7. **Change a label on one of the Pods to see the DaemonSet's self-healing behavior:**
   ```shell
   MYPOD=$(kubectl get pods -l app=hello-world-app | grep hello-world | head -n 1 | awk '{print $1}')
   kubectl label pods $MYPOD app=not-hello-world --overwrite
   ```

8. **Observe that a new Pod is created by the DaemonSet:**
   ```shell
   kubectl get pods --show-labels
   ```

9. **Clean up by deleting the DaemonSet:**
   ```shell
   kubectl delete daemonsets hello-world-ds
   ```

---

### Creating a `DaemonSet` on a `Subset` of `Nodes`

- **Step 1**: Create a DaemonSet with a specified `nodeSelector`
    ```bash
    kubectl apply -f DaemonSetWithNodeSelector.yaml
    daemonset.apps/hello-world-ds created
    ```

- **Observation**: No pods are created because no nodes match the specified label
    ```bash
    kubectl get daemonsets
    NAME             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR         AGE
    hello-world-ds   0         0         0       0            0           node=hello-world-ns   26s
    ```

- **Step 2**: Label a Node to satisfy the `Node Selector`
    ```bash
    kubectl label node node2 node=hello-world-ns
    node/node2 labeled
    ```

- **Verification**: Check if a pod gets created
    ```bash
    kubectl get daemonsets
    NAME             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR         AGE
    hello-world-ds   1         1         1       1            1           node=hello-world-ns   91s

    kubectl get daemonsets -o wide
    NAME             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR         AGE    CONTAINERS    IMAGES                                SELECTOR
    hello-world-ds   1         1         1       1            1           node=hello-world-ns   115s   hello-world   ghcr.io/hungtran84/hello-app:1.0   app=hello-world-app

    kubectl get pods -o wide
    NAME                   READY   STATUS    RESTARTS   AGE   IP         NODE    NOMINATED NODE   READINESS GATES
    hello-world-ds-59qwm   1/1     Running   0          64s   10.5.1.4   node2   <none>           <none>
    ```

- **Step 3**: What happens if the label is removed?
    ```bash
    kubectl label node node2 node-
    node/node2 unlabeled
    ```

- **Outcome**: The pod is terminated. Check events and node scheduling status
    ```bash
    kubectl describe daemonsets hello-world-ds
    Name:           hello-world-ds
    Selector:       app=hello-world-app
    Node-Selector:  node=hello-world-ns
    Labels:         <none>
    Annotations:    deprecated.daemonset.template.generation: 1
    Desired Number of Nodes Scheduled: 0
    Current Number of Nodes Scheduled: 0
    Number of Nodes Scheduled with Up-to-date Pods: 0
    Number of Nodes Scheduled with Available Pods: 0
    Number of Nodes Misscheduled: 0
    Pods Status:  0 Running / 0 Waiting / 0 Succeeded / 0 Failed
    Pod Template:
      Labels:  app=hello-world-app
      Containers:
       hello-world:
        Image:        ghcr.io/hungtran84/hello-app:1.0
        Port:         <none>
        Host Port:    <none>
        Environment:  <none>
        Mounts:       <none>
      Volumes:        <none>
    Events:
      Type    Reason            Age    From                  Message
      ----    ------            ----   ----                  -------
      Normal  SuccessfulCreate  2m44s  daemonset-controller  Created pod: hello-world-ds-59qwm
      Normal  SuccessfulDelete  39s    daemonset-controller  Deleted pod: hello-world-ds-59qwm
    ```

- **Cleanup**: Delete the DaemonSet
    ```bash
    kubectl delete daemonsets hello-world-ds
    ```


---

### Updating a `DaemonSet`

- **Step 1**: Deploy the `v1` `DaemonSet`
    ```bash
    kubectl apply -f DaemonSet.yaml
    ```

- **Check the Image Version**: Verify that the container image version is `1.0`
    ```bash
    kubectl describe daemonsets hello-world
    ```

- **Check Update Strategy**: Note that the `updateStrategy` defaults to `rollingUpdate` with `maxUnavailable` set to 1
    ```bash
    kubectl get DaemonSet hello-world-ds -o yaml | more

    apiVersion: apps/v1
    kind: DaemonSet
    metadata:
      annotations:
        deprecated.daemonset.template.generation: "1"
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"apps/v1","kind":"DaemonSet","metadata":{"annotations":{},"name":"hello-world-ds","namespace":"default"},"spec":{"selector":{"matchLabels":{"app":"hello-world-app"}},"template":{"metadata":{"labels":{"app":"hello-world-app"}},"spec":{"containers":[{"image":"ghcr.io/hungtran84/hello-app:1.0","name":"hello-world"}]}}}}
      creationTimestamp: "2023-08-18T15:37:09Z"
      generation: 1
      name: hello-world-ds
      namespace: default
      resourceVersion: "3301"
      uid: e39ea27d-1561-4fdd-bc3b-2d21fe771376
    spec:
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app: hello-world-app
      template:
        metadata:
          creationTimestamp: null
          labels:
            app: hello-world-app
        spec:
          containers:
          - image: ghcr.io/hungtran84/hello-app:1.0
            imagePullPolicy: IfNotPresent
            name: hello-world
            resources: {}
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
      updateStrategy:
        rollingUpdate:
          maxSurge: 0
          maxUnavailable: 1
        type: RollingUpdate
    ```

- **Step 2**: Update the Container Image to `2.0` and Apply Changes
    ```bash
    diff DaemonSet.yaml DaemonSet-v2.yaml
    
    #16,17c16
    #<           image: ghcr.io/hungtran84/hello-app:1.0
    #---
    #>           image: ghcr.io/hungtran84/hello-app:2.0
    ```

    ```bash
    kubectl apply -f DaemonSet-v2.yaml
    # daemonset.apps/hello-world-ds configured
    ```

- **Check Rollout Status**: Monitor the rollout; note that the `maxUnavailable` setting affects the update speed.
    ```bash
    kubectl rollout status daemonsets hello-world-ds
    # daemon set "hello-world-ds" successfully rolled out
    ```

- **Verify the Update**: Confirm the container image is now `2.0`, and check the rollout in the `Events` section.
    ```bash
    kubectl describe daemonsets hello-world-ds
    ```

    **Output:**
   ```plaintext
    Name:           hello-world-ds
    Selector:       app=hello-world-app
    Node-Selector:  <none>
    Labels:         <none>
    Annotations:    deprecated.daemonset.template.generation: 2
    Desired Number of Nodes Scheduled: 4
    Current Number of Nodes Scheduled: 4
    Number of Nodes Scheduled with Up-to-date Pods: 4
    Number of Nodes Scheduled with Available Pods: 4
    Number of Nodes Misscheduled: 0
    Pods Status:  4 Running / 0 Waiting / 0 Succeeded / 0 Failed
    Pod Template:
      Labels:  app=hello-world-app
      Containers:
       hello-world:
        Image:        ghcr.io/hungtran84/hello-app:2.0
        Port:         <none>
        Host Port:    <none>
        Environment:  <none>
        Mounts:       <none>
      Volumes:        <none>
    Events:
      Type    Reason            Age    From                  Message
      ----    ------            ----   ----                  -------
      Normal  SuccessfulCreate  3m54s  daemonset-controller  Created pod: hello-world-ds-nksld
      Normal  SuccessfulCreate  3m54s  daemonset-controller  Created pod: hello-world-ds-cdtdw
      Normal  SuccessfulCreate  3m54s  daemonset-controller  Created pod: hello-world-ds-vv4lp
      Normal  SuccessfulCreate  3m54s  daemonset-controller  Created pod: hello-world-ds-9g5v5
      Normal  SuccessfulDelete  69s    daemonset-controller  Deleted pod: hello-world-ds-nksld
      Normal  SuccessfulCreate  69s    daemonset-controller  Created pod: hello-world-ds-hz4bx
      Normal  SuccessfulDelete  65s    daemonset-controller  Deleted pod: hello-world-ds-cdtdw
      Normal  SuccessfulCreate  64s    daemonset-controller  Created pod: hello-world-ds-7j5jg
      Normal  SuccessfulDelete  62s    daemonset-controller  Deleted pod: hello-world-ds-9g5v5
      Normal  SuccessfulCreate  61s    daemonset-controller  Created pod: hello-world-ds-tdprd
      Normal  SuccessfulDelete  59s    daemonset-controller  Deleted pod: hello-world-ds-vv4lp
      Normal  SuccessfulCreate  58s    daemonset-controller  Created pod: hello-world-ds-6lp76
    ```

- **Check Labels**: Observe the new `controller-revision-hash` and updated `pod-template-generation`.
    ```bash
    kubectl get pods --show-labels
    ```

    **Output:**
   ```plaintext
    NAME                   READY   STATUS    RESTARTS   AGE     LABELS
    hello-world-ds-jv4qj   1/1     Running   0          2m18s   app=hello-world-app,controller-revision-hash=54d6ff5949,pod-template-generation=2
    hello-world-ds-z8nfr   1/1     Running   0          2m19s   app=hello-world-app,controller-revision-hash=54d6ff5949,pod-template-generation=2
    ```

- **Cleanup**: Delete the `DaemonSet`
    ```bash
    kubectl delete daemonsets hello-world-ds
    ```

## Summary

In this lab, we've explored essential operations for managing DaemonSets in Kubernetes:

1. **Creating a DaemonSet**:
   - We deployed a basic DaemonSet, ensuring that each node in the cluster runs a single instance of our containerized application.

2. **Updating a DaemonSet**:
   - We modified the DaemonSet to use an updated container image, leveraging the default `RollingUpdate` strategy to perform a gradual rollout with minimal downtime. This included adjusting the `maxUnavailable` setting for more controlled rollout behavior and verifying the updated image version.

3. **Using Node Selectors**:
   - We applied `nodeSelector` constraints to our DaemonSet, targeting specific nodes for scheduling based on node labels. This allowed us to deploy DaemonSet pods only to nodes that met certain criteria.

Through these exercises, we gained a practical understanding of how DaemonSets work, including their lifecycle, update mechanisms, and node-specific targeting capabilities. This knowledge is crucial for deploying cluster-wide services or monitoring agents that need to run consistently across all (or specific) nodes in a Kubernetes cluster.