# http接口

## 概述

rubik对外开放接口均为http接口，当前包括pod优先级设置/更新接口、rubik探活接口和rubik版本号查询接口。

## 接口介绍

### 设置、更新Pod优先级接口

rubik提供了设置或更新pod优先级的功能，外部可通过调用该接口发送pod相关信息，rubik根据接收到的pod信息对其设置优先级从而达到资源隔离的目的。接口调用格式为：

```bash
HTTP POST /run/rubik/rubik.sock
{
    "Pods": {
        "podaaa": {
            "CgroupPath": "kubepods/burstable/podaaa",
            "QosLevel": 0
        },
        "podbbb": {
            "CgroupPath": "kubepods/burstable/podbbb",
            "QosLevel": -1
        }
    }
}
```

Pods 配置中为需要设置或更新优先级的 Pod 信息，每一个http请求至少需要指定配置1个 pod，每个 pod 必须指定CgroupPath 和 QosLevel，其含义如下：

| 配置项     | 配置值类型 | 配置取值范围 | 配置含义                                                |
| ---------- | ---------- | ------------ | ------------------------------------------------------- |
| QosLevel   | int        | 0、-1        | pod优先级，0表示其为在线业务，-1表示其为离线业务        |
| CgroupPath | string     | 相对路径     | 对应Pod的cgroup子路径（即其在cgroup子系统下的相对路径） |

接口调用示例如下：

```sh
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST --data '{"Pods": {"podaaa": {"CgroupPath": "kubepods/burstable/podaaa","QosLevel": 0},"podbbb": {"CgroupPath": "kubepods/burstable/podbbb","QosLevel": -1}}}' --unix-socket /run/rubik/rubik.sock http://localhost/
```

### 探活接口

rubik作为HTTP服务，提供探活接口用于帮助判断rubik是否处于运行状态。

接口形式：HTTP/GET /ping

接口调用示例如下：

```sh
curl -XGET --unix-socket /run/rubik/rubik.sock http://localhost/ping
```

若返回ok则代表rubik服务处于运行状态。

### 版本信息查询接口

rubik支持通过HTTP请求查询当前rubik的版本号。

接口形式：HTTP/GET /version

接口调用示例如下：

```sh
curl -XGET --unix-socket /run/rubik/rubik.sock http://localhost/version
{"Version":"0.0.1","Release":"1","Commit":"29910e6","BuildTime":"2021-05-12"}
```
