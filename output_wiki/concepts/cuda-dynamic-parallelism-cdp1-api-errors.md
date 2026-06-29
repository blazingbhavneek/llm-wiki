# CUDA Dynamic Parallelism (CDP1) API Errors

In CUDA Dynamic Parallelism version 1 (CDP1), error handling follows the standard CUDA runtime model but with specific considerations for device-side execution contexts.

## Launch Failures

Similar to host-side launches, device-side kernel launches may fail for various reasons, such as invalid arguments. To determine if a launch generated an error, the user must call `cudaGetLastError()` [CUDA_C_Programming_Guide:L14643-L14652].

### Per-Thread Error Tracking

As with the general CUDA runtime, any function may return an error code. The last error code returned is recorded and can be retrieved via the `cudaGetLastError()` call [CUDA_C_Programming_Guide:L14643-L14652]. Errors are recorded on a per-thread basis, allowing each thread to identify the most recent error it has generated [CUDA_C_Programming_Guide:L14643-L14652]. The error code is of type `cudaError_t` [CUDA_C_Programming_Guide:L14643-L14652].

### Asynchronous Nature of Launches

It is important to note that a lack of an error immediately after a launch does not imply that the child kernel completed successfully [CUDA_C_Programming_Guide:L14643-L14652].

## Device-Side Exceptions

For device-side exceptions, such as access to an invalid address, the error handling mechanism differs from standard launch failures. In these cases, an error in a child grid is returned to the host instead of being returned by the parent’s call to `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L14643-L14652].

## See Also

For the CDP2 version of this documentation, see API Errors and Launch Failures (CDP2) [CUDA_C_Programming_Guide:L14643-L14652].
