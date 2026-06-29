# EGM Memory Management APIs

## Overview

The Exascale GPU (EGM) architecture extends current CUDA memory management APIs to support complex multi-socket and multi-node environments. These extensions allow developers to manage physical memory allocation and mapping across all sockets within a system.

## Allocator Support

EGM memory can be mapped using two primary allocation mechanisms:

1. **Virtual Memory**: Utilizes the `cuMemCreate` API.
2. **Stream Ordered Memory**: Utilizes the `cudaMemPoolCreate` API.

In both cases, the user is responsible for allocating physical memory and mapping it to a virtual memory address space on all sockets [CUDA_C_Programming_Guide:L22236-L22236].

## NUMA-Aware Location Properties

To facilitate proper memory placement, new CUDA property types have been introduced. These allow APIs to understand allocation locations using NUMA-like node identifiers [CUDA_C_Programming_Guide:L22242-L22242].

The following table details the specific CUDA types and their associated APIs:

| CUDA Type | Used with |
| :--- | :--- |
| `CU_MEM_LOCATION_TYPE_HOST_NUMA` | `CUmemAllocationProp` for `cuMemCreate` |
| `cudaMemLocationTypeHostNuma` | `cudaMemPoolProps` for `cudaMemPoolCreate` |

[CUDA_C_Programming_Guide:L22244-L22244]

## Multi-Node Considerations

For multi-node, single-GPU platforms, interprocess communication is required to manage memory across nodes. Users are encouraged to refer to Chapter 3 of the CUDA C Programming Guide for details on interprocess communication mechanisms [CUDA_C_Programming_Guide:L22238-L22238].

## References

- CUDA C Programming Guide, Section 26.1.4: Memory management extensions to current APIs [CUDA_C_Programming_Guide:L22234-L22234]
