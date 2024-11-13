## Lab: Building, Installing/Upgrading, Rolling Back, and Deleting a Helm Chart

### Prerequisites
- Helm CLI installed
- Kubernetes cluster running
- kubectl configured to access the cluster
- NGINX Ingress installed

### Objectives
- Build a Helm chart from scratch
- Install a Helm chart
- Render Helm chart templates locally
- Add dependencies to the chart
- Install, upgrade, and delete a Helm chart
- Clean up resources after installation

### Steps

#### 1. Building Helm Chart from Scratch

1. **Create Chart Directory and Templates**
   ```shell
   mkdir guestbook
   mkdir -p guestbook/charts/backend/templates
   mkdir -p guestbook/charts/database/templates
   mkdir -p guestbook/charts/frontend/templates
   cp 1-helm/lab6_helm_chart_version2/yaml/backend* guestbook/charts/backend/templates
   cp 1-helm/lab6_helm_chart_version2/yaml/mongo* guestbook/charts/database/templates
   cp 1-helm/lab6_helm_chart_version2/yaml/frontend* guestbook/charts/frontend/templates
   cp 1-helm/lab6_helm_chart_version2/yaml/ingress* guestbook/charts/frontend/templates
   ```

2. **Create `Chart.yaml` for the Main Chart**
   ```yaml
   # vim guestbook/Chart.yaml
   apiVersion: v2
   name: guestbook
   appVersion: "2.0"
   description: A Helm chart for Guestbook 2.0
   version: 1.1.0
   type: application
   ```

3. **Create `Chart.yaml` for Subcharts (backend, frontend, database)**

   - **Backend Chart**
     ```yaml
     # vim guestbook/charts/backend/Chart.yaml
     apiVersion: v2
     name: backend
     appVersion: "1.0"
     description: A Helm chart for Guestbook Backend 1.0
     version: 0.1.0
     type: application
     ```

   - **Frontend Chart**
     ```yaml
     # vim guestbook/charts/frontend/Chart.yaml
     apiVersion: v2
     name: frontend
     appVersion: "2.0"
     description: A Helm chart for Guestbook Frontend 2.0
     version: 1.1.0
     type: application
     ```

   - **Database Chart**
     ```yaml
     # vim guestbook/charts/database/Chart.yaml
     apiVersion: v2
     name: database
     appVersion: "3.6"
     description: A Helm chart for Guestbook Database MongoDB 3.6
     version: 0.1.0
     type: application
     ```

4. **Package the Chart**
   ```shell
   helm package guestbook
   ```

5. **Render Chart Templates Locally**
   ```shell
   helm template guestbook
   ```

#### 2. Installing a Chart

1. **Install `guestbook` Chart**
   ```shell
   helm install demo-guestbook guestbook
   ```

   Output:
   ```
   NAME: demo-guestbook
   LAST DEPLOYED: Sun Sep 17 16:24:51 2023
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   ```

2. **Get the `frontend` Pods**
   ```shell
   kubectl get pod -l app=frontend
   ```

   Output:
   ```
   NAME                        READY   STATUS    RESTARTS   AGE
   frontend-5548f6f498-vvzjs   1/1     Running   0          20m
   ```

3. **List All Helm Releases in Current Namespace**
   ```shell
   helm list
   ```

   Output:
   ```
   NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
   demo-guestbook  default         1               2023-09-16 16:57:11.664022 +0700 +07    deployed        guestbook-0.1.0 1.0
   ```

4. **Fetch the Manifest for `demo-guestbook` Release**
   ```shell
   helm get manifest demo-guestbook
   ```

5. **Examine the Ingress Resource and Get External IP Address**
   ```shell
   kubectl get ingress guestbook-ingress
   ```

   Output:
   ```
   NAME                CLASS   HOSTS                                  ADDRESS        PORTS   AGE
   guestbook-ingress   nginx   frontend.gke.local,backend.gke.local   34.87.76.196   80      32m
   ```

   ```shell
   EXTERNAL_IP=$(kubectl get ingress guestbook-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   ```

6. **Add Local Host Entries (If Not Available)**
   ```shell
   echo "$EXTERNAL_IP frontend.gke.local" | sudo tee -a /etc/hosts
   echo "$EXTERNAL_IP backend.gke.local" | sudo tee -a /etc/hosts
   ```

7. **Access the Frontend Web UI**
   Open the frontend at `http://frontend.gke.local`

   ![Guestbook Web UI](image.png)

#### 3. Cleanup Resources

1. **Uninstall `demo-guestbook` Chart**
   ```shell
   helm uninstall demo-guestbook
   ```

2. **Remove the Chart Directory**
   ```shell
   rm -rf guestbook/
   ```

### Summary
In this lab, you learned how to:
- Build a Helm chart from scratch, including creating templates and defining dependencies.
- Install, upgrade, and manage Helm charts with subcharts.
- Render Helm chart templates locally.
- Clean up resources after installation.
