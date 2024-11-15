# Lab: Getting Started with Kustomize

## Objectives

- Understand the purpose and functionality of the **Kustomize** CLI.
- Learn how to use the standalone Kustomize binary.
- Explore the Kustomize functionality built into **kubectl**.

## Requirements

- Install the **Kustomize standalone binary**. You can download it from [Kustomize releases](https://github.com/kubernetes-sigs/kustomize/releases).
- Ensure **kubectl** is installed. Instructions for installing kubectl can be found [here](https://kubectl.docs.kubernetes.io/installation/kubectl/).

## Steps

1. Familiarize yourself with the Kustomize CLI by exploring its help options:

    ```bash
    kustomize --help
    kustomize build --help
    kustomize create --help
    kustomize edit --help
    ```

2. Check the version of the standalone Kustomize binary:

    ```bash
    kustomize version
    ```

3. Explore the Kustomize options available in **kubectl**:

    ```bash
    kubectl kustomize --help
    kubectl apply --help | grep -C1 kustomize
    ```

4. Verify the version of Kustomize integrated into **kubectl** and compare it with the standalone version:

    ```bash
    kubectl version --short
    ```

> Exploring these commands will help you gain an overview of the features available in both the standalone binary and the kubectl-integrated version.

## Summary

This lab provided a hands-on introduction to the **Kustomize** CLI and its integration with **kubectl**. You should now have a basic understanding of how to access Kustomize functionality and check version information for both tools.
