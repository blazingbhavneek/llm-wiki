# Tensor Map

A **tensor map** is a hardware object that describes the layout of a multi-dimensional array in global and shared memory. It is a prerequisite for performing bulk tensor asynchronous copies of multi-dimensional data.

## Overview

Tensor Memory Accelerator (TMA) supports copying both one-dimensional and multi-dimensional arrays, with support for up to 5-dimensional arrays. The programming model distinguishes between:

*   **One-dimensional contiguous arrays:** These can be copied on-device using a pointer and size parameter without requiring a tensor map.
*   **Multi-dimensional arrays:** These require a tensor map to define the layout for bulk tensor asynchronous copies.

## Creation and Usage

A tensor map is typically created on the host using the `cuTensorMapEncode` API. Once created, it is transferred from the host to the device as a constant kernel parameter annotated with `__grid_constant__`. On the device, the tensor map is used to copy a tile of data between shared and global memory.

## Memory Operations

Bulk-asynchronous copy operations using tensor maps can involve shared memory, global memory, and Distributed Shared Memory (DSM):

*   **Global to Shared:** Reading data from global memory to shared memory.
*   **Shared to Global:** Writing data from shared memory to global memory.
*   **Shared to Shared (Cluster):** Copying from shared memory to the Distributed Shared Memory of another block within the same cluster.
*   **Multicast:** When operating within a cluster, a bulk-asynchronous operation can be specified as multicast, transferring data from global memory to the shared memory of multiple blocks simultaneously.

### Performance Considerations

The multicast feature is optimized for the `sm_90a` target architecture. Using multicast on other compute architectures may result in significantly reduced performance; therefore, it is advised to use this feature primarily with `sm_90a`.

## References

- Dimensions, creation, and usage details [CUDA_C_Programming_Guide:L10224-L10227]
- Source/destination capabilities and multicast optimization [CUDA_C_Programming_Guide:L10224-L10227]
