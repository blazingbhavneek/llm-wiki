# CUDA Dynamic Parallelism Errors

Error handling, API error codes, and launch failure reporting in the device runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14014-L14027

Citation: [CUDA_C_Programming_Guide:L14014-L14027]

````text
## 13.3.1.7 API Errors and Launch Failures

As usual for the CUDA runtime, any function may return an error code. The last error code returned is recorded and may be retrieved via the cudaGetLastError() call. Errors are recorded per-thread, so that each thread can identify the most recent error that it has generated. The error code is of type cudaError\_t.

Similar to a host-side launch, device-side launches may fail for many reasons (invalid arguments, etc). The user must call cudaGetLastError() to determine if a launch generated an error, however lack of an error after launch does not imply the child kernel completed successfully.

For device-side exceptions, e.g., access to an invalid address, an error in a child grid will be returned to the host.

## 13.3.1.7.1 Launch Setup APIs

Kernel launch is a system-level mechanism exposed through the device runtime library, and as such is available directly from PTX via the underlying cudaGetParameterBuffer() and cudaLaunchDevice() APIs. It is permitted for a CUDA application to call these APIs itself, with the same requirements as for PTX. In both cases, the user is then responsible for correctly populating all necessary data structures in the correct format according to specification. Backwards compatibility is guaranteed in these data structures.

As with host-side launch, the device-side operator <<<>>> maps to underlying kernel launch APIs. This is so that users targeting PTX will be able to enact a launch, and so that the compiler front-end can translate <<<>>> into these calls.
````
