# Error Checking

All CUDA runtime functions return an error code to indicate success or failure [CUDA_C_Programming_Guide:L3626-L3637]. However, the behavior of these error codes differs between synchronous and asynchronous operations.

## Asynchronous Errors

For asynchronous functions, the returned error code only reports errors that occur on the host prior to executing the task, typically related to parameter validation [CUDA_C_Programming_Guide:L3626-L3637]. It cannot report asynchronous errors that occur on the device because the function returns before the device has completed the task [CUDA_C_Programming_Guide:L3626-L3637]. If an asynchronous error occurs, it will be reported by some subsequent unrelated runtime function call [CUDA_C_Programming_Guide:L3626-L3637].

The only way to check for asynchronous errors immediately after an asynchronous function call is to synchronize the device by calling `cudaDeviceSynchronize()` (or using other synchronization mechanisms) and checking the error code returned by that synchronization call [CUDA_C_Programming_Guide:L3626-L3637].

## Thread-Local Error Variables

The CUDA runtime maintains an error variable for each host thread, initialized to `cudaSuccess` [CUDA_C_Programming_Guide:L3626-L3637]. This variable is overwritten by the error code every time an error occurs, whether it is a parameter validation error or an asynchronous error [CUDA_C_Programming_Guide:L3626-L3637].

Two functions manage this thread-local state:
*   `cudaPeekAtLastError()`: Returns the current value of the error variable without modifying it [CUDA_C_Programming_Guide:L3626-L3637].
*   `cudaGetLastError()`: Returns the current value of the error variable and resets it to `cudaSuccess` [CUDA_C_Programming_Guide:L3626-L3637].

## Kernel Launch Error Checking

Kernel launches do not return any error code directly [CUDA_C_Programming_Guide:L3626-L3637]. To check for errors associated with a kernel launch, `cudaPeekAtLastError()` or `cudaGetLastError()` must be called just after the kernel launch to retrieve any pre-launch errors [CUDA_C_Programming_Guide:L3626-L3637].

To ensure that the error retrieved does not originate from calls prior to the kernel launch, the runtime error variable must be set to `cudaSuccess` immediately before the kernel launch, for example, by calling `cudaGetLastError()` just before the launch [CUDA_C_Programming_Guide:L3626-L3637].

Since kernel launches are asynchronous, checking for asynchronous errors requires synchronization between the kernel launch and the call to `cudaPeekAtLastError()` or `cudaGetLastError()` [CUDA_C_Programming_Guide:L3626-L3637].

## Special Cases

The error code `cudaErrorNotReady`, which may be returned by `cudaStreamQuery()` and `cudaEventQuery()`, is not considered an error and is therefore not reported by `cudaPeekAtLastError()` or `cudaGetLastError()` [CUDA_C_Programming_Guide:L3626-L3637].
