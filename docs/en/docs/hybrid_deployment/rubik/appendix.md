# Appendix

## DaemonSet Configuration Template

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

## Dockerfile Template

```dockerfile
FROM scratch
COPY ./build/rubik /rubik
ENTRYPOINT ["/rubik"]
```

## Image Build Script

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

## Communication Matrix

- The Rubik service process communicates with the Kubernetes API server as a client through the list-watch mechanism to obtain information about Pods.

|Source IP Address|Source Port|Destination IP Address|Destination Port|Protocol|Port Description|Listening Port Modifiable|Authentication Method|
|----|----|----|----|----|----|----|----|
|Rubik node|32768-61000|api-server node|443|TCP|Kubernetes external resource port |No|Token|

## File Permissions

- All Rubik operations require root permissions.

- Related file permissions are as follows:

|Path|Permissions|Description|
|----|----|----|
|/var/lib/rubik|750|Directory generated after the RPM package is installed, which stores Rubik-related files|
|/var/lib/rubik/build|550|Directory for storing the Rubik binary file|
|/var/lib/rubik/build/rubik|550|Rubik binary file|
|/var/lib/rubik/rubik-daemonset.yaml|550|Rubik DaemonSet configuration template to be used for Kubernetes deployment|
|/var/lib/rubik/Dockerfile|640|Dockerfile template|
|/var/lib/rubik/build_rubik_image.sh|550|Rubik container image build script.|
|/var/log/rubik|640|Directory for storing Rubik log files (requires logDriver=file)|
|/var/log/rubik/rubik.log*|600|Rubik log files|

## Constraints

### Specifications

- Drive: More than 1 GB

- Memory: More than 100 MB

## Runtime

- Only one Rubik instance can exist on a Kubernetes node.

- Rubik cannot take any CLI parameters. Rubik will fail to be started if any CLI parameter is specified.

- When the Rubik process is in the T (TASK_STOPPED or TASK_TRACED) OR D (TASK_UNINTERRUPTIBLE) state, the server is unavailable and does not respond. The service becomes available after the process recovers from the abnormal state.

### Pod Priorities

- Pod priorities cannot be raised. If the priority of service A is changed from -1 to 0, Rubik will report an error.

- Adding or modifying annotations or re-applying Pod YAML configuration file does not trigger Pod rebuild. Rubik senses changes in Pod annotations through the list-watch mechanism.

- After an online service is moved to the offline group, do not move it back to the online group, otherwise QoS exception may occur.

- Do not add important system services and kernel processes to the offline group. Otherwise, they cannot be scheduled timely, causing system errors.

- Online and offline configurations for the CPU and memory must be consistent to avoid QoS conflicts between the two subsystems.

- In the scenario of hybrid service deployment, the original CPU share mechanism is restricted:
    - When both online and offline services run on a CPU, the CPU share of the offline service does not take effect.
    - If only an online or offline service runs on a CPU, its CPU share takes effect.
    - You are advised to set the Pod priority of the offline service to BestEffort.

- Priority inversion of user-mode processes, SMT, cache, NUMA load balancing, and offline service load balancing are not supported.

### Other

To prevent data inconsistency, do not manually modify cgroup or resctrl parameters of the pods, including:

- CPU cgroup directory, such as **/sys/fs/cgroup/cpu/kubepods/burstable/\<PodUID>/\<container-longid>**
    - cpu.qos_level
    - cpu.cfs_burst_us

- memory cgroup directory, such as **/sys/fs/cgroup/memory/kubepods/burstable/\<PodUID>/\<container-longid>**
    - memory.qos_level
    - memory.soft_limit_in_bytes
    - memory.force_empty
    - memory.limit_in_bytes
    - memory.high

- RDT cgroup directory, such as **/sys/fs/resctrl**
