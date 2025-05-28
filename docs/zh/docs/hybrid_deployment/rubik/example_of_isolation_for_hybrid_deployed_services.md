# 混部隔离示例

## 环境准备

查看内核是否支持混部隔离功能。

```bash
# 查看/boot/config-<kernel version>系统配置是否开启混部隔离功能
# 若 CONFIG_QOS_SCHED=y 则说明使能了混部隔离功能，例如：
cat /boot/config-5.10.0-60.18.0.50.oe2203.x86_64 | grep CONFIG_QOS
CONFIG_QOS_SCHED=y
```

安装 docker 容器引擎。

```bash
yum install -y docker-engine
docker version
# 如下为 docker version 显示结果
Client:
 Version:           18.09.0
 EulerVersion:      18.09.0.325
 API version:       1.39
 Go version:        go1.17.3
 Git commit:        ce4ae23
 Built:             Mon Jun 26 12:56:54 2023
 OS/Arch:           linux/arm64
 Experimental:      false

Server:
 Engine:
  Version:          18.09.0
  EulerVersion:     18.09.0.325
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.17.3
  Git commit:       ce4ae23
  Built:            Mon Jun 26 12:56:10 2023
  OS/Arch:          linux/arm64
  Experimental:     false
```

## 混部业务

### 在线业务 (clickhouse)

使用 clickhouse-benchmark 测试工具进行性能测试，统计出 QPS/P50/P90/P99 等相关性能指标，用法参考：<https://clickhouse.com/docs/zh/operations/utilities/clickhouse-benchmark/>

### 离线业务 (stress)

stress 是一个 CPU 密集型测试工具，可以通过指定--cpu 参数启动多个并发 CPU 密集型任务给系统环境加压。

## 使用说明

1. 启动一个 clickhouse 容器（在线业务）。

2. 进入容器内执行 clickhouse-benchmark 命令，设置并发线程数为 10 个、查询 10000 次、查询总时间 30s。

3. 同时启动一个 stress 容器（离线业务），并发执行 10 个 CPU 密集型任务对环境进行加压。

4. clickhouse-benchmark 执行完后输出一个性能测试报告。

混部隔离测试脚本 (**test_demo.sh**) 如下：

```bash
#!/bin/bash

with_offline=${1:-no_offline}
enable_isolation=${2:-no_isolation}
stress_num=${3:-10}
concurrency=10
timeout=30
output=/tmp/result.json
online_container=
offline_container=

exec_sql="echo \"SELECT * FROM system.numbers LIMIT 10000000 OFFSET 10000000\" | clickhouse-benchmark -i 10000 -c $concurrency -t $timeout"

function prepare() {
    echo "Launch clickhouse container."
    online_container=$(docker run -itd \
            -v /tmp:/tmp:rw \
            --ulimit nofile=262144:262144 \
            -p 34424:34424 \
            yandex/clickhouse-server)

    sleep 3
    echo "Clickhouse container launched."
}

function clickhouse() {
    echo "Start clickhouse benchmark test."
    docker exec $online_container bash -c "$exec_sql --json $output"
    echo "Clickhouse benchmark test done."
}

function stress() {
    echo "Launch stress container."
    offline_container=$(docker run -itd joedval/stress --cpu $stress_num)
    echo "Stress container launched."

    if [ $enable_isolation == "enable_isolation" ]; then
        echo "Set stress container qos level to -1."
        echo -1 > /sys/fs/cgroup/cpu/docker/$offline_container/cpu.qos_level
    fi
}

function benchmark() {
    if [ $with_offline == "with_offline" ]; then
        stress
        sleep 3
    fi
    clickhouse
    echo "Remove test containers."
    docker rm -f $online_container
    docker rm -f $offline_container
    echo "Finish benchmark test for clickhouse(online) and stress(offline) colocation."
    echo "===============================clickhouse benchmark=================================================="
    cat $output
    echo "===============================clickhouse benchmark=================================================="
}

prepare
benchmark
```

## 测试结果

单独执行 clickhouse 在线业务。

```bash
sh test_demo.sh no_offline no_isolation
```

得到在线业务的 QoS(QPS/P50/P90/P99 等指标）**基线数据**如下：

```json
{
    "localhost:9000": {
        "statistics": {
            "QPS": 1.8853412284364512,
            ......
        }
    },
    "query_time_percentiles": {
        ......
        "50": 0.484905256,
        "60": 0.519641313,
        "70": 0.570876148,
        "80": 0.632544937,
        "90": 0.728295525,
        "95": 0.808700418,
        "99": 0.873945121,
        ......
    }
}
```

启用 stress 离线业务，未开启混部隔离功能下，执行 test_demo.sh 测试脚本。

```bash
# with_offline 参数表示启用 stress 离线业务
# no_isolation 参数表示未开启混部隔离功能
sh test_demo.sh with_offline no_isolation
```

**未开启混部隔离的情况下**，clickhouse 业务 QoS 数据 (QPS/P80/P90/P99 等指标）如下：

```json
{
    "localhost:9000": {
        "statistics": {
            "QPS": 0.9424028693636205,
            ......
        }
    },
    "query_time_percentiles": {
        ......
        "50": 0.840476774,
        "60": 1.304607373,
        "70": 1.393591017,
        "80": 1.41277543,
        "90": 1.430316688,
        "95": 1.457534764,
        "99": 1.555646855,
        ......
    }
}
```

启用 stress 离线业务，开启混部隔离功能下，执行 test_demo.sh 测试脚本。

```bash
# with_offline 参数表示启用 stress 离线业务
# enable_isolation 参数表示开启混部隔离功能
sh test_demo.sh with_offline enable_isolation
```

**开启混部隔离功能的情况下**，clickhouse 业务 QoS 数据 (QPS/P80/P90/P99 等指标）如下：

```json
{
    "localhost:9000": {
        "statistics": {
            "QPS": 1.8825798759270718,
            ......
        }
    },
    "query_time_percentiles": {
        ......
        "50": 0.485725185,
        "60": 0.512629901,
        "70": 0.55656488,
        "80": 0.636395956,
        "90": 0.734695906,
        "95": 0.804118275,
        "99": 0.887807409,
        ......
    }
}
```

从上面的测试结果整理出一个表格如下：

| 业务部署方式                           | QPS           | P50           | P90           | P99           |
| -------------------------------------- | ------------- | ------------- | ------------- | ------------- |
| 单独运行 clickhouse 在线业务（基线）     | 1.885         | 0.485         | 0.728         | 0.874         |
| clickhouse+stress（未开启混部隔离功能） | 0.942(-50%)   | 0.840(-42%)   | 1.430(-49%)   | 1.556(-44%)   |
| clickhouse+stress（开启混部隔离功能）   | 1.883(-0.11%) | 0.486(-0.21%) | 0.735(-0.96%) | 0.888(-1.58%) |

在未开启混部隔离功能的情况下，在线业务 clickhouse 的 QPS 从 1.9 下降到 0.9，同时业务的响应时延 (P90) 也从 0.7s 增大到 1.4s，在线业务 QoS 下降了 50% 左右；而在开启混部隔离功能的情况下，不管是在线业务的 QPS 还是响应时延 (P50/P90/P99) 相比于基线值下降不到 2%，在线业务 QoS 基本没有变化。
