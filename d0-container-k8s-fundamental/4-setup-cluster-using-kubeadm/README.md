### 1. Requirements
Ensure each machine meets the following requirements:
- **Memory**: 4 GB or more RAM per machine.
- **CPU**: At least 2 CPUs on the control plane machine.
- **Network Connectivity**: Full connectivity between all nodes in the cluster, and internet access to pull required containers. Private registries can also be used if configured.

### 2. Set up Google Cloud Shell
Cloud Shell provides a free, browser-based environment for working with Google Cloud and offers default project and region configurations.

1. **Start Cloud Shell**: Launch a Cloud Shell session from your Google Cloud console.
2. **Set the Default Compute Region and Zone**: Define the region and zone close to your physical location for optimal performance.

   ```sh
   gcloud config set compute/region asia-southeast1
   gcloud config set compute/zone asia-southeast1-c
  
   ```

    Expected output:

    ```txt
    API [compute.googleapis.com] not enabled on project [ckad-23112024]. Would you like to enable and retry (this will take a few minutes)? (y/N)?  y

    Enabling service [compute.googleapis.com] on project [ckad-23112024]...
    Operation "operations/acf.p2-378697186890-a1288866-b712-48cd-8d90-4669166b3a42" finished successfully.
    WARNING: Property validation for compute/region was skipped.
    Updated property [compute/region].
    WARNING: Property validation for compute/zone was skipped.
    Updated property [compute/zone].
    ```


3. **Verify Configuration**:

   ```sh
   gcloud config list
   ```

   This will display your current region, zone, account, and project settings.

### 3. Create VM Instances for Control Plane and Worker Nodes
To build a Kubernetes cluster, we'll set up one control plane node and two worker nodes. Use the `e2-medium` machine type, which provides 2 vCPUs and 4GB RAM, and configure each with a 50GB boot disk.

1. **Create the Control Plane Node**:

   ```sh
   gcloud compute instances create cp1 \
     --machine-type=e2-medium \
     --image=ubuntu-2004-focal-v20240519 \
     --image-project=ubuntu-os-cloud \
     --boot-disk-size=50GB
   ```

2. **Create the Worker Nodes**:

   ```sh
   for i in 1 2; do
       gcloud compute instances create node${i} \
           --machine-type=e2-medium \
           --image=ubuntu-2004-focal-v20240519 \
           --image-project=ubuntu-os-cloud \
           --boot-disk-size=50GB
   done
   ```

3. **Allow NodePort Access**: This rule allows access to services exposed on NodePorts (ports 30000-40000).

   ```sh
   gcloud compute firewall-rules create nodeports --allow tcp:30000-40000
   ```

4. **Verify VM Creation**:

   ```sh
   gcloud compute instances list
   ```

5. **Connect to Each VM**: SSH into each node to configure Kubernetes.

   ```sh
   gcloud compute ssh cp1   --zone asia-southeast1-c
   gcloud compute ssh node1 --zone asia-southeast1-c
   gcloud compute ssh node2 --zone asia-southeast1-c
   ```

6. **Cleanup (Optional)**: Delete the instances and firewall rule if you need to reset the setup.

   ```sh
   gcloud compute instances delete cp1 node1 node2 --quiet
   gcloud compute firewall-rules delete nodeports
   ```

### 4. Install and Configure Containerd (All Nodes)
`containerd` is the recommended container runtime for Kubernetes. This setup is required on all nodes.

1. **Load Kernel Modules for Kubernetes Networking**:

Loading specific kernel modules is necessary to enable features required for network management in Kubernetes. The following modules are commonly needed:

- **overlay**: This module is used to enable overlay networking, allowing Kubernetes to create virtual networks that span multiple hosts.
- **br_netfilter**: This module allows bridge traffic to be processed by iptables, which is crucial for the proper functioning of network policies and traffic filtering.

   ```sh
   cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
   overlay
   br_netfilter
   EOF
   ```

   Then, load these modules manually:

   ```sh
   sudo modprobe overlay
   sudo modprobe br_netfilter
   ```

2. **Set Up Networking Sysctl Parameters**: Enable network bridging and IP forwarding to ensure proper network traffic handling within the cluster. The following parameters are commonly set:

