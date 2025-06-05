# 升级

- 若为相同大版本之间的升级，例如从2.x.x版本升级到2.x.x版本，请执行如下命令：

    ```sh
    # sudo yum update -y iSulad
    ```

- 若为不同大版本之间的升级，例如从1.x.x版本升级到2.x.x版本，请先保存当前的配置文件/etc/isulad/daemon.json，并卸载已安装的iSulad软件包，然后安装待升级的iSulad软件包，随后恢复配置文件。

>![NOTE]说明   
>
> - 可通过**sudo rpm -qa |grep iSulad**  或  **isula version**  命令确认当前iSulad的版本号。  
> - 相同大版本之间，如果希望手动升级，请下载iSulad及其所有依赖的RPM包进行升级，参考命令如下：  
>
> ```sh
> # sudo rpm -Uhv iSulad-xx.xx.xx-YYYYmmdd.HHMMSS.gitxxxxxxxx.aarch64.rpm  
>    ```  
>
> 若升级失败，可通过--force选项进行强制升级，参考命令如下：  
>
> ```sh 
> # sudo rpm -Uhv --force iSulad-xx.xx.xx-YYYYmmdd.HHMMSS.gitxxxxxxxx.aarch64.rpm  
>    ```  
>
> - 如若iSulad依赖的libisula组件发生升级，iSulad应该与对应版本的libisula一起升级，参考命令如下：
>
> ```sh
> # sudo rpm -Uvh libisula-xx.xx.xx-YYYYmmdd.HHMMSS.gitxxxxxxxx.aarch64.rpm iSulad-xx.xx.xx-YYYYmmdd.HHMMSS.gitxxxxxxxx.aarch64.rpm
>    ```
>
> - iSulad在openeuler 22.03-LTS-SP3之前的版本使用lcr作为默认容器运行时。因此，跨此版本升级时，在升级之前创建的容器仍是使用lcr作为容器运行时，只有在升级之后创建的容器才会采用新版本的默认运行时runc。若在新版本中仍需使用lcr容器运行时，需要修改isulad默认配置文件（默认为/etc/isulad/daemon.json）中的default-runtime为lcr或者在运行容器时指定容器运行时为lcr（--runtime lcr）, 在升级时若对应的lcr、lxc版本发生升级，同样应该与iSulad一起升级。
