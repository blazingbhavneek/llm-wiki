# Synchronization API Actions

Synchronization API actions represent an optimization enabled by the integration of the memory allocator with the CUDA driver. This integration allows the driver to manage memory state more efficiently during synchronization operations.

## Mechanism

When a user requests the CUDA driver to synchronize, the driver performs the following steps:

1.  **Wait for Completion**: The driver waits for all asynchronous work to complete [CUDA_C_Programming_Guide:L15858-L15861].
2.  **Guarantee Frees**: Before returning, the driver determines which memory frees are guaranteed to be completed by the synchronization point [CUDA_C_Programming_Guide:L15858-L15861].
3.  **Availability**: These allocations are made available for future allocation requests, regardless of the specified stream or any disabled allocation policies [CUDA_C_Programming_Guide:L15858-L15861].
4.  **Release Threshold**: The driver also checks the `cudaMemPoolAttrReleaseThreshold` attribute and releases any excess physical memory that it can at this time [CUDA_C_Programming_Guide:L15858-L15861].

## Implications

This behavior ensures that memory freed by asynchronous operations is reclaimed and made available for reuse as soon as the synchronization API confirms the completion of those operations, rather than waiting for explicit pool management calls or other triggers. It also facilitates automatic memory release to the host system when the pool's usage exceeds the defined release threshold during a synchronization event.
