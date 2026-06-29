# Function Pointers

In CUDA C++, function pointers are subject to strict restrictions regarding their scope and the ability to take their addresses across host and device code boundaries.

## Restrictions on __global__ Functions

The address of a `__global__` function (kernel) cannot be taken in a manner that allows it to be used across host and device boundaries:

*   **Host to Device**: The address of a `__global__` function taken in host code cannot be used in device code (for example, to launch the kernel from within a device function) [CUDA_C_Programming_Guide:L17235-L17238].
*   **Device to Host**: Similarly, the address of a `__global__` function taken in device code cannot be used in host code [CUDA_C_Programming_Guide:L17235-L17238].

## Restrictions on __device__ Functions

It is not allowed to take the address of a `__device__` function in host code [CUDA_C_Programming_Guide:L17235-L17238].

## Summary

These restrictions ensure that function pointers are used only within their appropriate execution spaces, preventing invalid cross-boundary references between host and device code. When working with function pointers in CUDA, ensure that the function's address is only taken and used within the same execution space (host or device) where it is defined, and be aware that `__global__` function addresses cannot be passed between these spaces. For more detailed information on function pointers and their usage in CUDA, refer to the CUDA C++ Programming Guide.
