# Usage Instructions

Start a Kuasar sandbox.

1. Ensure that Kuasar and related components have been correctly installed and configured.

2. Prepare the service container image. Assume that the container image is **busybox**. Use the iSula container engine to download the container image.

   ```sh
   isula pull busybox
   ```

3. Prepare the YAML files for the pod and container. The file examples are as follows:

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

4. Start a pod.

   ```sh
   $ crictl runp --runtime=vmm podsandbox.yaml
   5cbcf744949d8500e7159d6bd1e3894211f475549c0be15d9c60d3c502c7ede3
   ```

   Check the pod list. The pod is in the **Ready** state.

   ```sh
   $ crictl pods
   POD ID              CREATED              STATE               NAME                NAMESPACE           ATTEMPT
   5cbcf744949d8       About a minute ago   Ready               busybox-sandbox    default             1
   ```

5. Create a service container in the pod.

   ```sh
   $ crictl create 5cbcf744949d8500e7159d6bd1e3894211f475549c0be15d9c60d3c502c7ede3 pod-container.yaml podsandbox.yaml
   c11df540f913e57d1e28372334c028fd6550a2ba73208a3991fbcdb421804a50
   ```

   View the container list. The container is in the **Created** state.

   ```sh
   $ crictl ps -a
   CONTAINER           IMAGE                              CREATED             STATE               NAME                ATTEMPT             POD ID
   c11df540f913e       docker.io/library/busybox:latest   15 seconds ago         Created             busybox            0                   5cbcf744949d
   ```

6. Start the service container.

   ```sh
   crictl start c11df540f913e57d1e28372334c028fd6550a2ba73208a3991fbcdb421804a50
   ```

   Check the container list. The container is in the **Running** state.

   ```sh
   $ crictl ps
   CONTAINER           IMAGE                              CREATED             STATE               NAME                ATTEMPT             POD ID
   c11df540f913e       docker.io/library/busybox:latest   2 minutes ago       Running             busybox            0                   5cbcf744949d8
   ```

   > [!NOTE]NOTE
   > You can also run a `crictl run` command to start a pod with a service container.

   ```sh
   crictl run -r vmm --no-pull container-config.yaml podsandbox-config.yaml
   ```

7. Stop and delete the container and the pod.

   ```sh
   crictl rm -f c11df540f913e
   crictl rmp -f 5cbcf744949d8
   ```
