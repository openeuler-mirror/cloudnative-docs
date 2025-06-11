# iSulad Support for Cgroup v2

## Overview

cgroup is used to restrict process group resources in Linux. It has two versions: cgroup v1 and cgroup v2.

cgroup v2 is developed to replace cgroup v1. Compared with cgroup v1, cgroup v2 has the following advantages:

- Unified hierarchy: cgroup v2 introduces a unified hierarchy to combine different resource controls (such as CPU and memory) into one hierarchy. This eliminates the separated hierarchies in cgroup v1, making resource configuration more intuitive and simplified.
- Fine-grained resource control: cgroup v2 enables precise resource control, allowing users to restrict and allocate resources with fine granularity for each process group. It supports precise control and quota allocation for CPU, memory, I/O, network, and device resources.
- Improved performance: cgroup v2 has made some improvements in performance, including reducing lock contention and improving resource allocation efficiency. This could lead to better performance and scalability, especially in large-scale deployment and high-load environments.
- cgroup v2 combined with eBPF can dynamically modify device access rules at run time without reloading kernel modules or restarting containers. This enables device access policies of a container to be dynamically adjusted and updated as required, thereby improving flexibility and manageability of container environments.

iSulad has supported cgroup v2.

## Configuring iSulad to Support Cgroup v2

To enable iSulad to support cgroup v2, you are advised to use kernel 5.8 or later. You can run the `uname -r` command to query the kernel version.

iSulad automatically checks the current cgroup version. If the system supports only cgroup v2 and automatically mounts cgroup v2 to the **/sys/fs/cgroup** directory, iSulad uses cgroup v2 to restrict container resources.

You can configure **cgroup_no_v1=all** in the kernel boot parameters to disable all cgroups of v1. In this way, when the system starts, only cgroup v2 is enabled and the cgroup v2 subsystems are mounted to the **/sys/fs/cgroup** directory by default.

```sh
grubby --args="cgroup_no_v1=all" --update-kernel="/boot/vmlinuz-$(uname -r)"
```

**Tips**: Exercise caution when modifying boot parameters.

After system restart, run the `mount | grep cgroup` command. If cgroup v2 is mounted to **/sys/fs/cgroup**, the environment has switched to cgroup v2.

```sh
# mount | grep cgroup
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime)
```

## iSulad Using Cgroup v2 to Restrict Resources

iSulad provides the same interfaces (`isula create`, `isula run`, and `isula update`) for users no matter cgroup v1 or cgroup v2 is used. However, some functions supported by cgroup v1 are removed from cgroup v2 or the implementation modes are changed in cgroup v2. Therefore, some interfaces are unavailable or their meanings are changed in cgroup v2. iSulad can restrict the following resources:

| Resource        | Function                     | Difference from cgroup v1                                                                                      |
| ---------- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| devices    | Restricts access to devices in a container.| The **devices** subsystem uses eBPF instead of writing values to the cgroup file to restrict resources. The device restrictions for containers are the same.                                |
| memory     | Restricts the memory resources of a container.              | swappiness (`--memory-swappiness`), kmem option (`--kernel-memory`), and oom_control (`--oom-kill-disable`) are not supported.|
| cpu/cpuset | Restricts the CPU resources of a container.             | The restriction on real-time threads (`--cpu-rt-period` and `--cpu-rt-runtime`) is not supported.                                                       |
| blkio/io   | Restricts the block device I/Os of a container.             | After the limit is set, not only the I/O of the block device but also the I/O of the buffer can be limited.                                                                     |
| hugetlb    | Restricts the use of huge page memory.              | No difference.                                                                                                |
| pids       | Restricts the PIDs used by a container.             | No difference.                                                                                                |
| freeze     | Suspends a container.                   | No difference.                                                                                                |

For example, if an unsupported option (for example, `--memory-swappiness`) is used in the cgroup v2 environment, the following error information is displayed when you run the `isula` command:

```sh
[root@openEuler ~]# isula run -tid --memory-swappiness 90 busybox /bin/sh
Error response from daemon: Your kernel does not support memory swappiness capabilities, memory swappiness discarded.
```

## Constraints

1. iSulad identifies only cgroups mounted to the **/sys/fs/cgroup** directory.
2. iSulad does not support the mixed use of cgroup v1 and cgroup v2. The cgroup version used in iSulad is determined by the cgroup version in the **/sys/fs/cgroup** directory.
