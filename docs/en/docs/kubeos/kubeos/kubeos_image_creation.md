# KubeOS Image Creation

## Introduction

kbimg is an image creation tool required for KubeOS deployment and upgrade. You can use kbimg to create KubeOS Docker, VM, and physical machine images.

## Commands

### Command Format

**bash kbimg.sh** \[ --help \| -h \] create \[ COMMANDS \]  \[ OPTIONS \]

### Parameter Description

* COMMANDS

  | Parameter         | Description                                          |
  | ------------- | ---------------------------------------------- |
  | upgrade-image | Generates a OCI image for installation and upgrade.|
  | vm-image      | Generates a VM image for installation and upgrade.                |
  | pxe-image     | Generates images and files required for physical machine installation.                |

* OPTIONS

  | Option        | Description                                                        |
  | ------------ | ------------------------------------------------------------ |
  | -p           | Path of the repo file. The Yum source required for creating an image is configured in the repo file.       |
  | -v           | Version of the created KubeOS image.                                  |
  | -b           | Path of the os-agent binary file.                                        |
  | -e           | Password of the **root** user of the KubeOS image, which is an encrypted password with a salt value. You can run the OpenSSL or KIWI command to generate the password.|
  | -d           | Generated or used Docker image.                                    |
  | -h  --help | Help Information.                                                |

## Usage Description

### Precautions

* The root permission is required for executing **kbimg.sh**.
* Currently, only the x86 and AArch64 architectures are supported.
* The RPM sources of the kbimg are the **everything** and **EPOL** repositories of openEuler of a specific version. In the Repo file provided during image creation, you are advised to configure the **everything** and **EPOL** repositories of a specific openEuler version for the Yum source.

### Creating a KubeOS OCI Image

#### Precautions

* The created OCI image can be used only for subsequent VM or physical machine image creation or upgrade. It cannot be used to start containers.
* If the default RPM list is used to create a KubeOS image, at least 6 GB drive space is required. If the RPM list is customized, the occupied drive space may exceed 6 GB.

#### Example

* To configure the DNS, customize the `resolv.conf` file in the `scripts` directory.

```shell
  cd /opt/kubeOS/scripts
  touch resolv.conf
  vim resolv.conf
```

* Create a KubeOS image.

``` shell
cd /opt/kubeOS/scripts
bash kbimg.sh create upgrade-image -p xxx.repo -v v1 -b ../bin/os-agent -e '''$1$xyz$RdLyKTL32WEvK3lg8CXID0''' -d your_imageRepository/imageName:version
```

* After the creation is complete, view the created KubeOS image.

``` shell
docker images
```

### Creating a KubeOS VM Image

#### Precautions

* To use a Docker image to create a KubeOS VM image, pull the corresponding image or create a Docker image first and ensure the security of the Docker image.
* The created KubeOS VM image can be used only in a VM of the x86 or AArch64 architecture.
* Currently, KubeOS does not support legacy boot in an x86 VM.
* If the default RPM list is used to create a KubeOS image, at least 25 GB drive space is required. If the RPM list is customized, the occupied drive space may exceed 25 GB.

#### Example

* Using the Repo Source
    * To configure the DNS, customize the `resolv.conf` file in the `scripts` directory.

  ```shell
  cd /opt/kubeOS/scripts
  touch resolv.conf
  vim resolv.conf
  ```

    * Create a KubeOS VM image.

  ``` shell
  cd /opt/kubeOS/scripts
  bash kbimg.sh create vm-image -p xxx.repo -v v1 -b ../bin/os-agent -e '''$1$xyz$RdLyKTL32WEvK3lg8CXID0'''
  ```

* Using a Docker Image

  ``` shell
  cd /opt/kubeOS/scripts
  bash kbimg.sh create vm-image -d  your_imageRepository/imageName:version
  ```

* Result Description
  After the KubeOS image is created, the following files are generated in the **/opt/kubeOS/scripts** directory:
    * **system.qcow2**: system image in QCOW2 format. The default size is 20 GiB. The size of the root file system partition is less than 2,020 MiB, and the size of the Persist partition is less than 16 GiB.
    * **update.img**: partition image of the root file system used for upgrade.

### Creating Images and Files Required for Installing KubeOS on Physical Machines

#### Precautions

* To use a Docker image to create a KubeOS VM image, pull the corresponding image or create a Docker image first and ensure the security of the Docker image.
* The created image can only be used to install KubeOS on a physical machine of the x86 or AArch64 architecture.
* The IP address specified in the **Global.cfg** file is a temporary IP address used during installation. After the system is installed and started, configure the network by referring to **openEuler 22.09 Administrator Guide** > **Configuring the Network**.
* KubeOS cannot be installed on multiple drives at the same time. Otherwise, the startup may fail or the mounting may be disordered.
* Currently, KubeOS does not support legacy boot in an x86 physical machine.
* If the default RPM list is used to create a KubeOS image, at least 5 GB drive space is required. If the RPM list is customized, the occupied drive space may exceed 5 GB.

#### Example

* Modify the `00bootup/Global.cfg` file. All parameters are mandatory. Currently, only IPv4 addresses are supported. The following is a configuration example:

  ```shell
  # rootfs file name
  rootfs_name=kubeos.tar
  # select the target disk to install kubeOS
  disk=/dev/sda
  # pxe server ip address where stores the rootfs on the http server
  server_ip=192.168.1.50
  # target machine temporary ip
  local_ip=192.168.1.100
  # target machine temporary route
  route_ip=192.168.1.1
  # target machine temporary netmask
  netmask=255.255.255.0
  # target machine netDevice name
  net_name=eth0
  ```

* Using the Repo Source
    * To configure the DNS, customize the `resolv.conf` file in the `scripts` directory.

  ```shell
    cd /opt/kubeOS/scripts
    touch resolv.conf
    vim resolv.conf
  ```

    * Create an image required for installing KubeOS on a physical machine.

  ```shell
    cd /opt/kubeOS/scripts
    bash kbimg.sh create pxe-image -p xxx.repo -v v1 -b ../bin/os-agent -e '''$1$xyz$RdLyKTL32WEvK3lg8CXID0'''
  ```

* Using a Docker Image

  ``` shell
  cd /opt/kubeOS/scripts
  bash kbimg.sh create pxe-image -d your_imageRepository/imageName:version
  ```

* Result Description

    * **initramfs.img**: initramfs image used for boot from PXE.
    * **kubeos.tar**: OS used for installation from PXE.
