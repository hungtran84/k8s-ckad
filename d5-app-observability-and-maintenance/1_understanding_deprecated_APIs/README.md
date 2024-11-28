Here is the updated lab without Step 6 and the Key Updates part:

# Lab: Detecting and Fixing Deprecated Kubernetes APIs

## Objectives
In this lab, you will:
- Learn about deprecated Kubernetes APIs and their impact on cluster operations.
- Detect deprecated APIs in resource manifests using `kubectl`.
- Use `kubent` to scan the cluster for deprecated APIs and check for compatibility with future Kubernetes versions (e.g., `1.31`).
- Update resource manifests to use supported API versions.

---

## Steps

### 1. Prerequisites
- A running Kubernetes cluster.
- `kubectl` installed and configured.
- `kubent` installed (instructions provided for macOS and Linux).

---

### 2. Deploy a Resource Using a Deprecated API

#### 2.1 Apply a Manifest with Deprecated API
1. Create a manifest using a deprecated API version. For this example, we'll use `apps/v1beta1`, which is deprecated in favor of `apps/v1`.

   <details>
   <summary>Reveal Manifest</summary>

   ```yaml
   apiVersion: apps/v1beta1
   kind: Deployment
   metadata:
     name: deprecated-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: deprecated-app
     template:
       metadata:
         labels:
           app: deprecated-app
       spec:
         containers:
         - name: nginx
           image: nginx:1.21
           ports:
           - containerPort: 80
   ```
   </details>

2. Save the manifest as `deprecated-deployment.yaml`.

3. Apply the manifest:
   ```bash
   kubectl apply -f deprecated-deployment.yaml
   ```

4. Check the resource:
   ```bash
   kubectl get deployment deprecated-deployment
   ```

#### 2.2 Observe Deprecated API Warning
When applying the resource, you will see a warning such as:
```
Warning: apps/v1beta1 is deprecated in v1.16+, unavailable in v1.31+; use apps/v1 instead
```

Verify the API version used:
```bash
kubectl get deployment deprecated-deployment -o yaml | grep apiVersion
```

---

### 3. Detect Deprecated APIs with `kubectl`

#### 3.1 Dry-Run to Detect Deprecated APIs
1. Use `kubectl apply` with `--dry-run` to simulate resource creation:
   ```bash
   kubectl apply -f deprecated-deployment.yaml --dry-run=server
   ```

2. Review the output for any deprecation warnings related to your resources.

---

### 4. Use `kubent` to Detect Deprecated APIs

#### 4.1 Install `kubent` (If Not Installed)

**For macOS:**
1. Install `kubent` using Homebrew:
   ```bash
   brew install kubent
   ```

2. Verify installation:
   ```bash
   kubent --version
   ```

**For Linux:**
1. Install `kubent` using the following commands:

   ```bash
   curl -LO https://github.com/doitintl/kube-no-trouble/releases/download/v0.7.3/kubent-linux-amd64.tar.gz
   tar -xvzf kubent-linux-amd64.tar.gz
   sudo mv kubent /usr/local/bin/
   ```

2. Verify installation:
   ```bash
   kubent --version
   ```

#### 4.2 Run `kubent` to Detect Deprecated APIs
1. Scan the cluster for deprecated APIs, specifically checking for compatibility with Kubernetes **1.31**:
   ```bash
   kubent --target-version v1.31
   ```

2. Review the report, which identifies resources using deprecated APIs that will be removed or altered in version `1.31`.

---

### 5. Fix Deprecated APIs in Manifests

#### 5.1 Update the Manifest to Use Supported API Versions
1. Modify `deprecated-deployment.yaml` to use `apps/v1`, which is the supported API version starting from Kubernetes 1.16:
   
   <details>
   <summary>Reveal Updated Manifest</summary>

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: deprecated-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: deprecated-app
     template:
       metadata:
         labels:
           app: deprecated-app
       spec:
         containers:
         - name: nginx
           image: nginx:1.21
           ports:
           - containerPort: 80
   ```
   </details>

2. Save the updated manifest.

#### 5.2 Apply the Updated Manifest
1. Apply the corrected manifest:
   ```bash
   kubectl apply -f deprecated-deployment.yaml
   ```

2. Confirm the deployment uses the correct API version:
   ```bash
   kubectl get deployment deprecated-deployment -o yaml | grep apiVersion
   ```

#### 5.3 Delete the Old Deployment
1. Remove the deployment that used the deprecated API:
   ```bash
   kubectl delete -f deprecated-deployment.yaml
   ```

---

### 7. Clean Up
1. Delete all resources created during the lab:
   ```bash
   kubectl delete deployment deprecated-deployment
   ```

---

## Summary
In this lab, you:
- Deployed a resource using a deprecated Kubernetes API (`apps/v1beta1`).
- Detected deprecated APIs using `kubectl` and dry-run mode.
- Used `kubent` to identify deprecated APIs across the cluster and checked for compatibility with the target Kubernetes version `1.31`.
- Updated resource manifests to use supported API versions (`apps/v1`).
