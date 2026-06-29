# CUDA Device Errors and Launch Failures

## API Error Handling

In the CUDA runtime, any function may return an error code. The most recent error code is recorded and can be retrieved using the `cudaGetLastError()` call. These errors are recorded on a per-thread basis, allowing each thread to identify the most recent error it has generated. The error code is of type `cudaError_t` [CUDA_C_Programming_Guide:L14014-L14021].

## Device-Side Launch Failures

Similar to host-side launches, device-side kernel launches may fail for various reasons, such as invalid arguments. To determine if a launch generated an error, the user must call `cudaGetLastError()`. However, the absence of an error immediately after a launch does not imply that the child kernel completed successfully [CUDA_C_Programming_Guide:L14014-L14021].

## Device-Side Exceptions

Device-side exceptions, such as accessing an invalid memory address, result in errors within the child grid. These errors are returned to the host for handling [CUDA_C_Programming_Guide:L14014-L14021].
