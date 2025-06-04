# 功能特性描述

## 容器技术

NestOS通过容器化 (containerized) 的运算环境向应用程序提供运算资源，应用程序之间共享系统内核和资源，但是彼此之间又互不可见。这意味着应用程序将不会再被直接安装到操作系统中，而是通过 容器引擎(Docker、Podman、iSulad等) 运行在容器中。大大降低了操作系统、应用程序及运行环境之间的耦合度。相对于传统的应用程序部署部署方式而言，在NestOS 集群中部署应用程序更加灵活便捷，应用程序运行环境之间的干扰更少，而且操作系统自身的维护也更加容易。

## rpm-ostree

### 系统更新

rpm-ostree是一种镜像/包混合系统，可以看成是rpm和ostree的合体。一方面它提供了基于rpm的软件包安装管理方式，另一方面它提供了基于ostree的操作系统更新升级。rpm-ostree将这两种操作都视为对操作系统的更新，每次对系统的更新都像rpm-ostree在提交“Transaction-事务”，从而确保更新全部成功或全部失败，并且允许在更新系统后回滚到更新前的状态。

rpm-ostree在更新操作系统的时候会有2个bootable区域，分别为主动分区和被动分区，对系统的更新升级在被动分区进行，在重启操作系统主动分区和被动分区转换后才生效。如果软件安装或升级出现问题，通过rpm-ostree会使NestOS回滚到先前的状态。NestOS的“/ostree/”和“/boot/”目录是ostree Repository环境，通过该目录可以查看当前boot使用的哪个ostree。

### 只读文件系统

在rpm-ostree的文件系统布局中，只有/etc和/var是唯一可写的目录，/var中的任何数据不会被触及，而是在升级过程中共享。在系统升级的过程中采用新的缺省值/etc，并将更改添加到顶部。这意味着升级将会接收/etc中新的默认文件，这是一个非常关键的特性。

在通用操作系统中，/var目录下的部分文件采用“/var to tmpfiles.d”的处理策略，即系统通过systemd-tmpfile-setup.service读取/usr/lib/tmpfiles.d/目录下的conf文件，完成/var目录下文件夹和空白文件的创建，/usr/lib/tmpfiles.d/目录下的conf文件全部由相关rpm包提供。在NestOS中，/var目录不涉及rpm-ostree的commit分层，rpm-ostree各个commit 分层都会共享一个/var目录，但是/var目录下的文件会与ostree事务更新模型冲突，在安装软件包时rpm-ostree会将该文件删除。/var目录下的内容完全依赖“/var to tmpfiles.d”来生成，因此NestOS的/usr/lib/tmpfiles.d/目录下，除了部分rpm提供出的conf外，还存在由rpm-ostree在安装XXX软件包时生成的pkg-XXX.conf文件（即使XXX已经提供了conf文件），该文件记录了XXX软件包提供的/var下的文件夹，不涉及文件（文件在rpm-ostree安装包时已经删除）。当用户需要对rpm包提供的/var下的文件夹进行操作时，如删除某文件夹，简单的使用rm命令只能暂时删除，当系统重启后，该文件夹依旧存在，只有修改pkg-XXX.conf文件才能完成永久删除。

ostree旨在可以并行安装多个独立操作系统的版本，ostree依赖于一个新的ostree 目录，该目录实际上可以并行安装在现有的操作系统或者是占据物理/root目录的发行版本中。每台客户机和每组部署上都存储在 /ostree/deploy/STATEROOT/CHECKSUM 上，而且还有一个ostree Repository存储在 /ostree/repo 中。每个部署主要由一组指向存储库的硬链接组成，这意味着每个版本都进行了重复数据的删除并且升级过程中只消耗了与新文件成比例的磁盘空间加上一些恒定的开销。

ostree模型强调的是OS只读内容保存在 /usr 中，它附带了⽤于创建Linux只读安装以防止无意损坏的代码，对于给定的操作系统，每个部署之间都有一个 /var 共享的可供读写的目录。ostree核心代码不触及该目录的内容，如何管理和升级状态取决于每个操作系统中的代码。

### 系统扩展

