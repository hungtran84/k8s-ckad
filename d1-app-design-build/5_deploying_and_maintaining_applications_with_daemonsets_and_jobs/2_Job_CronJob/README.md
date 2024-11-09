# Lab Guide: Executing Tasks with Kubernetes Jobs

## Objectives
- Learn to create and manage Kubernetes Jobs.
- Understand Job configurations like `restartPolicy`, `backoffLimit`, and parallel execution.
- Monitor Job status and troubleshoot using logs and Job descriptions.

## Steps

### 1. Creating a Basic Job
- Define a `restartPolicy` in `job.yaml` since the default `Always` setting isn't compatible with Jobs. Set it to `OnFailure`.

  ```yaml
  # job.yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: hello-world-job
  spec:
    template:
      spec:
        restartPolicy: OnFailure
        containers:
          - name: ubuntu
            image: ubuntu
            command: ["/bin/bash", "-c", "/bin/echo Hello from Pod $(hostname) at $(date)"]
  ```

- Apply the Job:

  ```bash
  kubectl apply -f job.yaml
  ```

- Follow Job status:

  ```bash
  kubectl get job --watch
  ```

- List the Pods, which should show `STATUS` as `Completed`:

  ```bash
  kubectl get pods
  ```

- Describe the Job to see details such as `labels`, `selectors`, `Start Time`, `Duration`, and `Pod Statuses`:

  ```bash
  kubectl describe job hello-world-job
  ```

- Retrieve logs from the Job’s Pod:

  ```bash
  kubectl logs -l job-name=hello-world-job
  ```

- Clean up by deleting the Job, which also deletes its Pods:

  ```bash
  kubectl delete job hello-world-job
  ```

### 2. Handling Job Failures with `backoffLimit` and `restartPolicy`
- To demonstrate failed Jobs, define `restartPolicy: Never` in `job-failure-OnFailure.yaml`, so Pods remain available after failures.

  ```yaml
  # job-failure-OnFailure.yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: hello-world-job-fail
  spec:
    backoffLimit: 2
    template:
      spec:
        restartPolicy: Never
        containers:
          - name: ubuntu
            image: ubuntu
            command: ["/bin/bash", "-c", "/bin/ech Hello from Pod $(hostname) at $(date)"]
  ```

- Apply the Job:

  ```bash
  kubectl apply -f job-failure-OnFailure.yaml
  ```

- Monitor Pods to observe backoff behavior:

  ```bash
  kubectl get pods --watch
  ```

- Describe the Job to understand the backoff behavior and failure details:

  ```bash
  kubectl describe jobs
  ```

- Clean up by deleting the failed Job:

  ```bash
  kubectl delete job hello-world-job-fail
  ```

### Explanation

#### Key Configurations:
- **backoffLimit: 2**: The job will retry up to 2 times if it fails before considering it as failed (total of 3 attempts).
- **restartPolicy: Never**: The container will not be restarted if it fails.
- **Command**: The container runs a shell command (`/bin/bash -c "/bin/ech Hello from Pod $(hostname) at $(date)"`), but there is a typo (`/bin/ech` should be `/bin/echo`).

#### Why Are the Pods in Error Status?
The pods are repeatedly failing because:
- The command `/bin/ech` is incorrect and does not exist, causing the container to exit with an error status.
- The job retries by creating new pods (due to the `backoffLimit`), but each pod fails for the same reason.
- Pods go through various states like **Pending** and **ContainerCreating** before ultimately failing.


### 3. Defining a Parallel Job
- Define a parallel Job to execute multiple Pods concurrently until completion.

  ```yaml
  # ParallelJob.yaml
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: hello-world-job-parallel
  spec:
    parallelism: 10
    completions: 50
    template:
      spec:
        restartPolicy: OnFailure
        containers:
          - name: ubuntu
            image: ubuntu
            command: ["/bin/bash", "-c", "/bin/echo Hello from Pod $(hostname) at $(date)"]
  ```

- Apply the Job:

  ```bash
  kubectl apply -f ParallelJob.yaml
  ```

- List the Pods to observe parallel execution:

  ```bash
  kubectl get pods -w
  ```

- Monitor completion of the Job:

  ```bash
  kubectl get jobs
  ```

- Clean up by deleting the Job:

  ```bash
  kubectl delete job hello-world-job-parallel
  ```

### Explanation of Key Job Configurations

- **parallelism: 10**: This setting allows up to 10 pods to run in parallel for this job. This means that, at any given time, 10 pods can be actively working toward completing the job.

- **completions: 50**: The job requires a total of 50 successful pod executions to be marked as complete. With `parallelism` set to 10, this job will start 10 pods in parallel and continue to create new ones as others complete until it reaches the 50 completions goal.

- **restartPolicy: OnFailure**: The `OnFailure` policy means that if any pod fails, it will be restarted. This is useful for ensuring that the job reaches the required number of completions even if some pods encounter issues.

