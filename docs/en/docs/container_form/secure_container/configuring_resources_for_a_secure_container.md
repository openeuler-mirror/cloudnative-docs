# Configuring Resources for a Secure Container

The secure container runs on a virtualized and isolated lightweight VM. Therefore, resource configuration is divided into two parts: resource configuration for the lightweight VM, that is, host resource configuration; resource configuration for containers in the VM, that is, guest container resource configuration. The following describes resource configuration for the two parts in detail.

## Sharing Resources

Because the secure container runs on a virtualized and isolated lightweight VM, resources in some namespaces on the host cannot be accessed. Therefore,  **--net host**,  **--ipc host**,  **--pid host**, and  **--uts host**  are not supported during startup.

When a pod is started, all containers in the pod share the same net namespace and ipc namespace by default. If containers in the same pod need to share the pid namespace, you can use Kubernetes to configure the pid namespace. In Kubernetes 1.11, the pid namespace is disabled by default.

## Limiting Resources

Limitations on sandbox resources should be configured in **configuration.toml**. 
Common fields are:

- **default_vcpus**: specifies the default number of virtual CPUs.
- **default_maxvcpus**: specifies the max number of virtual CPUs.
- **default_root_ports**: specifies the default number of Root Ports in SB/VM.
- **default_bridges**: specifies the default number of bridges.
- **default_memory**: specifies the size of memory. The default size is 1024 MiB.
- **memory_slots**: specifies the number of memory slots. The default number is **10**.

## Limiting Memory Resources Through the Memory Hotplug Feature

Memory hotplug is a key feature for containers to allocate memory dynamically in deployment. As Kata containers are based on VMs, this feature needs support both from VMM and guest kernel. Luckily, it has been fully supported for the current default version of QEMU and guest kernel used by Kata on ARM64. For other VMMs, e.g, Cloud Hypervisor, the enablement work is on the road. Apart from VMM and guest kernel, memory hotplug also depends on ACPI which depends on firmware. On x86, you can boot a VM using QEMU with ACPI enabled directly, because it boots up with firmware implicitly. For ARM64, however, you need specify firmware explicitly. That is to say, if you are ready to run a normal Kata container on ARM64, what you need extra to do is to install the UEFI ROM before using the memory hotplug feature.

```shell
pushd $GOPATH/src/github.com/kata-containers/tests
sudo .ci/aarch64/install_rom_aarch64.sh # For Ubuntu only
popd
```
