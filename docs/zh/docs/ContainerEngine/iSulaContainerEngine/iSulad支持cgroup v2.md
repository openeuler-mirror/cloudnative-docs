# iSulad支持cgroup v2

## 概述

cgroup是linux中用于限制进程组资源的机制。cgroup目前包括两个版本，cgroup v1和cgroup v2。

cgroup v2的目标是取代cgroup v1，cgroup v2相较于cgroup v1具有以下优势：

- 统一层次结构：cgroup v2 引入了一个统一的层次结构，将不同的资源控制（如 CPU、内存等）合并到一个层次结构中。这消除了 cgroup v1 中的分离层次结构，使得资源配置更加直观和简化。
- 细粒度资源控制：cgroup v2 提供了更细粒度的资源控制，允许用户对各个进程组进行更精细的资源限制和分配。它支持对 CPU、内存、IO、网络、设备等资源进行精确的控制和配额分配。
- 改进的性能：cgroup v2 在性能方面进行了一些改进，包括减少锁竞争和提高资源分配的效率。这可能导致更好的性能和扩展性，特别是在大规模部署和高负载环境下。
- cgroup v2 结合 eBPF 可以在运行时动态修改设备访问规则，而无需重新加载内核模块或重启容器。这使得容器的设备访问策略可以根据实际需求进行动态调整和更新，提高了容器环境的灵活性和可管理性。

iSulad目前已支持 cgroup v2。

## 配置iSulad支持cgroup v2

要使用iSulad支持cgroup v2的功能，建议至少使用5.8以上的内核版本，可以使用uname -r命令查询内核的版本。

iSulad会自动检测当前的cgroup版本，如果系统配置成了只支持cgroup v2并将cgroup v2挂载到`/sys/fs/cgroup`目录下(系统自动挂载)，则iSulad会使用cgroup v2来限制容器的资源。

系统配置cgroup v2方式：可以在系统的启动命令行参数中配置`cgroup_no_v1=all`参数表示禁用所有v1的cgroup，这样系统启动时就会只开启cgroup v2并默认将cgroup v2子系统挂载到`/sys/fs/cgroup`目录下。

```sh
grubby --args="cgroup_no_v1=all" --update-kernel="/boot/vmlinuz-$(uname -r)"
```

`tips`:修改启动参数配置需谨慎

系统重启后，执行`mount | grep cgroup`命令，如果已经将cgroup2挂载到了`/sys/fs/cgroup`，则说明切换cgroup v2环境成功：

```sh
# mount | grep cgroup
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime)
```

## iSulad使用cgroup v2限制资源

无论是cgroup v1还是cgroup v2，iSulad提供给用户使用的接口都是一致的（在`isula create/isula run/isula update`有相应接口）。不过由于有部分cgroup v1支持的功能在cgroup v2中被去掉了或者实现方式有所变化，因此部分接口在cgroup v2中不可用或者含义发生变化。iSulad支持限制如下资源：

| 资源         | 功能                      | 和cgroup v1的差异                                                                                       |
| ---------- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| devices    | 限制对应的设备是否可以在容器中访问以及访问权限 | devcies子系统不再使用往cgroup文件里写值的方式进行限制，而是采用ebpf的方式进行限制，对于容器限制device而言无差异                                 |
| memory     | 限制容器的内存资源               | 不支持swappiness（--memory-swappiness），不支持kmem相关参数（--kernel-memory），不支持oom_control（"--oom-kill-disable） |
| cpu/cpuset | 限制容器的cpu资源              | 不支持实时线程的限制（--cpu-rt-period与--cpu-rt-runtime）                                                        |
| blkio/io   | 限制容器的块设备io              | 设置限制后，不仅限制块设备的IO，也能限制buffer IO                                                                      |
| hugetlb    | 限制大页内存的使用               | 无差异                                                                                                 |
| pids       | 限制容器使用的pid              | 无差异                                                                                                 |
| freeze     | 暂停容器                    | 无差异                                                                                                 |

例如：若在cgroup v2环境下v2使用不支持的选项(以`--memory-swappiness`为例)，isula命令会有如下报错：

```sh
[root@openEuler ~]# isula run -tid --memory-swappiness 90 busybox /bin/sh
Error response from daemon: Your kernel does not support memory swappiness capabilities, memory swappiness discarded.
```

## 使用限制

1. iSulad只识别挂载在`/sys/fs/cgroup`目录下的cgroup。
2. iSulad不支持cgroup v1与cgroup v2混用场景，仅根据`/sys/fs/cgroup`目录下的cgroup版本决定iSulad内部使用的cgroup版本。
