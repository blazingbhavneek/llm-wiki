# Pointers

## Overview
Pointers in CUDA C++ must respect the memory space boundaries between the host (CPU) and the device (GPU). Incorrect usage, such as dereferencing memory pointers across these boundaries, leads to undefined behavior.

## Host-Device Memory Access Rules
Dereferencing a pointer to global or shared memory in code executed on the host, or dereferencing a pointer to host memory in code executed on the device, results in undefined behavior. This typically manifests as a segmentation fault and application termination [CUDA_C_Programming_Guide:L16847-L16852].

## Address Usage Restrictions
The usage of addresses obtained from specific device memory qualifiers is restricted based on the execution context:

*   **Device Code Only**: The address obtained by taking the address of a `__device__`, `__shared__`, or `__constant__` variable can only be used in device code [CUDA_C_Programming_Guide:L16847-L16852].
*   **Host Code Only**: The address of a `__device__` or `__constant__` variable obtained through `cudaGetSymbolAddress()` can only be used in host code [CUDA_C_Programming_Guide:L16847-L16852].

## Related Concepts
*   Device Memory
*   cudaGetSymbolAddress
