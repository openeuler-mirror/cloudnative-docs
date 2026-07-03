# Hybrid Deployment Test Suite

## Overview

To maximize computing resource utilization, openEuler supports the co-location of online tasks and offline tasks (hereinafter referred to as "hybrid deployment"). However, a critical challenge of hybrid deployment lies in quantifying the performance interference caused by offline tasks on online tasks, which is essential to ensure a safe and controllable rollout of this feature in production environments.

This test suite provides quantitative metrics such as interference rates and latency sensitivity, and establishes a unified benchmark. It helps you objectively evaluate the risks and effectiveness of hybrid deployment, providing a solid basis for decision-making in service deployment. Furthermore, it enhances the community's capabilities in hybrid deployment testing, facilitating the large-scale adoption of hybrid deployment features in production environments.

The scope of this test suite primarily covers four major hybrid deployment scenarios: CPU, memory, I/O, and network.

This section focuses on the installation and deployment methods of the hybrid deployment test suite for online and offline tasks on openEuler, using openEuler 24.03 LTS SP4 as an example.

## Hardware and Software Requirements

### Hardware and Software Requirements

* Currently, only x86 and AArch64 architectures are supported.
* The physical environment must have at least two drives, with the `/data` directory dedicated to one separate drive.
* Network hybrid deployment testing requires two machines. Loopback testing on a single machine is not recommended.

### Software Requirements

* OS: openEuler 24.03 LTS SP4.
* Kernel: openEuler 24.03 LTS SP4 kernel.
* Network connectivity is required to download relevant software during test environment deployment.
* Docker must be installed in the environment.

## Hybrid Deployment Features

### Typical Hybrid Deployment Test Models

| Test Model     | Online  | Offline        | Related Kernel Technologies                   |
| ------------ | ------- | -------------- | ------------------------------ |
| CPU hybrid deployment | SOFARPC | stress-ng(cpu) | Scheduling preemption suppression, SMT eviction          |
| Memory hybrid deployment | MySQL   | stress-ng(mem) | Hierarchical OOM reclamation, asynchronous memory reclamation      |
| I/O hybrid deployment   | MySQL   | fio            | I/O InFlight or I/O Cost rate limiting |
| Network hybrid deployment | iperf3  | iperf3         | Bandwidth management (BWM)                    |

### CPU Hybrid Deployment Testing

#### CPU QoS Isolation Configuration

1. CPU preemption suppression

    Task priority is identified using `cpu.qos_level`:

    * Online tasks: `0`
    * Offline tasks: `-1`

    Configuration example:

    ```bash
    echo -1 > cpu.qos_level   # Set as offline
    echo 0 > cpu.qos_level    # Set as online
    ```

2. SMT eviction

    * This feature relies on the `cpu.qos_level` configuration and is enabled by default.
    * To disable it, add `nosmtexpell` to the kernel boot parameters (`cmdline`).

#### CPU Test Suite Tool Selection

* Online task: sofarpc-benchmark

    Characteristics: A Java-based tool, latency-sensitive, open-source, and customizable.

* Offline task: stress-ng

    Characteristics: Reliably simulates tasks with various CPU utilization rates.

### Memory Hybrid Deployment Testing

#### Memory QoS Isolation Configuration

1. Hierarchical OOM omission/termination

    * Enable configuration.

        ```bash
        echo 1 > /proc/sys/vm/memcg_qos_enable
        ```

    * Configure online/offline identifier (online: `0`, offline: `-1`).

        ```bash
        echo -1 > cpu.qos_level   # Set as offline
        echo 0 > cpu.qos_level    # Set as online
        ```

2. Asynchronous memory reclamation

    Asynchronous memory reclamation is triggered when memory usage exceeds `memory.high * memory.high_async_ratio / 100`, and stops when usage drops to `memory.high * (memory.high_async_ratio - 10) / 100`.

    * Configure `memory.high`: Configure this based on actual service debugging, with reference to `memory.limit_in_bytes` and `memory.max_usage_in_bytes`.

    * Configure `memory.high_async_ratio`: Set the warning and safe watermarks.

#### Memory Test Suite Tool Selection

* Online task: MySQL + sysbench

    Characteristics: Service performance is highly sensitive to memory usage.

* Offline task: stress-ng

    Characteristics: Reliably simulates tasks with continuous memory consumption.

### I/O Hybrid Deployment Testing

#### I/O QoS Isolation Configuration

