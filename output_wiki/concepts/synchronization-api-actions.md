# Synchronization API Actions

Details how the CUDA driver synchronizes and releases memory based on stream-ordered allocation policies, including checking release thresholds and making freed allocations available.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15859-L15861

Citation: [CUDA_C_Programming_Guide:L15859-L15861]

````text
## 15.12. Synchronization API Actions

One of the optimizations that comes with the allocator being part of the CUDA driver is integration with the synchronize APIs. When the user requests that the CUDA driver synchronize, the driver waits for asynchronous work to complete. Before returning, the driver will determine what frees the synchronization guaranteed to be completed. These allocations are made available for allocation regardless of specified stream or disabled allocation policies. The driver also checks cudaMemPoolAttrReleaseThreshold here and releases any excess physical memory that it can.
````
