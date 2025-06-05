# 安装与部署

## 概述

本章节主要介绍 rubik 组件的安装以及部署方式，以openEuler 24.03-LTS-SP1版本为例进行部署。

## 软硬件要求

### 硬件要求

* 当前仅支持 x86、aarch64 架构。
* rubik 磁盘使用需求：配额 1GB 及以上。
* rubik 内存使用需求：配额 100MB 及以上。

### 软件要求

* 操作系统：openEuler 24.03-LTS-SP1。
* 内核：openEuler 24.03-LTS-SP1 版本内核。

### 环境准备

* 安装 openEuler 系统。
* 安装并部署 kubernetes。
* 安装 docker 或 containerd 容器引擎。

## 安装 rubik

rubik 以`DaemonSet`形式部署在 k8s 的每一个节点上，故需要在每一个节点上使用以下步骤安装 rubik rpm 包。

1. 配置 yum 源：rubik组件位于openEuler EPOL源中，以openEuler 24.03-LTS-SP1版本为例，参考如下：

   ```sh
   # openEuler 24.03-LTS-SP1 官方发布源
   name=openEuler24.03-LTS-SP1
   baseurl=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/ 
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/RPM-GPG-KEY-openEuler
   ```

   ```sh
   # openEuler 24.03-LTS-SP1:Epol 官方发布源
   name=openEuler24.03-LTS-SP1-Epol
   baseurl=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/EPOL/$basearch/
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/RPM-GPG-KEY-openEuler
   ```

2. 使用 root 权限安装 rubik：

   ```shell
   sudo yum install -y rubik
   ```

> [!NOTE]说明
>
> rubik 工具相关文件会安装在/var/lib/rubik 目录下。

## 部署 rubik

rubik 以容器形式运行在混合部署场景下的 k8s 集群中，用于对不同优先级业务进行资源隔离和限制，避免离线业务对在线业务产生干扰，在提高资源总体利用率的同时保障在线业务的服务质量。当前 rubik 支持对 CPU、内存资源进行隔离和限制等特性，需配合 openEuler 24.03-LTS-SP1 版本的内核使用。若用户想要开启内存优先级特性（即针对不同优先级业务实现内存资源的分级），需要通过设置/proc/sys/vm/memcg_qos_enable 开关，有效值为 0 和 1，其中 0 为默认值表示关闭特性，1 表示开启特性。

```bash
sudo echo 1 > /proc/sys/vm/memcg_qos_enable
```

### 部署 rubik daemonset

1. 构建rubik镜像：使用`/var/lib/rubik/build_rubik_image.sh`脚本自动构建或者直接使用 docker容器引擎构建 rubik 镜像。由于 rubik 以 daemonSet 形式部署，故每一个节点都需要 rubik 镜像。用户可以在一个节点构建镜像后使用 docker save/load 功能将 rubik 镜像 load 到 k8s 的每一个节点，也可以在各节点上都构建一遍 rubik 镜像。以 docker 为例，其构建命令如下：

    ```sh
    docker build -f /var/lib/rubik/Dockerfile -t rubik:2.0.1-2 .
    ```

2. 在 k8s master 节点，修改`/var/lib/rubik/rubik-daemonset.yaml`文件中的 rubik 镜像名，与上一步构建出来的镜像名保持一致。

    ```yaml
    ...
    containers:
    - name: rubik-agent
      image: rubik_image_name_and_tag  # 此处镜像名需与上一步构建的 rubik 镜像名一致
      imagePullPolicy: IfNotPresent
    ...
    ```

3. 在 k8s master 节点，使用 kubectl 命令部署 rubik daemonset，rubik 会自动被部署在 k8s 的所有节点：

    ```sh
    kubectl apply -f /var/lib/rubik/rubik-daemonset.yaml
    ```

4. 使用`kubectl get pods -A`命令查看 rubik 是否已部署到集群每一个节点上（rubik-agent 数量与节点数量相同且均为 Running 状态）：

    ```sh
    [root@localhost rubik]# kubectl get pods -A | grep rubik
    NAMESPACE     NAME                                            READY   STATUS    RESTARTS   AGE
    ...
    kube-system   rubik-agent-76ft6                               1/1     Running   0          4s
    ...
    ```

## 常用配置说明

通过以上方式部署的 rubik 将以默认配置启动，用户可以根据实际需要修改 rubik 配置，可通过修改 rubik-daemonset.yaml 文件中的 config.json 段落内容后重新部署 rubik daemonset 实现。以下介绍几个常见配置，其他配置详见 [配置文档](./configuration.md)。

### Pod 绝对抢占特性

用户在开启了 rubik 绝对抢占特性后，仅需在部署业务 Pod 时在 yaml 中通过 annotation 指定其优先级。部署后 rubik 会自动感知当前节点 Pod 的创建与更新，并根据用户配置的优先级设置 Pod 优先级。对于已经启动的或者更改注解的Pod， rubik 会自动更正Pod的优先级配置。

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

> [!NOTE]说明
>
> 优先级配置仅支持Pod由在线切换为离线，不允许由离线切换为在线。

## 在/离线业务配置示例

rubik 部署成功后，用户在部署实际业务时，可以根据以下配置示例对业务 yaml 文件进行修改，指定业务的在离线类型，rubik 即可在业务部署后对其优先级进行配置，从而达到资源隔离的目的。

以下为部署一个 nginx 在线业务的示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: qosexample
  annotations:
    volcano.sh/preemptable: "false"   # volcano.sh/preemptable 为 true 代表业务为离线业务，false 代表业务为在线业务，默认为 false
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
