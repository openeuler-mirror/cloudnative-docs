# CRI V1alpha2 接口

## 描述

CRI API 接口是由kubernetes 推出的容器运行时接口，CRI定义了容器和镜像的服务接口。ISulad使用CRI接口，实现和kubernetes 的对接。

因为容器运行时与镜像的生命周期是彼此隔离的，因此需要定义两个服务。该接口使用[Protocol Buffer](https://developers.google.com/protocol-buffers/)定义，基于[gRPC](https://grpc.io/)。

当前iSulad使用默认CRI版本为v1alpha2版本，官方API描述文件如下：

[https://github.com/kubernetes/kubernetes/blob/release-1.14/pkg/kubelet/apis/cri/runtime/v1alpha2/api.proto](https://github.com/kubernetes/kubernetes/blob/release-1.14/pkg/kubelet/apis/cri/runtime/v1alpha2/api.proto)，

ISulad使用的为pass使用的1.14版本API描述文件，与官方API略有出入，以本文档描述的接口为准。

> [!NOTE]说明
>
> CRI接口websocket流式服务，服务端侦听地址为127.0.0.1，端口为10350，端口可通过命令行--websocket-server-listening-port参数接口或者daemon.json配置文件进行配置。  

## 接口

各接口中可能用到的参数清单如下，部分参数暂不支持配置，已在配置中标出。

### 接口参数列表

- <a name="zh-cn_topic_0182207110_li1197211439388"></a>**DNSConfig**

    配置sandbox的DNS服务器和搜索域

    | 参数成员                 | 描述                                                       |
    |--------------------------|------------------------------------------------------------|
    | repeated string servers  | 集群的DNS服务器列表                                        |
    | repeated string searches | 集群的DNS搜索域列表                                        |
    | repeated string options  | DNS可选项列表，参考<https://linux.die.net/man/5/resolv.conf> |

- <a name="zh-cn_topic_0182207110_li191811740184215"></a>**Protocol**

    协议的enum值列表

    <a name="zh-cn_topic_0182207110_table3751330407"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1775211308012"><th class="cellrowborder" valign="top" width="39.35%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p18470133608"><a name="zh-cn_topic_0182207110_p18470133608"></a><a name="zh-cn_topic_0182207110_p18470133608"></a><strong id="zh-cn_topic_0182207110_b1947019331101"><a name="zh-cn_topic_0182207110_b1947019331101"></a><a name="zh-cn_topic_0182207110_b1947019331101"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="60.650000000000006%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p147011336020"><a name="zh-cn_topic_0182207110_p147011336020"></a><a name="zh-cn_topic_0182207110_p147011336020"></a><strong id="zh-cn_topic_0182207110_b94707338010"><a name="zh-cn_topic_0182207110_b94707338010"></a><a name="zh-cn_topic_0182207110_b94707338010"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row127528301605"><td class="cellrowborder" valign="top" width="39.35%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p14707331901"><a name="zh-cn_topic_0182207110_p14707331901"></a><a name="zh-cn_topic_0182207110_p14707331901"></a>TCP = 0</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.650000000000006%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p3470833904"><a name="zh-cn_topic_0182207110_p3470833904"></a><a name="zh-cn_topic_0182207110_p3470833904"></a>TCP协议</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6752193015019"><td class="cellrowborder" valign="top" width="39.35%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p24701933605"><a name="zh-cn_topic_0182207110_p24701933605"></a><a name="zh-cn_topic_0182207110_p24701933605"></a>UDP = 1</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.650000000000006%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p04701338015"><a name="zh-cn_topic_0182207110_p04701338015"></a><a name="zh-cn_topic_0182207110_p04701338015"></a>UDP协议</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li01684174215"></a>**PortMapping**

    指定sandbox的端口映射配置

    | **参数成员**         | **描述**           |
    |----------------------|--------------------|
    | Protocol protocol    | 端口映射使用的协议 |
    | int32 container_port | 容器内的端口号     |
    | int32 host_port      | 主机上的端口号     |
    | string host_ip       | 主机IP地址         |

- **MountPropagation**

    挂载传播属性的enum列表

    <a name="zh-cn_topic_0182207110_table227603213110"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row19276183217111"><th class="cellrowborder" valign="top" width="39.53%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p1438363819110"><a name="zh-cn_topic_0182207110_p1438363819110"></a><a name="zh-cn_topic_0182207110_p1438363819110"></a><strong id="zh-cn_topic_0182207110_b18383238119"><a name="zh-cn_topic_0182207110_b18383238119"></a><a name="zh-cn_topic_0182207110_b18383238119"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="60.47%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p538314381119"><a name="zh-cn_topic_0182207110_p538314381119"></a><a name="zh-cn_topic_0182207110_p538314381119"></a><strong id="zh-cn_topic_0182207110_b3383338211"><a name="zh-cn_topic_0182207110_b3383338211"></a><a name="zh-cn_topic_0182207110_b3383338211"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row92761932719"><td class="cellrowborder" valign="top" width="39.53%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p73843384118"><a name="zh-cn_topic_0182207110_p73843384118"></a><a name="zh-cn_topic_0182207110_p73843384118"></a>PROPAGATION_PRIVATE = 0</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.47%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p438419385115"><a name="zh-cn_topic_0182207110_p438419385115"></a><a name="zh-cn_topic_0182207110_p438419385115"></a>无挂载传播属性，即linux中的private</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row827615321111"><td class="cellrowborder" valign="top" width="39.53%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1384138718"><a name="zh-cn_topic_0182207110_p1384138718"></a><a name="zh-cn_topic_0182207110_p1384138718"></a>PROPAGATION_HOST_TO_CONTAINER = 1</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.47%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p63841381115"><a name="zh-cn_topic_0182207110_p63841381115"></a><a name="zh-cn_topic_0182207110_p63841381115"></a>挂载属性能从host传播到容器中，即linux中的rslave</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row52761232617"><td class="cellrowborder" valign="top" width="39.53%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p13848383118"><a name="zh-cn_topic_0182207110_p13848383118"></a><a name="zh-cn_topic_0182207110_p13848383118"></a>PROPAGATION_BIDIRECTIONAL = 2</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.47%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1938419381917"><a name="zh-cn_topic_0182207110_p1938419381917"></a><a name="zh-cn_topic_0182207110_p1938419381917"></a>挂载属性能在host和容器中双向传播，即linux中的rshared</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li6779341144216"></a>**Mount**

    Mount指定host上的一个挂载卷挂载到容器中（只支持文件和文件夹\)

    | **参数成员**                 | **描述**                                                                        |
    |------------------------------|---------------------------------------------------------------------------------|
    | string container_path        | 容器中的路径                                                                    |
    | string host_path             | 主机上的路径                                                                    |
    | bool readonly                | 是否配置在容器中是只读的， 缺省值： false                                       |
    | bool selinux_relabel         | 是否设置SELinux标签（不支持配置）                                               |
    | MountPropagation propagation | 挂载传播属性配置（取值**0/1/2**，分别对应**private/rslave/rshared**传播属性） **缺省值：0** |

- <a name="zh-cn_topic_0182207110_li1182444614213"></a>**NamespaceOption**

    <a name="zh-cn_topic_0182207110_table02020429414"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row320210420420"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p3202142345"><a name="zh-cn_topic_0182207110_p3202142345"></a><a name="zh-cn_topic_0182207110_p3202142345"></a><strong id="zh-cn_topic_0182207110_b192021642444"><a name="zh-cn_topic_0182207110_b192021642444"></a><a name="zh-cn_topic_0182207110_b192021642444"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p192039421544"><a name="zh-cn_topic_0182207110_p192039421544"></a><a name="zh-cn_topic_0182207110_p192039421544"></a><strong id="zh-cn_topic_0182207110_b42031422411"><a name="zh-cn_topic_0182207110_b42031422411"></a><a name="zh-cn_topic_0182207110_b42031422411"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row12032421840"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p4203942245"><a name="zh-cn_topic_0182207110_p4203942245"></a><a name="zh-cn_topic_0182207110_p4203942245"></a>bool host_network</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1420374210411"><a name="zh-cn_topic_0182207110_p1420374210411"></a><a name="zh-cn_topic_0182207110_p1420374210411"></a>是否使用host的网络命名空间</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row132037421842"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p520312421344"><a name="zh-cn_topic_0182207110_p520312421344"></a><a name="zh-cn_topic_0182207110_p520312421344"></a>bool host_pid</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p17203194215418"><a name="zh-cn_topic_0182207110_p17203194215418"></a><a name="zh-cn_topic_0182207110_p17203194215418"></a>是否使用host的PID命名空间</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row1320315420416"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p620344217419"><a name="zh-cn_topic_0182207110_p620344217419"></a><a name="zh-cn_topic_0182207110_p620344217419"></a>bool host_ipc</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p12049428416"><a name="zh-cn_topic_0182207110_p12049428416"></a><a name="zh-cn_topic_0182207110_p12049428416"></a>是否使用host的IPC命名空间</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li115631277434"></a>**Capability**

    包含待添加与待删除的权能信息

    <a name="zh-cn_topic_0182207110_table4642103774315"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1642837164314"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p12642737104318"><a name="zh-cn_topic_0182207110_p12642737104318"></a><a name="zh-cn_topic_0182207110_p12642737104318"></a><strong id="zh-cn_topic_0182207110_b136421037184314"><a name="zh-cn_topic_0182207110_b136421037184314"></a><a name="zh-cn_topic_0182207110_b136421037184314"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1642193713437"><a name="zh-cn_topic_0182207110_p1642193713437"></a><a name="zh-cn_topic_0182207110_p1642193713437"></a><strong id="zh-cn_topic_0182207110_b66421237104316"><a name="zh-cn_topic_0182207110_b66421237104316"></a><a name="zh-cn_topic_0182207110_b66421237104316"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row86421337144310"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1855613286710"><a name="zh-cn_topic_0182207110_p1855613286710"></a><a name="zh-cn_topic_0182207110_p1855613286710"></a>repeated string add_capabilities</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p199319241760"><a name="zh-cn_topic_0182207110_p199319241760"></a><a name="zh-cn_topic_0182207110_p199319241760"></a>待新增的权能</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row5642103716437"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p3664193316710"><a name="zh-cn_topic_0182207110_p3664193316710"></a><a name="zh-cn_topic_0182207110_p3664193316710"></a>repeated string drop_capabilities</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p5492190683"><a name="zh-cn_topic_0182207110_p5492190683"></a><a name="zh-cn_topic_0182207110_p5492190683"></a>待删除的权能</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li1439643415372"></a>**Int64Value**

    int64类型的封装

    <a name="zh-cn_topic_0182207110_table175763341468"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1157618341465"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p457610342062"><a name="zh-cn_topic_0182207110_p457610342062"></a><a name="zh-cn_topic_0182207110_p457610342062"></a><strong id="zh-cn_topic_0182207110_b20576163416620"><a name="zh-cn_topic_0182207110_b20576163416620"></a><a name="zh-cn_topic_0182207110_b20576163416620"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p185762341468"><a name="zh-cn_topic_0182207110_p185762341468"></a><a name="zh-cn_topic_0182207110_p185762341468"></a><strong id="zh-cn_topic_0182207110_b13576163419614"><a name="zh-cn_topic_0182207110_b13576163419614"></a><a name="zh-cn_topic_0182207110_b13576163419614"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row357619342066"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p15763341367"><a name="zh-cn_topic_0182207110_p15763341367"></a><a name="zh-cn_topic_0182207110_p15763341367"></a>int64 value</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p175761534163"><a name="zh-cn_topic_0182207110_p175761534163"></a><a name="zh-cn_topic_0182207110_p175761534163"></a>实际的int64值</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li1886455713453"></a>**UInt64Value**

    uint64类型的封装

    <a name="zh-cn_topic_0182207110_table1286495744514"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1486419572459"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p886515724519"><a name="zh-cn_topic_0182207110_p886515724519"></a><a name="zh-cn_topic_0182207110_p886515724519"></a><strong id="zh-cn_topic_0182207110_b188652575456"><a name="zh-cn_topic_0182207110_b188652575456"></a><a name="zh-cn_topic_0182207110_b188652575456"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p11865155764517"><a name="zh-cn_topic_0182207110_p11865155764517"></a><a name="zh-cn_topic_0182207110_p11865155764517"></a><strong id="zh-cn_topic_0182207110_b1386575710453"><a name="zh-cn_topic_0182207110_b1386575710453"></a><a name="zh-cn_topic_0182207110_b1386575710453"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row10865185718453"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p8865145713455"><a name="zh-cn_topic_0182207110_p8865145713455"></a><a name="zh-cn_topic_0182207110_p8865145713455"></a>uint64 value</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1486535720450"><a name="zh-cn_topic_0182207110_p1486535720450"></a><a name="zh-cn_topic_0182207110_p1486535720450"></a>实际的uint64值</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li20215550104713"></a>**LinuxSandboxSecurityContext** 

    配置sandbox的linux安全选项。

    注意，这些安全选项不会应用到sandbox中的容器中，也可能不适用于没有任何running进程的sandbox。

    | **参数成员**                       | **描述**                                                                                                                                                                                       |
    |------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | NamespaceOption namespace_options  | 配置sandbox的命名空间选项                                                                                                                                                                      |
    | SELinuxOption selinux_options      | 配置SELinux选项（不支持）                                                                                                                                                                      |
    | Int64Value run_as_user             | 配置sandbox中进程的uid                                                                                                                                                                         |
    | bool readonly_rootfs               | 配置sandbox的根文件系统是否只读                                                                                                                                                                |
    | repeated int64 supplemental_groups | 配置除主GID之外的sandbox的1号进程用户组信息                                                                                                                                                    |
    | bool privileged                    | 配置sandbox是否为特权容器                                                                                                                                                                      |
    | string seccomp_profile_path        | seccomp配置文件路径，有效值为：<br> // unconfined: 不配置seccomp <br> // localhost/\<配置文件的全路径>： 安装在系统上的配置文件路径 <br> // \<配置文件的全路径>： 配置文件全路径 <br> // 默认不配置，即unconfined。 |

- <a name="zh-cn_topic_0182207110_li14801654104710"></a>**LinuxPodSandboxConfig**

    设定和Linux主机及容器相关的一些配置

    | **参数成员**                                 | **描述**                                                                                |
    |----------------------------------------------|-----------------------------------------------------------------------------------------|
    | string cgroup_parent                         | sandbox的cgroup父路径，runtime可根据实际情况使用cgroupfs或systemd的语法。（不支持配置） |
    | LinuxSandboxSecurityContext security_context | sandbox的安全属性                                                                       |
    | map\<string, string> sysctls                  | sandbox的linux sysctls配置                                                              |

- <a name="zh-cn_topic_0182207110_li2359918134912"></a>**PodSandboxMetadata**

    Sandbox元数据包含构建sandbox名称的所有信息，鼓励容器运行时在用户界面中公开这些元数据以获得更好的用户体验，例如，运行时可以根据元数据生成sandbox的唯一命名。

    <a name="zh-cn_topic_0182207110_table2402163911295"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1040017392290"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p19400339132913"><a name="zh-cn_topic_0182207110_p19400339132913"></a><a name="zh-cn_topic_0182207110_p19400339132913"></a><strong id="zh-cn_topic_0182207110_b16400163915299"><a name="zh-cn_topic_0182207110_b16400163915299"></a><a name="zh-cn_topic_0182207110_b16400163915299"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1040013932916"><a name="zh-cn_topic_0182207110_p1040013932916"></a><a name="zh-cn_topic_0182207110_p1040013932916"></a><strong id="zh-cn_topic_0182207110_b1640093912291"><a name="zh-cn_topic_0182207110_b1640093912291"></a><a name="zh-cn_topic_0182207110_b1640093912291"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row164012392296"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1240016398298"><a name="zh-cn_topic_0182207110_p1240016398298"></a><a name="zh-cn_topic_0182207110_p1240016398298"></a>string name</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p184001139192918"><a name="zh-cn_topic_0182207110_p184001139192918"></a><a name="zh-cn_topic_0182207110_p184001139192918"></a>sandbox的名称</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row16401739152913"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p164010395299"><a name="zh-cn_topic_0182207110_p164010395299"></a><a name="zh-cn_topic_0182207110_p164010395299"></a>string uid</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p18401183917297"><a name="zh-cn_topic_0182207110_p18401183917297"></a><a name="zh-cn_topic_0182207110_p18401183917297"></a>sandbox的UID</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row5401143962911"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p7560134312404"><a name="zh-cn_topic_0182207110_p7560134312404"></a><a name="zh-cn_topic_0182207110_p7560134312404"></a>string namespace</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p104011339192911"><a name="zh-cn_topic_0182207110_p104011339192911"></a><a name="zh-cn_topic_0182207110_p104011339192911"></a>sandbox的命名空间</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row16402739152910"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p386824574014"><a name="zh-cn_topic_0182207110_p386824574014"></a><a name="zh-cn_topic_0182207110_p386824574014"></a>uint32 attempt</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p5402133913294"><a name="zh-cn_topic_0182207110_p5402133913294"></a><a name="zh-cn_topic_0182207110_p5402133913294"></a>尝试创建sandbox的次数，默认为0</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li253629701"></a>**PodSandboxConfig**

    包含创建sandbox的所有必选和可选配置信息

    | **参数成员**                       | **描述**                                                                                                                                            |
    |------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
    | PodSandboxMetadata metadata        | sandbox的元数据，这项信息唯一标识一个sandbox，runtime必须利用此信息确保操作正确，runtime也可以根据此信息来改善用户体验，例如构建可读的sandbox名称。 |
    | string hostname                    | sandbox的hostname                                                                                                                                   |
    | string log_directory               | 配置sandbox内的容器的日志文件所存储的文件夹                                                                                                         |
    | DNSConfig dns_config               | sandbox的DNS配置                                                                                                                                    |
    | repeated PortMapping port_mappings | sandbox的端口映射                                                                                                                                   |
    | map\<string, string> labels         | 可用于标识单个或一系列sandbox的键值对                                                                                                               |
    | map\<string, string> annotations    | 存储任意信息的键值对，这些值是不可更改的，且能够利用PodSandboxStatus接口查询                                                                        |
    | LinuxPodSandboxConfig linux        | 与linux主机相关的可选项                                                                                                                             |

- <a name="zh-cn_topic_0182207110_li255017717184"></a>**PodSandboxNetworkStatus**

    描述sandbox的网络状态

    <a name="zh-cn_topic_0182207110_table72691154578"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1426817555712"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p11268195195715"><a name="zh-cn_topic_0182207110_p11268195195715"></a><a name="zh-cn_topic_0182207110_p11268195195715"></a><strong id="zh-cn_topic_0182207110_b326855125718"><a name="zh-cn_topic_0182207110_b326855125718"></a><a name="zh-cn_topic_0182207110_b326855125718"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p62682585719"><a name="zh-cn_topic_0182207110_p62682585719"></a><a name="zh-cn_topic_0182207110_p62682585719"></a><strong id="zh-cn_topic_0182207110_b3268125185718"><a name="zh-cn_topic_0182207110_b3268125185718"></a><a name="zh-cn_topic_0182207110_b3268125185718"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row172681054577"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p2268115105719"><a name="zh-cn_topic_0182207110_p2268115105719"></a><a name="zh-cn_topic_0182207110_p2268115105719"></a>string ip</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1126875195713"><a name="zh-cn_topic_0182207110_p1126875195713"></a><a name="zh-cn_topic_0182207110_p1126875195713"></a>sandbox的ip地址</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row5269185155714"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p17269156575"><a name="zh-cn_topic_0182207110_p17269156575"></a><a name="zh-cn_topic_0182207110_p17269156575"></a>string name</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p42699510571"><a name="zh-cn_topic_0182207110_p42699510571"></a><a name="zh-cn_topic_0182207110_p42699510571"></a>sandbox内的网络接口名</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row42691252575"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p9269135185718"><a name="zh-cn_topic_0182207110_p9269135185718"></a><a name="zh-cn_topic_0182207110_p9269135185718"></a>string network</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p162698595711"><a name="zh-cn_topic_0182207110_p162698595711"></a><a name="zh-cn_topic_0182207110_p162698595711"></a>附加网络的名称</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li523062951815"></a>**Namespace**

    命名空间选项

    | **参数成员**            | **描述**           |
    |-------------------------|--------------------|
    | NamespaceOption options | Linux 命名空间选项 |

- <a name="zh-cn_topic_0182207110_li313112151212"></a>**LinuxPodSandboxStatus**

    描述Linux sandbox的状态

    | **参数成员**         | **描述**        |
    |----------------------|-----------------|
    | Namespace **namespaces** | sandbox命名空间 |

- <a name="zh-cn_topic_0182207110_li1818214574195"></a>**PodSandboxState**

    sandbox状态值的enum数据

    <a name="zh-cn_topic_0182207110_table143182491816"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row843262417180"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p94326242187"><a name="zh-cn_topic_0182207110_p94326242187"></a><a name="zh-cn_topic_0182207110_p94326242187"></a><strong id="zh-cn_topic_0182207110_b943212249180"><a name="zh-cn_topic_0182207110_b943212249180"></a><a name="zh-cn_topic_0182207110_b943212249180"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1643202481814"><a name="zh-cn_topic_0182207110_p1643202481814"></a><a name="zh-cn_topic_0182207110_p1643202481814"></a><strong id="zh-cn_topic_0182207110_b1343252414189"><a name="zh-cn_topic_0182207110_b1343252414189"></a><a name="zh-cn_topic_0182207110_b1343252414189"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row943216241182"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p19432724181818"><a name="zh-cn_topic_0182207110_p19432724181818"></a><a name="zh-cn_topic_0182207110_p19432724181818"></a>SANDBOX_READY = 0</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p114321124161816"><a name="zh-cn_topic_0182207110_p114321124161816"></a><a name="zh-cn_topic_0182207110_p114321124161816"></a>sandbox处于ready状态</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row8935427161820"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p10935102791811"><a name="zh-cn_topic_0182207110_p10935102791811"></a><a name="zh-cn_topic_0182207110_p10935102791811"></a>SANDBOX_NOTREADY = 1</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p193562716181"><a name="zh-cn_topic_0182207110_p193562716181"></a><a name="zh-cn_topic_0182207110_p193562716181"></a>sandbox处于非ready状态</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li146986172010"></a>**PodSandboxStatus**

    描述Podsandbox的状态信息

    | **参数成员**                              | **描述**                                          |
    |-------------------------------------------|---------------------------------------------------|
    | string id                                 | sandbox的ID                                       |
    | PodSandboxMetadata metadata               | sandbox的元数据                                   |
    | PodSandboxState state                     | sandbox的状态值                                   |
    | int64 created_at                          | sandbox的创建时间戳，单位纳秒                     |
    | repeated PodSandboxNetworkStatus networks | sandbox的多平面网络状态                           |
    | LinuxPodSandboxStatus linux               | Linux规范的sandbox状态                            |
    | map\<string, string> labels                | 可用于标识单个或一系列sandbox的键值对             |
    | map\<string, string> annotations           | 存储任意信息的键值对，这些值是不可被runtime更改的 |

- <a name="zh-cn_topic_0182207110_li64922552019"></a>**PodSandboxStateValue**

    对PodSandboxState的封装

    | **参数成员**          | **描述**        |
    |-----------------------|-----------------|
    | PodSandboxState state | sandbox的状态值 |

- **PodSandboxFilter**

    用于列出sandbox时添加过滤条件，多个条件取交集显示

    | **参数成员**                       | **描述**                                             |
    |------------------------------------|------------------------------------------------------|
    | string id                          | sandbox的ID                                          |
    | PodSandboxStateValue state         | sandbox的状态                                        |
    | map\<string, string> label_selector | sandbox的labels，label只支持完全匹配，不支持正则匹配 |

- **PodSandbox**

    包含最小化描述一个sandbox的数据

    | **参数成员**                    | **描述**                                          |
    |---------------------------------|---------------------------------------------------|
    | string id                       | sandbox的ID                                       |
    | PodSandboxMetadata metadata     | sandbox的元数据                                   |
    | PodSandboxState state           | sandbox的状态值                                   |
    | int64 created_at                | sandbox的创建时间戳，单位纳秒                     |
    | map\<string, string> labels      | 可用于标识单个或一系列sandbox的键值对             |
    | map\<string, string> annotations | 存储任意信息的键值对，这些值是不可被runtime更改的 |

- <a name="zh-cn_topic_0182207110_li11598132815225"></a>**KeyValue**

    键值对的封装

    <a name="zh-cn_topic_0182207110_table062733315339"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row136281333113315"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p10628173318339"><a name="zh-cn_topic_0182207110_p10628173318339"></a><a name="zh-cn_topic_0182207110_p10628173318339"></a><strong id="zh-cn_topic_0182207110_b1362843363314"><a name="zh-cn_topic_0182207110_b1362843363314"></a><a name="zh-cn_topic_0182207110_b1362843363314"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1562811331332"><a name="zh-cn_topic_0182207110_p1562811331332"></a><a name="zh-cn_topic_0182207110_p1562811331332"></a><strong id="zh-cn_topic_0182207110_b1362863383315"><a name="zh-cn_topic_0182207110_b1362863383315"></a><a name="zh-cn_topic_0182207110_b1362863383315"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row12628153353311"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p14766942153319"><a name="zh-cn_topic_0182207110_p14766942153319"></a><a name="zh-cn_topic_0182207110_p14766942153319"></a>string key</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p9629733163311"><a name="zh-cn_topic_0182207110_p9629733163311"></a><a name="zh-cn_topic_0182207110_p9629733163311"></a>键</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row6629533163311"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p156291633153319"><a name="zh-cn_topic_0182207110_p156291633153319"></a><a name="zh-cn_topic_0182207110_p156291633153319"></a>string value</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p56291333113311"><a name="zh-cn_topic_0182207110_p56291333113311"></a><a name="zh-cn_topic_0182207110_p56291333113311"></a>值</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li816815620237"></a>**SELinuxOption**

    应用于容器的SELinux标签

    <a name="zh-cn_topic_0182207110_table275114812514"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row18751148155112"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p1775113816517"><a name="zh-cn_topic_0182207110_p1775113816517"></a><a name="zh-cn_topic_0182207110_p1775113816517"></a><strong id="zh-cn_topic_0182207110_b1975117865116"><a name="zh-cn_topic_0182207110_b1975117865116"></a><a name="zh-cn_topic_0182207110_b1975117865116"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1175215815114"><a name="zh-cn_topic_0182207110_p1175215815114"></a><a name="zh-cn_topic_0182207110_p1175215815114"></a><strong id="zh-cn_topic_0182207110_b47521895117"><a name="zh-cn_topic_0182207110_b47521895117"></a><a name="zh-cn_topic_0182207110_b47521895117"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row117521812514"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p2752178195111"><a name="zh-cn_topic_0182207110_p2752178195111"></a><a name="zh-cn_topic_0182207110_p2752178195111"></a>string user</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p775288145117"><a name="zh-cn_topic_0182207110_p775288145117"></a><a name="zh-cn_topic_0182207110_p775288145117"></a>用户</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row1775214818512"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p57524815514"><a name="zh-cn_topic_0182207110_p57524815514"></a><a name="zh-cn_topic_0182207110_p57524815514"></a>string role</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p975216895119"><a name="zh-cn_topic_0182207110_p975216895119"></a><a name="zh-cn_topic_0182207110_p975216895119"></a>角色</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row9445413125116"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p644521385118"><a name="zh-cn_topic_0182207110_p644521385118"></a><a name="zh-cn_topic_0182207110_p644521385118"></a>string type</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1445713125113"><a name="zh-cn_topic_0182207110_p1445713125113"></a><a name="zh-cn_topic_0182207110_p1445713125113"></a>类型</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row9753198165114"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1175368205113"><a name="zh-cn_topic_0182207110_p1175368205113"></a><a name="zh-cn_topic_0182207110_p1175368205113"></a>string level</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1475320875112"><a name="zh-cn_topic_0182207110_p1475320875112"></a><a name="zh-cn_topic_0182207110_p1475320875112"></a>级别</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li17135914132319"></a>**ContainerMetadata**

    Container元数据包含构建container名称的所有信息，鼓励容器运行时在用户界面中公开这些元数据以获得更好的用户体验，例如，运行时可以根据元数据生成container的唯一命名。

    <a name="zh-cn_topic_0182207110_table18487181915536"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row348741935315"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p748891945320"><a name="zh-cn_topic_0182207110_p748891945320"></a><a name="zh-cn_topic_0182207110_p748891945320"></a><strong id="zh-cn_topic_0182207110_b04881192534"><a name="zh-cn_topic_0182207110_b04881192534"></a><a name="zh-cn_topic_0182207110_b04881192534"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p948811191538"><a name="zh-cn_topic_0182207110_p948811191538"></a><a name="zh-cn_topic_0182207110_p948811191538"></a><strong id="zh-cn_topic_0182207110_b10488141955315"><a name="zh-cn_topic_0182207110_b10488141955315"></a><a name="zh-cn_topic_0182207110_b10488141955315"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row64884193535"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p4488181917535"><a name="zh-cn_topic_0182207110_p4488181917535"></a><a name="zh-cn_topic_0182207110_p4488181917535"></a>string name</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p14881419185315"><a name="zh-cn_topic_0182207110_p14881419185315"></a><a name="zh-cn_topic_0182207110_p14881419185315"></a>container的名称</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row3489121965312"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1848921975315"><a name="zh-cn_topic_0182207110_p1848921975315"></a><a name="zh-cn_topic_0182207110_p1848921975315"></a>uint32 attempt</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1048991916534"><a name="zh-cn_topic_0182207110_p1048991916534"></a><a name="zh-cn_topic_0182207110_p1048991916534"></a>尝试创建container的次数，默认为0</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li65182518309"></a>**ContainerState**

    容器状态值的enum列表

    <a name="zh-cn_topic_0182207110_table14224058145512"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row2224958205510"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p19224758185512"><a name="zh-cn_topic_0182207110_p19224758185512"></a><a name="zh-cn_topic_0182207110_p19224758185512"></a><strong id="zh-cn_topic_0182207110_b922410584550"><a name="zh-cn_topic_0182207110_b922410584550"></a><a name="zh-cn_topic_0182207110_b922410584550"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p132251658145511"><a name="zh-cn_topic_0182207110_p132251658145511"></a><a name="zh-cn_topic_0182207110_p132251658145511"></a><strong id="zh-cn_topic_0182207110_b192251585555"><a name="zh-cn_topic_0182207110_b192251585555"></a><a name="zh-cn_topic_0182207110_b192251585555"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row18225155815516"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1922525825513"><a name="zh-cn_topic_0182207110_p1922525825513"></a><a name="zh-cn_topic_0182207110_p1922525825513"></a>CONTAINER_CREATED = 0</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p19225115818550"><a name="zh-cn_topic_0182207110_p19225115818550"></a><a name="zh-cn_topic_0182207110_p19225115818550"></a>container创建完成</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row152257316563"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p12251436565"><a name="zh-cn_topic_0182207110_p12251436565"></a><a name="zh-cn_topic_0182207110_p12251436565"></a>CONTAINER_RUNNING = 1</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p4225132564"><a name="zh-cn_topic_0182207110_p4225132564"></a><a name="zh-cn_topic_0182207110_p4225132564"></a>container处于运行状态</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row1622595813559"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p931041915618"><a name="zh-cn_topic_0182207110_p931041915618"></a><a name="zh-cn_topic_0182207110_p931041915618"></a>CONTAINER_EXITED  = 2</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p19225658165519"><a name="zh-cn_topic_0182207110_p19225658165519"></a><a name="zh-cn_topic_0182207110_p19225658165519"></a>container处于退出状态</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row140581185618"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p194051110564"><a name="zh-cn_topic_0182207110_p194051110564"></a><a name="zh-cn_topic_0182207110_p194051110564"></a>CONTAINER_UNKNOWN = 3</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p292175415566"><a name="zh-cn_topic_0182207110_p292175415566"></a><a name="zh-cn_topic_0182207110_p292175415566"></a>未知的容器状态</p>
    </td>
    </tr>
    </tbody>
    </table>

- **ContainerStateValue**

    封装ContainerState的数据结构

    | **参数成员**         | **描述**   |
    |----------------------|------------|
    | ContainerState **state** | 容器状态值 |

- **ContainerFilter**

    用于列出container时添加过滤条件，多个条件取交集显示

    | **参数成员**                       | **描述**                                               |
    |------------------------------------|--------------------------------------------------------|
    | string id                          | container的ID                                          |
    | PodSandboxStateValue state         | container的状态                                        |
    | string pod_sandbox_id              | sandbox的ID                                            |
    | map\<string, string> label_selector | container的labels，label只支持完全匹配，不支持正则匹配 |

- <a name="zh-cn_topic_0182207110_li11771452124416"></a>**LinuxContainerSecurityContext**

    指定应用于容器的安全配置

    | **参数成员**                       | **描述**                                                                                                                           |
    |------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
    | Capability capabilities            | 新增或去除的权能                                                                                                                   |
    | bool privileged                    | 指定容器是否未特权模式， **缺省值：false**                                                                                             |
    | NamespaceOption namespace_options  | 指定容器的namespace选项                                                                                                            |
    | SELinuxOption selinux_options      | SELinux context(可选配置项) **暂不支持**                                                                                               |
    | Int64Value run_as_user             | 运行容器进程的UID。 一次只能指定run_as_user与run_as_username其中之一，run_as_username优先生效                                      |
    | string run_as_username             | 运行容器进程的用户名。 如果指定，用户必须存在于容器映像中（即在映像内的/etc/passwd中），并由运行时在那里解析; 否则，运行时必须出错 |
    | bool readonly_rootfs               | 设置容器中根文件系统是否为只读 **缺省值由config.json配置**                                                                             |
    | repeated int64 supplemental_groups | 容器运行的除主GID外首进程组的列表                                                                                                  |
    | string apparmor_profile            | 容器的AppArmor配置文件 **暂不支持**                                                                                                    |
    | string seccomp_profile_path        | 容器的seccomp配置文件路径                                                                                                          |
    | bool no_new_privs                  | 是否在容器上设置no_new_privs的标志                                                                                                 |

- <a name="zh-cn_topic_0182207110_li2050214613477"></a>**LinuxContainerResources**

    指定Linux容器资源的特定配置

    <a name="zh-cn_topic_0182207110_table1774515315492"></a>
    <table><tbody><tr id="zh-cn_topic_0182207110_row1774623104910"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p1474653124914"><a name="zh-cn_topic_0182207110_p1474653124914"></a><a name="zh-cn_topic_0182207110_p1474653124914"></a><strong id="zh-cn_topic_0182207110_b7746031114915"><a name="zh-cn_topic_0182207110_b7746031114915"></a><a name="zh-cn_topic_0182207110_b7746031114915"></a>参数成员</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p4746183124920"><a name="zh-cn_topic_0182207110_p4746183124920"></a><a name="zh-cn_topic_0182207110_p4746183124920"></a><strong id="zh-cn_topic_0182207110_b77461131174911"><a name="zh-cn_topic_0182207110_b77461131174911"></a><a name="zh-cn_topic_0182207110_b77461131174911"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row174653112494"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p7746103120496"><a name="zh-cn_topic_0182207110_p7746103120496"></a><a name="zh-cn_topic_0182207110_p7746103120496"></a>int64 cpu_period</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p9746113114911"><a name="zh-cn_topic_0182207110_p9746113114911"></a><a name="zh-cn_topic_0182207110_p9746113114911"></a>CPU CFS（完全公平调度程序）周期。 <strong id="zh-cn_topic_0182207110_b336722813364"><a name="zh-cn_topic_0182207110_b336722813364"></a><a name="zh-cn_topic_0182207110_b336722813364"></a>缺省值：0</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row474673164917"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p14746143134912"><a name="zh-cn_topic_0182207110_p14746143134912"></a><a name="zh-cn_topic_0182207110_p14746143134912"></a>int64 cpu_quota</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p17746931104919"><a name="zh-cn_topic_0182207110_p17746931104919"></a><a name="zh-cn_topic_0182207110_p17746931104919"></a>CPU CFS（完全公平调度程序）配额。 <strong id="zh-cn_topic_0182207110_b191427331363"><a name="zh-cn_topic_0182207110_b191427331363"></a><a name="zh-cn_topic_0182207110_b191427331363"></a>缺省值：0</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row9746103124914"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p17746131164912"><a name="zh-cn_topic_0182207110_p17746131164912"></a><a name="zh-cn_topic_0182207110_p17746131164912"></a>int64 cpu_shares</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p5746103111491"><a name="zh-cn_topic_0182207110_p5746103111491"></a><a name="zh-cn_topic_0182207110_p5746103111491"></a>所占CPU份额（相对于其他容器的相对权重）。<strong id="zh-cn_topic_0182207110_b18359133643614"><a name="zh-cn_topic_0182207110_b18359133643614"></a><a name="zh-cn_topic_0182207110_b18359133643614"></a> 缺省值：0</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row47463316492"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p5746183117499"><a name="zh-cn_topic_0182207110_p5746183117499"></a><a name="zh-cn_topic_0182207110_p5746183117499"></a>int64 memory_limit_in_bytes</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p17746731114919"><a name="zh-cn_topic_0182207110_p17746731114919"></a><a name="zh-cn_topic_0182207110_p17746731114919"></a>内存限制（字节）。 <strong id="zh-cn_topic_0182207110_b18820940103614"><a name="zh-cn_topic_0182207110_b18820940103614"></a><a name="zh-cn_topic_0182207110_b18820940103614"></a>缺省值：0</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row117463319495"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p1374723114913"><a name="zh-cn_topic_0182207110_p1374723114913"></a><a name="zh-cn_topic_0182207110_p1374723114913"></a>int64 oom_score_adj</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p11747731134911"><a name="zh-cn_topic_0182207110_p11747731134911"></a><a name="zh-cn_topic_0182207110_p11747731134911"></a>OOMScoreAdj用于调整oom-killer。 <strong id="zh-cn_topic_0182207110_b14735194416364"><a name="zh-cn_topic_0182207110_b14735194416364"></a><a name="zh-cn_topic_0182207110_b14735194416364"></a>缺省值：0</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row2747153115491"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p1174793116499"><a name="zh-cn_topic_0182207110_p1174793116499"></a><a name="zh-cn_topic_0182207110_p1174793116499"></a>string cpuset_cpus</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p15747133111495"><a name="zh-cn_topic_0182207110_p15747133111495"></a><a name="zh-cn_topic_0182207110_p15747133111495"></a>指定容器使用的CPU核心。 <strong id="zh-cn_topic_0182207110_b118419484363"><a name="zh-cn_topic_0182207110_b118419484363"></a><a name="zh-cn_topic_0182207110_b118419484363"></a>缺省值：“”</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row474713316497"><td class="cellrowborder" valign="top" width="39.410000000000004%"><p id="zh-cn_topic_0182207110_p1474783184919"><a name="zh-cn_topic_0182207110_p1474783184919"></a><a name="zh-cn_topic_0182207110_p1474783184919"></a>string cpuset_mems</p>
    </td>
    <td class="cellrowborder" valign="top" width="60.589999999999996%"><p id="zh-cn_topic_0182207110_p6747331134912"><a name="zh-cn_topic_0182207110_p6747331134912"></a><a name="zh-cn_topic_0182207110_p6747331134912"></a>指定容器使用的内存节点。<strong id="zh-cn_topic_0182207110_b133071051163613"><a name="zh-cn_topic_0182207110_b133071051163613"></a><a name="zh-cn_topic_0182207110_b133071051163613"></a> 缺省值：“”</strong></p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li597891416252"></a>**Image**

    Image信息描述一个镜像的基本数据。

    | **参数成员**                 | **描述**               |
    |------------------------------|------------------------|
    | string id                    | 镜像ID                 |
    | repeated string repo_tags    | 镜像tag 名称 repo_tags |
    | repeated string repo_digests | 镜像digest信息         |
    | uint64 size                  | 镜像大小               |
    | Int64Value uid               | 镜像默认用户UID        |
    | string username              | 镜像默认用户名称       |

- **ImageSpec**

    表示镜像的内部数据结构，当前，ImageSpec只封装容器镜像名称

    <a name="zh-cn_topic_0182207110_table312519561623"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row18125195617212"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p11257567212"><a name="zh-cn_topic_0182207110_p11257567212"></a><a name="zh-cn_topic_0182207110_p11257567212"></a><strong id="zh-cn_topic_0182207110_b91256561827"><a name="zh-cn_topic_0182207110_b91256561827"></a><a name="zh-cn_topic_0182207110_b91256561827"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p712510568216"><a name="zh-cn_topic_0182207110_p712510568216"></a><a name="zh-cn_topic_0182207110_p712510568216"></a><strong id="zh-cn_topic_0182207110_b6125756624"><a name="zh-cn_topic_0182207110_b6125756624"></a><a name="zh-cn_topic_0182207110_b6125756624"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row412515561825"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1712575615213"><a name="zh-cn_topic_0182207110_p1712575615213"></a><a name="zh-cn_topic_0182207110_p1712575615213"></a>string image</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p8125956526"><a name="zh-cn_topic_0182207110_p8125956526"></a><a name="zh-cn_topic_0182207110_p8125956526"></a>容器镜像名</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li3285401546"></a>**StorageIdentifier**

    唯一定义storage的标识

    <a name="zh-cn_topic_0182207110_table22818405417"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row22819405420"><th class="cellrowborder" valign="top" width="40.52%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p18283400411"><a name="zh-cn_topic_0182207110_p18283400411"></a><a name="zh-cn_topic_0182207110_p18283400411"></a><strong id="zh-cn_topic_0182207110_b528840047"><a name="zh-cn_topic_0182207110_b528840047"></a><a name="zh-cn_topic_0182207110_b528840047"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.48%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p8281140541"><a name="zh-cn_topic_0182207110_p8281140541"></a><a name="zh-cn_topic_0182207110_p8281140541"></a><strong id="zh-cn_topic_0182207110_b128940142"><a name="zh-cn_topic_0182207110_b128940142"></a><a name="zh-cn_topic_0182207110_b128940142"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row12817404411"><td class="cellrowborder" valign="top" width="40.52%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p942172311510"><a name="zh-cn_topic_0182207110_p942172311510"></a><a name="zh-cn_topic_0182207110_p942172311510"></a>string uuid</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.48%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p62920401145"><a name="zh-cn_topic_0182207110_p62920401145"></a><a name="zh-cn_topic_0182207110_p62920401145"></a>设备的UUID</p>
    </td>
    </tr>
    </tbody>
    </table>

- **FilesystemUsage**

    | **参数成员**                 | **描述**                   |
    |------------------------------|----------------------------|
    | int64 timestamp              | 收集文件系统信息时的时间戳 |
    | StorageIdentifier storage_id | 存储镜像的文件系统UUID     |
    | UInt64Value used_bytes       | 存储镜像元数据的大小       |
    | UInt64Value inodes_used      | 存储镜像元数据的inodes个数 |

- **AuthConfig**

    <a name="zh-cn_topic_0182207110_table51991144738"></a>
    <table><tbody><tr id="zh-cn_topic_0182207110_row419944410312"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1519964418314"><a name="zh-cn_topic_0182207110_p1519964418314"></a><a name="zh-cn_topic_0182207110_p1519964418314"></a><strong id="zh-cn_topic_0182207110_b51995449315"><a name="zh-cn_topic_0182207110_b51995449315"></a><a name="zh-cn_topic_0182207110_b51995449315"></a>参数成员</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p1319910447317"><a name="zh-cn_topic_0182207110_p1319910447317"></a><a name="zh-cn_topic_0182207110_p1319910447317"></a><strong id="zh-cn_topic_0182207110_b319914418314"><a name="zh-cn_topic_0182207110_b319914418314"></a><a name="zh-cn_topic_0182207110_b319914418314"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row819918441338"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1199174414319"><a name="zh-cn_topic_0182207110_p1199174414319"></a><a name="zh-cn_topic_0182207110_p1199174414319"></a>string username</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p16199194419310"><a name="zh-cn_topic_0182207110_p16199194419310"></a><a name="zh-cn_topic_0182207110_p16199194419310"></a>下载镜像使用的用户名</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row01991844833"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1119910441131"><a name="zh-cn_topic_0182207110_p1119910441131"></a><a name="zh-cn_topic_0182207110_p1119910441131"></a>string password</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p141998442310"><a name="zh-cn_topic_0182207110_p141998442310"></a><a name="zh-cn_topic_0182207110_p141998442310"></a>下载镜像使用的密码</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row21992441835"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p20199544734"><a name="zh-cn_topic_0182207110_p20199544734"></a><a name="zh-cn_topic_0182207110_p20199544734"></a>string auth</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p219917441631"><a name="zh-cn_topic_0182207110_p219917441631"></a><a name="zh-cn_topic_0182207110_p219917441631"></a>下载镜像时使用的认证信息，base64编码</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row161994442311"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1019917448312"><a name="zh-cn_topic_0182207110_p1019917448312"></a><a name="zh-cn_topic_0182207110_p1019917448312"></a>string server_address</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p1219915441319"><a name="zh-cn_topic_0182207110_p1219915441319"></a><a name="zh-cn_topic_0182207110_p1219915441319"></a>下载镜像的服务器地址，暂不支持</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row141995442310"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p5199944834"><a name="zh-cn_topic_0182207110_p5199944834"></a><a name="zh-cn_topic_0182207110_p5199944834"></a>string identity_token</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p7199134414318"><a name="zh-cn_topic_0182207110_p7199134414318"></a><a name="zh-cn_topic_0182207110_p7199134414318"></a>用于与镜像仓库鉴权的令牌信息，暂不支持</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row11199174420317"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p5199174410316"><a name="zh-cn_topic_0182207110_p5199174410316"></a><a name="zh-cn_topic_0182207110_p5199174410316"></a>string registry_token</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p2199104418310"><a name="zh-cn_topic_0182207110_p2199104418310"></a><a name="zh-cn_topic_0182207110_p2199104418310"></a>用于与镜像仓库交互的令牌信息，暂不支持</p>
    </td>
    </tr>
    </tbody>
    </table>

- **Container**

    用于描述容器信息，例如ID, 状态等。

    | **参数成员**                    | **描述**                                                    |
    |---------------------------------|-------------------------------------------------------------|
    | string id                       | container的ID                                               |
    | string pod_sandbox_id           | 该容器所属的sandbox的ID                                     |
    | ContainerMetadata metadata      | container的元数据                                           |
    | ImageSpec image                 | 镜像规格                                                    |
    | string image_ref                | 代表容器使用的镜像，对大多数runtime来产，这是一个image ID值 |
    | ContainerState state            | container的状态                                             |
    | int64 created_at                | container的创建时间戳，单位为纳秒                           |
    | map\<string, string> labels      | 可用于标识单个或一系列container的键值对                     |
    | map\<string, string> annotations | 存储任意信息的键值对，这些值是不可被runtime更改的           |

- **ContainerStatus**

    用于描述容器状态信息

    | **参数成员**                    | **描述**                                                                  |
    |---------------------------------|---------------------------------------------------------------------------|
    | string id                       | container的ID                                                             |
    | ContainerMetadata metadata      | container的元数据                                                         |
    | ContainerState state            | container的状态                                                           |
    | int64 created_at                | container的创建时间戳，单位为纳秒                                         |
    | int64 started_at                | container启动时的时间戳，单位为纳秒                                       |
    | int64 finished_at               | container退出时的时间戳，单位为纳秒                                       |
    | int32 exit_code                 | 容器退出码                                                                |
    | ImageSpec image                 | 镜像规格                                                                  |
    | string image_ref                | 代表容器使用的镜像，对大多数runtime来产，这是一个image ID值               |
    | string reason                   | 简要描述为什么容器处于当前状态                                            |
    | string message                  | 易于人工阅读的信息，用于表述容器处于当前状态的原因                        |
    | map\<string, string> labels      | 可用于标识单个或一系列container的键值对                                   |
    | map\<string, string> annotations | 存储任意信息的键值对，这些值是不可被runtime更改的                         |
    | repeated Mount mounts           | 容器的挂载点信息                                                          |
    | string log_path                 | 容器日志文件路径，该文件位于PodSandboxConfig中配置的log_directory文件夹下 |

- **ContainerStatsFilter**

    用于列出container stats时添加过滤条件，多个条件取交集显示

    <a name="zh-cn_topic_0182207110_table78595160148"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1860171616141"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p188605168143"><a name="zh-cn_topic_0182207110_p188605168143"></a><a name="zh-cn_topic_0182207110_p188605168143"></a><strong id="zh-cn_topic_0182207110_b486021611418"><a name="zh-cn_topic_0182207110_b486021611418"></a><a name="zh-cn_topic_0182207110_b486021611418"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p78601916161416"><a name="zh-cn_topic_0182207110_p78601916161416"></a><a name="zh-cn_topic_0182207110_p78601916161416"></a><strong id="zh-cn_topic_0182207110_b086011167149"><a name="zh-cn_topic_0182207110_b086011167149"></a><a name="zh-cn_topic_0182207110_b086011167149"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row486021618140"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p38609162146"><a name="zh-cn_topic_0182207110_p38609162146"></a><a name="zh-cn_topic_0182207110_p38609162146"></a>string id</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p5860171621418"><a name="zh-cn_topic_0182207110_p5860171621418"></a><a name="zh-cn_topic_0182207110_p5860171621418"></a>container的ID</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row18611316111416"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p586191610143"><a name="zh-cn_topic_0182207110_p586191610143"></a><a name="zh-cn_topic_0182207110_p586191610143"></a>string pod_sandbox_id</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p18861171641420"><a name="zh-cn_topic_0182207110_p18861171641420"></a><a name="zh-cn_topic_0182207110_p18861171641420"></a>sandbox的ID</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row1786381671416"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p138631016171414"><a name="zh-cn_topic_0182207110_p138631016171414"></a><a name="zh-cn_topic_0182207110_p138631016171414"></a>map&lt;string, string&gt; label_selector</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p5863181641417"><a name="zh-cn_topic_0182207110_p5863181641417"></a><a name="zh-cn_topic_0182207110_p5863181641417"></a>container的labels，label只支持完全匹配，不支持正则匹配</p>
    </td>
    </tr>
    </tbody>
    </table>

- **ContainerStats**

    用于列出container stats时添加过滤条件，多个条件取交集显示

    | **参数成员**                   | **描述**       |
    |--------------------------------|----------------|
    | ContainerAttributes attributes | 容器的信息     |
    | CpuUsage cpu                   | CPU使用情况    |
    | MemoryUsage memory             | 内存使用情况   |
    | FilesystemUsage writable_layer | 可写层使用情况 |

- <a name="zh-cn_topic_0182207110_li6207185712312"></a>**ContainerAttributes**

    列出container的基本信息

    | **参数成员**                   | **描述**                                          |
    |--------------------------------|---------------------------------------------------|
    | string id                      | 容器的ID                                          |
    | ContainerMetadata metadata     | 容器的metadata                                    |
    | map\<string,string> labels      | 可用于标识单个或一系列container的键值对           |
    | map\<string,string> annotations | 存储任意信息的键值对，这些值是不可被runtime更改的 |

- <a name="zh-cn_topic_0182207110_li1367131122711"></a>**CpuUsage**

    列出container的CPU使用信息

    <a name="zh-cn_topic_0182207110_table103679116272"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row113674110278"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p13681416276"><a name="zh-cn_topic_0182207110_p13681416276"></a><a name="zh-cn_topic_0182207110_p13681416276"></a><strong id="zh-cn_topic_0182207110_b11368191112715"><a name="zh-cn_topic_0182207110_b11368191112715"></a><a name="zh-cn_topic_0182207110_b11368191112715"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p1736861142719"><a name="zh-cn_topic_0182207110_p1736861142719"></a><a name="zh-cn_topic_0182207110_p1736861142719"></a><strong id="zh-cn_topic_0182207110_b8368913271"><a name="zh-cn_topic_0182207110_b8368913271"></a><a name="zh-cn_topic_0182207110_b8368913271"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row193687118272"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p96863242710"><a name="zh-cn_topic_0182207110_p96863242710"></a><a name="zh-cn_topic_0182207110_p96863242710"></a>int64 timestamp</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p17368412273"><a name="zh-cn_topic_0182207110_p17368412273"></a><a name="zh-cn_topic_0182207110_p17368412273"></a>时间戳</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row123686112271"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p2635942132713"><a name="zh-cn_topic_0182207110_p2635942132713"></a><a name="zh-cn_topic_0182207110_p2635942132713"></a>UInt64Value usage_core_nano_seconds</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p103680172713"><a name="zh-cn_topic_0182207110_p103680172713"></a><a name="zh-cn_topic_0182207110_p103680172713"></a>CPU的使用值，单位/纳秒</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li81221520111718"></a>**MemoryUsage**

    列出container的内存使用信息

    <a name="zh-cn_topic_0182207110_table81231820141716"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row1012332021712"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p11233203174"><a name="zh-cn_topic_0182207110_p11233203174"></a><a name="zh-cn_topic_0182207110_p11233203174"></a><strong id="zh-cn_topic_0182207110_b5123142014178"><a name="zh-cn_topic_0182207110_b5123142014178"></a><a name="zh-cn_topic_0182207110_b5123142014178"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p81231920111718"><a name="zh-cn_topic_0182207110_p81231920111718"></a><a name="zh-cn_topic_0182207110_p81231920111718"></a><strong id="zh-cn_topic_0182207110_b19123152010177"><a name="zh-cn_topic_0182207110_b19123152010177"></a><a name="zh-cn_topic_0182207110_b19123152010177"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row1012362017178"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1612318202170"><a name="zh-cn_topic_0182207110_p1612318202170"></a><a name="zh-cn_topic_0182207110_p1612318202170"></a>int64 timestamp</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p3124192071710"><a name="zh-cn_topic_0182207110_p3124192071710"></a><a name="zh-cn_topic_0182207110_p3124192071710"></a>时间戳</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row1312442021716"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p1712412071712"><a name="zh-cn_topic_0182207110_p1712412071712"></a><a name="zh-cn_topic_0182207110_p1712412071712"></a>UInt64Value working_set_bytes</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p11241209172"><a name="zh-cn_topic_0182207110_p11241209172"></a><a name="zh-cn_topic_0182207110_p11241209172"></a>内存的使用值</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li1606183118189"></a>**FilesystemUsage**

    列出container的读写层信息

    <a name="zh-cn_topic_0182207110_table166071315186"></a>
    <table><thead align="left"><tr id="zh-cn_topic_0182207110_row196071731201813"><th class="cellrowborder" valign="top" width="40.43%" id="mcps1.1.3.1.1"><p id="zh-cn_topic_0182207110_p13607163114183"><a name="zh-cn_topic_0182207110_p13607163114183"></a><a name="zh-cn_topic_0182207110_p13607163114183"></a><strong id="zh-cn_topic_0182207110_b3608931171814"><a name="zh-cn_topic_0182207110_b3608931171814"></a><a name="zh-cn_topic_0182207110_b3608931171814"></a>参数成员</strong></p>
    </th>
    <th class="cellrowborder" valign="top" width="59.57%" id="mcps1.1.3.1.2"><p id="zh-cn_topic_0182207110_p16608103181811"><a name="zh-cn_topic_0182207110_p16608103181811"></a><a name="zh-cn_topic_0182207110_p16608103181811"></a><strong id="zh-cn_topic_0182207110_b6608113114183"><a name="zh-cn_topic_0182207110_b6608113114183"></a><a name="zh-cn_topic_0182207110_b6608113114183"></a>描述</strong></p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="zh-cn_topic_0182207110_row3608731151813"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p360803151817"><a name="zh-cn_topic_0182207110_p360803151817"></a><a name="zh-cn_topic_0182207110_p360803151817"></a>int64 timestamp</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p1860973118188"><a name="zh-cn_topic_0182207110_p1860973118188"></a><a name="zh-cn_topic_0182207110_p1860973118188"></a>时间戳</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row106094314181"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p17609113181811"><a name="zh-cn_topic_0182207110_p17609113181811"></a><a name="zh-cn_topic_0182207110_p17609113181811"></a>StorageIdentifier storage_id</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p16609231151818"><a name="zh-cn_topic_0182207110_p16609231151818"></a><a name="zh-cn_topic_0182207110_p16609231151818"></a>可写层目录</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row368116322190"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p968113281915"><a name="zh-cn_topic_0182207110_p968113281915"></a><a name="zh-cn_topic_0182207110_p968113281915"></a>UInt64Value used_bytes</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p2681193221911"><a name="zh-cn_topic_0182207110_p2681193221911"></a><a name="zh-cn_topic_0182207110_p2681193221911"></a>镜像在可写层的占用字节</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row29601026152012"><td class="cellrowborder" valign="top" width="40.43%" headers="mcps1.1.3.1.1 "><p id="zh-cn_topic_0182207110_p896002618203"><a name="zh-cn_topic_0182207110_p896002618203"></a><a name="zh-cn_topic_0182207110_p896002618203"></a>UInt64Value inodes_used</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.57%" headers="mcps1.1.3.1.2 "><p id="zh-cn_topic_0182207110_p17960122616208"><a name="zh-cn_topic_0182207110_p17960122616208"></a><a name="zh-cn_topic_0182207110_p17960122616208"></a>镜像在可写层的占用inode数</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li19916726173311"></a>**Device**

    指定待挂载至容器的主机卷

    <a name="zh-cn_topic_0182207110_table178013246294"></a>
    <table><tbody><tr id="zh-cn_topic_0182207110_row0807249290"><td class="cellrowborder" valign="top" width="40.61%"><p id="zh-cn_topic_0182207110_p15804244293"><a name="zh-cn_topic_0182207110_p15804244293"></a><a name="zh-cn_topic_0182207110_p15804244293"></a><strong id="zh-cn_topic_0182207110_b1380524152918"><a name="zh-cn_topic_0182207110_b1380524152918"></a><a name="zh-cn_topic_0182207110_b1380524152918"></a>参数成员</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="59.39%"><p id="zh-cn_topic_0182207110_p14801324132915"><a name="zh-cn_topic_0182207110_p14801324132915"></a><a name="zh-cn_topic_0182207110_p14801324132915"></a><strong id="zh-cn_topic_0182207110_b88032412298"><a name="zh-cn_topic_0182207110_b88032412298"></a><a name="zh-cn_topic_0182207110_b88032412298"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row98002422914"><td class="cellrowborder" valign="top" width="40.61%"><p id="zh-cn_topic_0182207110_p28062414297"><a name="zh-cn_topic_0182207110_p28062414297"></a><a name="zh-cn_topic_0182207110_p28062414297"></a>string container_path</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.39%"><p id="zh-cn_topic_0182207110_p188019244297"><a name="zh-cn_topic_0182207110_p188019244297"></a><a name="zh-cn_topic_0182207110_p188019244297"></a>容器内的挂载路径</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row48042417299"><td class="cellrowborder" valign="top" width="40.61%"><p id="zh-cn_topic_0182207110_p88082412293"><a name="zh-cn_topic_0182207110_p88082412293"></a><a name="zh-cn_topic_0182207110_p88082412293"></a>string host_path</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.39%"><p id="zh-cn_topic_0182207110_p118062420297"><a name="zh-cn_topic_0182207110_p118062420297"></a><a name="zh-cn_topic_0182207110_p118062420297"></a>主机上的挂载路径</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row3801624162913"><td class="cellrowborder" valign="top" width="40.61%"><p id="zh-cn_topic_0182207110_p51611220303"><a name="zh-cn_topic_0182207110_p51611220303"></a><a name="zh-cn_topic_0182207110_p51611220303"></a>string permissions</p>
    </td>
    <td class="cellrowborder" valign="top" width="59.39%"><p id="zh-cn_topic_0182207110_p10801124132918"><a name="zh-cn_topic_0182207110_p10801124132918"></a><a name="zh-cn_topic_0182207110_p10801124132918"></a>设备的Cgroup权限，（r允许容器从指定的设备读取; w允许容器从指定的设备写入; m允许容器创建尚不存在的设备文件)</p>
    </td>
    </tr>
    </tbody>
    </table>

