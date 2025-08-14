# 监控安全容器

## 描述

kata 2.x中移除了kata-runtime events命令，代之以kata-runtime metrics命令，用以收集sandbox的指标信息，包括但不限于虚拟机信息、shim v2的cpu seconds、guest OS的CPU信息等等。格式符合Prometheus metric，可以配合kata-monitor上报至Prometheus。

## 用法

```bash
kata-runtime metrics <sandbox id>
```

## 前置条件

sandbox id为长id，要查询的容器状态必须为running，否则报错：`Get "<http://shim/metrics":dial> unix /run/vc/\<id\>/shim-monitor : connect : connection refused`

当使用annotation指定容器类型为运行在某个sandbox中的容器时，用kata-runtime metrics查询该容器会失败，只能去查询该容器对应的sandbox。

该命令只支持查询监控一个sandbox的状态。

## 示例

```bash
$ kata-runtime metrics e2270357d23f9d3dd424011e1e70aa8defb267d813c3d451db58f35aeac97a04

# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 2.656e-05
go_gc_duration_seconds{quantile="0.25"} 3.345e-05
go_gc_duration_seconds{quantile="0.5"} 3.778e-05
go_gc_duration_seconds{quantile="0.75"} 4.657e-05
go_gc_duration_seconds{quantile="1"} 0.00023001
go_gc_duration_seconds_sum 0.00898126
go_gc_duration_seconds_count 195
# HELP go_goroutines Number of goroutines that currently exist.
# TYPE go_goroutines gauge
go_goroutines 27
# HELP go_info Information about the Go environment.
# TYPE go_info gauge
go_info{version="go1.17.3"} 1
# HELP kata_hypervisor_netdev Net devices statistics.
# TYPE kata_hypervisor_netdev gauge
kata_hypervisor_netdev{interface="lo",item="recv_bytes"} 0
kata_hypervisor_netdev{interface="lo",item="recv_compressed"} 0
kata_hypervisor_netdev{interface="lo",item="recv_drop"} 0
kata_hypervisor_netdev{interface="lo",item="recv_errs"} 0
kata_hypervisor_netdev{interface="lo",item="recv_fifo"} 0
kata_hypervisor_netdev{interface="lo",item="recv_frame"} 0
kata_hypervisor_netdev{interface="lo",item="recv_multicast"} 0
kata_hypervisor_netdev{interface="lo",item="recv_packets"} 0
kata_hypervisor_netdev{interface="lo",item="sent_bytes"} 0
kata_hypervisor_netdev{interface="lo",item="sent_carrier"} 0
kata_hypervisor_netdev{interface="lo",item="sent_colls"} 0
```