1. I/O Cost solution

    Obtaining the `rbps`, `rseqiops`, `rrandiops`, `wbps`, `wseqiops`, and `wrandiops` parameters for I/O Cost will sweep the entire `/dev/sda` drive. Therefore, the test requires a separate, isolated drive.

    * Configure `blkio.cost.qos` at the cgroup root node.

        ```bash
        echo "8:0 enable=1 min=100.00 max=100.00" > blkio.cost.qos // 8:0 specifies the block device major:minor numbers.
        ```

    * Configure `blkio.cost.model` at the cgroup root node.

        ```bash
        echo "8:0 ctrl=user model=linear rbps=1057334144 rseqiops=175363 rrandiops=180459 wbps=500824931 wseqiops=75499 wrandiops=69629" > blkio.cost.model
        ```

        The parameters such as `rbps`, `rseqiops`, `rrandiops`, `wbps`, `wseqiops`, and `wrandiops` can be obtained using the following command:

        ```bash
        python iscost_coef_gen.py --testdev /dev/sdx
        ```

        Note: The `iscost_coef_gen.py` script is sourced from the openEuler-6.6 kernel source code, located at `tools/cgroup/iscost_coef_gen.py`. In addition, replace the device path in the command (for example, `sdm`) based on the actual drive name queried via `lsblk`.

    * Configure `blkio.cost.weight` for the specific cgroup node. The value ranges from 1 to 10000, with a default value of `100`.

        ```bash
        echo "8:0 100" > blkio.cost.weight      //Configure the weight for device 8:0. For example, set it to 100 for online tasks and 10 for offline tasks.
        ```

    * Configure `cgroup.procs` to assign processes to the cgroup child node.

        ```bash
        echo 1053 > cgroup.procs
        ```

        Note: Processes should only be bound to leaf nodes, as binding them to intermediate nodes will not take effect. The limits apply only when tasks from two cgroup groups are in a state of resource contention.

2. I/O InFlight solution

    The I/O InFlight test requires an initial test to determine the baseline values for `rlat` and `wlat` (read/write I/O latency thresholds).

    * Configure the QoS control policy.

        ```bash
        echo "8:0 enable=1 qos_enable=1 rlat=5000000 rpct=95 wlat=5000000 wpct=95 flags=0" > /sys/fs/cgroup/blkio/blkio.inf.qos
        ```

    * Configure the weight.

        ```bash
        echo "8:0 0" > /sys/fs/cgroup/blkio/$cgroup_path/blkio.inf.weight
        ```

#### I/O Test Suite Tool Selection

* Online task: MySQL + sysbench

    Characteristics: Service performance is highly sensitive to I/O bandwidth.

* Offline task: fio

    Characteristics: A standard testing tool that reliably simulates tasks with continuous I/O bandwidth consumption.

### Network Hybrid Deployment Testing

#### Network QoS Isolation Configuration

1. Configure the online/offline identifier (online: `0`, offline: `-1`).

    ```bash
    bwmcli -s /sys/fs/cgroup/net_cls/xxxx -1
    ```

2. Limit offline network bandwidth.

    ```bash
    bwmcli -s bandwidth 10MB,1GB // Set to 10 MB/s when online tasks are active, and 1 GB/s when no online task is active (modify based on actual network bandwidth).
    ```

3. Configure the policy to limit offline bandwidth to within 10 MB/s when online bandwidth reaches 20 MB/s. If online bandwidth is below 20 MB/s, limit offline bandwidth to within 1 GB/s.

    ```bash
    bwmcli -s waterline 20MB
    ```

4. Enable network bandwidth isolation configuration.

    ```bash
    bwmcli -e eth0 -e eth1
    ```

5. Disable network bandwidth isolation configuration.

    ```bash
    bwmcli -d eth0 -d eth1
    ```

#### Network Test Suite Tool Selection

* Online task: iperf

* Offline task: iperf

Characteristics: A generic tool for te sting network bandwidth.

## Hybrid Deployment Test Result Examples

### CPU Hybrid Deployment Test Result Example

* Raw data

    | Test Name | thrpt(ops/ms) | avgt(ms/op) | p99(ms/op) |
    | ---- | ---- | ---- | ---- |
    | Online Test Only | 0.423 | 37.765 | 47.645 |
    | Direct Deployment Test | 0.363 | 44.282 | 61.145 |
    | Co-Deployment Test | 0.403 | 39.435 | 48.431 |

* Interference rate (compared to Online Test Only)

    | Test Name | thrpt | avgt | p99 |
    | ---- | ---- | ---- | ---- |
    | Direct Deployment Test | 14.18% | 17.26% | 28.33% |
    | Co-Deployment Test | 4.73% | 4.42% | 1.65% |

