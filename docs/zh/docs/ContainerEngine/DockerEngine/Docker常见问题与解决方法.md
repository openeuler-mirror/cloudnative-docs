# Docker常见问题与解决方法

## **问题1：docker v18.09.9拉起的容器挂载点相比docker v19.03.0及以后的版本多一个**

原因：18.09版本的docker，默认ipcmode为shareable，该配置会多挂载一个shmpath挂载点。
解决方法：结合实际情况修改docker配置文件中的ipcmode选项为private，或者使用新版本的docker。
