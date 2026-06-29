# CUDA Dynamic Parallelism (CDP1) Device-side Launch from PTX

This section provides the low-level details related to supporting kernel launches at the PTX level, intended for programming language and compiler implementers who target Parallel Thread Execution (PTX) and plan to support Dynamic Parallelism in their language [CUDA_C_Programming_Guide:L14687-L14698].

## Kernel Launch APIs (CDP1)

Device-side kernel launches can be implemented using the following two APIs accessible from PTX [CUDA_C_Programming_Guide:L14687-L14698]:

*   `cudaLaunchDevice()`
*   `cudaGetParameterBuffer()`

`cudaLaunchDevice()` launches the specified kernel with the parameter buffer that is obtained by calling `cudaGetParameterBuffer()` and filled with the parameters to the launched kernel [CUDA_C_Programming_Guide:L14687-L14698]. The parameter buffer can be `NULL`, meaning there is no need to invoke `cudaGetParameterBuffer()`, if the launched kernel does not take any parameters [CUDA_C_Programming_Guide:L14687-L14698].
