# Store Functions Using Cache Hints

Reference for cache-hinted store intrinsics (__stwb, __stcg, __stcs, __stwt) that control cache behavior for global memory writes, supporting various data types and requiring compute capability 5.0 or higher.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7615-L7627

Citation: [CUDA_C_Programming_Guide:L7615-L7627]

````text
## 10.12. Store Functions Using Cache Hints

These store functions are only supported by devices of compute capability 5.0 and higher.

```c
void __stwb(T* address, T value);
void __stcg(T* address, T value);
void __stcs(T* address, T value);
void __stwt(T* address, T value);
```

stores the value argument of type T to the location at address address, where T is char, signed char, short, int, long, long longunsigned char, unsigned short, unsigned int, unsigned long, unsigned long long, char2, char4, short2, short4, int2, int4, longlong2uchar2, uchar4, ushort2, ushort4, uint2, uint4, ulonglong2float, float2, float4, double, or double2. With the cuda\_fp16.h header included, T can be \_\_half or \_\_half2. Similarly, with the cuda\_bf16.h header included, T can also be \_\_nv\_bfloat16 or \_\_nv\_bfloat162. The operation is using the corresponding cache operator (see PTX ISA )
````
