# Rubik Configuration Description

The Rubik program is written in Go and compiled into a static executable file to minimize the coupling with the system.

## Commands

Besides the `-v` option for querying version information, Rubik does not support other options. The following is an example of version query output:

```bash
$ ./rubik -v
Version:       2.0.1
Release:       2.oe2403sp1
Go Version:    go1.22.1
Git Commit:    bcaace8
Built:         2024-12-10
OS/Arch:       linux/amd64
```

## Configuration

When the Rubik binary file is executed, Rubik parses configuration file **/var/lib/rubik/config.json**.

> [!NOTE]Note
>
> Custom configuration file path is currently not supported to avoid confusion.
> When Rubik runs as a Daemonset in a Kubernetes cluster, modify the ConfigMap in the **hack/rubik-daemonset.yaml** file to configure Rubik.

The configuration file is in JSON format and keys are in lower camel case.

An example configuration file is as follows:

```json
{
  "agent": {
    "logDriver": "stdio",
    "logDir": "/var/log/rubik",
    "logSize": 2048,
    "logLevel": "info",
    "cgroupRoot": "/sys/fs/cgroup",
    "enabledFeatures": [
      "preemption",
      "dynCache",
      "ioLimit",
      "ioCost",
      "quotaBurst",
      "quotaTurbo",
      "psi",
      "cpuevict",
      "memoryevict"
    ]
  },
  "preemption": {
    "resource": [
      "cpu",
      "memory"
    ]
  },
  "quotaTurbo": {
    "highWaterMark": 50,
    "syncInterval": 100
  },
  "dynCache": {
    "defaultLimitMode": "static",
    "adjustInterval": 1000,
    "perfDuration": 1000,
    "l3Percent": {
      "low": 20,
      "mid": 30,
      "high": 50
    },
    "memBandPercent": {
      "low": 10,
      "mid": 30,
      "high": 50
    }
  },
  "ioCost": [
    {
      "nodeName": "k8s-single",
      "config": [
        {
          "dev": "sdb",
          "enable": true,
          "model": "linear",
          "param": {
            "rbps": 10000000,
            "rseqiops": 10000000,
            "rrandiops": 10000000,
            "wbps": 10000000,
            "wseqiops": 10000000,
            "wrandiops": 10000000
          }
        }
      ]
    }
  ],
  "psi": {
    "interval": 10,
    "resource": [
      "cpu",
      "memory",
      "io"
    ],
    "avg10Threshold": 5.0
  },
  "cpuevict": {
    "threshold": 60,
    "interval": 1,
    "windows": 2,
    "cooldown": 20
  },
  "memoryevict": {
    "threshold": 60,
    "interval": 1,
    "cooldown": 4
  }
}
```

Rubik configuration items include common items and feature items. Common items are under the **agent** section and are applied globally. Feature items are applied to sub-features that are enabled in the **enabledFeatures** field under **agent**.

### agent

The **agent** section stores common configuration items related to Rubik running, such as log configurations and cgroup mount points.

| Key\[=Default Value]       | Type   | Description                                                                 | Example Value        |
| ------------------------- | ---------- | -------------------------------------- | --------------------------- |
| logDriver=stdio           | string     | Log driver, which can be the standard I/O or file           | stdio, file                 |
| logDir=/var/log/rubik     | string     | Log directory                           | Anu readable and writable directory              |
| logSize=1024              | int        | Total size of logs in MB when logDriver=file | \[10, $2^{20}$]              |
| logLevel=info             | string     | Log level                           | debug,info,warn,error       |
| cgroupRoot=/sys/fs/cgroup | string     | Mount point of the system cgroup                   | Mount point of the system cgroup        |
| enabledFeatures=\[]        | string array | List of Rubik features to be enabled                | Rubik features. see [Feature Introduction](./feature_introduction.md) for details. |

### preemption

The **preemption** field stores configuration items of the absolute preemption feature, including CPU and memory preemption. You can configure this field to use either or both of CPU and memory preemption.

| Key\[=Default Value]       | Type   | Description                                                                 | Example Value        |
| --------------- | ---------- | -------------------------------- | ----------- |
| resource=\[]     | string array | Resource type to be accessed | cpu, memory |

### dynCache

The **dynCache** field stores configuration items related to pod memory bandwidth and last-level cache (LLC) limits. **l3Percent** indicates the watermarks of each LLC level. **memBandPercent** indicates watermarks of memory bandwidth in MB.

| Key\[=Default Value]    | Type   | Description                                                       | Example Value   |
| ----------------------- | ------ | ----------------------------------------------------------------- | --------------- |
| defaultLimitMode=static | string | dynCache control mode                                             | static, dynamic |
| adjustInterval=1000     | int    | Interval for dynCache control, in milliseconds                    | \[10, 10000]    |
| perfDuration=1000       | int    | perf execution duration for dynCache, in milliseconds             | \[10, 10000]    |
| l3Percent               | map    | Watermarks of each L3 cache level of dynCache in percents         |                 |
| .low=20                 | int    | Watermark of the low L3 cache level                               | \[10, 100]      |
| .mid=30                 | int    | Watermark of the middle L3 cache level                            | \[low, 100]     |
| .high=50                | int    | Watermark of the high L3 cache level                              | \[mid, 100]     |
| memBandPercent          | map    | Watermarks of each memory bandwidth level of dynCache in percents |                 |
| .low=10                 | int    | Watermark of the low bandwidth level in MB                        | \[10, 100]      |
| .mid=30                 | int    | Watermark of the middle bandwidth level in MB                     | \[low, 100]     |
| .high=50                | int    | Watermark of the high bandwidth level in MB                       | \[mid, 100]     |

