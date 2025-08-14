# Usage Instructions

<!-- TOC -->

- [Usage Instructions](#usage-instructions)
    - [Precautions](#precautions)
    - [OS CR Parameters](#os-cr-parameters)
    - [Upgrade](#upgrade)
    - [Settings](#settings)
    - [Rollback](#rollback)
    - [Appendixes](#appendixes)
        - [Settings List](#settings-list)
            - [kernel Settings](#kernel-settings)
            - [GRUB Settings](#grub-settings)

<!-- /TOC -->
## Precautions

- General precautions
    - KubeOS currently only supports virtual machines (VMs) and physical machines using UEFI with x86 and AArch64 architectures.
    - When creating or updating the OS CustomResource (CR) using `kubectl apply` with a YAML file, avoid concurrent `apply` operations. Excessive concurrent requests may overwhelm the kube-apiserver, leading to failures.
    - If you configure certificates or keys for the container image registry, ensure that the permissions on these files are set to the minimum necessary.
- Upgrade precautions
    - Upgrades are performed as atomic upgrades for all packages. Individual package upgrades are not supported.
    - Upgrades use a dual-partition upgrade strategy. Configurations with more than two partitions are not supported.
    - Cross-major version upgrades are not currently supported.
    - Logs for the upgrade process on a single node can be found in the **/var/log/messages** file on that node.
    - Strictly adhere to the provided upgrade and rollback procedures. Deviation from the prescribed order of operations may result in upgrade or rollback failures.
    - If you need to configure private images for `ctr` (used by `containerd`) on a node, place the **host.toml** configuration file in the `/etc/containerd/certs.d` directory, following the `ctr` guidelines.
    - Upgrades using OCI images and mutual TLS (mTLS) authentication are only supported on openEuler 22.09 and later.
    - Features `nodeselector`, `executionmode`, `timewindow`, and `timeinterval` are only supported on openEuler 24.09 and later.
    - KubeOS 24.09 is not compatible with previous versions.

- Configuration Precautions
    - Users are responsible for the security and reliability of any custom configurations, particularly persistent configurations such as `kernel.sysctl.persist`, `grub.cmdline.current`, and `grub.cmdline.next`. KubeOS does not validate the effectiveness of these parameters.
    - When `opstype` is set to `config`, configurations will not be applied if the specified `osversion` does not match the OS version of the target nodes in the cluster.
    - Currently, only temporary kernel parameter configuration (`kernel.sysctl`), persistent kernel parameter configuration (`kernel.sysctl.persist`), and GRUB command line configuration (`grub.cmdline.current` and `grub.cmdline.next`) are supported.
    - Persistent configurations are written to the persistent partition and will be retained after upgrades and reboots. Temporary kernel parameter configurations will not be retained after a reboot.
    - When configuring `grub.cmdline.current` or `grub.cmdline.next`, if a single parameter is provided (not in the `key=value` format), specify the parameter as the key and leave the value empty.
    - When deleting a configuration (`operation=delete`), ensure that the key and value in the `key=value` format match the actual configuration.
    - Configuration changes cannot be rolled back. If a rollback is required, modify the configuration version and content and reapply the configuration.
    - If a configuration error occurs and a node enters the `config` state, revert the configuration version to the previous version and reapply it. This should return the node to the `idle` state. However, note that parameters successfully configured before the error occurred cannot be reverted.
    - When configuring `grub.cmdline.current` or `grub.cmdline.next`, if you need to update an existing parameter in the format of `key=value` to a format with only key and no value, for example, updating `rd.info=0` to `rd.info`, you need to delete `key=value` first, and then add the key in the next configuration. Direct updates or updates and deletions in the same operation are not supported.

## OS CR Parameters

Create a custom object of the OS type in the cluster and set the corresponding fields. The OS type comes from the CRD object created in the installation and deployment sections. The following describes the fields.

- The `imageurl` field specifies the location of the operating system image. This URL must use either the `http` or `https` protocol. For `https`, the image transfer is secure. For `http`, you must set the `flagSafe` parameter to `true`. This explicitly signals that you trust the source and allows the image download to proceed. If `imageurl` uses `http` and `flagSafe` is not `true`, the URL is considered unsafe, the image will not be downloaded, and an error message will appear in the node upgrade log.
- You are advised to use the `https` protocol for security. When using `https`, ensure that the target machines being upgraded have the necessary certificates installed. If you maintain the image server yourself, you must sign the images to guarantee their authenticity and ensure the nodes being upgraded trust your certificate. Place the certificate file in the `/etc/KubeOS/certs` directory. The administrator provides the `imageurl` and is responsible for ensuring the security and validity of this URL. An internal network address is recommended for enhanced security.
- The provider of the container OS image is responsible for its integrity. Verify that you obtain images from a trustworthy source.
- When your cluster uses multiple OS versions (meaning that there are multiple OS instances), each OS must have a distinct `nodeselector`. This ensures that a group of nodes identified by a specific label corresponds to only one OS instance.
    - If an OS instance has `nodeselector` set to `all-label`, it will be the only valid instance in the cluster (only nodes matching its criteria will be managed).
    - Similarly, only one OS instance can have an unconfigured `nodeselector`. This is because an absent `nodeselector` is interpreted as targeting nodes without any labels.
- `timewinterval` parameter
    - When not set, the default value is 15 seconds.
    - Setting this parameter to `0` will cause the task dispatch interval of the operator to gradually increase until it reaches 1000 seconds. This behavior is due to rate limiting imposed by the Kubernetes `controller-runtime`.
    - In parallel execution mode, `timeinterval` defines the delay between the operator dispatching upgrade/configuration tasks for each batch of nodes.
    - In serial execution mode,  `timeinterval`  represents the delay between the completion of one batch of nodes (upgraded/configured serially) and the dispatch of the next upgrade/configuration task. Within a batch, the interval between individual nodes remains 15 seconds.
    - Any update to fields of an OS instance will immediately trigger the operator.

  | Parameter        | Type   | Description                                                                                      | Usage Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Mandatory                             |
  | ---------------- | ------ | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
  | `imagetype`      | string | Type of image used for the upgrade                                                               | The value can be `docker`, `containerd`, or `disk` and is valid only for upgrades. **Note:** When the value is `containerd`, the agent prioritizes the `crictl` tool for pulling images. If `crictl` is unavailable, it uses the `ctr` command. When `ctr` is used to pull images from a private repository, configure the repository host information in the **/etc/containerd/certs.d** directory according to the [containerd official documentation](https://github.com/containerd/containerd/blob/main/docs/hosts.md).                                                                                                                                                                                                                               | Yes                                   |
  | `opstype`        | string | Operation type (upgrade, configuration, or rollback)                                             | The value can be  `upgrade`, `config`, or `rollback`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Yes                                   |
  | `osversion`      | string | Target version for the upgrade or rollback                                                       | `osversion` must match the target OS version of the nodes (specified in the `PRETTY_NAME` field in the **/etc/os-release** file or the OS version detected by Kubernetes). For example: `KubeOS 1.0.0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Yes                                   |
  | `maxunavailable` | int    | Maximum number of nodes undergoing upgrade/configuration/rollback concurrently                   | If `maxunavailable` exceeds the actual number of nodes, the operation proceeds with the actual number of nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Yes                                   |
  | `containerimage` | string | Container image used for the upgrade                                                             | This parameter is only applicable when `imagetype` is a container type. The value can be one of the three container image address formats: `repository/name`, `repository/name@sha256:xxxx`, and `repository/name:tag`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Yes                                   |
  | `imageurl`       | string | URL of the drive image used for the upgrade                                                      | `imageurl` must include the protocol and supports only `http` or `https`. Example: `https://192.168.122.15/update.img`. Valid only for upgrades using drive images.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Yes                                   |
  | `checksum`       | string | Checksum (SHA-256) of the drive image used for the upgrade or the digests of the container image | This parameter is valid only for upgrades.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Yes                                   |
  | `flagSafe`       | bool   | Whether the address specified by `imageurl` is safe when the `http` protocol is used             | The value must be `true` or `false`. This parameter is valid only when `imageurl` uses the `http` protocol.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Yes                                   |
  | `mtls`           | bool   | Whether the connection to `imageurl` uses two-way HTTPS authentication                           | The value must be `true` or `false`. This parameter is valid only when `imageurl` uses the `https` protocol.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Yes                                   |
  | `cacert`         | string | Root certificate file used for HTTPS or two-way HTTPS authentication                             | This parameter is valid only when `imageurl` uses the `https` protocol.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Required when `imageurl` uses `https` |
  | `clientcert`     | string | Client certificate file used for two-way HTTPS authentication                                    | This parameter is valid only when two-way HTTPS authentication is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Required when `mtls` is `true`        |
  | `clientkey`      | string | Client private key file used for two-way HTTPS authentication                                    | This parameter is valid only when two-way HTTPS authentication is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Required when `mtls` is `true`        |
  | `evictpodforce`  | bool   | Whether to forcibly evict pods during upgrade/rollback                                           | Must be `true` or `false`. This parameter is valid only for upgrades or rollbacks.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Yes                                   |
  | `sysconfigs`     | /      | Configuration settings                                                                           | 1. When `opstype` is `config`, only configuration is performed. <br>  2. When `opstype` is `upgrade/rollback`, it indicates post-upgrade/rollback configuration, meaning it takes effect after the upgrade/rollback and subsequent reboot. For detailed field descriptions, see the [Settings](#settings).                                                                                                                                                                                                                                                                                                                                                                                                                                               | Required when `opstype` is `config`   |
  | `upgradeconfigs` | /      | Configuration settings to apply before an upgrade.                                               | This parameter is valid for upgrades or rollbacks and takes effect before the upgrade or rollback operation. For detailed field descriptions, see the [Settings](#settings).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Optional                              |
  | `nodeselector`   | string | Label of the nodes targeted for the upgrade/configuration/rollback                               | This parameter is used to perform operations on nodes with specific labels, rather than all worker nodes in the cluster. The nodes targeted for the operation need to have a label with the `upgrade.openeuler.org/node-selector` key. The `nodeselector` parameter should be set to the value of this label. **Notes:**  1. When this parameter is not set or is set to `no-label`, operations are performed on nodes that do not have the `upgrade.openeuler.org/node-selector`  label. <br> 2. When this parameter is set to `""` (an empty string), operations are performed on nodes that have the `upgrade.openeuler.org/node-selector=""` label. <br>3. To ignore labels and perform operations on all nodes, set this parameter to `all-label`. | Optional                              |
  | `timewindow`     | /      | Time window during which the upgrade/configuration/rollback can take place.                      | 1. When specifying a time window, both `starttime` and `endtime` must be specified. That is, they should either both be empty or both be non-empty.<br>1. Both `starttime` and `endtime` are strings and should be in the `YYYY-MM-DD HH:MM:SS` or `HH:MM:SS` format, and both should follow the same format. <br>2. When in `HH:MM:SS` format, if `starttime` is less than `endtime`, it is assumed that `starttime` refers to that time on the next day. <br>3. When `timewindow` is not specified, it defaults to no time window restrictions.                                                                                                                                                                                                      | Optional                              |
  | `timeinterval`   | int    | The time interval between each batch of tasks for the upgrade/configuration/rollback operation.  | This parameter is in seconds and defines the time interval between the operator dispatching tasks. If the Kubernetes cluster is busy and cannot immediately respond to the operator's request, the actual interval may be longer than the specified time.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Optional                              |
  | `executionmode`  | string | The mode in which the upgrade/configuration/rollback operation is executed.                      | The value can be `serial` or `parallel`. If this parameter is not set, the operation defaults to parallel mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Optional                              |

## Upgrade

1. Create a YAML file and deploy an instance of the OS Custom Resource (CR) in the cluster. This YAML file defines the upgrade process. The following example assumes you save the YAML content to **upgrade_v1alpha1_os.yaml**.

    - Upgrade using a drive image

        ```yaml
        apiVersion: upgrade.openeuler.org/v1alpha1
        kind: OS
        metadata:
            name: os-sample
        spec:
            imagetype: disk
            opstype: upgrade
            osversion: edit.os.version
            maxunavailable: edit.node.upgrade.number
            containerimage: ""
            evictpodforce: true/false
            imageurl: edit.image.url
            checksum: image.checksum
            flagSafe: imageurl.safety
            mtls: imageurl use mtls or not
            cacert:  ca certificate 
            clientcert:  client certificate 
            clientkey:  client certificate key 
        ```

    - Upgrade using a container image
        - Before you can upgrade using a container image, you need to create a container image specifically for the upgrade process. For detailed instructions on how to create this image, see [Creating a KubeOS OCI Image](./kubeos_image_creation.md#creating-a-kubeos-oci-image) in [KubeOS Image Creation](./kubeos_image_creation.md).

        ``` yaml
        apiVersion: upgrade.openeuler.org/v1alpha1
        kind: OS
        metadata:
            name: os-sample
        spec:
            imagetype: docker
            opstype: upgrade
            osversion: edit.os.version
            maxunavailable: edit.node.upgrade.number
            containerimage: container image like repository/name:tag
            evictpodforce: true/false
            imageurl: ""
            checksum: container image digests
            flagSafe: false
            mtls: true
        ```

        - Using containerd as the container engine

        ```yaml
        apiVersion: upgrade.openeuler.org/v1alpha1
        kind: OS
        metadata:
            name: os-sample
        spec:
            imagetype: containerd
            opstype: upgrade
            osversion: edit.os.version
            maxunavailable: edit.node.upgrade.number
            containerimage: container image like repository/name:tag
            evictpodforce: true/false
            imageurl: ""
            checksum: container image digests
            flagSafe: false
            mtls: true
        ```

        - Example of upgrading and applying configurations
            - This example uses containerd as the container engine. The upgrade method does not affect the configuration process. `upgradeconfigs` are applied before the upgrade. `sysconfigs` are applied after the machine reboots from the upgrade. See [Settings](#settings) for detailed information about the configuration parameters.
            - When upgrading and configuring, set the `opstype` field to `upgrade`.

            ```yaml
            apiVersion: upgrade.openeuler.org/v1alpha1
            kind: OS
            metadata:
                name: os-sample
            spec:
                imagetype: ""
                opstype: upgrade
                osversion: edit.os.version
                maxunavailable: edit.node.upgrade.number
                containerimage: ""
                evictpodforce: true/false
                imageurl: ""
                checksum: container image digests
                flagSafe: false
                mtls: false
                sysconfigs:
                    version: edit.os.version
                    configs:
                        - model: kernel.sysctl
                        contents:
                            - key: kernel param key1
                            value: kernel param value1
                            - key: kernel param key2
                            value: kernel param value2
                        - model: kernel.sysctl.persist
                        configpath: persist file path
                        contents:
                            - key: kernel param key3
                            value: kernel param value3
                            - key: ""
                            value: ""
                upgradeconfigs:
                    version: 1.0.0
                    configs:
                        - model: kernel.sysctl
                        contents:
                            - key: kernel param key4
                            value: kernel param value4          
            ```

        - Example of upgrading specific nodes using `nodeselector`, `timewindow`, `timeinterval`, and `executionmode`
            - This example uses containerd as the container engine. The upgrade method does not affect node selection.
            - Nodes targeted for upgrade must include the `upgrade.openeuler.org/node-selector` label. The value of `nodeselector` in the YAML file should match the value of this label on the desired nodes. For example, if `nodeselector` is set to `kubeos`, only worker nodes with the `upgrade.openeuler.org/node-selector=kubeos` label will be upgraded.
            - `nodeselector`, `timewindow`, `timeinterval`, and `executionmode` are also applicable to configuration and rollback operations.
            - Example commands for managing node labels:

            ``` shell
            # Add a label to node kubeos-node1
            kubectl label nodes kubeos-node1 upgrade.openeuler.org/node-selector=kubeos-v1
            # Modify the label of node kubeos-node1
            kubectl label --overwrite nodes kubeos-node1 upgrade.openeuler.org/node-selector=kubeos-v2
            # Delete the label from node kubeos-node1
            kubectl label nodes kubeos-node1 upgrade.openeuler.org/node-selector-
            # View the labels of all nodes
            kubectl get nodes --show-labels
            ```

            - Example YAML file:

            ```yaml
            apiVersion: upgrade.openeuler.org/v1alpha1
            kind: OS
            metadata:
                name: os-sample
            spec:
                imagetype: containerd
                opstype: upgrade
                osversion: edit.os.version
                maxunavailable: edit.node.upgrade.number
                containerimage: container image like repository/name:tag
                evictpodforce: true/false
                imageurl: ""
                checksum: container image digests
                flagSafe: false
                mtls: true
                nodeselector: edit.node.label.key
                timewindow:
                starttime: "HH::MM::SS/YYYY-MM-DD HH::MM::SS"
                endtime: "HH::MM::SS/YYYY-MM-DD HH::MM::SS"
                timeinterval: time intervel like 30
                executionmode: serial/parallel
            ```

2. Check the OS version of nodes that have not been upgraded.

    ```shell
    kubectl get nodes -o custom-columns='NAME:.metadata.name,OS:.status.nodeInfo.osImage'
    ```

3. Deploy the CR instance in the cluster. Nodes will be upgraded based on the parameters specified in the YAML file.

    ```shell
    kubectl apply -f upgrade_v1alpha1_os.yaml
    ```

4. Check the OS version of the nodes again to confirm if the upgrade is complete.

    ```shell
    kubectl get nodes -o custom-columns='NAME:.metadata.name,OS:.status.nodeInfo.osImage'
    ```

5. If you need to perform the upgrade again, modify the corresponding fields in **upgrade_v1alpha1_os.yaml**.

> [!NOTE]Note
>
> If you need to perform the upgrade again, modify the `imageurl`, `osversion`, `checksum`, `maxunavailable`, `flagSafe`, or `dockerimage` parameters in **upgrade_v1alpha1_os.yaml**.

## Settings

- Settings parameters

    This section describes the configuration parameters using an example YAML file. Your configuration should follow the same indentation as the example:

    ```yaml
    apiVersion: upgrade.openeuler.org/v1alpha1
    kind: OS
    metadata:
        name: os-sample
    spec:
        imagetype: ""
        opstype: config
        osversion: edit.os.version
        maxunavailable: edit.node.config.number
        containerimage: ""
        evictpodforce: false
        checksum: ""
        sysconfigs:
            version: edit.sysconfigs.version
            configs:
                - model: kernel.sysctl
                contents: 
                    - key: kernel param key1
                    value: kernel param value1
                    - key: kernel param key2
                    value: kernel param value2
                    operation: delete
                - model: kernel.sysctl.persist
                configpath: persist file path
                contents:
                    - key: kernel param key3
                    value: kernel param value3
                - model: grub.cmdline.current
                contents:
                    - key: boot param key1
                    - key: boot param key2
                    value: boot param value2
                    - key: boot param key3
                    value: boot param value3
                    operation: delete
                - model: grub.cmdline.next
                contents:
                    - key: boot param key4
                    - key: boot param key5
                    value: boot param value5
                    - key: boot param key6
                    value: boot param value6
                    operation: delete         
    ```

    Configuration parameters

    | Parameter       | Type | Description                    | Usage Note                                                     | Mandatory          |
    | ---------- | -------- | --------------------------- | ------------------------------------------------------------ | ----------------------- |
    | `version` | string | Configuration version | This parameter determines if the configuration should be applied by comparing versions. If `version` is empty (`""` or not set), the comparison will still be performed. Therefore, if `sysconfigs` or `upgradeconfigs` is not configured, the existing `version` will be cleared, triggering the configuration. | Yes |
    | `configs` | / | Specific configuration content | This parameter contains a list of specific configuration items. | Yes |
    | `model` | string | Configuration type | See the [Settings List](#settings-list) in the appendix for supported configuration types. | Yes |
    | `configpath` | string | Configuration file path | This parameter is only effective for the `kernel.sysctl.persist` configuration type. See the [Settings List](#settings-list) in the appendix for the description of the configuration file path. | No |
    | `contents` | / | Specific key/value pairs and operation type | This parameter contains a list of specific configuration items. | Yes |
    | `key` | string | Parameter name | `key` cannot be empty or contain `=`. You are advised not to configure strings containing spaces or tabs. For specific usage of `key` for each configuration type, see the [Settings List](#settings-list) in the appendix. | Yes |
    | `value` | string | Parameter value | `value` cannot be empty for parameters in the `key=value` format. You are advised not to configure strings containing spaces or tabs. For specific usage of `value` for each configuration type, see the [Settings List](#settings-list) in the appendix. | Required for parameters in the `key=value` format |
    | `operation` | string | Operation to be performed on the parameter | This parameter is only effective for `kernel.sysctl.persist`, `grub.cmdline.current`, and `grub.cmdline.next` parameter types. The default behavior is to add or update. The value can only be `delete`, which means deleting the existing parameter (the `key=value` must match exactly for deletion). | No |

    - `upgradeconfigs` has the same parameters as `sysconfigs`. `upgradeconfigs` is for configuration before upgrade/rollback and only takes effect in upgrade/rollback scenarios. `sysconfigs` supports both configuration only and configuration after upgrade/rollback reboot.

- Usage

    1. Create a YAML file like the **upgrade_v1alpha1_os.yaml** example above and deploy the OS CR instance in the cluster.

    2. Check the configuration version and node status before applying the configuration (`NODESTATUS` should be `idle`).

        ```shell
        kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
        ```

    3. Apply the configuration, then check the node status again (`NODESTATUS` should change to `config`).

        ```shell
        kubectl apply -f upgrade_v1alpha1_os.yaml
        kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
        ```

    4. Check the node configuration version again to confirm whether the configuration is complete (`NODESTATUS` should return to `idle`):

        ```shell
        kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
        ```

- If you need to perform the configuration again, modify the corresponding fields in **upgrade_v1alpha1_os.yaml**.

## Rollback

- Scenarios
    - When a VM fails to start, you can manually select the previous version from the GRUB boot menu. This method only supports rollback to the previous version.
    - When a VM starts successfully and you can access the system, you can use the rollback tool (recommended) or manually select the previous version from the GRUB boot menu.
    - You can use the rollback tool in two ways:
    1. Rollback mode: reverts to the previous version.
    2. Upgrade mode: re-upgrades to the previous version.

- Manual rollback instructions
    - Restart the VM and select the second boot option in the GRUB boot menu to roll back to the previous version.

- Rollback tool instructions
    - Rolling back to any version
        1. Modify the YAML configuration file of the OS CR instance (for example, **upgrade_v1alpha1_os.yaml**). Set the relevant fields to the image information of the desired version. The OS category originates from the CRD object created in the installation and deployment document. Refer to the upgrade instructions in the previous section for field descriptions and examples.
        2. After modifying the YAML file, execute the update command. Nodes will then roll back according to the configured field information.

            ```shell
            kubectl apply -f upgrade_v1alpha1_os.yaml
            ```

    - Rolling back to the previous version
        - To roll back to the previous OS version, modify the **upgrade_v1alpha1_os.yaml** file. Set `osversion` to the previous version and `opstype` to `rollback` to roll back to the previous version (that is, switch to the previous partition). Example YAML file:

        ```yaml
        apiVersion: upgrade.openeuler.org/v1alpha1
        kind: OS
        metadata:
        name: os-sample
        spec:
            imagetype: ""
            opstype: rollback
            osversion: KubeOS previous version
            maxunavailable: 2
            containerimage: ""
            evictpodforce: true/false
            imageurl: ""
            checksum: ""
            flagSafe: false
            mtls: true
        ```

        - To roll back to the previous configuration version (note that already configured parameters cannot be rolled back), modify the `upgrade_v1alpha1_os.yaml` file. Set `version` of `sysconfigs/upgradeconfigs` to the previous version. Example YAML file:

        ```yaml
            apiVersion: upgrade.openeuler.org/v1alpha1
            kind: OS
            metadata:
                name: os-sample
            spec:
                imagetype: ""
                opstype: config
                osversion: edit.os.version
                maxunavailable: edit.node.config.number
                containerimage: ""
                evictpodforce: true/false
                imageurl: ""
                checksum: ""
                flagSafe: false
                mtls: false
                sysconfigs:
                    version: previous config version
                    configs:
                        - model: kernel.sysctl
                        contents:
                            - key: kernel param key1
                            value: kernel param value1
                            - key: kernel param key2
                            value: kernel param value2
                        - model: kernel.sysctl.persist
                        configpath: persist file path
                        contents:
                            - key: kernel param key3
                            value: kernel param value3         
            ```

    - After modifying the YAML file and executing the update command, the nodes will roll back based on the configured information.

    ```shell
    kubectl apply -f upgrade_v1alpha1_os.yaml
    ```

    - Verify that the rollback was successful.
        - To check the container OS version (for OS version rollback), verify container OS version of the node. To check the configuration version (for configuration rollback), verify the node configuration version and that the node status is `idle`.

        ```shell
        kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
        ```

## Appendixes

### Settings List

#### kernel Settings

- `kernel.sysctl`: temporarily sets kernel parameters. These settings will be lost after a reboot. The key/value pairs represent key/value pairs of kernel parameters. Both keys and values cannot be empty. Keys cannot contain the `=` character. The value of `operation` cannot be `delete`. Example:

    ```yaml
    configs:
      - model: kernel.sysctl
        contents:
            - key: user.max_user_namespaces
              value: 16384
            - key: net.ipv4.tcp_tw_recycle
              value: 0
              operation: delete
    ```

- `kernel.sysctl.persist`: sets persistent kernel parameters that will be retained after a reboot. The key/value pairs represent key/value pairs of kernel parameters. Both keys and values cannot be empty. Keys cannot contain the `=` character. `configpath` specifies the path to the configuration file, which can be a new file (given that the parent directory exists). If not specified, it defaults to **/etc/sysctl.conf**. Example:

    ```yaml
    configs:
      - model: kernel.sysctl.persist
        configpath : /etc/persist.conf
        contents:
            - key: user.max_user_namespaces
              value: 16384
            - key: net.ipv4.tcp_tw_recycle
              value: 0
              operation: delete
    ```

#### GRUB Settings

- `grub.cmdline.current/next`: sets the kernel boot parameters in the **grub.cfg** file. These parameters appear on the line resembling the following example in **grub.cfg**:

    ```text
    linux   /boot/vmlinuz root=/dev/sda2 ro rootfstype=ext4 nomodeset quiet oops=panic softlockup_panic=1 nmi_watchdog=1 rd.shell=0 selinux=0 crashkernel=256M panic=3
    ```

    - The `grub.cmdline.current/next` settings allow configuration for either the current or the next partition:

        - `grub.cmdline.current`: Configures the boot parameters for the current partition.
        - `grub.cmdline.next`: Configures the boot parameters for the next partition.

    - Note: During upgrades/rollbacks, the `current` and `next` partition designations in the configuration (`sysconfigs`) are determined at the time the upgrade/rollback operation is initiated. For instance, if the current partition is `A` and an upgrade is initiated with `grub.cmdline.current` configured in `sysconfigs`, the configuration will still be applied to partition `A` after the reboot, even though it may no longer be the `current` partition.

    - `grub.cmdline.current/next` supports both `key=value` (where `value` cannot be empty) and single `key` formats. If `value` contains an equal sign (for example, `root=UUID=some-uuid`), `key` should be set to all characters before the first `=` and `value` should be set to all characters after the first `=`. Example:

    ```yaml
    configs:
    - model: grub.cmdline.current
      contents:
          - key: selinux
            value: "0"
          - key: root
            value: UUID=e4f1b0a0-590e-4c5f-9d8a-3a2c7b8e2d94
          - key: panic
            value: "3"
            operation: delete
          - key: crash_kexec_post_notifiers
    - model: grub.cmdline.next
      contents:
          - key: selinux
            value: "0"
          - key: root
            value: UUID=e4f1b0a0-590e-4c5f-9d8a-3a2c7b8e2d94
          - key: panic
            value: "3"
            operation: delete
          - key: crash_kexec_post_notifiers
    ```
