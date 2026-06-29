# Stream Ordered Memory Allocator

> **Warning**: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA. [CUDA_C_Programming_Guide:L15390-L15398]

The Stream Ordered Memory Allocator is a memory management system introduced in CUDA 11.3 that allows applications to order memory allocation and deallocation operations with other work launched into a CUDA stream, such as kernel launches and asynchronous copies [CUDA_C_Programming_Guide:L15390-L15398].

## Problem Statement

Traditional memory management using `cudaMalloc` and `cudaFree` causes the GPU to synchronize across all executing CUDA streams [CUDA_C_Programming_Guide:L15390-L15398]. This synchronization can create performance bottlenecks and limit concurrency [CUDA_C_Programming_Guide:L15390-L15398].

## Key Features

### Stream-Ordered Semantics

The allocator enables applications to order memory allocation and deallocation with other work launched into a CUDA stream [CUDA_C_Programming_Guide:L15390-L15398]. This stream-ordering semantics allows the allocator to reuse memory allocations more effectively, improving application memory use [CUDA_C_Programming_Guide:L15390-L15398].

### Memory Caching and OS Calls

Applications can control the allocator’s memory caching behavior [CUDA_C_Programming_Guide:L15390-L15398]. When configured with an appropriate release threshold, the caching behavior allows the allocator to avoid expensive calls into the operating system when the application indicates it is willing to accept a larger memory footprint [CUDA_C_Programming_Guide:L15390-L15398].

### Inter-Process Sharing

The allocator supports the easy and secure sharing of allocations between processes [CUDA_C_Programming_Guide:L15390-L15398].

## Benefits

### Reduced Custom Management

For many applications, the Stream Ordered Memory Allocator reduces the need for custom memory management abstractions [CUDA_C_Programming_Guide:L15390-L15398]. It makes it easier to create high-performance custom memory management for applications that require it [CUDA_C_Programming_Guide:L15390-L15398].

### Library Integration

For applications and libraries that already have custom memory allocators, adopting the Stream Ordered Memory Allocator enables multiple libraries to share a common pool of memory managed by the driver [CUDA_C_Programming_Guide:L15390-L15398]. This sharing reduces excess memory consumption [CUDA_C_Programming_Guide:L15390-L15398].

### Driver Optimizations

The driver can perform optimizations based on its awareness of the allocator and other stream management APIs [CUDA_C_Programming_Guide:L15390-L15398].

## Tooling Support

Nsight Compute and the Next-Gen CUDA debugger are aware of the allocator as part of their CUDA 11.3 toolkit support [CUDA_C_Programming_Guide:L15390-L15398].

## API

The primary functions associated with the Stream Ordered Memory Allocator are:

*   `cudaMallocAsync`: Allocates memory in a stream-ordered manner.
*   `cudaFreeAsync`: Frees memory in a stream-ordered manner.

These functions allow memory operations to be ordered relative to other stream work, enabling the benefits described above [CUDA_C_Programming_Guide:L15390-L15398].
