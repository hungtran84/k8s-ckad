# Lab: Creating, managing and consuming ConfigMaps

## Objectives
- Learn how to create and manage ConfigMaps in Kubernetes.
- Use ConfigMaps as environment variables and files in Pods.
- Update ConfigMaps dynamically and observe changes in Pods.
- Explore additional examples of ConfigMap usage for application configurations.

---

## Steps

### Step 1: Creating ConfigMaps

#### Create a PROD ConfigMap
Use literals to create a ConfigMap for the PROD environment:
```bash
kubectl create configmap appconfigprod \
  --from-literal=DATABASE_SERVERNAME=sql.example.local \
  --from-literal=BACKEND_SERVERNAME=be.example.local
```

#### Create a QA ConfigMap
Create a ConfigMap from a file for the QA environment:
1. Save the configuration into a file:
   ```bash
   echo -e 'DATABASE_SERVERNAME="sqlqa.example.local"\nBACKEND_SERVERNAME="beqa.example.local"' > appconfigqa
   ```
2. Create the ConfigMap:
   ```bash
   kubectl create configmap appconfigqa --from-file=appconfigqa
   ```

#### Verify ConfigMap Structures
Inspect the created ConfigMaps:
```bash
kubectl get configmap appconfigprod -o yaml
kubectl get configmap appconfigqa -o yaml
```

---

### Step 2: Using ConfigMaps in Pod Configurations

#### Use ConfigMaps as Environment Variables
1. Apply the deployment configuration:
   ```bash
   kubectl apply -f deployment-configmaps-env-prod.yaml
   ```
2. Verify the environment variables in the running Pod:
   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-configmaps-env-prod | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- env | sort
   ```

#### Use ConfigMaps as Files
1. Apply the deployment configuration:
   ```bash
   kubectl apply -f deployment-configmaps-files-qa.yaml
   ```
2. Verify the ConfigMap data exposed as a file:
   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-configmaps-files-qa | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- cat /etc/appconfig/appconfigqa
   ```

---

### Step 3: Updating a ConfigMap Dynamically
1. Edit the `appconfigqa` ConfigMap to change `BACKEND_SERVERNAME`:
   ```bash
   kubectl edit configmap appconfigqa
   ```
2. Observe the changes reflected in the Pod:
   ```bash
   kubectl exec -it $PODNAME -- watch cat /etc/appconfig/appconfigqa
   ```

---

### Step 4: Additional ConfigMap Examples

#### Read Configurations from a Directory
1. Create a ConfigMap from a directory:
   ```bash
   kubectl create configmap httpdconfigprod1 --from-file=./configs/
   ```
2. Apply the deployment and inspect the mounted files:
   ```bash
   kubectl apply -f deployment-configmaps-directory-qa.yaml
   PODNAME=$(kubectl get pods | grep hello-world-configmaps-directory-qa | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- /bin/sh
   ls /etc/httpd
   cat /etc/httpd/httpd.conf
   cat /etc/httpd/ssl.conf
   ```

#### Use a Custom Key for a File
1. Create a ConfigMap with a custom key:
   ```bash
   kubectl create configmap appconfigprod1 --from-file=app1=appconfigprod
   ```
2. Inspect the ConfigMap and its usage in a Pod:
   ```bash
   kubectl describe configmap appconfigprod1
   kubectl apply -f deployment-configmaps-files-key-qa.yaml
   PODNAME=$(kubectl get pods | grep hello-world-configmaps-files-key-qa | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- /bin/sh
   ls /etc/appconfig
   cat /etc/appconfig/app1
   ```

---

### Step 5: Cleanup
Clean up all resources created in the lab:
```bash
kubectl delete deployment hello-world-configmaps-env-prod
kubectl delete deployment hello-world-configmaps-files-qa
kubectl delete deployment hello-world-configmaps-directory-qa
kubectl delete deployment hello-world-configmaps-files-key-qa
kubectl delete configmap appconfigprod
kubectl delete configmap appconfigqa
kubectl delete configmap httpdconfigprod1
```

---

## Summary
- Created ConfigMaps using literals, files, and directories.
- Used ConfigMaps in Pods as environment variables and mounted files.
- Updated a ConfigMap dynamically and observed the changes in the associated Pods.
- Explored advanced ConfigMap examples for application configurations.
