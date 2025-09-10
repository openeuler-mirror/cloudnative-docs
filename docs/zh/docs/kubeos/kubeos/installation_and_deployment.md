# 安装与部署

本章介绍如何安装和部署容器 OS 升级工具。

## 软硬件要求

### 硬件要求

* 当前仅支持 x86和 AArch64 架构

### 软件要求

* 操作系统：openEuler 24.03-LTS-SP1

### 环境准备

* 安装 openEuler 系统，安装方法参考《[安装指南](https://docs.openeuler.openatom.cn/zh/docs/24.03_LTS_SP2/server/installation_upgrade/installation/installation_on_servers.html)》

* 安装 qemu-img，bc，parted，tar，yum，docker，dosfstools

## 安装容器OS升级工具

安装容器 OS 升级工具的操作步骤如下：

1. 配置 openEuler 24.03-LTS-SP1 yum 源：

   ```sh
   [openEuler24.03-LTS-SP1] # openEuler 24.03-LTS-SP1 官方发布源
   name=openEuler24.03-LTS-SP1
   baseurl=http://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/ 
   enabled=1
   gpgcheck=1
   gpgkey=http://repo.openeuler.org/openEuler-24.03-LTS-SP1/everything/$basearch/RPM-GPG-KEY-openEuler
   ```

2. 使用 root 帐户安装容器 OS 升级工具：

   ```shell
   yum install KubeOS KubeOS-scripts -y
   ```

> [!NOTE]说明
>
> 容器 OS 升级工具会安装在 /opt/kubeOS 目录下，包括os-operator，os-proxy，os-agent二进制，制作容器 OS 工具及相应配置文件 。

## 部署容器OS升级工具

容器OS升级工具安装完成后，需要对此进行配置部署，本章介绍如何配置和部署容器OS升级工具。

### 制作os-operator和os-proxy镜像

#### 环境准备

使用 Docker 制作容器镜像，请先确保 Docker 已经安装和配置完成。

#### 操作步骤

1. 进入工作目录。

   ```shell
   cd /opt/kubeOS
   ```

2. 指定 proxy 的镜像仓库、镜像名及版本。

   ```shell
   export IMG_PROXY=your_imageRepository/os-proxy_imageName:version
   ```

3. 指定 operator 的镜像仓库、镜像名及版本。

   ```shell
   export IMG_OPERATOR=your_imageRepository/os-operator_imageName:version
   ```

4. 请用户自行编写Dockerfile来构建镜像 ，Dockfile编写请注意以下几项：

    * os-operator和os-proxy镜像需要基于baseimage进行构建，请用户保证baseimage的安全性。
    * 需将os-operator和os-proxy二进制文件分别拷贝到对应的镜像中。
    * 请确保os-proxy镜像中os-proxy二进制文件件属主和属组为root，文件权限为500。
    * 请确保os-operator镜像中os-operator二进制文件属主和属组为容器内运行os-operator进程的用户，文件权限为500。
    * os-operator和os-proxy的二进制文件在镜像内的位置和容器启动时运行的命令需与部署的yaml中指定的字段相对应。

   Dockerfile示例如下

   ```dockerfile
   FROM your_baseimage
   COPY ./bin/proxy /proxy
   ENTRYPOINT ["/proxy"]
   ```

   ```dockerfile
   FROM your_baseimage
   COPY --chown=6552:6552 ./bin/operator /operator
   ENTRYPOINT ["/operator"]
   ```

   Dockerfile也可以使用多阶段构建。

5. 构建容器镜像（os-operator 和 os-proxy 镜像）。

   ```shell
   # 指定proxy的Dockerfile地址
   export DOCKERFILE_PROXY=your_dockerfile_proxy
   # 指定operator的Dockerfile路径
   export DOCKERFILE_OPERATOR=your_dockerfile_operator
   # 镜像构建
   docker build -t ${IMG_OPERATOR} -f ${DOCKERFILE_OPERATOR} .
   docker build -t ${IMG_PROXY} -f ${DOCKERFILE_PROXY} .
   ```

6. 将容器镜像 push 到镜像仓库。

   ```shell
   docker push ${IMG_OPERATOR}
   docker push ${IMG_PROXY}
   ```

### 制作容器OS虚拟机镜像

#### 注意事项

* 以虚拟机镜像为例，如需进行物理机的镜像制作请见《[容器OS镜像制作指导](./kubeos_image_creation.md)》。
* 制作容器OS 镜像需要使用 root 权限。
* 容器OS 镜像制作工具的 rpm 包源为 openEuler 具体版本的 everything 仓库和 EPOL 仓库。制作镜像时提供的 repo 文件中，yum 源建议同时配置 openEuler 具体版本的 everything 仓库和 EPOL 仓库。
* 使用默认 rpmlist 制作的容器OS虚拟机镜像，默认保存在调用`kbimg`路径下的`scripts-auto`文件夹内，该分区至少有 25GiB 的剩余磁盘空间。
* 制作容器 OS 镜像时，不支持用户自定义配置挂载文件。

#### 操作步骤

制作容器OS 虚拟机镜像使用 kbimg，命令详情请见《[容器OS镜像制作指导](./kubeos_image_creation.md)》。

制作容器OS 虚拟机镜像的步骤如下：

1. 进入执行目录：

   ```shell
   cd /opt/kubeOS/scripts
   ```

2. 执行 kbming 制作容器OS，参考命令如下：

   ```shell
   ./kbimg create -f ./kbimg.toml vm-img
   ```

   容器 OS 镜像制作完成后，会在 /opt/kubeOS/scripts/scripts-auto 目录下生成：

    * raw格式的系统镜像system.img，system.img大小默认为20G，支持的根文件系统分区大小<2560MiB，持久化分区<15GB。
    * qcow2 格式的系统镜像 system.qcow2。
    * 可用于升级的根文件系统 kubeos.tar。

   制作出来的容器 OS 虚拟机镜像目前只能用于 CPU 架构为 x86 和 AArch64 的虚拟机场景，不支持 x86 架构的虚拟机使用 legacy 启动模式启动。

### 部署CRD,operator和proxy

#### 注意事项

* 请先部署 Kubernetes 集群，部署方法参考[《openEuler 24.03-LTS-SP2 Kubernetes 集群部署指南》](../../cluster_deployment/kubernetes/overview.md)。

* 集群中准备进行升级的 Worker 节点的 OS 需要为使用上一节方式制作出来的容器 OS，如不是，请用 system.qcow2重新部署虚拟机，虚拟机部署请见[《openEuler 24.03-LTS-SP2 虚拟化用户指南》](https://docs.openeuler.openatom.cn/zh/docs/24.03_LTS_SP2/virtualization/virtulization_platform/stratovirt/stratovirt_introduction.html)，Master节点目前不支持容器 OS 升级，请用openEuler 24.03-LTS-SP1部署Master节点。
* 部署 OS 的 CRD（CustomResourceDefinition），os-operator，os-proxy 以及 RBAC (Role-based access control) 机制的 YAML 需要用户自行编写。
* operator 和 proxy 部署在 kubernetes 集群中，operator 应部署为 deployment，proxy 应部署为daemonset。
* 尽量部署好 kubernetes 的安全措施，如 rbac 机制，pod 的 service account 和 security policy 配置等。

#### 操作步骤

1. 准备 YAML 文件，包括用于部署 OS 的CRD、RBAC 机制、os- operator 和os- proxy 的 YAML 文件，可参考[yaml-example](https://gitee.com/openeuler/KubeOS/tree/master/docs/example/config)。假设分别为 crd.yaml、rbac.yaml、manager.yaml 。

2. 部署 CRD、RBAC、os-operator 和 os-proxy。假设 crd.yaml、rbac.yaml、manager.yaml 文件分别存放在当前目录的 config/crd、config/rbac、config/manager 目录下 ，参考命令如下：

   ```shell
   kubectl apply -f config/crd
   kubectl apply -f config/rbac 
   kubectl apply -f config/manager
   ```

3. 部署完成后，执行以下命令，确认各个组件是否正常启动。如果所有组件的 STATUS 为 Running，说明组件已经正常启动。

   ```shell
   kubectl get pods -A
   ```
