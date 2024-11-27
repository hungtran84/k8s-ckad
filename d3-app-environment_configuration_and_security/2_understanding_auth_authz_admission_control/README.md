# Lab: Investigating Certificate-Based Authentication and Service Accounts

## Objectives
1. Understand and investigate certificate-based authentication in Kubernetes.
2. Work with Service Accounts to explore their roles and permissions.
3. Modify Service Account permissions using RBAC.

---

## Steps

### **1. Investigating Certificate-Based Authentication**

#### **View Kubernetes Configuration**
```bash
kubectl config view
kubectl config view --raw
```

#### **Read Certificate Information**
- Extract and decode the certificate:
  ```bash
  kubectl config view --raw -o jsonpath='{ .users[*].user.client-certificate-data }' | base64 --decode > admin.crt
  openssl x509 -in admin.crt -text -noout | head
  ```

- Verify API server communication:
  ```bash
  kubectl get pods -v 6
  ```

- Clean up:
  ```bash
  rm admin.crt
  ```

---

### **2. Working with Service Accounts**

#### **Inspect Service Accounts**
- Get all Service Accounts:
  ```bash
  kubectl get serviceaccounts
  ```

- Inspect the default Service Account:
  ```bash
  kubectl describe serviceaccounts default
  ```

#### **Create a Service Account**
- Create and inspect a new Service Account:
  ```bash
  kubectl create serviceaccount mysvcaccount1
  kubectl describe serviceaccounts mysvcaccount1
  ```

#### **Deploy a Workload with a Service Account**
- Deploy an application:
  ```bash
  kubectl apply -f nginx-deployment.yaml
  kubectl get pods
  ```

- Store pod name in a variable:
  ```bash
  PODNAME=$(kubectl get pods -l app=nginx -o jsonpath='{ .items[*].metadata.name }')
  kubectl get pod $PODNAME -o yaml
  ```

#### **Access the API Server Inside a Pod**
- Access and explore:
  ```bash
  kubectl exec $PODNAME -it -- /bin/bash
  ls /var/run/secrets/kubernetes.io/serviceaccount/
  cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  cat /var/run/secrets/kubernetes.io/serviceaccount/namespace
  cat /var/run/secrets/kubernetes.io/serviceaccount/token
  ```

- Test API access:
  ```bash
  TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  curl --cacert $CACERT -X GET https://kubernetes.default.svc/api/
  curl --cacert $CACERT --header "Authorization: Bearer $TOKEN" -X GET https://kubernetes.default.svc/api/
  ```

- Attempt to list pods:
  ```bash
  curl --cacert $CACERT --header "Authorization: Bearer $TOKEN" -X GET https://kubernetes.default.svc/api/v1/namespaces/default/pods
  exit
  ```

---

### **3. Modifying Service Account Permissions**

#### **Impersonation and Testing Authorization**
- Test permissions:
  ```bash
  kubectl auth can-i list pods --as=system:serviceaccount:default:mysvcaccount1
  kubectl get pods -v 6 --as=system:serviceaccount:default:mysvcaccount1
  ```

#### **Grant Permissions Using RBAC**
- Create a role and bind it to the Service Account:
  ```bash
  kubectl create role demorole --verb=get,list --resource=pods
  kubectl create rolebinding demorolebinding \
      --role=demorole \
      --serviceaccount=default:mysvcaccount1
  ```

- Test updated permissions:
  ```bash
  kubectl auth can-i list pods --as=system:serviceaccount:default:mysvcaccount1
  kubectl get pods -v 6 --as=system:serviceaccount:default:mysvcaccount1
  ```

- Validate inside the pod:
  ```bash
  PODNAME=$(kubectl get pods -l app=nginx -o jsonpath='{ .items[*].metadata.name }')
  kubectl exec $PODNAME -it -- /bin/bash

  TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
  CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

  curl --cacert $CACERT --header "Authorization: Bearer $TOKEN" -X GET https://kubernetes.default.svc/api/v1/namespaces/default/pods
  exit
  ```

---

### **4. Exploring Default Service Accounts**

#### **Inspect Default Service Account**
- List all default Service Accounts:
  ```bash
  kubectl get sa --all-namespaces | grep default
  ```

- Check details of the default Service Account:
  ```bash
  kubectl get sa default -o yaml
  ```

#### **Anonymous API Access**
- Try accessing the API server:
  ```bash
  kubectl exec -ti pod-default -- sh
  apk add --update curl
  curl https://kubernetes/api --insecure
  ```

#### **Call Using a ServiceAccount Token**
- Use the default Service Account's token:
  ```bash
  TOKEN=$(cat /run/secrets/kubernetes.io/serviceaccount/token)
  curl -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/ --insecure
  ```

- Attempt to list pods (insufficient permissions):
  ```bash
  curl -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/namespaces/default/pods/ --insecure
  ```

#### **Using a Custom Service Account**
- Create and assign a custom Service Account:
  ```bash
  kubectl apply -f custom_serviceaccount.yaml
  kubectl apply -f pod-with-sa.yaml
  ```

- Test API access with the custom Service Account:
  ```bash
  kubectl exec -ti pod-demo-sa -- sh
  apk add --update curl
  TOKEN=$(cat /run/secrets/kubernetes.io/serviceaccount/token)
  curl -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/namespaces/default/pods/ --insecure
  ```

---

## Summary
This lab demonstrated how to investigate certificate-based authentication, work with Service Accounts, modify permissions using RBAC, and test API access in Kubernetes. It highlighted the importance of Service Accounts in managing access to Kubernetes resources.

---

## Cleanup
```bash
kubectl delete deployment nginx
kubectl delete serviceaccount mysvcaccount1
kubectl delete role demorole
kubectl delete rolebinding demorolebinding
kubectl delete -f pod-noserviceaccount.yaml
kubectl delete -f pod-with-sa.yaml
```
