# CDP1 Synchronization

This section covers synchronization behavior specific to CUDA Dynamic Parallelism version 1 (CDP1). For synchronization details in CDP2, refer to the general Synchronization section.

## Deprecation of Explicit Synchronization

Explicit synchronization with child kernels from a parent block, such as using `cudaDeviceSynchronize()` in device code, is deprecated in CUDA 11.6. This functionality has been removed for compilation targeting compute capability 9.0 and higher, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14323-L14332].

## Implicit Synchronization and Visibility

CUDA runtime operations, including kernel launches, are visible across a thread block. This visibility allows an invoking thread in the parent grid to perform synchronization on:

* Grids launched by that thread.
* Grids launched by other threads within the same thread block.
* Streams created within the same thread block [CUDA_C_Programming_Guide:L14323-L14332].

Execution of a thread block is not considered complete until all launches by all threads in that block have finished. Consequently, if all threads in a block exit before all child launches have completed, a synchronization operation is automatically triggered to ensure completion [CUDA_C_Programming_Guide:L14323-L14332].
