# Lab: Creating and Accessing Secrets in Kubernetes

## Objectives
- Understand how to create and manage Kubernetes secrets.
- Learn different methods to access secrets in Pods.
- Explore the use of secrets as environment variables and mounted volumes.

## Steps

### 1. Creating a Generic Secret
- Create a secret using literal values:
  ```bash
  kubectl create secret generic app1 --from-literal=USERNAME=app1login --from-literal=PASSWORD='S0methingS@Str0ng!'
  # Output: secret/app1 created
  ```

- Verify the secret:
  ```bash
  kubectl get secrets
  # Output:
  # NAME   TYPE     DATA   AGE
  # app1   Opaque   2      20s
  ```

- Describe the secret to view details:
  ```bash
  kubectl describe secret app1
  ```

- Access the secret values at the command line:
  ```bash
  echo $(kubectl get secret app1 --template={{.data.USERNAME}})
  echo $(kubectl get secret app1 --template={{.data.USERNAME}} | base64 --decode)

  echo $(kubectl get secret app1 --template={{.data.PASSWORD}})
  echo $(kubectl get secret app1 --template={{.data.PASSWORD}} | base64 --decode)
  ```

### 2. Accessing Secrets in Pods

#### As Environment Variables
1. Apply a deployment manifest:
   ```bash
   kubectl apply -f deployment-secrets-env.yaml
   ```

2. Get the pod name:
   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-secrets-env | awk '{print $1}' | head -n 1)
   echo $PODNAME
   ```

3. Retrieve the environment variables from the pod:
   ```bash
   kubectl exec -it $PODNAME -- env | grep ^app1
   # Output:
   # app1username=app1login
   # app1password=S0methingS@Str0ng!
   ```

#### As Mounted Files
1. Apply a deployment manifest:
   ```bash
   kubectl apply -f deployment-secrets-files.yaml
   ```

2. Get the pod name:
   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-secrets-files | awk '{print $1}' | head -n 1)
   echo $PODNAME
   ```

3. Inspect the pod for volume details:
   ```bash
   kubectl describe pod $PODNAME
   ```

4. Access the secret files inside the pod:
   ```bash
   kubectl exec -it $PODNAME -- /bin/sh
   ls /etc/appconfig
   cat /etc/appconfig/USERNAME
   cat /etc/appconfig/PASSWORD
   exit
   ```

### 3. Additional Examples

#### Using `stringData` for Clear Text Secrets
1. Apply a manifest:
   ```bash
   kubectl apply -f secret.string.yaml
   ```

#### Using Encoded Values for Secrets
1. Encode values:
   ```bash
   echo -n 'app2login' | base64
   echo -n 'S0methingS@Str0ng!' | base64
   ```

2. Apply the encoded secret manifest:
   ```bash
   kubectl apply -f secret.encoded.yaml
   ```

3. Verify secrets:
   ```bash
   kubectl get secrets
   ```

#### Using `envFrom` to Create Environment Variables
1. Create a secret:
   ```bash
   kubectl create secret generic app1 --from-literal=USERNAME=app1login --from-literal=PASSWORD='S0methingS@Str0ng!'
   ```

2. Apply the deployment manifest:
   ```bash
   kubectl apply -f deployment-secrets-env-from.yaml
   ```

3. Verify environment variables in the pod:
   ```bash
   PODNAME=$(kubectl get pods | grep hello-world-secrets-env-from | awk '{print $1}' | head -n 1)
   kubectl exec -it $PODNAME -- printenv | sort
   ```

### 4. Cleanup
Remove resources created during the lab:
```bash
kubectl delete secret app1
kubectl delete secret app2
kubectl delete secret app3
kubectl delete deployment hello-world-secrets-env
kubectl delete deployment hello-world-secrets-files
kubectl delete deployment hello-world-secrets-env-from
```

## Summary
- Kubernetes secrets can securely store sensitive data.
- Secrets can be accessed in pods as environment variables or mounted files.
- `envFrom` allows creating environment variables from all keys in a secret.
- Clear text secrets should be avoided in favor of encoded values.
