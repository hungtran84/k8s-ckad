# Lab: Installing Helm and Deploying MySQL with Helm in Separate Namespaces

## Objectives
- Install Helm on different operating systems.
- Deploy MySQL using both the legacy Helm chart and an OCI-based chart.
- Deploy each release in separate namespaces to avoid conflicts.
- Connect to each MySQL instance using a client pod.
- Run a simple SQL command to validate connectivity.

## Steps

### Step 1: Install Helm

#### Install Helm from Script

Use the following script to install Helm automatically:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

#### Install Helm with Homebrew (macOS)

```bash
brew install helm
```

#### Install Helm with Chocolatey (Windows)

```bash
choco install kubernetes-helm
```

#### Install Helm with Apt (Debian/Ubuntu)

```bash
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

#### Install Helm with dnf/yum

```bash
sudo dnf install helm
```

#### Verify Helm Installation

Check the installed Helm version:

```bash
helm version --short
```

#### Add Helm Repo

Add the stable Helm repository:

```bash
helm repo add stable https://charts.helm.sh/stable
```

### Step 2: Deploy MySQL Using the Legacy Helm Chart

1. **Create a Namespace for Legacy MySQL**  
   Create a namespace to deploy the legacy MySQL chart.

   ```bash
   kubectl create namespace mysql-legacy
   ```

2. **Install MySQL Chart**  
   Deploy the MySQL chart (for testing purposes, as this chart is deprecated) in the `mysql-legacy` namespace.

   ```bash
   helm install mysql-legacy stable/mysql --namespace mysql-legacy
   ```

3. **Get MySQL Root Password**  
   Retrieve the root password for the MySQL instance.

   ```bash
   MYSQL_LEGACY_ROOT_PASSWORD=$(kubectl get secret --namespace mysql-legacy mysql-legacy -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)
   ```

### Step 3: Deploy MySQL Using an OCI Helm Chart

1. **Create a Namespace for OCI MySQL**  
   Create a separate namespace for the OCI-based MySQL deployment.

   ```bash
   kubectl create namespace mysql-oci
   ```

2. **Install OCI-Based MySQL Chart**  
   Deploy the OCI-based MySQL chart in the `mysql-oci` namespace.

   ```bash
   helm install mysql-oci oci://ghcr.io/hungtran84/mysql --namespace mysql-oci
   ```

3. **Get MySQL Root Password**  
   Retrieve the root password for the MySQL instance.

   ```bash
   MYSQL_OCI_ROOT_PASSWORD=$(kubectl get secret --namespace mysql-oci mysql-oci -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)
   ```

### Step 4: Test MySQL Connections

1. **Run a Client Pod for Legacy MySQL**  
   Launch a temporary MySQL client pod to connect to the legacy MySQL instance.

   ```bash
   kubectl run mysql-legacy-client --rm --tty -i --restart='Never' --image docker.io/bitnami/mysql:8.0.34-debian-11-r31 --namespace mysql-legacy --env MYSQL_ROOT_PASSWORD=$MYSQL_LEGACY_ROOT_PASSWORD --command -- bash
   ```

2. **Connect to Legacy MySQL**  
   Inside the client pod, connect to the MySQL server and run a simple SQL command to validate connectivity.

   ```bash
   mysql -h mysql-legacy.mysql-legacy.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"

   exit
   ```

3. **Run a Client Pod for OCI MySQL**  
   Launch a temporary MySQL client pod to connect to the OCI-based MySQL instance.

   ```bash
   kubectl run mysql-oci-client --rm --tty -i --restart='Never' --image docker.io/bitnami/mysql:8.0.34-debian-11-r31 --namespace mysql-oci --env MYSQL_ROOT_PASSWORD=$MYSQL_OCI_ROOT_PASSWORD --command -- bash
   ```

4. **Connect to OCI MySQL**  
   Inside the client pod, connect to the MySQL server and run a simple SQL command to validate connectivity.

   ```bash
   mysql -h mysql-oci.mysql-oci.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"

   exit
   ```

### Step 5: Clean Up Resources

1. **Display Helm Releases**  
   List all Helm releases to confirm installations.

   ```bash
   helm ls --all-namespaces
   ```

2. **Examine Kubernetes Resources**  
   Check resources in each namespace associated with the MySQL deployments.

   ```bash
   helm get manifest mysql-legacy -n mysql-legacy
   helm get manifest mysql-oci -n mysql-oci
   ```

3. **Uninstall Helm Releases**  
   Remove both MySQL releases.

   ```bash
   helm uninstall mysql-legacy --namespace mysql-legacy
   helm uninstall mysql-oci --namespace mysql-oci
   ```

4. **Delete Namespaces**  
   Delete the namespaces used in this lab.

   ```bash
   kubectl delete namespace mysql-legacy
   kubectl delete namespace mysql-oci
   ```

## Summary

In this lab, you installed Helm on your system and deployed two MySQL instances using Helm charts in separate namespaces to avoid conflicts. You connected to each MySQL instance using a client pod, validated connectivity with a simple SQL command, and then cleaned up the resources created during the lab.