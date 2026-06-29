# __ldg

The `__ldg` function is the Read-Only Data Cache Load Function, which reads data from global memory into the read-only data cache [CUDA_C_Programming_Guide:L7591-L7600]. This operation is cached in the read-only data cache [CUDA_C_Programming_Guide:L7591-L7600].

## Syntax

```c
T __ldg(const T* address);
```

The function returns the data of type `T` located at the specified `address` [CUDA_C_Programming_Guide:L7591-L7600].

## Supported Types

The template type `T` supports the following data types:

*   **Scalars**: `char`, `signed char`, `short`, `int`, `long`, `long long`, `unsigned char`, `unsigned short`, `unsigned int`, `unsigned long`, `unsigned long long`, `float`, `double` [CUDA_C_Programming_Guide:L7591-L7600].
*   **Vectors**: `char2`, `char4`, `short2`, `short4`, `int2`, `int4`, `longlong2`, `uchar2`, `uchar4`, `ushort2`, `ushort4`, `uint2`, `uint4`, `ulonglong2`, `float2`, `float4`, `double2` [CUDA_C_Programming_Guide:L7591-L7600].
*   **Half-Precision**: With the `cuda_fp16.h` header included, `T` can be `__half` or `__half2` [CUDA_C_Programming_Guide:L7591-L7600].
*   **BFloat16**: With the `cuda_bf16.h` header included, `T` can be `__nv_bfloat16` or `__nv_bfloat162` [CUDA_C_Programming_Guide:L7591-L7600].

## Requirements

The read-only data cache load function is only supported by devices of compute capability 5.0 and higher [CUDA_C_Programming_Guide:L7591-L7600].

## See Also

*   Global Memory
