# CKAD Labs Repository

Welcome to the CKAD Labs repository! This repository is designed to provide hands-on labs to supplement the CKAD (Certified Kubernetes Application Developer) course, guiding you through Docker, Kubernetes fundamentals, application deployment, observability, security, and networking. Each lab corresponds to a specific domain in the CKAD curriculum, helping you gain the practical skills needed for certification.

## Table of Contents

### Domain 0: Docker and Kubernetes Fundamentals
- [Lab 1: Containerize an Application](d0-container-k8s-fundamental/1-containerize-app/README.md)
  - Containerize a python app   
  
- [Lab 2: Using Docker Compose](d0-container-k8s-fundamental/2-docker-compose/README.md)
  - Using Docker Compose

- [Lab 3: Exploring a Kubernetes Cluster](d0-container-k8s-fundamental/3-exploring-k8s-cluster/README.md)
  - Exercises for exploring and interacting with a Kubernetes cluster.

- [Lab 4: Setting up a Cluster Using Kubeadm](d0-container-k8s-fundamental/4-setup-cluster-using-kubeadm/README.md)
  - Guide for setting up a Kubernetes cluster using `kubeadm`.

- [Lab 5: Create GKE Cluster](d0-container-k8s-fundamental/5-create-gke-cluster/README.md)
  - Guide for creating and managing a Google Kubernetes Engine (GKE) cluster.

---

### Domain 1: Application Design and Build
- [Lab 1.1: Running and Managing Pods](d1-app-design-build/1_running_and_managing_pods/README.md)
  - Exercises on pod creation, management, and multi-container patterns.

- [Lab 1.2.2a: Ambassador Pattern](d1-app-design-build/1_running_and_managing_pods/2_multi_containers_pods/2a-ambassador-pattern/README.md)
  - Learn the Ambassador pattern for multi-container applications.

- [Lab 1.2.2b: Sidecar Pattern](d1-app-design-build/1_running_and_managing_pods/2_multi_containers_pods/2b-sidecar-pattern/README.md)
  - Learn the Sidecar pattern for multi-container applications.

---

### Domain 2: Application Deployment
- [Lab 2.1: Implementing Deployment Strategies](d2-app-deployment/1_implement_deployment_strategies/README.md)
  - Exploring blue-green, canary, and rolling deployment strategies.

- [Lab 2.2: Using Helm](d2-app-deployment/2_helm)
  - [Lab 2.2.1: Installing Helm and Deploying MySQL](d2-app-deployment/2_helm/1_install_hem_and_deploy_mysql_with_helm/README.md)
  - [Lab 2.2.2: Developing a Helm Chart with Dependencies](d2-app-deployment/2_helm/3_develop_chart_with_dependancies/README.md)
  - [Lab 2.2.3: Developing a Helm Chart from Scratch](d2-app-deployment/2_helm/2_develop_chart_from_scratch/README.md)
  - [Lab 2.2.4: Working with Helm Template](d2-app-deployment/2_helm/4_working_with_helm_template/README.md)
    - [Lab 2.2.4.1: if-else with eq](d2-app-deployment/2_helm/4_working_with_helm_template/3_if_else_eq/README.md)
    - [Lab 2.2.4.2: Built-in Helm Objects](d2-app-deployment/2_helm/4_working_with_helm_template/1_helm_built_in-objects/README.md)
    - [Lab 2.2.4.3: Helm Variables](d2-app-deployment/2_helm/4_working_with_helm_template/8_Variables/README.md)
    - [Lab 2.2.4.4: if-else with OR](d2-app-deployment/2_helm/4_working_with_helm_template/5_if_else_OR/README.md)
    - [Lab 2.2.4.5: Range with Dictionary](d2-app-deployment/2_helm/4_working_with_helm_template/10_range_dictionary/README.md)
    - [Lab 2.2.4.6: Helm Basics](d2-app-deployment/2_helm/4_working_with_helm_template/2_helm_basics/README.md)
    - [Lab 2.2.4.7: Range with List](d2-app-deployment/2_helm/4_working_with_helm_template/9_range_list/README.md)
    - [Lab 2.2.4.8: Call Template in Template](d2-app-deployment/2_helm/4_working_with_helm_template/13_call_template_in_template/README.md)
    - [Lab 2.2.4.9: if-else with AND](d2-app-deployment/2_helm/4_working_with_helm_template/4_if_else_AND/README.md)
    - [Lab 2.2.4.10: Named Templates](d2-app-deployment/2_helm/4_working_with_helm_template/11_named_templates/README.md)
    - [Lab 2.2.4.11: Printf Function](d2-app-deployment/2_helm/4_working_with_helm_template/12_Printf_Function/README.md)
    - [Lab 2.2.4.12: if-else with NOT](d2-app-deployment/2_helm/4_working_with_helm_template/6_if_else_NOT/README.md)
    - [Lab 2.2.4.13: with](d2-app-deployment/2_helm/4_working_with_helm_template/7_with/README.md)
  
  - [Lab 2.2.5: Creating and Packaging a Helm Chart](d2-app-deployment/2_helm/5_create_and_package_chart/README.md)

