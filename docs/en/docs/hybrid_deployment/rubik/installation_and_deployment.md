# Installation and Deployment

## Overview

This chapter describes how to install and deploy the Rubik component.

## Software and Hardware Requirements

### Hardware

* Architecture: x86 or AArch64
* Drive: 1 GB or more
* Memory: 100 MB or more

### Software

* OS: openEuler 22.03-LTS
* Kernel: openEuler 22.03-LTS kernel

### Environment Preparation

* Install the openEuler OS. For details, see the openEuler _Installation Guide_.
* Install and deploy Kubernetes. For details, see the _Kubernetes Cluster Deployment Guide_.
* Install the Docker or iSulad container engine. If the iSulad container engine is used, you need to install the isula-build container image building tool.

## Installing Rubik

Rubik is deployed on each Kubernetes node as a DaemonSet. Therefore, you need to perform the following steps to install the Rubik RPM package on each node.

1. Configure the Yum repositories openEuler 22.03-LTS and openEuler 22.03-LTS:EPOL (the Rubik component is available only in the EPOL repository).

   ```conf
   # openEuler 22.03-LTS official repository
   name=openEuler22.03
   baseurl=https://repo.openeuler.org/openEuler-22.03-LTS/everything/$basearch/ 
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-22.03-LTS/everything/$basearch/RPM-GPG-KEY-openEuler
   ```

   ```conf
   # openEuler 22.03-LTS:EPOL official repository
   name=Epol
   baseurl=https://repo.openeuler.org/openEuler-22.03-LTS/EPOL/$basearch/
   enabled=1
   gpgcheck=0
   ```

2. Install Rubik with **root** permissions.

   ```shell
   sudo yum install -y rubik
   ```

> [!NOTE]NOTE   :
>
> Files related to Rubik are installed in the **/var/lib/rubik** directory.

## Deploying Rubik

Rubik runs as a container in a Kubernetes cluster in hybrid deployment scenarios. It is used to isolate and restrict resources for services with different priorities to prevent offline services from interfering with online services, improving the overall resource utilization and ensuring the quality of online services. Currently, Rubik supports isolation and restriction of CPU and memory resources, and must be used together with the openEuler 22.03-LTS kernel. To enable or disable the memory priority feature (that is, memory tiering for services with different priorities), you need to set the value in the **/proc/sys/vm/memcg_qos_enable** file. The value can be **0** or **1**. The default value **0** indicates that the feature is disabled, and the value **1** indicates that the feature is enabled.

```bash
sudo echo 1 > /proc/sys/vm/memcg_qos_enable
```

### Deploying Rubik DaemonSet

1. Use the Docker or isula-build engine to build Rubik images. Because Rubik is deployed as a DaemonSet, each node requires a Rubik image. After building an image on a node, use the **docker save** and **docker load** commands to load the Rubik image to each node of Kubernetes. Alternatively, build a Rubik image on each node. The following uses isula-build as an example. The command is as follows:

    ```sh
    isula-build ctr-img build -f /var/lib/rubik/Dockerfile --tag rubik:0.1.0 .
    ```

