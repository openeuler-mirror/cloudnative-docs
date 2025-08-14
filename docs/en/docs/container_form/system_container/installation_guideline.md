# Installation Guideline

1. Install the container engine iSulad.

    ```shell
    # yum install iSulad
    ```

2. Install dependent packages of system containers.

    ```shell
    # yum install isulad-tools authz isulad-lxcfs-toolkit lxcfs
    ```

3. Run the following command to check whether iSulad is started:

    ```shell
    # systemctl status isulad
    ```

4. Enable the lxcfs and authz services.

    ```shell
    # systemctl start lxcfs
    # systemctl start authz
    ```