- <a name="zh-cn_topic_0182207110_li13021147134718"></a>**LinuxContainerConfig**

    包含特定于Linux平台的配置

    | **参数成员**                                   | **描述**                |
    |------------------------------------------------|-------------------------|
    | LinuxContainerResources resources              | 容器的资源规范          |
    | LinuxContainerSecurityContext security_context | 容器的Linux容器安全配置 |

- **ContainerConfig**

    包含用于创建容器的所有必需和可选字段

    | **参数成员**                    | **描述**                                                                                                                                             |
    |---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
    | ContainerMetadata metadata      | 容器的元数据。 此信息将唯一标识容器，运行时应利用此信息来确保正确操作。 运行时也可以使用此信息来提升UX（用户体检设计），例如通过构造可读名称。(必选) |
    | ImageSpec image                 | 容器使用的镜像 (**必选**)                                                                                                                                |
    | repeated string command         | 待执行的命令 **缺省值： "/bin/sh"**                                                                                                                      |
    | repeated string args            | 待执行命令的参数                                                                                                                                     |
    | string working_dir              | 命令执行的当前工作路径                                                                                                                               |
    | repeated KeyValue envs          | 在容器中配置的环境变量                                                                                                                               |
    | repeated Mount mounts           | 待在容器中挂载的挂载点信息                                                                                                                           |
    | repeated Device devices         | 待在容器中映射的设备信息                                                                                                                             |
    | map\<string, string> labels      | 可用于索引和选择单个资源的键值对。                                                                                                                   |
    | map\<string, string> annotations | 可用于存储和检索任意元数据的非结构化键值映射。                                                                                                       |
    | string log_path                 | 相对于PodSandboxConfig.LogDirectory的路径，用于存储容器主机上的日志（STDOUT和STDERR）。                                                              |
    | bool stdin                      | 是否打开容器的stdin                                                                                                                                  |
    | bool stdin_once                 | 当某次连接stdin的数据流断开时，是否立即断开其他与stdin连接的数据流 **（暂不支持）**                                                                       |
    | bool tty                        | 是否使用伪终端连接容器的stdio                                                                                                                        |
    | LinuxContainerConfig linux      | linux系统上容器的特定配置信息                                                                                                                        |

