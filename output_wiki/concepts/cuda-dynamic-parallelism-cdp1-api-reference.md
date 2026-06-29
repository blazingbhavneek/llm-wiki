# CUDA Dynamic Parallelism (CDP1) API Reference

This page details the portions of the CUDA Runtime API that are supported when executing from device code under the CUDA Dynamic Parallelism version 1 (CDP1) model. While the host and device runtime APIs share identical syntax, their semantics differ in specific areas, particularly regarding synchronization scope, error handling, and memory management constraints.

## Synchronization and Device State

Device code has limited synchronization capabilities compared to host code. The primary synchronization function is `cudaDeviceSynchronize`, which synchronizes on work launched from the thread's own block only [CUDA_C_Programming_Guide:L14676-L14684]. 

**Deprecation Warning:** Calling `cudaDeviceSynchronize` from device code is deprecated in CUDA 11.6, removed for `compute_90+` compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14676-L14684].

Other device state queries are supported with specific behaviors:
*   `cudaDeviceGetCacheConfig`: Supported [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaDeviceGetLimit`: Supported [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaDeviceGetAttribute`: Returns attributes for any device [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaGetDevice`: Always returns the current device ID as it would be seen from the host [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaRuntimeGetVersion`: Supported [CUDA_C_Programming_Guide:L14676-L14684].

## Error Handling

Error handling in device code differs from host code in that the last error is considered per-thread state, not per-block state [CUDA_C_Programming_Guide:L14676-L14684]. The following functions are supported:
*   `cudaGetLastError` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaPeekAtLastError` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaGetErrorString` [CUDA_C_Programming_Guide:L14676-L14684]

## Streams and Events

Stream and event management is supported but with strict flag requirements:
*   `cudaStreamCreateWithFlags`: The `cudaStreamNonBlocking` flag must be passed [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaStreamDestroy`: Supported [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaStreamWaitEvent`: Supported [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaEventCreateWithFlags`: The `cudaEventDisableTiming` flag must be passed [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaEventRecord`: Supported [CUDA_C_Programming_Guide:L14676-L14684].
*   `cudaEventDestroy`: Supported [CUDA_C_Programming_Guide:L14676-L14684].

## Memory Management

Memory allocation and copying from device code are subject to significant restrictions:

### Allocation
*   `cudaMalloc` and `cudaFree` are supported [CUDA_C_Programming_Guide:L14676-L14684].
*   **Cross-Context Restriction:** You may not call `cudaFree` on the device on a pointer created on the host, and vice-versa [CUDA_C_Programming_Guide:L14676-L14684].

### Memory Copies and Sets
Only asynchronous memory copy and set functions are supported [CUDA_C_Programming_Guide:L14676-L14684]. The following functions are available:
*   `cudaMemcpyAsync` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaMemcpy2DAsync` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaMemcpy3DAsync` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaMemsetAsync` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaMemset2DAsync` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaMemset3DAsync` [CUDA_C_Programming_Guide:L14676-L14684]

**Restrictions on Memory Operations:**
1.  Only device-to-device memory copies are permitted [CUDA_C_Programming_Guide:L14676-L14684].
2.  Local or shared memory pointers may not be passed as arguments to these functions [CUDA_C_Programming_Guide:L14676-L14684].

## Occupancy and Function Attributes

The following functions are supported for querying function attributes and occupancy:
*   `cudaFuncGetAttributes` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaOccupancyMaxActiveBlocksPerMultiprocessor` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaOccupancyMaxPotentialBlockSize` [CUDA_C_Programming_Guide:L14676-L14684]
*   `cudaOccupancyMaxPotentialBlockSizeVariableSMem` [CUDA_C_Programming_Guide:L14676-L14684]

## Summary of Supported Functions

The following table summarizes the API functions supported in the device runtime for CDP1, along with specific details or constraints relative to the host version [CUDA_C_Programming_Guide:L14676-L14684].

| Runtime API Functions | Details |
| :--- | :--- |
| `cudaDeviceSynchronize` | Synchronizes on work launched from thread's own block only. **Deprecated in CUDA 11.6, removed for compute_90+, slated for full removal.** |
| `cudaDeviceGetCacheConfig` | Supported |
| `cudaDeviceGetLimit` | Supported |
| `cudaGetLastError` | Last error is per-thread state, not per-block state |
| `cudaPeekAtLastError` | Supported |
| `cudaGetErrorString` | Supported |
| `cudaGetDeviceCount` | Supported |
| `cudaDeviceGetAttribute` | Will return attributes for any device |
| `cudaGetDevice` | Always returns current device ID as would be seen from host |
| `cudaStreamCreateWithFlags` | Must pass `cudaStreamNonBlocking` flag |
| `cudaStreamDestroy` | Supported |
| `cudaStreamWaitEvent` | Supported |
| `cudaEventCreateWithFlags` | Must pass `cudaEventDisableTiming` flag |
| `cudaEventRecord` | Supported |
| `cudaEventDestroy` | Supported |
| `cudaFuncGetAttributes` | Supported |
| `cudaMemcpyAsync` | See notes below |
| `cudaMemcpy2DAsync` | See notes below |
| `cudaMemcpy3DAsync` | See notes below |
| `cudaMemsetAsync` | See notes below |
| `cudaMemset2DAsync` | See notes below |
| `cudaMemset3DAsync` | See notes below |
| `cudaRuntimeGetVersion` | Supported |
| `cudaMalloc` | See notes below |
| `cudaFree` | See notes below |
| `cudaOccupancyMaxActiveBlocksPerMultiprocessor` | Supported |
| `cudaOccupancyMaxPotentialBlockSize` | Supported |
| `cudaOccupancyMaxPotentialBlockSizeVariableSMem` | Supported |

**Notes for Memory Functions:**
*   Only async memcpy/set functions are supported.
*   Only device-to-device memcpy is permitted.
*   May not pass in local or shared memory pointers.

**Notes for Allocation Functions:**
*   May not call `cudaFree` on the device on a pointer created on the host, and vice-versa.
