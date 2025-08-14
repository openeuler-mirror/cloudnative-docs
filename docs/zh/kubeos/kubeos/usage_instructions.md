# 使用方法

## 注意事项

* 公共注意事项
    * 仅支持虚拟机和物理机x86和arm64 UEFI场景。
    * 使用kubectl apply通过YAML创建或更新OS的CR时，不建议并发apply，当并发请求过多时，kube-apiserver会无法处理请求导致失败。
    * 如用户配置了容器镜像仓的证书或密钥，请用户保证证书或密钥文件的权限最小。
* 升级注意事项
    * 升级为所有软件包原子升级，默认不提供单包升级能力。
    * 升级为双区升级的方式，不支持更多分区数量。
    * 当前暂不支持跨大版本升级。
    * 单节点的升级过程的日志可在节点的 /var/log/messages 文件查看。
    * 请严格按照提供的升级和回退流程进行操作，异常调用顺序可能会导致系统无法升级或回退。
    * 节点上containerd如需配置ctr使用的私有镜像，请将配置文件host.toml按照ctr指导放在/etc/containerd/certs.d目录下。
    * 使用OCI 镜像升级和mtls双向认证仅支持 openEuler 22.09 及之后的版本。
    * nodeselector、executionmode、timewindow和timeinterval 仅支持openEuler 24.09及之后版本。
    * KubeOS 24.03-LTS-SP1 版本与历史版本不兼容。
    * 使用从http/https服务器下载升级镜像功能需要同步使用对应版本镜像制作工具。

* 配置注意事项
    * 用户自行指定配置内容，用户需保证配置内容安全可靠 ，尤其是持久化配置（kernel.sysctl.persist、grub.cmdline.current、grub.cmdline.next、kubernetes.kubelet、container.containerd、pam.limits），KubeOS不对参数有效性进行检验。
    * opstype=config时，若osversion与当前集群节点的OS版本不一致，配置不会进行。
    * 当前仅支持kernel参数临时配置（kernel.sysctl）、持久化配置（kernel.sysctl.persist）和grub cmdline配置（grub.cmdline.current和grub.cmdline.next）、kubelet配置（kubernetes.kubelet）、containerd配置（container.containerd）和pam limits配置（pam.limits）。
    * 持久化配置会写入persist持久化分区，升级重启后配置保留；kernel参数临时配置重启后不保留。
    * 配置grub.cmdline.current或grub.cmdline.next时，如为单个参数（非key=value格式参数），请指定key为该参数，value为空。
    * 进行配置删除（operation=delete）时，key=value形式的配置需保证key、value和实际配置一致。
    * 配置不支持回退，如需回退，请修改配置版本和配置内容，重新下发配置。
    * 配置出现错误，节点状态陷入config时，请将配置版本恢复成上一版本并重新下发配置，从而使节点恢复至idle状态。 但是请注意：出现错误前已经配置完成的参数无法恢复。
    * 在配置grub.cmdline.current或grub.cmdline.next时，若需要将已存在的“key=value”格式的参数更新为只有key无value格式，比如将“rd.info=0”更新成rd.info，需要先删除“key=value”，然后在下一次配置时，添加key。不支持直接更新或者更新删除动作在同一次完成。

## OS CR参数说明

在集群中创建类别为OS的定制对象，设置相应字段。类别OS来自于[安装和部署章节](./installation_and_deployment.md)创建的CRD对象，字段及说明如下：

