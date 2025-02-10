# 使用指南

启动kuasar沙箱的操作步骤如下：

1. 确保kuasar及其相关组件已经正确安装配置

2. 准备业务容器镜像，假设容器镜像为busybox，使用iSula容器引擎下载容器镜像

   ```sh
   $ isula pull busybox
   ```

3. 准备pod和container的yaml文件，范例如下：

   ```sh
   $ cat podsandbox.yaml 
   metadata:
     name: busybox-sandbox
     namespace: default
     uid: hdishd83djaidwnduwk28bcsc
   log_directory: /tmp
   linux:
     namespaces:
       options: {}

   $ cat pod-container.yaml
   metadata:
     name: busybox
   image:
     image: docker.io/library/busybox:latest
   command:
   - top
   log_path: busybox.log
   ```

4. 启动pod

   ```sh
   $ crictl runp --runtime=vmm podsandbox.yaml
   5cbcf744949d8500e7159d6bd1e3894211f475549c0be15d9c60d3c502c7ede3
   ```

   查看pod列表，pod为Ready状态

   ```sh
   $ crictl pods
   POD ID              CREATED              STATE               NAME                NAMESPACE           ATTEMPT
   5cbcf744949d8       About a minute ago   Ready               busybox-sandbox    default             1
   ```

5. 在pod内创建一个业务容器

   ```sh
   $ crictl create 5cbcf744949d8500e7159d6bd1e3894211f475549c0be15d9c60d3c502c7ede3 pod-container.yaml podsandbox.yaml
   c11df540f913e57d1e28372334c028fd6550a2ba73208a3991fbcdb421804a50
   ```

   查看容器列表，容器为Created状态

   ```sh
   $ crictl ps -a
   CONTAINER           IMAGE                              CREATED             STATE               NAME                ATTEMPT             POD ID
   c11df540f913e       docker.io/library/busybox:latest   15 seconds ago         Created             busybox            0                   5cbcf744949d
   ```

6. 启动业务容器

   ```sh
   $ crictl start c11df540f913e57d1e28372334c028fd6550a2ba73208a3991fbcdb421804a50
   ```

   查看容器列表，容器为running状态

   ```sh
   $ crictl ps
   CONTAINER           IMAGE                              CREATED             STATE               NAME                ATTEMPT             POD ID
   c11df540f913e       docker.io/library/busybox:latest   2 minutes ago       Running             busybox            0                   5cbcf744949d8
   ```

   > ![](./public_sys-resources/icon-note.gif) **说明：**
   > 以上步骤4、5、6也可以通过`crictl run`命令直接启动一个pod以及对应的业务容器
   >
   > ```sh
   > $ crictl run -r vmm --no-pull container-config.yaml podsandbox-config.yaml
   > ```

7. 停止并删除容器以及pod

   ```sh
   $ crictl rm -f c11df540f913e
   $ crictl rmp -f 5cbcf744949d8
   ```