Conclusion: After implementing CPU isolation for hybrid deployment, the QPS interference rate of online tasks decreased from 14.18% to 4.73%. Concurrently, the average latency interference rate dropped from 17.26% to 4.42%, and the P99 latency interference rate declined from 28.33% to 1.65%.

### Memory Hybrid Deployment Test Result Example

* Raw data

    | Test Name | Transactions | avg(ms) | p95(ms) |
    | ---- | ---- | ---- | ---- |
    | Online Test Only | 173212 | 560.46 | 780.61 |
    | Direct Deployment Test | 126385 | 1799.68 | 2711.56 |
    | Co-Deployment Test | 169118 | 582.35 | 801.72 |

* Interference rate (compared to Online Test Only)

    | Test Name | Transactions | avg | p95 |
    | ---- | ---- | ---- | ---- |
    | Direct Deployment Test | 27.03% | 221.07% | 247.36% |
    | Co-Deployment Test | 2.36% | 3.91% | 2.70% |

Formula: Interference rate = (Online - Test)/Online x 100%

* Conclusion: After implementing memory isolation for hybrid deployment, the QPS interference rate decreased from 27.03% to 2.36%. Concurrently, the average latency interference rate dropped from 221.07% to 3.91%, and the P95 latency interference rate declined from 247.36% to 2.70%.

### I/O Hybrid Deployment Test Result Example

* Raw data

    | Test Name | Transactions | avg(ms) | p95(ms) |
    | ---- | ---- | ---- | ---- |
    | Online Test Only | 5454 | 176.17 | 282.25 |
    | Direct Deployment Test | 1248 | 770.72 | 1149.76 |
    | Co-Deployment Test | 4189 | 229.35 | 376.49 |

* Interference rate (compared to Online Test Only)

    | Test Name | Transactions | avg | p95 |
    | ---- | ---- | ---- | ---- |
    | Direct Deployment Test | 77.12% | 337.49% | 307.36% |
    | Co-Deployment Test | 23.19% | 30.19% | 33.39% |

Formula: Interference rate = (Online - Test)/Online x 100%

*Conclusion: After implementing I/O isolation for hybrid deployment, the QoS interference rate of online tasks decreased from 77.12% to 23.19%. Concurrently, the average latency interference rate dropped from 337.49% to 30.19%, and the P95 latency interference rate declined from 307.36% to 33.39%.

### Network Hybrid Deployment Test Result Example

| Test Scenario | Network Bandwidth (Gbits/sec) | Interference Rate |
| ------------- | ----------------------------- | ----------------- |
| Baseline      | 0.93                          | -                 |
| Direct Deploy | 0.42                          | 54.84%            |
| Co-deployment | 0.87                          | 6.45%             |

* Conclusion: After implementing network isolation for hybrid deployment, the interference rate of online tasks decreased from 54.84% to 6.45%.

## SOFARPC

### Overview

Scalable Open Financial Architecture Remote Procedure Call (SOFARPC) is a high-performance, highly extensible, and production-ready Java RPC framework developed by the Ant Group. It has been validated in financial-grade production environments for over a decade. As one of the core components of the SOFAStack ecosystem, SOFARPC provides efficient and stable inter-service remote invocation capabilities for distributed microservices. It is widely used in latency-sensitive financial scenarios such as payment, transaction, and risk control.

This test suite selects SOFARPC as the online task workload for CPU hybrid deployment testing, aiming to simulate the CPU-intensive and latency-sensitive workload characteristics found in real-world microservice invocations.

### Project Repository

