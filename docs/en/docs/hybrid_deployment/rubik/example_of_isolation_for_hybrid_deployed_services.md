# Example of Isolation for Hybrid Deployed Services

## Environment Preparation

Check whether the kernel supports isolation of hybrid deployed services.

```bash
# Check whether isolation of hybrid deployed services is enabled in the /boot/config-<kernel version> system configuration.
# If CONFIG_QOS_SCHED=y, the function is enabled. Example:
cat /boot/config-5.10.0-60.18.0.50.oe2203.x86_64 | grep CONFIG_QOS
CONFIG_QOS_SCHED=y
```

Install the Docker engine.

```bash
yum install -y docker-engine
docker version
# The following shows the output of docker version.
Client:
 Version:           18.09.0
 EulerVersion:      18.09.0.300
 API version:       1.39
 Go version:        go1.17.3
 Git commit:        aa1eee8
 Built:             Wed Mar 30 05:07:38 2022
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.09.0
  EulerVersion:     18.09.0.300
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.17.3
  Git commit:       aa1eee8
  Built:            Tue Mar 22 00:00:00 2022
  OS/Arch:          linux/amd64
  Experimental:     false
```

## Hybrid Deployed Services

**Online Service ClickHouse**

Use the clickhouse-benchmark tool to test the performance and collect statistics on performance metrics such as QPS, P50, P90, and P99. For details, see <https://clickhouse.com/docs/en/operations/utilities/clickhouse-benchmark/>.

**Offline Service Stress**

Stress is a CPU-intensive test tool. You can specify the **--cpu** option to start multiple concurrent CPU-intensive tasks to increase the stress on the system.

## Usage Instructions

1) Start a ClickHouse container (online service).

2) Access the container and run the **clickhouse-benchmark** command. Set the number of concurrent queries to **10**, the number of queries to **10000**, and time limit to **30**.

3) Start a Stress container (offline service) at the same time and concurrently execute 10 CPU-intensive tasks to increase the stress on the environment.

4) After the **clickhouse-benchmark** command is executed, a performance test report is generated.

The **test_demo.sh** script for the isolation test for hybrid deployed services is as follows:

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

function prepare()
{
    echo "Launch clickhouse container."
    online_container=$(docker run -itd \
            -v /tmp:/tmp:rw \
            --ulimit nofile=262144:262144 \
            -p 34424:34424 \
            yandex/clickhouse-server)

    sleep 3
    echo "Clickhouse container launched."
}

function clickhouse()
{
    echo "Start clickhouse benchmark test."
    docker exec $online_container bash -c "$exec_sql --json $output"
    echo "Clickhouse benchmark test done."
}

function stress()
{
    echo "Launch stress container."
    offline_container=$(docker run -itd joedval/stress --cpu $stress_num)
    echo "Stress container launched."

    if [ $enable_isolation == "enable_isolation" ]; then
        echo "Set stress container qos level to -1."
        echo -1 > /sys/fs/cgroup/cpu/docker/$offline_container/cpu.qos_level
    fi
}

function benchmark()
{
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

## Test Results

Independently execute the online service ClickHouse.

```bash
sh test_demo.sh no_offline no_isolation
```

The baseline QoS data (QPS/P50/P90/P99) of the online service is as follows:

```json
{
"localhost:9000": {
"statistics": {
"QPS": 1.8853412284364512,
......
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
}
```

Execute the **test_demo.sh** script to start the offline service Stress and run the test with the isolation function disabled.

```bash
# **with_offline** indicates that the offline service Stress is enabled.
# **no_isolation** indicates that isolation of hybrid deployed services is disabled.
sh test_demo.sh with_offline no_isolation
```

**When isolation of hybrid deployed services is disabled**, the QoS data (QPS/P80/P90/P99) of the ClickHouse service is as follows:

```json
{
"localhost:9000": {
"statistics": {
"QPS": 0.9424028693636205,
......
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

Execute the **test_demo.sh** script to start the offline service Stress and run the test with the isolation function enabled.

```bash
# **with_offline** indicates that the offline service Stress is enabled.
# **enable_isolation** indicates that isolation of hybrid deployed services is enabled.
sh test_demo.sh with_offline enable_isolation
```

**When isolation of hybrid deployed services is enabled**, the QoS data (QPS/P80/P90/P99) of the ClickHouse service is as follows:

```json
{
"localhost:9000": {
"statistics": {
"QPS": 1.8825798759270718,
......
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
}
```

The following table lists the test results.

| Service Deployment Mode                          | QPS           | P50           | P90           | P99           |
| -------------------------------------- | ------------- | ------------- | ------------- | ------------- |
| ClickHouse (baseline)    | 1.885         | 0.485         | 0.728         | 0.874         |
| ClickHouse + Stress (isolation disabled)| 0.942 (-50%)   | 0.840 (-42%)   | 1.430 (-49%)   | 1.556 (-44%)   |
| ClickHouse + Stress (isolation enabled)  | 1.883 (-0.11%) | 0.486 (-0.21%) | 0.735 (-0.96%) | 0.888 (-1.58%) |

When isolation of hybrid deployed services is disabled, the QPS of ClickHouse decreases from approximately 1.9 to 0.9, the service response delay (P90) increases from approximately 0.7s to 1.4s, and the QoS decreases by about 50%. When isolation of hybrid deployed services is enabled, the QPS and response delay (P50/P90/P99) of ClickHouse decrease by less than 2% compared with the baseline, and the QoS remains unchanged.
