# CDP1 Scope of CUDA Primitives

In the context of CUDA Dynamic Parallelism version 1 (CDP1), the visibility and sharing of CUDA primitives such as streams and events are strictly bound to the thread block hierarchy.

## Scope on the Host
On the host system, the CUDA runtime provides APIs for launching kernels, waiting for launched work to complete, and tracking dependencies between launches via streams and events [CUDA_C_Programming_Guide:L14313-L14322]. The state of these launches and the CUDA primitives referencing streams and events are shared by all threads within a process [CUDA_C_Programming_Guide:L14313-L14322]. However, processes execute independently and may not share CUDA objects [CUDA_C_Programming_Guide:L14313-L14322].

## Scope on the Device
A similar hierarchy exists on the device, where launched kernels and CUDA objects are visible to all threads in a thread block, but are independent between thread blocks [CUDA_C_Programming_Guide:L14313-L14322]. This means that a stream may be created by one thread and used by any other thread in the same thread block, but may not be shared with threads in any other thread block [CUDA_C_Programming_Guide:L14313-L14322].

## Deprecation Warning
Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14313-L14322].

## See Also
For the CDP2 version of this document, see Scope of CUDA Primitives, above.
