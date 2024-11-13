# Lab: Create and Package Helm Charts

## Introduction
In this lab, we will learn:
- How to create a Helm chart using `helm create`.
- How to update the chart with Docker image information, app version, and chart version.
- How to convert the Kubernetes service to a LoadBalancer type and install the chart using `helm install`.
- How to package the Helm chart using `helm package` with `--app-version` and `--version` options.
- [Docker Image used](https://github.com/users/hungtran84/packages/container/package/frontend).

## Objectives
- Create a new Helm Chart using `helm create`.
- Update the Chart with Docker image information, app version, and chart version.
- Modify the Kubernetes Service to use `LoadBalancer` type.
- Customize the deployment template to use `.Values.service.targetPort` for `containerPort`, `readinessProbe`, and `livenessProbe`.
- Package the Helm Chart and manage versioning.
- Install and test the Helm Chart.

## Steps

### 1. Navigate to the Lab Directory and Remove Existing Chart

```sh
# Navigate to the lab directory
cd d2-app-deployment/2_helm/5_create_and_package_chart

# Remove the existing directories: myfirstchart and packages
rm -rf myfirstchart
rm -rf packages
```

### 2. Create the Helm Chart Again

```sh
# Helm Create Chart
helm create myfirstchart

# Observation:
# 1. It will create a base Helm Chart template.
# 2. We can call it a starter chart.
```

### 3. Update `Chart.yaml` File

Update the `Chart.yaml` file to specify the chart version and app version.

```yaml
# Chart.yaml
apiVersion: v2
name: myfirstchart
description: A simple Helm chart for deploying a sample app
version: 1.0.0  # Define the chart version
appVersion: "1.0"  # Define the app version (Docker image version)
```

### 4. Customize the Existing Chart

#### a. Update `values.yaml` with Docker Image Repository and Service Type

Modify `values.yaml` to update the Docker image repository and change the service type to `LoadBalancer`.

```yaml
# values.yaml
image:
  repository: ghcr.io/hungtran84/frontend  # Change to your custom image repository
  pullPolicy: IfNotPresent
  tag: ""  # Defaults to chart appVersion if not provided

service:
  type: LoadBalancer  # Change service type to LoadBalancer
  port: 80
  targetPort: 4200  # Define targetPort for the service
```

#### b. Modify `deployment.yaml` for `containerPort`, `readinessProbe`, and `livenessProbe`

In `myfirstchart/templates/deployment.yaml`, update the deployment template to use `.Values.service.targetPort` for `containerPort`, `readinessProbe`, and `livenessProbe`.

```yaml
# deployment.yaml
containers:
  - name: {{ .Chart.Name }}
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
    ports:
      - containerPort: {{ .Values.service.targetPort }}  # Use targetPort from values.yaml
    readinessProbe:
      httpGet:
        path: /
        port: {{ .Values.service.targetPort }}
    livenessProbe:
      httpGet:
        path: /
        port: {{ .Values.service.targetPort }}
```

### 5. Install the Chart

```sh
# Install the Helm Chart
helm install myapp1v1 myfirstchart

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v1 --show-resources

# Using kubectl commands to verify
kubectl get pods
kubectl get svc

# Access the application in a browser
export SERVICE_IP=$(kubectl get svc --namespace default myapp1v1-myfirstchart --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")

open http://$SERVICE_IP:80
```

### 6. Package the Helm Chart

```sh
# Package the Helm Chart with version 1.0.0
helm package myfirstchart/ --destination 1-helm/lab8_create_and_package_chart/packages/

# Review the packaged file
ls -lrta 1-helm/lab8_create_and_package_chart/packages/
```

### 7. Update Chart Version and Repackage

Update the `Chart.yaml` to change the chart version to `1.1.0` and `appVersion` to the new Docker tag.

```yaml
# Chart.yaml
version: 1.1.0
description: A Helm Chart with LoadBalancer Service
appVersion: "1.1"  # Update Docker Image tag version
```

```sh
# Package the Helm Chart with updated version
helm package myfirstchart/ --destination 1-helm/lab8_create_and_package_chart/packages/
```

### 8. Install the Packaged Chart and Verify

```sh
# Install the Helm Chart from the packaged file
helm install myapp1v11 1-helm/lab8_create_and_package_chart/packages/myfirstchart-1.1.0.tgz

# Using kubectl commands to verify
kubectl get pods
kubectl get svc

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v11 --show-resources

# Access the application in a browser
export SERVICE_IP=$(kubectl get svc --namespace default myapp1v11-myfirstchart --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")

open http://$SERVICE_IP:80
```

### 9. Package the Helm Chart with Specific Version

```sh
# Package with specific app-version and version
helm package myfirstchart/ --app-version "2.0" --version "2.0.0" --destination 1-helm/lab8_create_and_package_chart/packages/
```

### 10. Install the Packaged Chart with New Version

```sh
# Install from packaged chart with version "2.0.0"
helm install myapp1v2 1-helm/lab8_create_and_package_chart/packages/myfirstchart-2.0.0.tgz

# Using kubectl commands to verify
kubectl get pods
kubectl get svc

# List Helm Releases
helm list
helm list --output=yaml

# Helm Status
helm status myapp1v2 --show-resources

# Access the application in a browser
export SERVICE_IP=$(kubectl get svc --namespace default myapp1v2-myfirstchart --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")

open http://$SERVICE_IP:80
```

### 11. Uninstall the Helm Releases

```sh
# List Helm Releases
helm list
helm list --output=yaml

# Uninstall Helm Releases
helm uninstall myapp1v1
helm uninstall myapp1v11
helm uninstall myapp1v2

# Cleanup helm chart
rm -rf myfirstchart
```

### 12. Helm Show Commands

You can use `helm show` to display information about a chart.

```sh
# Show information about the chart
helm show chart myfirstchart/
helm show chart 1-helm/lab8_create_and_package_chart/packages/myfirstchart-2.0.0.tgz

# Show values
helm show values myfirstchart/
helm show values 1-helm/lab8_create_and_package_chart/packages/myfirstchart-2.0.0.tgz

# Show readme
helm show readme myfirstchart/
helm show readme 1-helm/lab8_create_and_package_chart/packages/myfirstchart-2.0.0.tgz

# Show all details
helm show all myfirstchart/
helm show all 1-helm/lab8_create_and_package_chart/packages/myfirstchart-2.0.0.tgz

# Cleanup helm chart
rm -rf myfirstchart
```

## Summary
In this lab, we:
- Created a new Helm chart using `helm create`.
- Updated the `Chart.yaml` with the chart version and app version (Docker image version).
- Customized the chart by updating the `values.yaml` with Docker image details and service type to `LoadBalancer`.
- Modified the `deployment.yaml` to use `.Values.service.targetPort` for `containerPort`, `readinessProbe`, and `livenessProbe`.
- Installed the Helm chart and tested it by accessing the application through the LoadBalancer IP.
- Packaged the chart and tested different versions using `helm package`.
- Cleaned up by uninstalling the Helm releases and removing the chart files.
