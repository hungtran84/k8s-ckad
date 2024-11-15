# Lab: Creating a Variant of Kubernetes Configuration with Kustomize

## Objectives

- Learn to use **Kustomize** to create variants of Kubernetes configurations.
- Use a base configuration and define a variant through an overlay.
- Understand how Kustomize overlays work to extend and modify base configurations.

## Requirements

- Install the **Kustomize standalone binary** from [Kustomize releases](https://github.com/kubernetes-sigs/kustomize/releases).
- Install the `tree` command for better visibility of the folder structure:
  ```bash
  # CloudShell
  sudo apt-get install tree
  ```

  ```bash
  # MacOS
  brew install tree
  ```

## Steps

1. **Review the Initial Directory Structure**  
   Familiarize yourself with the directory structure and its initial content:
   ```bash
   cd config
   ls -lR
   tree .
   ```

2. **Create a Kustomization in the Base Directory**  
   Move to the base directory and create a Kustomization file:
   ```bash
   cd before/base
   kustomize create --autodetect
   ```

3. **Inspect the Kustomization in the Base Directory**  
   Verify the newly created Kustomization file:
   ```bash
   ls -l
   cat kustomization.yaml
   ```

4. **Build the Kustomization in the Base Directory**  
   Generate the configuration and ensure it includes the Deployment and Service without any modifications:
   ```bash
   kustomize build .
   ```

5. **Create a Kustomization in the Overlay Directory**  
   Set up a new overlay directory and reference the base as a resource:
   ```bash
   cd .. && mkdir overlays
   cd overlays
   kustomize create --resources ../base
   ```

6. **Add Build Metadata**  
   Add the `managed-by` label to indicate the configuration was rendered by Kustomize:
   ```bash
   kustomize edit add buildmetadata managedByLabel
   ```

7. **Inspect the Overlay Kustomization**  
   Review the Kustomization file in the overlay directory:
   ```bash
   cat kustomization.yaml
   ```

8. **Build the Kustomization in the Overlay Directory**  
   Render the configuration and confirm that the Deployment and Service include the `managed-by` label:
   ```bash
   kustomize build .
   ```

   Example output:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     labels:
       app: todo
       app.kubernetes.io/managed-by: kustomize-v5.2.1
     name: todo
   spec:
     ports:
     - port: 3000
       targetPort: 3000
     selector:
       app: todo
     type: LoadBalancer
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     labels:
       app: todo
       app.kubernetes.io/managed-by: kustomize-v5.2.1
     name: todo
   spec:
     selector:
       matchLabels:
         app: todo
     template:
       metadata:
         labels:
           app: todo
       spec:
         containers:
         - image: ghcr.io/username/todo:1.0
           imagePullPolicy: IfNotPresent
           name: todo
           ports:
           - containerPort: 3000
         securityContext:
           runAsGroup: 0
           runAsUser: 0
   ```

## Summary

Congratulations! You've created your first Kustomize overlay to generate a variant of a base configuration. This lab demonstrated how to use Kustomize to extend and modify Kubernetes configurations, a foundational skill for managing Kubernetes environments effectively.
