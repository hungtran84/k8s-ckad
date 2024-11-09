# Examining System Pods and Their Controllers

## Objectives
- Understand the purpose of system pods within the `kube-system` namespace.
- Learn how static pod manifests facilitate the initial deployment of essential Kubernetes components.
- Explore the roles of different controllers and their scalability as new nodes are added.

## Prerequisite

For the sake of simplicity, we're going to use [PlayWithKuberênts](https://labs.play-with-k8s.com/) to create a 3-node cluster.

## Steps

1. **Check System Pods:**
   To begin, we will retrieve all resources running in the `kube-system` namespace, which includes the core components of the Kubernetes control plane.
   ```bash
   kubectl get --namespace kube-system all
   ```

   Example output:
   ```
   NAME                                READY   STATUS    RESTARTS   AGE
   pod/coredns-5d78c9869d-6626t        1/1     Running   0          13m
   pod/coredns-5d78c9869d-pnhkq        1/1     Running   0          13m
   pod/etcd-node1                      1/1     Running   0          13m
   pod/kube-apiserver-node1            1/1     Running   0          13m
   pod/kube-controller-manager-node1   1/1     Running   0          13m
   pod/kube-proxy-xflzb                1/1     Running   0          13m
   pod/kube-router-ndmt8               1/1     Running   0          13m
   pod/kube-scheduler-node1            1/1     Running   0          14m

   NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
   service/kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   14m

   NAME                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
   daemonset.apps/kube-proxy    1         1         1       1            1           kubernetes.io/os=linux   14m
   daemonset.apps/kube-router   1         1         1       1            1           <none>                   13m

   NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/coredns   2/2     2            2           14m

   NAME                                 DESIRED   CURRENT   READY   AGE
   replicaset.apps/coredns-5d78c9869d   2         2         2       13m
   ```

2. **Examine the CoreDNS Deployment:**
   Next, we will focus on the `coredns` deployment to verify its configuration, which maintains two pods at all times:
   ```bash
   kubectl get --namespace kube-system deployments coredns
   ```

   Example output:
   ```
   NAME      READY   UP-TO-DATE   AVAILABLE   AGE
   coredns   2/2     2            2           14m
   ```

3. **Understand DaemonSet Functionality:**
   `DaemonSets` ensure that pods run on every node within the cluster by default. As new nodes are added, the pods are automatically deployed to these nodes. We can check the `DaemonSets` currently running in the `kube-system` namespace:
   ```bash
   kubectl get --namespace kube-system daemonset
   ```

   Example output:
   ```
   NAME          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
   kube-proxy    1         1         1       1            1           kubernetes.io/os=linux   15m
   kube-router   1         1         1       1            1           <none>                   15m
   ```

4. **Scale the Cluster:**
   To observe how `DaemonSet` pods scale with the addition of nodes, let’s increase the cluster size to 5 nodes and verify the changes in the `DaemonSet`:
   ```bash
   kubectl get nodes
   ```

   Example output:
   ```
   NAME    STATUS   ROLES           AGE    VERSION
   node1   Ready    control-plane   2m6s   v1.27.2
   node2   Ready    <none>          56s    v1.27.2
   node3   Ready    <none>          52s    v1.27.2
   node4   Ready    <none>          49s    v1.27.2
   node5   Ready    <none>          45s    v1.27.2

   kubectl get --namespace kube-system daemonset
   ```

   Example output after scaling:
   ```
   NAME          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
   kube-proxy    5         5         5       5            5           kubernetes.io/os=linux   104s
   kube-router   5         5         5       5            5           <none>                   49s
   ```

## Summary
In this lab, we explored the system pods within the `kube-system` namespace and learned about their roles in managing the Kubernetes control plane. We examined how Static Pod Manifests enable these pods to come online even before the cluster is fully operational. Additionally, we observed how `DaemonSets` deploy their pods across nodes and how these deployments scale with the addition of new nodes.
