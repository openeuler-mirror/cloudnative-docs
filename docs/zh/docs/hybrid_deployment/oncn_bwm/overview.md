# oncn-bwm用户指南

## 简介

随着云计算、大数据、人工智能、5G、物联网等技术的迅速发展，数据中心的建设越来越重要。然而，数据中心的服务器资源利用率很低，造成了巨大的资源浪费。为了提高服务器资源利用率，oncn-bwm应运而生。

oncn-bwm是一款适用于在、离线业务混合部署场景的Pod带宽管理工具，它会根据QoS分级对节点内的网络资源进行合理调度，保障在线业务服务体验的同时，大幅提升节点整体的网络带宽利用率。

oncn-bwm工具支持如下功能：

- 使能/去除/查询Pod带宽管理
- 设置Pod网络优先级
- 设置离线业务带宽范围和在线业务水线
- 内部统计信息查询

## 安装

### 环境要求

操作系统为openEuler-24.03-LTS，且配置了openEuler-24.03-LTS的yum源。

### 安装步骤

使用以下命令直接安装：

```shell
yum install oncn-bwm
```

## 使用方法

oncn-bwm工具提供了`bwmcli`命令行工具来使能Pod带宽管理或进行相关配置。`bwmcli`命令的整体格式如下：

**bwmcli**  \< option(s) >

> 说明：
>
> 使用`bwmcli`命令需要root权限。
>
> 仅支持节点上出方向（报文从节点内发往其他节点）的Pod带宽管理。
>
> 已设置tc qdisc规则的网卡，不支持使能Pod带宽管理。
>
> 升级oncn-bwm包不会影响升级前的使能状态；卸载oncn-bwm包会关闭所有网卡的Pod带宽管理。

### 命令接口

#### Pod带宽管理

##### 命令和功能

| 命令格式                    | 功能                                                         |
| --------------------------- | ------------------------------------------------------------ |
| **bwmcli -e** \<网卡名称>    | 使能指定网卡的Pod带宽管理。 |
| **bwmcli -d** \<网卡名称>    | 去除指定网卡的Pod带宽管理。 |
| **bwmcli -p devs**          | 查询节点所有网卡的Pod带宽管理。 |

> 说明：
>
> - 不指定网卡名时，上述命令会对节点上的所有的网卡生效。
>
> - 执行 `bwmcli` 其他命令前需要开启Pod带宽管理。

##### 使用示例

- 使能网卡eth0和eth1的Pod带宽管理

  ```shell
  # bwmcli -e eth0 -e eth1
  enable eth0 success
  enable eth1 success
  ```

- 取消网卡eth0和eth1的Pod带宽管理

  ```shell
  # bwmcli -d eth0 -d eth1
  disable eth0 success
  disable eth1 success
  ```

- 查询节点所有网卡的Pod带宽管理

  ```shell
  # bwmcli -p devs
  eth0            : enabled
  eth1            : disabled
  eth2            : disabled
  docker0         : disabled
  lo              : disabled
  ```

#### Pod网络优先级

##### 命令和功能

| 命令格式                                                     | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **bwmcli -s** path \<prio>                                | 设置Pod网络优先级。其中*path*为Pod对应的cgroup路径，*prio*为优先级。*path*取相对路径或者绝对路径均可。 *prio*默认值为0，可选值为0和-1，0标识为在线业务，-1标识为离线业务。 |
| **bwmcli -p** *path*                                         | 查询Pod网络优先级。                                          |

> 说明：
>
> 支持在线或离线两种网络优先级，oncn-bwm工具会按照网络优先级实时控制Pod的带宽，具体策略为：对于在线类型的Pod，不会限制其带宽；对于离线类型的Pod，会将其带宽限制在离线带宽范围内。

##### 使用示例

- 设置cgroup路径为/sys/fs/cgroup/net_cls/test_online的Pod的优先级为0

  ```shell
  # bwmcli -s /sys/fs/cgroup/net_cls/test_online 0
  set prio success
  ```

- 查询cgroup路径为/sys/fs/cgroup/net_cls/test_online的Pod的优先级

  ```shell
  # bwmcli -p /sys/fs/cgroup/net_cls/test_online
  0
  ```

#### 离线业务带宽范围

| 命令格式                             | 功能                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| **bwmcli -s bandwidth** \<low,high> | 设置一个主机/虚拟机的离线带宽。其中*low*表示最低带宽，*high*表示最高带宽，其单位可取值为kb/mb/gb，有效范围为[1mb, 9999gb]。|
| **bwmcli -p bandwidth**              | 查询设置一个主机/虚拟机的离线带宽。                          |

