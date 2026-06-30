# Graph Memory Footprint

Management of physical memory footprint for graphs, including trimming via cudaDeviceGraphMemTrim and querying attributes.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16243-L16248

Citation: [CUDA_C_Programming_Guide:L16243-L16248]

````text
## 16.6. Physical Memory Footprint

The pool-management behavior of asynchronous allocation means that destroying a graph which contains memory nodes (even if their allocations are free) will not immediately return physical memory to the OS for use by other processes. To explicitly release memory back to the OS, an application should use the cudaDeviceGraphMemTrim API.

cudaDeviceGraphMemTrim will unmap and release any physical memory reserved by graph memory nodes that is not actively in use. Allocations that have not been freed and graphs that are scheduled or running are considered to be actively using the physical memory and will not be impacted. Use of the trim API will make physical memory available to other allocation APIs and other applications or processes, but will cause CUDA to reallocate and remap memory when the trimmed graphs are next launched. Note that cudaDeviceGraphMemTrim operates on a diferent pool from cudaMem-PoolTrimTo(). The graph memory pool is not exposed to the steam ordered memory allocator. CUDA allows applications to query their graph memory footprint through the cudaDeviceGetGraphMemAttribute API. Querying the attribute cudaGraphMemAttrReservedMemCurrent returns the amount of physical memory reserved by the driver for graph allocations in the current process. Querying cudaGraphMemAttrUsedMemCurrent returns the amount of physical memory currently mapped by at least one graph. Either of these attributes can be used to track when new physical memory is acquired by CUDA for the sake of an allocating graph. Both of these attributes are useful for examining how much memory is saved by the sharing mechanism.
````
