# CDP1 Ordering and Concurrency

In CUDA Dynamic Parallelism version 1 (CDP1), the ordering and concurrency of kernel launches from the device runtime follow specific rules based on CUDA Stream semantics and thread block execution. While CDP1 facilitates easier expression of concurrency within a program, it does not introduce new concurrency guarantees beyond the standard CUDA execution model.

## Stream Ordering Semantics

The ordering of kernel launches from the device runtime adheres to CUDA Stream ordering semantics [CUDA_C_Programming_Guide:L14343-L14359].

### Intra-Block Ordering

Within a single thread block, all kernel launches directed into the same stream are executed in-order [CUDA_C_Programming_Guide:L14343-L14359]. If multiple threads within the same thread block launch kernels into the same stream, the specific ordering of these launches depends on the thread scheduling within that block [CUDA_C_Programming_Guide:L14343-L14359]. This scheduling can be controlled using synchronization primitives such as `__syncthreads()` [CUDA_C_Programming_Guide:L14343-L14359].

### Implicit vs. Explicit Streams

Streams are shared by all threads within a thread block, including the implicit NULL stream [CUDA_C_Programming_Guide:L14343-L14359]. Consequently, if multiple threads in a thread block launch kernels into the implicit stream, these launches are guaranteed to be executed in-order [CUDA_C_Programming_Guide:L14343-L14359]. To achieve concurrency between kernel launches from different threads within the same block, explicit named streams must be used [CUDA_C_Programming_Guide:L14343-L14359].

## Concurrency Guarantees

CDP1 does not guarantee concurrent execution between different thread blocks on a device [CUDA_C_Programming_Guide:L14343-L14359]. This lack of concurrency guarantee extends to the relationship between parent thread blocks and their child grids [CUDA_C_Programming_Guide:L14343-L14359].

### Parent-Child Execution

When a parent thread block launches a child grid, there is no guarantee that the child grid will begin execution until the parent thread block reaches an explicit synchronization point, such as `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L14343-L14359].

> **Warning:** Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14343-L14359].

### Unreliability of Concurrency

While concurrency between different thread blocks may often be achieved in practice, it is not guaranteed and may vary based on device configuration, application workload, and runtime scheduling [CUDA_C_Programming_Guide:L14343-L14359]. Therefore, it is unsafe to depend upon any concurrency between different thread blocks [CUDA_C_Programming_Guide:L14343-L14359].

## See Also

For the CDP2 version of these ordering and concurrency rules, see the relevant documentation section for CDP2.
