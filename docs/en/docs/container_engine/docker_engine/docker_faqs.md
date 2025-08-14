# Common Docker Issues and Solutions

## Issue 1: Additional Mount Point in Docker v18.09.9 Compared to v19.03.0 and Later

In Docker version 18.09.9, containers have an extra mount point compared to those launched in Docker v19.03.0 and later. This is because the default `ipcmode` in v18.09 is set to `shareable`, which creates an additional `shmpath` mount point. To resolve this, either update the `ipcmode` option to `private` in the Docker configuration file or upgrade to a newer Docker version.
