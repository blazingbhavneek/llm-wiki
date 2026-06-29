# EGM Platforms and System Topology

Extended GPU Memory (EGM) is supported across three distinct system topologies, each leveraging specific hardware interconnects to facilitate memory extension.

## Supported Platforms

EGM can be enabled in the following three platform configurations:

1. **Single-Node, Single-GPU**: This topology consists of an ARM-based CPU, CPU-attached memory, and a GPU. Communication between the CPU and the GPU is facilitated by a high-bandwidth Chip-to-Chip (C2C) interconnect [CUDA_C_Programming_Guide:L22216-L22216].

2. **Single-Node, Multi-GPU**: This configuration consists of fully connected single-node, single-GPU platforms [CUDA_C_Programming_Guide:L22216-L22216].

3. **Multi-Node, Single-GPU**: This topology involves two or more single-node multi-socket systems [CUDA_C_Programming_Guide:L22216-L22216].

## Device Management and Routing

Proper device management is critical for EGM functionality. Using cgroups to limit available devices will block routing over EGM and cause performance issues. Instead, `CUDA_VISIBLE_DEVICES` should be used to manage device visibility [CUDA_C_Programming_Guide:L22218-L22218].
