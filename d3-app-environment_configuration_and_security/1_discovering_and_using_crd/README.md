# Lab: Discovering and using Custom Resource Definitions (CRDs)

## Objectives

1. Develop a CRD for a logging service (`loggingservice`) to manage log retention policies across namespaces.
2. Implement a CRD for an auto-scaling service (`autoscaler`) to dynamically adjust pods based on resource usage.

## Steps

### Task 1: Logging Service CRD

Create a Custom Resource Definition for a logging service with the following fields:
- **`logRetentionDays`**: Number of days to retain logs.
- **`logLevel`**: Acceptable values are `info`, `warn`, or `error`.

1. Create the CRD file:

   ```bash
   vim loggingservice.yaml
   ```

2. Populate the file with the following content:

   ```yaml
   apiVersion: apiextensions.k8s.io/v1
   kind: CustomResourceDefinition
   metadata:
     name: loggingservices.example.com
   spec:
     group: example.com
     scope: Namespaced
     names:
       plural: loggingservices
       singular: loggingservice
       kind: LoggingService
       shortNames:
         - ls
     versions:
       - name: v1
         served: true
         storage: true
         schema:
           openAPIV3Schema:
             type: object
             properties:
               spec:
                 type: object
                 properties:
                   logRetentionDays:
                     type: integer
                   logLevel:
                     type: string
                     enum: ["info", "warn", "error"]
   ```

3. Deploy the CRD:

   ```bash
   kubectl apply -f loggingservice.yaml
   ```

4. Confirm the CRD is deployed:

   ```bash
   kubectl get crd loggingservices
   ```

5. Test the CRD by applying a resource manifest (`my-service.yaml`) and verifying it:

   ```bash
   kubectl apply -f my-service.yaml
   kubectl get loggingservices
   ```

---

### Task 2: Auto-Scaling Service CRD

Create a Custom Resource Definition for an auto-scaling service with the following fields:
- **`cpuThresholdPercent`**: CPU usage percentage threshold for scaling.
- **`memoryThresholdPercent`**: Memory usage percentage threshold for scaling.

1. Create the CRD file:

   ```bash
   vim autoscalers.yaml
   ```

2. Populate the file with the following content:

   ```yaml
   apiVersion: apiextensions.k8s.io/v1
   kind: CustomResourceDefinition
   metadata:
     name: autoscalers.example.com
   spec:
     group: example.com
     scope: Namespaced
     names:
       plural: autoscalers
       singular: autoscaler
       kind: AutoScaler
       shortNames:
         - as
     versions:
       - name: v1
         served: true
         storage: true
         schema:
           openAPIV3Schema:
             type: object
             properties:
               spec:
                 type: object
                 properties:
                   cpuThresholdPercent:
                     type: integer
                   memoryThresholdPercent:
                     type: integer
   ```

3. Deploy the CRD:

   ```bash
   kubectl apply -f autoscalers.yaml
   ```

4. Test the CRD by applying a resource manifest (`my-autoscaler.yaml`) and verifying it:

   ```bash
   kubectl apply -f my-autoscaler.yaml
   kubectl get autoscalers
   ```

---

## Summary

- Created and deployed a **`loggingservice`** CRD to manage log retention and log levels.
- Created and deployed an **`autoscaler`** CRD to dynamically adjust pods based on resource thresholds.
- Successfully tested both CRDs with example resource manifests.
