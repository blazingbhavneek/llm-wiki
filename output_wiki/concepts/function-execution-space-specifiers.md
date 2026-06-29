# Function Execution Space Specifiers

Function execution space specifiers denote whether a function executes on the host or on the device and whether it is callable from the host or from the device [CUDA_C_Programming_Guide:L6543-L6543].

## __global__

The __global__ execution space specifier declares a function as being a kernel [CUDA_C_Programming_Guide:L6544-L6561]. Such a function is:

*   Executed on the device
*   Callable from the host
*   Callable from the device for devices of compute capability 5.0 or higher (see CUDA Dynamic Parallelism for more details) [CUDA_C_Programming_Guide:L6544-L6561]

A __global__ function must have void return type, and cannot be a member of a class [CUDA_C_Programming_Guide:L6544-L6561]. Any call to a __global__ function must specify its execution configuration as described in Execution Configuration [CUDA_C_Programming_Guide:L6544-L6561]. A call to a __global__ function is asynchronous, meaning it returns before the device has completed its execution [CUDA_C_Programming_Guide:L6544-L6561].

## __device__

The __device__ execution space specifier declares a function that is:

*   Executed on the device
*   Callable from the device only [CUDA_C_Programming_Guide:L6562-L6571]

The __global__ and __device__ execution space specifiers cannot be used together [CUDA_C_Programming_Guide:L6562-L6571].

## __host__

The __host__ execution space specifier declares a function that is:

*   Executed on the host
*   Callable from the host only [CUDA_C_Programming_Guide:L6572-L6601]

It is equivalent to declare a function with only the __host__ execution space specifier or to declare it without any of the __host__, __device__, or __global__ execution space specifier; in either case the function is compiled for the host only [CUDA_C_Programming_Guide:L6572-L6601]. The __global__ and __host__ execution space specifiers cannot be used together [CUDA_C_Programming_Guide:L6572-L6601].

The __device__ and __host__ execution space specifiers can be used together however, in which case the function is compiled for both the host and the device [CUDA_C_Programming_Guide:L6572-L6601]. The __CUDA_ARCH__ macro introduced in Application Compatibility can be used to differentiate code paths between host and device [CUDA_C_Programming_Guide:L6572-L6601]:

```c
__host__ __device__ func()
{
#if __CUDA_ARCH__ >= 800
    // Device code path for compute capability 8.x
#elif __CUDA_ARCH__ >= 700
    // Device code path for compute capability 7.x
#elif __CUDA_ARCH__ >= 600
    // Device code path for compute capability 6.x
#elif __CUDA_ARCH__ >= 500
    // Device code path for compute capability 5.x
#elif !defined(__CUDA_ARCH__)
    // Host code path
#endif
}
```
