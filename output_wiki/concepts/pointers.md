# Pointers

Rules for pointer dereferencing across host/device boundaries and usage of addresses for device/shared/constant variables.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16847-L16852

Citation: [CUDA_C_Programming_Guide:L16847-L16852]

````text
## 18.5.4. Pointers

Dereferencing a pointer either to global or shared memory in code that is executed on the host, or to host memory in code that is executed on the device results in an undefined behavior, most often in a segmentation fault and application termination.

The address obtained by taking the address of a \_\_device\_\_, \_\_shared\_\_ or \_\_constant\_\_ variable can only be used in device code. The address of a \_\_device\_\_ or \_\_constant\_\_ variable obtained through cudaGetSymbolAddress() as described in Device Memory can only be used in host code.
````