2. On the Kubernetes master node, change the Rubik image name in the **/var/lib/rubik/rubik-daemonset.yaml** file to the name of the image built in the previous step.

    ```yaml
    ...
    containers:
    - name: rubik-agent
    image: rubik:0.1.0  # The image name must be the same as the Rubik image name built in the previous step.
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

The Rubik deployed using the preceding method is started with the default configurations. You can modify the Rubik configurations as required by modifying the **config.json** section in the **rubik-daemonset.yaml** file and then redeploy the Rubik DaemonSet.

This section describes common configurations in **config.json**.

### Configuration Item Description

```yaml
# The configuration items are in the config.json section of the rubik-daemonset.yaml file.
{
    "autoConfig": true,
    "autoCheck": false,
    "logDriver": "stdio",
    "logDir": "/var/log/rubik",
    "logSize": 1024,
    "logLevel": "info",
    "cgroupRoot": "/sys/fs/cgroup"
}
```

| Item    | Value Type| Value Range      | Description                                                    |
| ---------- | ---------- | ------------------ | ------------------------------------------------------------ |
| autoConfig | Boolean      | **true** or **false**       | **true**: enables automatic pod awareness.<br> **false**: disables automatic pod awareness.|
| autoCheck  | Boolean      | **true** or **false**       | **true**: enables pod priority check.<br>**false**: disables pod priority check.|
| logDriver  | String    | **stdio** or **file**       | **stdio**: prints logs to the standard output. The scheduling platform collects and dumps logs.<br>**file**: prints files to the log directory specified by **logDir**.|
| logDir     | String    | Absolute path          | Directory for storing logs.                                    |
| logSize    | Integer        | \[10,1048576]     | Total size of logs, in MB. If the total size of logs reaches the upper limit, the earliest logs will be discarded.|
| logLevel   | String    | **error**, **info**, or **debug**| Log level.                                              |
| cgroupRoot | String    | Absolute path          | cgroup mount point.                                        |

### Automatic Configuration of Pod Priorities

If **autoConfig** is set to **true** in **config.json** to enable automatic pod awareness, you only need to specify the priority using annotations in the YAML file when deploying the service pods. After being deployed successfully, Rubik automatically detects the creation and update of the pods on the current node, and sets the pod priorities based on the configured priorities.

### Pod Priority Configuration Depending on kubelet

Automatic pod priority configuration depends on the pod creation event notifications from the API server, which have a certain delay. The pod priority cannot be configured before the process is started. As a result, the service performance may fluctuate. To avoid this problem, you can disable the automatic priority configuration option and modify the kubelet source code, so that pod priorities can be configured using Rubik HTTP APIs after the cgroup of each container is created and before each container process is started. For details about how to use the HTTP APIs, see [HTTP APIs](./http_apis.md).

### Automatic Verification of Pod Priorities

Rubik supports consistency check on the pod QoS priority configurations of the current node during startup. It checks whether the configuration in the Kubernetes cluster is consistent with the pod priority configuration of Rubik. This function is disabled by default. You can enable or disable it using the **autoCheck** option. If this function is enabled, Rubik automatically verifies and corrects the pod priority configuration of the current node when it is started or restarted.

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

## Restrictions

* The maximum number of concurrent HTTP requests that Rubik can receive is 1,000 QPS. If the number of concurrent HTTP requests exceeds the upper limit, an error is reported.

* The maximum number of pods in a single request received by Rubik is 100. If the number of pods exceeds the upper limit, an error is reported.

* Only one set of Rubik instances can be deployed on each Kubernetes node. Multiple sets of Rubik instances may conflict with each other.

* Rubik does not provide port access and can communicate only through sockets.

* Rubik accepts only valid HTTP request paths and network protocols: `<http://localhost/>` (POST), `<http://localhost/ping>` (GET), and `<http://localhost/version>` (GET). For details about the functions of HTTP requests, see HTTP APIs(./http-apis.md).

* Rubik drive requirement: 1 GB or more.

* Rubik memory requirement: 100 MB or more.

* Services cannot be switched from a low priority (offline services) to a high priority (online services). For example, if service A is set to an offline service and then to an online service, Rubik reports an error.

* When directories are mounted to a Rubik container, the minimum permission on the Rubik local socket directory **/run/Rubik** is **700** on the service side.

* When the Rubik service is available, the timeout interval of a single request is 120s. If the Rubik process enters the T (stopped or being traced) or D (uninterruptible sleep) state, the service becomes unavailable. In this case, the Rubik service does not respond to any request. To avoid this problem, set the timeout interval on the client to avoid infinite waiting.

* If hybrid deployment is used, the original CPU share function of cgroup has the following restrictions:

  If both online and offline tasks are running on the CPU, the CPU share configuration of offline tasks does not take effect.

  If the current CPU has only online or offline tasks, the CPU share configuration takes effect.
