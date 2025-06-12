# Usage Guide

System container functions are enhanced based on the iSula container engine. The container management function and the command format of the function provided by system containers are the same as those provided by the iSula container engine.

The following sections describe how to use the enhanced functions provided by system containers. For details about other command operations, see iSulad container engine documents.

The system container functions involve only the  **isula create/run**  command. Unless otherwise specified, this command is used for all functions. The command format is as follows:

```shell
isula create/run [OPTIONS] [COMMAND] [ARG...]
```

In the preceding format:

- **OPTIONS**: one or more command parameters. For details about supported parameters, see iSulad container engine [appendix](../../container_engine/isula_container_engine/appendix.md#command-line-parameters).
- **COMMAND**: command executed after a system container is started.
- **ARG**: parameter corresponding to the command executed after a system container is started.

>[!NOTE]Note
> Root privileges are necessary for using system containers.