This configuration results in a job that runs multiple instances of the pod simultaneously, retrying only failed pods, and completes when 50 successful pod runs have been achieved.


### 4. Scheduling Tasks with `CronJobs`

To create a CronJob, apply the configuration file:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello-world-cron
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: ubuntu
            image: ubuntu
            command:
            - "/bin/bash"
            - "-c"
            - "/bin/echo Hello from Pod $(hostname) at $(date)"
          restartPolicy: Never
```

```bash
kubectl apply -f CronJob.yaml
```

```plaintext
cronjob.batch/hello-world-cron created
```

#### Checking the Schedule of the Job

Get a quick overview of the job and its schedule:

```bash
kubectl get cronjobs
```

```plaintext
NAME               SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello-world-cron   */1 * * * *   False     1        2s              20s
```

#### Examining Key CronJob Parameters

Use `describe` to explore CronJob parameters like `Schedule`, `Concurrency`, `Suspend`, `Starting Deadline Seconds`, and `Events`:

```bash
kubectl describe cronjobs | more
```

```plaintext
Name:                          hello-world-cron
Namespace:                     default
Schedule:                      */1 * * * *
Concurrency Policy:            Allow
Suspend:                       False
Successful Job History Limit:  3
Failed Job History Limit:      1
Starting Deadline Seconds:     <unset>
Events:
  Type    Reason            Age   From                Message
  ----    ------            ----  ----                -------
  Normal  SuccessfulCreate  113s  cronjob-controller  Created job hello-world-cron-28206259
  Normal  SawCompletedJob   108s  cronjob-controller  Saw completed job: hello-world-cron-28206259, status: Complete
```

#### Checking Job Overview Again

Verify the job status, schedule, and activity:

```bash
kubectl get cronjobs
```

```plaintext
NAME               SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello-world-cron   */1 * * * *   False     0        41s             2m59s
```

#### Retention of Completed Pods

The pods from the CronJob will remain for log retention or inspection, based on `successfulJobsHistoryLimit`, which defaults to `3`:

```bash
kubectl get pods --watch
```

```plaintext
NAME                              READY   STATUS      RESTARTS   AGE
hello-world-cron-28206260-lgw6d   0/1     Completed   0          2m36s
hello-world-cron-28206263-t94qb   0/1     Completed   0          5s
```

#### Viewing CronJob Configuration in YAML Format

Inspect the CronJob settings in detail:

```bash
kubectl get cronjobs hello-world-cron -o yaml
```

#### Cleaning Up the CronJob

To delete the CronJob:

```bash
kubectl delete cronjobs hello-world-cron
```

```plaintext
cronjob.batch "hello-world-cron" deleted
```

### Explanation of Key CronJob Configurations

- **schedule: "*/1 * * * *"**: This `schedule` field uses a Cron format to define when the CronJob should run. Here, it’s set to `*/1 * * * *`, meaning the job will run every minute.

- **jobTemplate**: The `jobTemplate` specifies the template for the job that will be created on each scheduled run of the CronJob. Within this template, key configurations for the pod and job are set.

- **restartPolicy: Never**: With `restartPolicy` set to `Never`, pods that complete or fail will not restart. This is typical for CronJobs where each execution is treated as an independent run, and the job will proceed to the next scheduled instance without retrying pods.

This configuration results in a CronJob that runs a new pod every minute, where each pod executes the specified command once and then terminates, without restarting. This setup is useful for tasks that don’t require persistence or retries within each scheduled run.


### Summary

In this lab, we explored Kubernetes `Job` and `CronJob` configurations, focusing on their setup, scheduling, and key parameters.

- **Jobs**: We created a `Job` that runs multiple pods in parallel with defined completion and restart policies. This configuration is ideal for **finite, one-time tasks** such as:
  - **Data processing** (e.g., aggregating data from various sources)
  - **Image processing** (e.g., resizing or compressing images)
  - **Batch processing** (e.g., applying updates across a large dataset)
  - **File transformations** (e.g., converting file formats)
  
  The `parallelism` and `completions` fields allowed us to control the level of concurrency and the total number of successful pod executions needed. The `restartPolicy: OnFailure` ensured that any failed pods would restart, helping the job reach its completion target reliably.

- **CronJobs**: We configured a `CronJob` that schedules recurring tasks using Cron syntax, allowing jobs to run at specific times. **CronJobs are suitable for recurring tasks** such as:
  - **Database backups** (e.g., nightly or hourly backups)
  - **System monitoring** (e.g., collecting metrics at regular intervals)
  - **Report generation** (e.g., generating daily or weekly reports)
  - **Data cleanup** (e.g., deleting temporary files periodically)

  By setting the `schedule` field, we specified when the job would run, and with `restartPolicy: Never`, we ensured each scheduled pod executed only once per schedule without restarts.

This lab demonstrated how to effectively use `Job` and `CronJob` resources in Kubernetes to handle both finite and recurring tasks, providing flexible control over pod execution, parallelism, and scheduling for various automation needs.
