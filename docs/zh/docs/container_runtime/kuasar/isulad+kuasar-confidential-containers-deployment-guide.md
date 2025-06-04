# isulad+kuasar机密容器部署指南

机密容器用于解决云原生场景下的数据安全问题，满足数据合规、数据隐私保护、算法和模型等创新 IP 保护，数据可用但是不可见等使用需求，以及解决云厂商的信任依赖问题。

## 环境准备

### 物理环境准备

为了获取更好的性能体验，kuasar需要运行在裸金属服务器上，**暂不支持kuasar运行在虚拟机内**。
当前机密虚机只支持基于鲲鹏920新型号处理器环境搭建TEE套件环境使用。服务器目前只支持在aarch64环境上加载TEE License使能TEE套件特性，并通过BIOS配置选项开启TEE特性并设置TEE安全内存大小。

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

#### 修改iSulad 配置文件

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

cri-sandboxers 和 cri-runtimes指定启动sandbox运行时的相关配置。其他参数可以参考[安装与配置](./kuasar_install_config.md)文档。

#### 配置机密容器参数

默认情况下kuasar可以使用普通镜像仓库，如果需要使用机密镜像仓库，可以修改/var/lib/kuasar/cc-config.toml中的kernel_params参数，参考下表，以key=value的形式补充需要的参数。

|Key|Type|Description|
|---|---|---|
|task.aa_kbc_params|String|远程证明代理的IP和端口。|
|task.aa_kbc_key_provider|String|key provider类型，目前支持"secgear"类型。|
|task.aa_ser_url|String|远程证明密钥托管服务器地址。|
|task.aa_cert|String|远程证明根证书文件路径。|
|task.aa_proto|String|与远程证明服务器通信的协议类型。|
|task.https_proxy|String|拉取镜像时的https代理环境变量。|
|task.no_proxy|String|拉取镜像时不使用代理地址的环境变量。|
|task.enable_signature_verification|bool|安全验证开关控制。|
|task.image_policy|String|`Policy.json`路径。|
|task.image_registry_auth|String|鉴权文件路径。|
|task.simple_signing_sigstore_config|String|用于简单签名的Sigstore配置文件。|

修改/var/lib/kuasar/cc-config.toml后，重启cc-kuasar-vmm.service后配置生效，用于拉起之后的机密沙箱。

值得注意的是，由于机密容器需要在沙箱内拉容器镜像，因此需要重新打包目标镜像网站的CA证书到机密虚机的rootfs镜像，方法示例如下：

1.在镜像仓服务器：如果是本地镜像仓，需要先将镜像仓证书写入镜像本地仓所在服务器根证书，如果domain.crt文件为镜像仓证书，执行如下命令：

```sh
$cat domain.crt >> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
$cat domain.crt >> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
```

2.在机密容器服务器：需要将访问远程镜像仓库所需的证书，打包到机密沙箱镜像：比如当机密容器服务器已经可以成功访问镜像仓服务器时，将机密容器服务器上的证书和镜像仓服务器证书domain.crt都打包到机密沙箱镜像：

```sh
$ls /var/lib/kuasar/cc-rootfs.img
/var/lib/kuasar/cc-rootfs.img
$mkdir cc-rootfs
$mount /var/lib/kuasar/cc-rootfs.img ./cc-rootfs
$cp -r /etc/pki/ca-trust ./cc-rootfs/etc/pki/ca-trust
$cat domain.crt >> ./cc-rootfs/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
$cat domain.crt >> ./cc-rootfs/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
$umount ./cc-rootfs
```

如果还需使用远程代理和加密镜像的功能，需要做如下配置：

1.上传加密镜像到远程镜像服务器时，需要为镜像的manifest添加注解，格式如下：

```json
"org.opencontainers.image.enc.keys.provider.secgear": "<远程托管的密钥路径的base64编码>"
```

2.为远程证明服务节点预置远程证明根证书，如果该证书文件为as_cert.pem，示例步骤如下：

```sh
$mount /var/lib/kuasar/cc-rootfs.img ./cc-rootfs
$mkdir -p ./cc-rootfs/etc/attestation/attestation-agent
$cp as_cert.pem ./cc-rootfs/etc/attestation/attestation-agent/as_cert.pem
$umount ./cc-rootfs
```

3.为远程证明和镜像解密服务配置参数，示例如下：

```bash
$cat /var/lib/kuasar/cc-config.toml
... ...
kernel_params = "task.aa_kbc_params=127.0.0.1:8088 task.aa_kbc_key_provider=secgear task.aa_ser_url=xx.xx.xx.xx:8080: task.aa_cert=/etc/attestation/attestation-agent/as_cert.pem task.aa_proto=http ... ..."
```

当前task.aa_kbc_key_provider只支持"secgear"，task.aa_proto只支持"http"，默认为"http"。

配置完毕上述参数后，重启cc-kuasar-vmm.service后配置生效，用于拉起之后的机密沙箱。

### 准备容器配置文件

#### 增加cni配置文件

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

>[!WARNING]注意
>如果要使用加密镜像的话，在配置完毕，将`"docker.io/library/busybox-aarch64:latest"`替换为加密镜像的地址，比如：`x.x.x.x:5000/test_encryted_image:latest`。

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

重新启动iSulad 和 kuasar进程

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
