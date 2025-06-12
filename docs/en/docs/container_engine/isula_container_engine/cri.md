# CRI API v1alpha2

## Description

CRI API is the container runtime APIs provided by Kubernetes. CRI defines service interfaces for containers and images. iSulad uses CRI API to interconnect with Kubernetes.

The lifecycle of a container is isolated from that of an image. Therefore, two services are required. CRI API is defined using [Protocol Buffers](https://developers.google.com/protocol-buffers/) and is based on [gRPC](https://grpc.io/).

Currently, the default CRI API version used by iSulad is v1alpha2. The official API description file is as follows:

[https://github.com/kubernetes/kubernetes/blob/release-1.14/pkg/kubelet/apis/cri/runtime/v1alpha2/api.proto](https://github.com/kubernetes/kubernetes/blob/release-1.14/pkg/kubelet/apis/cri/runtime/v1alpha2/api.proto),

iSulad uses the API description file of version 1.14 used by Pass, which is slightly different from the official API. The interfaces in this document prevail.

> [!NOTE]NOTE  
> For the WebSocket streaming service of CRI API, the listening address of the server is 127.0.0.1, and the port number is 10350. The port number can be configured through the `--websocket-server-listening-port` command option or in the **daemon.json** configuration file.

## Interfaces

The following tables list the parameters that may be used by the interfaces. Some parameters cannot be configured.

### Interface Parameters

- **DNSConfig**

    Specifies the DNS servers and search domains of a sandbox.

    | Member                   | Description                                                         |
    | ------------------------ | ------------------------------------------------------------------- |
    | repeated string servers  | List of DNS servers of the cluster                                  |
    | repeated string searches | List of DNS search domains of the cluster                           |
    | repeated string options  | List of DNS options. See <https://linux.die.net/man/5/resolv.conf>. |

- **Protocol**

    Enum values of the protocols.

    | Member  | Description |
    | ------- | ----------- |
    | TCP = 0 | TCP         |
    | UDP = 1 | UDP         |

- **PortMapping**

    Specifies the port mapping configurations of a sandbox.

    | Member               | Description                      |
    | -------------------- | -------------------------------- |
    | Protocol protocol    | Protocol of the port mapping     |
    | int32 container_port | Port number within the container |
    | int32 host_port      | Port number on the host          |
    | string host_ip       | Host IP address                  |

- **MountPropagation**

    Enum values for mount propagation.

    | Member                            | Description                                                                                                  |
    | --------------------------------- | ------------------------------------------------------------------------------------------------------------ |
    | PROPAGATION_PRIVATE = 0           | No mount propagation ("rprivate" in Linux)                                                                   |
    | PROPAGATION_HOST_TO_CONTAINER = 1 | Mounts get propagated from the host to the container ("rslave" in Linux)                                     |
    | PROPAGATION_BIDIRECTIONAL = 2     | Mounts get propagated from the host to the container and from the container to the host ("rshared" in Linux) |

- **Mount**

    Specifies a host volume to mount into a container. (Only files and folders are supported.)

    | Member                       | Description                                                                                                                                                      |
    | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | string container_path        | Path in the container                                                                                                                                            |
    | string host_path             | Path on the host                                                                                                                                                 |
    | bool readonly                | Whether the configuration is read-only in the container. The default value is **false**.                                                                         |
    | bool selinux_relabel         | Whether to set the SELinux label (not supported)                                                                                                                 |
    | MountPropagation propagation | Mount propagation configuration. The value can be **0**, **1**, or **2**, corresponding to **rprivate**, **rslave**, or **rshared**. The default value is **0**. |

- **NamespaceOption**

    | Member            | Description                                      |
    | ----------------- | ------------------------------------------------ |
    | bool host_network | Whether to use the network namespace of the host |
    | bool host_pid     | Whether to use the PID namespace of the host     |
    | bool host_ipc     | Whether to use the IPC namespace of the host     |

- **Capability**

    Contains information about the capabilities to add or drop.

    | Member                            | Description          |
    | --------------------------------- | -------------------- |
    | repeated string add_capabilities  | Capabilities to add  |
    | repeated string drop_capabilities | Capabilities to drop |

- **Int64Value**

    Wrapper of the int64 type.

    | Member      | Description        |
    | ----------- | ------------------ |
    | int64 value | Actual int64 value |

- **UInt64Value**

    Wrapper of the uint64 type.

    | Member       | Description         |
    | ------------ | ------------------- |
    | uint64 value | Actual uint64 value |

- **LinuxSandboxSecurityContext**

    Specifies Linux security options for a sandbox.

    Note that these security options are not applied to containers in the sandbox and may not be applicable to a sandbox without any running process.

    | Member | Description |
    | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | NamespaceOption namespace_options | Options for namespaces of the sandbox |
    | SELinuxOption selinux_options | SELinux options (not supported) |
    | Int64Value run_as_user | UID to run sandbox processes |
    | bool readonly_rootfs | Whether the root file system of the sandbox is read-only |
    | repeated int64 supplemental_groups | User group information of process 1 in the sandbox besides the primary group |
    | bool privileged | Whether the sandbox can run a privileged container |
    | string seccomp_profile_path | Path of the seccomp configuration file. Valid values are: <br>// **unconfined**: seccomp is not used.<br>// **localhost/***\<full_file_path>*: path of the configuration file installed in the system. <br>// *\<full_file_path>*:Full path of the configuration file. <br>//By default, this parameter is not set, which is identical to **unconfined**.|

- **LinuxPodSandboxConfig**

    Sets configurations related to Linux hosts and containers.

    | Member                                       | Description                                                                                                                        |
    | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
    | string cgroup_parent                         | Parent cgroup path of the sandbox. The runtime can convert it to the cgroupfs or systemd semantics as required. (Not configurable) |
    | LinuxSandboxSecurityContext security_context | Security attributes of the sandbox                                                                                                 |
    | map\<string, string> sysctls                 | Linux sysctls configurations of the sandbox                                                                                        |

- **PodSandboxMetadata**

    Stores all necessary information for building the sandbox name. The container runtime is encouraged to expose the metadata in its user interface for better user experience. For example, the runtime can construct a unique sandbox name based on the metadata.

    | Member           | Description                                                           |
    | ---------------- | --------------------------------------------------------------------- |
    | string name      | Sandbox name                                                          |
    | string uid       | Sandbox UID                                                           |
    | string namespace | Sandbox namespace                                                     |
    | uint32 attempt   | Number of attempts to create the sandbox. The default value is **0**. |

- **PodSandboxConfig**

    Contains all the required and optional fields for creating a sandbox.

    | Member | Description |
    | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
    | PodSandboxMetadata metadata | Metadata of the sandbox. This information uniquely identifies the sandbox, and the runtime should leverage this to ensure correct operation. The runtime may also use this information to improve user experience, such as by constructing a readable sandbox name.|
    | string hostname | Host name of the sandbox |
    | string log_directory | Directory for storing log files of containers in the sandbox |
    | DNSConfig dns_config | DNS configuration of the sandbox |
    | repeated PortMapping port_mappings | Port mappings of the sandbox |
    | map\<string, string> labels | Key-value pairs that may be used to identify a single sandbox or a series of sandboxes |
    | map\<string, string> annotations | Key-value pair holding arbitrary data. The value cannot be modified and can be queried by using **PodSandboxStatus**. |
    | LinuxPodSandboxConfig linux | Options related to the linux host |

- **PodSandboxNetworkStatus**

    Describes the network status of the sandbox.

    | Member         | Description                                  |
    | -------------- | -------------------------------------------- |
    | string ip      | IP address of the sandbox                    |
    | string name    | Name of the network interface in the sandbox |
    | string network | Name of the additional network               |

- **Namespace**

    Stores namespace options.

    | Member                  | Description             |
    | ----------------------- | ----------------------- |
    | NamespaceOption options | Linux namespace options |

- **LinuxPodSandboxStatus**

    Describes the status of the Linux sandbox.

    | Member                  | Description       |
    | ----------------------- | ----------------- |
    | Namespace**namespaces** | Sandbox namespace |

- **PodSandboxState**

    Enum values for sandbox states.

    | Member               | Description                    |
    | -------------------- | ------------------------------ |
    | SANDBOX_READY = 0    | Ready state of the sandbox     |
    | SANDBOX_NOTREADY = 1 | Non-ready state of the sandbox |

- **PodSandboxStatus**

    Describes the podsandbox status.

    | Member                                    | Description                                                                            |
    | ----------------------------------------- | -------------------------------------------------------------------------------------- |
    | string id                                 | Sandbox ID                                                                             |
    | PodSandboxMetadata metadata               | Sandbox metadata                                                                       |
    | PodSandboxState state                     | Sandbox state                                                                          |
    | int64 created_at                          | Creation timestamps of the sandbox in nanoseconds                                      |
    | repeated PodSandboxNetworkStatus networks | Multi-plane network status of the sandbox                                              |
    | LinuxPodSandboxStatus linux               | Status specific to Linux sandboxes                                                     |
    | map\<string, string> labels               | Key-value pairs that may be used to identify a single sandbox or a series of sandboxes |
    | map\<string, string> annotations          | Key-value pair holding arbitrary data. The value cannot be modified by the runtime.    |

- **PodSandboxStateValue**

    Wrapper of **PodSandboxState**.

    | Member                | Description   |
    | --------------------- | ------------- |
    | PodSandboxState state | Sandbox state |

- **PodSandboxFilter**

    Filtering conditions when listing sandboxes. The intersection of multiple conditions is displayed.

    | Member                              | Description                                                                          |
    | ----------------------------------- | ------------------------------------------------------------------------------------ |
    | string id                           | Sandbox ID                                                                           |
    | PodSandboxStateValue state          | Sandbox state                                                                        |
    | map\<string, string> label_selector | Sandbox labels. Only full match is supported. Regular expressions are not supported. |

- **PodSandbox**

    Minimal data that describes a sandbox.

    | Member                           | Description                                                                            |
    | -------------------------------- | -------------------------------------------------------------------------------------- |
    | string id                        | Sandbox ID                                                                             |
    | PodSandboxMetadata metadata      | Sandbox metadata                                                                       |
    | PodSandboxState state            | Sandbox state                                                                          |
    | int64 created_at                 | Creation timestamps of the sandbox in nanoseconds                                      |
    | map\<string, string> labels      | Key-value pairs that may be used to identify a single sandbox or a series of sandboxes |
    | map\<string, string> annotations | Key-value pair holding arbitrary data. The value cannot be modified by the runtime     |

- **KeyValue**

    Wrapper of a key-value pair.

    | Member       | Description |
    | ------------ | ----------- |
    | string key   | Key         |
    | string value | Value       |

- **SELinuxOption**

    SELinux labels to be applied to the container.

    | Member       | Description |
    | ------------ | ----------- |
    | string user  | User        |
    | string role  | Role        |
    | string type  | Type        |
    | string level | Level       |

- **ContainerMetadata**

    ContainerMetadata contains all necessary information for building the container name. The container runtime is encouraged to expose the metadata in its user interface for better user experience. For example, the runtime can construct a unique container name based on the metadata.

    | Member         | Description                                                             |
    | -------------- | ----------------------------------------------------------------------- |
    | string name    | Name of a container                                                     |
    | uint32 attempt | Number of attempts to create the container. The default value is **0**. |

- **ContainerState**

    Enum values for container states.

    | Member                | Description                        |
    | --------------------- | ---------------------------------- |
    | CONTAINER_CREATED = 0 | The container is created           |
    | CONTAINER_RUNNING = 1 | The container is running           |
    | CONTAINER_EXITED = 2  | The container is in the exit state |
    | CONTAINER_UNKNOWN = 3 | The container state is unknown     |

- **ContainerStateValue**

    Wrapper of ContainerState.

    | Member               | Description           |
    | -------------------- | --------------------- |
    | ContainerState state | Container state value |

- **ContainerFilter**

    Filtering conditions when listing containers. The intersection of multiple conditions is displayed.

    | Member                              | Description                                                                            |
    | ----------------------------------- | -------------------------------------------------------------------------------------- |
    | string id                           | Container ID                                                                           |
    | PodSandboxStateValue state          | Container state                                                                        |
    | string pod_sandbox_id               | Sandbox ID                                                                             |
    | map\<string, string> label_selector | Container labels. Only full match is supported. Regular expressions are not supported. |

- **LinuxContainerSecurityContext**

    Security configuration that will be applied to a container.

    | Member | Description |
    | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
    | Capability capabilities | Capabilities to add or drop |
    | bool privileged | Whether the container is in privileged mode. The default value is **false**. |
    | NamespaceOption namespace_options | Namespace options of the container |
    | SELinuxOption selinux_options | SELinux context to be optionally applied (**not supported currently**) |
    | Int64Value run_as_user | UID to run container processes. Only one of **run_as_user** and **run_as_username** can be specified at a time. **run_as_username** takes effect preferentially. |
    | string run_as_username | User name to run container processes. If specified, the user must exist in the container image (that is, in **/etc/passwd** inside the image) and be resolved there by the runtime. Otherwise, the runtime must throw an error.|
    | bool readonly_rootfs | Whether the root file system in the container is read-only. The default value is configured in **config.json**. |
    | repeated int64 supplemental_groups | List of groups of the first process in the container besides the primary group |
    | string apparmor_profile | AppArmor configuration file for the container (**not supported currently**) |
    | string seccomp_profile_path | Seccomp configuration file for the container |
    | bool no_new_privs | Whether to set the **no_new_privs** flag on the container |

- **LinuxContainerResources**

    Resource specification for the Linux container.

    | Member                      | Description                                                                   |
    | --------------------------- | ----------------------------------------------------------------------------- |
    | int64 cpu_period            | CPU Completely Fair Scheduler (CFS) period. The default value is **0**.       |
    | int64 cpu_quota             | CPU CFS quota. The default value is **0**.                                    |
    | int64 cpu_shares            | CPU shares (weight relative to other containers). The default value is **0**. |
    | int64 memory_limit_in_bytes | Memory limit, in bytes. The default value is **0**.                           |
    | int64 oom_score_adj         | oom-killer score. The default value is **0**.                                 |
    | string cpuset_cpus          | CPU cores to be used by the container. The default value is **""**.           |
    | string cpuset_mems          | Memory nodes to be used by the container. The default value is **""**.        |

- **Image**

    Basic information about a container image.

    | Member                       | Description                    |
    | ---------------------------- | ------------------------------ |
    | string id                    | Image ID                       |
    | repeated string repo_tags    | Image tag name (**repo_tags**) |
    | repeated string repo_digests | Image digest information       |
    | uint64 size                  | Image size                     |
    | Int64Value uid               | UID of the default image user  |
    | string username              | Name of the default image user |

- **ImageSpec**

    Internal data structure that represents an image. Currently, **ImageSpec** wraps only the container image name.

    | Member       | Description          |
    | ------------ | -------------------- |
    | string image | Container image name |

- **StorageIdentifier**

    Unique identifier of a storage device.

    | Member      | Description        |
    | ----------- | ------------------ |
    | string uuid | UUID of the device |

- **FilesystemUsage**

    | Member                       | Description                                      |
    | ---------------------------- | ------------------------------------------------ |
    | int64 timestamp              | Timestamp at which the information was collected |
    | StorageIdentifier storage_id | UUID of the file system that stores the image    |
    | UInt64Value used_bytes       | Space size used for storing image metadata       |
    | UInt64Value inodes_used      | Number of inodes for storing image metadata      |

- **AuthConfig**

    | Member                | Description                                                                                   |
    | --------------------- | --------------------------------------------------------------------------------------------- |
    | string username       | User name used for downloading images                                                         |
    | string password       | Password used for downloading images                                                          |
    | string auth           | Base64-encoded authentication information used for downloading images                         |
    | string server_address | Address of the server for downloaded images (not supported currently)                         |
    | string identity_token | Token information used for authentication with the image repository (not supported currently) |
    | string registry_token | Token information used for interaction with the image repository (not supported currently)    |

- **Container**

    Container description information, such as the ID and state.

    | Member                           | Description                                                                               |
    | -------------------------------- | ----------------------------------------------------------------------------------------- |
    | string id                        | Container ID                                                                              |
    | string pod_sandbox_id            | ID of the sandbox to which the container belongs                                          |
    | ContainerMetadata metadata       | Container metadata                                                                        |
    | ImageSpec image                  | Image specifications                                                                      |
    | string image_ref                 | Reference to the image used by the container. For most runtimes, this is an image ID.     |
    | ContainerState state             | Container state                                                                           |
    | int64 created_at                 | Creation timestamps of the container in nanoseconds                                       |
    | map\<string, string> labels      | Key-value pairs that may be used to identify a single container or a series of containers |
    | map\<string, string> annotations | Key-value pair holding arbitrary data. The value cannot be modified by the runtime        |

- **ContainerStatus**

    Container status information.

    | Member                           | Description                                                                                              |
    | -------------------------------- | -------------------------------------------------------------------------------------------------------- |
    | string id                        | Container ID                                                                                             |
    | ContainerMetadata metadata       | Container metadata                                                                                       |
    | ContainerState state             | Container state                                                                                          |
    | int64 created_at                 | Creation timestamps of the container in nanoseconds                                                      |
    | int64 started_at                 | Startup timestamps of the container in nanoseconds                                                       |
    | int64 finished_at                | Exit timestamps of the container in nanoseconds                                                          |
    | int32 exit_code                  | Container exit code                                                                                      |
    | ImageSpec image                  | Image specifications                                                                                     |
    | string image_ref                 | Reference to the image used by the container. For most runtimes, this is an image ID.                    |
    | string reason                    | Brief explanation of why the container is in its current state                                           |
    | string message                   | Human-readable message explaining why the container is in its current state                              |
    | map\<string, string> labels      | Key-value pairs that may be used to identify a single container or a series of containers                |
    | map\<string, string> annotations | Key-value pair holding arbitrary data. The value cannot be modified by the runtime.                      |
    | repeated Mount mounts            | Container mount point information                                                                        |
    | string log_path                  | Container log file path. The file is in the **log_directory** folder configured in **PodSandboxConfig**. |

- **ContainerStatsFilter**

    Filtering conditions when listing container states. The intersection of multiple conditions is displayed.

    | Member                              | Description                                                                            |
    | ----------------------------------- | -------------------------------------------------------------------------------------- |
    | string id                           | Container ID                                                                           |
    | string pod_sandbox_id               | Sandbox ID                                                                             |
    | map\<string, string> label_selector | Container labels. Only full match is supported. Regular expressions are not supported. |

- **ContainerStats**

    Filtering conditions when listing container states. The intersection of multiple conditions is displayed.

    | Member                         | Description                 |
    | ------------------------------ | --------------------------- |
    | ContainerAttributes attributes | Container Information       |
    | CpuUsage cpu                   | CPU usage                   |
    | MemoryUsage memory             | Memory usage                |
    | FilesystemUsage writable_layer | Usage of the writable layer |

- **ContainerAttributes**

    Basic information about the container.

    | Member                          | Description                                                                               |
    | ------------------------------- | ----------------------------------------------------------------------------------------- |
    | string id                       | Container ID                                                                              |
    | ContainerMetadata metadata      | Container metadata                                                                        |
    | map\<string,string> labels      | Key-value pairs that may be used to identify a single container or a series of containers |
    | map\<string,string> annotations | Key-value pair holding arbitrary data. The value cannot be modified by the runtime.       |

- **CpuUsage**

    Container CPU usage.

    | Member                              | Description                        |
    | ----------------------------------- | ---------------------------------- |
    | int64 timestamp                     | Timestamp                          |
    | UInt64Value usage_core_nano_seconds | CPU usage duration, in nanoseconds |

- **MemoryUsage**

    Container memory usage.

    | Member                        | Description  |
    | ----------------------------- | ------------ |
    | int64 timestamp               | Timestamp    |
    | UInt64Value working_set_bytes | Memory usage |

- **FilesystemUsage**

    Usage of the writable layer of the container.

    | Member                       | Description                                                  |
    | ---------------------------- | ------------------------------------------------------------ |
    | int64 timestamp              | Timestamp                                                    |
    | StorageIdentifier storage_id | Writable layer directory                                     |
    | UInt64Value used_bytes       | Number of bytes occupied by the image at the writable layer  |
    | UInt64Value inodes_used      | Number of inodes occupied by the image at the writable layer |

- **Device**

    Host volume to mount into a container.

    | Member | Description |
    | -------------------- | --------------------------------------------------------------------------------------------------------- |
    | string container_path | Mount path within the container |
    | string host_path | Mount path on the host |
    | string permissions | cgroup permissions of the device (**r** allows the container to read from the specified device; **w** allows the container to write to the specified device; **m** allows the container to create device files that do not yet exist).|

- **LinuxContainerConfig**

    Configuration specific to Linux containers.

    | Member                                         | Description                            |
    | ---------------------------------------------- | -------------------------------------- |
    | LinuxContainerResources resources              | Container resource specifications      |
    | LinuxContainerSecurityContext security_context | Linux container security configuration |

- **ContainerConfig**

    Required and optional fields for creating a container.

    | Member                     | Description                                                                                                                                                                                                                                                                       |
    | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | ContainerMetadata metadata | Container metadata. This information uniquely identifies the container, and the runtime should leverage this to ensure correct operation. The runtime may also use this information to improve user experience, such as by constructing a readable container name. (**Required**) |
    | ImageSpec image            | Image used by the container. (Required)                                                                                                                                                                                                                                           |
    | repeated string command    | Command to be executed. The default value is **"/bin/sh"**.                                                                                                                                                                                                                       |
    | repeated string args       | Arguments of the command to be executed                                                                                                                                                                                                                                           |
    | string working_dir         | Current working directory of the command to be executed                                                                                                                                                                                                                           |
    | repeated KeyValue envs     | Environment variables to set in the container                                                                                                                                                                                                                                     |
    | repeated Mount mounts      | Mount points in the container                                                                                                                                                                                                                                                     |
    | repeated Device devices    | Devices to be mapped in the container                                                                                                                                                                                                                                             |
    | mapstring, labels          | Key-value pairs that may be used to index and select individual resources                                                                                                                                                                                                         |
    | mapstring, annotations     | Unstructured key-value map that may be used to store and retrieve arbitrary metadata                                                                                                                                                                                              |
    | string log_path            | Path relative to **PodSandboxConfig.LogDirectory** for container to store the logs (STDOUT and STDERR) on the host                                                                                                                                                                |
    | bool stdin                 | Whether to enable STDIN of the container                                                                                                                                                                                                                                          |
    | bool stdin_once            | Whether to immediately disconnect all data streams connected to STDIN when a data stream connected to stdin is disconnected (**not supported currently**)                                                                                                                         |
    | bool tty                   | Whether to use a pseudo terminal to connect to STDIO of the container                                                                                                                                                                                                             |
    | LinuxContainerConfig linux | Configuration specific to Linux containers                                                                                                                                                                                                                                        |

- **NetworkConfig**

    Runtime network configuration.

    | Member          | Description               |
    | --------------- | ------------------------- |
    | string pod_cidr | CIDR for pod IP addresses |

- **RuntimeConfig**

    Runtime network configuration.

    | Member                       | Description                   |
    | ---------------------------- | ----------------------------- |
    | NetworkConfig network_config | Runtime network configuration |

- **RuntimeCondition**

    Runtime condition information.

    | Member         | Description                                                                   |
    | -------------- | ----------------------------------------------------------------------------- |
    | string type    | Runtime condition type                                                        |
    | bool status    | Runtime status                                                                |
    | string reason  | Brief description of the reason for the runtime condition change              |
    | string message | Human-readable message describing the reason for the runtime condition change |

- **RuntimeStatus**

    Runtime status.

    | Member                               | Description                |
    | ------------------------------------ | -------------------------- |
    | repeated RuntimeCondition conditions | Current runtime conditions |

### Runtime Service

The runtime service contains interfaces for operating pods and containers, and interfaces for querying the configuration and status of the runtime service.

#### RunPodSandbox

#### Interface Prototype

```protobuf
rpc RunPodSandbox(RunPodSandboxRequest) returns (RunPodSandboxResponse) {}
```

#### Interface Description

Creates and starts a pod sandbox. The sandbox is in the ready state on success.

#### Precautions

1. The default image for starting the sandbox is **rnd-dockerhub.huawei.com/library/pause-$\{machine\}:3.0**, where **$\{machine\}** indicates the architecture. On x86\_64, the value of **machine** is **amd64**, on ARM64, the value of **machine** is **aarch64**. Currently, only the **amd64** and **aarch64** images can be downloaded from the rnd-dockerhub repository. If the images do not exist on the host, ensure that the host can download them from the rnd-dockerhub repository.
2. The container names use the field in **PodSandboxMetadata** and are separated by underscores (\_). Therefore, the data in metadata cannot contain underscores. Otherwise, the sandbox runs successfully, but the **ListPodSandbox** interface cannot query the sandbox.

#### Parameter

| Member                  | Description                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------- |
| PodSandboxConfig config | Sandbox configuration                                                                  |
| string runtime_handler  | Runtime to use for the sandbox. Currently, **lcr** and **kata-runtime** are supported. |

#### Returns

| Return                | Description                             |
| --------------------- | --------------------------------------- |
| string pod_sandbox_id | The response data is return on success. |

#### StopPodSandbox

#### Interface Prototype

```protobuf
rpc StopPodSandbox(StopPodSandboxRequest) returns (StopPodSandboxResponse) {}
```

#### Interface Description

Stops the pod sandbox, stops the sandbox container, and reclaims the network resources (such as IP addresses) allocated to the sandbox. If any running container belongs to the sandbox, the container must be forcibly terminated.

#### Parameter

| Member                | Description |
| --------------------- | ----------- |
| string pod_sandbox_id | Sandbox ID  |

#### Returns

| Return | Description |
| ------ | ----------- |
| None   | None        |

#### RemovePodSandbox

#### Interface Prototype

```text
rpc RemovePodSandbox(RemovePodSandboxRequest) returns (RemovePodSandboxResponse) {}
```

#### Interface Description

Removes a sandbox. If there are any running containers in the sandbox, they must be forcibly terminated and removed. This interface must not return an error if the sandbox has already been removed.

#### Precautions

1. When a sandbox is deleted, the network resources of the sandbox are not deleted. Before deleting the pod, you must call **StopPodSandbox** to remove the network resources. Ensure that **StopPodSandbox** is called at least once before deleting the sandbox.
2. If the container in a sandbox fails to be deleted when the sandbox is deleted, the sandbox is deleted but the container remains. In this case, you need to manually delete the residual container.

#### Parameter

| Member                | Description |
| --------------------- | ----------- |
| string pod_sandbox_id | Sandbox ID  |

#### Returns

| Return | Description |
| ------ | ----------- |
| None   | None        |

#### PodSandboxStatus

#### Interface Prototype

```text
rpc PodSandboxStatus(PodSandboxStatusRequest) returns (PodSandboxStatusResponse) {}
```

#### Interface Description

Queries the status of the sandbox. If the sandbox does not exist, this interface returns an error.

#### Parameter

| Member                | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| string pod_sandbox_id | Sandbox ID                                                                         |
| bool verbose          | Whether to return extra information about the sandbox (not configurable currently) |

#### Returns

| Return | Description |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| PodSandboxStatus status | Sandbox status information |
| map\<string, string> info | Extra information of the sandbox. The **key** can be an arbitrary string, and **value** is in JSON format. **info** can include anything debug information. When **verbose** is set to **true**, **info** cannot be empty (not configurable currently). |

#### ListPodSandbox

#### Interface Prototype

```text
rpc ListPodSandbox(ListPodSandboxRequest) returns (ListPodSandboxResponse) {}
```

#### Interface Description

Returns sandbox information. Conditional filtering is supported.

#### Parameter

| Member                  | Description                      |
| ----------------------- | -------------------------------- |
| PodSandboxFilter filter | Conditional filtering parameters |

#### Returns

| Return                    | Description |
| ------------------------- | ----------- |
| repeated PodSandbox items | Sandboxes   |

#### CreateContainer

#### Interface Prototype

```text
rpc CreateContainer(CreateContainerRequest) returns (CreateContainerResponse) {}
```

#### Interface Description

Creates a container in a PodSandbox.

#### Precautions

- **sandbox\_config** in **CreateContainerRequest** is the same as the configuration passed to **RunPodSandboxRequest** to create the PodSandbox. It is passed again for reference. **PodSandboxConfig** is immutable and remains unchanged throughout the lifecycle of a pod.
- The container names use the field in **ContainerMetadata** and are separated by underscores (\_). Therefore, the data in metadata cannot contain underscores. Otherwise, the container runs successfully, but the **ListContainers** interface cannot query the container.
- **CreateContainerRequest** does not contain the **runtime\_handler** field. The runtime type of the created container is the same as that of the corresponding sandbox.

#### Parameter

| Member                          | Description                                               |
| ------------------------------- | --------------------------------------------------------- |
| string pod_sandbox_id           | ID of the PodSandbox where the container is to be created |
| ContainerConfig config          | Container configuration information                       |
| PodSandboxConfig sandbox_config | PodSandbox configuration information                      |

#### Supplementary Information

Unstructured key-value map that may be used to store and retrieve arbitrary metadata. Some fields can be transferred through this field because CRI does not provide specific parameters.

- Customization

    | Custom Key:Value        | Description                                                                        |
    | ----------------------- | ---------------------------------------------------------------------------------- |
    | cgroup.pids.max:int64_t | Limits the number of processes/threads in a container. (Set **-1** for unlimited.) |

#### Returns

| Return              | Description                 |
| ------------------- | --------------------------- |
| string container_id | ID of the created container |

#### StartContainer

#### Interface Prototype

```text
rpc StartContainer(StartContainerRequest) returns (StartContainerResponse) {}
```

#### Interface Description

Starts a container.

#### Parameter

| Member              | Description  |
| ------------------- | ------------ |
| string container_id | Container ID |

#### Returns

| Return | Description |
| ------ | ----------- |
| None   | None        |

#### StopContainer

#### Interface Prototype

```text
rpc StopContainer(StopContainerRequest) returns (StopContainerResponse) {}
```

#### Interface Description

Stops a running container. The graceful stop timeout can be configured. If the container has been stopped, no error can be returned.

#### Parameter

| Member              | Description                                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| string container_id | Container ID                                                                                                                                    |
| int64 timeout       | Waiting time before a container is forcibly stopped. The default value is **0**, indicating that the container is forcibly stopped immediately. |

#### Returns

None

#### RemoveContainer

#### Interface Prototype

```text
rpc RemoveContainer(RemoveContainerRequest) returns (RemoveContainerResponse) {}
```

#### Interface Description

Deletes a container. If the container is running, it must be forcibly stopped. If the container has been deleted, no error can be returned.

#### Parameter

| Member | Description|
| ---------------   --- | ------------- |
| string container_id | Container ID |

#### Returns

None

#### ListContainers

#### Interface Prototype

```text
rpc ListContainers(ListContainersRequest) returns (ListContainersResponse) {}
```

#### Interface Description

Returns container information. Conditional filtering is supported.

#### Parameter

| Member                 | Description                      |
| ---------------------- | -------------------------------- |
| ContainerFilter filter | Conditional filtering parameters |

#### Returns

| Return                        | Description |
| ----------------------------- | ----------- |
| repeated Container containers | Containers  |

#### ContainerStatus

#### Interface Prototype

```text
rpc ContainerStatus(ContainerStatusRequest) returns (ContainerStatusResponse) {}
```

#### Interface Description

Returns container status information. If the container does not exist, an error is returned.

#### Parameter

| Member              | Description                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------- |
| string container_id | Container ID                                                                             |
| bool verbose        | Whether to display additional information about the sandbox (not configurable currently) |

#### Returns

| Return | Description |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| ContainerStatus status | Container status information |
| map\<string, string> info | Extra information of the sandbox. The **key** can be an arbitrary string, and **value** is in JSON format. **info** can include anything debug information. When **verbose** is set to **true**, **info** cannot be empty (not configurable currently).|

#### UpdateContainerResources

#### Interface Prototype

```text
rpc UpdateContainerResources(UpdateContainerResourcesRequest) returns (UpdateContainerResourcesResponse) {}
```

#### Interface Description

Updates container resource configurations.

#### Precautions

- This interface is used exclusively to update the resource configuration of a container, not a pod.
- Currently, the **oom\_score\_adj** configuration of containers cannot be updated.

#### Parameter

| Member                        | Description                              |
| ----------------------------- | ---------------------------------------- |
| string container_id           | Container ID                             |
| LinuxContainerResources linux | Linux resource configuration information |

#### Returns

None

#### ExecSync

#### Interface Prototype

```text
rpc ExecSync(ExecSyncRequest) returns (ExecSyncResponse) {}
```

#### Interface Description

Runs a command synchronously in a container and communicates using gRPC.

#### Precautions

This interface runs a single command and cannot open a terminal to interact with the container.

#### Parameter

| Member | Description |
| ------------------ | ------------------------------------------------------------------ |
| string container_id | Container ID |
| repeated string cmd | Command to be executed |
| int64 timeout | Timeout interval before a command to be stopped is forcibly terminated, in seconds. The default value is **0**, indicating that there is no timeout limit (**not supported currently**).|

#### Returns

| Return          | Description                                                                          |
| --------------- | ------------------------------------------------------------------------------------ |
| bytes stdout    | Captures the standard output of the command                                          |
| bytes stderr    | Captures the standard error output of the command                                    |
| int32 exit_code | Exit code the command finished with. The default value is **0**, indicating success. |

#### Exec

#### Interface Prototype

```text
rpc Exec(ExecRequest) returns (ExecResponse) {}
```

#### Interface Description

Runs a command in the container, obtains the URL from the CRI server using gRPC, and establishes a persistent connection with the WebSocket server based on the obtained URL to interact with the container.

#### Precautions

This interface runs a single command and can open a terminal to interact with the container. One of **stdin**, **stdout**, or **stderr** must be true. If **tty** is true, **stderr** must be false. Multiplexing is not supported. In that case, the outputs of **stdout** and **stderr** are combined into a single stream.

#### Parameter

| Member              | Description                             |
| ------------------- | --------------------------------------- |
| string container_id | Container ID                            |
| repeated string cmd | Command to be executed                  |
| bool tty            | Whether to run the command in a TTY     |
| bool stdin          | Whether to stream standard input        |
| bool stdout         | Whether to stream standard output       |
| bool stderr         | Whether to stream standard error output |

#### Returns

| Return     | Description                                      |
| ---------- | ------------------------------------------------ |
| string url | Fully qualified URL of the exec streaming server |
|            |                                                  |

#### Attach

#### Interface Prototype

```text
rpc Attach(AttachRequest) returns (AttachResponse) {}
```

#### Interface Description

Takes over process 1 of the container, obtains the URL from the CRI server using gRPC, and establishes a persistent connection with the WebSocket server based on the obtained URL to interact with the container.

#### Parameter

| Member              | Description                             |
| ------------------- | --------------------------------------- |
| string container_id | Container ID                            |
| bool tty            | Whether to run the command in a TTY     |
| bool stdin          | Whether to stream standard input        |
| bool stdout         | Whether to stream standard output       |
| bool stderr         | Whether to stream standard error output |

#### Returns

| Return     | Description                                        |
| ---------- | -------------------------------------------------- |
| string url | Fully qualified URL of the attach streaming server |

#### ContainerStats

#### Interface Prototype

```text
rpc ContainerStats(ContainerStatsRequest) returns (ContainerStatsResponse) {}
```

#### Interface Description

Returns information about the resources occupied by a single container. Only containers whose runtime type is lcr are supported.

#### Parameter

| Member              | Description  |
| ------------------- | ------------ |
| string container_id | Container ID |

#### Returns

| Return               | Description                                                                                                                        |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| ContainerStats stats | Container information. Information about drives and inodes can be returned only for containers started using images in oci format. |

#### ListContainerStats

#### Interface Prototype

```text
rpc ListContainerStats(ListContainerStatsRequest) returns (ListContainerStatsResponse) {}
```

#### Interface Description

Returns information about resources occupied by multiple containers. Conditional filtering is supported.

#### Parameter

| Member                      | Description                      |
| --------------------------- | -------------------------------- |
| ContainerStatsFilter filter | Conditional filtering parameters |

#### Returns

| Return                        | Description                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| repeated ContainerStats stats | List of container information. Information about drives and inodes can be returned only for containers started using images in OCI format. |

#### UpdateRuntimeConfig

#### Interface Prototype

```text
rpc UpdateRuntimeConfig(UpdateRuntimeConfigRequest) returns (UpdateRuntimeConfigResponse);
```

#### Interface Description

Provides standard CRI for updating pod CIDR of the network plugin. Currently, the CNI network plugins do not need to update the pod CIDR. Therefore, this interface only records access logs.

#### Precautions

This interface does not modify the system management information, but only records logs.

#### Parameter

| Member                       | Description                                  |
| ---------------------------- | -------------------------------------------- |
| RuntimeConfig runtime_config | Information to be configured for the runtime |

#### Returns

None

#### Status

#### Interface Prototype

```text
rpc Status(StatusRequest) returns (StatusResponse) {};
```

#### Interface Description

Obtains the network status of the runtime and pod. When the network status is obtained, the network configuration is updated.

#### Precautions

If the network configuration fails to be updated, the original configuration is not affected. The original configuration is overwritten only when the network configuration is updated successfully.

#### Parameter

| Member       | Description                                                                 |
| ------------ | --------------------------------------------------------------------------- |
| bool verbose | Whether to display additional runtime information (not supported currently) |

#### Returns

| Return | Description |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| RuntimeStatus status | Runtime status |
| map\<string, string> info | Additional runtime information. The key of **info** can be any value, and the **value** is in JSON format and can contain any debug information. Additional information is displayed only when **Verbose** is set to **true**.|

### Image Service

Provides gRPC APIs for pulling, viewing, and removing images from the image repository.

#### ListImages

#### Interface Prototype

```text
rpc ListImages(ListImagesRequest) returns (ListImagesResponse) {}
```

#### Interface Description

Lists information about existing images.

#### Precautions

This interface is a unified interface. Images of embedded format can be queried using **cri images**. However, because embedded images are not in OCI standard, the query result has the following restrictions:

- The displayed image ID is **digest** of **config** of the image because embedded images do not have image IDs.
- **digest** cannot be displayed because embedded images have only **digest** of **config**, not **digest** of themselves, and **digest** does not comply with OCI specifications.

#### Parameter

| Member           | Description                   |
| ---------------- | ----------------------------- |
| ImageSpec filter | Name of images to be filtered |
|                  |                               |

#### Returns

| Return | Description|
| -------------------- | ------------- |
| repeated Image images | List of images |

#### ImageStatus

#### Interface Prototype

```text
rpc ImageStatus(ImageStatusRequest) returns (ImageStatusResponse) {}
```

#### Interface Description

Queries the details about a specified image.

#### Precautions

1. This interface is used to query information about a specified image. If the image does not exist, **ImageStatusResponse** is returned, in which **Image** is **nil**.
2. This interface is a unified interface. Images of embedded format cannot be queried because they do not comply with the OCI specification and lack some fields.

#### Parameter

| Member          | Description                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| ImageSpec image | Image name                                                                                                 |
| bool verbose    | Queries extra information. This parameter is not supported currently and no extra information is returned. |

#### Returns

| Return                    | Description                                                                                              |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| Image image               | Image information                                                                                        |
| map\<string, string> info | Extra image information. This parameter is not supported currently and no extra information is returned. |

#### PullImage

#### Interface Prototype

```text
rpc PullImage(PullImageRequest) returns (PullImageResponse) {}
```

#### Interface Description

Downloads an image.

#### Precautions

You can download public images or private images using the username, password, and authentication information. The **server_address**, **identity_token**, and **registry_token** fields in **AuthConfig** are not supported.

#### Parameter

| Member                          | Description                                                      |
| ------------------------------- | ---------------------------------------------------------------- |
| ImageSpec image                 | Name of the image to download                                    |
| AuthConfig auth                 | Authentication information for downloading a private image       |
| PodSandboxConfig sandbox_config | Downloads an Image in the pod context (not supported currently). |

#### Returns

| Return           | Description                            |
| ---------------- | -------------------------------------- |
| string image_ref | Information about the downloaded image |
|                  |                                        |

#### RemoveImage

#### Interface Prototype

```text
rpc RemoveImage(RemoveImageRequest) returns (RemoveImageResponse) {}
```

#### Interface Description

Deletes a specified image.

#### Precautions

This interface is a unified interface. Images of embedded format cannot be deleted based on the image ID because they do not comply with the OCI specification and lack some fields.

#### Parameter

| Member          | Description                           |
| --------------- | ------------------------------------- |
| ImageSpec image | Name or ID of the image to be deleted |

#### Returns

None

#### ImageFsInfo

#### Interface Prototype

```text
rpc ImageFsInfo(ImageFsInfoRequest) returns (ImageFsInfoResponse) {}
```

#### Interface Description

Queries information about the file systems of an image.

#### Precautions

The queried information is the file system information in the image metadata.

#### Parameter

None

#### Returns

| Return                                     | Description                   |
| ------------------------------------------ | ----------------------------- |
| repeated FilesystemUsage image_filesystems | Image file system information |

### Constraints

1. If **log_directory** is configured in **PodSandboxConfig** when a sandbox is created, **log_path** must be specified in **ContainerConfig** when a container of the sandbox is created. Otherwise, the container may fail to be started or even deleted using CRI API.

    The actual **LOGPATH** of the container is **log_directory/log_path**. If **log_path** is not configured, the final **LOGPATH** changes to **log_directory**.

    - If the path does not exist, iSulad creates a soft link pointing to the final path of container logs when starting the container, and **log_directory** becomes a soft link. In this case, there are two situations:

    1. If **log_path** is not configured for other containers in the sandbox, when other containers are started, **log_directory** is deleted and points to **log_path** of the newly started container. As a result, the logs of the previously started container point to the logs of the container started later.
    2. If **log_path** is configured for other containers in the sandbox, **LOGPATH** of the container is **log_directory/log_path**. Because **log_directory** is a soft link, if **log_directory/log_path** is used as the soft link target to point to the actual log path of the container, the container creation fails.
    - If the path exists, iSulad attempts to delete the path (non-recursively) when starting the container. If the path is a folder that contains content, the deletion fails. As a result, the soft link fails to be created and the container fails to be started. When the container is deleted, the same symptom occurs. As a result, the container deletion fails.
2. If **log_directory** is configured in **PodSandboxConfig** when a sandbox is created and **log_path** is configured in **ContainerConfig** when a container is created, the final **LOGPATH** is **log_directory/log_path**. iSulad does not create **LOGPATH** recursively. Therefore, you must ensure that **dirname(LOGPATH)**, that is, the parent directory of the final log directory, exists.
3. If **log_directory** is configured in **PodSandboxConfig** when a sandbox is created, and the same **log_path** is specified in **ContainerConfig** when two or more containers are created or containers in different sandboxes point to the same **LOGPATH**, when the containers are started successfully, the log path of the container that is started later overwrites that of the container that is started earlier.
4. If the image content in the remote image repository changes and the CRI image pulling interface is used to download the image again, the image name and tag of the local original image (if it exists) change to "none."

    Example:

    Local image:

    ```text
    IMAGE                                        TAG                 IMAGE ID            SIZE
    rnd-dockerhub.huawei.com/pproxyisulad/test   latest              99e59f495ffaa       753kB
    ```

    After the **rnd-dockerhub.huawei.com/pproxyisulad/test:latest** image in the remote repository is updated and downloaded again:

    ```text
    IMAGE                                        TAG                 IMAGE ID            SIZE
    <none>                                       <none>              99e59f495ffaa       753kB
    rnd-dockerhub.huawei.com/pproxyisulad/test   latest              d8233ab899d41       1.42MB
    ```

    Run the `isula images` command. **REF** is displayed as **-**.

    ```text
    REF                                               IMAGE ID               CREATED              SIZE   
    rnd-dockerhub.huawei.com/pproxyisulad/test:latest d8233ab899d41          2019-02-14 19:19:37  1.42MB   
    -                                                 99e59f495ffaa          2016-05-04 02:26:41  753kB
    ```

5. The exec and attach interfaces of iSulad CRI API are implemented using WebSocket. Clients interact with iSulad using the same protocol. When using the exec or attach interface, do not transfer a large amount of data or files over the serial port. The exec or attach interface is used only for basic command interaction. If the user side does not process the data or files in a timely manner, data may be lost. In addition, do not use the exec or attach interface to transfer binary data or files.
6. The iSulad CRI API exec/attach depends on libwebsockets (LWS). It is recommended that the streaming API be used only for persistent connection interaction but not in high-concurrency scenarios, because the connection may fail due to insufficient host resources. It is recommended that the number of concurrent connections be less than or equal to 100.
