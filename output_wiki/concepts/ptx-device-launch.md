# PTX Device-Side Launch

This section is intended for programming language and compiler implementers targeting Parallel Thread Execution (PTX) who plan to support Dynamic Parallelism. It provides the low-level details required to support kernel launches at the PTX level [CUDA_C_Programming_Guide:L14051-L14057].

## Kernel Launch APIs

Device-side kernel launches are implemented using two specific APIs accessible from PTX [CUDA_C_Programming_Guide:L14051-L14057]:

*   `cudaLaunchDevice()`
*   `cudaGetParameterBuffer()`

The `cudaLaunchDevice()` function launches the specified kernel using a parameter buffer obtained by calling `cudaGetParameterBuffer()`. This buffer must be filled with the parameters for the launched kernel [CUDA_C_Programming_Guide:L14051-L14057].

If the kernel being launched does not take any parameters, the parameter buffer can be `NULL`, in which case there is no need to invoke `cudaGetParameterBuffer()` [CUDA_C_Programming_Guide:L14051-L14057].
