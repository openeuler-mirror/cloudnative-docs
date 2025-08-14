# Installation and Deployment

This chapter describes how to install and deploy the KubeOS tool.

## Software and Hardware Requirements

### Hardware Requirements

- Currently, only the x86 and AArch64 architectures are supported.

### Software Requirements

- OS: openEuler 24.09

### Environment Preparation

- Install the openEuler system. For details, see the *openEuler Installation Guide*.
- Install qemu-img, bc, Parted, tar, Yum, Docker, and dosfstools.

## KubeOS Installation

To install KubeOS, perform the following steps:

1. Configure the Yum sources openEuler 24.09 and openEuler 24.09:EPOL:

    ```conf
    [openEuler24.09] # openEuler 24.09 official source
    name=openEuler24.09
    baseurl=http://repo.openeuler.org/openEuler-24.09/everything/$basearch/ 
    enabled=1
    gpgcheck=1
    gpgkey=http://repo.openeuler.org/openEuler-24.09/everything/$basearch/RPM-GPG-KEY-openEuler
    ```

2. Install KubeOS as the **root** user.

    ```shell
    # yum install KubeOS KubeOS-scripts -y
    ```

> [!NOTE]NOTE   :
>
> KubeOS is installed in the **/opt/kubeOS** directory, including the os-operator, os-proxy, os-agent binary files, KubeOS image build tools, and corresponding configuration files.

## KubeOS Deployment

After KubeOS is installed, you need to configure and deploy it. This section describes how to configure and deploy KubeOS.

### Building the os-operator and os-proxy Images

#### Environment Preparation

Before using Docker to create a container image, ensure that Docker has been installed and configured.

#### Procedure

1. Go to the working directory.

    ```shell
    cd /opt/kubeOS
    ```

2. Specify the image repository, name, and version for os-proxy.

    ```shell
    export IMG_PROXY=your_imageRepository/os-proxy_imageName:version
    ```

3. Specify the image repository, name, and version for os-operator.

    ```shell
    export IMG_OPERATOR=your_imageRepository/os-operator_imageName:version
    ```

4. Compile a Dockerfile to build an image. Pay attention to the following points when compiling a Dockerfile:

    - The os-operator and os-proxy images must be built based on the base image. Ensure that the base image is safe.
    - Copy the os-operator and os-proxy binary files to the corresponding images.
    - Ensure that the owner and owner group of the os-proxy binary file in the os-proxy image are **root**, and the file permission is **500**.
    - Ensure that the owner and owner group of the os-operator binary file in the os-operator image are the user who runs the os-operator process in the container, and the file permission is **500**.
    - The locations of the os-operator and os-proxy binary files in the image and the commands run during container startup must correspond to the parameters specified in the YAML file used for deployment.

    An example Dockerfile is as follows:

    ```text
    FROM your_baseimage
    COPY ./bin/proxy /proxy
    ENTRYPOINT ["/proxy"]
    ```

    ```text
    FROM your_baseimage
    COPY --chown=6552:6552 ./bin/operator /operator
    ENTRYPOINT ["/operator"]
    ```

    Alternatively, you can use multi-stage builds in the Dockerfile.

5. Build the images (the os-operator and os-proxy images) to be included in the containers OS image.

    ```shell
    # Specify the Dockerfile path of os-proxy.
    export DOCKERFILE_PROXY=your_dockerfile_proxy
    # Specify the Dockerfile path of os-operator.
    export DOCKERFILE_OPERATOR=your_dockerfile_operator
    # Build images.
    docker build -t ${IMG_OPERATOR} -f ${DOCKERFILE_OPERATOR} .
    docker build -t ${IMG_PROXY} -f ${DOCKERFILE_PROXY} .
    ```

6. Push the images to the image repository.

    ```shell
    docker push ${IMG_OPERATOR}
    docker push ${IMG_PROXY}
    ```

### Creating a KubeOS VM Image

#### Precautions

- The VM image is used as an example. For details about how to create a physical machine image, see **KubeOS Image Creation**.
- The root permission is required for creating a KubeOS image.
- The RPM sources of the kbimg are the **everything** and **EPOL** repositories of openEuler of a specific version. In the Repo file provided during image creation, you are advised to configure the **everything** and **EPOL** repositories of a specific openEuler version for the Yum source.
- By default, the KubeOS VM image built using the default RPM list is stored in the same path as the kbimg tool. This partition must have at least 25 GiB free drive space.
- When creating a KubeOS image, you cannot customize the file system to be mounted.

#### Procedure

Use the **kbimg.sh** script to create a KubeOS VM image. For details about the commands, see **KubeOS Image Creation**.

To create a KubeOS VM image, perform the following steps:

1. Go to the working directory.

    ```shell
    cd /opt/kubeOS/scripts
    ```

2. Run `kbming.sh` to create a KubeOS image. The following is a command example:

    ```shell
    bash kbimg.sh create vm-image -p xxx.repo -v v1 -b ../bin/os-agent -e '''$1$xyz$RdLyKTL32WEvK3lg8CXID0'''
    ```

    In the command, **xx.repo** indicates the actual Yum source file used for creating the image. You are advised to configure both the **everything** and **EPOL** repositories as Yum sources.

    After the KubeOS image is created, the following files are generated in the **/opt/kubeOS/scripts** directory:

    - **system.img**: system image in raw format. The default size is 20 GB. The size of the root file system partition is less than 2,560 MiB, and the size of the Persist partition is less than 14 GiB.
    - **system.qcow2**: system image in QCOW2 format.
    - **update.img**: partition image of the root file system that is used for upgrade.

    The created KubeOS VM image can be used only in a VM of the x86 or AArch64 architecture. KubeOS does not support legacy boot in an x86 VM

### Deploying CRD, os-operator, and os-proxy

#### Precautions

- The Kubernetes cluster must be deployed first. For details, see the *openEuler 24.09 Kubernetes Cluster Deployment Guide*.

- The OS of the worker nodes to be upgraded in the cluster must be the KubeOS built using the method described in the previous section. If it is not, use **system.qcow2** to deploy the VM again. For details about how to deploy a VM, see the *openEuler 24.09 Virtualization User Guide*. Currently, KubeOS does not support the master nodes. Use openEuler 24.09 to deploy the upgrade on the master nodes.
- The YAML files for deploying CustomResourceDefinition (CRD), os-operator, os-proxy, and role-based access control (RBAC) of the OS need to be compiled.
- The os-operator and os-proxy components are deployed in the Kubernetes cluster. os-operator must be deployed as a Deployment, and os-proxy as a DaemonSet.
- Kubernetes security mechanisms, such as the RBAC, pod service account, and security policies, must be deployed.

#### Procedure

1. Prepare YAML files used for deploying CRD, RBAC, os-operator, and os-proxy of the OS. For details, see [YAML examples](https://gitee.com/openeuler/KubeOS/tree/master/docs/example/config). The following uses **crd.yaml**, **rbac.yaml**, and **manager.yaml** as examples.

2. Deploy CRD, RBAC, os-operator, and os-proxy. Assume that the **crd.yaml**, **rbac.yaml**, and **manager.yaml** files are stored in the **config/crd**, **config/rbac**, and **config/manager** directories, respectively. Run the following commands:

    ```shell
    kubectl apply -f config/crd
    kubectl apply -f config/rbac 
    kubectl apply -f config/manager
    ```

3. After the deployment is complete, run the following command to check whether each component is started properly. If **STATUS** of all components is **Running**, the components are started properly.

    ```shell
    kubectl get pods -A
    ```
