# 安装与部署

## 概述

本章节主要介绍rubik组件的安装以及部署方式。

## 软硬件要求

### 硬件要求

* 当前仅支持 x86、aarch64架构。
* rubik磁盘使用需求：配额1GB及以上。
* rubik内存使用需求：配额100MB及以上。

### 软件要求

* 操作系统：openEuler 22.03-LTS
* 内核：openEuler 22.03-LTS版本内核

### 环境准备

* 安装 openEuler 系统，安装方法参考《[安装指南](../Installation/installation.md)》。
* 安装并部署 kubernetes，安装及部署方法参考《Kubernetes 集群部署指南》。
* 安装docker或isulad容器引擎，若采用isulad容器引擎，需同时安装isula-build容器镜像构建工具。

## 安装rubik

rubik以k8s daemonSet形式部署在k8s的每一个节点上，故需要在每一个节点上使用以下步骤安装rubik rpm包。

1. 配置 yum 源：openEuler 22.03-LTS 和 openEuler 22.03-LTS:EPOL（rubik组件当前仅在EPOL源中），参考如下：

   ```conf
   # openEuler 22.03-LTS 官方发布源
   name=openEuler22.03
   baseurl=https://repo.openeuler.org/openEuler-22.03-LTS/everything/$basearch/ 
   enabled=1
   gpgcheck=1
   gpgkey=https://repo.openeuler.org/openEuler-22.03-LTS/everything/$basearch/RPM-GPG-KEY-openEuler
   ```

   ```conf
   # openEuler 22.03-LTS:Epol 官方发布源
   name=Epol
   baseurl=https://repo.openeuler.org/openEuler-22.03-LTS/EPOL/$basearch/
   enabled=1
   gpgcheck=0
   ```

2. 使用root权限安装rubik：

   ```bash
   sudo yum install -y rubik
   ```

> ![](./figures/icon-note.gif)**说明**：
>
> rubik工具相关文件会安装在/var/lib/rubik目录下

## 部署rubik

rubik以容器形式运行在混合部署场景下的k8s集群中，用于对不同优先级业务进行资源隔离和限制，避免离线业务对在线业务产生干扰，在提高资源总体利用率的同时保障在线业务的服务质量。当前rubik支持对CPU、内存资源进行隔离和限制，需配合openEuler 22.03-LTS版本的内核使用。若用户想要开启内存优先级特性（即针对不同优先级业务实现内存资源的分级），需要通过设置/proc/sys/vm/memcg_qos_enable开关，有效值为0和1，其中0为缺省值表示关闭特性，1表示开启特性。

```bash
sudo echo 1 > /proc/sys/vm/memcg_qos_enable
```

### 部署rubik daemonset

1. 使用docker或isula-build容器引擎构建rubik镜像，由于rubik以daemonSet形式部署，故每一个节点都需要rubik镜像。用户可以在一个节点构建镜像后使用docker save/load功能将rubik镜像load到k8s的每一个节点，也可以在各节点上都构建一遍rubik镜像。以isula-build为例，参考命令如下：

    ```bash
    isula-build ctr-img build -f /var/lib/rubik/Dockerfile --tag rubik:0.1.0 .
    ```

2. 在k8s master节点，修改`/var/lib/rubik/rubik-daemonset.yaml`文件中的rubik镜像名，与上一步构建出来的镜像名保持一致。

    ```yaml
    ...
    containers:
    - name: rubik-agent
      image: rubik:0.1.0  # 此处镜像名需与上一步构建的rubik镜像名一致
      imagePullPolicy: IfNotPresent
    ...
    ```

3. 在k8s master节点，使用kubectl命令部署rubik daemonset，rubik会自动被部署在k8s的所有节点：

    ```bash
    kubectl apply -f /var/lib/rubik/rubik-daemonset.yaml
    ```

4. 使用`kubectl get pods -A`命令查看rubik是否已部署到集群每一个节点上（rubik-agent数量与节点数量相同且均为Running状态）

    ```bash
    [root@localhost rubik]# kubectl get pods -A
    NAMESPACE     NAME                                            READY   STATUS    RESTARTS   AGE
    ...
    kube-system   rubik-agent-76ft6                               1/1     Running   0          4s
    ...
    ```

## 常用配置说明

通过以上方式部署的rubik将以默认配置启动，用户可以根据实际需要修改rubik配置，可通过修改rubik-daemonset.yaml文件中的config.json段落内容后重新部署rubik daemonset实现。

