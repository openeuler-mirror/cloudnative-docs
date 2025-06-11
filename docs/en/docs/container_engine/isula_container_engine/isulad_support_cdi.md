# iSulad Support for CDI

## Overview

Container Device Interface (CDI) is a container runtime specification used to support third-party devices.

CDI solves the following problems:  
In Linux, only one device node needed to be exposed in a container in the past to enable device awareness of the container. However, as devices and software become more complex, vendors want to perform more operations, such as:

- Exposing multiple device nodes to a container, mounting files from a runtime namespace to a container, or hiding procfs entries.
- Checking the compatibility between containers and devices. For example, checking whether a container can run on a specified device.
- Performing runtime-specific operations, such as virtual machines and Linux container-based runtimes.
- Performing device-specific operations, such as GPU memory cleanup and FPGA re-programming.

In the absence of third-party device standards, vendors often have to write and maintain multiple plugins for different runtimes, or even contribute vendor-specific code directly in a runtime. In addition, the runtime does not expose the plugin system in a unified manner (or even not at all), resulting in duplication of functionality in higher-level abstractions (such as Kubernetes device plugins).

To solve the preceding problem, CDI provides the following features:  
CDI describes a mechanism that allows third-party vendors to interact with devices without modifying the container runtime.

The mechanism is exposed as a JSON file (similar to the container network interface CNI), which allows vendors to describe the operations that the container runtime should perform on the OCI-based container.

Currently, iSulad supports the [CDI v0.6.0](https://github.com/cncf-tags/container-device-interface/blob/v0.6.0/SPEC.md) specification.

## Configuring iSulad to Support CDI

Modify the **daemon.json** file as follows and restart iSulad:

```json
{
    ...
    "enable-cri-v1": true,
    "cdi-spec-dirs": ["/etc/cdi", "/var/run/cdi"],
    "enable-cdi": true
}
```

**cdi-spec-dirs** specifies the directory where CDI specifications are stored. If this parameter is not specified, the default value **/etc/cdi** or **/var/run/cdi** is used.

## Examples

### CDI Specification Example

For details about each field, see [CDI v0.6.0](https://github.com/cncf-tags/container-device-interface/blob/v0.6.0/SPEC.md).

```bash
$ mkdir /etc/cdi
$ cat > /etc/cdi/vendor.json <<EOF
{
  "cdiVersion": "0.6.0",
  "kind": "vendor.com/device",
  "devices": [
    {
      "name": "myDevice",
      "containerEdits": {
        "deviceNodes": [
          {"hostPath": "/vendor/dev/card1", "path": "/dev/card1", "type": "c", "major": 25, "minor": 25, "fileMode": 384, "permissions": "rw", "uid": 1000, "gid": 1000},
          {"path": "/dev/card-render1", "type": "c", "major": 25, "minor": 25, "fileMode": 384, "permissions": "rwm", "uid": 1000, "gid": 1000}
        ]
      }
    }
  ],
  "containerEdits": {
    "env": [
      "FOO=VALID_SPEC",
      "BAR=BARVALUE1"
    ],
    "deviceNodes": [
      {"path": "/dev/vendorctl", "type": "b", "major": 25, "minor": 25, "fileMode": 384, "permissions": "rw", "uid": 1000, "gid": 1000}
    ],
    "mounts": [
      {"hostPath": "/bin/vendorBin", "containerPath": "/bin/vendorBin"},
      {"hostPath": "/usr/lib/libVendor.so.0", "containerPath": "/usr/lib/libVendor.so.0"},
      {"hostPath": "tmpfs", "containerPath": "/tmp/data", "type": "tmpfs", "options": ["nosuid","strictatime","mode=755","size=65536k"]}
    ],
    "hooks": [
      {"createContainer": {"path": "/bin/vendor-hook"} },
      {"startContainer": {"path": "/usr/bin/ldconfig"} }
    ]
  }
}
EOF
```

### Using CDI in the Parameters for Creating a Container in CRI

Assume that the **vendor.json** specification has been generated, and the specification is available in **/etc/cdi** or **/var/run/cdi** (or the specification is available in the directory specified by **cdi-spec-dirs** in the iSulad configuration file), the container can access the device using its fully qualified device name, for example, **vendor.com/device=myDevice**.

In the JSON file of the container, you can use either of the following methods to specify a device:

1. Specify a device in **annotations**.

    ```json
    {
        ... ...
        "annotations": [
            ... ...
            {"cdi.k8s.io/test": "vendor.com/device=myDevice"},
            ... ...
        ]
        ... ...
    }
    ```

2. Specify a device in **CDI_Devices**.

    ```json
    {
        ... ...
        "CDI_Devices": [
            ... ...
            {"Name": "vendor.com/device=myDevice"},
            ... ...
        ]
        ... ...
    }
    ```

## Constraints

1. Currently, iSulad supports the CDI feature using CRI only.
