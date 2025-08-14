# Common Issues and Solutions

## Issue 1: Changing iSulad Default Runtime to `lxc` Causes Container Startup Error: Failed to Initialize Engine or Runtime

**Cause**: iSulad uses `runc` as its default runtime. Switching to `lxc` without the required dependencies causes this issue.

**Solution**: To set `lxc` as the default runtime, install the `lcr` and `lxc` packages. Then, either configure the `runtime` field in the iSulad configuration file to `lcr` or use the `--runtime lcr` flag when launching containers. Avoid uninstalling `lcr` or `lxc` after starting containers, as this may leave behind residual resources during container deletion.

## Issue 2: Error When Using iSulad CRI V1 Interface: rpc error: code = Unimplemented desc =

**Cause**: iSulad supports both CRI V1alpha2 and CRI V1 interfaces, with CRI V1alpha2 enabled by default. Using CRI V1 requires explicit configuration.

**Solution**: Enable the CRI V1 interface by modifying the iSulad configuration file at **/etc/isulad/daemon.json**.

```json
{
    "enable-cri-v1": true,
}
```

When compiling iSulad from source, include the `cmake` option `-D ENABLE_CRI_API_V1=ON` to enable CRI V1 support.
