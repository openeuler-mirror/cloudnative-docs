# Rubik User Guide

## Overview

Low server resource utilization has always been a recognized challenge in the industry. With the development of cloud native technologies, hybrid deployment of online (high-priority) and offline (low-priority) services becomes an effective means to improve resource utilization.

In hybrid service deployment scenarios, Rubik can properly schedule resources based on Quality if Service (QoS) levels to greatly improve resource utilization while ensuring the quality of online services.

Rubik supports the following features:

- Pod CPU priority configuration
- Pod memory priority configuration

This document is intended for community developers, open source enthusiasts, and partners who use the openEuler system and want to learn and use Rubik. Users must:

- Know basic Linux operations.
- Be familiar with basic operations of Kubernetes and Docker/iSulad.
