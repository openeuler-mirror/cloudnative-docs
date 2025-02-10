# iSulad支持NRI

## 概述

NRI(Node Resource Interface), 是用于控制节点资源的公共接口, 是CRI兼容的容器运行时插件扩展的通用框架。

它为扩展插件提供了跟踪容器状态，并对其配置进行有限修改的基本机制。允许将用户某些自定的逻辑插入到OCI兼容的运行时中，此逻辑可以对容器进行受控更改，或在容器生命周期的某些时间点执行 OCI 范围之外的额外操作。例如，用于改进设备和其他容器资源的分配和管理。

iSulad目前支持的NRI api 版本为[0.6.1](https://github.com/containerd/nri/blob/v0.6.1/pkg/api/api.proto)。

## 配置iSulad支持NRI

tips: 该功能仅在openeuler 24.09版本中默认可用

### 依赖软件包

需安装[isula-rust-extensions](https://gitee.com/src-openeuler/isula-rust-extensions)软件包

### 相关配置

首先打开CRI v1支持，NRI功能仅在V1中生效

```conf
"enable-cri-v1": true,
```

若使用默认的配置，仅需将以下选项打开：

```conf
"nri-support": true,
```

其他均有默认值。

若需要配置其他项，参照：

```sh
# add support for NRI plugin.
"nri-support": true,
# Allow connections from externally launched NRI plugins.
"disable-connections": true,
# plugin-config-path is the directory to search for plugin-specific configuration.
"plugin-config-path": "/etc/nri/conf.d"
# plugin-path is the directory to search for plugins to launch on startup.
"plugin-path": "/opt/nri/plugins"
# plugin-registration-timeout is the timeout for a plugin to register after connection.
"plugin-registration-timeout": 5
# plugin-request-timeout is the timeout for a plugin to handle an event/request.
"plugin-request-timeout": 2
```

## 使用示例

NRI 简单插件实例可参照[NRI 仓库](https://github.com/containerd/nri/tree/main/plugins),以下使用`Logger`为示例：

拉取nri代码库，编译plugin二进制：

```sh
git clone https://github.com/containerd/nri.git
cd plugins/logger
go build .
```

### pre-started NRI 插件使用示例

1. 若需要在iSulad启动时自动拉取`logger`插件，则将其二进制置于iSulad配置中设置的`plugin_path`路径下，并将`logger`插件的配置置于`plugin_config_path`路径下

    ```sh
    [root@openEuler logger]# mkdir -p /opt/nri/plugins
    [root@openEuler logger]# cp 01-logger /opt/nri/plugins
    [root@openEuler logger]# ls -l /opt/nri/plugins
    total 16896
    -rwxr-xr-x. 1 root root 17300525 Aug 19 15:26 01-logger
    [root@openEuler logger]# mkdir -p /etc/nri/conf.d/
    [root@openEuler logger]# vim /etc/nri/conf.d/01-logger.conf
    [root@openEuler logger]# cat /etc/nri/conf.d/01-logger.conf
    AddAnnotation: test_nri_isula
    [root@openEuler logger]#
    ```

2. 重启isuald后，由于未配置log日志存储位置，默认打印与isulad日志中，若在`01-logger.conf`中配置了日志存储位置则日志存储于配置路径中，产生的日志如下：

  ```conf
  INFO   [0026] RemovePodSandbox: pod:                       
  INFO   [0026] RemovePodSandbox:    annotations:            
  INFO   [0026] RemovePodSandbox:      cri.sandbox.isulad.checkpoint: '{"version":"v1","name":"test-nri-sandbox2","ns":"testns","data":{"host_network":true},"checksum":"c86a8542e7380049831cca636355345cc5921beebc41cd93e80467491c27a8d9"}' 
  INFO   [0026] RemovePodSandbox:      cri.sandbox.network.setup.v2: "true" 
  INFO   [0026] RemovePodSandbox:      devices.nri.io/container.c0: | 
  INFO   [0026] RemovePodSandbox:        - path: /dev/nri-null 
  INFO   [0026] RemovePodSandbox:          type: c           
  INFO   [0026] RemovePodSandbox:          major: 1          
  INFO   [0026] RemovePodSandbox:          minor: 3          
  INFO   [0026] RemovePodSandbox:      io.kubernetes.cri.container-type: sandbox 
  INFO   [0026] RemovePodSandbox:      io.kubernetes.cri.sandbox-attempt: "1" 
  INFO   [0026] RemovePodSandbox:      io.kubernetes.cri.sandbox-name: test-nri-sandbox2 
  INFO   [0026] RemovePodSandbox:      io.kubernetes.cri.sandbox-namespace: testns 
  INFO   [0026] RemovePodSandbox:      io.kubernetes.cri.sandbox-uid: b49ef5ee-ee30-11ed-a05b-0242ac120003 
  INFO   [0026] RemovePodSandbox:      ulimits.nri.containerd.io/container.c0: | 
  INFO   [0026] RemovePodSandbox:        - type: RLIMIT_NOFILE 
  INFO   [0026] RemovePodSandbox:          hard: 1048576     
  INFO   [0026] RemovePodSandbox:          soft: 1048576     
  INFO   [0026] RemovePodSandbox:    id: 475daee4ca64e1d35894a5c27771bee32e55b22753f3ba80f57869e9b294a62b 
  INFO   [0026] RemovePodSandbox:    labels:                 
  INFO   [0026] RemovePodSandbox:      cri.isulad.type: podsandbox 
  INFO   [0026] RemovePodSandbox:      io.kubernetes.container.name: POD 
  INFO   [0026] RemovePodSandbox:    linux:                  
  INFO   [0026] RemovePodSandbox:      pod_resources:        
  INFO   [0026] RemovePodSandbox:        cpu:                
  INFO   [0026] RemovePodSandbox:          period: {}        
  INFO   [0026] RemovePodSandbox:          quota: {}         
  INFO   [0026] RemovePodSandbox:          shares:           
  INFO   [0026] RemovePodSandbox:            value: 2        
  INFO   [0026] RemovePodSandbox:        memory:             
  INFO   [0026] RemovePodSandbox:          limit: {}         
  INFO   [0026] RemovePodSandbox:    name: k8s_POD_test-nri-sandbox2_testns_b49ef5ee-ee30-11ed-a05b-0242ac120003_1 
  INFO   [0026] RemovePodSandbox:    namespace: testns       
  INFO   [0026] RemovePodSandbox:    uid: b49ef5ee-ee30-11ed-a05b-0242ac120003 
            iSula 20240829135021.168 - Event: {Object: CRI, Type: Removed Pod: 47}
  ```

### 外部注册NRI插件使用

若需要在iSulad启动后注册`logger`插件，则直接运行此插件二进制

```conf
➜  logger git:(v0.6.1) ✗ sudo ./02-logger
INFO   [0000] Created plugin 02-logger (02-logger, handles RunPodSandbox,StopPodSandbox,RemovePodSandbox,CreateContainer,PostCreateContainer,StartContainer,PostStartContainer,UpdateContainer,PostUpdateContainer,StopContainer,RemoveContainer) 
INFO   [0000] Registering plugin 02-logger...              
INFO   [0000] Configuring plugin 02-logger for runtime v2/2.0.0-beta.2+unknown... 
INFO   [0000] got configuration data: "" from runtime v2 2.0.0-beta.2+unknown 
INFO   [0000] Subscribing plugin 02-logger (02-logger) for events RunPodSandbox,StopPodSandbox,RemovePodSandbox,CreateContainer,PostCreateContainer,StartContainer,PostStartContainer,UpdateContainer,PostUpdateContainer,StopContainer,RemoveContainer 
INFO   [0000] Started plugin 02-logger...                  
INFO   [0000] Synchronize: pods:                           
INFO   [0000] Synchronize:    null                         
INFO   [0000] Synchronize: containers:                     
INFO   [0000] Synchronize:    null 
```

## 限制说明

### 接口参数限制

暂不支持修改某些参数：

```proto
// Container to evict(IOW unsolicitedly stop).
ContainerEviction evict;

// ref:https://github.com/containerd/containerd/pull/5490
// - User defines blockio classes, for example: ThrottledIO and LowLatency. Class names are not restricted, and the number of classes is not limited.
// iSulad not support
OptionalString blockio_class;

// iSulad now not support the following hook types
message Hooks {
  repeated Hook create_runtime = 2;
  repeated Hook create_container = 3;
  repeated Hook start_container = 4;
}
```

### 使用限制

1. iSulad目前仅支持CRI V1方式使用NRI特性
2. 目前支持的NRI api 版本为0.6.1
3. 对于插件异常退出场景，iSulad目前仅在下次调用出错时打印日志
4. 对于external 注册的plugin，若iSulad退出，iSulad不对其进行强制kill，生命周期与iSulad无关。