出于安全性和可维护性的考虑，NestOS让基础镜像尽可能保持小巧和精简。但是在某些情况下，需要向基本操作系统本⾝添加软件，例如驱动软件，VPN等等，因为它们比较难容器化。这些包拓展了操作系统的功能，为此，rpm-ostree将这些包视为拓展，而不是仅仅在用户运行时提供。也就是说，目前NestOS对于实际安装哪些包没有限制，默认情况下，软件包是从openEuler仓库下载的。

要对软件包进行分层，需要重新编写一个systemd单元来执行rpm-ostree命令安装所需要的包，所做的更改应⽤于新部署，重新启动才能⽣效。

## nestos-installer

nestos-installer是一个帮助安装Nestos的程序，它可以执行以下操作：

（1）安装操作系统到一个目标磁盘，可使用Ignition和首次引导内核参数对其进行自定义(nestos-installer install)

（2）下载并验证各种云平台、虚拟化或者裸机平台的操作系统映像(nestos-installer download)

（3）列出可供下载的nestos镜像(nestos-installer list-stream)

（4）在ISO中嵌入一个Ignition配置，以自定义地从中启动操作系统(nestos-installer iso ignition)

（5）将Ignition配置包装在initd映像中，该映像可以被加入到PXE initramfs中以自定义从中启动的操作系统(nestos-installer pxe ignition)

## zincati

Zincati是NestOS⾃动更新的代理，它作为Cincinnati服务的客户端，负责监听NestOS版本变化并调用rpm-ostree进行⾃动更新。Zincati有如下特点：

（1）支持自动更新代理，支持分阶段推出

（2）通过toml配置文件支持运行时自定义，用户自定义配置文件可覆盖默认配置

（3）多种更新策略

（4）通过维护窗口每周在特定时间范围内进行更新的策略

（5）收集和导出本地运行的zincati内部指标，可提供给Prometheus以减轻跨大量节点的监控任务

（6）具有可配置优先级的日志记录

（7）通过Cincinnati协议支持复杂的更新图

（8）通过外部锁管理器支持集群范围的重启编排

## 系统初始化（Ignition）

Ignition 是一个与分发无关的配置实用程序，不仅用于安装，还读取配置文件（JSON 格式）并根据该配置初始化NestOS。可配置的组件包括存储和文件系统、systemd单元和用户。

Ignition仅在系统第一次引导期间运行一次（在initramfs中）。因为 Ignition 在启动过程的早期运行，所以它可以在用户空间开始启动之前重新分区磁盘、格式化文件系统、创建用户和写入文件。 因此，systemd 服务在 systemd 启动时已经写入磁盘，从而加快了启动速度。

（1）Ignition 仅在第一次启动时运行

Ignition 旨在用作配置工具，而不是配置管理工具。 Ignition 鼓励不可变的基础设施，其中机器修改要求用户丢弃旧节点并重新配置机器。

（2）Ignition不是在任何情况下都可以完成配置

Ignition 执行它需要的操作，使系统与 Ignition 配置中描述的状态相匹配。 如果由于任何原因 Ignition 无法提供配置要求的确切机器，Ignition 会阻止机器成功启动。例如，如果用户想要获取托管在[foo.conf](https://example.com/foo.conf)的文档并将其写入磁盘，如果无法解析给定的 URL，Ignition 将阻止机器启动。 

（3）Ignition只是声明性配置

Ignition配置只描述了系统的状态，没有列出 Ignition 应该采取的一系列步骤。

Ignition 配置不允许用户提供任意逻辑（包括 Ignition 运行的脚本）。用户只需描述哪些文件系统必须存在、哪些文件必须创建、哪些用户必须存在等等。任何进一步的定制都必须使用由 Ignition 创建的 systemd 服务。 

（4）Ignition配置不应手写

Ignition 配置被设计为人类可读但难以编写，是为了阻止用户尝试手动编写配置。可以使用Butane或类似工具生成或转化生成Ignition 配置。

## Afterburn

Afterburn是类似于云平台一样的一次性代理，可以用于与特定的提供者的元数据端点进行交互，通常和Ignition结合使用。

Afterburn包含了很多可以在实例生命周期中不同时间段运行的模块。下面是特定的平台可能在第一次启动时在initramfs中运行的服务：

（1）设置本地主机名

（2）加入网络命令行参数

以下的功能是在一定条件下，作为systemd服务单元在一些平台上才能使用的：

（1）为本地系统用户安装公共SSH密钥

（2）从实例元数据中检索属性

（3）给提供者登记以便报道成功的启动或实例供应
