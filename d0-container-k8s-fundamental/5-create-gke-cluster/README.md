# Lab Guide: Creating a Test GKE Cluster from Cloud Shell

## Objective

In this lab, you will create a test Google Kubernetes Engine (GKE) cluster using Google Cloud Shell. This setup is ideal for learning and experimentation without incurring significant costs.

## Prerequisites

- A Google Cloud Platform (GCP) account.
- Access to Google Cloud Console.
- Enabled billing on your GCP account.

## Steps

### 1. **Open Google Cloud Shell**

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click on the Cloud Shell icon (a terminal icon) in the top right corner of the console.

### 2. **Set Your Project**

Set the GCP project where you want to create your GKE cluster. Replace `<YOUR_PROJECT_ID>` with your actual project ID:

```bash
gcloud config set project <YOUR_PROJECT_ID>
```

### 3. **Enable the Kubernetes Engine API**

Enable the Kubernetes Engine API for your project:

```bash
gcloud services enable container.googleapis.com
```

### 4. **Create a GKE Cluster**

Create a low-cost GKE cluster using the following command. This command creates a zonal cluster with a single node pool, a small machine type, and a maximum of 3 nodes to minimize costs. Adjust the name as necessary:

> [!NOTE]  
> Provisioning a GKE cluster may take about 10-15 minutes as the platform needs to create and configure various resources, including virtual machines, networking components, and Kubernetes control plane elements.

```bash
gcloud container clusters create test-cluster \
  --zone asia-southeast1-c \
  --num-nodes 1 \
  --max-nodes 3 \
  --machine-type e2-micro \
  --enable-autoscaling
```

### 5. **Get Credentials for the Cluster**

After the cluster is created, retrieve the credentials to access it:

```bash
gcloud container clusters get-credentials test-cluster --zone asia-southeast1-c
```

### 6. **Verify Cluster Access**

To verify that you can access the cluster, run:

```bash
kubectl get nodes
```

You should see the node(s) in your cluster listed.

### 7. **Deploy a Sample Application**

To test your cluster, deploy a sample application (e.g., NGINX) using the following command:

```bash
kubectl create deployment nginx --image=nginx
```

Then expose the deployment to access it:

```bash
kubectl expose deployment nginx --type NodePort --port 80
```

### 8. **Get the External IP Address**

To access the application, get the external IP address of the node:

```bash
kubectl get service nginx
```

### 9. **Cleanup Resources**

Once you’re done with your experiments, delete the GKE cluster to avoid incurring charges:

```bash
gcloud container clusters delete test-cluster --zone asia-southeast1-c --quiet
```

## Conclusion

You have successfully created a test GKE cluster in Google Cloud using Cloud Shell. This setup provides a cost-effective way to learn and explore Kubernetes. Feel free to experiment further with deployments and services as you continue your Kubernetes journey!
