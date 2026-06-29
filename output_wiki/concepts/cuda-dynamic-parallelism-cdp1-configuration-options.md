# CUDA Dynamic Parallelism (CDP1) Configuration Options

Resource allocation for the device runtime system software in CUDA Dynamic Parallelism (CDP1) is controlled via the `cudaDeviceSetLimit()` API from the host program [CUDA_C_Programming_Guide:L14952-L14963]. Limits must be set before any kernel is launched and may not be changed while the GPU is actively running programs [CUDA_C_Programming_Guide:L14952-L14963].

## Warning: Deprecated Synchronization

Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14952-L14963].

## Named Limits

The following named limits may be set using `cudaDeviceSetLimit()`:

### cudaLimitDevRuntimeSyncDepth

Sets the maximum depth at which `cudaDeviceSynchronize()` may be called [CUDA_C_Programming_Guide:L14952-L14963]. Launches may be performed deeper than this limit, but explicit synchronization deeper than this limit will return the `cudaErrorLaunchMaxDepthExceeded` error [CUDA_C_Programming_Guide:L14952-L14963]. The default maximum sync depth is 2 [CUDA_C_Programming_Guide:L14952-L14963].

### cudaLimitDevRuntimePendingLaunchCount

Controls the amount of memory set aside for buffering kernel launches which have not yet begun to execute, due either to unresolved dependencies or lack of execution resources [CUDA_C_Programming_Guide:L14952-L14963]. When the buffer is full, the device runtime system software will attempt to track new pending launches in a lower performance virtualized buffer [CUDA_C_Programming_Guide:L14952-L14963]. If the virtualized buffer is also full (i.e., when all available heap space is consumed), launches will not occur, and the thread's last error will be set to `cudaErrorLaunchPendingCountExceeded` [CUDA_C_Programming_Guide:L14952-L14963]. The default pending launch count is 2048 launches [CUDA_C_Programming_Guide:L14952-L14963].

### cudaLimitStackSize

Controls the stack size in bytes of each GPU thread [CUDA_C_Programming_Guide:L14952-L14963]. The CUDA driver automatically increases the per-thread stack size for each kernel launch as needed [CUDA_C_Programming_Guide:L14952-L14963]. This size isn't reset back to the original value after each launch [CUDA_C_Programming_Guide:L14952-L14963]. To set the per-thread stack size to a different value, `cudaDeviceSetLimit()` can be called to set this limit [CUDA_C_Programming_Guide:L14952-L14963]. The stack will be immediately resized, and if necessary, the device will block until all preceding requested tasks are complete [CUDA_C_Programming_Guide:L14952-L14963]. `cudaDeviceGetLimit()` can be called to get the current per-thread stack size [CUDA_C_Programming_Guide:L14952-L14963].

## See Also

*   Configuration Options (CDP2)