* imageurl指定的地址里包含协议，只支持http或https协议。imageurl为https协议时为安全传输，imageurl为http地址时，需指定flagSafe为true，即用户明确该地址为安全时，才会下载镜像。如imageurl为http地址且没有指定flagSafe为true，默认该地址不安全，不会下载镜像并且在升级节点的日志中提示用户该地址不安全。
* 对于imageurl，推荐使用https协议，使用https协议需要升级的机器已安装相应证书。如果镜像服务器由用户自己维护，需要用户自己进行签名，并保证升级节点已安装对应证书。用户需要将证书放在容器OS```/etc/KubeOS/certs```目录下。地址由管理员传入，管理员应该保证网址的安全性，推荐采用内网地址。
* 容器OS镜像的合法性检查需要由容器OS镜像服务提供者做合法性检查，确保下载的容器OS镜像来源可靠。
* 集群存在多OS版本即存在多个OS的实例时，OS的nodeselector字段需要与其他OS不同，即通过label区分的一类node只能对应一个OS实例：
    * 当有OS的nodeselector为all-label时，集群只能存在这一个OS的有效实例（有效实例为存在与这个OS对应的节点）。
    * nodeselector不配置的OS也只能有一个，因为nodeselector不配置时认为是对没有label的节点进行操作。
