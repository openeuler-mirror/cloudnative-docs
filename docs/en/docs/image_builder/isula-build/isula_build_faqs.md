# Common Issues and Solutions

## Issue 1: isula-build Image Pull Error: Connection Refused

When pulling an image, isula-build encounters the error: `pinging container registry xx: get xx: dial tcp host:repo: connect: connection refused`.

This occurs because the image is sourced from an untrusted registry.

To resolve this, edit the isula-build registry configuration file located at **/etc/isula-build/registries.toml**. Add the untrusted registry to the `[registries.insecure]` section and restart isula-build.
