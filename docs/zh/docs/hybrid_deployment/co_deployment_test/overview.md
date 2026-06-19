# 在离线混部测试套件

## 概述

为提升计算资源利用率，openEuler 支持在线业务与离线任务的混合部署（简称“混部”）。然而，混部带来的关键挑战在于量化离线任务对在线业务的性能干扰，从而确保该特性在生产环境中安全、可控地落地。
本测试套件可提供干扰率、时延敏感度等量化指标，并建立统一的对比基准，从而帮助用户客观评估混部的风险与成效，为业务部署提供决策依据；同时，它也补充了社区在混部测试方面的能力，有利于推动混部特性在生产环境中规模化落地。
本测试套件的测试范围主要涵盖 CPU、内存、I/O、网络四大混部场景。

本章节将重点介绍 openEuler 在离线混部测试套件的安装与部署方法，并以 openEuler 24.03-LTS-SP4 版本为例进行说明。

## 软硬件要求

### 硬件要求

* 当前仅支持 x86、aarch64 架构。
* 物理环境至少有2块硬盘，其中，/data目录要单独占用一块硬盘。
* 网络混部测试要求提供两台机器，不建议同一台机器回环测试。

### 软件要求

* 操作系统：openEuler 24.03-LTS-SP4。
* 内核：openEuler 24.03-LTS-SP4 版本内核。
* 因测试环境部署需要下载相关软件，要求环境支持链接网络。
* 环境需要安装Docker。

## 混部特性介绍

### 典型混部测试模型

| 测试模型     | online  | offline        | 相关内核技术                   |
| ------------ | ------- | -------------- | ------------------------------ |
| CPU混部模型  | SOFARPC | stress-ng(cpu) | 调度抢占压制、SMT驱离          |
| 内存混部模型 | MYSQL   | stress-ng(mem) | OOM分级回收、内存异步回收      |
| IO混部模型   | MYSQL   | fio            | IO InFlight限速 或 IO Cost限速 |
| 网络混部模型 | iperf3  | iperf3         | BWM带宽管控                    |

### CPU混部测试

#### CPU QOS隔离配置

1、cpu抢占压制
通过 cpu.qos_level 标识任务优先级：
* 在线任务：0
* 离线任务：-1
配置示例：

```bash
echo -1 > cpu.qos_level   # 设为离线
echo 0 > cpu.qos_level    # 设为在线
```

2、smt驱离
* 依赖cpu.qos_level配置，默认使能
* 关闭方式：内核启动参数cmdline配置添加nosmtexpell。

#### CPU测试套工具选取

* 在线业务：sofarpc-benchmark
特点：java工具，业务时延敏感，开源可修改

* 离线业务：stress-ng
特点：稳定模拟各种cpu利用率的任务

### 内存混部测试

#### 内存 QOS隔离配置

1.OOM分级查杀
* 配置使能

```bash
echo 1 > /proc/sys/vm/memcg_qos_enable
```
* 配置在离线标识(在线：0 , 离线：-1)

```bash
echo -1 > cpu.qos_level   # 设为离线
echo 0 > cpu.qos_level    # 设为在线
```

2.内存异步回收
内存超过memory.high*memory.high_async_ratio/100的时候开始异步回收，回收到memory.high*(memory.high_async_ratio–10)/100这个值结束。
* 配置memory.high                                //参考memory.limit_in_bytes、memory.max_usage_in_bytes配置，基于业务实际调试
* 配置memory.high_async_ratio                    //警戒水位线和安全水位线设置

#### 内存测试套工具选取

* 在线业务：mysql + sysbenchmark
特点：业务性能对内存使用敏感
* 离线业务：stress-ng
特点：稳定模拟持续消耗内存任务

### IO混部测试

#### IO QOS隔离配置

1.IO Cost方案
IO cost执行获取rbps/rseqiops/rrandiops/wbps/wseqiops/wrandiops参数会将整个/dev/sda刷一遍，因此测试需要单独隔离出一块盘
* cgroup根节点设置blkio.cost.qos

```bash
echo "8:0 enable=1 min=100.00 max=100.00" > blkio.cost.qos // 8:0指定块设备号maj:mi
```

* cgroup根节点设置blkio.cost.model

```bash
echo "8:0 ctrl=user model=linear rbps=1057334144 rseqiops=175363 rrandiops=180459 wbps=500824931 wseqiops=75499 wrandiops=69629" > blkio.cost.model
```

* 设置具体cgroup节点blkio.cost.weight
取值范围：[1, 10000]，默认值：100

```bash
echo "8:0 100" > blkio.cost.weight      //配置设备8:0 weight为100; 例如在线设置100，离线设置10。
```

* 设置进程到cgroup子节点cgroup.procs

```bash
echo 1053 > cgroup.procs
```            

*注：只在叶子节点绑定进程，在中间节点绑定不生效。两个cgroup组任务竞争状态下，限制才有效果。*

2.IO Inflight方案
IO inflight测试需要初步测试确定rlat/wlat（读写IO延时阈值）的基准值。
* 配置QOS控制策略

