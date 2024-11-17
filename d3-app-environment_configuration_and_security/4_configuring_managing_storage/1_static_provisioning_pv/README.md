# Lab: Create NFS Storage in GCP

## Objectives
- Learn how to create and manage an NFS-backed Persistent Volume (PV) in GCP.
- Understand how to use GCP Filestore for NFS storage.
- Deploy applications that utilize the NFS storage for shared access.

## Prerequisites
- A Google Kubernetes Engine (GKE) cluster.
- GCloud Filestore API enabled.

## Steps

### Step 1: Create a Google Filestore Instance
1. Create a Filestore instance with a 1TB capacity (this process can take up to 10 minutes):
    ```bash
    gcloud filestore instances create nfs-server \
        --zone=asia-southeast1-c \
        --tier=STANDARD \
        --file-share=name="vol1",capacity=1TB \
        --network=name="default"
    ```

2. Enable the `file.googleapis.com` API if prompted:
    ```bash
    API [file.googleapis.com] not enabled on project [PROJECT_ID]. Would you like to enable and retry (this will take a few minutes)? (y/N)? y
    ```

### Step 2: Retrieve the Filestore Instance IP Address
1. List Filestore instances and note the `IP_ADDRESS`:
    ```bash
    gcloud filestore instances list
    ```

2. Save the IP address to a variable:
    ```bash
    IP=$(gcloud filestore instances list | grep IP_ADDRESS | cut -d : -f 2)
    ```

### Step 3: Static Provisioning of Persistent Volumes
1. Create a Persistent Volume (PV) using the retrieved IP address:
    ```bash
    sed "s/1.2.3.4/$IP/g" GFS-PersistentVolume.yaml | kubectl apply -f-
    ```

2. Verify the PV is created:
    ```bash
    kubectl get PersistentVolume fileserver
    ```

3. Describe the PV to inspect its configuration:
    ```bash
    kubectl describe PersistentVolume fileserver
    ```

### Step 4: Create a Persistent Volume Claim (PVC)
1. Create a PVC for the PV:
    ```bash
    kubectl apply -f GFS-PersistentVolumeClaim.yaml
    ```

2. Verify the PVC status:
    ```bash
    kubectl get PersistentVolume
    kubectl get PersistentVolumeClaim fileserver-claim
    ```

3. Inspect the PVC details:
    ```bash
    kubectl describe PersistentVolumeClaim fileserver-claim
    ```

### Step 5: Deploy Pods with NFS Mount
1. Create two pods that mount the NFS volume:
    ```bash
    kubectl apply -f GFS-Pods.yaml
    ```

2. Test NFS functionality:
    - Access the first pod and write data:
      ```bash
      kubectl exec -it my-pod1 -- /bin/bash
      echo "Hello students" > workdir/test.txt
      exit
      ```

    - Delete the first pod:
      ```bash
      kubectl delete pod my-pod1
      ```

    - Access the second pod and verify the data:
      ```bash
      kubectl exec -it my-pod2 -- cat workdir/test.txt
      ```

### Step 6: Deploy Application Using NFS
1. Create a Deployment with a PVC mounted:
    ```bash
    kubectl apply -f nfs.nginx.yaml
    ```

2. Access the deployed application through the NFS mount:
    ```bash
    kubectl exec -it my-pod2 -- curl http://nginx-nfs-service/web-app/demo.html
    ```

### Step 7: Control PV Access and Scale Deployment
1. Scale the deployment to 4 replicas:
    ```bash
    kubectl scale deployment nginx-nfs-deployment --replicas=4
    ```

2. Verify multiple pods share the same NFS storage:
    ```bash
    kubectl describe PersistentVolumeClaim fileserver-claim
    ```

3. Delete the deployment and clean up resources:
    ```bash
    kubectl delete deployment nginx-nfs-deployment
    kubectl delete pod my-pod2
    ```

### Step 8: Clean Up Resources
1. Delete the PVC and PV:
    ```bash
    kubectl delete PersistentVolumeClaim fileserver-claim
    kubectl delete PersistentVolume fileserver
    ```

2. Delete the Filestore instance:
    ```bash
    gcloud filestore instances delete nfs-server --zone=asia-southeast1-c
    ```

## Summary
In this lab, you:
- Created a GCP Filestore instance for NFS storage.
- Configured a Kubernetes PV and PVC for the Filestore.
- Deployed applications sharing data via NFS.
- Learned about PV access modes and reclaim policies.