- [Lab 2.3: Using Kustomize](d2-app-deployment/3_kustomize)
  - [Lab 2.3.1: Getting Started with Kustomize](d2-app-deployment/3_kustomize/1_getting_started_with_todo_app/README.md)
  - [Lab 2.3.2: Kustomize CLI](d2-app-deployment/3_kustomize/2_cli/README.md)
  - [Lab 2.3.3: Using Kustomize to create an Overlay](d2-app-deployment/3_kustomize/3_using_kustomize_to_create_overlays/README.md)
  - [Lab 2.3.4: Setting Namespaces in an Overlay](d2-app-deployment/3_kustomize/4_setting_namespaces_in_an_overlay/README.md)
  - [Lab 2.3.5: Applying Labels to Objects](d2-app-deployment/3_kustomize/5_applying_labels_to_objects/README.md)
  - [Lab 2.3.6: Generating Application Configuration Data](d2-app-deployment/3_kustomize/6_generating_app_config_data/README.md)
  - [Lab 2.3.7: Workload Update on Configuration Changes](d2-app-deployment/3_kustomize/7_workload_update_on_config_change/README.md)

---

### Domain 3: Application Environment, Storage, Configuration and Security
- [Lab 3.1: Custom Resource Definition](d3-app-environment_configuration_and_security/1_discovering_and_using_crd/README.md)
  - Discovering and using CRD

- [Lab 3.2: Application Security with RBAC](d3-app-environment_configuration_and_security/2_rbac/README.md)
  - Learn about Role-Based Access Control (RBAC) for securing Kubernetes resources.

- [Lab 3.3: Resource management and quotas](d3-app-environment_configuration_and_security/3_resource_request_limit_quota/README.md)
  - Learn about resource request, limit and quotas.

- [Lab 3.4: Configure and manage Kubernetes storage](d3-app-environment_configuration_and_security/4_configuring_managing_storage)
  - [Lab 3.4.1: Static Provisioning](d3-app-environment_configuration_and_security/4_configuring_managing_storage/1_static_provisioning_pv/README.md)
  - [Lab 3.4.2: Dynamic Provisioning](d3-app-environment_configuration_and_security/4_configuring_managing_storage/2_dynamic_provisioning/README.md)

- [Lab 3.5: Configmaps and Secrets](d3-app-environment_configuration_and_security/5_configuration_as_data_environment_variables_secrets_and_configmaps)
  - [Lab 3.5.1: Environment Variables](d3-app-environment_configuration_and_security/5_configuration_as_data_environment_variables_secrets_and_configmaps/1_environment_variables/README.md)
  - [Lab 3.5.2: Secrets](d3-app-environment_configuration_and_security/5_configuration_as_data_environment_variables_secrets_and_configmaps/2_secrets/README.md)
  - [Lab 3.5.3: Docker Registry Secret](d3-app-environment_configuration_and_security/5_configuration_as_data_environment_variables_secrets_and_configmaps/3_docker_registry_secret/README.md)
  - [Lab 3.5.4: ConfigMaps](d3-app-environment_configuration_and_security/5_configuration_as_data_environment_variables_secrets_and_configmaps/4_configMap/README.md)

- [Lab 3.6: securityContext](d3-app-environment_configuration_and_security/6_securityContext/README.md)
  - Learn about securityContext for Pod and Container
---

### Domain 4: Services and Networking


---

### Domain 5: Application Observability and Maintenance


---

## Requirements

- Docker
- Kubernetes (Minikube, kubeadm, or GKE)
- Helm
- Kustomize
- Python 3.x (for some exercises)

---

## Getting Started

To begin, clone this repository and follow the instructions in the relevant subdirectories for each exercise. Each directory contains a `README.md` with specific setup and usage instructions.

```sh
git clone https://github.com/yourusername/ckad-labs.git
```

---

## License

This repository is licensed under the MIT License. See the `LICENSE` file for details.
