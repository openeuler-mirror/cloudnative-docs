# Appendix

## Command Line Parameters

**Table 1** Parameters of the `ctr-img build` command

| **Command** | **Parameter** | **Description** |
| ------------- | -------------- | ------------------------------------------------------------ |
| ctr-img build | --build-arg | String list, which contains variables required during the build. |
| | --build-static | Key value, which is used to build binary equivalence. Currently, the following key values are included: - build-time: string, which indicates that a fixed timestamp is used to build a container image. The timestamp format is YYYY-MM-DD HH-MM-SS. |
| | -f, --filename | String, which indicates the path of the Dockerfiles. If this parameter is not specified, the current path is used. |
| | --format | String, which indicates the image format **oci** or **docker** (**ISULABUILD_CLI_EXPERIMENTAL** needs to be enabled). |
| | --iidfile | String, which indicates the ID of the image output to a local file. |
| | -o, --output | String, which indicates the image export mode and path.|
| | --proxy | Boolean, which inherits the proxy environment variable on the host. The default value is true. |
| | --tag | String, which indicates the tag value of the image that is successfully built. |
| | --cap-add | String list, which contains permissions required by the **RUN** instruction during the build process.|

**Table 2** Parameters of the `ctr-img load` command

| **Command** | **Parameter** | **Description** |
| ------------ | ----------- | --------------------------------- |
| ctr-img load | -i, --input | String, path of the local .tar package to be imported.|

**Table 3** Parameters of the `ctr-img push` command

| **Command** | **Parameter** | **Description** |
| ------------ | ----------- | --------------------------------- |
| ctr-img push | -f, --format | String, which indicates the pushed image format **oci** or **docker** (**ISULABUILD_CLI_EXPERIMENTAL** needs to be enabled).|

**Table 4** Parameters of the `ctr-img rm` command

| **Command** | **Parameter** | **Description** |
| ---------- | ----------- | --------------------------------------------- |
| ctr-img rm | -a, --all | Boolean, which is used to delete all local persistent images. |
| | -p, --prune | Boolean, which is used to delete all images that are stored persistently on the local host and do not have tags. |

**Table 5** Parameters of the `ctr-img save` command

| **Command** | **Parameter** | **Description** |
| ------------ | ------------ | ---------------------------------- |
| ctr-img save | -o, --output | String, which indicates the local path for storing the exported images.|
| ctr-img save | -f, --format | String, which indicates the exported image format **oci** or **docker** (**ISULABUILD_CLI_EXPERIMENTAL** needs to be enabled).|

**Table 6** Parameters of the `login` command

| **Command** | **Parameter** | **Description** |
| -------- | -------------------- | ------------------------------------------------------- |
| login | -p, --password-stdin | Boolean, which indicates whether to read the password through stdin. or enter the password in interactive mode. |
| | -u, --username | String, which indicates the username for logging in to the image repository.|

**Table 7** Parameters of the `logout` command

| **Command** | **Parameter** | **Description** |
| -------- | --------- | ------------------------------------ |
| logout | -a, --all | Boolean, which indicates whether to log out of all logged-in image repositories. |

**Table 8** Parameters of the `manifest annotate` command

| **Command**       | **Parameter** | **Description**              |
| ----------------- | ------------- | ---------------------------- |
| manifest annotate | --arch        | Set architecture             |
|                   | --os          | Set operating system         |
|                   | --os-features | Set operating system feature |
|                   | --variant     | Set architecture variant     |

## Communication Matrix

The isula-build component processes communicate with each other through the Unix socket file. No port is used for communication.

## File and Permission

- All isula-build operations must be performed by the **root** user. To perform operations as a non-privileged user, you need to configure the `--group` option.

- The following table lists the file permissions involved in the running of isula-build.

| **File Path** | **File/Folder Permission** | **Description** |
| ------------------------------------------- | ------------------- | ------------------------------------------------------------ |
| /usr/bin/isula-build                        | 550                 | Binary file of the command line tool.                                       |
| /usr/bin/isula-builder                      | 550                 | Binary file of the isula-builder process.                          |
| /usr/lib/systemd/system/isula-build.service | 640                 | systemd configuration file, which is used to manage the isula-build service.                   |
| /usr/isula-build                            | 650                 | Root directory of the isula-builder configuration file. |
| /etc/isula-build/configuration.toml         | 600                 | General isula-builder configuration file, including the settings of the isula-builder log level, persistency directory, runtime directory, and OCI runtime. |
| /etc/isula-build/policy.json                | 600                 | Syntax file of the signature verification policy file.                                 |
| /etc/isula-build/registries.toml            | 600                 | Configuration file of each image repository, including the available image repository list and image repository blacklist. |
| /etc/isula-build/storage.toml               | 600                 | Configuration file of the local persistent storage, including the configuration of the used storage driver.       |
| /etc/isula-build/isula-build.pub            | 400                 | Asymmetric encryption public key file. |
| /var/run/isula_build.sock                   | 660                 | Local socket of isula-builder.                            |
| /var/lib/isula-build                        | 700                 | Local persistency directory.                                             |
| /var/run/isula-build                        | 700                 | Local runtime directory.                                             |
| /var/lib/isula-build/tmp/\[build_id\]/isula-build-tmp-*.tar              | 644                 | Local temporary directory for storing the images when they are exported to iSulad.                           |
