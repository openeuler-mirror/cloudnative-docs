# 安装与部署

## 软件要求

* 操作系统：openEuler 24.03 LTS SP1

## 硬件要求

* x86_64架构

## 环境准备

* 安装openEuler系统，安装方法参考 《[安装指南](https://docs.openeuler.org/zh/docs/24.03_LTS_SP2/server/installation_upgrade/installation/installation-on-servers.html)》。
* 安装Kmesh需要使用root权限。

## 安装Kmesh

* 安装Kmesh软件包，参考命令如下：

```shell
[root@openEuler ~]# yum install Kmesh
```

* 查看安装是否成功，参考命令如下，若回显有对应软件包，表示安装成功：

```shell
[root@openEuler ~]# rpm -q Kmesh
```

## 部署Kmesh

### 集群启动模式

启动前，先进行配置修改，设置集群中控制面程序ip信息（如istiod ip地址），操作如下：

```json
    "clusters": [
      {
        "name": "xds-grpc",
        "type" : "STATIC",
        "connect_timeout": "1s",
        "lb_policy": "ROUND_ROBIN",
        "load_assignment": {
          "cluster_name": "xds-grpc",
          "endpoints": [{
            "lb_endpoints": [{
              "endpoint": {
                "address":{
                  "socket_address": {
                          "protocol": "TCP",
                          "address": "192.168.0.1",# 设置控制面ip(如istiod ip)
                          "port_value": 15010
                     }
                }
              }
            }]
          }]
```

当前集群启动模式下仅支持Kmesh流量编排功能。

### 本地启动模式

启动前，修改kmesh.service，选择需要使用的功能选项。

使用流量编排功能，操作如下：

```shell
# 选择-enable-kmesh，禁用ads开关
[root@openEuler ~]# vim /usr/lib/systemd/system/kmesh.service
ExecStart=/usr/bin/kmesh-daemon -enable-kmesh -enable-ads=false
[root@openEuler ~]# systemctl daemon-reload
```

使用网格加速功能，操作如下：

```shell
# 选择-enable-mda选项，禁用ads开关
[root@openEuler ~]# vim /usr/lib/systemd/system/kmesh.service
ExecStart=/usr/bin/kmesh-daemon -enable-mda -enable-ads=false
[root@openEuler ~]# systemctl daemon-reload
```

Kmesh服务启动时会调用kmesh-daemon程序，具体使用方式可以参考[kmesh-daemon使用](./usage.md)。

### 启动Kmesh

```shell
# 启动Kmesh服务
[root@openEuler ~]# systemctl start kmesh.service
# 查看Kmesh运行状态
[root@openEuler ~]# systemctl status kmesh.service
```

### 停止Kmesh

```shell
# 停止Kmesh服务
[root@openEuler ~]# systemctl stop kmesh.service
```