Gitee: [sofa-rpc](https://gitee.com/sofastack/sofa-rpc/)

### Features

* **Multi-protocol support**: Supports mainstream communication protocols such as Bolt (Ant Group's self-developed high-performance binary protocol), Dubbo, REST, and HTTP/2, offering flexible adaptation to various business scenarios.
* **Extensive serialization schemes**: Supports multiple serialization protocols including Hessian2 (default), Protobuf, JSON, and SofaFury (Ant Group's self-developed ultra-high-performance serialization solution).
* **Comprehensive service governance**: Provides built-in capabilities such as load balancing, fault tolerance (failover, circuit breaking, and degradation), traffic control, and dynamic routing to guarantee the high availability and stability of service calls.
* **High extensibility**: Adopts a microkernel + Service Provider Interface (SPI) extension mechanism, supporting protocol, serialization, and filter chain extensions. Internal implementations are treating on an absolutely equal footing with third-party extensions.
* **Distributed link tracing**: Integrates with SOFATracer to support OpenTracing-compliant distributed tracing, enabling transparent instrumentation and reporting to backends like Zipkin, Jaeger, and SkyWalking.

### Architecture and Performance Characteristics

SOFARPC employs a classic service registration, discovery, and invocation architecture. Its core components include the Registry, Service, and Reference. The underlying layer is built upon the Netty asynchronous event-driven network framework, achieving high-performance communication through TCP long-connection multiplexing and the Reactor multi-threading model.

Typical performance metrics (Bolt protocol, 50 concurrent clients, 4C8G VM):

| Request/Response Size | TPS | Average RT (ms) |
| --- | --- | --- |
| 100 byte/100 byte | ~45,000 | 1.1 |
| 1 KB/1 KB | ~41,000 | 1.2 |
| 5 KB/5 KB | ~32,000 | 1.6 |

*Note: The above data are official benchmark reference values. Actual performance depends on the hardware environment and business complexity.*

### Selection Basis as an Online Workload for CPU Hybrid Deployment

| Feature | Description |
| --- | --- |
| Java application | The JVM runtime is highly sensitive to CPU scheduling and preemption. When CPU resources are preempted by offline tasks, JVM GC, JIT compilation, and application thread scheduling are all affected. |
| Latency-sensitive RPC | Microservice invocation scenarios require controllable P99 latency. CPU contention directly leads to request queueing and amplified latency jitter. |
| Multi-threading model | The server-side comprises multiple thread groups, including I/O threads, business thread pools, and heartbeat threads, which exhibits distinct thread scheduling interference characteristics under hybrid deployment. |
| Production-grade workload | Compared to pure CPU benchmarking tools (such as idle loops), SOFARPC aligns more closely with the actual CPU utilization patterns of real-world online tasks. |
| Open-source & customizable | Accessible and customizable within the community, making it easy to adjust parameters such as business complexity, invocation frequency, and data size based on testing requirements. |

### Benchmark Suite Description

This test suite utilizes the SOFARPC Benchmark to conduct performance pressure testing, simulating RPC calls and collecting critical metrics such as TPS (throughput), Average RT (response time), and P99 latency. These metrics are compared against the baseline data obtained from the isolated scenario (Online Test Only) to calculate the hybrid deployment interference rate. The specific formula is as follows:

```text
Interference rate = (Online metric - Hybrid deployment metric)/Online metric × 100%
```

By comparing the interference rates before and after implementing CPU QoS isolation (scheduling preemption suppression and SMT eviction), you can quantitatively evaluate the protective effects of hybrid deployment features on online tasks.

## Acronyms and Abbreviations

| Acronym/Abbreviation | Full Name | Description|
| ----------- | --------------------------- | ------------------------------------------------------------ |
| SMT         | Simultaneous Multithreading | Simultaneous Multithreading (Hyper-threading) refers to running multiple logical threads in parallel within a single physical CPU core, sharing hardware resources such as core execution units and caches. |
| OOM         | Out of Memory               | A state where both system available memory and swap space are exhausted, triggering the kernel's memory reclamation or process termination (OOM killer) mechanism. |
| IO Cost     | Input/Output Cost           | A Linux cgroup block device I/O control mechanism that performs dynamic rate limiting based on weights and I/O execution time to guarantee I/O latency for online tasks while constraining offline workloads. |
| I/O InFlight | Input/Output InFlight       | The number of current I/O requests that have been issued but not yet completed (in-flight), counted by the kernel block layer. Rate limiting controls this concurrency ceiling to prevent offline I/Os from saturating queues and blocking online tasks. This is the I/O concurrency management capability of openEuler hybrid deployment QoS. |
| BWM         | Bandwidth Management        | A network QoS capability implemented based on eBPF and EDT. It distinguishes between online and offline priorities, allowing online traffic to preempt bandwidth to guarantee network quality in hybrid deployment scenarios. |
| RPC         | Remote Procedure Call       | A foundational technology for inter-node communication in distributed systems, making remote service invocations as transparent as calling local methods. |
| SOFARPC     | Scalable Open Financial Architecture RPC | A high-performance Java RPC framework developed by Ant Group. It supports multiple protocols, multiple serialization schemes, and distributed tracing, and is widely used in financial-grade microservice scenarios. It serves as the online task workload for the CPU hybrid deployment scenario in this test suite. |

---
