# Installation and Deployment

## Overview

This chapter describes how to install and deploy the Rubik component, using openEUler 24.03 LTS SP1 as an example.

## Software and Hardware Requirements

### Hardware

- Architecture: x86 or AArch64
- Drive: 1 GB or more
- Memory: 100 MB or more

### Software

- OS: openEuler 24.03_LTS_SP1
- Kernel: openEuler 24.03_LTS_SP1 kernel

### Environment Preparation

- Install the openEuler OS.
- Install and deploy Kubernetes.
- Install the Docker or containerd container engine.

## Installing Rubik

Rubik is deployed on each Kubernetes node as a DaemonSet. Therefore, you need to perform the following steps to install the Rubik RPM package on each node.

1. The Rubik component is available in the EPOL repository. Configure the Yum repositories openEuler 24.03-LTS-SP1 and openEuler 24.03-LTS-SP1:EPOL.

    ```ini
    # openEuler 24.03-LTS-SP1 official repository
   name=openEuler24.03-LTS-SP1
   baseurl=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/ 
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/RPM-GPG-KEY-openEuler
    ```

    ```ini
    # openEuler 24.03-LTS-SP1:EPOL official repository
   name=openEuler24.03-LTS-SP1-Epol
   baseurl=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/EPOL/$basearch/
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/RPM-GPG-KEY-openEuler
    ```

2. Install Rubik with **root** permissions.

    ```shell
    sudo yum install -y rubik
    ```

> ![](./figures/icon-note.gif)**Note**:
>
> Files related to Rubik are installed in the **/var/lib/rubik** directory.

## Deploying Rubik

Rubik runs as a container in a Kubernetes cluster in hybrid deployment scenarios. It is used to isolate and restrict resources for services with different priorities to prevent offline services from interfering with online services, improving the overall resource utilization and ensuring the quality of online services. Currently, Rubik supports isolation and restriction of CPU and memory resources, and must be used together with the openEuler 24.03-LTS-SP1 kernel. To enable or disable the memory priority feature (that is, memory tiering for services with different priorities), you need to set the value in the **/proc/sys/vm/memcg_qos_enable** file. The value can be **0** or **1**. The default value **0** indicates that the feature is disabled, and the value **1** indicates that the feature is enabled.

```bash
sudo echo 1 > /proc/sys/vm/memcg_qos_enable
```

### Deploying the Rubik DaemonSet

1. Build the Rubik image: Use the **/var/lib/rubik/build_rubik_image.sh** script to automatically build the Rubik image or directly use Docker to build it. Since Rubik is deployed as a DaemonSet, the Rubik image must be available on every node. You can build the image on one node and then use the save/load functionality of Docker to load the image onto all nodes in the Kubernetes cluster. Alternatively, you can build the Rubik image on each node individually. For Docker, the build command is:

    ```sh
    docker build -f /var/lib/rubik/Dockerfile -t rubik:2.0.1-2 .
    ```

2. On the Kubernetes master node, update the Rubik image name in the **/var/lib/rubik/rubik-daemonset.yaml** file to match the image name created in the previous step.

    ```yaml
    ...
    containers:
    - name: rubik-agent
    image: rubik_image_name_and_tag  # Ensure this matches the Rubik image name built earlier.
    imagePullPolicy: IfNotPresent
    ...
    ```

3. On the Kubernetes master node, run the **kubectl** command to deploy the Rubik DaemonSet so that Rubik will be automatically deployed on all Kubernetes nodes.

    ```sh
    kubectl apply -f /var/lib/rubik/rubik-daemonset.yaml
    ```

4. Run the **kubectl get pods -A** command to check whether Rubik has been deployed on each node in the cluster. (The number of rubik-agents is the same as the number of nodes and all rubik-agents are in the Running status.)

```sh
$ kubectl get pods -A
NAMESPACE     NAME                                            READY   STATUS    RESTARTS   AGE
...
kube-system   rubik-agent-76ft6                               1/1     Running   0          4s
...
```

## Common Configuration Description

The Rubik deployed using the preceding method is started with the default configurations. You can modify the Rubik configurations as required by modifying the **config.json** section in the **rubik-daemonset.yaml** file and then redeploy the Rubik DaemonSet. The following describes some common configurations. For other configurations, see [Rubik Configuration Description](./configuration.md).

### Absolute Pod Preemption

If absolute pod preemption is enabled, you only need to specify the priority using annotations in the YAML file when deploying the service pods. After being deployed successfully, Rubik automatically detects the creation and update of the pods on the current node, and sets the pod priorities based on the configured priorities. For pods that are already started or whose annotations are modified, Rubik automatically updates the pod priority configurations.

```yaml
...
  "agent": {
    "enabledFeatures": [
      "preemption"
    ]
  },
  "preemption": {
    "resource": [
      "cpu",
      "memory"
    ]
  }
...
```

> [!NOTE]Note
>
> Priority configurations support only pods switching from online to offline.

## Configuring Rubik for Online and Offline Services

After Rubik is successfully deployed, you can modify the YAML file of a service to specify the service type based on the following configuration example. Then Rubik can configure the priority of the service after it is deployed to isolate resources.

The following is an example of deploying an online Nginx service:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: qosexample
  annotations:
    volcano.sh/preemptable: "false"   # If volcano.sh/preemptable is set to true, the service is an offline service. If it is set to false, the service is an online service. The default value is false.
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "1"
      requests:
        memory: "200Mi"
        cpu: "1"
```
