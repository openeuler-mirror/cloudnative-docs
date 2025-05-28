# 附录

## 命令行参数说明

**表1** ctr-img build 命令参数列表

| **命令**      | **参数**       | **说明**                                                     |
| ------------- | -------------- | ------------------------------------------------------------ |
| ctr-img build | --build-arg    | string列表，构建过程中需要用到的变量                         |
|               | --build-static | KV值，构建二进制一致性。目前包含如下K值：- build-time：string，使用固定时间戳来构建容器镜像；时间戳格式为“YYYY-MM-DD HH-MM-SS” |
|               | -f, --filename | string，Dockerfile的路径，不指定则是使用当前路径的Dockerfile文件 |
|               | --format       | string，设置构建镜像的镜像格式：oci｜docker（需开启实验特性选项）|
|               | --iidfile      | string，输出 image ID 到本地文件                             |
|               | -o, --output   | string，镜像导出的方式和路径                                 |
|               | --proxy        | 布尔值，继承主机侧环境的proxy环境变量（默认为true）          |
|               | --tag          | string，给构建的镜像添加tag                                  |
|               | --cap-add      | string列表，构建过程中RUN指令所需要的权限                    |

**表2** ctr-img load 命令参数列表

| **命令**     | **参数**    | **说明**                          |
| ------------ | ----------- | --------------------------------- |
| ctr-img load | -i, --input | string，需要导入的本地tar包的路径 |

**表3** ctr-img push 命令参数列表

| **命令**     | **参数**    | **说明**                          |
| ------------ | ----------- | --------------------------------- |
| ctr-img push | -f, --format | string，推送的镜像格式：oci｜docker（需开启实验特性选项）|

**表4** ctr-img rm 命令参数列表

| **命令**   | **参数**    | **说明**                                      |
| ---------- | ----------- | --------------------------------------------- |
| ctr-img rm | -a, --all   | 布尔值，删除所有本地持久化存储的镜像          |
|            | -p, --prune | 布尔值，删除所有没有tag的本地持久化存储的镜像 |

**表5** ctr-img save 命令参数列表

| **命令**     | **参数**     | **说明**                           |
| ------------ | ------------ | ---------------------------------- |
| ctr-img save | -o, --output | string，镜像导出后在本地的存储路径 |
|              | -f, --format | string，导出层叠镜像的镜像格式：oci｜docker（需开启实验特性选项）|

**表6** login 命令参数列表

| **命令** | **参数**             | **说明**                                                |
| -------- | -------------------- | ------------------------------------------------------- |
| login    | -p, --password-stdin | 布尔值，是否通过stdin读入密码；或采用交互式界面输入密码 |
|          | -u, --username       | string，登录镜像仓库所使用的用户名                      |

**表7** logout 命令参数列表

| **命令** | **参数**  | **说明**                             |
| -------- | --------- | ------------------------------------ |
| logout   | -a, --all | 布尔值，是否登出所有已登录的镜像仓库 |

**表8** manifest annotate命令参数列表

| **命令**          | **说明**      | **参数**                                   |
| ----------------- | ------------- | ------------------------------------------ |
| manifest annotate | --arch        | string，重写镜像适用架构                   |
|                   | --os          | string，重写镜像适用系统                   |
|                   | --os-features | string列表，指定镜像需要的OS特性，很少使用 |
|                   | --variant     | string，指定列表中记录镜像的变量           |

## 通信矩阵

isula-build两个组件进程之间通过unix socket套接字文件进行通信，无端口通信。

## 文件与权限

* isula-build 所有的操作均需要使用 root 权限。如需使用非特权用户操作，则需要配置--group参数

* isula-build 运行涉及文件权限如下表所示：

| **文件路径**                                | **文件/文件夹权限** | **说明**                                                     |
| ------------------------------------------- | ------------------- | ------------------------------------------------------------ |
| /usr/bin/isula-build                        | 550                 | 命令行工具二进制文件。                                       |
| /usr/bin/isula-builder                      | 550                 | 服务端isula-builder进程二进制文件。                          |
| /usr/lib/systemd/system/isula-build.service | 640                 | systemd配置文件，用于管理isula-build服务。                   |
| /etc/isula-build                            | 650                 | isula-builder 配置文件根目录                                 |
| /etc/isula-build/configuration.toml         | 600                 | isula-builder 总配置文件，包含设置 isula-builder 日志级别、持久化目录和运行时目录、OCI runtime等。 |
| /etc/isula-build/policy.json                | 600                 | 签名验证策略文件的语法文件。                                 |
| /etc/isula-build/registries.toml            | 600                 | 针对各个镜像仓库的配置文件，含可用的镜像仓库列表、镜像仓库黑名单。 |
| /etc/isula-build/storage.toml               | 600                 | 本地持久化存储的配置文件，包含所使用的存储驱动的配置。       |
| /etc/isula-build/isula-build.pub            | 400                 | 非对称加密公钥文件                                           |
| /var/run/isula_build.sock                   | 660                 | 服务端isula-builder的本地套接字。                            |
| /var/lib/isula-build                        | 700                 | 本地持久化目录。                                             |
| /var/run/isula-build                        | 700                 | 本地运行时目录。                                             |
| /var/lib/isula-build/tmp/[buildid]/isula-build-tmp-*.tar              | 644                 | 镜像导出至iSulad时的本地暂存目录。                           |
