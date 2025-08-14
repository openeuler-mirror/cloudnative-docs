# isulad+kuasar 机密容器部署指南

机密容器用于解决云原生场景下的数据安全问题，满足数据合规、数据隐私保护、算法和模型等创新 IP 保护，数据可用但是不可见等使用需求，以及解决云厂商的信任依赖问题。

## 环境准备

### 物理环境准备

为了获取更好的性能体验，kuasar 需要运行在裸金属服务器上，**暂不支持 kuasar 运行在虚拟机内**。
当前机密虚机只支持基于鲲鹏920新型号处理器环境搭建TEE套件环境使用。服务器目前只支持在 aarch64 环境上加载 TEE License 使能TEE套件特性，并通过 BIOS 配置选项开启 TEE 特性并设置 TEE 安全内存大小。

### 软件安装

```sh
$ yum install iSulad kuasar-cc qemu-system-aarch64
```

#### cni插件安装

```sh
$ wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-arm64-v1.3.0.tgz
$ mkdir -p /opt/cni/bin/
$ tar -zxvf cni-plugins-linux-arm64-v1.3.0.tgz -C /opt/cni/bin/
```

### 修改容器引擎与容器运行时配置文件

#### 修改 iSulad 配置文件

```sh
vi /etc/isulad/daemon.json

{
    ... ...
    "network-plugin": "cni",
    "default-sandboxer": "cc",
    "enable-cri-v1": true,
    "cri-sandboxers": {
        "cc": {
            "name": "cc", 
            "image-type":"remote",
            "address": "/run/cc-vmm-sandboxer.sock"
        }
    },
    "cri-runtimes": {
        "cc": "io.containerd.cc.v1"
    }
    ... ...
}
```

cri-sandboxers 和 cri-runtimes 指定启动 sandbox 运行时的相关配置。其他参数可以参考[安装与配置](../../container_engine/isula_container_engine/installation_configuration.md)文档。

#### 配置机密容器参数

默认情况下 kuasar 可以使用普通镜像仓库，如果需要使用机密镜像仓库，可以修改/var/lib/kuasar/cc-config.toml中的kernel_params参数，参考下表，以 key=value 的形式补充需要的参数。

值得注意的是，由于机密容器需要在沙箱内拉容器镜像，因此需要保证主机上镜像网站的 TLS 证书验证通过，能正常访问镜像网站。

|Key|Type|Description|
|---|---|---|
|task.aa_kbc_params|String|远程证明代理和密钥代理配置的参数。|
|task.https_proxy|String|拉取镜像时的https代理环境变量。|
|task.no_proxy|String|拉取镜像时不使用代理地址的环境变量。|
|task.enable_signature_verification|bool|安全验证开关控制。|
|task.image_policy|String|`Policy.json`路径。|
|task.image_registry_auth|String|鉴权文件路径。|
|task.simple_signing_sigstore_config|String|用于简单签名的Sigstore配置文件。|

修改 /var/lib/kuasar/cc-config.toml 后，重启 cc-kuasar-vmm.service 后配置生效，用于拉起下一个机密沙箱。

### 准备容器配置文件

#### 增加 cni 配置文件

```sh
cat /etc/cni/net.d/mynet.conf 
{
  "cniVersion":"1.0.0",
  "name":"bridge-network",
  "type":"bridge",
  "bridge":"cni0",
  "isGateway":true,
  "ipMasq":true,
  "ipam":{
    "type":"host-local",
    "subnet":"10.244.0.0/16",
    "routes":[
      {"dst":"0.0.0.0/0"}
    ]
  }
}
```

#### pod 配置文件

```json
cat pod.json
{
        "annotations": {
        "cri.sandbox.network.setup.v2": "true"
        },
        "hostname": "testhostname",
        "log_directory": "/tmp",
        "linux": {
                "cgroup_parent": "/sys/fs/cgroup",
                "security_context": {
                        "namespace_options": {
                                "network": 0,
                                "pid": 0,
                                "ipc": 0
                        },
                "run_as_user": {
                        "value": 1003
                },
                "readonly_rootfs": true,
                "privileged": false
                }
        },
        "metadata": {
                "attempt": 1,
                "name": "liuxuPod",
                "namespace": "default",
                "uid": "2dishd83djaidwnduwk28baaa"
        }
}
```

#### container 配置文件

```json
cat local_container.json
{
    "metadata": {
        "name": "test-busybox"
    },
    "image": {
        "image": "docker.io/library/busybox-aarch64:latest"
    },
    "command": [
        "top"
    ],
    "log_path":"console.log",
    "linux": {
        "security_context": {
            "capabilities": {},
            "namespace_options": {
                "network": 0,
                "pid": 1
            }
        }
    }
}
```

## 启动机密容器

重新启动 iSulad 和 kuasar 进程

```sh
$systemctl restart cc-kuasar-vmm.service
$systemctl restart isulad.service
```

启动机密容器

```sh
$crictl runp --runtime cc pod.json 
8d69fee1179c4b0626230c315f48daf5ae75fcd36f080c4547724cc9aa590db9
$crictl create 8d local_container.json pod.json
e69888c21385facad647e51998c5406092734d73834f9b84842820f8aef9d408
$crictl start e6
e6
```

当不再需要容器时，可以分别使用`crictl rm ${container id}` 删除容器，使用`crictl rmp ${sandbox id}`删除沙箱。
