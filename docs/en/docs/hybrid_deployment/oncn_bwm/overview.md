# oncn-bwm User Guide

## Introduction

With the rapid development of technologies such as cloud computing, big data, artificial intelligence, 5G, and the Internet of Things (IoT), data center construction becomes more and more important. However, the server resource utilization of the data center is very low, resulting in a huge waste of resources. To improve the utilization of server resources, oncn-bwm emerges.

oncn-bwm is a pod bandwidth management tool applicable to hybrid deployment of offline services. It properly schedules network resources for nodes based on QoS levels to ensure online service experience and greatly improve the overall network bandwidth utilization of nodes.

The oncn-bwm tool supports the following functions:

- Enabling/Disabling/Querying pod bandwidth management
- Setting the pod network priority
- Setting the offline service bandwidth range and online service waterline
- Querying internal statistics

## Installation

### Environmental Requirements

- Operating system: openEuler 24.03 LTS with the Yum repository of openEuler 24.03 LTS

### Installation Procedure

Run the following command:

```shell
yum install oncn-bwm
```

## How to Use

The oncn-bwm tool provides the `bwmcli` command line tool to enable pod bandwidth management or perform related configurations. The overall format of the `bwmcli` command is as follows:

**bwmcli**  \< option(s) >

> Note:
>
> The root permission is required for running the `bwmcli` command.
>
> Pod bandwidth management is supported only in the outbound direction of a node (packets are sent from the node to other nodes).
>
> Pod bandwidth management cannot be enabled for NICs for which tc qdisc rules have been configured.
>
> Upgrading the oncn-bwm package does not affect the enabling status before the upgrade. Uninstalling the oncn-bwm package disables pod bandwidth management for all NICs.

### Command Interfaces

#### Pod Bandwidth Management

##### Commands and Functions

| Command Format                   | Function                                                        |
| --------------------------- | ------------------------------------------------------------ |
| **bwmcli -e** \<NIC name >   | Enables pod bandwidth management for a specified NIC.|
| **bwmcli -d** \<NIC name >   | Disables pod bandwidth management for a specified NIC.|
| **bwmcli -p devs**          | Queries pod bandwidth management of all NICs on a node.|

> Note:
>
> - If no NIC name is specified, the preceding commands take effect for all NICs on a node.
>
> - Enable pod bandwidth management before running other `bwmcli` commands.

##### Examples

- Enable pod bandwidth management for NICs eth0 and eth1.

  ```shell
  # bwmcli -e eth0 -e eth1
  enable eth0 success
  enable eth1 success
  ```

- Disable pod bandwidth management for NICs eth0 and eth1.

  ```shell
  # bwmcli -d eth0 -d eth1
  disable eth0 success
  disable eth1 success
  ```

- Query pod bandwidth management of all NICs on a node.

  ```shell
  # bwmcli -p devs
  eth0            : enabled
  eth1            : disabled
  eth2            : disabled
  docker0         : disabled
  lo              : disabled
  ```

#### Pod Network Priority

##### Commands and Functions

| Command Format                                                    | Function                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **bwmcli -s** *path* \<prio>                                  | Sets the network priority of a pod. *path* indicates the cgroup path corresponding to the pod, and *prio* indicates the priority. The value of *path* can be a relative path or an absolute path. The default value of *prio* is **0**. The optional values are **0** and **-1**. The value **0** indicates online services, and the value **-1** indicates offline services.|
| **bwmcli -p** *path*                                         | Queries the network priority of a pod.                                         |

> Note:
>
> Online and offline network priorities are supported. The oncn-bwm tool controls the bandwidth of pods in real time based on the network priority. The specific policy is as follows: For online pods, the bandwidth is not limited. For offline pods, the bandwidth is limited within the offline bandwidth range.

##### Examples

- Set the priority of the pod whose cgroup path is **/sys/fs/cgroup/net_cls/test_online** to **0**.

  ```shell
  # bwmcli -s /sys/fs/cgroup/net_cls/test_online 0
  set prio success
  ```

- Query the priority of the pod whose cgroup path is **/sys/fs/cgroup/net_cls/test_online**.

  ```shell
  # bwmcli -p /sys/fs/cgroup/net_cls/test_online
  0
  ```

#### Offline Service Bandwidth Range

| Command Format                          | Function                                                        |
| ---------------------------------- | ------------------------------------------------------------ |
| **bwmcli -s bandwidth** \<low,high> | Sets the offline bandwidth for a host or VM. **low** indicates the minimum bandwidth, and **high** indicates the maximum bandwidth. The unit is KB, MB, or GB, and the value range is \[1 MB, 9999 GB].|
| **bwmcli -p bandwidth**            | Queries the offline bandwidth of a host or VM.                         |

