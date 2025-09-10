# Installation and Configuration

## Installation

### Prerequisites

- To obtain better performance experience, Kuasar must run on bare metal servers. **Currently, Kuasar cannot run on VMs.**
- The running of Kuasar depends on the following openEuler components. Ensure that the dependent components of the required versions have been installed in the environment.
    - iSulad (See [Installation and Configuration](../../container_engine/isula_container_engine/installation_configuration.md) of iSulad.)
    - StratoVirt (See [Installing StratoVirt](https://docs.openeuler.openatom.cn/en/docs/24.03_LTS_SP2/virtualization/virtulization_platform/stratovirt/install_stratovirt.html))

### Procedure

1. The Kuasar deliverables are included in the **kuasar** RPM package. Run the `yum` command to directly install Kuasar.

   ```sh
   yum install kuasar
   ```

2. Install the CRI command line tool crictl required for starting sandboxes and containers.

   ```sh
   # Arm environment
   $ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.25.0/crictl-v1.25.0-linux-arm64.tar.gz
   $ tar -zxvf crictl-v1.25.0-linux-arm64.tar.gz -C /usr/local/bin
   # x86 environment
   $ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.25.0/crictl-v1.25.0-linux-amd64.tar.gz
   $ tar -zxvf crictl-v1.25.0-linux-amd64.tar.gz -C /usr/local/bin
   ```

3. Install the CNI plugins required for CRI to configure the network.

   ```sh
   $ mkdir -p /opt/cni/bin && mkdir -p /etc/cni/net.d
   
   # Arm environment
   $ wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-arm64-v1.3.0.tgz
   $ tar -zxvf cni-plugins-linux-arm64-v1.3.0.tgz -C /opt/cni/bin/
   # x86 environment
   $ wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
   $ tar -zxvf cni-plugins-linux-amd64-v1.3.0.tgz -C /opt/cni/bin/
   ```

## Configuration

### Configuring iSulad

Modify the iSulad configuration file **/etc/isulad/daemon.json** so that iSulad can invoke the container runtime of the Kuasar VMM type. Add the following information:

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

Restart iSulad.

```sh
systemctl restart isulad
```

### crictl Configuration

Modify the crictl configuration file **/etc/crictl.yaml** to connect to iSulad.

```sh
$ cat /etc/crictl.yaml
runtime-endpoint: unix:///var/run/isulad.sock
image-endpoint: unix:///var/run/isulad.sock
timeout: 10
```

### Kuasar configuration

Modify the configuration file to connect Kuasar to StratoVirt. (You can use the default configuration. For details about the fields in the configuration file, see [Appendix](./kuasar_appendix.md).)

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

Start the kuasar-vmm service.

```sh
systemctl start kuasar-vmm
```

Check whether the service is running.

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
