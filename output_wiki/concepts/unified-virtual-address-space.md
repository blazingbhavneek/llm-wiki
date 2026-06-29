# Unified Virtual Address Space (UVA)

Unified Virtual Address Space (UVA) is a feature available in 64-bit CUDA applications that provides a single, unified virtual address space for the host and all devices with compute capability 2.0 or higher [CUDA_C_Programming_Guide:L3598-L3609].

## Key Characteristics

### Single Address Space
When an application runs as a 64-bit process, all host memory allocations made via CUDA API calls and all device memory allocations on supported devices reside within the same virtual address range [CUDA_C_Programming_Guide:L3598-L3609].

### Pointer Location and Attributes
Because host and device memory share the same address space, the location of any memory can be determined directly from the pointer value [CUDA_C_Programming_Guide:L3598-L3609]. This is achieved using the `cudaPointerGetAttributes()` function, which can identify whether a pointer refers to host or device memory [CUDA_C_Programming_Guide:L3598-L3609].

### Simplified Memory Copies
The `cudaMemcpyDefault` parameter can be used with `cudaMemcpy*()` functions when copying to or from memory in a UVA environment [CUDA_C_Programming_Guide:L3598-L3609]. This setting automatically determines the source and destination locations based on the pointers provided [CUDA_C_Programming_Guide:L3598-L3609]. This functionality also extends to host pointers that were not allocated through CUDA, provided the current device supports unified addressing [CUDA_C_Programming_Guide:L3598-L3609].

### Portable Host Memory
Memory allocated via `cudaHostAlloc()` is automatically portable across all devices that use the unified address space [CUDA_C_Programming_Guide:L3598-L3609]. Pointers returned by `cudaHostAlloc()` can be used directly within kernels running on these devices, eliminating the need to obtain a separate device pointer using `cudaHostGetDevicePointer()` [CUDA_C_Programming_Guide:L3598-L3609].

## Verification

Applications can verify if a specific device supports the unified address space by checking the `unifiedAddressing` device property [CUDA_C_Programming_Guide:L3598-L3609]. A value of 1 indicates that the device uses the unified address space [CUDA_C_Programming_Guide:L3598-L3609].
