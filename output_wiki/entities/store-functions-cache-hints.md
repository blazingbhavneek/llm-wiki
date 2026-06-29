# Store Functions Using Cache Hints

These store functions are only supported by devices of compute capability 5.0 and higher [CUDA_C_Programming_Guide:L7615-L7627].

## Function Signatures

The following functions store a value argument of type `T` to the location at `address` [CUDA_C_Programming_Guide:L7615-L7627]:

```c
void __stwb(T* address, T value);
void __stcg(T* address, T value);
void __stcs(T* address, T value);
void __stwt(T* address, T value);
```

## Supported Types

The type `T` can be any of the following [CUDA_C_Programming_Guide:L7615-L7627]:

- `char`, `signed char`
- `short`, `int`, `long`, `long long`
- `unsigned char`, `unsigned short`, `unsigned int`, `unsigned long`, `unsigned long long`
- `char2`, `char4`
- `short2`, `short4`
- `int2`, `int4`
- `longlong2`
- `uchar2`, `uchar4`
- `ushort2`, `ushort4`
- `uint2`, `uint4`
- `ulonglong2`
- `float`, `float2`, `float4`
- `double`, `double2`

With the `cuda_fp16.h` header included, `T` can also be `__half` or `__half2` [CUDA_C_Programming_Guide:L7615-L7627].

Similarly, with the `cuda_bf16.h` header included, `T` can also be `__nv_bfloat16` or `__nv_bfloat162` [CUDA_C_Programming_Guide:L7615-L7627].

## Operation

The operation uses the corresponding cache operator (see PTX ISA) [CUDA_C_Programming_Guide:L7615-L7627].

## Aliases

- `__stwb`
- `__stcg`
- `__stcs`
- `__stwt`
