# Common Issues and Solutions

## Issue 1: Kubernetes + Docker Deployment Failure

Reason: Kubernetes dropped support for Kubernetes + Docker cluster deployments starting from version 1.21.

Solution: Use cri-dockerd + Docker for cluster deployment, or consider alternatives like containerd or iSulad.

## Issue 2: Unable to Install Kubernetes RPM Packages via yum on openEuler

Reason: Installing Kubernetes-related RPM packages requires proper configuration of the EPOL repository in yum.

Solution: Follow the repository configuration guide provided in [this link](https://forum.openeuler.org/t/topic/768) to set up the EPOL repository in your environment.
