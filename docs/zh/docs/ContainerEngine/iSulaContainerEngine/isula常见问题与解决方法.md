# 常见问题与解决方法

## **问题1：修改`iSulad`默认运行时为`lxc`，启动容器报错：Failed to initialize engine or runtime**

原因：`iSulad`默认运行时为`runc`，设置默认运行时为`lxc`时缺少依赖。

解决方法：若需修改`iSulad`默认运行时为`lxc`，需要安装`lcr`、`lxc`软件包依赖，且配置`iSulad`配置文件中`runtime`为`lcr`
或者启动容器时指定`--runtime lcr`。启动容器后不应该随意卸载`lcr`、`lxc`软件包，否则可能会导致删除容器时的资源残留。

## **问题2：使用`iSulad` `CRI V1`接口，报错：rpc error: code = Unimplemented desc =**

原因：`iSulad`同时支持`CRI V1alpha2`和`CRI V1`接口，默认使用`CRI V1alpha2`，若使用`CRI V1`，需要开启相应的配置。

解决方法：在`iSulad`配置文件`/etc/isulad/daemon.json`中开启`CRI V1`的配置。

```json
{
    "enable-cri-v1": true,
}
```

若使用源码编译`iSulad`，还需在编译时增加`cmake`编译选项`-D ENABLE_CRI_API_V1=ON`。
