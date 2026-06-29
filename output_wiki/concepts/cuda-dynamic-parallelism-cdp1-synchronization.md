# CUDA Dynamic Parallelism (CDP1) Synchronization

In CUDA Dynamic Parallelism version 1 (CDP1), explicit synchronization with child kernels from a parent block is handled via the `cudaDeviceSynchronize()` function. This mechanism allows a parent thread to wait for the completion of child kernels launched by threads within its block.

## Deprecation Status

Explicit synchronization using `cudaDeviceSynchronize()` in device code is deprecated in CUDA 11.6. It has been removed for compilation targeting compute capability 90 or higher and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14560-L14577].

## Function Behavior

The `cudaDeviceSynchronize()` function synchronizes on all work launched by any thread in the thread-block up to the point where the function was called [CUDA_C_Programming_Guide:L14560-L14577]. It may be called from within divergent code [CUDA_C_Programming_Guide:L14560-L14577].

## Block Wide Synchronization

`cudaDeviceSynchronize()` does not imply intra-block synchronization [CUDA_C_Programming_Guide:L14560-L14577]. Without explicit synchronization via a `__syncthreads()` directive, the calling thread can make no assumptions about what work has been launched by any thread other than itself [CUDA_C_Programming_Guide:L14560-L14577].

Programs must perform sufficient additional inter-thread synchronization if the calling thread is intended to synchronize with child grids invoked from other threads [CUDA_C_Programming_Guide:L14560-L14577]. For example, if multiple threads within a block are each launching work and synchronization is desired for all this work at once, the program must guarantee that this work is submitted by all threads before calling `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L14560-L14577].

## Concurrent Calls

Because the implementation is permitted to synchronize on launches from any thread in the block, simultaneous calls to `cudaDeviceSynchronize()` by multiple threads may have undefined effects on subsequent calls [CUDA_C_Programming_Guide:L14560-L14577]. It is possible that simultaneous calls will drain all work in the first call and have no effect for the later calls [CUDA_C_Programming_Guide:L14560-L14577].

## See Also

*   Synchronization (CDP2)
*   CUDA Dynamic Parallelism
