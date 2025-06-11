# Container Management

## Creating a Container

### Description

To create a container, run the  **isula create**  command. The container engine will use the specified container image to create a read/write layer, or use the specified local rootfs as the running environment of the container. After the creation is complete, the container ID is output as standard output. You can run the  **isula start**  command to start the container. The new container is in the  **inited**  state.

### Usage

```shell
isula create [OPTIONS] IMAGE [COMMAND] [ARG...]
```

### Parameters

The following table lists the parameters supported by the  **create**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0182207105_table36127413817"></a>
<table><tbody><tr id="en-us_topic_0182207105_row1457792217573"><td class="cellrowborder" valign="top" width="17.44%"><p id="en-us_topic_0182207105_p2578182275712"><a name="en-us_topic_0182207105_p2578182275712"></a><a name="en-us_topic_0182207105_p2578182275712"></a><strong id="en-us_topic_0182207105_b6563101485812"><a name="en-us_topic_0182207105_b6563101485812"></a><a name="en-us_topic_0182207105_b6563101485812"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.190000000000005%"><p id="en-us_topic_0182207105_p657892213573"><a name="en-us_topic_0182207105_p657892213573"></a><a name="en-us_topic_0182207105_p657892213573"></a><strong id="en-us_topic_0182207105_b18644195580"><a name="en-us_topic_0182207105_b18644195580"></a><a name="en-us_topic_0182207105_b18644195580"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.37%"><p id="en-us_topic_0182207105_p15578102285710"><a name="en-us_topic_0182207105_p15578102285710"></a><a name="en-us_topic_0182207105_p15578102285710"></a><strong id="en-us_topic_0182207105_b1064111916582"><a name="en-us_topic_0182207105_b1064111916582"></a><a name="en-us_topic_0182207105_b1064111916582"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row11591115892517"><td class="cellrowborder" rowspan="42" valign="top" width="17.44%"><p id="en-us_topic_0182207105_p1921425017550"><a name="en-us_topic_0182207105_p1921425017550"></a><a name="en-us_topic_0182207105_p1921425017550"></a><strong id="en-us_topic_0182207105_b112687501808"><a name="en-us_topic_0182207105_b112687501808"></a><a name="en-us_topic_0182207105_b112687501808"></a>create</strong></p>
<p id="en-us_topic_0182207105_p7986133491612"><a name="en-us_topic_0182207105_p7986133491612"></a><a name="en-us_topic_0182207105_p7986133491612"></a>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--add-host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Add custom host-to-IP mapping (host:ip)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top" width="39.190000000000005%"><p id="en-us_topic_0182207105_p8129151463514"><a name="en-us_topic_0182207105_p8129151463514"></a><a name="en-us_topic_0182207105_p8129151463514"></a>--annotation</p>
</td>
<td class="cellrowborder" valign="top" width="43.37%"><p id="en-us_topic_0182207105_p5129191418354"><a name="en-us_topic_0182207105_p5129191418354"></a><a name="en-us_topic_0182207105_p5129191418354"></a>Set container annotations. For example, supporting the native.umask option:</p>
<pre class="screen" id="en-us_topic_0182207105_screen1112917145352"><a name="en-us_topic_0182207105_screen1112917145352"></a><a name="en-us_topic_0182207105_screen1112917145352"></a>--annotation native.umask=normal # The umask value of the launched container is 0022
--annotation native.umask=secure # The umask value of the launched container is 0027</pre>
<p id="en-us_topic_0182207105_p10129314183518"><a name="en-us_topic_0182207105_p10129314183518"></a><a name="en-us_topic_0182207105_p10129314183518"></a>Note: If this parameter is not configured, the umask configuration in isulad is used.</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--blkio-weight</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--blkio-weight-device</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Block IO weight (relative device weight), format: DEVICE_NAME: weight, weight value between 10 and 1000, or 0 to disable (default 0)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--cap-add</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Add Linux capability</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--cap-drop</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Drop Linux capability</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row858858181018"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p359014818108"><a name="en-us_topic_0182207105_p359014818108"></a><a name="en-us_topic_0182207105_p359014818108"></a>--cgroup-parent</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p15905813106"><a name="en-us_topic_0182207105_p15905813106"></a><a name="en-us_topic_0182207105_p15905813106"></a>Specify container cgroup parent path</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU CFS (Completely Fair Scheduler) period</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-quota</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU CFS (Completely Fair Scheduler) quota</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-rt-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU real-time period (in microseconds)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-rt-runtime</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU real-time runtime (in microseconds)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row5991571341"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p14237174014515"><a name="en-us_topic_0182207105_p14237174014515"></a><a name="en-us_topic_0182207105_p14237174014515"></a>--cpu-shares</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p42394406520"><a name="en-us_topic_0182207105_p42394406520"></a><a name="en-us_topic_0182207105_p42394406520"></a>CPU shares (relative weight)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpus</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>Number of CPUs</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpuset-cpus</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>Allowed CPUs (e.g. 0-3, 0, 1)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpuset-mems</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>Allowed memory nodes (e.g. 0-3, 0, 1)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Add a host device to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-cgroup-rule</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Add a rule to the cgroup allowed device list</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-read-bps</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit read rate from device (bytes per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-read-iops</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit read rate from device (IOPS)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-write-bps</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit write rate to device (bytes per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-write-iops</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit write rate to device (IOPS)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row960516596183"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p126061759201819"><a name="en-us_topic_0182207105_p126061759201819"></a><a name="en-us_topic_0182207105_p126061759201819"></a>--dns</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1560625917186"><a name="en-us_topic_0182207105_p1560625917186"></a><a name="en-us_topic_0182207105_p1560625917186"></a>Add DNS server</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row035317281915"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1735311218199"><a name="en-us_topic_0182207105_p1735311218199"></a><a name="en-us_topic_0182207105_p1735311218199"></a>--dns-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p935319217193"><a name="en-us_topic_0182207105_p935319217193"></a><a name="en-us_topic_0182207105_p935319217193"></a>Add DNS options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1345415571916"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19455250193"><a name="en-us_topic_0182207105_p19455250193"></a><a name="en-us_topic_0182207105_p19455250193"></a>--dns-search</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p204552531916"><a name="en-us_topic_0182207105_p204552531916"></a><a name="en-us_topic_0182207105_p204552531916"></a>Set the container's search domain</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16463212570"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1021516396713"><a name="en-us_topic_0182207105_p1021516396713"></a><a name="en-us_topic_0182207105_p1021516396713"></a>--entrypoint</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p421833918713"><a name="en-us_topic_0182207105_p421833918713"></a><a name="en-us_topic_0182207105_p421833918713"></a>Entrypoint to run when the container starts</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row173714521568"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p72051939470"><a name="en-us_topic_0182207105_p72051939470"></a><a name="en-us_topic_0182207105_p72051939470"></a>-e, --env</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p15209739476"><a name="en-us_topic_0182207105_p15209739476"></a><a name="en-us_topic_0182207105_p15209739476"></a>Set environment variables</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1453110523575"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8531185213573"><a name="en-us_topic_0182207105_p8531185213573"></a><a name="en-us_topic_0182207105_p8531185213573"></a>--env-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p20531052135713"><a name="en-us_topic_0182207105_p20531052135713"></a><a name="en-us_topic_0182207105_p20531052135713"></a>Configure environment variables from a file</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1453110523575"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8531185213573"><a name="en-us_topic_0182207105_p8531185213573"></a><a name="en-us_topic_0182207105_p8531185213573"></a>--env-target-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p20531052135713"><a name="en-us_topic_0182207105_p20531052135713"></a><a name="en-us_topic_0182207105_p20531052135713"></a>Export environment variables to the target file path in rootfs</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row197464191473"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p152241239276"><a name="en-us_topic_0182207105_p152241239276"></a><a name="en-us_topic_0182207105_p152241239276"></a>--external-rootfs=PATH</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p152288395712"><a name="en-us_topic_0182207105_p152288395712"></a><a name="en-us_topic_0182207105_p152288395712"></a>Specify a rootfs (can be a directory or block device) not managed by iSulad for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row9905848153714"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p371584910376"><a name="en-us_topic_0182207105_p371584910376"></a><a name="en-us_topic_0182207105_p371584910376"></a>--files-limit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19715749163711"><a name="en-us_topic_0182207105_p19715749163711"></a><a name="en-us_topic_0182207105_p19715749163711"></a>Adjust the number of file handles that can be opened within the container (-1 means no limit)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row6682753194610"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p971311443316"><a name="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p971311443316"></a><a name="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p971311443316"></a>--group-add=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p343520423515"><a name="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p343520423515"></a><a name="en-us_topic_0182207105_en-us_topic_0124544921_en-us_topic_0043209392_p343520423515"></a>Specify additional user groups to add to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row17428191317713"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p42336396714"><a name="en-us_topic_0182207105_p42336396714"></a><a name="en-us_topic_0182207105_p42336396714"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p823614398716"><a name="en-us_topic_0182207105_p823614398716"></a><a name="en-us_topic_0182207105_p823614398716"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row614972012483"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p61501220104817"><a name="en-us_topic_0182207105_p61501220104817"></a><a name="en-us_topic_0182207105_p61501220104817"></a>--health-cmd</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p191500208483"><a name="en-us_topic_0182207105_p191500208483"></a><a name="en-us_topic_0182207105_p191500208483"></a>Command to execute inside the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1280173244812"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p2028013325485"><a name="en-us_topic_0182207105_p2028013325485"></a><a name="en-us_topic_0182207105_p2028013325485"></a>--health-exit-on-unhealthy</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1928033213487"><a name="en-us_topic_0182207105_p1928033213487"></a><a name="en-us_topic_0182207105_p1928033213487"></a>Whether to kill the container when it is detected as unhealthy</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1039723584810"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1039711350489"><a name="en-us_topic_0182207105_p1039711350489"></a><a name="en-us_topic_0182207105_p1039711350489"></a>--health-interval</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p113971935134817"><a name="en-us_topic_0182207105_p113971935134817"></a><a name="en-us_topic_0182207105_p113971935134817"></a>Interval time between two consecutive command executions</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row104982394488"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1849953934818"><a name="en-us_topic_0182207105_p1849953934818"></a><a name="en-us_topic_0182207105_p1849953934818"></a>--health-retries</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12499173910484"><a name="en-us_topic_0182207105_p12499173910484"></a><a name="en-us_topic_0182207105_p12499173910484"></a>Maximum number of health check failures to retry</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row11177446154813"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11177114634819"><a name="en-us_topic_0182207105_p11177114634819"></a><a name="en-us_topic_0182207105_p11177114634819"></a>--health-start-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9177146184818"><a name="en-us_topic_0182207105_p9177146184818"></a><a name="en-us_topic_0182207105_p9177146184818"></a>Container initialization time</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1318252595020"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1118313259506"><a name="en-us_topic_0182207105_p1118313259506"></a><a name="en-us_topic_0182207105_p1118313259506"></a>--health-timeout</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1718342515503"><a name="en-us_topic_0182207105_p1718342515503"></a><a name="en-us_topic_0182207105_p1718342515503"></a>Upper time limit for a single check command execution</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1233115174718"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p142425395718"><a name="en-us_topic_0182207105_p142425395718"></a><a name="en-us_topic_0182207105_p142425395718"></a>--hook-spec</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p2247173913718"><a name="en-us_topic_0182207105_p2247173913718"></a><a name="en-us_topic_0182207105_p2247173913718"></a>Hook configuration file</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row841117457260"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p17569154712612"><a name="en-us_topic_0182207105_p17569154712612"></a><a name="en-us_topic_0182207105_p17569154712612"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p20572194752612"><a name="en-us_topic_0182207105_p20572194752612"></a><a name="en-us_topic_0182207105_p20572194752612"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row09098231714"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1125217390718"><a name="en-us_topic_0182207105_p1125217390718"></a><a name="en-us_topic_0182207105_p1125217390718"></a>--host-channel</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11255113910714"><a name="en-us_topic_0182207105_p11255113910714"></a><a name="en-us_topic_0182207105_p11255113910714"></a>Create shared memory between host and container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row09098231714"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1125217390718"><a name="en-us_topic_0182207105_p1125217390718"></a><a name="en-us_topic_0182207105_p1125217390718"></a>-h, --hostname</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11255113910714"><a name="en-us_topic_0182207105_p11255113910714"></a><a name="en-us_topic_0182207105_p11255113910714"></a>Container hostname</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row64315281478"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p326313393713"><a name="en-us_topic_0182207105_p326313393713"></a><a name="en-us_topic_0182207105_p326313393713"></a>--hugetlb-limit=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p182668394714"><a name="en-us_topic_0182207105_p182668394714"></a><a name="en-us_topic_0182207105_p182668394714"></a>Huge page file limit, e.g., --hugetlb-limit 2MB:32MB</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1857164385519"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324317539553"><a name="en-us_topic_0182207105_p324317539553"></a><a name="en-us_topic_0182207105_p324317539553"></a>-i, --interactive</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9243195320559"><a name="en-us_topic_0182207105_p9243195320559"></a><a name="en-us_topic_0182207105_p9243195320559"></a>Keep container's standard input open even if not attached</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1857164385519"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324317539553"><a name="en-us_topic_0182207105_p324317539553"></a><a name="en-us_topic_0182207105_p324317539553"></a>--ipc</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9243195320559"><a name="en-us_topic_0182207105_p9243195320559"></a><a name="en-us_topic_0182207105_p9243195320559"></a>IPC namespace to use</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1857164385519"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324317539553"><a name="en-us_topic_0182207105_p324317539553"></a><a name="en-us_topic_0182207105_p324317539553"></a>--kernel-memory</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9243195320559"><a name="en-us_topic_0182207105_p9243195320559"></a><a name="en-us_topic_0182207105_p9243195320559"></a>Kernel memory limit</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row10298153113371"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11298113113710"><a name="en-us_topic_0182207105_p11298113113710"></a><a name="en-us_topic_0182207105_p11298113113710"></a>-l, --label</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p15298143143711"><a name="en-us_topic_0182207105_p15298143143711"></a><a name="en-us_topic_0182207105_p15298143143711"></a>Set labels for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1753552953820"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p75351029113820"><a name="en-us_topic_0182207105_p75351029113820"></a><a name="en-us_topic_0182207105_p75351029113820"></a>--label-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8535122916381"><a name="en-us_topic_0182207105_p8535122916381"></a><a name="en-us_topic_0182207105_p8535122916381"></a>Set container labels from a file</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1753552953820"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p75351029113820"><a name="en-us_topic_0182207105_p75351029113820"></a><a name="en-us_topic_0182207105_p75351029113820"></a>--log-driver</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8535122916381"><a name="en-us_topic_0182207105_p8535122916381"></a><a name="en-us_topic_0182207105_p8535122916381"></a>Log driver for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1292919294714"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p132831239572"><a name="en-us_topic_0182207105_p132831239572"></a><a name="en-us_topic_0182207105_p132831239572"></a>--log-opt=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p2028510390711"><a name="en-us_topic_0182207105_p2028510390711"></a><a name="en-us_topic_0182207105_p2028510390711"></a>Log driver options, logging of container serial console is disabled by default, it can be enabled via "--log-opt disable-log=false".</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1676892518712"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p629323915710"><a name="en-us_topic_0182207105_p629323915710"></a><a name="en-us_topic_0182207105_p629323915710"></a>-m, --memory</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p122954399719"><a name="en-us_topic_0182207105_p122954399719"></a><a name="en-us_topic_0182207105_p122954399719"></a>Memory limit</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row601514193211"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_en-us_topic_0138971318_p11811595428"><a name="en-us_topic_0182207105_en-us_topic_0138971318_p11811595428"></a><a name="en-us_topic_0182207105_en-us_topic_0138971318_p11811595428"></a>--memory-reservation</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_en-us_topic_0138971318_p21815598424"><a name="en-us_topic_0182207105_en-us_topic_0138971318_p21815598424"></a><a name="en-us_topic_0182207105_en-us_topic_0138971318_p21815598424"></a>Set container memory limit, the default is the same as --memory. --memory can be considered a hard limit, and --memory-reservation a soft limit; when memory usage exceeds the preset value, it will be dynamically adjusted (the system attempts to reduce memory usage below the preset value when reclaiming memory), but it is not guaranteed to stay below the preset value. It can generally be used with --memory, with a value less than the preset value of --memory, minimum 4MB.</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1052344477"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1930383914714"><a name="en-us_topic_0182207105_p1930383914714"></a><a name="en-us_topic_0182207105_p1930383914714"></a>--memory-swap</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p203051539579"><a name="en-us_topic_0182207105_p203051539579"></a><a name="en-us_topic_0182207105_p203051539579"></a>Positive integer, Memory + Swap space, -1 means no limit</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1728751718149"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p18287417161414"><a name="en-us_topic_0182207105_p18287417161414"></a><a name="en-us_topic_0182207105_p18287417161414"></a>--memory-swappiness</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p15287111731410"><a name="en-us_topic_0182207105_p15287111731410"></a><a name="en-us_topic_0182207105_p15287111731410"></a>Positive integer, swappiness parameter value can be set between 0 and 100. A lower value makes the Linux system use less swap partition and more memory; a higher value does the opposite, making the kernel use more swap space. The default value is -1, meaning use the system default.</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row154751863710"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p7312539679"><a name="en-us_topic_0182207105_p7312539679"></a><a name="en-us_topic_0182207105_p7312539679"></a>--mount</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p183152391174"><a name="en-us_topic_0182207105_p183152391174"></a><a name="en-us_topic_0182207105_p183152391174"></a>Mount host directory/volume/filesystem into the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row8679175615614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p16321113910720"><a name="en-us_topic_0182207105_p16321113910720"></a><a name="en-us_topic_0182207105_p16321113910720"></a>--name=NAME</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p163231391675"><a name="en-us_topic_0182207105_p163231391675"></a><a name="en-us_topic_0182207105_p163231391675"></a>Container name</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row19100528719"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1033216391775"><a name="en-us_topic_0182207105_p1033216391775"></a><a name="en-us_topic_0182207105_p1033216391775"></a>--net=none</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1633611391076"><a name="en-us_topic_0182207105_p1633611391076"></a><a name="en-us_topic_0182207105_p1633611391076"></a>Connect container to network</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--no-healthcheck</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Disable health check configuration</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--ns-change-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Namespace kernel parameter options for system containers</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--oom-kill-disable</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Disable OOM</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--oom-score-adj</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Adjust host OOM preference settings (-1000 to 1000)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--pid</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>PID namespace to use</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row10108143810"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p17982489384"><a name="en-us_topic_0182207105_p17982489384"></a><a name="en-us_topic_0182207105_p17982489384"></a>--pids-limit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12982587385"><a name="en-us_topic_0182207105_p12982587385"></a><a name="en-us_topic_0182207105_p12982587385"></a>Adjust the number of processes that can be executed within the container (-1 means no limit)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row204644595611"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8346153919718"><a name="en-us_topic_0182207105_p8346153919718"></a><a name="en-us_topic_0182207105_p8346153919718"></a>--privileged</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p10349123910710"><a name="en-us_topic_0182207105_p10349123910710"></a><a name="en-us_topic_0182207105_p10349123910710"></a>Give extended privileges to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row204644595611"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8346153919718"><a name="en-us_topic_0182207105_p8346153919718"></a><a name="en-us_topic_0182207105_p8346153919718"></a>--pull</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p10349123910710"><a name="en-us_topic_0182207105_p10349123910710"></a><a name="en-us_topic_0182207105_p10349123910710"></a>Pull image before running</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row4715417611"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p93596391276"><a name="en-us_topic_0182207105_p93596391276"></a><a name="en-us_topic_0182207105_p93596391276"></a>-R, --runtime</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1436203919713"><a name="en-us_topic_0182207105_p1436203919713"></a><a name="en-us_topic_0182207105_p1436203919713"></a>Container runtime, parameter supports "lcr", case-insensitive, so "LCR" and "lcr" are equivalent.</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row9631144512610"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1837363910713"><a name="en-us_topic_0182207105_p1837363910713"></a><a name="en-us_topic_0182207105_p1837363910713"></a>--read-only</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11378103915718"><a name="en-us_topic_0182207105_p11378103915718"></a><a name="en-us_topic_0182207105_p11378103915718"></a>Set the container's root filesystem to read-only</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row111022509616"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1538418391715"><a name="en-us_topic_0182207105_p1538418391715"></a><a name="en-us_topic_0182207105_p1538418391715"></a>--restart</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p193871391976"><a name="en-us_topic_0182207105_p193871391976"></a><a name="en-us_topic_0182207105_p193871391976"></a>Restart policy when container exits</p>
<p id="en-us_topic_0182207105_p1371141235411"><a name="en-us_topic_0182207105_p1371141235411"></a><a name="en-us_topic_0182207105_p1371141235411"></a>System containers support --restart on-reboot</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--security-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Security options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--shm-size</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Size of /dev/shm, default value is 64MB</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--stop-signal</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Signal to stop container, default is SIGTERM</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--storage-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Configure storage driver options for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--sysctl</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Set sysctl options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--system-container</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Start system container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row19571175416574"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p35093214585"><a name="en-us_topic_0182207105_p35093214585"></a><a name="en-us_topic_0182207105_p35093214585"></a>--tmpfs</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p750913265817"><a name="en-us_topic_0182207105_p750913265817"></a><a name="en-us_topic_0182207105_p750913265817"></a>Mount tmpfs directory</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row19571175416574"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p35093214585"><a name="en-us_topic_0182207105_p35093214585"></a><a name="en-us_topic_0182207105_p35093214585"></a>-t, --tty</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p750913265817"><a name="en-us_topic_0182207105_p750913265817"></a><a name="en-us_topic_0182207105_p750913265817"></a>Allocate a pseudo-TTY</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--ulimit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Set ulimit limits for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row26709251165"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p2408193911715"><a name="en-us_topic_0182207105_p2408193911715"></a><a name="en-us_topic_0182207105_p2408193911715"></a>-u, --user</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p2041110391273"><a name="en-us_topic_0182207105_p2041110391273"></a><a name="en-us_topic_0182207105_p2041110391273"></a>Username or UID, format [&amp;lt;name|uid&amp;gt;][:&amp;lt;group|gid&amp;gt;]</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--user-remap</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Map user to container (for system containers)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--userns</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Set user namespace for the container when enabling 'user-remap' option</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--uts</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Set PID namespace</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row969873217614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1443220391575"><a name="en-us_topic_0182207105_p1443220391575"></a><a name="en-us_topic_0182207105_p1443220391575"></a>-v, --volume=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p343617396718"><a name="en-us_topic_0182207105_p343617396718"></a><a name="en-us_topic_0182207105_p343617396718"></a>Mount a volume</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row969873217614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1443220391575"><a name="en-us_topic_0182207105_p1443220391575"></a><a name="en-us_topic_0182207105_p1443220391575"></a>--volumes-from=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p343617396718"><a name="en-us_topic_0182207105_p343617396718"></a><a name="en-us_topic_0182207105_p343617396718"></a>Use mount configuration from specified container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row969873217614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1443220391575"><a name="en-us_topic_0182207105_p1443220391575"></a><a name="en-us_topic_0182207105_p1443220391575"></a>--workdir</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p343617396718"><a name="en-us_topic_0182207105_p343617396718"></a><a name="en-us_topic_0182207105_p343617396718"></a>Set working directory inside container</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- When the  **--user**  or  **--group-add**  parameter is used to verify the user or group during container startup, if the container uses an OCI image, the verification is performed in the  **etc/passwd**  and  **etc/group**  files of the actual rootfs of the image. If a folder or block device is used as the rootfs of the container, the  **etc/passwd**  and  **etc/group**  files in the host are verified. The rootfs ignores mounting parameters such as  **-v**  and  **--mount**. That is, when these parameters are used to attempt to overwrite the  **etc/passwd**  and  **etc/group**  files, the parameters do not take effect during the search and take effect only when the container is started. The generated configuration is saved in the  **iSulad root directory/engine/container ID/start\_generate\_config.json**  file. The file format is as follows:

    ```json
    {
        "uid": 0,
        "gid": 8,
        "additionalGids": [
            1234,
            8
        ]
    }
    ```

### Example

Create a container.

```shell
$ isula create busybox
fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
$ isula ps -a
STATUS PID IMAGE   COMMAND EXIT_CODE RESTART_COUNT STARTAT FINISHAT RUNTIME ID           NAMES                                                            inited -   busybox "sh"    0         0             -       -        lcr     fd7376591a9c fd7376591a9c4521...
```

## Starting a Container

### Description

To start one or more containers, run the  **isula start**  command.

### Usage

```shell
isula start [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **start**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0182207106_table279824718555"></a>
<table>
<tbody>
<tr id="en-us_topic_0182207106_row224115355713">
<td class="cellrowborder" valign="top" width="17.333333333333336%">
<p id="en-us_topic_0182207106_p447450105817"><a name="en-us_topic_0182207106_p447450105817"></a><a name="en-us_topic_0182207106_p447450105817"></a><strong id="en-us_topic_0182207106_b1347410105817"><a name="en-us_topic_0182207106_b1347410105817"></a><a name="en-us_topic_0182207106_b1347410105817"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%">
<p id="en-us_topic_0182207106_p24741801581"><a name="en-us_topic_0182207106_p24741801581"></a><a name="en-us_topic_0182207106_p24741801581"></a><strong id="en-us_topic_0182207106_b164747015586"><a name="en-us_topic_0182207106_b164747015586"></a><a name="en-us_topic_0182207106_b164747015586"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%">
<p id="en-us_topic_0182207106_p547411015820"><a name="en-us_topic_0182207106_p547411015820"></a><a name="en-us_topic_0182207106_p547411015820"></a><strong id="en-us_topic_0182207106_b1647430185815"><a name="en-us_topic_0182207106_b1647430185815"></a><a name="en-us_topic_0182207106_b1647430185815"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0182207106_row177619332245">
<td class="cellrowborder" rowspan="4" valign="top" width="17.333333333333336%">
<p id="en-us_topic_0182207106_p108381258112215"><a name="en-us_topic_0182207106_p108381258112215"></a><a name="en-us_topic_0182207106_p108381258112215"></a><strong id="en-us_topic_0182207106_b3709195112316"><a name="en-us_topic_0182207106_b3709195112316"></a><a name="en-us_topic_0182207106_b3709195112316"></a>start</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%">
<p id="en-us_topic_0182207106_p1977623312410"><a name="en-us_topic_0182207106_p1977623312410"></a><a name="en-us_topic_0182207106_p1977623312410"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%">
<p id="en-us_topic_0182207106_p577673362410"><a name="en-us_topic_0182207106_p577673362410"></a><a name="en-us_topic_0182207106_p577673362410"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0182207106_p207603617248"></a><a name="en-us_topic_0182207106_p207603617248"></a>-a, --attach</p>
</td>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0182207106_p176218616242"></a><a name="en-us_topic_0182207106_p176218616242"></a>Attach to container's STDOUT and STDERR</p>
</td>
</tr>
<tr>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top">
<p><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Example

Start a new container.

```shell
isula start fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
```

## Running a Container

### Description

To create and start a container, run the  **isula run**  command. You can use a specified container image to create a container read/write layer and prepare for running the specified command. After the container is created, run the specified command to start the container. The  **run**  command is equivalent to creating and starting a container.

### Usage

```shell
isula run [OPTIONS] ROOTFS|IMAGE [COMMAND] [ARG...]
```

### Parameters

The following table lists the parameters supported by the  **run**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0182207107_table62441570237"></a>
<table><tbody><tr id="en-us_topic_0182207107_row139736211246"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0182207107_p148610405244"><a name="en-us_topic_0182207107_p148610405244"></a><a name="en-us_topic_0182207107_p148610405244"></a><strong id="en-us_topic_0182207107_b5486144014247"><a name="en-us_topic_0182207107_b5486144014247"></a><a name="en-us_topic_0182207107_b5486144014247"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0182207107_p048644010248"><a name="en-us_topic_0182207107_p048644010248"></a><a name="en-us_topic_0182207107_p048644010248"></a><strong id="en-us_topic_0182207107_b748616402241"><a name="en-us_topic_0182207107_b748616402241"></a><a name="en-us_topic_0182207107_b748616402241"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0182207107_p648624042417"><a name="en-us_topic_0182207107_p648624042417"></a><a name="en-us_topic_0182207107_p648624042417"></a><strong id="en-us_topic_0182207107_b748619403240"><a name="en-us_topic_0182207107_b748619403240"></a><a name="en-us_topic_0182207107_b748619403240"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row134199513352"><td class="cellrowborder" rowspan="86" valign="top" width="17.333333333333336%"><p id="en-us_topic_0182207107_p1668419095711"><a name="en-us_topic_0182207107_p1668419095711"></a><a name="en-us_topic_0182207107_p1668419095711"></a><strong id="en-us_topic_0182207107_b479810255419"><a name="en-us_topic_0182207107_b479810255419"></a><a name="en-us_topic_0182207107_b479810255419"></a>run</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0182207107_p8129151463514"><a name="en-us_topic_0182207107_p8129151463514"></a><a name="en-us_topic_0182207107_p8129151463514"></a>--annotation</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0182207107_p5129191418354"><a name="en-us_topic_0182207107_p5129191418354"></a><a name="en-us_topic_0182207107_p5129191418354"></a>Set container annotations. For example, support the native.umask option:</p>
<pre class="screen" id="en-us_topic_0182207107_screen1112917145352"><a name="en-us_topic_0182207107_screen1112917145352"></a><a name="en-us_topic_0182207107_screen1112917145352"></a>--annotation native.umask=normal # The umask value of the started container is 0022
--annotation native.umask=secure # The umask value of the started container is 0027</pre>
<p id="en-us_topic_0182207107_p10129314183518"><a name="en-us_topic_0182207107_p10129314183518"></a><a name="en-us_topic_0182207107_p10129314183518"></a>Note that if this parameter is not configured, the umask configuration in isulad will be used.</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row861311411819"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1716101018113"><a name="en-us_topic_0182207107_p1716101018113"></a><a name="en-us_topic_0182207107_p1716101018113"></a>--add-host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p17421752153311"><a name="en-us_topic_0182207107_p17421752153311"></a><a name="en-us_topic_0182207107_p17421752153311"></a>Add a custom host-to-IP mapping (host:ip)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--blkio-weight</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Block IO (relative weight), between 10 and 1000, or 0 to disable (default is 0)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row7680255217"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p522218401851"><a name="en-us_topic_0182207105_p522218401851"></a><a name="en-us_topic_0182207105_p522218401851"></a>--blkio-weight-device</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1222414019518"><a name="en-us_topic_0182207105_p1222414019518"></a><a name="en-us_topic_0182207105_p1222414019518"></a>Block IO weight (relative device weight), format: DEVICE_NAME: weight, weight value is between 10 and 1000, or 0 to disable (default 0)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row861311411819"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1716101018113"><a name="en-us_topic_0182207107_p1716101018113"></a><a name="en-us_topic_0182207107_p1716101018113"></a>--cap-add</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p17421752153311"><a name="en-us_topic_0182207107_p17421752153311"></a><a name="en-us_topic_0182207107_p17421752153311"></a>Add Linux capabilities</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row17870171515015"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p38709151502"><a name="en-us_topic_0182207107_p38709151502"></a><a name="en-us_topic_0182207107_p38709151502"></a>--cap-drop</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p96851021937"><a name="en-us_topic_0182207107_p96851021937"></a><a name="en-us_topic_0182207107_p96851021937"></a>Drop Linux capabilities</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row429165541015"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p12412155631016"><a name="en-us_topic_0182207107_p12412155631016"></a><a name="en-us_topic_0182207107_p12412155631016"></a>--cgroup-parent</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p2412156151014"><a name="en-us_topic_0182207107_p2412156151014"></a><a name="en-us_topic_0182207107_p2412156151014"></a>Specify the container cgroup parent path</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU CFS (Completely Fair Scheduler) period</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-quota</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU CFS (Completely Fair Scheduler) quota</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-rt-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU real-time period (in microseconds)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row511418111746"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p124434019510"><a name="en-us_topic_0182207105_p124434019510"></a><a name="en-us_topic_0182207105_p124434019510"></a>--cpu-rt-runtime</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324519401555"><a name="en-us_topic_0182207105_p324519401555"></a><a name="en-us_topic_0182207105_p324519401555"></a>Limit CPU real-time runtime (in microseconds)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row17941113011010"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p794114304016"><a name="en-us_topic_0182207107_p794114304016"></a><a name="en-us_topic_0182207107_p794114304016"></a>--cpu-shares</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p468516214314"><a name="en-us_topic_0182207107_p468516214314"></a><a name="en-us_topic_0182207107_p468516214314"></a>CPU shares (relative weight)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpus</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>Number of CPUs</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpuset-cpus</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>CPUs allowed to execute (e.g. 0-3, 0, 1)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row136971311725"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p023010400516"><a name="en-us_topic_0182207105_p023010400516"></a><a name="en-us_topic_0182207105_p023010400516"></a>--cpuset-mems</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p32320401756"><a name="en-us_topic_0182207105_p32320401756"></a><a name="en-us_topic_0182207105_p32320401756"></a>Memory nodes allowed to execute (0-3, 0, 1)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row176131541687"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p116131041289"><a name="en-us_topic_0182207107_p116131041289"></a><a name="en-us_topic_0182207107_p116131041289"></a>-d, --detach</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p26851321335"><a name="en-us_topic_0182207107_p26851321335"></a><a name="en-us_topic_0182207107_p26851321335"></a>Run container in background and print container ID</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1061354115812"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p206133411080"><a name="en-us_topic_0182207107_p206133411080"></a><a name="en-us_topic_0182207107_p206133411080"></a>--device=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p5861121218270"><a name="en-us_topic_0182207107_p5861121218270"></a><a name="en-us_topic_0182207107_p5861121218270"></a>Add a host device to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-cgroup-rule</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Add a rule to the cgroup allowed device list</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-read-bps</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit read rate from device (bytes per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-read-iops</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit read rate from device (IO per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-write-bps</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit write rate to device (bytes per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1898442169"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8194739375"><a name="en-us_topic_0182207105_p8194739375"></a><a name="en-us_topic_0182207105_p8194739375"></a>--device-write-iops</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p19196339574"><a name="en-us_topic_0182207105_p19196339574"></a><a name="en-us_topic_0182207105_p19196339574"></a>Limit write rate to device (IO per second)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row623119489243"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p15231148132418"><a name="en-us_topic_0182207107_p15231148132418"></a><a name="en-us_topic_0182207107_p15231148132418"></a>--dns</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p123110486245"><a name="en-us_topic_0182207107_p123110486245"></a><a name="en-us_topic_0182207107_p123110486245"></a>Add DNS server</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row7357105142411"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p15357195116248"><a name="en-us_topic_0182207107_p15357195116248"></a><a name="en-us_topic_0182207107_p15357195116248"></a>--dns-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p735775132419"><a name="en-us_topic_0182207107_p735775132419"></a><a name="en-us_topic_0182207107_p735775132419"></a>Add DNS options</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row15443154132410"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1544335492417"><a name="en-us_topic_0182207107_p1544335492417"></a><a name="en-us_topic_0182207107_p1544335492417"></a>--dns-search</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1443165472412"><a name="en-us_topic_0182207107_p1443165472412"></a><a name="en-us_topic_0182207107_p1443165472412"></a>Set container search domains</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16463212570"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1021516396713"><a name="en-us_topic_0182207105_p1021516396713"></a><a name="en-us_topic_0182207105_p1021516396713"></a>--entrypoint</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p421833918713"><a name="en-us_topic_0182207105_p421833918713"></a><a name="en-us_topic_0182207105_p421833918713"></a>The entrypoint for the container when starting</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row156137414817"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1261417415811"><a name="en-us_topic_0182207107_p1261417415811"></a><a name="en-us_topic_0182207107_p1261417415811"></a>-e, --env</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p176852211639"><a name="en-us_topic_0182207107_p176852211639"></a><a name="en-us_topic_0182207107_p176852211639"></a>Set environment variables</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row161909508118"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p6191135020112"><a name="en-us_topic_0182207107_p6191135020112"></a><a name="en-us_topic_0182207107_p6191135020112"></a>--env-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p101911950112"><a name="en-us_topic_0182207107_p101911950112"></a><a name="en-us_topic_0182207107_p101911950112"></a>Configure environment variables from a file</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1453110523575"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8531185213573"><a name="en-us_topic_0182207105_p8531185213573"></a><a name="en-us_topic_0182207105_p8531185213573"></a>--env-target-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p20531052135713"><a name="en-us_topic_0182207105_p20531052135713"></a><a name="en-us_topic_0182207105_p20531052135713"></a>Target file path in rootfs to export environment variables</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row84421230185918"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p24421330125913"><a name="en-us_topic_0182207107_p24421330125913"></a><a name="en-us_topic_0182207107_p24421330125913"></a>--external-rootfs=PATH</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p176851721939"><a name="en-us_topic_0182207107_p176851721939"></a><a name="en-us_topic_0182207107_p176851721939"></a>Specify a rootfs not managed by iSulad (can be a directory or block device) for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207108_row244213301259"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207108_p26851721939"><a name="en-us_topic_0182207108_p26851721939"></a><a name="en-us_topic_0182207108_p26851721939"></a>--files-limit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207108_p176851721939"><a name="en-us_topic_0182207108_p176851721939"></a><a name="en-us_topic_0182207108_p176851721939"></a>Adjust the number of file handles that can be opened inside the container (-1 means unlimited)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1295325111472"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p20395344714"><a name="en-us_topic_0182207107_p20395344714"></a><a name="en-us_topic_0182207107_p20395344714"></a>--group-add=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p2365313470"><a name="en-us_topic_0182207107_p2365313470"></a><a name="en-us_topic_0182207107_p2365313470"></a>Specify additional user groups to add to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row49051865195"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p16905146161917"><a name="en-us_topic_0182207107_p16905146161917"></a><a name="en-us_topic_0182207107_p16905146161917"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1690512618195"><a name="en-us_topic_0182207107_p1690512618195"></a><a name="en-us_topic_0182207107_p1690512618195"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1863011175146"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1063041731417"><a name="en-us_topic_0182207107_p1063041731417"></a><a name="en-us_topic_0182207107_p1063041731417"></a>--health-cmd</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p18630517191411"><a name="en-us_topic_0182207107_p18630517191411"></a><a name="en-us_topic_0182207107_p18630517191411"></a>Command to execute inside the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row753412041411"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p11535132013142"><a name="en-us_topic_0182207107_p11535132013142"></a><a name="en-us_topic_0182207107_p11535132013142"></a>--health-exit-on-unhealthy</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p0535152041412"><a name="en-us_topic_0182207107_p0535152041412"></a><a name="en-us_topic_0182207107_p0535152041412"></a>Kill container if unhealthy is detected</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row17173192319142"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p91733234142"><a name="en-us_topic_0182207107_p91733234142"></a><a name="en-us_topic_0182207107_p91733234142"></a>--health-interval</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p217320238146"><a name="en-us_topic_0182207107_p217320238146"></a><a name="en-us_topic_0182207107_p217320238146"></a>Time between consecutive command executions</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row65618261149"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p55612611410"><a name="en-us_topic_0182207107_p55612611410"></a><a name="en-us_topic_0182207107_p55612611410"></a>--health-retries</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p205619268141"><a name="en-us_topic_0182207107_p205619268141"></a><a name="en-us_topic_0182207107_p205619268141"></a>Maximum number of retries for failed health check</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row6356102941410"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1835612991419"><a name="en-us_topic_0182207107_p1835612991419"></a><a name="en-us_topic_0182207107_p1835612991419"></a>--health-start-period</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p93568290147"><a name="en-us_topic_0182207107_p93568290147"></a><a name="en-us_topic_0182207107_p93568290147"></a>Container initialization time</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1029384718146"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p16294154716147"><a name="en-us_topic_0182207107_p16294154716147"></a><a name="en-us_topic_0182207107_p16294154716147"></a>--health-timeout</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p142942047201411"><a name="en-us_topic_0182207107_p142942047201411"></a><a name="en-us_topic_0182207107_p142942047201411"></a>Execution time limit for a single check command</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row417113495919"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p15172183445920"><a name="en-us_topic_0182207107_p15172183445920"></a><a name="en-us_topic_0182207107_p15172183445920"></a>--hook-spec</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p8685112118314"><a name="en-us_topic_0182207107_p8685112118314"></a><a name="en-us_topic_0182207107_p8685112118314"></a>Hook configuration file</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1498202319272"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p9571162842711"><a name="en-us_topic_0182207107_p9571162842711"></a><a name="en-us_topic_0182207107_p9571162842711"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1157482818273"><a name="en-us_topic_0182207107_p1157482818273"></a><a name="en-us_topic_0182207107_p1157482818273"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row09098231714"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1125217390718"><a name="en-us_topic_0182207105_p1125217390718"></a><a name="en-us_topic_0182207105_p1125217390718"></a>--host-channel</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11255113910714"><a name="en-us_topic_0182207105_p11255113910714"></a><a name="en-us_topic_0182207105_p11255113910714"></a>Create shared memory between host and container</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row6362153610268"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p13621736192618"><a name="en-us_topic_0182207107_p13621736192618"></a><a name="en-us_topic_0182207107_p13621736192618"></a>-h, --hostname</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p103621036122610"><a name="en-us_topic_0182207107_p103621036122610"></a><a name="en-us_topic_0182207107_p103621036122610"></a>Container hostname</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row144214385598"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1144213389599"><a name="en-us_topic_0182207107_p1144213389599"></a><a name="en-us_topic_0182207107_p1144213389599"></a>--hugetlb-limit=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p268516211335"><a name="en-us_topic_0182207107_p268516211335"></a><a name="en-us_topic_0182207107_p268516211335"></a>Hugepage limit, e.g.: --hugetlb-limit 2MB:32MB</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row205911371908"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1059163713014"><a name="en-us_topic_0182207107_p1059163713014"></a><a name="en-us_topic_0182207107_p1059163713014"></a>-i, --interactive</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p158943505"><a name="en-us_topic_0182207107_p158943505"></a><a name="en-us_topic_0182207107_p158943505"></a>Keep STDIN open even if not attached</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1857164385519"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324317539553"><a name="en-us_topic_0182207105_p324317539553"></a><a name="en-us_topic_0182207105_p324317539553"></a>--ipc</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9243195320559"><a name="en-us_topic_0182207105_p9243195320559"></a><a name="en-us_topic_0182207105_p9243195320559"></a>IPC namespace usage</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1857164385519"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p324317539553"><a name="en-us_topic_0182207105_p324317539553"></a><a name="en-us_topic_0182207105_p324317539553"></a>--kernel-memory</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p9243195320559"><a name="en-us_topic_0182207105_p9243195320559"></a><a name="en-us_topic_0182207105_p9243195320559"></a>Kernel memory limit</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row10298153113371"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11298113113710"><a name="en-us_topic_0182207105_p11298113113710"></a><a name="en-us_topic_0182207105_p11298113113710"></a>-l, --label</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p15298143143711"><a name="en-us_topic_0182207105_p15298143143711"></a><a name="en-us_topic_0182207105_p15298143143711"></a>Set metadata on a container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row1753552953820"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p75351029113820"><a name="en-us_topic_0182207105_p75351029113820"></a><a name="en-us_topic_0182207105_p75351029113820"></a>--label-file</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8535122916381"><a name="en-us_topic_0182207105_p8535122916381"></a><a name="en-us_topic_0182207105_p8535122916381"></a>Set container labels from a file</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row659103717013"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p8599371505"><a name="en-us_topic_0182207107_p8599371505"></a><a name="en-us_topic_0182207107_p8599371505"></a>--log-driver</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p668514211339"><a name="en-us_topic_0182207107_p668514211339"></a><a name="en-us_topic_0182207107_p668514211339"></a>Set log driver, supports syslog and json-file.</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row659103717013"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p8599371505"><a name="en-us_topic_0182207107_p8599371505"></a><a name="en-us_topic_0182207107_p8599371505"></a>--log-opt=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p668514211339"><a name="en-us_topic_0182207107_p668514211339"></a><a name="en-us_topic_0182207107_p668514211339"></a>Log driver options, logging container serial port function is disabled by default, you can enable it with "--log-opt disable-log=false".</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row75913717012"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p175918371019"><a name="en-us_topic_0182207107_p175918371019"></a><a name="en-us_topic_0182207107_p175918371019"></a>-m, --memory</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p156851211039"><a name="en-us_topic_0182207107_p156851211039"></a><a name="en-us_topic_0182207107_p156851211039"></a>Memory limit</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row10796185703219"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p3692125919328"><a name="en-us_topic_0182207107_p3692125919328"></a><a name="en-us_topic_0182207107_p3692125919328"></a>--memory-reservation</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p12693185913322"><a name="en-us_topic_0182207107_p12693185913322"></a><a name="en-us_topic_0182207107_p12693185913322"></a>Set memory soft limit, default is the same as --memory. --memory is considered a hard limit, --memory-reservation is a soft limit; when memory usage exceeds the preset value, it will be dynamically adjusted (the system tries to reduce memory usage below the preset value when reclaiming memory), but it is not guaranteed that it will not exceed the preset value. It can generally be used with --memory, with a value less than the preset value of --memory, and a minimum setting of 4MB.</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row20593371607"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p12592371704"><a name="en-us_topic_0182207107_p12592371704"></a><a name="en-us_topic_0182207107_p12592371704"></a>--memory-swap</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p15685521736"><a name="en-us_topic_0182207107_p15685521736"></a><a name="en-us_topic_0182207107_p15685521736"></a>Positive integer, memory + swap space, -1 means unlimited</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row18121147112914"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p18287417161414"><a name="en-us_topic_0182207107_p18287417161414"></a><a name="en-us_topic_0182207107_p18287417161414"></a>--memory-swappiness</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p101221378297"><a name="en-us_topic_0182207107_p101221378297"></a><a name="en-us_topic_0182207107_p101221378297"></a>Positive integer, swappiness parameter value can be set between 0 and 100. The lower the parameter value, the less the Linux system will use swap partitions and the more it will use memory; the higher the parameter value, the opposite is true, making the kernel use more swap space, the default value is -1, which means using the system default value.</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row53314518493"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p134145154916"><a name="en-us_topic_0182207107_p134145154916"></a><a name="en-us_topic_0182207107_p134145154916"></a>--mount</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p968518211831"><a name="en-us_topic_0182207107_p968518211831"></a><a name="en-us_topic_0182207107_p968518211831"></a>Mount a host directory into the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row17591371014"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p19601237408"><a name="en-us_topic_0182207107_p19601237408"></a><a name="en-us_topic_0182207107_p19601237408"></a>--name=NAME</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p206851721434"><a name="en-us_topic_0182207107_p206851721434"></a><a name="en-us_topic_0182207107_p206851721434"></a>Container name</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row56017376010"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p17601537306"><a name="en-us_topic_0182207107_p17601537306"></a><a name="en-us_topic_0182207107_p17601537306"></a>--net=none</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p86855212031"><a name="en-us_topic_0182207107_p86855212031"></a><a name="en-us_topic_0182207107_p86855212031"></a>Connect container to network</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row206012104181"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p196011710151815"><a name="en-us_topic_0182207107_p196011710151815"></a><a name="en-us_topic_0182207107_p196011710151815"></a>--no-healthcheck</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p146011610121814"><a name="en-us_topic_0182207107_p146011610121814"></a><a name="en-us_topic_0182207107_p146011610121814"></a>Disable healthcheck configuration</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--ns-change-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Namespace kernel parameter options for system containers</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--oom-kill-disable</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Disable OOM (Out-of-Memory) killer</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--oom-score-adj</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>Adjust host's OOM preference setting (-1000 to 1000)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row565519595210"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p12655457526"><a name="en-us_topic_0182207105_p12655457526"></a><a name="en-us_topic_0182207105_p12655457526"></a>--pid</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p765517511527"><a name="en-us_topic_0182207105_p765517511527"></a><a name="en-us_topic_0182207105_p765517511527"></a>PID namespace to use</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1442163033611"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p14422173013363"><a name="en-us_topic_0182207107_p14422173013363"></a><a name="en-us_topic_0182207107_p14422173013363"></a>--pids-limit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p8869114683618"><a name="en-us_topic_0182207107_p8869114683618"></a><a name="en-us_topic_0182207107_p8869114683618"></a>Adjust the number of processes that can be executed inside the container (-1 means unlimited)</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row11605371201"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p196012371304"><a name="en-us_topic_0182207107_p196012371304"></a><a name="en-us_topic_0182207107_p196012371304"></a>--privileged</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p968516212319"><a name="en-us_topic_0182207107_p968516212319"></a><a name="en-us_topic_0182207107_p968516212319"></a>Give extended privileges to the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row204644595611"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p8346153919718"><a name="en-us_topic_0182207105_p8346153919718"></a><a name="en-us_topic_0182207105_p8346153919718"></a>--pull</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p10349123910710"><a name="en-us_topic_0182207105_p10349123910710"></a><a name="en-us_topic_0182207105_p10349123910710"></a>Pull image before running</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row10649172419178"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1464912421718"><a name="en-us_topic_0182207107_p1464912421718"></a><a name="en-us_topic_0182207107_p1464912421718"></a>-R, --runtime</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p186853211837"><a name="en-us_topic_0182207107_p186853211837"></a><a name="en-us_topic_0182207107_p186853211837"></a>Container runtime, parameter supports "lcr", case-insensitive, so "LCR" and "lcr" are equivalent</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row151954516154"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p319705161516"><a name="en-us_topic_0182207107_p319705161516"></a><a name="en-us_topic_0182207107_p319705161516"></a>--read-only</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p819713551519"><a name="en-us_topic_0182207107_p819713551519"></a><a name="en-us_topic_0182207107_p819713551519"></a>Set container's root filesystem as read-only</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row3601237402"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p36013375013"><a name="en-us_topic_0182207107_p36013375013"></a><a name="en-us_topic_0182207107_p36013375013"></a>--restart</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p46863217311"><a name="en-us_topic_0182207107_p46863217311"></a><a name="en-us_topic_0182207107_p46863217311"></a>Restart policy when container exits</p>
<p id="en-us_topic_0182207107_p51198252521"><a name="en-us_topic_0182207107_p51198252521"></a><a name="en-us_topic_0182207107_p51198252521"></a>System containers support --restart on-reboot</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row83001819192212"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1301131911225"><a name="en-us_topic_0182207107_p1301131911225"></a><a name="en-us_topic_0182207107_p1301131911225"></a>--rm</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p2301819192212"><a name="en-us_topic_0182207107_p2301819192212"></a><a name="en-us_topic_0182207107_p2301819192212"></a>Automatically clean up container when it exits</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--security-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Security options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--shm-size</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Size of /dev/shm, default is 64MB</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--stop-signal</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Signal to stop container, defaults to SIGTERM</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--storage-opt</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Configure container storage driver options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--sysctl</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Set sysctl options</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row16393140174"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p26411214161716"><a name="en-us_topic_0182207105_p26411214161716"></a><a name="en-us_topic_0182207105_p26411214161716"></a>--system-container</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p156411614201714"><a name="en-us_topic_0182207105_p156411614201714"></a><a name="en-us_topic_0182207105_p156411614201714"></a>Start system container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row19571175416574"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p35093214585"><a name="en-us_topic_0182207105_p35093214585"></a><a name="en-us_topic_0182207105_p35093214585"></a>--tmpfs</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p750913265817"><a name="en-us_topic_0182207105_p750913265817"></a><a name="en-us_topic_0182207105_p750913265817"></a>Mount tmpfs directory</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row1160183710015"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p9601837302"><a name="en-us_topic_0182207107_p9601837302"></a><a name="en-us_topic_0182207107_p9601837302"></a>-t, --tty</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p176861211319"><a name="en-us_topic_0182207107_p176861211319"></a><a name="en-us_topic_0182207107_p176861211319"></a>Allocate a pseudo-TTY</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row13353886542"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p193531487548"><a name="en-us_topic_0182207107_p193531487548"></a><a name="en-us_topic_0182207107_p193531487548"></a>--ulimit</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1944203011543"><a name="en-us_topic_0182207107_p1944203011543"></a><a name="en-us_topic_0182207107_p1944203011543"></a>Set ulimit limits for the container</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row192184195910"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1310416598"><a name="en-us_topic_0182207107_p1310416598"></a><a name="en-us_topic_0182207107_p1310416598"></a>-u, --user</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1568613211317"><a name="en-us_topic_0182207107_p1568613211317"></a><a name="en-us_topic_0182207107_p1568613211317"></a>Username or UID, format [&amp;lt;name|uid&amp;gt;][:&amp;lt;group|gid&amp;gt;]</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--user-remap</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Map user to container (for system containers)</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--userns</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Set user namespace for the container when the 'user-remap' option is enabled</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row15496195712522"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p11497185745212"><a name="en-us_topic_0182207105_p11497185745212"></a><a name="en-us_topic_0182207105_p11497185745212"></a>--uts</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1349715755214"><a name="en-us_topic_0182207105_p1349715755214"></a><a name="en-us_topic_0182207105_p1349715755214"></a>Set PID namespace</p>
</td>
</tr>
<tr id="en-us_topic_0182207107_row287661103"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p8877613012"><a name="en-us_topic_0182207107_p8877613012"></a><a name="en-us_topic_0182207107_p8877613012"></a>-v, --volume=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207107_p1717301115357"><a name="en-us_topic_0182207107_p1717301115357"></a><a name="en-us_topic_0182207107_p1717301115357"></a>Mount a volume</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row969873217614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1443220391575"><a name="en-us_topic_0182207105_p1443220391575"></a><a name="en-us_topic_0182207105_p1443220391575"></a>--volumes-from=[]</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p343617396718"><a name="en-us_topic_0182207105_p343617396718"></a><a name="en-us_topic_0182207105_p343617396718"></a>Use the mount configuration from the specified container</p>
</td>
</tr>
<tr id="en-us_topic_0182207105_row969873217614"><td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p1443220391575"><a name="en-us_topic_0182207105_p1443220391575"></a><a name="en-us_topic_0182207105_p1443220391575"></a>--workdir</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0182207105_p343617396718"><a name="en-us_topic_0182207105_p343617396718"></a><a name="en-us_topic_0182207105_p343617396718"></a>Set working directory inside the container</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- When the parent process of a container exits, the corresponding container automatically exits.
- When a common container is created, the parent process cannot be initiated because the permission of common containers is insufficient. As a result, the container does not respond when you run the  **attach**  command though it is created successfully.
- If  **--net**  is not specified when the container is running, the default host name is  **localhost**.
- If the  **--files-limit**  parameter is to transfer a small value, for example, 1, when the container is started, iSulad creates a cgroup, sets the files.limit value, and writes the PID of the container process to the  **cgroup.procs**  file of the cgroup. At this time, the container process has opened more than one handle. As a result, a write error is reported, and the container fails to be started.
- If both**--mount**  and  **--volume**  exist and their destination paths conflict,  **--mount**  will be run after  **--volume**  \(that is, the mount point in  **--volume**  will be overwritten\).

    Note: The value of the  **type**  parameter of lightweight containers can be  **bind**  or  **squashfs**. When  **type**  is set to  **squashfs**,  **src**  is the image path. The value of the  **type**  parameter of the native Docker can be  **bind**,  **volume**, and  **tmpfs**.

- The restart policy does not support  **unless-stopped**.
- The values returned for Docker and lightweight containers are 127 and 125 respectively in the following three scenarios:

    The host device specified by  **--device**  does not exist.

    The hook JSON file specified by  **--hook-spec**  does not exist.

    The entry point specified by  **--entrypoint**  does not exist.

- When the  **--volume**  parameter is used, /dev/ptmx will be deleted and recreated during container startup. Therefore, do not mount the  **/dev**  directory to that of the container. Use  **--device**  to mount the devices in  **/dev**  of the container.
- Do not use the echo option to input data to the standard input of the  **run**  command. Otherwise, the client will be suspended. The echo value should be directly transferred to the container as a command line parameter.

    ```shell
    [root@localhost ~]# echo ls | isula run -i busybox /bin/sh
    
    
    ^C
    [root@localhost ~]# 
    ```

    The client is suspended when the preceding command is executed because the preceding command is equivalent to input  **ls**  to  **stdin**. Then EOF is read and the client does not send data and waits for the server to exit. However, the server cannot determine whether the client needs to continue sending data. As a result, the server is suspended in reading data, and both parties are suspended.

    The correct execution method is as follows:

    ```shell
    [root@localhost ~]# isula run -i busybox ls
    bin
    dev
    etc
    home
    proc
    root
    sys
    tmp
    usr
    var
    [root@localhost ~]# 
    ```

- If the root directory \(/\) of the host is used as the file system of the container, the following situations may occur during the mounting:

    **Table  2**  Mounting scenarios

    <a name="en-us_topic_0182207107_table1075313351843"></a>
    <table><thead align="left"><tr id="en-us_topic_0182207107_row1875314355413"><th class="cellrowborder" valign="top" width="50%" id="mcps1.2.3.1.1"><p id="en-us_topic_0182207107_p075318354418"><a name="en-us_topic_0182207107_p075318354418"></a><a name="en-us_topic_0182207107_p075318354418"></a>Host Path (source)</p>
    </th>
    <th class="cellrowborder" valign="top" width="50%" id="mcps1.2.3.1.2"><p id="en-us_topic_0182207107_p1975316357419"><a name="en-us_topic_0182207107_p1975316357419"></a><a name="en-us_topic_0182207107_p1975316357419"></a>Container Path (<span>dest</span>)</p>
    </th>
    </tr>
    </thead>
    <tbody><tr id="en-us_topic_0182207107_row11753435245"><td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.1 "><p id="en-us_topic_0182207107_p1775317351414"><a name="en-us_topic_0182207107_p1775317351414"></a><a name="en-us_topic_0182207107_p1775317351414"></a>/home/test1</p>
    </td>
    <td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.2 "><p id="en-us_topic_0182207107_p17532352412"><a name="en-us_topic_0182207107_p17532352412"></a><a name="en-us_topic_0182207107_p17532352412"></a>/mnt/</p>
    </td>
    </tr>
    <tr id="en-us_topic_0182207107_row47531735341"><td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.1 "><p id="en-us_topic_0182207107_p15753235749"><a name="en-us_topic_0182207107_p15753235749"></a><a name="en-us_topic_0182207107_p15753235749"></a>/home/test2</p>
    </td>
    <td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.2 "><p id="en-us_topic_0182207107_p675383516412"><a name="en-us_topic_0182207107_p675383516412"></a><a name="en-us_topic_0182207107_p675383516412"></a>/mnt/abc</p>
    </td>
    </tr>
    </tbody>
    </table>

    > [!WARNING]NOTICE   
    > Scenario 1: Mount  **/home/test1**  and then  **/home/test2**. In this case, the content in  **/home/test1**  overwrites the content in  **/mnt**. As a result, the  **abc**  directory does not exist in  **/mnt**, and mounting**/home/test2**  to  **/mnt/abc**  fails.  
    > Scenario 2: Mount  **/home/test2**  and then  **/home/test1**. In this case, the content of  **/mnt**  is replaced with the content of  **/home/test1**  during the second mounting. In this way, the content mounted during the first mounting from  **/home/test2**  to  **/mnt/abc**  is overwritten.  
    > The first scenario is not supported. For the second scenario, users need to understand the risk of data access failures.  

- Exercise caution when configuring the **/sys** and **/proc** directories as writable. The **/sys** and **/proc** directories contain interfaces for Linux to manage kernel parameters and devices. Configuring these directories as writable in a container may lead to container escape.
- Exercise caution when configuring containers to share namespaces with the host. For example, using **--pid**, **--ipc**, **--uts**, or **--net** to share namespace spaces between the container and the host eliminates namespace isolation between them. This allows attacks on the host from within the container. For instance, using **--pid** to share the PID namespace with the host enables the container to view and kill processes on the host.
- Exercise caution when using parameters like **--device** or **-v** to mount host resources. Avoid mapping sensitive directories or devices of the host into the container to prevent sensitive information leakage.
- Exercise caution when starting containers with the **--privileged** option. The **--privileged** option grants excessive permissions to the container, which can affect the host configuration.

    > [!WARNING]NOTICE   
    > In high concurrency scenarios \(200 containers are concurrently started\), the memory management mechanism of Glibc may cause memory holes and large virtual memory \(for example, 10 GB\). This problem is caused by the restriction of the Glibc memory management mechanism in the high concurrency scenario, but not by memory leakage. Therefore, the memory consumption does not increase infinitely. You can set the  **MALLOC\_ARENA\_MAX**  environment variable to reduce the virtual memory and increase the probability of reducing the physical memory. However, this environment variable will cause the iSulad concurrency performance to deteriorate. Set this environment variable based on the site requirements.  
    >
    > To balance performance and memory usage, set MALLOC_ARENA_MAX to 4. (The iSulad performance deterioration on the ARM64 server is controlled by less than 10%.)  
    > Configuration method:  
    > 1. To manually start iSulad, run the export MALLOC_ARENA_MAX=4 command and then start the iSulad.  
    > 2. If systemd manages iSulad, you can modify the /etc/sysconfig/iSulad file by adding MALLOC_ARENA_MAX=4.  

### Example

Run a new container.

```shell
$ isula run -itd busybox
9c2c13b6c35f132f49fb7ffad24f9e673a07b7fe9918f97c0591f0d7014c713b
```

## Stopping a Container

### Description

To stop a container, run the  **isula stop**  command. The SIGTERM signal is sent to the first process in the container. If the container is not stopped within the specified time \(10s by default\), the SIGKILL signal is sent.

### Usage

```shell
isula stop [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **stop**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292664_table177040323515"></a>
<table><tbody><tr id="en-us_topic_0183292664_row8712538252"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292664_p588494216519"><a name="en-us_topic_0183292664_p588494216519"></a><a name="en-us_topic_0183292664_p588494216519"></a><strong id="en-us_topic_0183292664_b1688413421253"><a name="en-us_topic_0183292664_b1688413421253"></a><a name="en-us_topic_0183292664_b1688413421253"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292664_p188847428520"><a name="en-us_topic_0183292664_p188847428520"></a><a name="en-us_topic_0183292664_p188847428520"></a><strong id="en-us_topic_0183292664_b1188414428517"><a name="en-us_topic_0183292664_b1188414428517"></a><a name="en-us_topic_0183292664_b1188414428517"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292664_p178848422515"><a name="en-us_topic_0183292664_p178848422515"></a><a name="en-us_topic_0183292664_p178848422515"></a><strong id="en-us_topic_0183292664_b1288417421351"><a name="en-us_topic_0183292664_b1288417421351"></a><a name="en-us_topic_0183292664_b1288417421351"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row1674140193219"><td class="cellrowborder" rowspan="5" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292664_p0513915955"><a name="en-us_topic_0183292664_p0513915955"></a><a name="en-us_topic_0183292664_p0513915955"></a><strong id="en-us_topic_0183292664_b985082143420"><a name="en-us_topic_0183292664_b985082143420"></a><a name="en-us_topic_0183292664_b985082143420"></a>stop</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292664_p93955542325"><a name="en-us_topic_0183292664_p93955542325"></a><a name="en-us_topic_0183292664_p93955542325"></a>-f, --force</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292664_p177516011323"><a name="en-us_topic_0183292664_p177516011323"></a><a name="en-us_topic_0183292664_p177516011323"></a>Force stop the running container</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row19123163783212"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p6279743153214"><a name="en-us_topic_0183292664_p6279743153214"></a><a name="en-us_topic_0183292664_p6279743153214"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p16284174363216"><a name="en-us_topic_0183292664_p16284174363216"></a><a name="en-us_topic_0183292664_p16284174363216"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-t, --time</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Stop gracefully first, and terminate forcefully after this time</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- If the  **t**  parameter is specified and the value of  **t**  is less than 0, ensure that the application in the container can process the stop signal.

    Principle of the Stop command: Send the SIGTERM signal to the container, and then wait for a period of time \(**t**  entered by the user\). If the container is still running after the period of time, the SIGKILL signal is sent to forcibly kill the container.

- The meaning of the input parameter  **t**  is as follows:

    **t**  < 0: Wait for graceful stop. This setting is preferred when users are assured that their applications have a proper stop signal processing mechanism.

    **t**  = 0: Do not wait and send  **kill -9**  to the container immediately.

    **t**  \> 0: Wait for a specified period and send  **kill -9**  to the container if the container does not stop within the specified period.

    Therefore, if  **t**  is set to a value less than 0 \(for example,  **t**  = -1\), ensure that the container application correctly processes the SIGTERM signal. If the container ignores this signal, the container will be suspended when the  **isula stop**  command is run.

### Example

Stop a container.

```shell
$ isula stop fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
```

## Forcibly Stopping a Container

### Description

To forcibly stop one or more running containers, run the  **isula kill**  command.

### Usage

```shell
isula kill [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **kill**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292665_table169751130165112"></a>
<table><tbody><tr id="en-us_topic_0183292665_row319819347519"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292665_p29829438516"><a name="en-us_topic_0183292665_p29829438516"></a><a name="en-us_topic_0183292665_p29829438516"></a><strong id="en-us_topic_0183292665_b898274385115"><a name="en-us_topic_0183292665_b898274385115"></a><a name="en-us_topic_0183292665_b898274385115"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292665_p209821543135113"><a name="en-us_topic_0183292665_p209821543135113"></a><a name="en-us_topic_0183292665_p209821543135113"></a><strong id="en-us_topic_0183292665_b098274365110"><a name="en-us_topic_0183292665_b098274365110"></a><a name="en-us_topic_0183292665_b098274365110"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292665_p79821843145113"><a name="en-us_topic_0183292665_p79821843145113"></a><a name="en-us_topic_0183292665_p79821843145113"></a><strong id="en-us_topic_0183292665_b1598244395110"><a name="en-us_topic_0183292665_b1598244395110"></a><a name="en-us_topic_0183292665_b1598244395110"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292665_row58305372820"><td class="cellrowborder" rowspan="4" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292665_p118191410451"><a name="en-us_topic_0183292665_p118191410451"></a><a name="en-us_topic_0183292665_p118191410451"></a><strong id="en-us_topic_0183292665_b173181853113112"><a name="en-us_topic_0183292665_b173181853113112"></a><a name="en-us_topic_0183292665_b173181853113112"></a>kill</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292665_p788705815285"><a name="en-us_topic_0183292665_p788705815285"></a><a name="en-us_topic_0183292665_p788705815285"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292665_p98932586284"><a name="en-us_topic_0183292665_p98932586284"></a><a name="en-us_topic_0183292665_p98932586284"></a>Specify the path to the iSulad socket file to connect to.</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode.</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information.</p>
</td>
</tr>
<tr id="en-us_topic_0183292665_row1581911017514"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292665_p118190101656"><a name="en-us_topic_0183292665_p118190101656"></a><a name="en-us_topic_0183292665_p118190101656"></a>-s, --signal</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292665_p16861421431"><a name="en-us_topic_0183292665_p16861421431"></a><a name="en-us_topic_0183292665_p16861421431"></a>Signal to send to the container.</p>
</td>
</tr>
</tbody>
</table>

### Example

Kill a container.

```shell
$ isula kill fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
```

## Removing a Container

### Description

To remove a container, run the  **isula rm**  command.

### Usage

```shell
isula rm [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **rm**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292666_table1415911244586"></a>
<table><tbody><tr id="en-us_topic_0183292666_row7264628165818"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292666_p135193313581"><a name="en-us_topic_0183292666_p135193313581"></a><a name="en-us_topic_0183292666_p135193313581"></a><strong id="en-us_topic_0183292666_b14511233125813"><a name="en-us_topic_0183292666_b14511233125813"></a><a name="en-us_topic_0183292666_b14511233125813"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292666_p15116335589"><a name="en-us_topic_0183292666_p15116335589"></a><a name="en-us_topic_0183292666_p15116335589"></a><strong id="en-us_topic_0183292666_b18517333584"><a name="en-us_topic_0183292666_b18517333584"></a><a name="en-us_topic_0183292666_b18517333584"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292666_p651153325816"><a name="en-us_topic_0183292666_p651153325816"></a><a name="en-us_topic_0183292666_p651153325816"></a><strong id="en-us_topic_0183292666_b7511833115817"><a name="en-us_topic_0183292666_b7511833115817"></a><a name="en-us_topic_0183292666_b7511833115817"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292666_row1551311511520"><td class="cellrowborder" rowspan="5" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292666_p1551301514517"><a name="en-us_topic_0183292666_p1551301514517"></a><a name="en-us_topic_0183292666_p1551301514517"></a><strong id="en-us_topic_0183292666_b232374193312"><a name="en-us_topic_0183292666_b232374193312"></a><a name="en-us_topic_0183292666_b232374193312"></a>rm</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292666_p18513141514517"><a name="en-us_topic_0183292666_p18513141514517"></a><a name="en-us_topic_0183292666_p18513141514517"></a>-f, --force</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292666_p18686121639"><a name="en-us_topic_0183292666_p18686121639"></a><a name="en-us_topic_0183292666_p18686121639"></a>Forcefully remove the running container</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255_1"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292666_row1394151573014"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292666_p445111743017"><a name="en-us_topic_0183292666_p445111743017"></a><a name="en-us_topic_0183292666_p445111743017"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292666_p1145701733014"><a name="en-us_topic_0183292666_p1145701733014"></a><a name="en-us_topic_0183292666_p1145701733014"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292666_row11287834145116"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292666_p132871334115116"><a name="en-us_topic_0183292666_p132871334115116"></a><a name="en-us_topic_0183292666_p132871334115116"></a>-v, --volume</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292666_p15287103415118"><a name="en-us_topic_0183292666_p15287103415118"></a><a name="en-us_topic_0183292666_p15287103415118"></a>Remove volumes mounted on the container (Note: iSulad does not support this function yet)</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- In normal I/O scenarios, it takes T1 to delete a running container in an empty environment \(with only one container\). In an environment with 200 containers \(without a large number of I/O operations and with normal host I/O\), it takes T2 to delete a running container. The specification of T2 is as follows: T2 = max \{T1 x 3, 5\}s.

### Example

Delete a stopped container.

```shell
$ isula rm fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
```

## Attaching to a Container

### Description

To attach standard input, standard output, and standard error of the current terminal to a running container, run the  **isula attach**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula attach [OPTIONS] CONTAINER
```

### Parameters

The following table lists the parameters supported by the  **attach**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292667_table14752840142911"></a>
<table><thead align="left"><tr id="en-us_topic_0183292667_row1561315411186"><th class="cellrowborder" valign="top" width="17.333333333333336%" id="mcps1.2.4.1.1"><p id="en-us_topic_0183292667_p16197118172112"><a name="en-us_topic_0183292667_p16197118172112"></a><a name="en-us_topic_0183292667_p16197118172112"></a><strong id="en-us_topic_0183292667_b121981618182110"><a name="en-us_topic_0183292667_b121981618182110"></a><a name="en-us_topic_0183292667_b121981618182110"></a>Command</strong></p>
</th>
<th class="cellrowborder" valign="top" width="39.57575757575758%" id="mcps1.2.4.1.2"><p id="en-us_topic_0183292667_p131981218102117"><a name="en-us_topic_0183292667_p131981218102117"></a><a name="en-us_topic_0183292667_p131981218102117"></a><strong id="en-us_topic_0183292667_b719861814214"><a name="en-us_topic_0183292667_b719861814214"></a><a name="en-us_topic_0183292667_b719861814214"></a>Option</strong></p>
</th>
<th class="cellrowborder" valign="top" width="43.09090909090909%" id="mcps1.2.4.1.3"><p id="en-us_topic_0183292667_p7685132114311"><a name="en-us_topic_0183292667_p7685132114311"></a><a name="en-us_topic_0183292667_p7685132114311"></a><strong id="en-us_topic_0183292667_b238118331471"><a name="en-us_topic_0183292667_b238118331471"></a><a name="en-us_topic_0183292667_b238118331471"></a>Description</strong></p>
</th>
</tr>
</thead>
<tbody><tr id="en-us_topic_0183292667_row378741121914"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%" headers="mcps1.2.4.1.1"><p id="en-us_topic_0183292667_p2788111171911"><a name="en-us_topic_0183292667_p2788111171911"></a><a name="en-us_topic_0183292667_p2788111171911"></a><strong id="en-us_topic_0183292667_b19827526183312"><a name="en-us_topic_0183292667_b19827526183312"></a><a name="en-us_topic_0183292667_b19827526183312"></a>attach</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%" headers="mcps1.2.4.1.2"><p id="en-us_topic_0183292667_p440023182210"><a name="en-us_topic_0183292667_p440023182210"></a><a name="en-us_topic_0183292667_p440023182210"></a>--help</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%" headers="mcps1.2.4.1.3"><p id="en-us_topic_0183292667_p114002313226"><a name="en-us_topic_0183292667_p114002313226"></a><a name="en-us_topic_0183292667_p114002313226"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292667_row159823516222"><td class="cellrowborder" valign="top" headers="mcps1.2.4.1.2"><p id="en-us_topic_0183292667_p622945315220"><a name="en-us_topic_0183292667_p622945315220"></a><a name="en-us_topic_0183292667_p622945315220"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" headers="mcps1.2.4.1.3"><p id="en-us_topic_0183292667_p11229125362213"><a name="en-us_topic_0183292667_p11229125362213"></a><a name="en-us_topic_0183292667_p11229125362213"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292667_row14595112722316"><td class="cellrowborder" valign="top" headers="mcps1.2.4.1.2"><p id="en-us_topic_0183292667_p17595162742311"><a name="en-us_topic_0183292667_p17595162742311"></a><a name="en-us_topic_0183292667_p17595162742311"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top" headers="mcps1.2.4.1.3"><p id="en-us_topic_0183292667_p1959513279236"><a name="en-us_topic_0183292667_p1959513279236"></a><a name="en-us_topic_0183292667_p1959513279236"></a>Enable debug mode</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- For the native Docker, running the  **attach**  command will directly enter the container. For the iSulad container, you have to run the  **attach**  command and press  **Enter**  to enter the container.

### Example

Attach to a running container.

```shell
$ isula attach fd7376591a9c3d8ee9a14f5d2c2e5255b02cc44cddaabca82170efd4497510e1
/ #
/ #
```

## Renaming a Container

### Description

To rename a container, run the  **isula rename**  command.

### Usage

```shell
isula rename [OPTIONS] OLD_NAME NEW_NAME
```

### Parameters

The following table lists the parameters supported by the  **rename**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292668_table0848174213413"></a>
<table><thead align="left"><tr id="en-us_topic_0183292667_row1561315411186"><th class="cellrowborder" valign="top" width="17.333333333333336%" id="mcps1.2.4.1.1"><p id="en-us_topic_0183292667_p16197118172112"><a name="en-us_topic_0183292667_p16197118172112"></a><a name="en-us_topic_0183292667_p16197118172112"></a><strong id="en-us_topic_0183292667_b121981618182110"><a name="en-us_topic_0183292667_b121981618182110"></a><a name="en-us_topic_0183292667_b121981618182110"></a>Command</strong></p>
</th>
<th class="cellrowborder" valign="top" width="39.57575757575758%" id="mcps1.2.4.1.2"><p id="en-us_topic_0183292667_p131981218102117"><a name="en-us_topic_0183292667_p131981218102117"></a><a name="en-us_topic_0183292667_p131981218102117"></a><strong id="en-us_topic_0183292667_b719861814214"><a name="en-us_topic_0183292667_b719861814214"></a><a name="en-us_topic_0183292667_b719861814214"></a>Option</strong></p>
</th>
<th class="cellrowborder" valign="top" width="43.09090909090909%" id="mcps1.2.4.1.3"><p id="en-us_topic_0183292667_p7685132114311"><a name="en-us_topic_0183292667_p7685132114311"></a><a name="en-us_topic_0183292667_p7685132114311"></a><strong id="en-us_topic_0183292667_b238118331471"><a name="en-us_topic_0183292667_b238118331471"></a><a name="en-us_topic_0183292667_b238118331471"></a>Description</strong></p>
</th>
</tr>
</thead>
<tbody><tr id="en-us_topic_0183292667_row378741121914"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%" headers="mcps1.2.4.1.1 "><p id="en-us_topic_0183292667_p2788111171911"><a name="en-us_topic_0183292667_p2788111171911"></a><a name="en-us_topic_0183292667_p2788111171911"></a><strong id="en-us_topic_0183292667_b19827526183312"><a name="en-us_topic_0183292667_b19827526183312"></a><a name="en-us_topic_0183292667_b19827526183312"></a>rename</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%" headers="mcps1.2.4.1.2 "><p id="en-us_topic_0183292667_p440023182210"><a name="en-us_topic_0183292667_p440023182210"></a><a name="en-us_topic_0183292667_p440023182210"></a>--help</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%" headers="mcps1.2.4.1.3 "><p id="en-us_topic_0183292667_p114002313226"><a name="en-us_topic_0183292667_p114002313226"></a><a name="en-us_topic_0183292667_p114002313226"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292667_row159823516222"><td class="cellrowborder" valign="top" headers="mcps1.2.4.1.1 "><p id="en-us_topic_0183292667_p622945315220"><a name="en-us_topic_0183292667_p622945315220"></a><a name="en-us_topic_0183292667_p622945315220"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" headers="mcps1.2.4.1.2 "><p id="en-us_topic_0183292667_p11229125362213"><a name="en-us_topic_0183292667_p11229125362213"></a><a name="en-us_topic_0183292667_p11229125362213"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292667_row14595112722316"><td class="cellrowborder" valign="top" headers="mcps1.2.4.1.1 "><p id="en-us_topic_0183292667_p17595162742311"><a name="en-us_topic_0183292667_p17595162742311"></a><a name="en-us_topic_0183292667_p17595162742311"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top" headers="mcps1.2.4.1.2 "><p id="en-us_topic_0183292667_p1959513279236"><a name="en-us_topic_0183292667_p1959513279236"></a><a name="en-us_topic_0183292667_p1959513279236"></a>Enable debug mode</p>
</td>
</tr>
</tbody>
</table>

### Example

Rename a container.

```shell
isula rename my_container my_new_container
```

## Executing a Command in a Running Container

### Description

To execute a command in a running container, run the  **isula exec**  command. This command is executed in the default directory of the container. If a user-defined directory is specified for the basic image, the user-defined directory is used.

### Usage

```shell
isula exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

### Parameters

The following table lists the parameters supported by the  **exec**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292669_table123271972373"></a>
<table><tbody><tr id="en-us_topic_0183292669_row11911910193715"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292669_p1599121519378"><a name="en-us_topic_0183292669_p1599121519378"></a><a name="en-us_topic_0183292669_p1599121519378"></a><strong id="en-us_topic_0183292669_b129918157370"><a name="en-us_topic_0183292669_b129918157370"></a><a name="en-us_topic_0183292669_b129918157370"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292669_p129921517375"><a name="en-us_topic_0183292669_p129921517375"></a><a name="en-us_topic_0183292669_p129921517375"></a><strong id="en-us_topic_0183292669_b109921517373"><a name="en-us_topic_0183292669_b109921517373"></a><a name="en-us_topic_0183292669_b109921517373"></a>Option</strong></strong"></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292669_p159941513375"><a name="en-us_topic_0183292669_p159941513375"></a><a name="en-us_topic_0183292669_p159941513375"></a><strong id="en-us_topic_0183292669_b699131593718"><a name="en-us_topic_0183292669_b699131593718"></a><a name="en-us_topic_0183292669_b699131593718"></a>Description</strong></strong"></p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row27694315596"><td class="cellrowborder" rowspan="9" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292669_p059393215315"><a name="en-us_topic_0183292669_p059393215315"></a><a name="en-us_topic_0183292669_p059393215315"></a><strong id="en-us_topic_0183292669_b1060012451269"><a name="en-us_topic_0183292669_b1060012451269"></a><a name="en-us_topic_0183292669_b1060012451269"></a>exec</strong></strong></p>
<p id="en-us_topic_0183292669_p17332618610"><a name="en-us_topic_0183292669_p17332618610"></a><a name="en-us_topic_0183292669_p17332618610"></a>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292669_p176843115914"><a name="en-us_topic_0183292669_p176843115914"></a><a name="en-us_topic_0183292669_p176843115914"></a>-d, --detach</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292669_p166861121233"><a name="en-us_topic_0183292669_p166861121233"></a><a name="en-us_topic_0183292669_p166861121233"></a>Run command in the background</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row144815810419"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p248105814415"><a name="en-us_topic_0183292669_p248105814415"></a><a name="en-us_topic_0183292669_p248105814415"></a>-e, --env</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p1240225963710"><a name="en-us_topic_0183292669_p1240225963710"></a><a name="en-us_topic_0183292669_p1240225963710"></a>Set environment variables (Note: This feature is currently not used by iSulad)</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row225582276"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p16101657289"><a name="en-us_topic_0183292669_p16101657289"></a><a name="en-us_topic_0183292669_p16101657289"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p10104456281"><a name="en-us_topic_0183292669_p10104456281"></a><a name="en-us_topic_0183292669_p10104456281"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row185407613516"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p115401661558"><a name="en-us_topic_0183292669_p115401661558"></a><a name="en-us_topic_0183292669_p115401661558"></a>-i, --interactive</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p4818143019389"><a name="en-us_topic_0183292669_p4818143019389"></a><a name="en-us_topic_0183292669_p4818143019389"></a>Keep standard input open even if not connected (Note: This feature is currently not used by iSulad)</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row2054016654"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p65401663515"><a name="en-us_topic_0183292669_p65401663515"></a><a name="en-us_topic_0183292669_p65401663515"></a>-t, --tty</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p1783413176392"><a name="en-us_topic_0183292669_p1783413176392"></a><a name="en-us_topic_0183292669_p1783413176392"></a>Allocate a pseudo-TTY (Note: This feature is currently not used by iSulad)</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row3321661767"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p18331961361"><a name="en-us_topic_0183292669_p18331961361"></a><a name="en-us_topic_0183292669_p18331961361"></a>-u, --user</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p93326361"><a name="en-us_topic_0183292669_p93326361"></a><a name="en-us_topic_0183292669_p93326361"></a>Specify the user to log into the container to execute the command</p>
</td>
</tr>
<tr id="en-us_topic_0183292669_row3321661767"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p18331961361"><a name="en-us_topic_0183292669_p18331961361"></a><a name="en-us_topic_0183292669_p18331961361"></a>--workdir</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292669_p93326361"><a name="en-us_topic_0183292669_p93326361"></a><a name="en-us_topic_0183292669_p93326361"></a>Specify the working directory for executing the command; this function is only supported when the runtime is lcr</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- If no parameter is specified in the  **isula exec**  command, the  **-it**  parameter is used by default, indicating that a pseudo terminal is allocated and the container is accessed in interactive mode.
- When you run the  **isula exec**  command to execute a script and run a background process in the script, you need to use the  **nohup**  flag to ignore the  **SIGHUP**  signal.

    When you run the  **isula exec**  command to execute a script and run a background process in the script, you need to use the  **nohup**  flag. Otherwise, the kernel sends the  **SIGHUP**  signal to the process executed in the background when the process \(first process of the session\) exits. As a result, the background process exits and zombie processes occur.

- After running the  **isula exec**  command to access the container process, do not run background programs. Otherwise, the system will be suspended.

    To run the  **isula exec**  command to execute a background process, perform the following steps:

    1. Run the  **isula exec container\_name bash**  command to access the container.
    2. After entering the container, run the  **script &**  command.
    3. Run the  **exit**  command. The terminal stops responding.

    After the **isula exec** command is executed to enter the container, the background program stops responding because the **isula exec** command is executed to enter the container and run the background while1 program. When Bash exits, the while1 program does not exit and becomes an orphan process, which is taken over by process 1.
    The the while1 process is executed by the initial Bash process **fork &exec** of the container. The while1 process copies the file handle of the Bash process. As a result, the handle is not completely closed when the Bash process exits. The console process cannot receive the handle closing event, epoll_wait stops responding, and the process does not exit.

- Do not run the  **isula exec**  command in the background. Otherwise, the system may be suspended.

    Run the  **isula exec**  command in the background as follows:

    Run the  **isula exec script &**  command in the background, for example,  **isula exec container\_name script &,isula exec**. The command is executed in the background. The script continuously displays a file by running the  **cat**  command. Normally, there is output on the current terminal. If you press  **Enter**  on the current terminal, the client exits the stdout read operation due to the I/O read failure. As a result, the terminal does not output data. The server continues to write data to the buffer of the FIFO because the process is still displaying files by running the  **cat**  command. When the buffer is full, the process in the container is suspended in the write operation.

- When a lightweight container uses the  **exec**  command to execute commands with pipe operations, you are advised to run the  **/bin/bash -c**  command.

    Typical application scenarios:

    Run the  **isula exec container\_name -it ls /test | grep "xx" | wc -l**  command to count the number of xx files in the test directory. The output is processed by  **grep**  and  **wc**  through the pipe because  **ls /test**  is executed with  **exec**. The output of  **ls /test**  executed by  **exec**  contains line breaks. When the output is processed, the result is incorrect.

    Cause: Run the  **ls /test**  command using  **exec**. The command output contains a line feed character. Run the**| grep "xx" | wc -l**  command for the output. The processing result is 2 \(two lines\).

    ```shell
    [root@localhost ~]# isula exec  -it container ls /test
    xx    xx10  xx12  xx14  xx3   xx5   xx7   xx9
    xx1   xx11  xx13  xx2   xx4   xx6   xx8
    [root@localhost ~]#
    ```

    Suggestion: When running the  **run/exec**  command to perform pipe operations, run the  **/bin/bash -c**  command to perform pipe operations in the container.

    ```shell
    [root@localhost ~]# isula exec  -it container  /bin/sh -c "ls /test | grep "xx" | wc -l"
    15
    [root@localhost ~]#
    ```

- Do not use the  **echo**  option to input data to the standard input of the  **exec**  command. Otherwise, the client will be suspended. The echo value should be directly transferred to the container as a command line parameter.

    ```shell
    [root@localhost ~]# echo ls | isula exec 38 /bin/sh
    
    
    ^C
    [root@localhost ~]# 
    ```

    The client is suspended when the preceding command is executed because the preceding command is equivalent to input  **ls**  to  **stdin**. Then EOF is read and the client does not send data and waits for the server to exit. However, the server cannot determine whether the client needs to continue sending data. As a result, the server is suspended in reading data, and both parties are suspended.

    The correct execution method is as follows:

    ```shell
    [root@localhost ~]# isula exec 38 ls
    bin   dev   etc   home  proc  root  sys   tmp   usr   var
    ```

### Example

Run the echo command in a running container.

```shell
$ isula exec c75284634bee echo "hello,world"
hello,world
```

## Querying Information About a Single Container

### Description

To query information about a single container, run the  **isula inspect**  command.

### Usage

```shell
isula inspect [OPTIONS] CONTAINER|IMAGE [CONTAINER|IMAGE...]
```

### Parameters

The following table lists the parameters supported by the  **inspect**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292670_table13831181815417"></a>
<table><tbody><tr id="en-us_topic_0183292670_row4440192185418"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p><strong id="en-us_topic_0183292670_b934022675420">Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p><strong id="en-us_topic_0183292670_b103408265544">Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p><strong id="en-us_topic_0183292670_b1934011266545">Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292670_row1451341192811"><td class="cellrowborder" rowspan="5" valign="top" width="17.333333333333336%"><p><strong id="en-us_topic_0183292670_b155461026123118">inspect</strong></p>
<p>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p>Specifies the path to the iSulad socket file to connect to.</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p>Enables debug mode.</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p>--help</p>
</td>
<td class="cellrowborder" valign="top"><p>Prints help information.</p>
</td>
</tr>
<tr id="en-us_topic_0183292670_row88191210357"><td class="cellrowborder" valign="top"><p>-f, --format</p>
</td>
<td class="cellrowborder" valign="top"><p>Formats the output using a template.</p>
</td>
</tr>
<tr id="en-us_topic_0183292670_row084314449019"><td class="cellrowborder" valign="top"><p>-t, --time</p>
</td>
<td class="cellrowborder" valign="top"><p>Timeout duration in seconds. If the inspect command fails to query container information within this time, it stops waiting and reports an error immediately. The default is 120 seconds. If the value is less than or equal to 0, the timeout mechanism is disabled, and the inspect command will wait indefinitely until container information is successfully retrieved.</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- Lightweight containers do not support the output in \{ \{.State\} \} format but support the output in the \{ \{json .State\} \} format. The  **-f**  parameter is not supported when the object is an image.

### Example

Query information about a container.

```shell
$ isula inspect c75284634bee
[
    {
        "Id": "c75284634beeede3ab86c828790b439d16b6ed8a537550456b1f94eb852c1c0a",
        "Created": "2019-08-01T22:48:13.993304927-04:00",
        "Path": "sh",
        "Args": [],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "Pid": 21164,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2019-08-02T06:09:25.535049168-04:00",
            "FinishedAt": "2019-08-02T04:28:09.479766839-04:00",
            "Health": {
                "Status": "",
                "FailingStreak": 0,
                "Log": []
            }
        },
        "Image": "busybox",
        "ResolvConfPath": "",
        "HostnamePath": "",
        "HostsPath": "",
        "LogPath": "none",
        "Name": "c75284634beeede3ab86c828790b439d16b6ed8a537550456b1f94eb852c1c0a",
        "RestartCount": 0,
        "HostConfig": {
            "Binds": [],
            "NetworkMode": "",
            "GroupAdd": [],
            "IpcMode": "",
            "PidMode": "",
            "Privileged": false,
            "SystemContainer": false,
            "NsChangeFiles": [],
            "UserRemap": "",
            "ShmSize": 67108864,
            "AutoRemove": false,
            "AutoRemoveBak": false,
            "ReadonlyRootfs": false,
            "UTSMode": "",
            "UsernsMode": "",
            "Sysctls": {},
            "Runtime": "lcr",
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "CapAdd": [],
            "CapDrop": [],
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": [],
            "HookSpec": "",
            "CPUShares": 0,
            "Memory": 0,
            "OomScoreAdj": 0,
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "CPUPeriod": 0,
            "CPUQuota": 0,
            "CPURealtimePeriod": 0,
            "CPURealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "SecurityOpt": [],
            "StorageOpt": {},
            "KernelMemory": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "OomKillDisable": false,
            "PidsLimit": 0,
            "FilesLimit": 0,
            "Ulimits": [],
            "Hugetlbs": [],
            "HostChannel": {
                "PathOnHost": "",
                "PathInContainer": "",
                "Permissions": "",
                "Size": 0
            },
            "EnvTargetFile": "",
            "ExternalRootfs": ""
        },
        "Mounts": [],
        "Config": {
            "Hostname": "localhost",
            "User": "",
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "TERM=xterm",
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Tty": true,
            "Cmd": [
                "sh"
            ],
            "Entrypoint": [],
            "Labels": {},
            "Annotations": {
                "log.console.file": "none",
                "log.console.filerotate": "7",
                "log.console.filesize": "1MB",
                "rootfs.mount": "/var/lib/isulad/mnt/rootfs",
                "native.umask": "secure"
            },
            "HealthCheck": {
                "Test": [],
                "Interval": 0,
                "Timeout": 0,
                "StartPeriod": 0,
                "Retries": 0,
                "ExitOnUnhealthy": false
            }
        },
        "NetworkSettings": {
            "IPAddress": ""
        }
    }
]
```

## Querying Information About All Containers

### Description

To query information about all containers, run the  **isula ps**  command.

### Usage

```shell
isula ps [OPTIONS]
```

### Parameters

The following table lists the parameters supported by the  **ps**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292671_table116431017151015"></a>
<table><tbody><tr id="en-us_topic_0183292671_row1892743561016"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292671_p647714113100"><strong id="en-us_topic_0183292671_b947764101011">Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292671_p19477184141017"><strong id="en-us_topic_0183292671_b1247784161017">Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292671_p14772415101"><strong id="en-us_topic_0183292671_b16477841141015">Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row1051316155514"><td class="cellrowborder" rowspan="8" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292671_p1751361519519"><strong id="en-us_topic_0183292671_b17395283215">ps</strong></p>
<p id="en-us_topic_0183292671_p187333219234">&nbsp;&nbsp;</p>
<p id="en-us_topic_0183292671_p961891475811">&nbsp;&nbsp;</p>
<p id="en-us_topic_0183292671_p11287101518">&nbsp;&nbsp;</p>
<p id="en-us_topic_0183292671_p1354335311522">&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292671_p55132151556">-a, --all</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292671_p86860216314">Show all containers</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514">-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314">Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514">--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314">Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row1293653612919"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p1950214384295">-H, --host</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p10506113822910">Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row4733729230"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p5733162132318">-q, --quiet</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p473352142318">Only display container names</p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row11618514105815"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p161812143587">-f, --filter</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p461891416584">Add filter conditions</p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row12287190155116"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p42872015512">--format</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p1228717019517">Output data in the format specified by the template</p>
</td>
</tr>
<tr id="en-us_topic_0183292671_row1454255310529"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p854305314521">--no-trunc</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292671_p554315313522">Do not truncate the container ID when printing</p>
</td>
</tr>
</tbody>
</table>

### Example

Query information about all containers.

```shell
$ isula ps -a

ID           IMAGE                                     STATUS  PID    COMMAND EXIT_CODE RESTART_COUNT STARTAT        FINISHAT    RUNTIME NAMES
e84660aa059c rnd-dockerhub.huawei.com/official/busybox running 304765 "sh"    0         0             13 minutes ago -           lcr     e84660aa059cafb0a77a4002e65cc9186949132b8e57b7f4d76aa22f28fde016
$ isula ps -a --format "table {{.ID}} {{.Image}}" --no-trunc
ID                                                               IMAGE
e84660aa059cafb0a77a4002e65cc9186949132b8e57b7f4d76aa22f28fde016 rnd-dockerhub.huawei.com/official/busybox
```

## Restarting a Container

### Description

To restart one or more containers, run the  **isula restart**  command.

### Usage

```shell
isula restart [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **restart**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292672_table137858361717"></a>
<table><tbody><tr id="en-us_topic_0183292672_row267501311712"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292672_p46961418141710"><a name="en-us_topic_0183292672_p46961418141710"></a><a name="en-us_topic_0183292672_p46961418141710"></a><strong id="en-us_topic_0183292672_b18696181817172"><a name="en-us_topic_0183292672_b18696181817172"></a><a name="en-us_topic_0183292672_b18696181817172"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292672_p1569691821712"><a name="en-us_topic_0183292672_p1569691821712"></a><a name="en-us_topic_0183292672_p1569691821712"></a><strong id="en-us_topic_0183292672_b06971184174"><a name="en-us_topic_0183292672_b06971184174"></a><a name="en-us_topic_0183292672_b06971184174"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292672_p11697121811175"><a name="en-us_topic_0183292672_p11697121811175"></a><a name="en-us_topic_0183292672_p11697121811175"></a><strong id="en-us_topic_0183292672_b1969761891719"><a name="en-us_topic_0183292672_b1969761891719"></a><a name="en-us_topic_0183292672_b1969761891719"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292672_row1937135117295"><td class="cellrowborder" rowspan="4" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292672_p151311157514"><a name="en-us_topic_0183292672_p151311157514"></a><a name="en-us_topic_0183292672_p151311157514"></a><strong id="en-us_topic_0183292672_b1764311131331"><a name="en-us_topic_0183292672_b1764311131331"></a><a name="en-us_topic_0183292672_b1764311131331"></a>restart</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292672_p1153405792918"><a name="en-us_topic_0183292672_p1153405792918"></a><a name="en-us_topic_0183292672_p1153405792918"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292672_p12538145719290"><a name="en-us_topic_0183292672_p12538145719290"></a><a name="en-us_topic_0183292672_p12538145719290"></a>Specify the path of the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183292672_row351313151155"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292672_p1151310155517"><a name="en-us_topic_0183292672_p1151310155517"></a><a name="en-us_topic_0183292672_p1151310155517"></a>-t, --time</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292672_p1168613218314"><a name="en-us_topic_0183292672_p1168613218314"></a><a name="en-us_topic_0183292672_p1168613218314"></a>Stop gracefully first, forcibly terminate if this time is exceeded</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- If the  **t**  parameter is specified and the value of  **t**  is less than 0, ensure that the application in the container can process the stop signal.

    The restart command first calls the stop command to stop the container. Send the SIGTERM signal to the container, and then wait for a period of time \(**t**  entered by the user\). If the container is still running after the period of time, the SIGKILL signal is sent to forcibly kill the container.

- The meaning of the input parameter  **t**  is as follows:

    **t**  < 0: Wait for graceful stop. This setting is preferred when users are assured that their applications have a proper stop signal processing mechanism.

    **t**  = 0: Do not wait and send  **kill -9**  to the container immediately.

    **t**  \> 0: Wait for a specified period and send  **kill -9**  to the container if the container does not stop within the specified period.

    Therefore, if  **t**  is set to a value less than 0 \(for example,  **t**  = -1\), ensure that the container application correctly processes the SIGTERM signal. If the container ignores this signal, the container will be suspended when the  **isula stop**  command is run.

### Example

Restart a container.

```shell
$ isula restart c75284634beeede3ab86c828790b439d16b6ed8a537550456b1f94eb852c1c0a
 c75284634beeede3ab86c828790b439d16b6ed8a537550456b1f94eb852c1c0a 
```

## Waiting for a Container to Exit

### Description

To wait for one or more containers to exit, run the  **isula wait**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula wait [OPTIONS] CONTAINER [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **wait**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292673_table5504410103614"></a>
<table><tbody><tr id="en-us_topic_0183292673_row3860413123616"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292673_p1924011817360"><a name="en-us_topic_0183292673_p1924011817360"></a><a name="en-us_topic_0183292673_p1924011817360"></a><strong id="en-us_topic_0183292673_b18240518153611"><a name="en-us_topic_0183292673_b18240518153611"></a><a name="en-us_topic_0183292673_b18240518153611"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292673_p2240131815362"><a name="en-us_topic_0183292673_p2240131815362"></a><a name="en-us_topic_0183292673_p2240131815362"></a><strong id="en-us_topic_0183292673_b12402189364"><a name="en-us_topic_0183292673_b12402189364"></a><a name="en-us_topic_0183292673_b12402189364"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292673_p824010189363"><a name="en-us_topic_0183292673_p824010189363"></a><a name="en-us_topic_0183292673_p824010189363"></a><strong id="en-us_topic_0183292673_b5240131863612"><a name="en-us_topic_0183292673_b5240131863612"></a><a name="en-us_topic_0183292673_b5240131863612"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183292673_row1877872243318"><td class="cellrowborder" rowspan="4" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292673_p12454121193413"><a name="en-us_topic_0183292673_p12454121193413"></a><a name="en-us_topic_0183292673_p12454121193413"></a><strong id="en-us_topic_0183292673_b10950153316341"><a name="en-us_topic_0183292673_b10950153316341"></a><a name="en-us_topic_0183292673_b10950153316341"></a>wait</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292673_p1949112354334"><a name="en-us_topic_0183292673_p1949112354334"></a><a name="en-us_topic_0183292673_p1949112354334"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292673_p249913515339"><a name="en-us_topic_0183292673_p249913515339"></a><a name="en-us_topic_0183292673_p249913515339"></a>Specifies the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Example

Wait for a single container to exit.

```shell
$ isula wait c75284634beeede3ab86c828790b439d16b6ed8a537550456b1f94eb852c1c0a
 137 
```

## Viewing Process Information in a Container

### Description

To view process information in a container, run the  **isula top**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula top [OPTIONS] container [ps options]
```

### Parameters

The following table lists the parameters supported by the  **top**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183292674_table17675155184214"></a>
<table><thead><tr id="en-us_topic_0183292674_row20270691423"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292674_p3380191384218"><a name="en-us_topic_0183292674_p3380191384218"></a><a name="en-us_topic_0183292674_p3380191384218"></a><strong id="en-us_topic_0183292674_b163807135422"><a name="en-us_topic_0183292674_b163807135422"></a><a name="en-us_topic_0183292674_b163807135422"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292674_p18380313174219"><a name="en-us_topic_0183292674_p18380313174219"></a><a name="en-us_topic_0183292674_p18380313174219"></a><strong id="en-us_topic_0183292674_b15380213124216"><a name="en-us_topic_0183292674_b15380213124216"></a><a name="en-us_topic_0183292674_b15380213124216"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292674_p17380413164215"><a name="en-us_topic_0183292674_p17380413164215"></a><a name="en-us_topic_0183292674_p17380413164215"></a><strong id="en-us_topic_0183292674_b1838021364210"><a name="en-us_topic_0183292674_b1838021364210"></a><a name="en-us_topic_0183292674_b1838021364210"></a>Description</strong></p>
</td>
</tr></thead><tbody><tr id="en-us_topic_0183292674_row12517277157"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183292674_p225222714151"><a name="en-us_topic_0183292674_p225222714151"></a><a name="en-us_topic_0183292674_p225222714151"></a><strong id="en-us_topic_0183292674_b1048744013165"><a name="en-us_topic_0183292674_b1048744013165"></a><a name="en-us_topic_0183292674_b1048744013165"></a>top</strong></p>
<p id="en-us_topic_0183292674_p16253122751518"><a name="en-us_topic_0183292674_p16253122751518"></a><a name="en-us_topic_0183292674_p16253122751518"></a>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183292674_p999125117202"><a name="en-us_topic_0183292674_p999125117202"></a><a name="en-us_topic_0183292674_p999125117202"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183292674_p599115517207"><a name="en-us_topic_0183292674_p599115517207"></a><a name="en-us_topic_0183292674_p599115517207"></a>Specifies the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Example

Query process information in a container.

```shell
$ isula top 21fac8bb9ea8e0be4313c8acea765c8b4798b7d06e043bbab99fc20efa72629c
UID        PID  PPID  C STIME TTY          TIME CMD
root     22166 22163  0 23:04 pts/1    00:00:00 sh
```

## Displaying Resource Usage Statistics of a Container

### Description

To display resource usage statistics in real time, run the  **isula stats**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula stats [OPTIONS] [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **stats**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183385024_table17441132195013"></a>
<table><tbody><tr id="en-us_topic_0183385024_row1946936105017"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183385024_p1032317392502"><a name="en-us_topic_0183385024_p1032317392502"></a><a name="en-us_topic_0183385024_p1032317392502"></a><strong id="en-us_topic_0183385024_b1832323911500"><a name="en-us_topic_0183385024_b1832323911500"></a><a name="en-us_topic_0183385024_b1832323911500"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385024_p432313914504"><a name="en-us_topic_0183385024_p432313914504"></a><a name="en-us_topic_0183385024_p432313914504"></a><strong id="en-us_topic_0183385024_b1032343910507"><a name="en-us_topic_0183385024_b1032343910507"></a><a name="en-us_topic_0183385024_b1032343910507"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385024_p17323739195015"><a name="en-us_topic_0183385024_p17323739195015"></a><a name="en-us_topic_0183385024_p17323739195015"></a><strong id="en-us_topic_0183385024_b93238398503"><a name="en-us_topic_0183385024_b93238398503"></a><a name="en-us_topic_0183385024_b93238398503"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183602765_row345895810479"><td class="cellrowborder" rowspan="6" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183602765_p154581458134710"><a name="en-us_topic_0183602765_p154581458134710"></a><a name="en-us_topic_0183602765_p154581458134710"></a><strong id="en-us_topic_0183602765_b15458135804712"><a name="en-us_topic_0183602765_b15458135804712"></a><a name="en-us_topic_0183602765_b15458135804712"></a>stats</strong></p>
<p id="en-us_topic_0183602765_p119301526174714"><a name="en-us_topic_0183602765_p119301526174714"></a><a name="en-us_topic_0183602765_p119301526174714"></a>&nbsp;&nbsp;</p>
<p id="en-us_topic_0183602765_p18280132164715"><a name="en-us_topic_0183602765_p18280132164715"></a><a name="en-us_topic_0183602765_p18280132164715"></a>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385024_p104901417103610"><a name="en-us_topic_0183385024_p104901417103610"></a><a name="en-us_topic_0183385024_p104901417103610"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385024_p166979433617"><a name="en-us_topic_0183385024_p166979433617"></a><a name="en-us_topic_0183385024_p166979433617"></a>Specifies the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183602765_row194501657194718"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183602765_p114501157194717"><a name="en-us_topic_0183602765_p114501157194717"></a><a name="en-us_topic_0183602765_p114501157194717"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183602765_p1945095734716"><a name="en-us_topic_0183602765_p1945095734716"></a><a name="en-us_topic_0183602765_p1945095734716"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183602765_row194501657194718"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183602765_p114501157194717"><a name="en-us_topic_0183602765_p114501157194717"></a><a name="en-us_topic_0183602765_p114501157194717"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183602765_p1945095734716"><a name="en-us_topic_0183602765_p1945095734716"></a><a name="en-us_topic_0183602765_p1945095734716"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183385024_row114031757103617"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p194045578363"><a name="en-us_topic_0183385024_p194045578363"></a><a name="en-us_topic_0183385024_p194045578363"></a>-a, --all</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p5404457163611"><a name="en-us_topic_0183385024_p5404457163611"></a><a name="en-us_topic_0183385024_p5404457163611"></a>Show all containers (by default, only running containers are shown)</p>
</td>
</tr>
<tr id="en-us_topic_0183385024_row056333013377"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p165641030193716"><a name="en-us_topic_0183385024_p165641030193716"></a><a name="en-us_topic_0183385024_p165641030193716"></a>--no-stream</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p01374203812"><a name="en-us_topic_0183385024_p01374203812"></a><a name="en-us_topic_0183385024_p01374203812"></a>Non-streaming stats, only prints the first result</p>
</td>
</tr>
<tr id="en-us_topic_0183385024_row056333013377"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p165641030193716"><a name="en-us_topic_0183385024_p165641030193716"></a><a name="en-us_topic_0183385024_p165641030193716"></a>--original</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385024_p01374203812"><a name="en-us_topic_0183385024_p01374203812"></a><a name="en-us_topic_0183385024_p01374203812"></a>Show original container data, no statistical calculation performed</p>
</td>
</tr>
</tbody>
</table>

### Example

Display resource usage statistics.

```shell
$ isula stats --no-stream 21fac8bb9ea8e0be4313c8acea765c8b4798b7d06e043bbab99fc20efa72629c                                                                                 CONTAINER        CPU %      MEM USAGE / LIMIT          MEM %      BLOCK I / O                PIDS      
21fac8bb9ea8     0.00       56.00 KiB / 7.45 GiB       0.00       0.00 B / 0.00 B            1  
```

## Obtaining Container Logs

### Description

To obtain container logs, run the  **isula logs**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula logs [OPTIONS] [CONTAINER...]
```

### Parameters

The following table lists the parameters supported by the  **logs**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183385749_table947315512062"></a>
<table><tbody><tr id="en-us_topic_0183385749_row3520144677"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183385749_p19203188678"><a name="en-us_topic_0183385749_p19203188678"></a><a name="en-us_topic_0183385749_p19203188678"></a><strong id="en-us_topic_0183385749_b820311811711"><a name="en-us_topic_0183385749_b820311811711"></a><a name="en-us_topic_0183385749_b820311811711"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385749_p11203148076"><a name="en-us_topic_0183385749_p11203148076"></a><a name="en-us_topic_0183385749_p11203148076"></a><strong id="en-us_topic_0183385749_b82031484716"><a name="en-us_topic_0183385749_b82031484716"></a><a name="en-us_topic_0183385749_b82031484716"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385749_p1020398773"><a name="en-us_topic_0183385749_p1020398773"></a><a name="en-us_topic_0183385749_p1020398773"></a><strong id="en-us_topic_0183385749_b182031381770"><a name="en-us_topic_0183385749_b182031381770"></a><a name="en-us_topic_0183385749_b182031381770"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183385749_row14697142222913"><td class="cellrowborder" rowspan="6" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183385749_p16819111014516"><a name="en-us_topic_0183385749_p16819111014516"></a><a name="en-us_topic_0183385749_p16819111014516"></a><strong id="en-us_topic_0183385749_b1379012813322"><a name="en-us_topic_0183385749_b1379012813322"></a><a name="en-us_topic_0183385749_b1379012813322"></a>logs</strong></p>
<p id="en-us_topic_0183385749_p8819810351"><a name="en-us_topic_0183385749_p8819810351"></a><a name="en-us_topic_0183385749_p8819810351"></a>&nbsp;&nbsp;</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385749_p5821430112915"><a name="en-us_topic_0183385749_p5821430112915"></a><a name="en-us_topic_0183385749_p5821430112915"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385749_p284113015293"><a name="en-us_topic_0183385749_p284113015293"></a><a name="en-us_topic_0183385749_p284113015293"></a>Specify the path to the iSulad socket file to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255_1"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514_1"><a name="en-us_topic_0183292664_p3513121512514_1"></a><a name="en-us_topic_0183292664_p3513121512514_1"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314_1"><a name="en-us_topic_0183292664_p176864215314_1"></a><a name="en-us_topic_0183292664_p176864215314_1"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255_2"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514_2"><a name="en-us_topic_0183292664_p3513121512514_2"></a><a name="en-us_topic_0183292664_p3513121512514_2"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314_2"><a name="en-us_topic_0183292664_p176864215314_2"></a><a name="en-us_topic_0183292664_p176864215314_2"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0183385749_row128198101251"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p108192101852"><a name="en-us_topic_0183385749_p108192101852"></a><a name="en-us_topic_0183385749_p108192101852"></a>-f, --follow</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p86861211314"><a name="en-us_topic_0183385749_p86861211314"></a><a name="en-us_topic_0183385749_p86861211314"></a>Follow log output</p>
</td>
</tr>
<tr id="en-us_topic_0183385749_row58191610350"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p118191110955"><a name="en-us_topic_0183385749_p118191110955"></a><a name="en-us_topic_0183385749_p118191110955"></a>--tail</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p1568617213316"><a name="en-us_topic_0183385749_p1568617213316"></a><a name="en-us_topic_0183385749_p1568617213316"></a>Show number of log lines</p>
</td>
</tr>
<tr id="en-us_topic_0183385749_row58191610350_1"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p118191110955_1"><a name="en-us_topic_0183385749_p118191110955_1"></a><a name="en-us_topic_0183385749_p118191110955_1"></a>-t, --timestamps</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183385749_p1568617213316_1"><a name="en-us_topic_0183385749_p1568617213316_1"></a><a name="en-us_topic_0183385749_p1568617213316_1"></a>Show timestamps</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- By default, the container log function is enabled. To disable this function, run the  **isula create --log-opt disable-log=true**  or  **isula run --log-opt disable-log=true**  command.

### Example

Obtain container logs.

```shell
$ isula logs 6a144695f5dae81e22700a8a78fac28b19f8bf40e8827568b3329c7d4f742406
hello, world
hello, world
hello, world
```

## Copying Data Between a Container and a Host

### Description

To copy data between a host and a container, run the  **isula cp**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
isula cp [OPTIONS] SRC_PATH CONTAINER:DEST_PATH
```

### Parameters

The following table lists the parameters supported by the  **cp**  command.

**Table  1**  Parameter description

<a name="en-us_topic_0183385750_table45852013111514"></a>
<table><tbody><tr id="en-us_topic_0183385750_row1790211601513"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183385750_p7179821161516"><a name="en-us_topic_0183385750_p7179821161516"></a><a name="en-us_topic_0183385750_p7179821161516"></a><strong id="en-us_topic_0183385750_b91798219151"><a name="en-us_topic_0183385750_b91798219151"></a><a name="en-us_topic_0183385750_b91798219151"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385750_p15179121111511"><a name="en-us_topic_0183385750_p15179121111511"></a><a name="en-us_topic_0183385750_p15179121111511"></a><strong id="en-us_topic_0183385750_b717982112150"><a name="en-us_topic_0183385750_b717982112150"></a><a name="en-us_topic_0183385750_b717982112150"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385750_p10180152151511"><a name="en-us_topic_0183385750_p10180152151511"></a><a name="en-us_topic_0183385750_p10180152151511"></a><strong id="en-us_topic_0183385750_b718015216152"><a name="en-us_topic_0183385750_b718015216152"></a><a name="en-us_topic_0183385750_b718015216152"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0183385750_row89859561117"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%"><p id="en-us_topic_0183385750_p69851856411"><a name="en-us_topic_0183385750_p69851856411"></a><a name="en-us_topic_0183385750_p69851856411"></a><strong id="en-us_topic_0183385750_b192299211024"><a name="en-us_topic_0183385750_b192299211024"></a><a name="en-us_topic_0183385750_b192299211024"></a>cp</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0183385750_p549293210212"><a name="en-us_topic_0183385750_p549293210212"></a><a name="en-us_topic_0183385750_p549293210212"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0183385750_p1049213321528"><a name="en-us_topic_0183385750_p1049213321528"></a><a name="en-us_topic_0183385750_p1049213321528"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- When iSulad copies files, note that the  **/etc/hostname**,  **/etc/resolv.conf**, and  **/etc/hosts**  files are not mounted to the host, neither the  **--volume**  and  **--mount**  parameters. Therefore, the original files in the image instead of the files in the real container are copied.

    ```shell
    [root@localhost tmp]# isula cp b330e9be717a:/etc/hostname /tmp/hostname
    [root@localhost tmp]# cat /tmp/hostname
    [root@localhost tmp]# 
    ```

- When decompressing a file, iSulad does not check the type of the file or folder to be overwritten in the file system. Instead, iSulad directly overwrites the file or folder. Therefore, if the source is a folder, the file with the same name is forcibly overwritten as a folder. If the source file is a file, the folder with the same name will be forcibly overwritten as a file.

    ```shell
    [root@localhost tmp]# rm -rf /tmp/test_file_to_dir && mkdir /tmp/test_file_to_dir
    [root@localhost tmp]# isula exec b330e9be717a /bin/sh -c "rm -rf /tmp/test_file_to_dir && touch /tmp/test_file_to_dir"
    [root@localhost tmp]# isula cp b330e9be717a:/tmp/test_file_to_dir /tmp
    [root@localhost tmp]# ls -al /tmp | grep test_file_to_dir
    -rw-r-----    1 root     root             0 Apr 26 09:59 test_file_to_dir
    ```

- iSulad freezes the container during the copy process and restores the container after the copy is complete.

### Example

Copy the  **/test/host**  directory on the host to the  **/test**  directory on container 21fac8bb9ea8.

```shell
isula cp /test/host 21fac8bb9ea8:/test
```

Copy the  **/www**  directory on container 21fac8bb9ea8 to the  **/tmp**  directory on the host.

```shell
isula cp 21fac8bb9ea8:/www /tmp/
```

## Pausing a Container

### Description

To pause all processes in a container, run the  **isula pause**  command. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula pause CONTAINER [CONTAINER...]
```

### Parameters

<a name="en-us_topic_0224966142_table45852013111514"></a>
<table><tbody><tr id="en-us_topic_0224966142_row1790211601513"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0224966142_p7179821161516"><a name="en-us_topic_0224966142_p7179821161516"></a><a name="en-us_topic_0224966142_p7179821161516"></a><strong id="en-us_topic_0224966142_b91798219151"><a name="en-us_topic_0224966142_b91798219151"></a><a name="en-us_topic_0224966142_b91798219151"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0224966142_p15179121111511"><a name="en-us_topic_0224966142_p15179121111511"></a><a name="en-us_topic_0224966142_p15179121111511"></a><strong id="en-us_topic_0224966142_b717982112150"><a name="en-us_topic_0224966142_b717982112150"></a><a name="en-us_topic_0224966142_b717982112150"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0224966142_p10180152151511"><a name="en-us_topic_0224966142_p10180152151511"></a><a name="en-us_topic_0224966142_p10180152151511"></a><strong id="en-us_topic_0224966142_b718015216152"><a name="en-us_topic_0224966142_b718015216152"></a><a name="en-us_topic_0224966142_b718015216152"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0224966142_row89859561117"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%"><p id="en-us_topic_0224966142_p69851856411"><a name="en-us_topic_0224966142_p69851856411"></a><a name="en-us_topic_0224966142_p69851856411"></a>pause</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0224966142_p549293210212"><a name="en-us_topic_0224966142_p549293210212"></a><a name="en-us_topic_0224966142_p549293210212"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0224966142_p1049213321528"><a name="en-us_topic_0224966142_p1049213321528"></a><a name="en-us_topic_0224966142_p1049213321528"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- Only containers in the running state can be paused.
- After a container is paused, other lifecycle management operations \(such as  **restart**,  **exec**,  **attach**,  **kill**,  **stop**, and  **rm**\) cannot be performed.
- After a container with health check configurations is paused, the container status changes to unhealthy.

### Example

Pause a running container.

```shell
$ isula pause 8fe25506fb5883b74c2457f453a960d1ae27a24ee45cdd78fb7426d2022a8bac
 8fe25506fb5883b74c2457f453a960d1ae27a24ee45cdd78fb7426d2022a8bac 
```

## Resuming a Container

### Description

To resume all processes in a container, run the  **isula unpause**  command. It is the reverse process of  **isula pause**. Only containers whose runtime is of the LCR type are supported.

### Usage

```shell
isula unpause CONTAINER [CONTAINER...]
```

### Parameters

<a name="en-us_topic_0224966143_table45852013111514"></a>
<table><tbody><tr id="en-us_topic_0224966143_row1790211601513"><td class="cellrowborder" valign="top" width="17.333333333333336%"><p id="en-us_topic_0224966143_p7179821161516"><a name="en-us_topic_0224966143_p7179821161516"></a><a name="en-us_topic_0224966143_p7179821161516"></a><strong id="en-us_topic_0224966143_b91798219151"><a name="en-us_topic_0224966143_b91798219151"></a><a name="en-us_topic_0224966143_b91798219151"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0224966143_p15179121111511"><a name="en-us_topic_0224966143_p15179121111511"></a><a name="en-us_topic_0224966143_p15179121111511"></a><strong id="en-us_topic_0224966143_b717982112150"><a name="en-us_topic_0224966143_b717982112150"></a><a name="en-us_topic_0224966143_b717982112150"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0224966143_p10180152151511"><a name="en-us_topic_0224966143_p10180152151511"></a><a name="en-us_topic_0224966143_p10180152151511"></a><strong id="en-us_topic_0224966143_b718015216152"><a name="en-us_topic_0224966143_b718015216152"></a><a name="en-us_topic_0224966143_b718015216152"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0224966143_row89859561117"><td class="cellrowborder" rowspan="3" valign="top" width="17.333333333333336%"><p id="en-us_topic_0224966143_p69851856411"><a name="en-us_topic_0224966143_p69851856411"></a><a name="en-us_topic_0224966143_p69851856411"></a>pause</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%"><p id="en-us_topic_0224966143_p549293210212"><a name="en-us_topic_0224966143_p549293210212"></a><a name="en-us_topic_0224966143_p549293210212"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%"><p id="en-us_topic_0224966143_p1049213321528"><a name="en-us_topic_0224966143_p1049213321528"></a><a name="en-us_topic_0224966143_p1049213321528"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255"><td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top"><p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- Only containers in the paused state can be unpaused.

### Example

Resume a paused container.

```shell
$ isula unpause 8fe25506fb5883b74c2457f453a960d1ae27a24ee45cdd78fb7426d2022a8bac
 8fe25506fb5883b74c2457f453a960d1ae27a24ee45cdd78fb7426d2022a8bac 
```

## Obtaining Event Messages from the Server in Real Time

### **Description**

The  **isula events**  command is used to obtain event messages such as container image lifecycle and running event from the server in real time. Only containers whose runtime type is  **lcr**  are supported.

### Usage

```shell
isula events [OPTIONS]
```

### Parameter

<a name="en-us_topic_0231454831_table45852013111514"></a>
<table>
<tbody>
<tr id="en-us_topic_0231454831_row1790211601513">
<td class="cellrowborder" valign="top" width="17.333333333333336%">
<p id="en-us_topic_0231454831_p7179821161516"><a name="en-us_topic_0231454831_p7179821161516"></a><a name="en-us_topic_0231454831_p7179821161516"></a><strong id="en-us_topic_0231454831_b91798219151"><a name="en-us_topic_0231454831_b91798219151"></a><a name="en-us_topic_0231454831_b91798219151"></a>Command</strong></p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%">
<p id="en-us_topic_0231454831_p15179121111511"><a name="en-us_topic_0231454831_p15179121111511"></a><a name="en-us_topic_0231454831_p15179121111511"></a><strong id="en-us_topic_0231454831_b717982112150"><a name="en-us_topic_0231454831_b717982112150"></a><a name="en-us_topic_0231454831_b717982112150"></a>Option</strong></p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%">
<p id="en-us_topic_0231454831_p10180152151511"><a name="en-us_topic_0231454831_p10180152151511"></a><a name="en-us_topic_0231454831_p10180152151511"></a><strong id="en-us_topic_0231454831_b718015216152"><a name="en-us_topic_0231454831_b718015216152"></a><a name="en-us_topic_0231454831_b718015216152"></a>Description</strong></p>
</td>
</tr>
<tr id="en-us_topic_0231454831_row89859561117">
<td class="cellrowborder" rowspan="6" valign="top" width="17.333333333333336%">
<p id="en-us_topic_0231454831_p69851856411"><a name="en-us_topic_0231454831_p69851856411"></a><a name="en-us_topic_0231454831_p69851856411"></a>events</p>
</td>
<td class="cellrowborder" valign="top" width="39.57575757575758%">
<p id="en-us_topic_0231454831_p549293210212"><a name="en-us_topic_0231454831_p549293210212"></a><a name="en-us_topic_0231454831_p549293210212"></a>-H, --host</p>
</td>
<td class="cellrowborder" valign="top" width="43.09090909090909%">
<p id="en-us_topic_0231454831_p1049213321528"><a name="en-us_topic_0231454831_p1049213321528"></a><a name="en-us_topic_0231454831_p1049213321528"></a>Specify the iSulad socket file path to connect to</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255">
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>-D, --debug</p>
</td>
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Enable debug mode</p>
</td>
</tr>
<tr id="en-us_topic_0183292664_row15138151255">
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0183292664_p3513121512514"><a name="en-us_topic_0183292664_p3513121512514"></a><a name="en-us_topic_0183292664_p3513121512514"></a>--help</p>
</td>
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0183292664_p176864215314"><a name="en-us_topic_0183292664_p176864215314"></a><a name="en-us_topic_0183292664_p176864215314"></a>Print help information</p>
</td>
</tr>
<tr id="en-us_topic_0231454831_row287455224012">
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p687465212409"><a name="en-us_topic_0231454831_p687465212409"></a><a name="en-us_topic_0231454831_p687465212409"></a>-n, --name</p>
</td>
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p1087455204011"><a name="en-us_topic_0231454831_p1087455204011"></a><a name="en-us_topic_0231454831_p1087455204011"></a>Get event messages for the specified container</p>
</td>
</tr>
<tr id="en-us_topic_0231454831_row59371553428">
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p199381955421"><a name="en-us_topic_0231454831_p199381955421"></a><a name="en-us_topic_0231454831_p199381955421"></a>-S, --since</p>
</td>
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p16938145144210"><a name="en-us_topic_0231454831_p16938145144210"></a><a name="en-us_topic_0231454831_p16938145144210"></a>Get event messages since the specified time</p>
</td>
</tr>
<tr id="en-us_topic_0231454831_row59371553428">
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p199381955421"><a name="en-us_topic_0231454831_p199381955421"></a><a name="en-us_topic_0231454831_p199381955421"></a>-U, --until</p>
</td>
<td class="cellrowborder" valign="top">
<p id="en-us_topic_0231454831_p16938145144210"><a name="en-us_topic_0231454831_p16938145144210"></a><a name="en-us_topic_0231454831_p16938145144210"></a>Get events up to the specified time</p>
</td>
</tr>
</tbody>
</table>

### Constraints

- Supported container events include `create`, `start`, `restart`, `stop`, `exec_create`, `exec_die`, `attach`, `kill`, `top`, `rename`, `archive-path`, `extract-to-dir`, `update`, `pause`, `unpause`, `export`, and `resize`.
- Supported image events include `load`, `remove`, `pull`, `login`, and `logout`.

### Example

Run the following command to obtain event messages from the server in real time:

```shell
isula events
```
