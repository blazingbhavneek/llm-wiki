# CUDA Dynamic Parallelism (CDP1) Memory Allocation

In CUDA Dynamic Parallelism version 1 (CDP1), memory allocation semantics differ significantly between the host and device environments. While `cudaMalloc()` and `cudaFree()` are available in both contexts, their behavior and constraints are distinct [CUDA_C_Programming_Guide:L14964-L14971].

## Host vs. Device Semantics

When invoked from the **host**, `cudaMalloc()` allocates a new region from unused device memory, subject to the total available free device memory [CUDA_C_Programming_Guide:L14964-L14971].

When invoked from the **device runtime**, these functions map to device-side `malloc()` and `free()` operations [CUDA_C_Programming_Guide:L14964-L14971]. This implies that within the device environment, the total allocatable memory is limited to the device `malloc()` heap size, which may be smaller than the available unused device memory [CUDA_C_Programming_Guide:L14964-L14971].

## Allocation Limits

The limit for device-side allocations is controlled by the `cudaLimitMallocHeapSize` parameter [CUDA_C_Programming_Guide:L14964-L14971]. This limit applies specifically to memory allocated via `cudaMalloc()` when called from the device [CUDA_C_Programming_Guide:L14964-L14971].

## Cross-Boundary Restrictions

It is an error to invoke `cudaFree()` from the host program on a pointer that was allocated by `cudaMalloc()` on the device, or vice-versa [CUDA_C_Programming_Guide:L14964-L14971]. The following table summarizes the supported combinations:

| Operation | Host | Device |
| :--- | :--- | :--- |
| **`cudaMalloc()` on Host** | Supported | Not Supported |
| **`cudaMalloc()` on Device** | Not Supported | Supported |
| **`cudaFree()` on Host** | Supported | Not Supported |
| **`cudaFree()` on Device** | Not Supported | Supported |

For CDP2, see the separate documentation on Memory Allocation and Lifetime [CUDA_C_Programming_Guide:L14964-L14971].
