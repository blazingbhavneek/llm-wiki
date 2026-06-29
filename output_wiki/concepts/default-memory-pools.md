# Default Memory Pools

The default memory pool, also known as an implicit pool, is a memory resource associated with a specific device that does not require explicit creation by the application [CUDA_C_Programming_Guide:L15495-L15498].

## Retrieval and Characteristics

The default memory pool of a device can be retrieved using the `cudaDeviceGetDefaultMempool` API [CUDA_C_Programming_Guide:L15495-L15498]. Allocations made from the default memory pool of a device are classified as non-migratable device allocations located on that specific device [CUDA_C_Programming_Guide:L15495-L15498]. Consequently, these allocations are always accessible from the device on which they reside [CUDA_C_Programming_Guide:L15495-L15498].

## Accessibility Management

The accessibility of the default memory pool can be modified using the `cudaMemPoolSetAccess` function [CUDA_C_Programming_Guide:L15495-L15498]. The current accessibility settings can be queried using the `cudaMemPoolGetAccess` function [CUDA_C_Programming_Guide:L15495-L15498].

## Limitations

The default memory pool of a device does not support Inter-Process Communication (IPC) [CUDA_C_Programming_Guide:L15495-L15498].

## Related APIs

*   `cudaDeviceGetDefaultMempool`: Retrieves the default memory pool for a device.
*   `cudaMemPoolSetAccess`: Modifies the accessibility of a memory pool.
*   `cudaMemPoolGetAccess`: Queries the accessibility of a memory pool.