> Note:
> 
> - All NICs with pod bandwidth management enabled on a host are considered as a whole, that is, the configured online service waterline and offline service bandwidth range are shared.
>
> - The pod bandwidth configured using `bwmcli` takes effect for all offline services on a node. The total bandwidth of all offline services cannot exceed the bandwidth range configured for the offline services. There is no network bandwidth limit for online services.
>
> - The offline service bandwidth range and online service waterline are used together to limit the offline service bandwidth. When the online service bandwidth is lower than the configured waterline, the offline services can use the configured maximum bandwidth. When the online service bandwidth is higher than the configured waterline, the offline services can use the configured minimum bandwidth.

##### Examples

- Set the offline bandwidth to 30 Mbit/s to 100 Mbit/s.

  ```shell
  # bwmcli -s bandwidth 30mb,100mb
  set bandwidth success
  ```

- Query the offline bandwidth range.

  ```shell
  # bwmcli -p bandwidth
  bandwidth is 31457280(B),104857600(B)
  ```

#### Online Service Waterline

##### Commands and Functions

| Command Format                                      | Function                                                        |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **bwmcli -s waterline** \<val>                  | Sets the online service waterline for a host or VM. *val* indicates the waterline value. The unit is KB, MB, or GB, and the value range is [20 MB, 9999 GB].|
| **bwmcli -p waterline**                        | Queries the online service waterline of a host or VM.                         |

> Note:
>
> - When the total bandwidth of all online services on a host is higher than the waterline, the bandwidth that can be used by offline services is limited. When the total bandwidth of all online services on a host is lower than the waterline, the bandwidth that can be used by offline services is increased.
> - The system determines whether the total bandwidth of online services exceeds or is lower than the configured waterline every 10 ms. Then the system determines the bandwidth limit for offline services based on whether the online bandwidth collected within each 10 ms is higher than the waterline.

##### Examples

- Set the online service waterline to 20 MB.

  ```shell
  # bwmcli -s waterline 20mb
  set waterline success
  ```

- Query the online service waterline.

  ```shell
  # bwmcli -p waterline
  waterline is 20971520(B)
  ```

#### Statistics

##### Commands and Functions

| Command Format           | Function              |
| ------------------- | ------------------ |
| **bwmcli -p stats** | Queries internal statistics.|

> Note:
>
> - **offline_target_bandwidth**: target bandwidth for offline services.
>
> - **online_pkts**: total number of online service packets after pod bandwidth management is enabled.
>
> - **offline_pkts**: total number of offline service packets after pod bandwidth management is enabled.
>
> - **online_rate**: current online service rate.
>
> - **offline_rate**: current offline service rate.

##### Examples

Query internal statistics.

```shell
# bwmcli -p stats
offline_target_bandwidth: 2097152
online_pkts: 2949775
offline_pkts: 0
online_rate: 602
offline_rate: 0
```

### Typical Use Case

To configure pod bandwidth management on a node, perform the following steps:

```shell
bwmcli -p devs #Query the pod bandwidth management status of the NICs in the system.
bwmcli -e eth0 # Enable pod bandwidth management for the eth0 NIC.
bwmcli -s /sys/fs/cgroup/net_cls/online 0 # Set the network priority of the online service pod to 0
bwmcli -s /sys/fs/cgroup/net_cls/offline -1 # Set the network priority of the offline service pod to -1.
bwmcli -s bandwidth 20mb,1gb # Set the bandwidth range for offline services.
bwmcli -s waterline 30mb # Set the waterline for online services.
```

### Constraints

1. Only the **root** user is allowed to run the bwmcli command.
2. Currently, this feature supports only two network QoS priorities: offline and online.
3. If the tc qdisc rules have been configured for a NIC, the network QoS function will fail to be enabled for the NIC.
4. After a NIC is removed and then inserted, the original QoS rules will be lost. In this case, you need to manually reconfigure the network QoS function.
5. When you run one command to enable or disable multiple NICs at the same time, if any NIC fails to be operated, operations on subsequent NICs will be stopped.
6. When SELinux is enabled in the environment, if the SELinux policy is not configured for the bwmcli program, some commands (such as setting or querying the waterline, bandwidth, and priority) may fail. You can confirm the failure in SELinux logs. To solve this problem, disable SELinux or configure the SELinux policy for the bwmcli program.
7. Upgrading the software package does not change the enabling status before the upgrade. Uninstalling the software package disables the function for all devices.
8. The NIC name can contain only digits, letters, hyphens (-), and underscores (_). NICs whose names contain other characters cannot be identified.
9. In actual scenarios, bandwidth limiting may cause protocol stack memory overstock. In this case, backpressure depends on transport-layer protocols. For protocols that do not have backpressure mechanisms, such as UDP, packet loss, ENOBUFS, and rate limiting deviation may occur.
10. After using bwmcli to enable the network QoS function of a certain network card, the tc command cannot be used to modify the tc rules of the network card. Otherwise, it may affect the network QoS function of the network card, leading to abnormal functionality.
