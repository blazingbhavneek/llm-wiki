# Modular Programs and Data Access Constraints

In modular programs involving multiple threads, managing data visibility between CPU and GPU execution is critical to prevent accidental interactions. The `cudaMemAttachHost` flag, when specified with `cudaMallocManaged()`, creates an allocation that is initially invisible to device-side execution [CUDA_C_Programming_Guide:L22049-L22055].

By default, allocations are visible to all GPU kernels on all streams. Specifying `cudaMemAttachHost` ensures that there is no accidental interaction with another thread’s execution in the interval between the data allocation and when the data is acquired for a specific stream [CUDA_C_Programming_Guide:L22049-L22055].

## Problem: Default Visibility Hazards

Without the `cudaMemAttachHost` flag, a new allocation is considered "in-use" on the GPU if a kernel launched by another thread happens to be running [CUDA_C_Programming_Guide:L22049-L22055]. This can impact the allocating thread's ability to access the newly allocated data from the CPU (for example, within a base-class constructor) before it is able to explicitly attach the data to a private stream [CUDA_C_Programming_Guide:L22049-L22055].

## Solution: Safe Independence

To enable safe independence between threads, allocations should be made specifying the `cudaMemAttachHost` flag [CUDA_C_Programming_Guide:L22049-L22055]. This simplifies the process of ensuring that data is not accessed by the GPU until it has been properly associated with a specific stream by the allocating thread.

## Alternative: Barrier-Based Approach

An alternative to using `cudaMemAttachHost` is to place a process-wide barrier across all threads after the allocation has been attached to the stream [CUDA_C_Programming_Guide:L22049-L22055]. This ensures that all threads complete their data/stream associations before any kernels are launched, thereby avoiding the hazard [CUDA_C_Programming_Guide:L22049-L22055].

However, this approach has limitations:
1. A second barrier would be needed before the stream is destroyed because stream destruction causes allocations to revert to their default visibility [CUDA_C_Programming_Guide:L22049-L22055].
2. It is not always possible to insert global barriers where required [CUDA_C_Programming_Guide:L22049-L22055].

The `cudaMemAttachHost` flag exists both to simplify this process and to address scenarios where global barriers are not feasible [CUDA_C_Programming_Guide:L22049-L22055].
