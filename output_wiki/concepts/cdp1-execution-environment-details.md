# CDP1 Execution Environment Details

The CUDA execution model is based on primitives of threads, thread blocks, and grids, with kernel functions defining the program executed by individual threads within a thread block and grid [CUDA_C_Programming_Guide:L14296-L14303]. When a kernel function is invoked, the grid’s properties are described by an execution configuration, which has a special syntax in CUDA [CUDA_C_Programming_Guide:L14296-L14303].

Support for dynamic parallelism in CUDA extends the ability to configure, launch, and synchronize upon new grids to threads that are running on the device [CUDA_C_Programming_Guide:L14296-L14303].

## Deprecation Warning

Explicit synchronization with child kernels from a parent block (i.e. using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14296-L14303].

## See Also

For the CDP2 version of this document, see Execution Environment, above [CUDA_C_Programming_Guide:L14296-L14303].
