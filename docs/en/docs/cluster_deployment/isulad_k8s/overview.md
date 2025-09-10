# iSulad + Kubernetes Cluster Deployment Guide

This document outlines the process of deploying a Kubernetes cluster with kubeadm on the openEuler OS, configuring a Kubernetes + iSulad environment, and setting up gitlab-runner. It serves as a comprehensive guide for creating a native openEuler development environment cluster.

The guide addresses two primary scenarios:

**Scenario 1**: A complete walkthrough for establishing a native openEuler development CI/CD pipeline from scratch using gitlab-ci.
**Scenario 2**: Instructions for integrating an existing native openEuler development execution machine cluster into gitlab-ci.

For scenario 1, the following steps are required:

1. Set up the Kubernetes + iSulad environment.
2. Deploy GitLab.
3. Install and test gitlab-runner.

For scenario 2, where a gitlab-ci platform is already available, the process involves:

1. Configure the Kubernetes + iSulad environment.
2. Install and test gitlab-runner.

> [!NOTE] Note
>
> All operations described in this document must be executed with root privileges.
