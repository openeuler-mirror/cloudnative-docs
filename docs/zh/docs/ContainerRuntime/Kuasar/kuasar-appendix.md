# 附录

 /var/lib/kuasar/config_stratovirt.toml配置文件字段说明：

```conf
[sandbox]
log_level ：指定kuasar日志级别，默认为info

[hypervisor]
path ：指定stratovirt二进制路径
machine_type ：指定模拟芯片类型，ARM架构为virt，x86架构为q35
kernel_path ：指定guest kernel执行路径
image_path ：指定guest image执行路径
initrd_path ：指定guest initrd执行路径，与image二选一
kernel_params ：指定guest内核运行参数
vcpus ：指定每个沙箱的默认vCPU数量，默认为1
memory_in_mb ：指定每个沙箱的默认内存大小，默认为1024 MiB
block_device_driver ：指定块设备驱动
debug ：指定是否开启debug模式 
enable_mem_prealloc ：指定是否开启内存预占

[hypervisor.virtiofsd_conf]
path ：指定vhost_user_fs路径 
```