- **RuntimeConfig**

    Runtime的网络配置

    | **参数成员**                 | **描述**          |
    |------------------------------|-------------------|
    | NetworkConfig network_config | Runtime的网络配置 |

- **RuntimeCondition**

    描述runtime的状态信息

    <a name="zh-cn_topic_0182207110_table1149371711577"></a>
    <table><tbody><tr id="zh-cn_topic_0182207110_row549391719578"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p16493217155713"><a name="zh-cn_topic_0182207110_p16493217155713"></a><a name="zh-cn_topic_0182207110_p16493217155713"></a><strong id="zh-cn_topic_0182207110_b1949321720573"><a name="zh-cn_topic_0182207110_b1949321720573"></a><a name="zh-cn_topic_0182207110_b1949321720573"></a>参数成员</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p1749301713578"><a name="zh-cn_topic_0182207110_p1749301713578"></a><a name="zh-cn_topic_0182207110_p1749301713578"></a><strong id="zh-cn_topic_0182207110_b1749311765718"><a name="zh-cn_topic_0182207110_b1749311765718"></a><a name="zh-cn_topic_0182207110_b1749311765718"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row18493141795713"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p19493151765717"><a name="zh-cn_topic_0182207110_p19493151765717"></a><a name="zh-cn_topic_0182207110_p19493151765717"></a>string type</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p17493161719576"><a name="zh-cn_topic_0182207110_p17493161719576"></a><a name="zh-cn_topic_0182207110_p17493161719576"></a>Runtime状态的类型</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row767112245813"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1671426589"><a name="zh-cn_topic_0182207110_p1671426589"></a><a name="zh-cn_topic_0182207110_p1671426589"></a>bool status</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p13671328589"><a name="zh-cn_topic_0182207110_p13671328589"></a><a name="zh-cn_topic_0182207110_p13671328589"></a>Runtime状态</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row38518584"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p48417586"><a name="zh-cn_topic_0182207110_p48417586"></a><a name="zh-cn_topic_0182207110_p48417586"></a>string reason</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p16919175818"><a name="zh-cn_topic_0182207110_p16919175818"></a><a name="zh-cn_topic_0182207110_p16919175818"></a>简要描述runtime状态变化的原因</p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row12981958155716"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p19915581570"><a name="zh-cn_topic_0182207110_p19915581570"></a><a name="zh-cn_topic_0182207110_p19915581570"></a>string message</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p39995818579"><a name="zh-cn_topic_0182207110_p39995818579"></a><a name="zh-cn_topic_0182207110_p39995818579"></a>具备可阅读性的信息表明runtime状态变化的原因</p>
    </td>
    </tr>
    </tbody>
    </table>

