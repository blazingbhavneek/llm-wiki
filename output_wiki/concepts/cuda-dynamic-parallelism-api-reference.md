# CUDA Dynamic Parallelism API Reference

Overview table of CUDA Runtime API functions supported in the device runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14042-L14049

Citation: [CUDA_C_Programming_Guide:L14042-L14049]

````text

## 13.3.1.8 API Reference

The portions of the CUDA Runtime API supported in the device runtime are detailed here. Host and device runtime APIs have identical syntax; semantics are the same except where indicated. The following table provides an overview of the API relative to the version available from the host.

Table 14: Supported API Functions

<table><tr><td>Runtime API Functions</td><td>Details</td></tr><tr><td>cudaDeviceGetCacheConfig</td><td></td></tr><tr><td>cudaDeviceGetLimit</td><td></td></tr><tr><td>cudaGetLastError</td><td>Last error is per-thread state, not per-block state</td></tr><tr><td>cudaPeekAtLastError</td><td></td></tr><tr><td>cudaGetErrorString</td><td></td></tr><tr><td>cudaGetDeviceCount</td><td></td></tr><tr><td>cudaDeviceGetAttribute</td><td>Will return attributes for any device</td></tr><tr><td>cudaGetDevice</td><td>Always returns current device ID as would be seen from host</td></tr><tr><td>cudaStreamCreateWithFlags</td><td>Must pass cudaStreamNonBlocking flag</td></tr><tr><td>cudaStreamDestroy</td><td></td></tr><tr><td>cudaStreamWaitEvent</td><td></td></tr><tr><td>cudaEventCreateWithFlags</td><td>Must pass cudaEventDisableTiming flag</td></tr><tr><td>cudaEventRecord</td><td></td></tr><tr><td>cudaEventDestroy</td><td></td></tr><tr><td>cudaFuncGetAttributes</td><td></td></tr><tr><td>cudaMemcpyAsync</td><td rowspan="4">Notes about all memcpy/memset functions:► Only async memcpy/set functions are supported► Only device-to-device memcpy is permitted► May not pass in local or shared memory pointers</td></tr><tr><td>cudaMemcpy2DAsync</td></tr><tr><td>cudaMemcpy3DAsync</td></tr><tr><td>cudaMemsetAsync</td></tr><tr><td>cudaMemset2DAsync</td><td></td></tr><tr><td>cudaMemset3DAsync</td><td></td></tr><tr><td>cudaRuntimeGetVersion</td><td></td></tr><tr><td>cudaMalloc</td><td rowspan="2">May not call cudaFree on the device on a pointer created on the host, and vice-versa</td></tr><tr><td>cudaFree</td></tr><tr><td>cudaOccupancyMaxActiveBlocksPerMulti-processor</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize-VariableSMem</td><td></td></tr></table>
````
