# CUDA Symbol Addresses on Device

## Overview

Device-side symbols, specifically those marked with the `__device__` qualifier, are accessible directly from within CUDA kernels. Because all global-scope device variables reside in the kernel's visible address space, they can be referenced using the address-of operator (`&`).

## Direct Symbol Referencing

Within a kernel, a `__device__` symbol can be accessed directly by its name or by taking its address using the `&` operator. This mechanism applies to `__constant__` symbols as well, with the critical distinction that pointers to `__constant__` space reference read-only data.

## Device Runtime Limitations

Since device-side symbols can be referenced directly from within kernels, the CUDA runtime APIs typically used to manage symbol addresses on the host are redundant in the device context. Consequently, the following APIs are **not supported** by the device runtime:

*   `cudaMemcpyToSymbol()`
*   `cudaGetSymbolAddress()`

## Imlications for Constant Data

The inability to use device runtime APIs to modify symbol addresses or data implies that constant data cannot be altered from within a running kernel. This restriction holds even ahead of a child kernel launch, as references to `__constant__` space are strictly read-only.

## References

- [CUDA_C_Programming_Guide:L14008-L14013]
