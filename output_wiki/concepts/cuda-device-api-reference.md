# CUDA Device API Reference

The CUDA Runtime API functions supported in the device runtime are detailed below. Host and device runtime APIs have identical syntax; semantics are the same except where indicated [CUDA_C_Programming_Guide:L14044-L14050].

The following table provides an overview of the API relative to the version available from the host [CUDA_C_Programming_Guide:L14044-L14050].

## Supported API Functions

| Runtime API Functions | Details |
| :--- | :--- |
| `cudaDeviceGetCacheConfig` | | |
| `cudaDeviceGetLimit` | | |
| `cudaGetLastError` | Last error is per-thread state, not per-block state |
| `cudaPeekAtLastError` | | |
| `cudaGetErrorString` | | |
| `cudaGetDeviceCount` | | |
| `cudaDeviceGetAttribute` | Will return attributes for any device |
| `cudaGetDevice` | Always returns current device ID as would be seen from host |
| `cudaStreamCreateWithFlags` | Must pass `cudaStreamNonBlocking` flag |
| `cudaStreamDestroy` | | |
| `cudaStreamWaitEvent` | | |
| `cudaEventCreateWithFlags` | Must pass `cudaEventDisableTiming` flag |
| `cudaEventRecord` | | |
| `cudaEventDestroy` | | |
| `cudaFuncGetAttributes` | | |
| `cudaMemcpyAsync` | rowspan="4" Notes about all memcpy/memset functions:<br>► Only async memcpy/set functions are supported<br>► Only device-to-device memcpy is permitted<br>► May not pass in local or shared memory pointers |
| `cudaMemcpy2DAsync` | |
| `cudaMemcpy3DAsync` | |
| `cudaMemsetAsync` | |
| `cudaMemset2DAsync` | |
| `cudaMemset3DAsync` | |
| `cudaRuntimeGetVersion` | | |
| `cudaMalloc` | rowspan="2" May not call `cudaFree` on the device on a pointer created on the host, and vice-versa |
| `cudaFree` | |
| `cudaOccupancyMaxActiveBlocksPerMulti-processor` | | |
| `cudaOccupancyMaxPotentialBlockSize` | | |
| `cudaOccupancyMaxPotentialBlockSize-VariableSMem` | |

[CUDA_C_Programming_Guide:L14044-L14050]