- **RuntimeStatus**

    Runtime的状态

    <a name="zh-cn_topic_0182207110_table6258136145512"></a>
    <table><tbody><tr id="zh-cn_topic_0182207110_row1225814635519"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p1125820695515"><a name="zh-cn_topic_0182207110_p1125820695515"></a><a name="zh-cn_topic_0182207110_p1125820695515"></a><strong id="zh-cn_topic_0182207110_b925813645514"><a name="zh-cn_topic_0182207110_b925813645514"></a><a name="zh-cn_topic_0182207110_b925813645514"></a>参数成员</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p12587625511"><a name="zh-cn_topic_0182207110_p12587625511"></a><a name="zh-cn_topic_0182207110_p12587625511"></a><strong id="zh-cn_topic_0182207110_b13258186105511"><a name="zh-cn_topic_0182207110_b13258186105511"></a><a name="zh-cn_topic_0182207110_b13258186105511"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0182207110_row225811655518"><td class="cellrowborder" valign="top" width="41.06%"><p id="zh-cn_topic_0182207110_p102589635513"><a name="zh-cn_topic_0182207110_p102589635513"></a><a name="zh-cn_topic_0182207110_p102589635513"></a>repeated RuntimeCondition conditions</p>
    </td>
    <td class="cellrowborder" valign="top" width="58.940000000000005%"><p id="zh-cn_topic_0182207110_p32581661554"><a name="zh-cn_topic_0182207110_p32581661554"></a><a name="zh-cn_topic_0182207110_p32581661554"></a>描述当前runtime状态的列表</p>
    </td>
    </tr>
    </tbody>
    </table>

