
The read-only data cache load function is only supported by devices of compute capability 5.0 and higher.

```javascript
T __ldg(const T* address);
```

returns the data of type T located at address address, where T is char, signed char, short, int, long, long longunsigned char, unsigned short, unsigned int, unsigned long, unsigned long long, char2, char4, short2, short4, int2, int4, longlong2uchar2, uchar4, ushort2, ushort4, uint2, uint4, ulonglong2float, float2, float4, double, or double2. With the cuda\_fp16.h header included, T can be \_\_half or \_\_half2. Similarly, with the cuda\_bf16.h header included, T can also be \_\_nv\_bfloat16 or \_\_nv\_bfloat162. The operation is cached in the read-only data cache (see Global Memory).

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

## 10.12. Store Functions Using Cache Hints
