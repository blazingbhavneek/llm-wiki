# CUDA Dynamic Parallelism Events

Inter-stream synchronization capabilities of CUDA events within the device runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L13949-L13953

Citation: [CUDA_C_Programming_Guide:L13949-L13953]

````text
## 13.3.1.3 Events

Only the inter-stream synchronization capabilities of CUDA events are supported. This means that cudaStreamWaitEvent() is supported, but cudaEventSynchronize(), cudaEventElapsedTime(), and cudaEventQuery() are not. As cudaEventElapsedTime() is not supported, cudaEvents must be created via cudaEventCreateWithFlags(), passing the cudaEventDisableTiming flag.

As with named streams, event objects may be shared between all threads within the grid which created them but are local to that grid and may not be passed to other kernels. Event handles are not guaranteed to be unique between grids, so using an event handle within a grid that did not create it will result in undefined behavior.
````