### Runtime服务

Runtime服务中包含操作pod和容器的接口，以及查询runtime自身配置和状态信息的接口。

#### RunPodSandbox

#### 接口原型

```text
rpc RunPodSandbox(RunPodSandboxRequest) returns (RunPodSandboxResponse) {}
```

#### 接口描述

创建和启动一个pod sandbox，若运行成功，sandbox处于ready状态。

#### 注意事项

1. 启动sandbox的默认镜像为rnd-dockerhub.huawei.com/library/pause-$\{machine\}:3.0， 其中$\{machine\}为架构，在x86\_64上，machine的值为amd64，在arm64上，machine的值为aarch64，当前rnd-dockerhub仓库上只有amd64和aarch64镜像可供下载，若机器上无此镜像，请确保机器能从rnd-dockerhub下载，若要使用其他镜像，请参考“iSulad部署配置”中的pod-sandbox-image指定镜像。
2. 由于容器命名以PodSandboxMetadata中的字段为来源，且以下划线"\_"为分割字符，因此限制metadata中的数据不能包含下划线，否则会出现sandbox运行成功，但无法使用ListPodSandbox接口查询的现象。

#### 参数

| **参数成员**            | **描述**                                                              |
|-------------------------|-----------------------------------------------------------------------|
| PodSandboxConfig config | sandbox的配置                                                         |
| string runtime_handler  | 指定创建sandbox的runtime运行时，当前支持lcr、kata-runtime运行时类型。 |

#### 返回值

<a name="zh-cn_topic_0183088020_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088020_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088020_p197485518319"><a name="zh-cn_topic_0183088020_p197485518319"></a><a name="zh-cn_topic_0183088020_p197485518319"></a><strong id="zh-cn_topic_0183088020_b77413551933"><a name="zh-cn_topic_0183088020_b77413551933"></a><a name="zh-cn_topic_0183088020_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088020_p374185520310"><a name="zh-cn_topic_0183088020_p374185520310"></a><a name="zh-cn_topic_0183088020_p374185520310"></a><strong id="zh-cn_topic_0183088020_b174125511315"><a name="zh-cn_topic_0183088020_b174125511315"></a><a name="zh-cn_topic_0183088020_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088020_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088020_p157445512318"><a name="zh-cn_topic_0183088020_p157445512318"></a><a name="zh-cn_topic_0183088020_p157445512318"></a>string pod_sandbox_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088020_p14745551137"><a name="zh-cn_topic_0183088020_p14745551137"></a><a name="zh-cn_topic_0183088020_p14745551137"></a>成功，返回response数据</p>
</td>
</tr>
</tbody>
</table>

#### StopPodSandbox

#### 接口原型

```text
rpc StopPodSandbox(StopPodSandboxRequest) returns (StopPodSandboxResponse) {}
```

#### 接口描述

停止pod sandbox，停止sandbox容器，回收分配给sandbox的网络资源（比如IP地址）。如果有任何running的容器属于该sandbox，则必须被强制停止。

#### 参数

<a name="zh-cn_topic_0183088041_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088041_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088041_p1089154617315"><a name="zh-cn_topic_0183088041_p1089154617315"></a><a name="zh-cn_topic_0183088041_p1089154617315"></a><strong id="zh-cn_topic_0183088041_b98915462314"><a name="zh-cn_topic_0183088041_b98915462314"></a><a name="zh-cn_topic_0183088041_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088041_p128984613319"><a name="zh-cn_topic_0183088041_p128984613319"></a><a name="zh-cn_topic_0183088041_p128984613319"></a><strong id="zh-cn_topic_0183088041_b989164612317"><a name="zh-cn_topic_0183088041_b989164612317"></a><a name="zh-cn_topic_0183088041_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088041_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088041_p1893714794317"><a name="zh-cn_topic_0183088041_p1893714794317"></a><a name="zh-cn_topic_0183088041_p1893714794317"></a>string pod_sandbox_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088041_p1189846434"><a name="zh-cn_topic_0183088041_p1189846434"></a><a name="zh-cn_topic_0183088041_p1189846434"></a>sandbox的id</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088041_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088041_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088041_p197485518319"><a name="zh-cn_topic_0183088041_p197485518319"></a><a name="zh-cn_topic_0183088041_p197485518319"></a><strong id="zh-cn_topic_0183088041_b77413551933"><a name="zh-cn_topic_0183088041_b77413551933"></a><a name="zh-cn_topic_0183088041_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088041_p374185520310"><a name="zh-cn_topic_0183088041_p374185520310"></a><a name="zh-cn_topic_0183088041_p374185520310"></a><strong id="zh-cn_topic_0183088041_b174125511315"><a name="zh-cn_topic_0183088041_b174125511315"></a><a name="zh-cn_topic_0183088041_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088041_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088041_p1772427114513"><a name="zh-cn_topic_0183088041_p1772427114513"></a><a name="zh-cn_topic_0183088041_p1772427114513"></a>无</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088041_p14745551137"><a name="zh-cn_topic_0183088041_p14745551137"></a><a name="zh-cn_topic_0183088041_p14745551137"></a>无</p>
</td>
</tr>
</tbody>
</table>

