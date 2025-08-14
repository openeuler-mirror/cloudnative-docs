# iSulad+k8s集群部署指南

本文档介绍在 openEuler 操作系统上，通过 kubeadm 部署 K8S 集群，搭建 K8S+iSulad 的环境，并在该环境上部署 gitlab-runner，指导部署欧拉原生开发环境集群。

本文档主要包括以下两个场景内容：

场景一： 基于 gitlab-ci 从 “0” 开始构建欧拉原生开发CICD部署指导。   
场景二： 欧拉原生开发执行机集群被 gitlab-ci 纳管指导。

场景一中需要额外部署gitlab，步骤操作顺序为：

1. K8s+iSulad 环境部署。
2. gitlab 部署。   
3. gitlab runner 部署和测试。

场景二中已有 gitlab-ci 平台，无需额外部署，步骤操作顺序为：

1. K8s+iSulad 环境部署。   
2. gitlab runner 部署和测试。  

> [!NOTE]说明
>
> 本文档所有操作均使用root权限执行。
