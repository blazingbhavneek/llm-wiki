# CUDA Memory Allocation and Lifetime

The functions `cudaMalloc()` and `cudaFree()` exhibit distinct semantics depending on whether they are invoked from the host or the device environment [CUDA_C_Programming_Guide:L14244-L14250].

## Host-Side Allocation

When `cudaMalloc()` is invoked from the host, it allocates a new region from the unused device memory [CUDA_C_Programming_Guide:L14244-L14250]. The corresponding `cudaFree()` call must also be performed from the host to release this memory [CUDA_C_Programming_Guide:L14244-L14250]. The allocation limit for host-side allocations is determined by the available free device memory [CUDA_C_Programming_Guide:L14244-L14250].

## Device-Side Allocation

When invoked from the device runtime, `cudaMalloc()` and `cudaFree()` map to device-side `malloc()` and `free()` functions [CUDA_C_Programming_Guide:L14244-L14250]. This implies that within the device environment, the total allocatable memory is limited to the device `malloc()` heap size, which may be smaller than the total available unused device memory [CUDA_C_Programming_Guide:L14244-L14250]. The allocation limit for device-side allocations is governed by `cudaLimitMallocHeapSize` [CUDA_C_Programming_Guide:L14244-L14250].

## Cross-Environment Errors

It is an error to invoke `cudaFree()` from the host program on a pointer that was allocated by `cudaMalloc()` on the device, and vice-versa [CUDA_C_Programming_Guide:L14244-L14250]. The following table summarizes the supported combinations:

| | cudaMalloc() on Host | cudaMalloc() on Device |
| :--- | :---: | :---: |
| **cudaFree() on Host** | Supported | Not Supported |
| **cudaFree() on Device** | Not Supported | Supported |

| Allocation Limit | Free device memory | cudaLimitMallocHeapSize |
| :--- | :--- | :--- |

</source> }