#### RemovePodSandbox

#### 接口原型

```text
rpc RemovePodSandbox(RemovePodSandboxRequest) returns (RemovePodSandboxResponse) {}
```

#### 接口描述

删除sandbox，如果有任何running的容器属于该sandbox，则必须被强制停止和删除，如果sandbox已经被删除，不能返回错误。

#### 注意事项

1. 删除sandbox时，不会删除sandbox的网络资源，在删除pod前必须先调用StopPodSandbox才能清理网络资源，调用者应当保证在删除sandbox之前至少调用一次StopPodSandbox。
2. 删除sandbox时，如果sandbox中的容器删除失败，则会出现sanbox被删除但容器还残留的情况，此时需要手动删除残留的容器进行清理。

#### 参数

<a name="zh-cn_topic_0183088042_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088042_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1089154617315"><a name="zh-cn_topic_0183088042_p1089154617315"></a><a name="zh-cn_topic_0183088042_p1089154617315"></a><strong id="zh-cn_topic_0183088042_b98915462314"><a name="zh-cn_topic_0183088042_b98915462314"></a><a name="zh-cn_topic_0183088042_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p128984613319"><a name="zh-cn_topic_0183088042_p128984613319"></a><a name="zh-cn_topic_0183088042_p128984613319"></a><strong id="zh-cn_topic_0183088042_b989164612317"><a name="zh-cn_topic_0183088042_b989164612317"></a><a name="zh-cn_topic_0183088042_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1893714794317"><a name="zh-cn_topic_0183088042_p1893714794317"></a><a name="zh-cn_topic_0183088042_p1893714794317"></a>string pod_sandbox_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p1189846434"><a name="zh-cn_topic_0183088042_p1189846434"></a><a name="zh-cn_topic_0183088042_p1189846434"></a>sandbox的id</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088042_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088042_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p197485518319"><a name="zh-cn_topic_0183088042_p197485518319"></a><a name="zh-cn_topic_0183088042_p197485518319"></a><strong id="zh-cn_topic_0183088042_b77413551933"><a name="zh-cn_topic_0183088042_b77413551933"></a><a name="zh-cn_topic_0183088042_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p374185520310"><a name="zh-cn_topic_0183088042_p374185520310"></a><a name="zh-cn_topic_0183088042_p374185520310"></a><strong id="zh-cn_topic_0183088042_b174125511315"><a name="zh-cn_topic_0183088042_b174125511315"></a><a name="zh-cn_topic_0183088042_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088042_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088042_p1772427114513"><a name="zh-cn_topic_0183088042_p1772427114513"></a><a name="zh-cn_topic_0183088042_p1772427114513"></a>无</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088042_p14745551137"><a name="zh-cn_topic_0183088042_p14745551137"></a><a name="zh-cn_topic_0183088042_p14745551137"></a>无</p>
</td>
</tr>
</tbody>
</table>

#### PodSandboxStatus

#### 接口原型

```text
rpc PodSandboxStatus(PodSandboxStatusRequest) returns (PodSandboxStatusResponse) {}
```

#### 接口描述

查询sandbox的状态，如果sandbox不存在，返回错误。

#### 参数

<a name="zh-cn_topic_0183088043_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088043_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088043_p1089154617315"><a name="zh-cn_topic_0183088043_p1089154617315"></a><a name="zh-cn_topic_0183088043_p1089154617315"></a><strong id="zh-cn_topic_0183088043_b98915462314"><a name="zh-cn_topic_0183088043_b98915462314"></a><a name="zh-cn_topic_0183088043_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088043_p128984613319"><a name="zh-cn_topic_0183088043_p128984613319"></a><a name="zh-cn_topic_0183088043_p128984613319"></a><strong id="zh-cn_topic_0183088043_b989164612317"><a name="zh-cn_topic_0183088043_b989164612317"></a><a name="zh-cn_topic_0183088043_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088043_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088043_p1893714794317"><a name="zh-cn_topic_0183088043_p1893714794317"></a><a name="zh-cn_topic_0183088043_p1893714794317"></a>string pod_sandbox_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088043_p1189846434"><a name="zh-cn_topic_0183088043_p1189846434"></a><a name="zh-cn_topic_0183088043_p1189846434"></a>sandbox的id</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088043_row1856117814815"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088043_p956148114812"><a name="zh-cn_topic_0183088043_p956148114812"></a><a name="zh-cn_topic_0183088043_p956148114812"></a>bool verbose</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088043_p155615864815"><a name="zh-cn_topic_0183088043_p155615864815"></a><a name="zh-cn_topic_0183088043_p155615864815"></a>标识是否显示sandbox的一些额外信息。（暂不支持配置）</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

| **返回值**               | **描述**                                                                                                                                 |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| PodSandboxStatus status  | sandbox的状态信息                                                                                                                        |
| map\<string, string> info | sandbox的额外信息，key是任意string，value是json格式的字符串，这些信息可以是任意调试内容。当verbose为true时info不能为空。（暂不支持配置） |

#### ListPodSandbox

#### 接口原型

```text
rpc ListPodSandbox(ListPodSandboxRequest) returns (ListPodSandboxResponse) {}
```

#### 接口描述

返回sandbox信息的列表，支持条件过滤。

#### 参数

| **参数成员**            | **描述**     |
|-------------------------|--------------|
| PodSandboxFilter filter | 条件过滤参数 |

#### 返回值

| **返回值**                | **描述**          |
|---------------------------|-------------------|
| repeated PodSandbox items | sandbox信息的列表 |

#### CreateContainer

#### 接口原型

```text
rpc CreateContainer(CreateContainerRequest) returns (CreateContainerResponse) {}
```

#### 接口描述

在PodSandbox内创建一个容器。

#### 注意事项

- 请求CreateContainerRequest 中的sandbox\_config与传递给RunPodSandboxRequest以创建PodSandbox的配置相同。 它再次传递，只是为了方便参考。 PodSandboxConfig是不可变的，在pod的整个生命周期内保持不变。
- 由于容器命名以ContainerMetadata中的字段为来源，且以下划线"\_"为分割字符，因此限制metadata中的数据不能包含下划线，否则会出现sandbox运行成功，但无法使用ListContainers接口查询的现象。
- CreateContainerRequest中无runtime\_handler字段，创建container时的runtime类型和其对应的sandbox的runtime相同。

#### 参数

| **参数成员**                    | **描述**                           |
|---------------------------------|------------------------------------|
| string pod_sandbox_id           | 待在其中创建容器的PodSandbox的ID。 |
| ContainerConfig config          | 容器的配置信息                     |
| PodSandboxConfig sandbox_config | PodSandbox的配置信息               |

#### 补充

可用于存储和检索任意元数据的非结构化键值映射。有一些字段由于cri接口没有提供特定的参数，可通过该字段将参数传入

- 自定义

    <a name="zh-cn_topic_0183088045_table18570435155317"></a>
    <table><tbody><tr id="zh-cn_topic_0183088045_row961273515313"><td class="cellrowborder" valign="top" width="50%"><p id="zh-cn_topic_0183088045_p146121535155310"><a name="zh-cn_topic_0183088045_p146121535155310"></a><a name="zh-cn_topic_0183088045_p146121535155310"></a><strong id="zh-cn_topic_0183088045_b83874913547"><a name="zh-cn_topic_0183088045_b83874913547"></a><a name="zh-cn_topic_0183088045_b83874913547"></a>自定义 key:value</strong></p>
    </td>
    <td class="cellrowborder" valign="top" width="50%"><p id="zh-cn_topic_0183088045_p1861233511533"><a name="zh-cn_topic_0183088045_p1861233511533"></a><a name="zh-cn_topic_0183088045_p1861233511533"></a><strong id="zh-cn_topic_0183088045_b461263545314"><a name="zh-cn_topic_0183088045_b461263545314"></a><a name="zh-cn_topic_0183088045_b461263545314"></a>描述</strong></p>
    </td>
    </tr>
    <tr id="zh-cn_topic_0183088045_row761273525315"><td class="cellrowborder" valign="top" width="50%"><p id="zh-cn_topic_0183088045_p221701745415"><a name="zh-cn_topic_0183088045_p221701745415"></a><a name="zh-cn_topic_0183088045_p221701745415"></a>cgroup.pids.max:int64_t</p>
    </td>
    <td class="cellrowborder" valign="top" width="50%"><p id="zh-cn_topic_0183088045_p1475318795514"><a name="zh-cn_topic_0183088045_p1475318795514"></a><a name="zh-cn_topic_0183088045_p1475318795514"></a>用于限制容器内的进/线程数（set -1 for unlimited）</p>
    </td>
    </tr>
    </tbody>
    </table>

#### 返回值

<a name="zh-cn_topic_0183088045_table1526093165012"></a>
<table><tbody><tr id="zh-cn_topic_0183088045_row926093115015"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088045_p14260143155018"><a name="zh-cn_topic_0183088045_p14260143155018"></a><a name="zh-cn_topic_0183088045_p14260143155018"></a><strong id="zh-cn_topic_0183088045_b10260153118509"><a name="zh-cn_topic_0183088045_b10260153118509"></a><a name="zh-cn_topic_0183088045_b10260153118509"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088045_p62602031155019"><a name="zh-cn_topic_0183088045_p62602031155019"></a><a name="zh-cn_topic_0183088045_p62602031155019"></a><strong id="zh-cn_topic_0183088045_b12601931165016"><a name="zh-cn_topic_0183088045_b12601931165016"></a><a name="zh-cn_topic_0183088045_b12601931165016"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088045_row326093175014"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088045_p3480192112404"><a name="zh-cn_topic_0183088045_p3480192112404"></a><a name="zh-cn_topic_0183088045_p3480192112404"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088045_p14745551137"><a name="zh-cn_topic_0183088045_p14745551137"></a><a name="zh-cn_topic_0183088045_p14745551137"></a>创建完成的容器ID</p>
</td>
</tr>
</tbody>
</table>

#### StartContainer

#### 接口原型

```text
rpc StartContainer(StartContainerRequest) returns (StartContainerResponse) {}
```

#### 接口描述

启动一个容器。

#### 参数

<a name="zh-cn_topic_0183088046_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088046_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088046_p1089154617315"><a name="zh-cn_topic_0183088046_p1089154617315"></a><a name="zh-cn_topic_0183088046_p1089154617315"></a><strong id="zh-cn_topic_0183088046_b98915462314"><a name="zh-cn_topic_0183088046_b98915462314"></a><a name="zh-cn_topic_0183088046_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088046_p128984613319"><a name="zh-cn_topic_0183088046_p128984613319"></a><a name="zh-cn_topic_0183088046_p128984613319"></a><strong id="zh-cn_topic_0183088046_b989164612317"><a name="zh-cn_topic_0183088046_b989164612317"></a><a name="zh-cn_topic_0183088046_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088046_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088046_p1019112316015"><a name="zh-cn_topic_0183088046_p1019112316015"></a><a name="zh-cn_topic_0183088046_p1019112316015"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088046_p1189846434"><a name="zh-cn_topic_0183088046_p1189846434"></a><a name="zh-cn_topic_0183088046_p1189846434"></a>容器id</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088046_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088046_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088046_p197485518319"><a name="zh-cn_topic_0183088046_p197485518319"></a><a name="zh-cn_topic_0183088046_p197485518319"></a><strong id="zh-cn_topic_0183088046_b77413551933"><a name="zh-cn_topic_0183088046_b77413551933"></a><a name="zh-cn_topic_0183088046_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088046_p374185520310"><a name="zh-cn_topic_0183088046_p374185520310"></a><a name="zh-cn_topic_0183088046_p374185520310"></a><strong id="zh-cn_topic_0183088046_b174125511315"><a name="zh-cn_topic_0183088046_b174125511315"></a><a name="zh-cn_topic_0183088046_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088046_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088046_p554418192002"><a name="zh-cn_topic_0183088046_p554418192002"></a><a name="zh-cn_topic_0183088046_p554418192002"></a>无</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088046_p4543101912019"><a name="zh-cn_topic_0183088046_p4543101912019"></a><a name="zh-cn_topic_0183088046_p4543101912019"></a>无</p>
</td>
</tr>
</tbody>
</table>

#### StopContainer

#### 接口原型

```text
rpc StopContainer(StopContainerRequest) returns (StopContainerResponse) {}
```

#### 接口描述

停止一个running的容器，支持配置优雅停止时间timeout，如果容器已经停止，不能返回错误。

#### 参数

<a name="zh-cn_topic_0183088047_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088047_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088047_p1089154617315"><a name="zh-cn_topic_0183088047_p1089154617315"></a><a name="zh-cn_topic_0183088047_p1089154617315"></a><strong id="zh-cn_topic_0183088047_b98915462314"><a name="zh-cn_topic_0183088047_b98915462314"></a><a name="zh-cn_topic_0183088047_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088047_p128984613319"><a name="zh-cn_topic_0183088047_p128984613319"></a><a name="zh-cn_topic_0183088047_p128984613319"></a><strong id="zh-cn_topic_0183088047_b989164612317"><a name="zh-cn_topic_0183088047_b989164612317"></a><a name="zh-cn_topic_0183088047_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088047_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088047_p1019112316015"><a name="zh-cn_topic_0183088047_p1019112316015"></a><a name="zh-cn_topic_0183088047_p1019112316015"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088047_p1189846434"><a name="zh-cn_topic_0183088047_p1189846434"></a><a name="zh-cn_topic_0183088047_p1189846434"></a>容器id</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088047_row660924815015"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088047_p06097481802"><a name="zh-cn_topic_0183088047_p06097481802"></a><a name="zh-cn_topic_0183088047_p06097481802"></a>int64 timeout</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088047_p360920481009"><a name="zh-cn_topic_0183088047_p360920481009"></a><a name="zh-cn_topic_0183088047_p360920481009"></a>强制停止容器前的等待时间，缺省值为0，即强制停止容器。</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

无

#### RemoveContainer

#### 接口原型

```text
rpc RemoveContainer(RemoveContainerRequest) returns (RemoveContainerResponse) {}
```

#### 接口描述

删除一个容器，如果容器正在运行，必须强制停止，如果容器已经被删除，不能返回错误。

