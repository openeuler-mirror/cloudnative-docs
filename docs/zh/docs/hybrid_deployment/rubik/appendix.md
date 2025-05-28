# 附录

## DaemonSet 配置模板

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: rubik
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["list", "watch"]
  - apiGroups: [""]
    resources: ["pods/eviction"]
    verbs: ["create"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: rubik
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: rubik
subjects:
  - kind: ServiceAccount
    name: rubik
    namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rubik
  namespace: kube-system
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: rubik-config
  namespace: kube-system
data:
  config.json: |
    {
      "agent": {
        "logDriver": "stdio",
        "logDir": "/var/log/rubik",
        "logSize": 1024,
        "logLevel": "info",
        "cgroupRoot": "/sys/fs/cgroup",
        "enabledFeatures": [
          "preemption"
        ]
      },
      "preemption": {
        "resource": [
          "cpu"
        ]
      }
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: rubik-agent
  namespace: kube-system
  labels:
    k8s-app: rubik-agent
spec:
  selector:
    matchLabels:
      name: rubik-agent
  template:
    metadata:
      namespace: kube-system
      labels:
        name: rubik-agent
    spec:
      serviceAccountName: rubik
      hostPID: true
      containers:
      - name: rubik-agent
        image: hub.oepkgs.net/cloudnative/rubik:latest
        imagePullPolicy: IfNotPresent
        env:
          - name: RUBIK_NODE_NAME
            valueFrom:
              fieldRef:
                fieldPath: spec.nodeName
        securityContext:
          capabilities:
            add:
            - SYS_ADMIN
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: rubiklog
          mountPath: /var/log/rubik
          readOnly: false
        - name: runrubik
          mountPath: /run/rubik
          readOnly: false
        - name: sysfs
          mountPath: /sys/fs
          readOnly: false
        - name: devfs
          mountPath: /dev
          readOnly: false
        - name: config-volume
          mountPath: /var/lib/rubik
      terminationGracePeriodSeconds: 30
      volumes:
      - name: rubiklog
        hostPath:
          path: /var/log/rubik
      - name: runrubik
        hostPath:
          path: /run/rubik
      - name: sysfs
        hostPath:
          path: /sys/fs
      - name: devfs
        hostPath:
          path: /dev
      - name: config-volume
        configMap:
          name: rubik-config
          items:
          - key: config.json
            path: config.json
```

## Dockerfile 模板

```dockerfile
FROM scratch
COPY ./build/rubik /rubik
ENTRYPOINT ["/rubik"]
```

## 镜像构建脚本

```bash
#!/bin/bash
set -e

CURRENT_DIR=$(cd "$(dirname "$0")" && pwd)
BINARY_NAME="rubik"

RUBIK_FILE="${CURRENT_DIR}/build/rubik"
DOCKERFILE="${CURRENT_DIR}/Dockerfile"
YAML_FILE="${CURRENT_DIR}/rubik-daemonset.yaml"

# Get version and release number of rubik binary
VERSION=$(${RUBIK_FILE} -v | grep ^Version | awk '{print $NF}')
RELEASE=$(${RUBIK_FILE} -v | grep ^Release | awk '{print $NF}')
IMG_TAG="${VERSION}-${RELEASE}"

# Get rubik image name and tag
IMG_NAME_AND_TAG="${BINARY_NAME}:${IMG_TAG}"

# Build container image for rubik
docker build -f "${DOCKERFILE}" -t "${IMG_NAME_AND_TAG}" "${CURRENT_DIR}"

echo -e "\n"
# Check image existence
docker images | grep -E "REPOSITORY|${BINARY_NAME}"

# Modify rubik-daemonset.yaml file, set rubik image name
sed -i "/image:/s/:.*/: ${IMG_NAME_AND_TAG}/" "${YAML_FILE}"
```

## 通信矩阵

- rubik 服务进程作为客户端通过 List/Watch 机制与 kubernetes API Server 进行通信，从而获取 Pod 等信息

|源IP|源端口|目的IP|目标端口|协议|端口说明|侦听端口是否可更改|认证方式|
|----|----|----|----|----|----|----|----|
|rubik所在节点机器|32768-61000|api-server所在服务器|443|tcp|kubernetes对外提供的访问资源的端口|不可更改|token|

## 文件与权限

- rubik 所有的操作均需要使用 root 权限。

- 涉及文件及权限如下表所示：

|文件路径|文件/文件夹权限|说明|
|----|----|----|
|/var/lib/rubik|750|rpm 安装完成后生成目录，存放 rubik 相关文件|
|/var/lib/rubik/build|550|存放 rubik 二进制文件的目录|
|/var/lib/rubik/build/rubik|550|rubik 二进制文件|
|/var/lib/rubik/rubik-daemonset.yaml|640|rubik daemon set 配置模板，供 k8s 部署使用|
|/var/lib/rubik/Dockerfile|640|Dockerfile 模板|
|/var/lib/rubik/build_rubik_image.sh|550|rubik 容器镜像构建脚本|
|/var/log/rubik|700|rubik 日志存放目录（需开启 logDriver=file 后使能）|
|/var/log/rubik/rubik.log*|600|rubik 日志文件|

## 约束限制

### 规格

- 磁盘：1GB+

- 内存：100MB+

## 运行时

- 每个 k8s 节点只能部署一个 rubik，多个 rubik 会冲突

- rubik 不接收任何命令行参数，若添加参数启动会报错退出

- 如果 rubik 进程进入 T、D 状态，则服务端不可用，此时服务不会响应，需恢复异常状态之后才可继续使用

### Pod 优先级设置

- 禁止低优先级往高优先级切换。如业务 A 先被设置为低优先级（-1），接着设置为高优先级（0），rubik 报错

- 用户添加注解、修改注解、修改 Pod yaml 中的注解并重新 apply 等操作不会触发 Pod 重建。rubik 会通过 List/Watch 机制感知 Pod 注解变化情况

- 禁止将任务从在线组迁移到离线组后再迁移回在线组，此操作会导致该任务 QoS 异常

- 禁止将重要的系统服务和内核线程加入到离线组中，否则可能导致调度不及时，进而导致系统异常

- CPU 和 memory 的在线、离线配置需要统一，否则可能导致两个子系统的 QoS 冲突

- 使用混部后，原始的 CPU share 功能存在限制。具体表现为：
    - 若当前 CPU 中同时存放在线任务和离线任务，则离线任务的 CPU share 无法生效
    - 若当前 CPU 中只有在线任务或只有离线任务，CPU share 能生效
    - 建议离线业务 Pod 优先级配置为 best effort

- 用户态的优先级反转、smt、cache、numa 负载均衡、离线任务的负载均衡，当前不支持

### 其他

禁止用户直接手动修改 Pod 对应 cgroup 或 resctrl 参数，否则可能出现数据不一致情况。

- CPU cgroup 目录， 如：`/sys/fs/cgroup/cpu/kubepods/burstable/<PodUID>/<container-longid>`
    - cpu.qos_level
    - cpu.cfs_burst_us

- memory cgroup 目录，如：`/sys/fs/cgroup/memory/kubepods/burstable/<PodUID>/<container-longid>`
    - memory.qos_level
    - memory.soft_limit_in_bytes
    - memory.force_empty
    - memory.limit_in_bytes
    - memory.high

- RDT 控制组目录，如：`/sys/fs/resctrl`
