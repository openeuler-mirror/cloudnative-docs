# rubik 使用指南

## 概述

如何改善服务器资源利用率低的现状一直是业界公认的难题，随着云原生技术的发展，将在线（高优先级）、离线（低优先级）业务混合部署成为了当下提高资源利用率的有效手段。

rubik 容器调度在业务混合部署的场景下，根据 QoS 分级，对资源进行合理调度，从而实现在保障在线业务服务质量的前提下，大幅提升资源利用率。

rubik 当前支持如下特性：

- [preemption 绝对抢占](./feature_introduction.md#preemption-绝对抢占)
    - [CPU绝对抢占](./feature_introduction.md#cpu绝对抢占)
    - [内存绝对抢占](./feature_introduction.md#内存绝对抢占)
- [dynCache 访存带宽和LLC限制](./feature_introduction.md#dyncache-访存带宽和llc限制)
- [dynMemory 内存异步分级回收](./feature_introduction.md#dynmemory-内存异步分级回收)
- [支持弹性限流](./feature_introduction.md#支持弹性限流)
    - [quotaBurst 支持弹性限流内核态解决方案](./feature_introduction.md#quotaburst-内核态解决方案)
    - [quotaTurbo 支持弹性限流用户态解决方案](./feature_introduction.md#quotaturbo-用户态解决方案)
- [ioCost 支持iocost对IO权重控制](./feature_introduction.md#iocost-支持iocost对io权重控制)
- [PSI 支持基于PSI指标的干扰检测](./feature_introduction.md#psi-支持基于psi指标的干扰检测)
- [CPU驱逐水位线控制](./feature_introduction.md#cpu驱逐水位线控制)
- [内存驱逐水位线控制](./feature_introduction.md#内存驱逐水位线控制)

本文档适用于使用 openEuler 系统并希望了解和使用 rubik 的社区开发者、开源爱好者以及相关合作伙伴。使用人员需要具备以下经验和技能：

- 熟悉 Linux 基本操作
- 熟悉 kubernetes 和 docker/iSulad 基本操作
