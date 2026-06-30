# atomicAdd()

Performs an atomic addition operation on 16-bit, 32-bit, 64-bit, and vector types (float2, float4, __half, __nv_bfloat16) in global or shared memory. Returns the old value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7786-L7823

Citation: [CUDA_C_Programming_Guide:L7786-L7823]

````text
## 10.14.1. Arithmetic Functions

## 10.14.1.1 atomicAdd()

```c
int atomicAdd(int* address, int val);
unsigned int atomicAdd(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicAdd(unsigned long long int* address,
                    unsigned long long int val);
float atomicAdd(float* address, float val);
double atomicAdd(double* address, double val);
__half2 atomicAdd(__half2 *address, __half2 val);
__half atomicAdd(__half *address, __half val);
__nv_bfloat162 atomicAdd(__nv_bfloat162 *address, __nv_bfloat162 val);
__nv_bfloat16 atomicAdd(__nv_bfloat16 *address, __nv_bfloat16 val);
float2 atomicAdd(float2* address, float2 val);
float4 atomicAdd(float4* address, float4 val);
```

reads the 16-bit, 32-bit or 64-bit old located at the address address in global or shared memory, computes (old + val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 32-bit floating-point version of atomicAdd() is only supported by devices of compute capability 2.x and higher.

The 64-bit floating-point version of atomicAdd() is only supported by devices of compute capability 6.x and higher.

The 32-bit \_\_half2 floating-point version of atomicAdd() is only supported by devices of compute capability 6.x and higher. The atomicity of the \_\_half2 or \_\_nv\_bfloat162 add operation is guaranteed separately for each of the two \_\_half or \_\_nv\_bfloat16 elements; the entire \_\_half2 or \_\_nv\_bfloat162 is not guaranteed to be atomic as a single 32-bit access.

The float2 and float4 floating-point vector versions of atomicAdd() are only supported by devices of compute capability 9.x and higher. The atomicity of the float2 or float4 add operation is guaranteed separately for each of the two or four float elements; the entire float2 or float4 is not guaranteed to be atomic as a single 64-bit or 128-bit access.

The 16-bit \_\_half floating-point version of atomicAdd() is only supported by devices of compute capability 7.x and higher.

The 16-bit \_\_nv\_bfloat16 floating-point version of atomicAdd() is only supported by devices of compute capability 8.x and higher.

The float2 and float4 floating-point vector versions of atomicAdd() are only supported by devices of compute capability 9.x and higher.

The float2 and float4 floating-point vector versions of atomicAdd() are only supported for global memory addresses.
````