#### 参数

<a name="zh-cn_topic_0183088048_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088048_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088048_p1089154617315"><a name="zh-cn_topic_0183088048_p1089154617315"></a><a name="zh-cn_topic_0183088048_p1089154617315"></a><strong id="zh-cn_topic_0183088048_b98915462314"><a name="zh-cn_topic_0183088048_b98915462314"></a><a name="zh-cn_topic_0183088048_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088048_p128984613319"><a name="zh-cn_topic_0183088048_p128984613319"></a><a name="zh-cn_topic_0183088048_p128984613319"></a><strong id="zh-cn_topic_0183088048_b989164612317"><a name="zh-cn_topic_0183088048_b989164612317"></a><a name="zh-cn_topic_0183088048_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088048_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088048_p1019112316015"><a name="zh-cn_topic_0183088048_p1019112316015"></a><a name="zh-cn_topic_0183088048_p1019112316015"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088048_p1189846434"><a name="zh-cn_topic_0183088048_p1189846434"></a><a name="zh-cn_topic_0183088048_p1189846434"></a>容器id</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

无

#### ListContainers

#### 接口原型

```text
rpc ListContainers(ListContainersRequest) returns (ListContainersResponse) {}
```

#### 接口描述

返回container信息的列表，支持条件过滤。

#### 参数

| **参数成员**           | **描述**     |
|------------------------|--------------|
| ContainerFilter filter | 条件过滤参数 |

#### 返回值

| **返回值**                    | **描述**       |
|-------------------------------|----------------|
| repeated Container containers | 容器信息的列表 |

#### ContainerStatus

#### 接口原型

```text
rpc ContainerStatus(ContainerStatusRequest) returns (ContainerStatusResponse) {}
```

#### 接口描述

返回容器状态信息，如果容器不存在，则返回错误。

#### 参数

<a name="zh-cn_topic_0183088050_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088050_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088050_p1089154617315"><a name="zh-cn_topic_0183088050_p1089154617315"></a><a name="zh-cn_topic_0183088050_p1089154617315"></a><strong id="zh-cn_topic_0183088050_b98915462314"><a name="zh-cn_topic_0183088050_b98915462314"></a><a name="zh-cn_topic_0183088050_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088050_p128984613319"><a name="zh-cn_topic_0183088050_p128984613319"></a><a name="zh-cn_topic_0183088050_p128984613319"></a><strong id="zh-cn_topic_0183088050_b989164612317"><a name="zh-cn_topic_0183088050_b989164612317"></a><a name="zh-cn_topic_0183088050_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088050_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088050_p1019112316015"><a name="zh-cn_topic_0183088050_p1019112316015"></a><a name="zh-cn_topic_0183088050_p1019112316015"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088050_p1189846434"><a name="zh-cn_topic_0183088050_p1189846434"></a><a name="zh-cn_topic_0183088050_p1189846434"></a>容器id</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088050_row134851364619"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088050_p956148114812"><a name="zh-cn_topic_0183088050_p956148114812"></a><a name="zh-cn_topic_0183088050_p956148114812"></a>bool verbose</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088050_p155615864815"><a name="zh-cn_topic_0183088050_p155615864815"></a><a name="zh-cn_topic_0183088050_p155615864815"></a>标识是否显示sandbox的一些额外信息。（暂不支持配置）</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

| **返回值**               | **描述**                                                                                                                                 |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| ContainerStatus status   | 容器的状态信息                                                                                                                           |
| map\<string, string> info | sandbox的额外信息，key是任意string，value是json格式的字符串，这些信息可以是任意调试内容。当verbose为true时info不能为空。（暂不支持配置） |

#### UpdateContainerResources

#### 接口原型

```text
rpc UpdateContainerResources(UpdateContainerResourcesRequest) returns (UpdateContainerResourcesResponse) {}
```

#### 接口描述

该接口用于更新容器资源配置。

#### 注意事项

- 该接口仅用于更新容器的资源配置，不能用于更新Pod的资源配置。
- 当前不支持更新容器oom\_score\_adj配置。

#### 参数

| **参数成员**                  | **描述**          |
|-------------------------------|-------------------|
| string container_id           | 容器id            |
| LinuxContainerResources linux | linux资源配置信息 |

#### 返回值

无

#### ExecSync

#### 接口原型

```text
rpc ExecSync(ExecSyncRequest) returns (ExecSyncResponse) {}
```

#### 接口描述

以同步的方式在容器中执行命令，采用的gRPC通讯方式。

#### 注意事项

执行一条单独的命令，不能打开终端与容器交互。

#### 参数

<a name="zh-cn_topic_0183088052_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088052_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p1089154617315"><a name="zh-cn_topic_0183088052_p1089154617315"></a><a name="zh-cn_topic_0183088052_p1089154617315"></a><strong id="zh-cn_topic_0183088052_b98915462314"><a name="zh-cn_topic_0183088052_b98915462314"></a><a name="zh-cn_topic_0183088052_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p128984613319"><a name="zh-cn_topic_0183088052_p128984613319"></a><a name="zh-cn_topic_0183088052_p128984613319"></a><strong id="zh-cn_topic_0183088052_b989164612317"><a name="zh-cn_topic_0183088052_b989164612317"></a><a name="zh-cn_topic_0183088052_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p293511573266"><a name="zh-cn_topic_0183088052_p293511573266"></a><a name="zh-cn_topic_0183088052_p293511573266"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p1189846434"><a name="zh-cn_topic_0183088052_p1189846434"></a><a name="zh-cn_topic_0183088052_p1189846434"></a>容器ID</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row17894468314"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p1489111122411"><a name="zh-cn_topic_0183088052_p1489111122411"></a><a name="zh-cn_topic_0183088052_p1489111122411"></a>repeated string cmd</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p780820166266"><a name="zh-cn_topic_0183088052_p780820166266"></a><a name="zh-cn_topic_0183088052_p780820166266"></a>待执行命令</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row4812119101610"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p24734935614"><a name="zh-cn_topic_0183088052_p24734935614"></a><a name="zh-cn_topic_0183088052_p24734935614"></a>int64 timeout</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p6510957162719"><a name="zh-cn_topic_0183088052_p6510957162719"></a><a name="zh-cn_topic_0183088052_p6510957162719"></a>停止命令的超时时间（秒）。 缺省值：0（无超时限制）。 <strong id="zh-cn_topic_0183088052_b921123104014"><a name="zh-cn_topic_0183088052_b921123104014"></a><a name="zh-cn_topic_0183088052_b921123104014"></a>暂不支持</strong></p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088052_table1244111592419"></a>
<table><tbody><tr id="zh-cn_topic_0183088052_row844114513243"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p244117515249"><a name="zh-cn_topic_0183088052_p244117515249"></a><a name="zh-cn_topic_0183088052_p244117515249"></a><strong id="zh-cn_topic_0183088052_b1044111592411"><a name="zh-cn_topic_0183088052_b1044111592411"></a><a name="zh-cn_topic_0183088052_b1044111592411"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p10441155152411"><a name="zh-cn_topic_0183088052_p10441155152411"></a><a name="zh-cn_topic_0183088052_p10441155152411"></a><strong id="zh-cn_topic_0183088052_b1944120532419"><a name="zh-cn_topic_0183088052_b1944120532419"></a><a name="zh-cn_topic_0183088052_b1944120532419"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row17442659244"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p44421057247"><a name="zh-cn_topic_0183088052_p44421057247"></a><a name="zh-cn_topic_0183088052_p44421057247"></a>bytes stdout</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p14442857248"><a name="zh-cn_topic_0183088052_p14442857248"></a><a name="zh-cn_topic_0183088052_p14442857248"></a>捕获命令标准输出</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row444214512412"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p19834172715201"><a name="zh-cn_topic_0183088052_p19834172715201"></a><a name="zh-cn_topic_0183088052_p19834172715201"></a>bytes stderr</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p18188336182011"><a name="zh-cn_topic_0183088052_p18188336182011"></a><a name="zh-cn_topic_0183088052_p18188336182011"></a>捕获命令标准错误输出</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088052_row16951195032014"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088052_p1195135062019"><a name="zh-cn_topic_0183088052_p1195135062019"></a><a name="zh-cn_topic_0183088052_p1195135062019"></a>int32 exit_code</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088052_p987318251219"><a name="zh-cn_topic_0183088052_p987318251219"></a><a name="zh-cn_topic_0183088052_p987318251219"></a>退出代码命令完成。 缺省值：0（成功）。</p>
</td>
</tr>
</tbody>
</table>

#### Exec

#### 接口原型

```text
rpc Exec(ExecRequest) returns (ExecResponse) {}
```

#### 接口描述

在容器中执行命令，采用的gRPC通讯方式从CRI服务端获取url，再通过获得的url与websocket服务端建立长连接，实现与容器的交互。

#### 注意事项

执行一条单独的命令，也能打开终端与容器交互。stdin/stdout/stderr之一必须是真的。如果tty为真，stderr必须是假的。 不支持多路复用,  在这种情况下, stdout和stderr的输出将合并为单流。

#### 参数

<a name="zh-cn_topic_0183088053_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088053_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p1089154617315"><a name="zh-cn_topic_0183088053_p1089154617315"></a><a name="zh-cn_topic_0183088053_p1089154617315"></a><strong id="zh-cn_topic_0183088053_b98915462314"><a name="zh-cn_topic_0183088053_b98915462314"></a><a name="zh-cn_topic_0183088053_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p128984613319"><a name="zh-cn_topic_0183088053_p128984613319"></a><a name="zh-cn_topic_0183088053_p128984613319"></a><strong id="zh-cn_topic_0183088053_b989164612317"><a name="zh-cn_topic_0183088053_b989164612317"></a><a name="zh-cn_topic_0183088053_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p1253351115517"><a name="zh-cn_topic_0183088053_p1253351115517"></a><a name="zh-cn_topic_0183088053_p1253351115517"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p1189846434"><a name="zh-cn_topic_0183088053_p1189846434"></a><a name="zh-cn_topic_0183088053_p1189846434"></a>容器ID</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row17894468314"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p1489111122411"><a name="zh-cn_topic_0183088053_p1489111122411"></a><a name="zh-cn_topic_0183088053_p1489111122411"></a>repeated string cmd</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p780820166266"><a name="zh-cn_topic_0183088053_p780820166266"></a><a name="zh-cn_topic_0183088053_p780820166266"></a>待执行的命令</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row4812119101610"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p3218304144"><a name="zh-cn_topic_0183088053_p3218304144"></a><a name="zh-cn_topic_0183088053_p3218304144"></a>bool tty</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p1947314925616"><a name="zh-cn_topic_0183088053_p1947314925616"></a><a name="zh-cn_topic_0183088053_p1947314925616"></a>是否在TTY中执行命令</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row1569883411415"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p06982346147"><a name="zh-cn_topic_0183088053_p06982346147"></a><a name="zh-cn_topic_0183088053_p06982346147"></a>bool stdin</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p469919340142"><a name="zh-cn_topic_0183088053_p469919340142"></a><a name="zh-cn_topic_0183088053_p469919340142"></a>是否流式标准输入</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row12135742161414"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p5135242161417"><a name="zh-cn_topic_0183088053_p5135242161417"></a><a name="zh-cn_topic_0183088053_p5135242161417"></a>bool stdout</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p1613584220142"><a name="zh-cn_topic_0183088053_p1613584220142"></a><a name="zh-cn_topic_0183088053_p1613584220142"></a>是否流式标准输出</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row101281154171413"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p151281754181412"><a name="zh-cn_topic_0183088053_p151281754181412"></a><a name="zh-cn_topic_0183088053_p151281754181412"></a>bool stderr</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p51282542141"><a name="zh-cn_topic_0183088053_p51282542141"></a><a name="zh-cn_topic_0183088053_p51282542141"></a>是否流式输出标准错误</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088053_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088053_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p197485518319"><a name="zh-cn_topic_0183088053_p197485518319"></a><a name="zh-cn_topic_0183088053_p197485518319"></a><strong id="zh-cn_topic_0183088053_b77413551933"><a name="zh-cn_topic_0183088053_b77413551933"></a><a name="zh-cn_topic_0183088053_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p374185520310"><a name="zh-cn_topic_0183088053_p374185520310"></a><a name="zh-cn_topic_0183088053_p374185520310"></a><strong id="zh-cn_topic_0183088053_b174125511315"><a name="zh-cn_topic_0183088053_b174125511315"></a><a name="zh-cn_topic_0183088053_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p15574205011242"><a name="zh-cn_topic_0183088053_p15574205011242"></a><a name="zh-cn_topic_0183088053_p15574205011242"></a>string url</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p103555206255"><a name="zh-cn_topic_0183088053_p103555206255"></a><a name="zh-cn_topic_0183088053_p103555206255"></a>exec流服务器的完全限定URL</p>
</td>
</tr>
</tbody>
</table>

#### Attach

#### 接口原型

```text
rpc Attach(AttachRequest) returns (AttachResponse) {}
```

#### 接口描述

接管容器的1号进程，采用gRPC通讯方式从CRI服务端获取url，再通过获取的url与websocket服务端建立长连接，实现与容器的交互。

#### 参数

<a name="zh-cn_topic_0183088056_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088056_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p1089154617315"><a name="zh-cn_topic_0183088056_p1089154617315"></a><a name="zh-cn_topic_0183088056_p1089154617315"></a><strong id="zh-cn_topic_0183088056_b98915462314"><a name="zh-cn_topic_0183088056_b98915462314"></a><a name="zh-cn_topic_0183088056_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p128984613319"><a name="zh-cn_topic_0183088056_p128984613319"></a><a name="zh-cn_topic_0183088056_p128984613319"></a><strong id="zh-cn_topic_0183088056_b989164612317"><a name="zh-cn_topic_0183088056_b989164612317"></a><a name="zh-cn_topic_0183088056_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>容器id</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>bool tty</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>是否在TTY中执行命令</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>bool stdin</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>是否流式标准输入</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>bool stdout</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>是否流式标准输出</p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>bool stderr</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>是否流式标准错误</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