```bash
echo "8:0 enable=1 qos_enable=1 rlat=5000000 rpct=95 wlat=5000000 wpct=95 flags=0" > /sys/fs/cgroup/blkio/blkio.inf.qos
```

* 权重配置

```bash
echo "8:0 0" > /sys/fs/cgroup/blkio/$cgroup_path/blkio.inf.weight
```

#### IO测试套选取

* 在线业务：mysql + sysbenchmark
特点：业务性能对IO带宽敏感
* 离线业务：fio
特点：标准测试工具，稳定模拟持续消耗IO带宽任务

### 网络混部测试

#### 网络 QOS隔离配置

1、配置在离线标识（在线：0 ，离线：-1）

```bash
bwmcli -s /sys/fs/cgroup/net_cls/xxxx -1
```

2、限制离线网络带宽

```bash
bwmcli -s bandwidth 10MB,1GB //有在线业务10MB，无在线业务是1GB（根据实际网络带宽修改）
```

3、配置当在线达到20MB时，开始限制离线带宽10MB以内;若低于20MB则限制离线1GB以内

```bash
bwmcli -s waterline 20MB
```

4、使能网络带宽隔离配置

```bash
bwmcli -e eth0 -e eth1
```

5、去使能网络带宽隔离配置

```bash
bwmcli -d eth0 -d eth1
```

#### 网络测试套工具选取

* 在线业务：iperf
* 离线业务：iperf
特点：测试网络带宽的通用工具

## 混部测试结果示例

### CPU混部测试结果示例

* 原始数据

| Test Name | thrpt(ops/ms) | avgt(ms/op) | p99(ms/op) |
| ---- | ---- | ---- | ---- |
| Online Test Only | 0.423 | 37.765 | 47.645 |
| Direct deployment Test | 0.363 | 44.282 | 61.145 |
| Co-Deployment Test | 0.403 | 39.435 | 48.431 |

* 干扰率 (相比Online Test Only)

| Test Name | thrpt | avgt | p99 |
| ---- | ---- | ---- | ---- |
| Direct deployment Test | 14.18% | 17.26% | 28.33% |
| Co-Deployment Test | 4.73% | 4.42% | 1.65% |

结论：混部CPU隔离后，在线业务QPS干扰率从14.18%下降到4.73%，平均时延干扰从17.26%下降到4.42%，P99干扰率从28.33%下降到1.65%。

### 内存混部测试结果示例

* 原始数据

| Test Name | transactions | avg(ms) | p95(ms) |
| ---- | ---- | ---- | ---- |
| Online Test Only | 65613 | 292.70 | 404.61 |
| Direct deployment Test | 62780 | 305.89 | 511.33 |
| Co-Deployment Test | 66969 | 286.83 | 427.07 |

* 干扰率 (相比Online Test Only)

| Test Name | transactions | avg | p95 |
| ---- | ---- | ---- | ---- |
| Direct deployment Test | 4.32% | 4.51% | 26.38% |
| Co-Deployment Test | -2.07% | -2.01% | 5.55% |

公式: 干扰率 = (Online - Test) / Online x 100%

* 结论：混部内存隔离后，QPS干扰率从4.32%下降到-2.07%，平均时延干扰率从4.51%下降到-2.01%，P95时延干扰率从26.38%下降到5.55%。

### IO混部测试结果示例

* 原始数据

| Test Name | transactions | avg(ms) | p95(ms) |
| ---- | ---- | ---- | ---- |
| Online Test Only | 5454 | 176.17 | 282.25 |
| Direct deployment Test | 1248 | 770.72 | 1149.76 |
| Co-Deployment Test | 4189 | 229.35 | 376.49 |

* 干扰率(相比Online Test Only)

| Test Name | transactions | avg | p95 |
| ---- | ---- | ---- | ---- |
| Direct deployment Test | 77.12% | 337.49% | 307.36% |
| Co-Deployment Test | 23.19% | 30.19% | 33.39% |

公式: 干扰率 = (Online - Test) / Online x 100%

* 结论：混部IO隔离后，在线业务QOS干扰率从77.12%下降到23.19%，平均时延干扰率从337.49%下降到30.19%，P95时延干扰率从307.36%下降到33.39%。

### 网络混部测试结果示例

| Test Scenario | Network Bandwidth (Gbits/sec) | Interference Rate |
| ------------- | ----------------------------- | ----------------- |
| Baseline      | 0.93                          | -                 |
| Direct Deploy | 0.42                          | 54.84%            |
| Co-deployment | 0.87                          | 6.45%             |

* 结论：混部网络隔离后，在线干扰率从54.84%下降到6.45%。

## SOFARPC 介绍

### 概述

SOFARPC（Scalable Open Financial Architecture Remote Procedure Call）是蚂蚁集团自研的高性能、高可扩展性、生产级 Java RPC 框架，历经十年金融级生产环境验证。作为 SOFAStack 技术栈的核心组件之一，SOFARPC 为分布式微服务提供高效、稳定的服务间远程调用能力，广泛应用于支付、交易、风控等对时延高度敏感的金融业务场景。

本测试套件选择 SOFARPC 作为 CPU 混部场景的在线业务负载，旨在模拟真实微服务调用中 CPU 密集、时延敏感的工作负载特征。

