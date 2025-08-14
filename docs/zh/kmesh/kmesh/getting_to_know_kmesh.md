# 认识Kmesh

## 简介

随着越来越多的应用云原生化，云上应用的规模、应用SLA诉求等都对云基础设施提出了很高的要求。

基于k8s的云基础设施能够帮助应用实现敏捷的部署管理，但在应用流量编排方面有所欠缺，serviceMesh的出现很好的弥补了k8s流量编排的缺陷，与k8s互补，真正实现敏捷的云应用开发运维；但随着对serviceMesh应用的逐步深入，当前基于sidecar的网格架构在数据面存在明显的性能缺陷，已成为业界共识的问题：

* 时延性能差
    以serviceMesh典型软件istio为例，网格化后，服务访问单跳时延增加2.65ms；无法满足时延敏感型应用诉求

* 底噪开销大
    istio中，每个sidecar软件占用内存50M+，CPU默认独占2 core，对于大规模集群底噪开销太大，降低了业务容器的部署密度

Kmesh基于可编程内核，将网格流量治理下沉OS，数据路径3跳->1跳，大幅提升网格数据面的时延性能，帮助业务快速创新。

## 架构

Kmesh总体架构如下图所示：

![](./figures/kmesh-arch.png)

Kmesh的主要部件包括：

* kmesh-controller：
    kmesh管理程序，负责Kmesh生命周期管理、XDS协议对接、观测运维等功能

* kmesh-api：
    kmesh对外提供的api接口层，主要包括：xds转换后的编排API、观测运维通道等

* kmesh-runtime：
    kernel中实现的支持L3~L7流量编排的运行时

* kmesh-orchestration：
    基于ebpf实现L3~L7流量编排，如路由、灰度、负载均衡等

* kmesh-probe：
    观测运维探针，提供端到端观测能力
