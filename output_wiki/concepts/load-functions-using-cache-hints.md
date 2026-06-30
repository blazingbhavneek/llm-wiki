# Load Functions Using Cache Hints

Reference for cache-hinted load intrinsics (__ldcg, __ldca, __ldcs, __ldlu, __ldcv) that control cache behavior for global memory reads, supporting various data types and requiring compute capability 5.0 or higher.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7601-L7614

Citation: [CUDA_C_Programming_Guide:L7601-L7614]

````text
## 10.11. Load Functions Using Cache Hints

These load functions are only supported by devices of compute capability 5.0 and higher.

```javascript
T __ldcg(const T* address);
T __ldca(const T* address);
T __ldcs(const T* address);
T __ldlu(const T* address);
T __ldcv(const T* address);
```

returns the data of type T located at address address, where T is char, signed char, short, int, long, long longunsigned char, unsigned short, unsigned int, unsigned long, unsigned long long, char2, char4, short2, short4, int2, int4, longlong2uchar2, uchar4, ushort2, ushort4, uint2, uint4, ulonglong2float, float2, float4, double, or double2. With the cuda\_fp16.h header included, T can be \_\_half or \_\_half2. Similarly, with the cuda\_bf16.h header included, T can also be \_\_nv\_bfloat16 or \_\_nv\_bfloat162. The operation is using the corresponding cache operator (see PTX ISA)
````
