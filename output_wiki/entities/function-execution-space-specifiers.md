# Function Execution Space Specifiers

Defines __global__, __device__, __host__, __noinline__, __forceinline__, and __inline_hint__ specifiers, their usage rules, cross-execution space call restrictions, and undefined behavior conditions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6541-L6626

Citation: [CUDA_C_Programming_Guide:L6541-L6626]

````text

## 10.1. Function Execution Space Specifiers

Function execution space specifiers denote whether a function executes on the host or on the device and whether it is callable from the host or from the device.

## 10.1.1. \_\_global\_\_

The \_\_global\_\_ execution space specifier declares a function as being a kernel. Such a function is:

Executed on the device,

▶ Callable from the host,

Callable from the device for devices of compute capability 5.0 or higher (see CUDA Dynamic Parallelism for more details).

A \_\_global\_\_ function must have void return type, and cannot be a member of a class.

Any call to a \_\_global\_\_ function must specify its execution configuration as described in Execution Configuration.

A call to a \_\_global\_\_ function is asynchronous, meaning it returns before the device has completed its execution.

## 10.1.2. \_\_device\_\_

The \_\_device\_\_ execution space specifier declares a function that is:

Executed on the device,

▶ Callable from the device only.

The \_\_global\_\_ and \_\_device\_\_ execution space specifiers cannot be used together.

## 10.1.3. \_\_host\_\_

The \_\_host\_\_ execution space specifier declares a function that is:

▶ Executed on the host,

Callable from the host only.

It is equivalent to declare a function with only the \_\_host\_\_ execution space specifier or to declare it without any of the \_\_host\_\_, \_\_device\_\_, or \_\_global\_\_ execution space specifier; in either case the function is compiled for the host only.

The \_\_global\_\_ and \_\_host\_\_ execution space specifiers cannot be used together.

The \_\_device\_\_ and \_\_host\_\_ execution space specifiers can be used together however, in which case the function is compiled for both the host and the device. The \_\_CUDA\_ARCH\_\_ macro introduced in Application Compatibility can be used to diferentiate code paths between host and device:

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

## 10.1.4. Undefined behavior

A ‘cross-execution space’ call has undefined behavior when:

▶ \_\_CUDA\_ARCH\_\_ is defined, a call from within a \_\_global\_\_, \_\_device\_\_ or \_\_host\_\_ \_\_device\_\_ function to a \_\_host\_\_ function.

▶ \_\_CUDA\_ARCH\_\_ is undefined, a call from within a \_\_host\_\_ function to a \_\_device\_\_ function.<sup>4</sup>

## 10.1.5. \_\_noinline\_\_ and \_\_forceinline\_

The compiler inlines any \_\_device\_\_ function when deemed appropriate.

The \_\_noinline\_\_ function qualifier can be used as a hint for the compiler not to inline the function if possible.

The \_\_forceinline\_\_ function qualifier can be used to force the compiler to inline the function.

The \_\_noinline\_\_ and \_\_forceinline\_\_ function qualifiers cannot be used together, and neither function qualifier can be applied to an inline function.

## 10.1.6. \_\_inline\_hint\_\_

The \_\_inline\_hint\_\_ qualifier enables more aggressive inlining in the compiler. Unlike \_\_forceinline\_\_, it does not imply that the function is inline. It can be used to improve inlining across modules when using LTO.

Neither the \_\_noinline\_\_ nor the \_\_forceinline\_\_ function qualifier can be used with the \_\_inline\_hint\_\_ function qualifier.
````
