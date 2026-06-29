# Load Functions Using Cache Hints

These load functions are only supported by devices of compute capability 5.0 and higher.

## Function Signatures

The following functions return the data of type `T` located at `address`:

```c
T __ldcg(const T* address);
T __ldca(const T* address);
T __ldcs(const T* address);
T __ldlu(const T* address);
T __ldcv(const T* address);
```

## Supported Types

The type `T` can be:

*   **Scalar types:** `char`, `signed char`, `short`, `int`, `long`, `long long`, `unsigned char`, `unsigned short`, `unsigned int`, `unsigned long`, `unsigned long long`, `float`, `double`.
*   **Vector types:** `char2`, `char4`, `short2`, `short4`, `int2`, `int4`, `longlong2`, `uchar2`, `uchar4`, `ushort2`, `ushort4`, `uint2`, `uint4`, `ulonglong2`, `float2`, `float4`, `double2`.
*   **Floating-point types (with `cuda_fp16.h`):** `__half`, `__half2`.
*   **Bfloat16 types (with `cuda_bf16.h`):** `__nv_bfloat16`, `__nv_bfloat162`.

## Operation

The operation uses the corresponding cache operator as defined in the PTX ISA [CUDA_C_Programming_Guide:L7601-L7614].

## Aliases

*   `__ldcg`
*   `__ldca`
*   `__ldcs`
*   `__ldlu`
*   `__ldcv`

## See Also

*   PTX ISA documentation for cache operator details.
