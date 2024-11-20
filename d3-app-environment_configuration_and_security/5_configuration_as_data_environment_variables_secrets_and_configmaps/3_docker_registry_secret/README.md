# Lab: Pulling a Container from a Private Container Registry

## Objectives
- Understand how to pull and publish an image to your GitHub Container Registry (GHCR).
- Learn to create a Kubernetes secret for private registry authentication.
- Deploy a pod using an image from a private registry.

## Steps

### Step 1: Generate Your GHCR Token
Before pushing an image to your GHCR, you need a personal access token:
1. Log in to your GitHub account.
2. Navigate to **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
3. Click **Generate new token**:
   - Set an appropriate **Expiration**.
   - Grant the **read:packages** and **write:packages** scopes.
4. Save the token securely (e.g., in a password manager).

### Step 2: Pull and Publish the Image to Your GHCR

#### Step 2.1: Pull the Public Image
Run the following command to pull the public image to your local Docker environment:
```bash
docker pull ghcr.io/hungtran84/hello-app:1.0
```

#### Step 2.2: Tag the Image for Your GHCR
Replace `<Your_GitHub_User>` with your GitHub username (e.g., `hungtran84`):
```bash
docker tag ghcr.io/hungtran84/hello-app:1.0 ghcr.io/<Your_GitHub_User>/hello-app:1.0
```

#### Step 2.3: Log in to Your GHCR
Authenticate with your GitHub username and the personal access token generated in Step 1:
```bash
echo "<GHCR_TOKEN>" | docker login ghcr.io -u <Your_GitHub_User> --password-stdin
```

#### Step 2.4: Push the Image to Your GHCR
Publish the tagged image to your personal GHCR:
```bash
docker push ghcr.io/<Your_GitHub_User>/hello-app:1.0
```

### Step 3: Create the Docker Registry Secret
Replace the placeholders with your details:
- `GHCR_USERNAME` = Your GitHub username.
- `GHCR_TOKEN` = The token generated in Step 1.
- `GHCR_EMAIL` = Your GitHub registered email.

```bash
kubectl create secret docker-registry private-reg-cred \
    --docker-server=https://ghcr.io \
    --docker-username=$GHCR_USERNAME \
    --docker-password=$GHCR_TOKEN \
    --docker-email=$GHCR_EMAIL
```

### Step 4: Deploy Using the ImagePullSecret
1. Update the `deployment-private-registry.yaml` file:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: hello-world-private-registry
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: hello-world-private
     template:
       metadata:
         labels:
           app: hello-world-private
       spec:
         containers:
         - name: hello-world
           image: ghcr.io/<Your_GitHub_User>/hello-app:1.0
           ports:
           - containerPort: 8080
         imagePullSecrets:
         - name: private-reg-cred
   ```
2. Apply the deployment:
   ```bash
   kubectl apply -f deployment-private-registry.yaml
   ```
3. Verify that the pod is running:
   ```bash
   kubectl get pods
   ```

### Step 5: Inspect the Pod
Check if the container was pulled successfully:
```bash
kubectl describe pods hello-world-private-registry
```

### Step 6: Cleanup
Remove the deployment and secret:
```bash
kubectl delete -f deployment-private-registry.yaml
kubectl delete secret private-reg-cred
```

## Summary
In this lab, you:
- Generated a GHCR token for authentication.
- Pulled a public image and published it to your own GHCR.
- Created a Kubernetes secret for private registry credentials.
- Deployed a pod using an image from a private GHCR registry.
- Verified the successful pull and cleaned up the resources.
