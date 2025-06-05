# iSulad支持CDI

## 概述

CDI（Container Device Interface，容器设备接口）是容器运行时的一种规范，用于支持第三方设备。

CDI解决了如下问题：  
在Linux上，为了使容器具有设备感知能力，过去只需在该容器中暴露一个设备节点。但是，随着设备和软件变得越来越复杂，供应商希望执行更多的操作，例如：

- 向容器公开设备可能需要公开多个设备节点、从运行时命名空间挂载文件或隐藏procfs条目。
- 执行容器和设备之间的兼容性检查（例如：检查容器是否可以在指定设备上运行）。
- 执行特定于运行时的操作（例如：虚拟机与基于Linux容器的运行时）。
- 执行特定于设备的操作（例如：清理GPU的内存或重新配置FPGA）。

在缺乏第三方设备标准的情况下，供应商通常不得不为不同的运行时编写和维护多个插件，甚至直接在运行时中贡献特定于供应商的代码。此外，运行时不统一地暴露插件系统（甚至根本不暴露插件系统），导致在更高级别的抽象（例如Kubernetes设备插件）中重复功能。

CDI解决上述问题的方法：  
CDI描述了一种允许第三方供应商与设备交互的机制，从而不需要更改容器运行时。

使用的机制是一个JSON文件（类似于容器网络接口(CNI）)，它允许供应商描述容器运行时应该对容器的OCI规范执行的操作。

iSulad目前已支持[CDI v0.6.0](https://github.com/cncf-tags/container-device-interface/blob/v0.6.0/SPEC.md)规范。

## 配置iSulad支持CDI

需要对daemon.json做如下配置，然后重启iSulad：

```json
{
    ...
    "enable-cri-v1": true,
    "cdi-spec-dirs": ["/etc/cdi", "/var/run/cdi"],
    "enable-cdi": true
}
```

其中"cdi-spec-dirs"用于指定CDI specs所在目录，如果不指定则默认为"/etc/cdi", "/var/run/cdi"。

## 使用示例

### CDI specification实例

具体每个字段含义详见[CDI v0.6.0](https://github.com/cncf-tags/container-device-interface/blob/v0.6.0/SPEC.md)

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

### 在CRI创建容器的参数中使用CDI

假设已经生成了vendor.json规范，并且该规范在"/etc/cdi"或"/var/run/cdi"中可用（或者当iSulad的配置文件"cdi-spec-dirs"有指定目录时，在"cdi-spec-dirs"指定目录中可用），则可以通过其完全限定的设备名称来访问设备，例子中为"vendor.com/device=myDevice"。

在容器json文件中，使用以下两种方式指定设备均可:

方式1:annotations中指定设备

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

方式2:CDI_Devices中指定设备

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

## 使用限制

iSulad目前仅支持CRI方式使用CDI特性。
