# Appendix

Fields in the **/var/lib/kuasar/config_stratovirt.toml** configuration file:

```conf
[sandbox]
log_level: Kuasar log level. The default value is info.

[hypervisor]
path: path of the StratoVirt binary file
machine_type: the processor type to be simulated (virt for the Arm architecture and q35 for the x86 architecture)
kernel_path: execution path of the guest kernel
image_path: execution path of the guest image
initrd_path: execution path of the guest initrd (Configure either initrd_path or image_path.)
kernel_params: guest kernel parameters
vcpus: default number of vCPUs for each sandbox (default: 1)
memory_in_mb: default memory size of each sandbox (default: 1024 MiB)
block_device_driver: block device driver
debug: whether to enable debug mode
enable_mem_prealloc: whether to enable memory pre-allocation

[hypervisor.virtiofsd_conf]
path: path of vhost_user_fs
```
