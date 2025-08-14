# oncn-bwm用户指南

## 简介

随着云计算、大数据、人工智能、5G、物联网等技术的迅速发展，数据中心的建设越来越重要。然而，数据中心的服务器资源利用率很低，造成了巨大的资源浪费。为了提高服务器资源利用率，oncn-bwm 应运而生。

oncn-bwm 是一款适用于在线、离线业务混合部署场景的 Pod 带宽管理工具，它会根据 QoS 分级对节点内的网络资源进行合理调度，保障在线业务服务体验的同时，大幅提升节点整体的网络带宽利用率。

oncn-bwm 工具支持如下功能：

- 使能/去除/查询 Pod 带宽管理
- 设置 Pod 网络优先级
- 设置离线业务带宽范围和在线业务水线
- 内部统计信息查询

## 安装

安装 oncn-bwm 工具需要操作系统为 openEuler 25.03，在配置了 openEuler yum 源的机器直接使用 yum 命令安装，参考命令如下：

```shell
# yum install oncn-bwm
```

此处介绍如何安装 oncn-bwm 工具。

### 环境要求

- 操作系统：openEuler 25.03

### 安装步骤

安装 oncn-bwm 工具的操作步骤如下：

1. 配置openEuler的yum源，直接使用yum命令安装

   ```shell
   yum install oncn-bwm
   ```

## 使用方法

oncn-bwm 工具提供了 `bwmcli` 命令行工具来使能 Pod 带宽管理或进行相关配置。`bwmcli` 命令的整体格式如下：

**bwmcli**  \< option(s) >

> 说明：
>
> 使用 `bwmcli` 命令需要 root 权限。
>
> 仅支持节点上出方向（报文从节点内发往其他节点）的 Pod 带宽管理。
>
> 已设置 tc qdisc 规则的网卡，不支持使能 Pod 带宽管理。
>
> 升级 oncn-bwm 包不会影响升级前的使能状态；卸载 oncn-bwm 包会关闭所有网卡的 Pod 带宽管理。

### 命令接口

#### Pod 带宽管理

**命令和功能**

| 命令格式                    | 功能                                                         |
| --------------------------- | ------------------------------------------------------------ |
| **bwmcli –e** \<网卡名称>    | 使能指定网卡的 Pod 带宽管理。 |
| **bwmcli -d** \<网卡名称>    | 去除指定网卡的 Pod 带宽管理。 |
| **bwmcli -p devs**          | 查询节点所有网卡的 Pod 带宽管理。 |

> 说明：
>
> - 不指定网卡名时，上述命令会对节点上的所有的网卡生效。
>
> - 执行 `bwmcli` 其他命令前需要开启 Pod 带宽管理。

**使用示例**

- 使能网卡 eth0 和 eth1 的 Pod 带宽管理

  ```shell
  # bwmcli –e eth0 –e eth1
  enable eth0 success
  enable eth1 success
  ```

- 取消网卡 eth0 和 eth1 的 Pod 带宽管理

  ```shell
  # bwmcli –d eth0 –d eth1
  disable eth0 success
  disable eth1 success
  ```

- 查询节点所有网卡的 Pod 带宽管理

  ```shell
  # bwmcli -p devs
  eth0            : enabled
  eth1            : disabled
  eth2            : disabled
  docker0         : disabled
  lo              : disabled
  ```

#### Pod 网络优先级

**命令和功能**

| 命令格式                                                     | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **bwmcli –s** *path* \<prio>                                  | 设置 Pod 网络优先级。其中 *path* 为 Pod 对应的 cgroup 路径， *prio* 为优先级。*path* 取相对路径或者绝对路径均可。 *prio* 缺省值为 0，可选值为 0 和 -1，0 标识为在线业务，-1 标识为离线业务。 |
| **bwmcli –p** *path*                                         | 查询 Pod 网络优先级。                                          |

> 说明：
>
> 支持在线或离线两种网络优先级，oncn-bwm 工具会按照网络优先级实时控制 Pod 的带宽，具体策略为：对于在线类型的 Pod ，不会限制其带宽；对于离线类型的 Pod ，会将其带宽限制在离线带宽范围内。

**使用示例**

- 设置 cgroup 路径为 /sys/fs/cgroup/net_cls/test_online 的 Pod 的优先级为 0

  ```shell
  # bwmcli -s /sys/fs/cgroup/net_cls/test_online 0
  set prio success
  ```

