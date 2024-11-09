# MySQL `StatefulSet` with `Headless` Service in Kubernetes

## Objectives

- Deploy a MySQL database cluster using `StatefulSet` in Kubernetes.
- Configure a headless service for `StatefulSet` pods.
- Use persistent storage for MySQL data with PersistentVolumeClaims (PVCs).
- Connect to the MySQL cluster from other pods in the same Kubernetes cluster.

## Prerequisites

- A **GKE (Google Kubernetes Engine)** cluster running and accessible.
- `kubectl` configured to communicate with the GKE cluster.
- A basic understanding of Kubernetes resources like `StatefulSet`, `Headless Service`, and Persistent Volumes.

## Step 1: Create a Headless Service

A **headless service** is used to allow direct access to the pods in the `StatefulSet`. This enables DNS resolution for each pod using their respective names.

### Create the Headless Service YAML

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-db
  labels:
    app: mysql-db
spec:
  clusterIP: None  # This makes it a headless service
  selector:
    app: mysql-db
  ports:
    - port: 3306
      targetPort: 3306
      name: mysql
```

### Apply the Service

```bash
kubectl apply -f mysql-db-service.yaml
```

## Step 2: Create a StatefulSet for MySQL

Now, we'll create a StatefulSet for MySQL. The StatefulSet will ensure each pod gets a unique persistent volume, and it will be able to scale with replica pods while maintaining the same storage across restarts.

### Create the StatefulSet YAML

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-db
  labels:
    app: mysql-db
spec:
  serviceName: mysql-db  # Points to the headless service
  replicas: 3  # Set the number of replicas (pods)
  selector:
    matchLabels:
      app: mysql-db
  template:
    metadata:
      labels:
        app: mysql-db
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        envFrom:
          - secretRef:
              name: mysql-db-password  # The secret containing MySQL password
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 50Gi  # Size of the persistent volume
      storageClassName: standard-pd  # Optional: Define the storage class for GCP Persistent Disks
```

### Apply the StatefulSet

```bash
kubectl apply -f mysql-db-statefulset.yaml
```

### Explanation:

- **Service**: The headless service `mysql-db` will expose each of the StatefulSet pods via DNS. The `clusterIP: None` ensures no load balancing occurs, and instead, each pod gets a unique DNS entry.
  
- **StatefulSet**: 
  - The StatefulSet ensures each pod has its own unique persistent volume.
  - `replicas: 3` specifies the number of MySQL replicas in the cluster.
  - `volumeClaimTemplates`: This will create PersistentVolumeClaims (PVCs) for each pod to ensure that the data is persistent across pod restarts.
  - The `storageClassName` is set to `standard-pd`, which is used for provisioning Google Cloud Persistent Disks.

## Step 3: Create a Secret for MySQL Password

We will create a Kubernetes Secret to securely store the MySQL root password.

### Create the Secret YAML

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-db-password
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: <base64-encoded-password>  # Replace with base64 encoded password
```

### Apply the Secret

```bash
kubectl apply -f mysql-db-secret.yaml
```

To encode your password in base64:

```bash
echo -n "yourpassword" | base64
```

Replace `<base64-encoded-password>` with the output of this command.

## Step 4: Verify the StatefulSet and Pods

Once you’ve applied the StatefulSet and the Secret, you can check the status of your StatefulSet and ensure that the pods are running and connected to their persistent volumes.

### Check Pods

```bash
kubectl get pods
```

You should see three pods created for the StatefulSet:

```
mysql-db-0    1/1     Running   0          30s
mysql-db-1    1/1     Running   0          30s
mysql-db-2    1/1     Running   0          30s
```

### Check Persistent Volumes

```bash
kubectl get pvc
```

You should see that the PVCs for each pod are bound to a PersistentVolume:

```
NAME            STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-mysql-db-0 Bound     pvc-xxxxx-xxxx-xxxx-xxxx-xxxxxx           50Gi       RWO            standard-pd    10m
data-mysql-db-1 Bound     pvc-xxxxx-xxxx-xxxx-xxxx-xxxxxx           50Gi       RWO            standard-pd    10m
data-mysql-db-2 Bound     pvc-xxxxx-xxxx-xxxx-xxxx-xxxxxx           50Gi       RWO            standard-pd    10m
```

## Step 5: Access MySQL Pods

To connect to one of the MySQL pods, you can use the following `kubectl` command to exec into the pod:

```bash
kubectl exec -it mysql-db-0 -- bash
```

Inside the pod, you can access MySQL by using the MySQL client:

```bash
mysql -u root -p
```

Enter the password that you specified in the secret.

## Step 6: Connecting to MySQL from Other Pods

Other pods can connect to the MySQL cluster using the service DNS, which will resolve to the appropriate pod.

Example connection string for MySQL:

```bash
mysql -h mysql-db-0.mysql-db.default.svc.cluster.local -u root -p
```

Where:
- `mysql-db-0.mysql-db.default.svc.cluster.local` is the DNS name of the first MySQL pod.
- Replace `default` with the appropriate namespace if your MySQL cluster is not in the `default` namespace.

## Step 7: Clean Up

After the lab, you can delete the resources you created:

```bash
kubectl delete -f mysql-db-statefulset.yaml
kubectl delete -f mysql-db-service.yaml
kubectl delete -f mysql-db-secret.yaml
```

---

## Summary

In this guide, you have successfully:
- Deployed a MySQL cluster in Kubernetes using a StatefulSet and a headless service.
- Configured persistent storage using StatefulSet's volumeClaimTemplates.
- Accessed MySQL via DNS and connected to the database.