> 说明：
>
> - 一个主机上所有使能Pod带宽管理的网卡在实现内部被当成一个整体看待，也就是共享设置的在线业务水线和离线业务带宽范围。
>
> - 使用 `bwmcli` 设置Pod带宽对此节点上所有离线业务生效，所有离线业务的总带宽不能超过离线业务带宽范围。在线业务没有网络带宽限制。
>
> - 离线业务带宽范围与在线业务水线共同完成离线业务带宽限制，当在线业务带宽低于设置的水线时：离线业务允许使用设置的最高带宽；当在线业务带宽高于设置的水线时，离线业务允许使用设置的最低带宽。

##### 使用示例

- 设置离线带宽范围在30mb到100mb

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

##### 命令和功能

| 命令格式                                       | 功能                                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **bwmcli -s waterline** \<val>                | 设置一个主机/虚拟机的在线业务水线，其中*val*为水线值，单位可取值为kb/mb/gb ，有效范围为[20mb, 9999gb]。 |
| **bwmcli -p waterline**                        | 查询一个主机/虚拟机的在线业务水线。                          |

> 说明：
>
> - 当一个主机上所有在线业务的总带宽高于水线时，会限制离线业务可以使用的带宽，反之当一个主机上所有在线业务的总带宽低于水线时，会提高离线业务可以使用的带宽。
> - 判断在线业务的总带宽是否超过/低于设置的水线的时机：每10ms判断一次，根据每个10ms内统计的在线带宽是否高于水线来决定对离线业务采用的带宽限制。

##### 使用示例

- 设置在线业务水线为20mb

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

##### 命令和功能

| 命令格式            | 功能               |
| ------------------- | ------------------ |
| **bwmcli -p stats** | 查询内部统计信息。 |

> 说明：
>
> - offline_target_bandwidth 表示离线业务目标带宽
>
> - online_pkts 表示开启Pod带宽管理后在线业务总包数
>
> - offline_pkts 表示开启Pod带宽管理后离线业务总包数
>
> - online_rate 表示当前在线业务速率
>
> - offline_rate 表示当前离线业务速率

##### 使用示例

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

完整配置一个节点上的Pod带宽管理可以按照如下步骤顺序操作：

```shell
bwmcli -p devs # 查询系统当前网卡Pod带宽管理状态
bwmcli -e eth0 # 使能eth0的网卡Pod带宽管理
bwmcli -s /sys/fs/cgroup/net_cls/online 0 # 设置在线业务Pod的网络优先级为0
bwmcli -s /sys/fs/cgroup/net_cls/offline -1 # 设置离线业务Pod的网络优先级为-1
bwmcli -s bandwidth 20mb,1gb # 配置离线业务带宽范围
bwmcli -s waterline 30mb # 配置在线业务的水线
```

### 约束限制

1. 仅允许root用户执行bwmcli命令行。
2. 本特性当前仅支持设置两档网络QoS优先级：离线和在线。
3. 某个网卡上已经设置过tc qdisc规则的情况下，对此网卡使能网络QoS功能会失败。
4. 网卡被插拔重新恢复后，原来设置的QoS规则会丢失，需要手动重新配置网络QoS功能。
5. 用一条命令同时使能/去使能多张网卡的时候，如果中间有网卡执行失败，则终止对后面网卡的执行。
6. 环境上开启SELinux的情况下，未对bwmcli程序配置SELinux策略可能导致部分命令（例如水线，带宽，优先级的设置或查询）失败，可在SELinux日志中确认。此情况可以通过关闭SELinux或对bwmcli程序配置SELinux策略解决。
7. 升级包不会影响升级前的使能状态，卸载包会关闭对所有设备的使能。
8. 网卡名仅支持数字、英文字母、中划线“-” 和下划线“_”这四类字符类型，包含其他字符类型的网卡不被识别。
9. 实际使用过程中，带宽限速有可能造成协议栈内存积压，此时依赖传输层协议自行反压，对于udp等无反压机制的协议场景，可能出现丢包、ENOBUFS、限速有偏差等问题。
10. 使用bwmcli使能某个网卡的网络Qos功能后，不能再使用tc命令修改该网卡的tc规则，否则可能会影响该网卡的网络Qos功能，导致功能异常。