- 查询 cgroup 路径为 /sys/fs/cgroup/net_cls/test_online 的 Pod 的优先级

  ```shell
  # bwmcli -p /sys/fs/cgroup/net_cls/test_online
  0
  ```

#### 离线业务带宽范围

| 命令格式                           | 功能                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| **bwmcli –s bandwidth** `<low,high>` | 设置一个主机/虚拟机的离线带宽。其中 low 表示最低带宽，high 表示最高带宽，其单位可取值为 kb/mb/gb ，有效范围为 [1mb, 9999gb]。 |
| **bwmcli –p bandwidth**            | 查询设置一个主机/虚拟机的离线带宽。                          |

> 说明：
>
> - 一个主机上所有使能 Pod 带宽管理的网卡在实现内部被当成一个整体看待，也就是共享设置的在线业务水线和离线业务带宽范围。
>
> - 使用 `bwmcli` 设置 Pod 带宽对此节点上所有离线业务生效，所有离线业务的总带宽不能超过离线业务带宽范围。在线业务没有网络带宽限制。
>
> - 离线业务带宽范围与在线业务水线共同完成离线业务带宽限制，当在线业务带宽低于设置的水线时，离线业务允许使用设置的最高带宽；当在线业务带宽高于设置的水线时，离线业务允许使用设置的最低带宽。

**使用示例**

- 设置离线带宽范围在 30mb 到 100mb

  ```shell
  # bwmcli -s bandwidth 30mb,100mb
  set bandwidth success
  ```

- 查询离线带宽范围

  ```shell
  # bwmcli -p bandwidth
  bandwidth is 31457280(B),104857600(B)
  ```

#### 在线业务水线

**命令和功能**

| 命令格式                                       | 功能                                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **bwmcli –s waterline** \<val>                  | 设置一个主机/虚拟机的在线业务水线，其中 *val* 为水线值，单位可取值为 kb/mb/gb ，有效范围为 [20mb, 9999gb]。 |
| **bwmcli –p waterline**                        | 查询一个主机/虚拟机的在线业务水线。                          |

> 说明：
>
> - 当一个主机上所有在线业务的总带宽高于水线时，会限制离线业务可以使用的带宽，反之当一个主机上所有在线业务的总带宽低于水线时，会提高离线业务可以使用的带宽。
> - 判断在线业务的总带宽是否超过/低于设置的水线的时机：每 10 ms 判断一次，根据每个 10 ms 内统计的在线带宽是否高于水线来决定对离线业务采用的带宽限制。

**使用示例**

- 设置在线业务水线为 20mb

  ```shell
  # bwmcli -s waterline 20mb
  set waterline success
  ```

- 查询在线业务水线

  ```shell
  # bwmcli -p waterline
  waterline is 20971520(B)
  ```

#### 统计信息

**命令和功能**

| 命令格式            | 功能               |
| ------------------- | ------------------ |
| **bwmcli –p stats** | 查询内部统计信息。 |

> 说明：
>
> - offline_target_bandwidth 表示离线业务目标带宽
>
> - online_pkts 表示开启 Pod 带宽管理后在线业务总包数
>
> - offline_pkts 表示开启 Pod 带宽管理后离线业务总包数
>
> - online_rate 表示当前在线业务速率
>
> - offline_rate 表示当前离线业务速率

**使用示例**

查询内部统计信息

```shell
# bwmcli -p stats
offline_target_bandwidth: 2097152
online_pkts: 2949775
offline_pkts: 0
online_rate: 602
offline_rate: 0
```

### 典型使用案例

完整配置一个节点上的 Pod 带宽管理可以按照如下步骤顺序操作：

```shell
bwmcli -p devs # 查询系统当前网卡 Pod 带宽管理状态
bwmcli -e eth0 # 使能 eth0 的网卡 Pod 带宽管理
bwmcli -s /sys/fs/cgroup/net_cls/online 0 # 设置在线业务 Pod 的网络优先级为 0
bwmcli -s /sys/fs/cgroup/net_cls/offline -1 # 设置离线业务 Pod 的网络优先级为 -1
bwmcli -s bandwidth 20mb,1gb # 配置离线业务带宽范围
bwmcli -s waterline 30mb # 配置在线业务的水线
```