- `net.bridge.bridge-nf-call-iptables = 1`: This setting ensures that packets traversing bridges are processed by iptables, allowing for effective network policy enforcement.

- `net.bridge.bridge-nf-call-ip6tables = 1`: Similar to the above, but for IPv6 traffic.

- `net.ipv4.ip_forward = 1`: This enables IP forwarding, allowing pods on different nodes to communicate with each other.

   ```sh
   cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
   net.bridge.bridge-nf-call-iptables  = 1
   net.bridge.bridge-nf-call-ip6tables = 1
   net.ipv4.ip_forward                 = 1
   EOF
   sudo sysctl --system
   ```


3. **Install Containerd**:

   ```sh
   sudo apt-get update
   sudo apt-get install -y containerd
   ```

### 5. Install Kubernetes Packages (All Nodes)
Install `kubeadm`, `kubelet`, and `kubectl`, which are required for setting up and managing the cluster.

1. **Add the Kubernetes Repository**:

   ```sh
   sudo mkdir -p /etc/apt/keyrings
   echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
   ```

2. **Install Kubernetes Packages** (using version 1.30.0 to match later upgrade exercises):

   ```sh
   VERSION=1.30.0
   sudo apt-get update
   sudo apt-get install -y kubelet=$VERSION-1.1 kubeadm=$VERSION-1.1 kubectl=$VERSION-1.1
   sudo apt-mark hold kubelet kubeadm kubectl containerd
   ```

3. **Enable kubelet and containerd on Startup**:

   ```sh
   sudo systemctl enable kubelet.service
   sudo systemctl enable containerd.service
   ```

    > [!NOTE]  
    > The kubelet will enter a crashloop until a cluster is created or the node is joined to an existing cluster.

### 6. Create the Kubernetes Cluster (On Control Plane Node `cp1`)
Use `kubeadm` to bootstrap the control plane node.

1. **Initialize the Cluster**:

    To retrieve the public IP address of CP1 directly from the instance metadata, use the following command:

    ```sh
    PUBLIC_IP=$(curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip -H "Metadata-Flavor: Google")
    ```

   ```sh
   sudo kubeadm init --kubernetes-version=${VERSION} --pod-network-cidr=192.168.0.0/16 --apiserver-cert-extra-sans=${PUBLIC_IP}
   ```

    #### What does the command do?

    - **Initialize the Cluster**: Sets up the Kubernetes control plane components.
    - **Specify Kubernetes Version**: Uses the version specified in `${VERSION}`.
    - **Define Pod Network CIDR**: Allocates the IP range for pods in the cluster.
    - **Configure SAN (Subject Alternative Name) for API Server**: Allows secure access using the public IP address.

    #### Important Note

    After the command completes, make sure to note down the `kubeadm join` command provided in the output. This command is crucial for adding worker nodes to your cluster.


