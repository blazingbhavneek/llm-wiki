# CUDA Dynamic Parallelism (CDP1) Symbol Addresses

In CUDA Dynamic Parallelism (CDP1), device-side symbols can be accessed directly from within kernels, altering how symbol management is handled compared to host-side execution.

## Accessing Device Symbols

Device-side symbols, specifically those marked with the `__device__` qualifier, may be referenced from within a kernel simply via the address-of operator (`&`) [CUDA_C_Programming_Guide:L14634-L14642]. This is possible because all global-scope device variables reside in the kernel's visible address space [CUDA_C_Programming_Guide:L14634-L14642].

## Constant Symbols

The `&` operator also applies to `__constant__` symbols [CUDA_C_Programming_Guide:L14634-L14642]. However, pointers obtained for constant symbols reference read-only data [CUDA_C_Programming_Guide:L14634-L14642]. Consequently, constant data cannot be altered from within a running kernel, even ahead of a child kernel launch [CUDA_C_Programming_Guide:L14634-L14642].

## Unsupported Runtime APIs

Because device-side symbols can be referenced directly, CUDA runtime APIs that traditionally reference symbols are redundant and therefore not supported by the device runtime in CDP1 [CUDA_C_Programming_Guide:L14634-L14642]. This includes:

*   `cudaMemcpyToSymbol()`
*   `cudaGetSymbolAddress()`

[CUDA_C_Programming_Guide:L14634-L14642]

> **Note:** For the CDP2 version of this document, see the section on Symbol Addresses (CDP2).

[CUDA_C_Programming_Guide:L14634-L14642]
