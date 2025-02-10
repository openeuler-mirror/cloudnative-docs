# 常见问题与解决方法

## **问题1：Kubernetes + docker为什么无法部署**

原因：Kubernetes自1.21版本开始不再支持Kubernetes + docker部署Kubernetes集群。

解决方法：改为使用cri-dockerd+docker部署集群，也可以使用containerd或者iSulad部署集群。

## **问题2：openEuler无法通过yum直接安装Kubernetes相关的rpm包**

原因：Kubernetes相关的rpm包需要配置yum的repo源有关EPOL的部分。

解决方法：[参考链接](https://forum.openeuler.org/t/topic/768)中repo源，重新配置环境中的EPOL源。