本章介绍 config.json 的常用配置，以方便用户根据需要进行配置。

### 配置项说明

```yaml
# 该部分配置内容位于rubik-daemonset.yaml文件中的config.json段落
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

| 配置项     | 配置值类型 | 配置取值范围       | 配置含义                                                     |
| ---------- | ---------- | ------------------ | ------------------------------------------------------------ |
| autoConfig | bool       | true、false        | true：开启Pod自动感知功能。<br> false：关闭 Pod 自动感知功能。 |
| autoCheck  | bool       | true、false        | true：开启 Pod 优先级校验功能。 <br>false：关闭 Pod 优先级校验功能。 |
| logDriver  | string     | stdio、file        | stdio：直接向标准输出打印日志，日志收集和转储由调度平台完成。 <br>file：将文件打印到日志目录，路径由logDir指定。 |
| logDir     | string     | 绝对路径           | 指定日志存放的目录路径。                                     |
| logSize    | int        | [10，1048576]      | 指定日志存储总大小，单位 MB，若日志总量达到上限则最早的日志会被丢弃。 |
| logLevel   | string     | error、info、debug | 指定日志级别。                                               |
| cgroupRoot | string     | 绝对路径           | 指定 cgroup 挂载点。                                         |

### Pod优先级自动配置

若在rubik config中配置autoConfig为true开启了Pod自动感知配置功能，用户仅需在部署业务pod时在yaml中通过annotation指定其优先级，部署后rubik会自动感知当前节点pod的创建与更新，并根据用户配置的优先级设置pod优先级。

### 依赖于kubelet的Pod优先级配置

由于Pod优先级自动配置依赖于来自api-server pod创建事件的通知，具有一定的延迟性，无法在进程启动之前及时完成Pod优先级的配置，导致业务性能可能存在抖动。用户可以关闭优先级自动配置选项，通过修改kubelet源码，在容器cgroup创建后、容器进程启动前调用rubik http接口配置pod优先级，http接口具体使用方法详见[http接口文档](./http接口文档.md)

### 支持自动校对Pod优先级

rubik支持在启动时对当前节点Pod QoS优先级配置进行一致性校对，此处的一致性是指k8s集群中的配置和rubik对pod优先级的配置之间的一致性。该校对功能默认关闭，用户可以通过 autoCheck 选项控制是否开启。若开启该校对功能，启动或者重启 rubik 时，rubik会自动校验并更正当前节点pod优先级配置。

## 在离线业务配置示例

rubik部署成功后，用户在部署实际业务时，可以根据以下配置示例对业务yaml文件进行修改，指定业务的在离线类型，rubik即可在业务部署后对其优先级进行配置，从而达到资源隔离的目的。

以下为部署一个nginx在线业务的示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: qosexample
  annotations:
    volcano.sh/preemptable: "false"   # volcano.sh/preemptable为true代表业务为离线业务，false代表业务为在线业务，默认为false
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

## 约束限制

* rubik接受HTTP请求并发量上限1000QPS，并发量超过上限则报错。

* rubik接受的单个请求中pod上限为100个，pod数量越界则报错。

* 每个k8s节点只能部署一个rubik，多个rubik会冲突。

* rubik不提供端口访问，只能通过socket通信。

* rubik只接收合法http请求路径及网络协议：<http://localhost/（POST）、http://localhost/ping（GET）、http://localhost/version（GET）。各http请求的功能详见[http接口文档>](./http接口文档.md)。

* rubik磁盘使用需求：配额1GB及以上。

* rubik内存使用需求：配额100MB及以上。

* 禁止将业务从低优先级（离线业务）往高优先级（在线业务）切换。如业务A先被设置为离线业务，接着请求设置为在线业务，rubik报错。

* 容器挂载目录时，rubik本地套接字/run/rubik的目录权限需由业务侧保证最小权限700。

* rubik服务端可用时，单个请求超时时间为120s。如果rubik进程进入T（暂停状态或跟踪状态）、D状态（不可中断的睡眠状态），则服务端不可用，此时rubik服务不会响应任何请求。为了避免此情况的发生，请在客户端设置超时时间，避免无限等待。

* 使用混部后，原始的cgroup cpu share功能存在限制。具体表现为：

  若当前CPU中同时有在线任务和离线任务运行，则离线任务的CPU share配置无法生效。

  若当前CPU中只有在线任务或只有离线任务，CPU share能生效。
