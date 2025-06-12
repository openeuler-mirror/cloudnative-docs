# Rubik User Guide

## Overview

Low server resource utilization has always been a recognized challenge in the industry. With the development of cloud native technologies, hybrid deployment of online (high-priority) and offline (low-priority) services becomes an effective means to improve resource utilization.

In hybrid service deployment scenarios, Rubik can properly schedule resources based on Quality if Service (QoS) levels to greatly improve resource utilization while ensuring the quality of online services.

Rubik supports the following features:

- [Absolute Preemption](./feature_introduction.md#absolute-preemption)
    - [CPU Absolute Preemption](./feature_introduction.md#cpu-absolute-preemption)
    - [Memory Absolute Preemption](./feature_introduction.md#memory-absolute-preemption)
- [dynCache Memory Bandwidth and L3 Cache Access Limit](./feature_introduction.md#dyncache-memory-bandwidth-and-l3-cache-access-limit)
- [dynMemory Tiered Memory Reclamation](./feature_introduction.md#dynmemory-tiered-memory-reclamation)
- [Flexible Bandwidth](./feature_introduction.md#flexible-bandwidth)
    - [quotaTurbo User-Mode Solution](./feature_introduction.md#quotaburst-kernel-mode-solution)
    - [quotaTurbo Configuration](./feature_introduction.md#quotaturbo-user-mode-solution)
- [I/O Weight Control Based on ioCost](./feature_introduction.md#io-weight-control-based-on-iocost)
- [Interference Detection Based on Pressure Stall Information Metrics](./feature_introduction.md#interference-detection-based-on-pressure-stall-information-metrics)
- [CPU Eviction Watermark Control](./feature_introduction.md#cpu-eviction-watermark-control)
- [Memory Eviction Watermark Control](./feature_introduction.md#memory-eviction-watermark-control)

This document is intended for community developers, open source enthusiasts, and partners who use the openEuler system and want to learn and use Rubik. Users must:

- Know basic Linux operations.
- Be familiar with basic operations of Kubernetes and Docker/iSulad.