2. **Configure kubectl for the Current User**: This allows you to run `kubectl` commands without needing elevated privileges.

   ```sh
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

3. **Install the Calico Network Plugin**: Calico will enable pod networking across nodes.

   ```sh
   kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/master/manifests/calico.yaml
   ```

4. **Check Node Status**: The control plane node should appear as `Ready`.

   ```sh
   kubectl get nodes
   ```

    Expected output:

    ```txt
    NAME   STATUS   ROLES           AGE     VERSION
    cp1    Ready    control-plane   7m52s   v1.30.0
    ```

### 7. Join Worker Nodes to the Cluster
Run the `kubeadm join` command on each worker node (e.g., `node1` and `node2`) to add them to the cluster.

1. **Generate the Join Command** on `cp1` if you missed it:

   ```sh
   sudo kubeadm token create --print-join-command
   ```

2. **Run the Join Command on Each Worker Node**:

   ```sh
   sudo kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash <hash>
   ```

3. **Verify Node Status**:

   ```sh
   kubectl get nodes
   ```

    Expected output:

    ```txt
    NAME    STATUS   ROLES           AGE   VERSION
    cp1     Ready    control-plane   21m   v1.30.0
    node1   Ready    <none>          11m   v1.30.0
    node2   Ready    <none>          11m   v1.30.0
    ```
    > [!NOTE]  
    > After joining a worker node to the control plane using the `kubeadm join` command, it may take some time for the node to become fully ready.


### Step 8: Configure Cloud Shell to Access the Kubernetes Cluster

To access your Kubernetes cluster from Google Cloud Shell using the Control Plane (CP) node's public IP, follow these steps:

1. **Set Up Firewall Rules**

    Ensure that the necessary firewall rules are in place to allow traffic to the Kubernetes API server. Run the following command to create a firewall rule that allows TCP traffic on port `6443` (the default port for the Kubernetes API server):

    ```sh
    gcloud compute firewall-rules create allow-k8s-api --allow tcp:6443
    ```


2. **Copy kubeconfig to Cloud Shell**

    Use `scp` to copy the kubeconfig file from your control plane node to the Cloud Shell's configuration directory. Assuming your kubeconfig is located at `/etc/kubernetes/admin.conf` on the CP node, use the following command (replace `<CP_PUBLIC_IP>` with your Control Plane node's public IP):

   ```bash
    gcloud compute scp cp1:~/.kube/config ~/.kube/config --zone asia-southeast1-c
   ```

3. **Retrieve the Internal and Public IP of CP Node**

    To retrieve the internal and public IP addresses of your Control Plane node directly from Cloud Shell, run the following commands:

    ```sh
    INTERNAL_IP=$(gcloud compute instances describe cp1 --zone asia-southeast1-c --format='get(networkInterfaces[0].networkIP)')
    PUBLIC_IP=$(gcloud compute instances describe cp1 --zone asia-southeast1-c --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
    ```
4. **Update kubeconfig with the Public IP**

    Now, use sed to replace the internal IP address in the kubeconfig file with the retrieved public IP:

    ```sh
    sed -i "s|$INTERNAL_IP|$PUBLIC_IP|g" ~/.kube/config
    ```

    And test access with

    ```sh
    kubectl get no
    ```


### 8. Run End-to-End Tests (On `cp1` or directly from your CloudShell)
Deploy a simple NGINX deployment to test the cluster setup.

1. **Deploy NGINX**:

   ```sh
   kubectl apply -f https://k8s.io/examples/application/deployment.yaml
   ```

2. **Expose NGINX with NodePort**:

   ```sh
   kubectl expose deployment nginx-deployment --type NodePort --port 80

   ```

3. **Check Access**: Replace `<nodeport>` with the actual NodePort number shown in `kubectl get services`.

   ```sh
   kubectl get services 
   ```

   You should get the output like below:

   ```txt
   NAME               TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
   nginx-deployment   NodePort   10.108.181.231   <none>        80:32453/TCP   28m
   ```

   the `<nodeport>` is 32453

   Retrive the `EXTERNAL_IP` of 3 nodes of the cluster with

   ```sh
   gcloud compute instances list
   ```

   Now you should be able to access to nginx web from CloudShell with a simple curl command

   ```sh
   curl --head http://<node1_external_ip>:<nodeport>
   curl --head http://<node1_external_ip>:<nodeport>
   curl --head http://<cp1_external_ip>:<nodeport>
   ```

    Expected output:

    ```txt
    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Wed, 30 Oct 2024 18:01:22 GMT
    Content-Type: text/html
    Content-Length: 612
    Last-Modified: Tue, 04 Dec 2018 14:44:49 GMT
    Connection: keep-alive
    ETag: "5c0692e1-264"
    Accept-Ranges: bytes
    ```

### Conclusion
In this lab, we have successfully set up a Kubernetes cluster using `kubeadm`, one of the simplest ways to deploy your cluster. This approach is versatile and can be implemented across various types of infrastructure, from cloud virtual machines to bare metal servers on-premises.

By using a `kubeadm-based` cluster, you gain full control over the Kubernetes control plane, which is not the case with managed Kubernetes services like EKS, AKS, and the upcoming GKE. This level of control allows for greater customization and flexibility in managing your cluster.

It's also worth noting that all CKx exams utilize kubeadm clusters as their examination environment, making this experience particularly relevant for certification preparation.

As you continue your journey in exploring Kubernetes, remember that it’s normal to encounter concepts that may seem complex at first. There’s no need to worry about understanding everything right away; in due time, you will dive deep into every aspect of the Kubernetes cluster.

Finally, this cluster is disposable, so feel free to delete and recreate it as needed to become more familiar with the setup process. Embrace the learning experience and enjoy your journey into the world of Kubernetes!