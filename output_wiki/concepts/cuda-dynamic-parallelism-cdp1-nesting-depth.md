# CUDA Dynamic Parallelism (CDP1) Nesting and Synchronization Depth

In CUDA Dynamic Parallelism (CDP1), the device runtime allows kernels to launch other kernels recursively. Each subordinate launch creates a new nesting level, and the total count of these levels defines the **nesting depth** of the program [CUDA_C_Programming_Guide:L14926-L14941].

## Nesting Depth Limits

The overall maximum nesting depth is limited to 24 [CUDA_C_Programming_Guide:L14926-L14941]. However, practical limits are often determined by the system memory required to support each new nesting level [CUDA_C_Programming_Guide:L14926-L14941]. Any launch that would result in a kernel at a depth exceeding the maximum will fail [CUDA_C_Programming_Guide:L14926-L14941]. This limit also applies to `cudaMemcpyAsync()`, which may internally generate a kernel launch [CUDA_C_Programming_Guide:L14926-L14941].

## Synchronization Depth

The **synchronization depth** is defined as the deepest level at which the program explicitly synchronizes on a child launch, typically using `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L14926-L14941]. 

- **Default:** By default, sufficient storage is reserved for two levels of synchronization [CUDA_C_Programming_Guide:L14926-L14941].
- **Configuration:** The maximum synchronization depth can be controlled by calling `cudaDeviceSetLimit()` with the argument `cudaLimitDevRuntimeSyncDepth` [CUDA_C_Programming_Guide:L14926-L14941].
- **Timing:** This configuration must be set before the top-level kernel is launched from the host to guarantee successful execution [CUDA_C_Programming_Guide:L14926-L14941].
- **Error Handling:** Calling `cudaDeviceSynchronize()` at a depth greater than the specified maximum synchronization depth will return an error [CUDA_C_Programming_Guide:L14926-L14941].

The synchronization depth may differ substantially from the nesting depth if the program does not call `cudaDeviceSynchronize()` at all levels [CUDA_C_Programming_Guide:L14926-L14941]. An optimization allows the system to avoid reserving space for a parent's state if the parent kernel never calls `cudaDeviceSynchronize()`, significantly reducing the memory footprint [CUDA_C_Programming_Guide:L14926-L14941].

## Deprecation Warning

Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6 [CUDA_C_Programming_Guide:L14926-L14941]. It has been removed for compilation with compute capability 9.0+ and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14926-L14941].

For the updated behavior and limits, refer to the CUDA Dynamic Parallelism (CDP2) documentation [CUDA_C_Programming_Guide:L14926-L14941].