<a name="zh-cn_topic_0183088053_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088053_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p197485518319"><a name="zh-cn_topic_0183088053_p197485518319"></a><a name="zh-cn_topic_0183088053_p197485518319"></a><strong id="zh-cn_topic_0183088053_b77413551933"><a name="zh-cn_topic_0183088053_b77413551933"></a><a name="zh-cn_topic_0183088053_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p374185520310"><a name="zh-cn_topic_0183088053_p374185520310"></a><a name="zh-cn_topic_0183088053_p374185520310"></a><strong id="zh-cn_topic_0183088053_b174125511315"><a name="zh-cn_topic_0183088053_b174125511315"></a><a name="zh-cn_topic_0183088053_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088053_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088053_p15574205011242"><a name="zh-cn_topic_0183088053_p15574205011242"></a><a name="zh-cn_topic_0183088053_p15574205011242"></a>string url</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088053_p103555206255"><a name="zh-cn_topic_0183088053_p103555206255"></a><a name="zh-cn_topic_0183088053_p103555206255"></a>attach流服务器的完全限定URL</p>
</td>
</tr>
</tbody>
</table>

#### ContainerStats

#### 接口原型

```text
rpc ContainerStats(ContainerStatsRequest) returns (ContainerStatsResponse) {}
```

#### 接口描述

返回单个容器占用资源信息，仅支持runtime类型为lcr的容器。

#### 参数

<a name="zh-cn_topic_0183088056_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088056_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p1089154617315"><a name="zh-cn_topic_0183088056_p1089154617315"></a><a name="zh-cn_topic_0183088056_p1089154617315"></a><strong id="zh-cn_topic_0183088056_b98915462314"><a name="zh-cn_topic_0183088056_b98915462314"></a><a name="zh-cn_topic_0183088056_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p128984613319"><a name="zh-cn_topic_0183088056_p128984613319"></a><a name="zh-cn_topic_0183088056_p128984613319"></a><strong id="zh-cn_topic_0183088056_b989164612317"><a name="zh-cn_topic_0183088056_b989164612317"></a><a name="zh-cn_topic_0183088056_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088056_row10898461533"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088056_p759712497119"><a name="zh-cn_topic_0183088056_p759712497119"></a><a name="zh-cn_topic_0183088056_p759712497119"></a>string container_id</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088056_p1189846434"><a name="zh-cn_topic_0183088056_p1189846434"></a><a name="zh-cn_topic_0183088056_p1189846434"></a>容器id</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

| **返回值**           | **描述**                                                |
|----------------------|---------------------------------------------------------|
| ContainerStats stats | 容器信息。<br>注：disk和inodes只支持oci格式镜像起的容器查询 |

#### ListContainerStats

#### 接口原型

```text
rpc ListContainerStats(ListContainerStatsRequest) returns (ListContainerStatsResponse) {}
```

#### 接口描述

返回多个容器占用资源信息，支持条件过滤

#### 参数

| **参数成员**                | **描述**     |
|-----------------------------|--------------|
| ContainerStatsFilter filter | 条件过滤参数 |

#### 返回值

| **返回值**                    | **描述**                                                        |
|-------------------------------|-----------------------------------------------------------------|
| repeated ContainerStats stats | 容器信息的列表。注：disk和inodes只支持oci格式镜像启动的容器查询 |

#### UpdateRuntimeConfig

#### 接口原型

```text
rpc UpdateRuntimeConfig(UpdateRuntimeConfigRequest) returns (UpdateRuntimeConfigResponse);
```

#### 接口描述

提供标准的CRI接口，目的为了更新网络插件的Pod CIDR，当前CNI网络插件无需更新Pod CIDR，因此该接口只会记录访问日志。

#### 注意事项

接口操作不会对系统管理信息修改，只是记录一条日志。

#### 参数

| **参数成员**                 | **描述**                |
|------------------------------|-------------------------|
| RuntimeConfig runtime_config | 包含Runtime要配置的信息 |

#### 返回值

无

#### Status

#### 接口原型

```text
rpc Status(StatusRequest) returns (StatusResponse) {};
```

#### 接口描述

获取runtime和pod的网络状态，在获取网络状态时，会触发网络配置的刷新。

#### 注意事项

如果网络配置刷新失败，不会影响原有配置；只有刷新成功时，才会覆盖原有配置。

#### 参数

<a name="zh-cn_topic_0183088059_table184320467318"></a>
<table><tbody><tr id="zh-cn_topic_0183088059_row78917461336"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088059_p1089154617315"><a name="zh-cn_topic_0183088059_p1089154617315"></a><a name="zh-cn_topic_0183088059_p1089154617315"></a><strong id="zh-cn_topic_0183088059_b98915462314"><a name="zh-cn_topic_0183088059_b98915462314"></a><a name="zh-cn_topic_0183088059_b98915462314"></a>参数成员</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088059_p128984613319"><a name="zh-cn_topic_0183088059_p128984613319"></a><a name="zh-cn_topic_0183088059_p128984613319"></a><strong id="zh-cn_topic_0183088059_b989164612317"><a name="zh-cn_topic_0183088059_b989164612317"></a><a name="zh-cn_topic_0183088059_b989164612317"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088059_row17894468314"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088059_p133821342185014"><a name="zh-cn_topic_0183088059_p133821342185014"></a><a name="zh-cn_topic_0183088059_p133821342185014"></a>bool verbose</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088059_p5596114510551"><a name="zh-cn_topic_0183088059_p5596114510551"></a><a name="zh-cn_topic_0183088059_p5596114510551"></a>是否显示关于Runtime额外的信息（暂不支持）</p>
</td>
</tr>
</tbody>
</table>

#### 返回值

| **返回值**               | **描述**                                                                                                    |
|--------------------------|-------------------------------------------------------------------------------------------------------------|
| RuntimeStatus status     | Runtime的状态                                                                                               |
| map\<string, string> info | Runtime额外的信息，info的key为任意值，value为json格式，可包含任何debug信息；只有Verbose为true是才应该被赋值 |

### Image服务

提供了从镜像仓库拉取、查看、和移除镜像的gRPC API。

#### ListImages

#### 接口原型

```text
rpc ListImages(ListImagesRequest) returns (ListImagesResponse) {}
```

#### 接口描述

列出当前已存在的镜像信息。

#### 注意事项

为统一接口，对于embedded格式镜像，可以通过cri images查询到。但是因embedded镜像不是标准OCI镜像，因此查询得到的结果有以下限制：

- 因embedded镜像无镜像ID，显示的镜像ID为镜像的config digest。
- 因embedded镜像本身无digest仅有config的digest，且格式不符合OCI镜像规范，因此无法显示digest。

#### 参数

| **参数成员**     | **描述**       |
|------------------|----------------|
| ImageSpec filter | 筛选的镜像名称 |

#### 返回值

| **返回值**            | **描述**     |
|-----------------------|--------------|
| repeated Image images | 镜像信息列表 |

#### ImageStatus

#### 接口原型

```text
rpc ImageStatus(ImageStatusRequest) returns (ImageStatusResponse) {}
```

#### 接口描述

查询指定镜像信息。

#### 注意事项

1. 查询指定镜像信息，若镜像不存在，则返回ImageStatusResponse，其中Image设置为nil。
2. 为统一接口，对于embedded格式镜像，因不符合OCI格式镜像，缺少字段，无法通过本接口进行查询。

#### 参数

| **参数成员**    | **描述**                               |
|-----------------|----------------------------------------|
| ImageSpec image | 镜像名称                               |
| bool verbose    | 查询额外信息，暂不支持，无额外信息返回 |

#### 返回值

| **返回值**               | **描述**                               |
|--------------------------|----------------------------------------|
| Image image              | 镜像信息                               |
| map\<string, string> info | 镜像额外信息，暂不支持，无额外信息返回 |

#### PullImage

#### 接口原型

```text
 rpc PullImage(PullImageRequest) returns (PullImageResponse) {}
```

#### 接口描述

下载镜像。

#### 注意事项

当前支持下载public镜像，使用用户名、密码、auth信息下载私有镜像，不支持authconfig中的server\_address、identity\_token、registry\_token字段。

#### 参数

| **参数成员**                    | **描述**                          |
|---------------------------------|-----------------------------------|
| ImageSpec image                 | 要下载的镜像名称                  |
| AuthConfig auth                 | 下载私有镜像时的验证信息          |
| PodSandboxConfig sandbox_config | 在Pod上下文中下载镜像（暂不支持） |

#### 返回值

<a name="zh-cn_topic_0183088062_table15296551936"></a>
<table><tbody><tr id="zh-cn_topic_0183088062_row18741555834"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088062_p197485518319"><a name="zh-cn_topic_0183088062_p197485518319"></a><a name="zh-cn_topic_0183088062_p197485518319"></a><strong id="zh-cn_topic_0183088062_b77413551933"><a name="zh-cn_topic_0183088062_b77413551933"></a><a name="zh-cn_topic_0183088062_b77413551933"></a>返回值</strong></p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088062_p374185520310"><a name="zh-cn_topic_0183088062_p374185520310"></a><a name="zh-cn_topic_0183088062_p374185520310"></a><strong id="zh-cn_topic_0183088062_b174125511315"><a name="zh-cn_topic_0183088062_b174125511315"></a><a name="zh-cn_topic_0183088062_b174125511315"></a>描述</strong></p>
</td>
</tr>
<tr id="zh-cn_topic_0183088062_row87419551317"><td class="cellrowborder" valign="top" width="39.54%"><p id="zh-cn_topic_0183088062_p157445512318"><a name="zh-cn_topic_0183088062_p157445512318"></a><a name="zh-cn_topic_0183088062_p157445512318"></a>string image_ref</p>
</td>
<td class="cellrowborder" valign="top" width="60.46%"><p id="zh-cn_topic_0183088062_p14745551137"><a name="zh-cn_topic_0183088062_p14745551137"></a><a name="zh-cn_topic_0183088062_p14745551137"></a>返回已下载镜像信息</p>
</td>
</tr>
</tbody>
</table>

#### RemoveImage

#### 接口原型

```text
rpc RemoveImage(RemoveImageRequest) returns (RemoveImageResponse) {}
```

#### 接口描述

删除指定镜像。

#### 注意事项

为统一接口，对于embedded格式镜像，因不符合OCI格式镜像，缺少字段，无法通过本接口使用image id进行删除。

#### 参数

| **参数成员**    | **描述**               |
|-----------------|------------------------|
| ImageSpec image | 要删除的镜像名称或者ID |

#### 返回值

无

#### ImageFsInfo

#### 接口原型

```text
rpc ImageFsInfo(ImageFsInfoRequest) returns (ImageFsInfoResponse) {}
```

#### 接口描述

查询存储镜像的文件系统信息。

#### 注意事项

查询到的为镜像元数据下的文件系统信息。

#### 参数

无

#### 返回值

| **返回值**                                 | **描述**             |
|--------------------------------------------|----------------------|
| repeated FilesystemUsage image_filesystems | 镜像存储文件系统信息 |

### 约束

1. 如果创建sandbox时，PodSandboxConfig参数中配置了log\_directory，则所有属于该sandbox的container在创建时必须在ContainerConfig中指定log\_path，否则可能导致容器无法使用CRI接口启动，甚至无法使用CRI接口删除。

    容器的真实LOGPATH=log\_directory/log\_path，如果log\_path不配置，那么最终的LOGPATH会变为LOGPATH=log\_directory。

    - 如果该路径不存在，isulad在启动容器时会创建一个软链接，指向最终的容器日志真实路径，此时log\_directory变成一个软链接，此时有两种情况：
        1. 第一种情况，如果该sandbox里其他容器也没配置log\_path，在启动其他容器时，log\_directory会被删除，然后重新指向新启动容器的log\_path，导致之前启动的容器日志指向后面启动容器的日志。
        2. 第二种情况，如果该sandbox里其他容器配置了log\_path，则该容器的LOGPATH=log\_directory/log\_path，由于log\_directory实际是个软链接，使用log\_directory/log\_path为软链接指向容器真实日志路径时，创建会失败。

    - 如果该路径存在，isulad在启动容器时首先会尝试删除该路径（非递归），如果该路径是个文件夹，且里面有内容，删除会失败，从而导致创建软链接失败，容器启动失败，删除该容器时，也会出现同样的现象，导致删除失败。

2. 如果创建sandbox时，PodSandboxConfig参数中配置了log\_directory，且container创建时在ContainerConfig中指定log\_path，那么最终的LOGPATH=log\_directory/log\_path，isulad不会递归的创建LOGPATH，因而用户必须保证dirname\(LOGPATH\)存在，即最终的日志文件的上一级路径存在。
3. 如果创建sandbox时，PodSandboxConfig参数中配置了log\_directory，如果有两个或多个container创建时在ContainerConfig中指定了同一个log\_path，或者不同的sandbox内的容器最终指向的LOGPATH是同一路径，若容器启动成功，则后启动的容器日志路径会覆盖掉之前启动的容器日志路径。
4. 如果远程镜像仓库中镜像内容发生变化，调用CRI Pull image接口重新下载该镜像时，若本地原来存储有原镜像，则原镜像的镜像名称、TAG会变更为“none”

    举例如下：

    本地已存储镜像：

    ```text
    IMAGE                                        TAG                 IMAGE ID            SIZE
    rnd-dockerhub.huawei.com/pproxyisulad/test   latest              99e59f495ffaa       753kB
    ```

    远程仓库中rnd-dockerhub.huawei.com/pproxyisulad/test:latest 镜像更新后，重新下载后：

    ```text
    IMAGE                                        TAG                 IMAGE ID            SIZE
    <none>                                       <none>              99e59f495ffaa       753kB
    rnd-dockerhub.huawei.com/pproxyisulad/test   latest              d8233ab899d41       1.42MB
    ```

    使用isula images 命令行查询，REF显示为"-"：

    ```text
    REF                                               IMAGE ID               CREATED              SIZE       
    rnd-dockerhub.huawei.com/pproxyisulad/test:latest d8233ab899d41          2019-02-14 19:19:37  1.42MB     
    -                                                 99e59f495ffaa          2016-05-04 02:26:41  753kB
    ```

5. iSulad CRI exec/attach接口采用websocket协议实现，需要采用同样协议的客户端与iSulad进行交互；使用exec/attach接口时，请避免进行串口大量数据及文件的传输，仅用于基本命令交互，若用户侧处理不及时将存在数据丢失的风险；同时请勿使用cri exec/attach接口进行二进制数据及文件传输。
6. iSulad CRI exec/attach流式接口依赖libwebsockets实现，流式接口建议仅用于长连接交互使用，不建议在大并发场景下使用，可能会因为宿主机资源不足导致连接失败，建议并发量不超过100。
