# Installation and Deployment

## Software

* OS: openEuler 23.09

## Hardware

* x86_64

## Preparing the Environment

* Install the openEuler OS by referring to the *openEuler Installation Guide*.

* Root permissions are required for installing Kmesh.

## Installing Kmesh

* Install the Kmesh software package.

```shell
yum install Kmesh
```

* Check whether the installation is successful. If the command output contains the name of the software package, the installation is successful.

```shell
rpm -q Kmesh
```

## Deploying Kmesh

### Cluster Mode

Before starting Kmesh, configure the IP address of the control plane program (for example, Istiod IP address) in the cluster.

```json
    "clusters": [
      {
        "name": "xds-grpc",
        "type" : "STATIC",
        "connect_timeout": "1s",
        "lb_policy": "ROUND_ROBIN",
        "load_assignment": {
          "cluster_name": "xds-grpc",
          "endpoints": [{
            "lb_endpoints": [{
              "endpoint": {
                "address":{
                  "socket_address": {
                          "protocol": "TCP",
                          "address": "192.168.0.1",# Configure the control plane IP address (for example, Istiod IP address).
                          "port_value": 15010
                     }
                }
              }
            }]
          }]
```

Currently, only the traffic orchestration function is supported in the cluster mode.

### Local Mode

Before starting Kmesh, modify `kmesh.service` to enable or disable required functions.

```shell
# Choose -enable-kmesh and disable ADS.
$ vim /usr/lib/systemd/system/kmesh.service
ExecStart=/usr/bin/kmesh-daemon -enable-kmesh -enable-ads=false
$ systemctl daemon-reload
```

To enable mesh acceleration, run the following commands:

```shell
# Choose -enable-mda and disable ADS.
$ vim /usr/lib/systemd/system/kmesh.service
ExecStart=/usr/bin/kmesh-daemon -enable-mda -enable-ads=false
$ systemctl daemon-reload
```

When the Kmesh service is started, the kmesh-daemon program is invoked. For details about how to use the kmesh-daemon program, see [Using kmesh-daemon](./usage.md).

### Starting Kmesh

```shell
# Start the Kmesh service.
$ systemctl start kmesh.service
# Check the Kmesh running status.
$ systemctl status kmesh.service
```

### Stopping Kmesh

```shell
# Stop the Kmesh service.
$ systemctl stop kmesh.service
```