### 项目地址

Gitee: [sofa-rpc](https://gitee.com/sofastack/sofa-rpc/)

### 核心特性

* **多协议支持**：支持 Bolt（蚂蚁自研高性能二进制协议）、Dubbo、REST、HTTP/2 等主流通信协议，可灵活适配不同业务场景。
* **丰富的序列化方案**：支持 Hessian2（默认）、Protobuf、JSON、SofaFury 等多种序列化协议，其中 SofaFury 为蚂蚁自研极致序列化方案。
* **完善的服务治理**：内置负载均衡、容错机制（失败重试、熔断降级）、流量控制、动态路由等能力，保障服务调用的高可用与稳定性。
* **高可扩展性**：采用微内核 + SPI 扩展机制，支持协议扩展、序列化扩展、过滤器链扩展等，各扩展点内部实现与第三方实现绝对平等。
* **分布式链路追踪**：集成 SOFATracer，支持基于 OpenTracing 规范的分布式链路追踪，可透明埋点并上报至 Zipkin、Jaeger、SkyWalking 等后端。

### 架构与性能特征

SOFARPC 采用经典的服务注册/发现/调用架构，核心组件包括服务注册中心（Registry）、服务提供者（Service）和服务消费者（Reference）。底层基于 Netty 异步事件驱动网络框架，通过 TCP 长连接复用、Reactor 多线程模型实现高性能通信。

典型性能指标（Bolt 协议，50 并发客户端，4C8G 虚拟机）：

| 请求/响应大小 | TPS | 平均 RT(ms) |
| --- | --- | --- |
| 100byte / 100byte | ~45,000 | 1.1 |
| 1KB / 1KB | ~41,000 | 1.2 |
| 5KB / 5KB | ~32,000 | 1.6 |

*注：以上为官方压测参考数据，实际性能取决于硬件环境和业务复杂度。*

### 作为 CPU 混部在线负载的选型依据

| 特征 | 说明 |
| --- | --- |
| Java 应用 | JVM 运行时对 CPU 调度抢占高度敏感，CPU 资源被离线任务抢占时，JVM GC、JIT 编译、业务线程调度均受影响 |
| RPC 时延敏感 | 微服务调用场景要求 P99 时延可控，CPU 争抢直接导致请求排队、时延抖动放大 |
| 多线程模型 | 服务端包含 IO 线程、业务线程池、心跳线程等多个线程组，CPU 混部时线程调度干扰特征明显 |
| 生产级负载 | 相比纯 CPU 压测工具（如 benchmark 空转），SOFARPC 更贴近真实在线业务的 CPU 使用模式 |
| 开源可修改 | 社区可获取、可定制，便于根据测试需求调整业务复杂度、调用频率、数据大小等参数 |

### Benchmark 套件说明

本测试套件采用 SOFARPC Benchmark 进行性能压测，模拟 RPC 调用，采集 TPS（吞吐量）、平均 RT（响应时间）、P99 时延等关键指标，并与在线独占场景（Online Test Only）的基线数据进行对比，从而计算混部干扰率。具体计算公式如下：

```text
干扰率 = (Online 指标 - 混部指标) / Online 指标 × 100%
```

通过 CPU QoS 隔离（调度抢占压制、SMT 驱离）前后干扰率的对比，量化评估混部特性对在线业务的保护效果。

## 缩略语清单

| 缩略语      | 英文全名                    | 中文解释                                                     |
| ----------- | --------------------------- | ------------------------------------------------------------ |
| SMT         | Simultaneous Multithreading | 同步多线程（超线程）：指一个物理 CPU 核心内，并行跑多个逻辑线程，共享核心执行单元、Cache 等硬件资源。 |
| OOM         | Out of Memory               | 内存溢出：系统可用内存、Swap 均不足，内核触发内存回收或进程杀死机制的状态。 |
| IO Cost     | Input/Output Cost           | I/O 成本：Linux cgroup 块设备 I/O 管控机制，基于权重与 IO 耗时做动态限速，保障在线业务 I/O 时延，约束离线负载。 |
| IO InFlight | Input/Output InFlight       | 在途 I/O/ 飞行中 I/O：内核块层统计当前已下发但未完成的 I/O 请求数（inflight）；限速通过控制该并发上限，防止离线 I/O 占满队列、阻塞在线业务，是 openEuler 混部 QoS 的 I/O 并发管控能力。 |
| BWM         | Bandwidth Management        | 带宽管控：基于 eBPF+EDT 实现的网络 QoS 能力，区分在线 / 离线优先级，在线流量可抢占带宽，保障混部场景网络质量。 |
| RPC         | Remote Procedure Call       | 远程过程调用：分布式系统中节点间通信的基础技术，使调用远程服务如同调用本地方法一样透明。 |
| SOFARPC     | Scalable Open Financial Architecture RPC | 蚂蚁集团自研的高性能 Java RPC 框架，支持多协议、多序列化、分布式链路追踪，广泛应用于金融级微服务场景。本测试套 CPU 混部场景的在线业务负载。 |

---
