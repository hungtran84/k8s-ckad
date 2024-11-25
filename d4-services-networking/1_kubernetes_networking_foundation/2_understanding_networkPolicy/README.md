# Lab: Troubleshooting and Fixing Pod Connectivity Issues with NetworkPolicy

## Scenario
You are deploying an application consisting of a PostgreSQL database and a backend service. The database is running, but the `store-backend` Pod fails to start. The failure is due to a misconfigured `NetworkPolicy` that prevents the backend from connecting to the database. Your task is to troubleshoot and resolve the issue, ensuring the `store-backend` Pod enters the `Running` state.

---

## Objectives
1. Deploy a PostgreSQL database and a store-backend application.
2. Apply restrictive `NetworkPolicy` configurations to simulate the connectivity issue.
3. Troubleshoot the issue and update the `NetworkPolicy` to allow the necessary traffic.
4. Verify the backend starts successfully and the issue is resolved.

---

## Step 1: Deploy the Database
1. Create the `db.yml` file for the PostgreSQL database:

   ```yaml
   # db.yml
   apiVersion: v1
   kind: Pod
   metadata:
     name: db
     namespace: app-namespace
     labels:
       app: database
   spec:
     containers:
     - name: postgres
       image: postgres:13
       env:
       - name: POSTGRES_USER
         value: user
       - name: POSTGRES_PASSWORD
         value: password
       - name: POSTGRES_DB
         value: storedb
       ports:
       - containerPort: 5432
         name: postgres
   ```

2. Apply the configuration:
   ```bash
   kubectl apply -f db.yml
   ```

3. Verify the database Pod is running:
   ```bash
   kubectl get pods -n app-namespace
   ```

---

## Step 2: Deploy the Store Backend
1. Create the `backend.yml` file for the store-backend service:

   ```yaml
   # backend.yml
   apiVersion: v1
   kind: Pod
   metadata:
     name: store-backend
     namespace: app-namespace
     labels:
       app: backend
   spec:
     containers:
     - name: backend
       image: busybox
       args:
       - sh
       - -c
       - >
         while true; do
           nc -z db 5432 || exit 1;
           sleep 5;
         done;
   ```

2. Apply the configuration:
   ```bash
   kubectl apply -f backend.yml
   ```

3. Observe that the backend Pod enters a `CrashLoopBackOff` state:
   ```bash
   kubectl get pods -n app-namespace
   kubectl describe pod store-backend -n app-namespace
   ```

---

## Step 3: Apply Restrictive Network Policies
1. Create a default `deny-all` policy in the `deny.yml` file:

   ```yaml
   # deny.yml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: default-deny
     namespace: app-namespace
   spec:
     podSelector: {}
     policyTypes:
     - Ingress
   ```

2. Apply the policy:
   ```bash
   kubectl apply -f deny.yml
   ```

3. Verify that the `store-backend` Pod cannot connect to the database:
   ```bash
   kubectl logs store-backend -n app-namespace
   ```

   The logs will indicate a failure to connect to the database.

---

## Step 4: Fix the NetworkPolicy
1. Create a `netpol.yml` file to allow traffic from the `store-backend` Pod to the database:

   ```yaml
   # netpol.yml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-backend-to-db
     namespace: app-namespace
   spec:
     podSelector:
       matchLabels:
         app: database
     ingress:
     - from:
       - podSelector:
           matchLabels:
             app: backend
       ports:
       - protocol: TCP
         port: 5432
   ```

2. Apply the updated NetworkPolicy:
   ```bash
   kubectl apply -f netpol.yml
   ```

3. Check the `store-backend` Pod logs to confirm successful connectivity:
   ```bash
   kubectl logs store-backend -n app-namespace
   ```

   The logs should no longer show errors.

---

## Step 5: Verify the Resolution
1. Ensure the `store-backend` Pod enters the `Running` state:
   ```bash
   kubectl get pods -n app-namespace
   ```

2. Verify the NetworkPolicy:
   ```bash
   kubectl get networkpolicy -n app-namespace
   ```

---

## Cleanup
1. Remove all resources created during this lab:
   ```bash
   kubectl delete namespace app-namespace
   ```

---

## Summary
In this lab, you:
- Simulated a network connectivity issue by applying a restrictive `NetworkPolicy`.
- Diagnosed and fixed the issue by creating a new `NetworkPolicy` to allow the required traffic.
- Verified the solution by ensuring the `store-backend` Pod started successfully.
