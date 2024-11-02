# D1.1.2a - Ambassador Pattern

The Ambassador Container Pattern refers to a design pattern where a secondary container in a pod acts as a proxy for the primary application container. This pattern is particularly useful in various scenarios, including:

- **Enabling HTTP Basic Authentication**: By routing traffic through a secondary container that handles authentication.
- **SSL/TLS Termination**: When the primary application runs on HTTP, and you need to expose it over HTTPS, you can use a secondary container (like Nginx) to manage secure connections.
- **Request Filtering**: If you want to drop connections from clients that do not provide a user agent, you can configure the ambassador container to filter requests accordingly.

## Example Configuration

This section demonstrates how to set up a simple ambassador container pattern using Kubernetes.

### 1. Creating the Essential Service and ConfigMap

Create a file named `00-init.yaml` to set up the necessary service and store the Nginx configurations as a ConfigMap.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: common-service
spec:
  selector:
    app: common-pod
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  reverse-proxy-drop-useragent: |
    server {
      listen 80;
      server_name _;
      
      if ($http_user_agent = "") { return 403; }

      location / {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $http_host;
      }
    }
```

#### Explanation

- **Service**: This exposes the pod to receive traffic on port 80.
- **ConfigMap**: This stores the Nginx configuration, which includes a condition to return a 403 Forbidden response if the user agent is empty. It proxies requests to the primary application running on port 8080.

### 2. Setting Up the Pod with Ambassador Container

Create another file named `01-ambassador.yaml` to define the pod with both the application and the ambassador container.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: common-pod
  labels:
    app: common-pod
spec:
  containers:
  - image: webratio/nodejs-http-server
    name: web-container
  - image: nginx:latest
    name: ambassador-container
    volumeMounts:
      - name: nginx
        mountPath: /etc/nginx/conf.d
    ports:
      - containerPort: 80
  volumes:
  - name: nginx
    configMap:
      name: nginx-config
      items:
        - key: reverse-proxy-drop-useragent
          path: default.conf
```

#### Explanation

- **Primary Container**: The `web-container` is based on a Node.js HTTP server image, which listens for incoming HTTP requests.
- **Ambassador Container**: The `ambassador-container` is an Nginx container that handles incoming traffic. It mounts the Nginx configuration from the ConfigMap.
- **Volume Mount**: The Nginx configuration is mounted to `/etc/nginx/conf.d` inside the ambassador container.

### 3. Apply the Configurations

To create the service and the pod, execute the following commands:

```bash
kubectl apply -f 00-init.yaml
kubectl apply -f 01-ambassador.yaml
```

### 4. Testing the Setup

Once both resources are created, you can test the functionality of the ambassador pattern.

#### Testing with a Bare Nginx Pod

**Port Forwarding service**:

```bash
kubectl port-forward service/common-service 8888:80 &
```

**Run a Bare Nginx Pod**: Start a bare Nginx pod in the default namespace using the following command:

```bash
kubectl run nginx-test --image=nginx:alpine -it --rm -- sh
```

This command will start a pod named `nginx-test` and access to the shell.

**Send Requests Without a User-Agent**: 

Inside the pod's shell, run the following curl command without a User-Agent header to test the ambassador behavior:

```bash
curl http://localhost:8888
```

**Expected output**:

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Index of /</title>
</head>
<body>
<h1>Index of /</h1>
<table></table>
<br><address>Node.js v4.7.0/ <a href="https://github.com/jfhbrook/node-ecstatic">ecstatic</a> server running @ localhost:8888</address>
</body></html>% 
```

**Send Requests with an Empty User-Agent**: 

Now, send a request while including an empty User-Agent header. Inside the same pod shell, run:

```bash
curl -iH 'User-Agent:' localhost:8888
```

You should receive an error with **403 Forbidden**:

```
HTTP/1.1 403 Forbidden
Server: nginx/1.27.2
Date: Fri, 01 Nov 2024 19:11:38 GMT
Content-Type: text/html
Content-Length: 153
Connection: keep-alive

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.27.2</center>
</body>
</html>
```

## Conclusion

This setup effectively demonstrates how to implement the ambassador container pattern in Kubernetes, allowing for enhanced traffic management and security features for your applications. By testing with and without a User-Agent, you can see how the Nginx ambassador controls access to the main application based on request headers.
