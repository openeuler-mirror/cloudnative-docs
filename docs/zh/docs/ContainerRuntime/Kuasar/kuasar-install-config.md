# 安装与配置

## 安装方法

### 前提条件

- 为了获取更好的性能体验，kuasar需要运行在裸金属服务器上，**暂不支持kuasar运行在虚拟机内**。
- kuasar运行依赖以下openEuler组件，请确保环境上已安装所需版本的依赖组件。
    - iSulad（请参考iSula容器引擎的[安装与配置](./安装与配置.md)章节安装iSulad）
    - StratoVirt（请参考StratoVirt的[安装](../StratoVirt/安装StratoVirt.md)章节安装StratoVirt）

### 安装操作

1. kuasar发布组件集成在kuasar rpm包中，使用yum命令可以直接安装

   ```sh
   $ yum install kuasar
   ```

2. 安装启动沙箱及容器需要使用的cri命令行工具crictl

   ```sh
   # arm环境
   $ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.25.0/crictl-v1.25.0-linux-arm64.tar.gz
   $ tar -zxvf crictl-v1.25.0-linux-arm64.tar.gz -C /usr/local/bin
   # x86环境
   $ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.25.0/crictl-v1.25.0-linux-amd64.tar.gz
   $ tar -zxvf crictl-v1.25.0-linux-amd64.tar.gz -C /usr/local/bin
   ```

3. 安装cri配置网络需要使用的cni插件

   ```sh
   $ mkdir -p /opt/cni/bin && mkdir -p /etc/cni/net.d
   
   # arm环境
   $ wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-arm64-v1.3.0.tgz
   $ tar -zxvf cni-plugins-linux-arm64-v1.3.0.tgz -C /opt/cni/bin/
   # x86环境
   $ wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
   $ tar -zxvf cni-plugins-linux-amd64-v1.3.0.tgz -C /opt/cni/bin/
   ```

## 配置方法

### iSulad容器引擎的配置

修改iSulad容器引擎的配置文件/etc/isulad/daemon.json以支持iSulad容器引擎调用kuasar vmm虚拟机类型的容器运行时，新增如下配置：

```sh
$ cat /etc/isulad/daemon.json
...
    "cri-sandboxers": {
        "vmm": {
            "name": "vmm",
            "address": "/run/vmm-sandboxer.sock"
        }
    },
    "cri-runtimes": {
        "vmm": "io.containerd.vmm.v1"
    },
...
```

重新启动iSulad

```sh
$ systemctl restart isulad
```

### crictl的配置

修改crictl配置文件/etc/crictl.yaml对接isulad

```sh
$ cat /etc/crictl.yaml
runtime-endpoint: unix:///var/run/isulad.sock
image-endpoint: unix:///var/run/isulad.sock
timeout: 10
```

### kuasar的配置

修改kuasar对接stratovirt配置文件（可使用默认配置，配置文件字段说明详见[附录](./kuasar附录.md )）

```sh
$ cat /var/lib/kuasar/config_stratovirt.toml
[sandbox]
log_level = "info"

[hypervisor]
path = "/usr/bin/stratovirt"
machine_type = "virt,mem-share=on"
kernel_path = "/var/lib/kuasar/vmlinux.bin"
image_path = ""
initrd_path = "/var/lib/kuasar/kuasar.initrd"
kernel_params = "task.log_level=debug task.sharefs_type=virtiofs"
vcpus = 1
memory_in_mb = 1024
block_device_driver = "virtio-blk"
debug = true 
enable_mem_prealloc = false

[hypervisor.virtiofsd_conf]
path = "/usr/bin/vhost_user_fs"
```

启动kuasar-vmm服务

```sh
$ systemctl start kuasar-vmm
```

确认服务已处于running状态

```sh
$ systemctl status kuasar-vmm
● kuasar-vmm.service - Kuasar microVM type sandboxer daemon process
     Loaded: loaded (/usr/lib/systemd/system/kuasar-vmm.service; disabled; vendor preset: disabled)
     Active: active (running) since Sat 2023-08-26 14:57:08 CST; 1h 25min ago
   Main PID: 1000445 (vmm-sandboxer)
      Tasks: 99 (limit: 814372)
     Memory: 226.4M
     CGroup: /system.slice/kuasar-vmm.service
             └─ 1000445 /usr/local/bin/vmm-sandboxer --listen /run/vmm-sandboxer.sock --dir /run/kuasar-vmm
```
