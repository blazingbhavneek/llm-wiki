# Memory Pools

Memory pools encapsulate virtual address and physical memory resources that are allocated and managed according to the pool's attributes and properties. The primary aspect of a memory pool is the kind and location of memory it manages [CUDA_C_Programming_Guide:L15485-L15494].

## Allocation and Usage

All calls to `cudaMallocAsync` use the resources of a memory pool. In the absence of a specified memory pool, `cudaMallocAsync` uses the current memory pool of the supplied stream’s device [CUDA_C_Programming_Guide:L15485-L15494].

### Current Memory Pool

The current memory pool for a device may be set with `cudaDeviceSetMempool` and queried with `cudaDeviceGetMempool` [CUDA_C_Programming_Guide:L15485-L15494]. By default, in the absence of a `cudaDeviceSetMempool` call, the current memory pool is the default memory pool of a device [CUDA_C_Programming_Guide:L15485-L15494].

It is important to note that the mempool current to a device is local to that device. Therefore, allocating without specifying a memory pool will always yield an allocation local to the stream’s device [CUDA_C_Programming_Guide:L15485-L15494].

### Explicit Pool Specification

The APIs `cudaMallocFromPoolAsync` and C++ overloads of `cudaMallocAsync` allow a user to specify the pool to be used for an allocation without setting it as the current pool [CUDA_C_Programming_Guide:L15485-L15494]. Users can obtain handles to memory pools using `cudaDeviceGetDefaultMempool` and `cudaMemPoolCreate` [CUDA_C_Programming_Guide:L15485-L15494].

## Attributes

The attributes of memory pools are controlled by the APIs `cudaMemPoolSetAttribute` and `cudaMemPoolGetAttribute` [CUDA_C_Programming_Guide:L15485-L15494].

## See Also

- [CUDA C Programming Guide: Memory Pools](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#memory-pools)
