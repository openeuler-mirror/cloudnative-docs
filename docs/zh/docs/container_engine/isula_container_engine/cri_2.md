# CRI V1接口支持

## 概述

CRI（Container Runtime Interface, 容器运行时接口）是kublet与容器引擎通信使用的主要协议。
在K8S 1.25及之前，K8S存在CRI v1alpha2 和 CRI V1两种版本的CRI接口，但从1.26开始，K8S仅提供对于CRI V1的支持。

iSulad同时提供对[CRI v1alpha2](./cri.md)和CRI v1的支持，
对于CRI v1，iSulad支持[CRI v1alpha2](./cri.md)所述功能，
并提供对CRI V1中所定义新接口和字段的支持。

目前iSulad支持的CRI V1版本为1.29，对应官网描述API如下：

[https://github.com/kubernetes/cri-api/blob/kubernetes-1.29.0/pkg/apis/runtime/v1/api.proto](https://github.com/kubernetes/cri-api/blob/kubernetes-1.29.0/pkg/apis/runtime/v1/api.proto)

iSulad使用的API描述文件，与官方API略有出入，以本文档描述的接口为准。

## 新增字段描述

- <a name="zh-cn_topic_0182207110_li191811740184215"></a>**CgroupDriver**

    cgroup驱动的enum值列表

    <a name="zh-cn_topic_0182207110_table3751330407"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1775211308012"><th class="cellrowborder" id="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p18470133608"><a name="zh-cn_topic_0182207110_p18470133608"></a><a name="zh-cn_topic_0182207110_p18470133608"></a><strong id="zh-cn_topic_0182207110_b1947019331101"><a name="zh-cn_topic_0182207110_b1947019331101"></a><a name="zh-cn_topic_0182207110_b1947019331101"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" id="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p147011336020"><a name="zh-cn_topic_0182207110_p147011336020"></a><a name="zh-cn_topic_0182207110_p147011336020"></a><strong id="zh-cn_topic_0182207110_b94707338010"><a name="zh-cn_topic_0182207110_b94707338010"></a><a name="zh-cn_topic_0182207110_b94707338010"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row127528301605"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p14707331901"><a name="zh-cn_topic_0182207110_p14707331901"></a><a name="zh-cn_topic_0182207110_p14707331901"></a>SYSTEMD = 0</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p3470833904"><a name="zh-cn_topic_0182207110_p3470833904"></a><a name="zh-cn_topic_0182207110_p3470833904"></a>systemd cgroup驱动</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>CGROUPFS = 1</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>cgroupfs驱动</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li201899371871"></a>**LinuxRuntimeConfiguration**

    容器引擎所使用的cgroup驱动

    <a name="zh-cn_topic_0182207110_table227603213110"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row19276183217111"><th class="cellrowborder" id="mcps1.1.3.1.1" valign="top" width="39.53%"><p id="zh-cn_topic_0182207110_p1438363819110"><a name="zh-cn_topic_0182207110_p1438363819110"></a><a name="zh-cn_topic_0182207110_p1438363819110"></a><strong id="zh-cn_topic_0182207110_b18383238119"><a name="zh-cn_topic_0182207110_b18383238119"></a><a name="zh-cn_topic_0182207110_b18383238119"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" id="mcps1.1.3.1.2" valign="top" width="60.47%"><p id="zh-cn_topic_0182207110_p538314381119"><a name="zh-cn_topic_0182207110_p538314381119"></a><a name="zh-cn_topic_0182207110_p538314381119"></a><strong id="zh-cn_topic_0182207110_b3383338211"><a name="zh-cn_topic_0182207110_b3383338211"></a><a name="zh-cn_topic_0182207110_b3383338211"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row92761932719"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.53%"><p id="zh-cn_topic_0182207110_p73843384118"><a name="zh-cn_topic_0182207110_p73843384118"></a><a name="zh-cn_topic_0182207110_p73843384118"></a>CgroupDriver cgroup_driver</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.47%"><p id="zh-cn_topic_0182207110_p438419385115"><a name="zh-cn_topic_0182207110_p438419385115"></a><a name="zh-cn_topic_0182207110_p438419385115"></a>容器引擎所使用的cgroup驱动枚举值</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li191811740184215"></a>**ContainerEventType**

    容器事件类型枚举值

    <a name="zh-cn_topic_0182207110_table3751330407"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1775211308012"><th class="cellrowborder" id="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p18470133608"><a name="zh-cn_topic_0182207110_p18470133608"></a><a name="zh-cn_topic_0182207110_p18470133608"></a><strong id="zh-cn_topic_0182207110_b1947019331101"><a name="zh-cn_topic_0182207110_b1947019331101"></a><a name="zh-cn_topic_0182207110_b1947019331101"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" id="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p147011336020"><a name="zh-cn_topic_0182207110_p147011336020"></a><a name="zh-cn_topic_0182207110_p147011336020"></a><strong id="zh-cn_topic_0182207110_b94707338010"><a name="zh-cn_topic_0182207110_b94707338010"></a><a name="zh-cn_topic_0182207110_b94707338010"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row127528301605"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p14707331901"><a name="zh-cn_topic_0182207110_p14707331901"></a><a name="zh-cn_topic_0182207110_p14707331901"></a>CONTAINER_CREATED_EVENT = 0</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p3470833904"><a name="zh-cn_topic_0182207110_p3470833904"></a><a name="zh-cn_topic_0182207110_p3470833904"></a>容器创建类型</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>CONTAINER_STARTED_EVENT = 1</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>容器启动类型</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>CONTAINER_STOPPED_EVENT = 1</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>容器停止类型</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>CONTAINER_DELETED_EVENT = 1</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>容器删除类型</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li191811740184215"></a>**SwapUsage**

    虚拟内存使用情况

    <a name="zh-cn_topic_0182207110_table3751330407"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1775211308012"><th class="cellrowborder" id="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p18470133608"><a name="zh-cn_topic_0182207110_p18470133608"></a><a name="zh-cn_topic_0182207110_p18470133608"></a><strong id="zh-cn_topic_0182207110_b1947019331101"><a name="zh-cn_topic_0182207110_b1947019331101"></a><a name="zh-cn_topic_0182207110_b1947019331101"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" id="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p147011336020"><a name="zh-cn_topic_0182207110_p147011336020"></a><a name="zh-cn_topic_0182207110_p147011336020"></a><strong id="zh-cn_topic_0182207110_b94707338010"><a name="zh-cn_topic_0182207110_b94707338010"></a><a name="zh-cn_topic_0182207110_b94707338010"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row127528301605"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p14707331901"><a name="zh-cn_topic_0182207110_p14707331901"></a><a name="zh-cn_topic_0182207110_p14707331901"></a>int64 timestamp</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p3470833904"><a name="zh-cn_topic_0182207110_p3470833904"></a><a name="zh-cn_topic_0182207110_p3470833904"></a>时间戳信息</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>UInt64Value swap_available_bytes</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>可使用虚拟内存字节数</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" headers="mcps1.1.3.1.1" valign="top" width="39.35%"><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>UInt64Value swap_usage_bytes</p>
    </td>
    <td class="cellrowborder" headers="mcps1.1.3.1.2" valign="top" width="60.650000000000006%"><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>已使用虚拟内存字节数</p>
    </td>
    </tr>
    </tbody>
    </table>

## 新增接口描述

### RuntimeConfig

#### 接口原型

```text
rpc RuntimeConfig(RuntimeConfigRequest) returns (RuntimeConfigResponse) {}
```

#### 接口描述

获取cgroup驱动配置 cgroupfs 或 systemd-cgroup

#### 参数 RuntimeConfigRequest

无字段

#### 返回值 RuntimeConfigResponse

<a name="zh-cn_topic_0183088042_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088042_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p197485518319"><a name="zh-cn_topic_0183088042_p197485518319"></a><a name="zh-cn_topic_0183088042_p197485518319"></a><strong id="zh-cn_topic_0183088042_b77413551933"><a name="zh-cn_topic_0183088042_b77413551933"></a><a name="zh-cn_topic_0183088042_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p374185520310"><a name="zh-cn_topic_0183088042_p374185520310"></a><a name="zh-cn_topic_0183088042_p374185520310"></a><strong id="zh-cn_topic_0183088042_b174125511315"><a name="zh-cn_topic_0183088042_b174125511315"></a><a name="zh-cn_topic_0183088042_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>LinuxRuntimeConfiguration linux</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>描述cgroupfs或者systemd-cgroup的CgroupDriver枚举值</p>
</td>
</tr>
</tbody>
</table>

### GetContainerEvents

#### 接口原型

```text
rpc GetContainerEvents(GetEventsRequest) returns (stream ContainerEventResponse) {}
```

#### 接口描述

获取Pod生命周期事件流

#### 参数 GetEventsRequest

无字段

#### 返回值 ContainerEventResponse

<a name="zh-cn_topic_0183088042_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088042_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p197485518319"><a name="zh-cn_topic_0183088042_p197485518319"></a><a name="zh-cn_topic_0183088042_p197485518319"></a><strong id="zh-cn_topic_0183088042_b77413551933"><a name="zh-cn_topic_0183088042_b77413551933"></a><a name="zh-cn_topic_0183088042_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p374185520310"><a name="zh-cn_topic_0183088042_p374185520310"></a><a name="zh-cn_topic_0183088042_p374185520310"></a><strong id="zh-cn_topic_0183088042_b174125511315"><a name="zh-cn_topic_0183088042_b174125511315"></a><a name="zh-cn_topic_0183088042_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>容器id</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>ContainerEventType container_event_type</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>容器事件类型</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>int64 created_at</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>容器事件产生时间</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>PodSandboxStatus pod_sandbox_status</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>容器所属Pod的status信息</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>repeated ContainerStatus containers_statuses</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>容器所属Pod内所有容器的status信息</p>
</td>
</tr>
</tbody>
</table>

## 变更描述

### CRI V1.29更新变更描述

#### [获取cgroup驱动配置](https://github.com/kubernetes/kubernetes/pull/118770)

`RuntimeConfig` 获取cgroup驱动配置 cgroupfs 或 systemd-cgroup

#### [GetContainerEvents支持pod生命周期事件](https://github.com/kubernetes/kubernetes/pull/111384)

`GetContainerEents`，提供对pod生命周期相关事件流

`PodSandboxStatus`有相应调整，增加ContainerStatuses提供沙箱内容器status信息

#### [ContainerStats虚拟内存信息](https://github.com/kubernetes/kubernetes/pull/118865)

`ContainerStats`新增虚拟内存使用情况信息： `SwapUsage`

#### [ContainerStatus reason字段OOMKilled设置](https://github.com/kubernetes/kubernetes/pull/112977)

ContainerStatus中reason字段在cgroup out-of-memory时应该设置为OOMKilled

#### [PodSecurityContext.SupplementalGroups描述修改](https://github.com/kubernetes/kubernetes/pull/113047)

描述修改，优化`PodSecurityContext.SupplementalGroups`的注释，明确容器镜像定义的主UID不在该列表下的行为

#### [ExecSync输出限制](https://github.com/kubernetes/kubernetes/pull/110435)

ExecSync返回值输出小于16MB

## 使用手册

### 配置iSulad支持CRI V1

该需求需要iSulad对K8S新版本CRI接口1.29提供支持，

对于1.25及之前的CRI接口，V1alpha2和V1功能保持一致，1.26及之后新增的特性仅在CRI V1中提供支持。
此次升级的功能和特性仅在CRI V1中提供支持，因此新增特性均需要按照以下配置使能CRI V1。

CRI V1使能：

iSulad daemon.json中enable-cri-v1设置为true，重启iSulad

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true
}
```

若通过源码进行编译安装iSulad需开启ENABLE_CRI_API_V1编译选项

```bash
cmake ../ -D ENABLE_CRI_API_V1=ON
```

### RuntimeConfig获取cgroup驱动配置

#### systemd-cgroup配置

iSulad同时提供对systemd和cgroupfs两种cgroup驱动支持，
默认使用cgroupfs作为cgroup驱动，可以通过配置iSulad容器引擎提供对systemd cgroup驱动支持。
iSulad仅提供底层运行时为runc时systemd-cgroup的支持。通过修改iSulad配置文件daemon.json，
设置systemd-cgroup为true，重启iSulad，则使用systemd cgroup驱动。

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true,
    "systemd-cgroup": true
}
```

### GetContainerEvents Pod 生命周期事件生成

#### Pod Events配置

修改iSulad配置文件daemon.json，
设置enable-pod-events为true，重启iSulad。

```json
{
    "group": "isula",
    "default-runtime": "runc",
    ...
    "enable-cri-v1": true,
    "enable-pod-events": true
}
```

## 使用限制

1. 以上新增特性，iSulad仅提供容器运行时设置为runc时的支持。
2. 由于cgroup oom会同时触发容器cgroup路径删除，若iSulad对oom事件处理发生在cgroup路径删除之后，iSulad则无法成功捕捉容器oom事件，可能导致ContainerStatus中reason字段设置不正确。
3. iSulad不支持交叉使用不同的cgroup驱动管理容器，启动容器后iSulad的cgroup驱动配置不应该发生变化。
