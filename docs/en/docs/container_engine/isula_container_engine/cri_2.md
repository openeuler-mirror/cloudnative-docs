# CRI API v1

## Overview

Container Runtime Interface (CRI) is the main protocol used by kublet to communicate with container engines.
Kubernetes 1.25 and earlier versions support CRI v1alpha2 and CRI v1. Kubernetes 1.26 and later versions support only CRI v1.

iSulad supports both [CRI v1alpha2](cri.md) and CRI v1.
For CRI v1, iSulad supports the functions described in [CRI v1alpha2](cri.md) and new interfaces and fields defined in CRI v1.

Currently, iSulad supports CRI v1 1.29. The API described on the official website is as follows:

[https://github.com/kubernetes/cri-api/blob/kubernetes-1.29.0/pkg/apis/runtime/v1/api.proto](https://github.com/kubernetes/cri-api/blob/kubernetes-1.29.0/pkg/apis/runtime/v1/api.proto)

The API description file used by iSulad is slightly different from the official API. The interfaces in this document prevail.

## New Fields of CRI v1

- **CgroupDriver**

  Enum values for cgroup drivers.

  | Member       | Description           |
  | ------------ | --------------------- |
  | SYSTEMD = 0  | systemd-cgroup driver |
  | CGROUPFS = 1 | cgroupfs driver       |

- **LinuxRuntimeConfiguration**

  cgroup driver used by the container engine

  | Member                     | Description                                                   |
  | -------------------------- | ------------------------------------------------------------- |
  | CgroupDriver cgroup_driver | Enum value for the cgroup driver used by the container engine |

- **ContainerEventType**

  Enum values for container event types

  | Member                      | Description              |
  | --------------------------- | ------------------------ |
  | CONTAINER_CREATED_EVENT = 0 | Container creation event |
  | CONTAINER_STARTED_EVENT = 1 | Container startup event  |
  | CONTAINER_STOPPED_EVENT = 1 | Container stop event     |
  | CONTAINER_DELETED_EVENT = 1 | Container deletion event |

- **SwapUsage**

  Virtual memory usage

  | Member                           | Description                    |
  | -------------------------------- | ------------------------------ |
  | int64 timestamp                  | Timestamp information          |
  | UInt64Value swap_available_bytes | Available virtual memory bytes |
  | UInt64Value swap_usage_bytes     | Used virtual memory bytes      |

## New Interfaces

### RuntimeConfig

#### Interface Prototype

```text
rpc RuntimeConfig(RuntimeConfigRequest) returns (RuntimeConfigResponse) {}
```

#### Interface Description

Obtains the cgroup driver configuration (cgroupfs or systemd-cgroup).

#### Parameter: RuntimeConfigRequest

No such field

#### Returns: RuntimeConfigResponse

| Return                          | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| LinuxRuntimeConfiguration linux | CgroupDriver enum value for cgroupfs or systemd-cgroup |

### GetContainerEvents

#### Interface Prototype

```text
rpc GetContainerEvents(GetEventsRequest) returns (stream ContainerEventResponse) {}
```

#### Interface Description

Obtains the pod lifecycle event stream.

#### Parameter: GetEventsRequest

No such field

#### Returns: ContainerEventResponse

| Return                                       | Description                                                        |
| -------------------------------------------- | ------------------------------------------------------------------ |
| string container_id                          | Container ID                                                       |
| ContainerEventType container_event_type      | Container event type                                               |
| int64 created_at                             | Time when the container event is generated                         |
| PodSandboxStatus pod_sandbox_status          | Status of the pod to which the container belongs                   |
| repeated ContainerStatus containers_statuses | Status of all containers in the pod to which the container belongs |

## Change Description

### CRI V1.29

#### [Obtaining the cgroup Driver Configuration](https://github.com/kubernetes/kubernetes/pull/118770)

`RuntimeConfig` obtains the cgroup driver configuration (cgroupfs or systemd-cgroup).

#### [GetContainerEvents Supports Pod Lifecycle Events](https://github.com/kubernetes/kubernetes/pull/111384)

`GetContainerEvents` provides event streams related to the pod lifecycle.

`PodSandboxStatus` is adjusted accordingly. `ContainerStatuses` is added to provide sandbox content status information.

#### [ContainerStats Virtual Memory Information](https://github.com/kubernetes/kubernetes/pull/118865)

The virtual memory usage information `SwapUsage` is added to `ContainerStats`.

#### [OOMKilled Setting in the Reason Field of ContainerStatus](https://github.com/kubernetes/kubernetes/pull/112977)

The **Reason** field in **ContainerStatus** should be set to OOMKilled when cgroup out-of-memory occurs.

#### [Modification of PodSecurityContext.SupplementalGroups Description](https://github.com/kubernetes/kubernetes/pull/113047)

The description is modified to optimize the comments of **PodSecurityContext.SupplementalGroups**. The behavior that the main UID defined by the container image is not in the list is clarified.

#### [ExecSync Output Restriction](https://github.com/kubernetes/kubernetes/pull/110435)

The **ExecSync** return value output is less than 16 MB.

## User Guide

### Configuring iSulad to Support CRI V1

Configure iSulad to support CRI v1 1.29 used by the new Kubernetes version.

For CRI v1 1.25 or earlier, the functions of V1alpha2 are the same as those of V1. The new features of CRI v1 1.26 or later are supported only in CRI v1.
The functions and features of this upgrade are supported only in CRI v1. Therefore, you need to enable CRI v1as follows.

Enable CRI v1.

Set **enable-cri-v1** in **daemon.json** of iSulad to **true** and restart iSulad.

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true
}
```

If iSulad is installed from source, enable the **ENABLE_CRI_API_V1** compile option.

```bash
cmake ../ -D ENABLE_CRI_API_V1=ON
```

### Using RuntimeConfig to Obtain the cgroup Driver Configuration

#### systemd-cgroup Configuration

iSulad supports both systemd and cgroupfs cgroup drivers.
By default, cgroupfs is used. You can configure iSulad to support systemd-cgroup.
iSulad supports only systemd-cgroup when the runtime is runc. In the iSulad configuration file **daemon.json**,
set **systemd-cgroup** to **true** and restart iSulad to use the systemd-cgroup driver.

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true,
    "systemd-cgroup": true
}
```

### Using GetContainerEvents to Generate Pod Lifecycle Events

#### Pod Events Configuration

In the iSulad configuration file **daemon.json**,
set **enable-pod-events** to **true** and restart iSulad.

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true,
    "enable-pod-events": true
}
```

## Constraints

1. The preceding new features are supported by iSulad only when the container runtime is runc.
2. cgroup out-of-memory (OOM) triggers the deletion of the cgroup path of the container. If iSulad processes the OOM event after the cgroup path is deleted, iSulad cannot capture the OOM event of the container. As a result, the **Reason** field in **ContainerStatus** may be incorrect.
3. iSulad does not support the mixed use of different cgroup drivers to manage containers. After a container is started, the cgroup driver configuration in iSulad should not change.
