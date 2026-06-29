# Extended GPU Memory (EGM)

Extended GPU Memory (EGM) is a feature designed for integrated CPU-GPU NVIDIA systems that facilitates efficient access to all system memory by GPUs within a single-node setup [CUDA_C_Programming_Guide:L22200-L22201]. It allows for physical memory allocation that can be accessed from any GPU thread within the system [CUDA_C_Programming_Guide:L22204-L22204].

## Overview

EGM leverages high-bandwidth interconnects to ensure that all GPUs can access memory resources at speeds comparable to GPU-GPU NVLink or NVLink-C2C [CUDA_C_Programming_Guide:L22204-L22204]. In this architecture, memory accesses occur via local high-bandwidth NVLink-C2C, while remote memory accesses utilize GPU NVLink and, in some cases, NVLink-C2C [CUDA_C_Programming_Guide:L22208-L22208].

With EGM, GPU threads gain the capability to access all available memory resources, including CPU-attached memory and HBM3, over the NVSwitch fabric [CUDA_C_Programming_Guide:L22208-L22208].

## Interface and Usage

The EGM interface is documented in Chapter 26 of the CUDA C Programming Guide, which covers preliminaries, platform topology, and usage examples for various configurations [CUDA_C_Programming_Guide:L737-L749]. Key aspects include:

*   **System Topology**: Understanding EGM platforms and system topology [CUDA_C_Programming_Guide:L737-L749].
*   **Socket Identifiers**: Accessing and identifying socket information [CUDA_C_Programming_Guide:L737-L749].
*   **Allocator Support**: Compatibility with various allocators and EGM support [CUDA_C_Programming_Guide:L737-L749].
*   **Memory Management Extensions**: Extensions to current APIs for memory management [CUDA_C_Programming_Guide:L737-L749].

### Configuration Examples

The guide provides usage examples for different system configurations [CUDA_C_Programming_Guide:L737-L749]:

*   **Single-Node, Single-GPU**: Basic usage scenarios [CUDA_C_Programming_Guide:L737-L749].
*   **Single-Node, Multi-GPU**: Utilizing Virtual Memory Management (VMM) APIs and CUDA Memory Pools [CUDA_C_Programming_Guide:L737-L749].
*   **Multi-Node, Single-GPU**: Configurations spanning multiple nodes [CUDA_C_Programming_Guide:L737-L749].

## See Also

*   CUDA Virtual Memory Management (VMM)
*   CUDA Memory Pool
*   NVLink-C2C
*   NVSwitch
