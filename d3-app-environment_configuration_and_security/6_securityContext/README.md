# Lab: Security Contexts in Kubernetes Pods

## Objectives

1. Configure a pod (`api-pod`) with strict security policies:
   - Run as specific user ID and group ID.
   - Add capability to bind to privileged ports.
   - Prevent privilege escalation.

2. Configure a pod (`cache-pod`) with secure access:
   - Run under a specific user and group ID.
   - Drop unnecessary capabilities.
   - Ensure root filesystem is read-only while allowing write access to a specific volume.

3. Verify that the configured security contexts are correctly applied by accessing the pods and running validation commands.

---

## Steps

### Task 1: Configure `api-pod` Security Context

**Requirements:**
- User ID: `2000`, Group ID: `3000`
- Add capability: `CAP_NET_BIND_SERVICE`
- Prevent privilege escalation

1. **Edit `api-pod.yaml`:**

   ```bash
   vim api-pod.yaml
   ```

   Add the following configuration under the container spec:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: api-pod
   spec:
     containers:
     - name: busybox
       image: busybox:stable
       command: ['sh', '-c', 'while true; do echo Running...; sleep 5; done']
       securityContext:
         runAsUser: 2000
         runAsGroup: 3000
         capabilities:
           add:
             - CAP_NET_BIND_SERVICE
         allowPrivilegeEscalation: false
   ```

2. **Apply the configuration:**

   ```bash
   kubectl apply -f api-pod.yaml
   ```

3. **Verify the security context settings:**

   Access the `api-pod` and validate the settings.

   ```bash
   kubectl exec -it api-pod -- sh
   ```

   - **Check the user and group ID:**

     ```bash
     id
     ```

     Expected output:
     ```
     uid=2000 gid=3000 groups=3000
     ```

   - **Verify the capability `CAP_NET_BIND_SERVICE`:**

     ```bash
     cat /proc/1/status | grep CapEff
     ```

     Ensure the output contains the hexadecimal value indicating `CAP_NET_BIND_SERVICE` is enabled (e.g., `0000000000002000`).

   - **Confirm privilege escalation is disabled:**

     ```bash
     cat /proc/1/status | grep NoNewPrivs
     ```

     Expected output:
     ```
     NoNewPrivs: 1
     ```

   Exit the pod:

   ```bash
   exit
   ```

---

### Task 2: Configure `cache-pod` Security Context

**Requirements:**
- User ID: `4050`, Group ID: `4050`
- Drop capability: `SYS_TIME`
- Ensure root filesystem is read-only
- Allow write access to `/var/cache` using a volume

1. **Edit `cache-pod.yaml`:**

   ```bash
   vim cache-pod.yaml
   ```

   Add the following configuration:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: cache-pod
   spec:
     containers:
     - name: busybox
       image: busybox:stable
       command: ['sh', '-c', 'while true; do echo Running...; sleep 5; done']
       securityContext:
         runAsUser: 4050
         runAsGroup: 4050
         capabilities:
           drop:
             - SYS_TIME
         readOnlyRootFilesystem: true
       volumeMounts:
       - mountPath: /var/cache
         name: cache-volume
     volumes:
       - name: cache-volume
         emptyDir: {}
   ```

2. **Apply the configuration:**

   ```bash
   kubectl apply -f cache-pod.yaml
   ```

3. **Verify the security context settings:**

   Access the `cache-pod` and validate the settings.

   ```bash
   kubectl exec -it cache-pod -- sh
   ```

   - **Check the user and group ID:**

     ```bash
     id
     ```

     Expected output:
     ```
     uid=4050 gid=4050 groups=4050
     ```

   - **Verify the capability `SYS_TIME` is dropped:**

     Attempt to set the system time:

     ```bash
     date --set="2023-01-01 00:00:00"
     ```

     Expected output:
     ```
     date: cannot set date: Operation not permitted
     ```

   - **Confirm root filesystem is read-only:**

     Try creating a file in the root filesystem:

     ```bash
     touch /testfile
     ```

     Expected output:
     ```
     touch: cannot touch '/testfile': Read-only file system
     ```

   - **Ensure write access to `/var/cache`:**

     Create a file in `/var/cache`:

     ```bash
     touch /var/cache/testfile
     ls /var/cache
     ```

     Expected output:
     ```
     testfile
     ```

   Exit the pod:

   ```bash
   exit
   ```

---

## Summary

In this lab, you:

1. Configured strict security contexts for `api-pod` and `cache-pod`.
2. Verified the security settings by accessing the pods and running commands to validate user/group IDs, capabilities, privilege escalation prevention, and filesystem permissions.
