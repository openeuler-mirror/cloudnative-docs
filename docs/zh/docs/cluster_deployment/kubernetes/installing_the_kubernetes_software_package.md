# 安装 Kubernetes 软件包

通过dnf安装k8s所需要的依赖工具包

```bash
dnf install -y docker conntrack-tools socat
```

配置EPOL源之后，可以直接通过 dnf 安装 K8S

```bash
dnf install kubernetes
```
