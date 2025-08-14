# Monitoring Secure Containers

- [Monitoring Secure Containers](#monitoring-secure-containers)

## Description

In kata 2.x, events subcommand is removed and replaced by **kata-runtime metrics**, which can be used to gather metrics associated with infrastructure used to run a sandbox, including virtual machine stats, shim v2 CPU seconds and CPU stat of guest OS and so on. Metrics are organized in a Prometheus compatible format so that they can be easily uploaded to Prometheus when work with kata-monitor.

## Usage

```shell
kata-runtime metrics <sandbox id>
```

## Prerequisites

The sandbox ID must be the full ID. The sandbox to be queried must be in the  **running**  state. Otherwise, the following error message will be displayed: "Container ID \(<container\_id\>\) does not exist".

When using annotation to make a container run in a specific sandbox, clients should not use kata-runtime metrics to gather metrics of that container. The correct way is to query the corresponding sandbox.

This command can be used to query the status of only one container.

## Example

```shell
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
