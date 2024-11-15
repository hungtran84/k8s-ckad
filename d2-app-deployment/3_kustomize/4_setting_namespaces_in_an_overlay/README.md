# Lab: Using Kustomize to Set Namespaces in Configurations

## Objectives

- Learn how to use **Kustomize** to set a namespace in Kubernetes resource definitions.
- Modify a base configuration with an overlay to set all resource namespaces to `dev`.
- Optionally test the transformed configuration by deploying it to a Kubernetes cluster.

---

## Steps

### 1. Create a Namespace Object
Create a `Namespace` object to use in your Kustomization. This can be done manually or using `kubectl`:

```bash
cd config/overlay
kubectl create namespace dev --dry-run=client -o yaml > namespace.yaml
cat namespace.yaml
```

This generates a `namespace.yaml` file that defines the `dev` namespace.

---

### 2. Modify the Overlay Kustomization
Edit the `kustomization.yaml` file in the overlay directory to include the following content:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../base
  - namespace.yaml
buildMetadata:
  - managedByLabel
namespace: dev
```

- The `resources` section references the base configuration and the `namespace.yaml` file.
- The `namespace` field ensures all resources are scoped to the `dev` namespace.

---

### 3. Build the Kustomization
Run the following command to generate the transformed configuration:

```bash
kustomize build .
```

Verify the output:
- It should include the `Namespace` resource.
- All other resources should have their `metadata.namespace` set to `dev`.

---

### 4. (Optional) Deploy the Transformed Configuration
If you have access to a Kubernetes cluster, you can test the deployment:

```bash
kustomize build . | kubectl apply -f -
```

---

### 5. Verify the Deployment
Check that the resources have been successfully deployed in the `dev` namespace:

```bash
kubectl -n dev get all
```

---

## Summary

In this lab, you learned how to:
- Use **Kustomize** to set namespaces for Kubernetes resources in an overlay.
- Build and inspect transformed configurations.
- Optionally deploy the transformed configurations to a Kubernetes cluster.

This lab introduced the **NamespaceTransformer**, one of the metadata transformers in Kustomize. In subsequent labs, you'll explore additional metadata transformations.
