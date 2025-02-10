# 常见问题与解决方法

## **问题1：isula-build拉取镜像报错：pinging container registry xx: get xx: dial tcp host:repo: connect: connection refused**

原因：拉取的镜像来源于非授信仓库。

解决方法：修改isula-build镜像仓库的配置文件/etc/isula-build/registries.toml，将该非授信仓库加入[registries.insecure]，重启isula-build。
