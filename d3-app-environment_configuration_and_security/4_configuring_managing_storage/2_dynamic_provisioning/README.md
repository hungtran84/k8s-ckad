# Lab: Storage Dynamic Provisioning

## Prerequisites
- A GKE cluster must be set up and available.

## Objectives
In this lab, you will:
1. Explore the available `StorageClasses` in the cluster.
2. Understand the `VolumeBindingMode` and other properties of `StorageClasses`.
3. Create a Deployment with a PersistentVolumeClaim (PVC) to dynamically provision storage.
4. Observe the behavior of dynamically provisioned `PersistentVolumes`.
5. Clean up resources after the lab.

## Steps

### 1. Check Available StorageClasses
Run the following command to view the list of available `StorageClasses` and their details:
```bash
kubectl get StorageClass
```
Sample output:
```
NAME                     PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
premium-rwo              pd.csi.storage.gke.io   Delete          WaitForFirstConsumer   true                   6d15h
standard                 kubernetes.io/gce-pd    Delete          Immediate              true                   6d15h
standard-rwo (default)   pd.csi.storage.gke.io   Delete          WaitForFirstConsumer   true                   6d15h
```

### 2. Describe a StorageClass
Examine details of a `StorageClass` to understand its properties:
```bash
kubectl describe StorageClass premium-rwo
```
Key details include:
- **Provisioner**: Storage provider.
- **ReclaimPolicy**: Action taken when the `PersistentVolumeClaim` (PVC) is deleted.
- **VolumeBindingMode**: Determines when a volume is provisioned.
  - `WaitForFirstConsumer`: The volume is created when a Pod is scheduled.
  - `Immediate`: The volume is created as soon as the PVC is created.

### 3. Verify PersistentVolumes (PV)
Check if there are any existing `PersistentVolumes`:
```bash
kubectl get pv
```
Expected output (if none exist):
```
No resources found
```

### 4. Deploy an Nginx Pod with a PVC
Apply a YAML manifest to create a PVC and a Deployment that uses the PVC:
```bash
kubectl apply -f GCP-DeploymentDisk.yaml
```
Sample output:
```
persistentvolumeclaim/pvc-managed created
deployment.apps/nginx-gcp-deployment created
```

### 5. Inspect the PersistentVolume
List the `PersistentVolumes` and review key details:
```bash
kubectl get PersistentVolume
```
Sample output:
```
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                 STORAGECLASS   REASON   AGE
pvc-f44711a2-d595-406e-bfef-202a11a55deb   10Gi       RWO            Delete           Bound    default/pvc-managed   premium-rwo             18s
```

### 6. Inspect the PersistentVolumeClaim
Check the status of the PVC to confirm it is `Bound`:
```bash
kubectl get PersistentVolumeClaim
```
Sample output:
```
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-managed   Bound    pvc-f44711a2-d595-406e-bfef-202a11a55deb   10Gi       RWO            premium-rwo    2m4s
```

### 7. Verify the Pod Deployment
Check if the Nginx pod has been created and is running:
```bash
kubectl get pods
```
Sample output:
```
NAME                                    READY   STATUS    RESTARTS   AGE
nginx-gcp-deployment-6f89654cdc-rvhxw   1/1     Running   0          2m20s
```

### 8. Clean Up Resources
Delete the Deployment and PVC to clean up:
```bash
kubectl delete deployment nginx-gcp-deployment
kubectl delete PersistentVolumeClaim pvc-managed
```

## Summary
In this lab, you:
- Explored `StorageClasses` and their properties.
- Used a `StorageClass` to dynamically provision a `PersistentVolume`.
- Deployed an Nginx pod with persistent storage.
- Cleaned up resources to maintain a tidy cluster.
