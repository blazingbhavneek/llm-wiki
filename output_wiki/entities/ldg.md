# Read-Only Data Cache Load Function (__ldg)

Documentation for the __ldg() intrinsic, which loads data from global memory into the read-only data cache, supporting various primitive and vector types, and requiring compute capability 5.0 or higher.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7591-L7600

Citation: [CUDA_C_Programming_Guide:L7591-L7600]

````text
## 10.10. Read-Only Data Cache Load Function

The read-only data cache load function is only supported by devices of compute capability 5.0 and higher.

```javascript
T __ldg(const T* address);
```

returns the data of type T located at address address, where T is char, signed char, short, int, long, long longunsigned char, unsigned short, unsigned int, unsigned long, unsigned long long, char2, char4, short2, short4, int2, int4, longlong2uchar2, uchar4, ushort2, ushort4, uint2, uint4, ulonglong2float, float2, float4, double, or double2. With the cuda\_fp16.h header included, T can be \_\_half or \_\_half2. Similarly, with the cuda\_bf16.h header included, T can also be \_\_nv\_bfloat16 or \_\_nv\_bfloat162. The operation is cached in the read-only data cache (see Global Memory).
````
