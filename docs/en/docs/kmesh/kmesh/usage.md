# Usage

## Using kmesh-daemon

```shell
# Display help information.
[root@openEuler ~]# kmesh-daemon -h
Usage of kmesh-daemon:
  -bpf-fs-path string
        bpf fs path (default "/sys/fs/bpf")
  -cgroup2-path string
        cgroup2 path (default "/mnt/kmesh_cgroup2")
  -config-file string
        [if -enable-kmesh] deploy in kube cluster (default "/etc/kmesh/kmesh.json")
  -enable-ads
        [if -enable-kmesh] enable control-plane from ads (default true)
  -enable-kmesh
        enable bpf kmesh
  -service-cluster string
        [if -enable-kmesh] TODO (default "TODO")
  -service-node string
        [if -enable-kmesh] TODO (default "TODO")

# Enable ADS by default.
[root@openEuler ~]# kmesh-daemon -enable-kmesh

# Enable ADS and specify the path of the configuration file.
[root@openEuler ~]# kmesh-daemon -enable-kmesh -enable-ads=true -config-file=/examples/kmesh.json

# Disable ADS.
[root@openEuler ~]# kmesh-daemon -enable-kmesh -enable-ads=false
```

## Using kmesh-cmd

```shell
# Display help information.
[root@openEuler ~]# kmesh-cmd -h
Usage of kmesh-cmd:
  -config-file string
        input config-resources to bpf maps (default "./config-resources.json")

# Manually load configurations.
[root@openEuler ~]# kmesh-cmd -config-file=/examples/config-resources.json
```

## Using O&M Commands

```shell
# Display help information.
[root@openEuler ~]# curl http://localhost:15200/help
    /help: print list of commands
    /options: print config options
    /bpf/kmesh/maps: print bpf kmesh maps in kernel
    /controller/envoy: print control-plane in envoy cache
    /controller/kubernetes: print control-plane in kubernetes cache

# Read the loaded configurations.
[root@openEuler ~]# curl http://localhost:15200/bpf/kmesh/maps
[root@openEuler ~]# curl http://localhost:15200/options
```

## Precautions

* If `-enable-ads=true` is configured, Kmesh automatically receives orchestration rules from the service mesh control plane. In this case, do not run the `kmesh-cmd` command to deliver rules to avoid duplicated configurations.

* The `-bpf-fs-path` option specifies the BPF directory of the OS. Data related to the Kmesh BPF program will be stored in this directory. The default directory is `/sys/fs/bpf`.

* The `-cgroup2-path` option specifies the cgroup directory of the OS. The default directory is `/mnt/kmesh_cgroup2`.