### quotaTurbo

The **quotaTurbo** field stores configuration items of the user-mode elastic traffic limiting feature.

| Key\[=Default Value]       | Type   | Description                                                                 | Example Value        |
| ----------------- | ------ | -------------------------------- | -------------------- |
| highWaterMark=60  | int | High watermark of CPU load         |\[0, alarmWaterMark) |
| alarmWaterMark=80 | int | Alarm watermark of CPU load | (highWaterMark,100\]            |
| syncInterval=100  | int | Interval for triggering container quota updates, in milliseconds | \[100,10000] |

### ioCost

The **ioCost** field stores configuration items of the iocost-based I/O weight control feature. The field is an array whose elements are names of nodes (**nodeName**) and their device configuration arrays (**config**).

| Key       | Type   | Description                                                                 | Example Value        |
| ----------------- | ------ | -------------------------------- | -------------------- |
| nodeName  | string | Node name         | Kubernetes cluster node name |
| config | array | Configurations of a block device |   /       |

**config** parameters of a block device:

| Key\[=Default Value] | Type   | Description                                                                 | Example Value        |
| --------------- | ------ | --------------------------------------------- | -------------- |
| dev             | string | Physical block device name                    | /              |
| model           | string | iocost model                                | linear         |
| param           | /      | Device parameters specific to the model               | /              |

For the **linear** model, the **param** field supports the following parameters:

| Key\[=Default Value] | Type   | Description                                                                 | Example Value        |
| --------------- | ---- | ---- | ------ |
| rbps            | int64  | Maximum read bandwidth     | (0, $2^{63}$) |
| rseqiops        | int64  | Maximum sequential read IOPS  | (0, $2^{63}$) |
| rrandiops       | int64  | Maximum random read IOPS | (0, $2^{63}$) |
| wbps            | int64  | Maximum write bandwidth     | (0, $2^{63}$) |
| wseqiops        | int64  | Maximum sequential write IOPS | (0, $2^{63}$) |
| wrandiops       | int64  | Maximum random write IOPS | (0, $2^{63}$) |

### psi

The **psi** field stores configuration items of the PSI-based interference detection feature. This feature can monitor CPUs, memory, and I/O resources.You can configure this field to monitor the PSI of any or all of the resources.

| Key\[=Default Value] | Type   | Description                                                                 | Example Value        |
| --------------- | ---------- | -------------------------------- | ----------- |
| interval=10 |int|Interval for PSI monitoring, in seconds| \[10,30]|
| resource=\[]     | string array | Resource type to be accessed | cpu, memory, io |
| avg10Threshold=5.0     | float | Average percentage of blocking time of a job in 10 seconds. If this threshold is reached, offline services are evicted. | \[5.0,100]|

### CPU Eviction Watermark Control

The **cpuevict** field is used to configure CPU eviction watermark control. This feature collects the node CPU utilization at specified intervals and calculates the average CPU utilization over a defined window. If the average CPU utilization exceeds the eviction watermark, offline Pods are evicted. Once Rubik evicts offline Pods, no further evictions occur during the cooldown period.

| Key\[=Default Value] | Type   | Description                                                                 | Example Value        |
|----------------------|---------|-----------------------------------------------------------------------------|----------------------|
| `threshold=60`       | int     | Threshold for average CPU utilization (%). If exceeded, offline Pods are evicted. | \[1, 99]            |
| `interval=1`         | int     | Interval (in seconds) for collecting node CPU utilization.                  | \[1, 3600]          |
| `windows=2`          | int     | Window period (in seconds) for calculating the average CPU utilization. The window must be greater than the interval. If not set, the window defaults to twice the interval. | \[1, 3600]          |
| `cooldown=20`        | int     | Cooldown period (in seconds). No evictions occur during this period after an eviction. | \[1, 9223372036854775806] |

### Memory Eviction Watermark Control

The **memoryevict** field is used to configure memory eviction watermark control. This feature collects the node memory utilization at specified intervals. If the memory utilization exceeds the eviction watermark, offline Pods are evicted. Once Rubik evicts offline Pods, no further evictions occur during the cooldown period.

| Key\[=Default Value] | Type   | Description                                                                 | Example Value        |
|----------------------|---------|-----------------------------------------------------------------------------|----------------------|
| `threshold`          | int     | Threshold for memory utilization (%). If exceeded, offline Pods are evicted. If not specified, this feature is disabled. | \[1, 99]            |
| `interval=1`         | int     | Interval (in seconds) for collecting node memory utilization.               | \[1, 3600]          |
| `cooldown=4`         | int     | Cooldown period (in seconds). No evictions occur during this period after an eviction. | \[1, 9223372036854775806] |
