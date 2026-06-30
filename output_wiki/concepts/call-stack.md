# Call Stack

Call stack size can be queried and set on compute capability 2.x+ devices using cudaDeviceGetLimit() and cudaDeviceSetLimit(). Stack overflow causes kernel failure or warnings, especially for recursive functions. Manual stack size configuration is required when the compiler cannot determine it statically.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3638-L3643

Citation: [CUDA_C_Programming_Guide:L3638-L3643]

````text
## 6.2.13. Call Stack

On devices of compute capability 2.x and higher, the size of the call stack can be queried usingcudaDeviceGetLimit() and set using cudaDeviceSetLimit().

When the call stack overflows, the kernel call fails with a stack overflow error if the application is run via a CUDA debugger (CUDA-GDB, Nsight) or an unspecified launch error, otherwise. When the compiler cannot determine the stack size, it issues a warning saying Stack size cannot be statically determined. This is usually the case with recursive functions. Once this warning is issued, user will need to set stack size manually if default stack size is not suficient.
````