* timewinterval参数说明：
    * 参数不设置时默认为15s。
    * 参数设置为0时，由于k8s controller-runtime的rate limit限制，operator下发任务的时间间隔会逐渐增加直至1000s。
    * 并行时为每批次operator下发升级/配置的时间间隔。
    * 在串行时为每批次节点串行升级完毕后与下次升级/配置下发的时间间隔，批次内部的时间间隔为15s。
    * OS的实例字段进行更新会立刻触发operator。

  | 参数            |参数类型  | 参数说明                                                     | 使用说明 | 是否必选         |
  | -------------- | ------ | ------------------------------------------------------------ | ----- | ---------------- |
  | imagetype      | string | 升级镜像的类型           | 仅支持docker ，containerd ，或者是 disk，仅在升级场景有效。**注意**：若使用containerd，agent优先使用crictl工具拉取镜像，没有crictl时才会使用ctr命令拉取镜像。使用ctr拉取镜像时，镜像如果在私有仓内，需按照[官方文档](https://github.com/containerd/containerd/blob/main/docs/hosts.md)在/etc/containerd/certs.d目录下配置私有仓主机信息，才能成功拉取镜像。 |是               |
  | opstype        | string | 操作类型：升级,回退或者配置 | 仅支持upgrade ，config 或者 rollback |是               |
  | osversion      | string | 升级/回退的目标版本  | osversion需与节点的目标os版本对应（节点上/etc/os-release中PRETTY_NAME字段或k8s检查到的节点os版本） 例如：KubeOS 1.0.0。 |是               |
  | maxunavailable | int    | 每批同时进行升级/回退/配置的节点数。 | maxunavailable值大于实际节点数时，取实际节点数进行升级/回退/配置。 |是               |
  | containerimage    | string | 用于升级的容器镜像               | 仅在imagetype是容器类型时生效，仅支持以下3种格式的容器镜像地址： repository/name repository/name@sha256:xxxx repository/name:tag |是               |
  | imageurl       | string | 用于升级的磁盘镜像的地址 | imageurl中包含协议，只支持http或https协议，例如：```https://192.168.122.15/update.img``` ，仅在使用磁盘镜像升级场景下有效 |是               |
  | checksum       | string | 用于升级的磁盘镜像校验的checksum(SHA-256)值或者是用于升级的容器镜像的digests值                      | 仅在升级场景下有效 |是               |
  | flagSafe       | bool   | 当imageurl的地址使用http协议表示是否是安全的                 | 需为 true 或者 false ，仅在imageurl使用http协议时有效 |是               |
  | mtls           | bool   | 用于表示与imageurl连接是否采用https双向认证     | 需为 true 或者 false ，仅在imageurl使用https协议时有效|是               |
  | cacert         | string | https或者https双向认证时使用的根证书文件                       | 仅在imageurl使用https协议时有效| imageurl使用https协议时必选 |
  | clientcert     | string | https双向认证时使用的客户端证书文件                          | 仅在使用https双向认证时有效|mtls为true时必选 |
  | clientkey      | string | https双向认证时使用的客户端公钥                              | 仅在使用https双向认证时有效|mtls为true时必选 |
  | evictpodforce      | bool | 升级/回退时是否强制驱逐pod                            | 需为 true 或者 false ，仅在升级或者回退时有效| 必选 |
  | sysconfigs      | / | 配置设置                          | 1. “opstype=config”时只进行配置。<br>  2.“opstype=upgrade/rollback”时，代表升级/回退后配置，即在升级/回退重启后进行配置，详细字段说明请见[配置（Settings）指导](#配置settings指导) | “opstype=config”时必选 |
  | upgradeconfigs | / | 升级前配置设置                       | 在升级或者回退时有效，在升级或者回退操作之前起效，详细字段说明请见[配置（Settings）指导](#配置settings指导)| 可选 |
  | nodeselector      | string | 需要进行升级/配置/回滚操作的节点label                           | 用于只对具有某些特定label的节点而不是集群所有worker节点进行运维的场景，需要进行运维操作的节点需要包含key为upgrade.openeuler.org/node-selector的label，nodeselector为该label的value值。<br>注意事项：<br> 1.此参数不配置时，或者配置为“no-label”时对没有upgrade.openeuler.org/node-selector的节点进行操作<br> 2.此参数为“”时，对具有upgrade.openeuler.org/node-selector=“”的节点进行操作 <br> 3.如需忽略label，对所有节点进行操作，需指定此参数为all-label| 可选 |
  | timewindow      | / | 升级/配置/回滚操作的时间窗口                           |1.指定时间窗口时starttime和endtime都需指定，即二者需要同时为空或者同时不为空<br> 2.starttime和endtime类型为string，需要为YYYY-MM-DD HH:MM:SS格式或者HH:MM:SS格式，且二者格式需一致<br> 3.为HH:MM:SS格式时，starttime \< endtime认为starttime是下一天的该时间<br> 4.timewindow不配置时默认为不存在时间窗限制| 可选 |
  | timeinterval      | int | 升级/配置/回滚操作每批次任务下发的时间间隔                           |参数单位为秒，时间间隔为operator下发任务的时间间隔，如k8s集群繁忙无法立即响应operator请求，实际时间间隔可能会大于指定时间| 可选 |
  | executionmode     | string | 升级/配置/回滚操作执行的方式                           |仅支持serial或者parallel，即串行或者并行，当次参数不设置时，默认采用并行的方式| 可选 |

## 升级指导

1. 编写YAML文件，在集群中部署 OS 的cr实例，用于部署cr实例的YAML示例如下，假定将上面的YAML保存到upgrade_v1alpha1_os.yaml;

    * 使用磁盘镜像进行升级

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

    * 使用容器镜像进行升级
        * 使用容器镜像进行升级前请先制作升级所需的容器镜像，制作方式请见[《容器OS镜像制作指导》](./kubeos_image_creation.md)中 [KubeOS OCI 镜像制作](./kubeos_image_creation.md#kubeos-oci-镜像制作)。

      节点容器引擎为docker

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

      节点容器引擎为containerd

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

    * 升级并且进行配置的示例如下：
        * 以节点容器引擎为containerd为例，升级方式对配置无影响，upgradeconfigs在升级前起效，sysconfigs在升级后起效，配置参数说明请见[配置（Settings）指导](#配置settings指导)。
        * 升级并且配置时opstype字段需为upgrade。
        * upgradeconfig为升级之前执行的配置，sysconfigs为升级机器重启后执行的配置，用户可按需进行配置。

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

        * 设置nodeselector、timewindow、timeinterval、executionmode升级部分节点示例如下：
            * 以节点容器引擎为containerd为例，升级方式对节点筛选无影响。
            * 需要进行升级的节点需包含key为`upgrade.openeuler.org/node-selector`的label，nodeselector的值为该label的value，即假定nodeselector值为kubeos，则只对包含`upgrade.openeuler.org/node-selector=kubeos`的label的worker节点进行升级。
            * nodeselector、timewindow、timeinterval、executionmode对配置和回滚同样有效。
            * 节点添加label、修改label、删除label和查看label命令示例如下：

          ``` bash
          # 为节点kubeos-node1增加label
          kubectl label nodes kubeos-node1 upgrade.openeuler.org/node-selector=kubeos-v1
          # 修改节点kubeos-node1的label
          kubectl label --overwrite nodes kubeos-node1 upgrade.openeuler.org/node-selector=kubeos-v2
          # 删除节点kubeos-node1的label
          kubectl label nodes kubeos-node1 upgrade.openeuler.org/node-selector-
          # 查看节点的label
          kubectl get nodes --show-labels
          ```

            * yaml示例如下：

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

2. 查看未升级的节点的 OS 版本。

    ```shell
    kubectl get nodes -o custom-columns='NAME:.metadata.name,OS:.status.nodeInfo.osImage'
    ```

3. 执行命令，在集群中部署cr实例后，节点会根据配置的参数信息进行升级。

    ```shell
    kubectl apply -f upgrade_v1alpha1_os.yaml
    ```

4. 再次查看节点的 OS 版本来确认节点是否升级完成。

    ```shell
    kubectl get nodes -o custom-columns='NAME:.metadata.name,OS:.status.nodeInfo.osImage'
    ```

> [!NOTE]说明
>
> 如果后续需要再次升级，与上面相同对 upgrade_v1alpha1_os.yaml 的 相应字段进行相应修改。

## 配置（Settings）指导

* Settings参数说明:

  基于示例YAML对配置的参数进行说明，示例YAML如下，配置的格式（缩进）需和示例保持一致：

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

  配置的参数说明如下：

  | 参数       | 参数类型 | 参数说明                    | 使用说明                                                     | 配置中是否必选          |
  | ---------- | -------- | --------------------------- | ------------------------------------------------------------ | ----------------------- |
  | version    | string   | 配置的版本                  | 通过version是否相等来判断配置是否触发，version为空（为""或者没有值）时同样进行判断，所以不配置sysconfigs/upgradeconfigs时，继存的version值会被清空并触发配置。 | 是                      |
  | configs    | /        | 具体配置内容                | 包含具体配置项列表。                                         | 是                      |
  | model      | string   | 配置的类型                  | 支持的配置类型请看附录下的[Settings列表](#setting-列表)                 | 是                      |
  | configpath | string   | 配置文件路径                | 仅在kernel.sysctl.persist配置类型中生效，请看附录下的[Settings列表](#setting-列表)对配置文件路径的说明。 | 否                      |
  | contents   | /        | 具体key/value的值及操作类型 | 包含具体配置参数列表。                                       | 是                      |
  | key        | string   | 参数名称                    | key不能为空，不能包含"="，不建议配置含空格、tab键的字符串，具体请看附录下的[Settings列表](#setting-列表)中每种配置类型对key的说明。 | 是                      |
  | value      | string   | 参数值                      | key=value形式的参数中，value不能为空，不建议配置含空格、tab键的字符串，具体请看附录下的[Settings列表](#setting-列表)中对每种配置类型对value的说明。 | key=value形式的参数必选 |
  | operation  | string   | 对参数进行的操作            | 仅对kernel.sysctl.persist、grub.cmdline.current、grub.cmdline.next类型的参数生效。默认为添加或更新。仅支持配置为delete，代表删除已存在的参数（key=value需完全一致才能删除）。 | 否                      |

    * upgradeconfigs与sysconfigs参数相同，upgradeconfigs为升级/回退前进行的配置，仅在upgrade/rollback场景起效，sysconfigs既支持只进行配置，也支持在升级/回退重启后进行配置。

* 使用说明

    * 编写YAML文件，在集群中部署 OS 的cr实例，用于部署cr实例的YAML示例如上，假定将上面的YAML保存到upgrade_v1alpha1_os.yaml。

    * 查看配置之前的节点的配置的版本和节点状态（NODESTATUS状态为idle）。

      ```shell
      kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
      ```

    * 执行命令，在集群中部署cr实例后，节点会根据配置的参数信息进行配置，再次查看节点状态(NODESTATUS变成config)。

      ```shell
      kubectl apply -f upgrade_v1alpha1_os.yaml
      kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
      ```

    * 再次查看节点的配置的版本确认节点是否配置完成(NODESTATUS恢复为idle)。

      ```shell
      kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
      ```

* 如果后续需要再次配置，与上面相同对 upgrade_v1alpha1_os.yaml 的相应字段进行相应修改。

## 回退指导

### 使用场景

* 虚拟机无法正常启动时，可在grub启动项页面手动切换启动项，使系统回退至上一版本（即手动回退）。
* 虚拟机能够正常启动并且进入系统时，支持工具回退和手动回退，建议使用工具回退。
* 工具回退有两种方式：
    1. rollback模式直接回退至上一版本。
    2. upgrade模式重新升级至上一版本。

### 手动回退指导

* 手动重启虚拟机，进入启动项页面后，选择第二启动项进行回退，手动回退仅支持回退到上一个版本。

### 工具回退指导

* 回退至任意版本
    1. 修改 OS 的cr实例的YAML 配置文件（例如 upgrade_v1alpha1_os.yaml），设置相应字段为期望回退的老版本镜像信息。类别OS来自于安装和部署章节创建的CRD对象，字段说明及示例请见上一节升级指导。

    2. YAML修改完成后执行更新命令，在集群中更新定制对象后，节点会根据配置的字段信息进行回退

        ```shell
        kubectl apply -f upgrade_v1alpha1_os.yaml
        ```

* 回退至上一版本
    * OS回退至上一版本：修改upgrade_v1alpha1_os.yaml，设置osversion为上一版本，opstype为rollback，回退至上一版本（即切换至上一分区）。YAML示例如下：

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

    * 配置回退至上一版本：修改upgrade_v1alpha1_os.yaml，设置sysconfigs/upgradeconfigs的version为上一版本，回退至上一版本（已配置的参数无法回退）。YAML示例如下：

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

* YAML修改完成后执行更新命令，在集群中更新定制对象后，节点会根据配置的字段信息进行回退。

  ```shell
  kubectl apply -f upgrade_v1alpha1_os.yaml
  ```

  更新完成后，节点会根据配置信息回退容器 OS。
* 查看节点容器 OS 版本(回退OS版本)或节点config版本&节点状态为idle(回退config版本)，确认回退是否成功。

  ```shell
  kubectl get osinstances -o custom-columns='NAME:.metadata.name,NODESTATUS:.spec.nodestatus,SYSCONFIG:status.sysconfigs.version,UPGRADECONFIG:status.upgradeconfigs.version'
  ```

## 附录

### Setting 列表

#### kernel Settings

* kernel.sysctl：临时设置内核参数，重启后无效，key/value 表示内核参数的 key/value， key与value均不能为空且key不能包含“=”，该参数不支持删除操作（operation=delete）示例如下:

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

* kernel.sysctl.persist: 设置持久化内核参数，key/value表示内核参数的key/value，key与value均不能为空且key不能包含“=”， configpath为配置文件路径，支持新建（需保证父目录存在），如不指定configpath默认修改/etc/sysctl.conf，示例如下：

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

#### Grub Settings

* grub.cmdline.current/next: 设置grub.cfg文件中的内核引导参数，该行参数在grub.cfg文件中类似如下示例：

    ```shell
    linux   /boot/vmlinuz root=/dev/sda2 ro rootfstype=ext4 nomodeset quiet oops=panic softlockup_panic=1 nmi_watchdog=1 rd.shell=0 selinux=0 crashkernel=256M panic=3
    ```

    * 在dm-verity模式下，grub.cmdline配置下发无效。

    * KubeOS使用双分区，grub.cmdline.current/next支持对当前分区或下一分区进行配置：

    * grub.cmdline.current：对当前分区的启动项参数进行配置。
    * grub.cmdline.next：对下一分区的启动项参数进行配置。

    * 注意：升级/回退前后的配置，始终基于升级/回退操作下发时的分区位置进行current/next的区分。假设当前分区为A分区，下发升级操作并在sysconfigs（升级重启后配置）中配置grub.cmdline.current，重启后进行配置时仍修改A分区对应的grub cmdline。

    * grub.cmdline.current/next支持“key=value”（value不能为空），也支持单key。若value中有“=”，例如“root=UUID=some-uuid”，key应设置为第一个“=”前的所有字符，value为第一个“=”后的所有字符。 配置方法示例如下：

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

#### kubelet配置

* kubernetes.kubelet: 配置节点kubelet的配置文件中的参数，参数说明和约束如下：
    * 仅支持```KubeletConfiguration```中的配置参数。
    * 节点kubelet配置文件需要为yaml格式的文件。
    * 如不指定configpath，默认配置文件路径为```/var/lib/kubelet/config.yaml```，并且需要注意的是配置文件的路径需要与kubelet启动时的```-- config```参数指定的路径一致才能生效，用户需保证配置文件路径有效。
    * kubelet配置的value参数类型支持为空/null、int、float、string、boolean和数组。当为数组时，数组元素允许重复，数组参数进行更新时会追加到已有数组中。如需修改数组中的元素，需要先删除数组，再新增数组来完成修改。
    * 如配置存在嵌套，则通过```'.'```连接嵌套的key值，例如如果修改如下yaml示例中```cacheAuthorizedTTL```参数为1s。

      ```yaml
      authorization:
        mode: Webhook
        webhook:
          cacheAuthorizedTTL: 0s
      ```

  参数配置示例如下：

  ```yaml
  configs:
  - model: kubernetes.kubelet
    configpath: /etc/test.yaml
    contents:
      - key: authorization.webhook.cacheAuthorizedTTL
        value: 1s
  ```

kubernetes.kubelet进行删除时，不对value与配置文件中的值进行比较。

#### containerd配置

* container.containerd: 配置节点上containerd的配置文件中的参数，参数说明和约束如下：
    * containerd需要配置文件为toml格式，所以key为toml中该参数的表头.键名，例如希望修改如下toml示例中```no_shim```为true。

    ```toml
    [plugins."io.containerd.runtime.v1.linux"]
    no_shim=false
    runtime="runc"
    runtime_root="
    ```

  参数配置示例如下：

  ```yaml
  configs:
  - model: container.containerd
    configpath: /etc/test.toml
    contents:
      - key: plugins."io.containerd.runtime.v1.linux".no_shim
        value: true
  ```

    * toml使用```.```分割键，os-agent识别时与toml保持一致，所以当键名中包含```.```时，该键名需要使用```""```，例如上例中的```"io.containerd.runtime.v1.linux"```为一个键
    * 如不指定configpath，默认配置文件路径为```/etc/containerd/config.toml```，用户需要保证配置文件路径有效。
    * container.conatainerd配置的key和value均不能为空，value参数类型支持int、float、string、boolean和数组。当为数组时，数组元素允许重复，数组参数进行更新时会追加到已有数组中。如需修改数组中的元素，需要先删除数组，再新增数组来完成修改。
    * container.containerd进行删除时，不对value与配置文件中的值进行比较。

#### Pam Limits配置

* pam.limits：配置节点上/etc/security/limits.conf文件
    * key为domain值，value的格式需要为type.item.value（limits.conf文件要求每行格式为：\<domain\> \<type\> \<item\> \<value\>），例如：

      ```yaml
      configs:
      - model: pam.limits
        contents:
          - key: ftp
            value: soft.core.0  
      ```

    * 更新时，如不需要对type/item/value更新时，可以使用```_```，忽略对此参数的更新，但value必须为点隔的三段式，例如：

      ```yaml
      configs:
      - model: pam.limits
        contents:
          - key: ftp
            value: hard._.1  
      ```

    * pam.limits新增时，value中不允许包含```_```
    * pam.limits删除时，会对value进行校验，当value与配置文件中的值不同时，删除失败
    * pam.limits配置的key和value均不能为空
