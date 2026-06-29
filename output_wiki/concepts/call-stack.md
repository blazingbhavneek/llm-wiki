# Call Stack

On devices with compute capability 2.x and higher, the size of the call stack is configurable. The size can be queried using `cudaDeviceGetLimit()` and set using `cudaDeviceSetLimit()`.

## Overflow and Compiler Warnings

When the call stack overflows, the behavior depends on the execution environment:

*   If the application is run via a CUDA debugger (such as CUDA-GDB or Nsight), the kernel call fails with a specific stack overflow error.
*   Otherwise, the kernel call fails with an unspecified launch error.

The compiler issues a warning stating "Stack size cannot be statically determined" when it cannot determine the stack size, which is usually the case with recursive functions. Once this warning is issued, the user must set the stack size manually if the default stack size is not sufficient [CUDA_C_Programming_Guide:L3638-L3643].
