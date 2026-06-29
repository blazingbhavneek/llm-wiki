# atomicAdd()

The `atomicAdd()` function performs an atomic addition operation on a value located at a specified memory address. It reads the old value, computes `(old + val)`, and stores the result back to the same address in a single atomic transaction. The function returns the old value that was read from memory.

## Supported Types and Signatures

The function supports integer, floating-point, and vector types. The following signatures are available:

```c
int atomicAdd(int* address, int val);
unsigned int atomicAdd(unsigned int* address, unsigned int val);
unsigned long long int atomicAdd(unsigned long long int* address, unsigned long long int val);
float atomicAdd(float* address, float val);
double atomicAdd(double* address, double val);
__half2 atomicAdd(__half2 *address, __half2 val);
__half atomicAdd(__half *address, __half val);
__nv_bfloat162 atomicAdd(__nv_bfloat162 *address, __nv_bfloat162 val);
__nv_bfloat16 atomicAdd(__nv_bfloat16 *address, __nv_bfloat16 val);
float2 atomicAdd(float2* address, float2 val);
float4 atomicAdd(float4* address, float4 val);
```

These operations can be performed on values located in global or shared memory [CUDA_C_Programming_Guide:L7789-L7823].

## Compute Capability Requirements

Support for specific data types depends on the device's compute capability:

*   **32-bit float (`float`)**: Supported by devices of compute capability 2.x and higher [CUDA_C_Programming_Guide:L7789-L7823].
*   **64-bit float (`double`)**: Supported by devices of compute capability 6.x and higher [CUDA_C_Programming_Guide:L7789-L7823].
*   **32-bit `__half2`**: Supported by devices of compute capability 6.x and higher [CUDA_C_Programming_Guide:L7789-L7823].
*   **16-bit `__half`**: Supported by devices of compute capability 7.x and higher [CUDA_C_Programming_Guide:L7789-L7823].
*   **16-bit `__nv_bfloat16`**: Supported by devices of compute capability 8.x and higher [CUDA_C_Programming_Guide:L7789-L7823].
*   **`float2` and `float4`**: Supported by devices of compute capability 9.x and higher [CUDA_C_Programming_Guide:L7789-L7823].

## Atomicity Guarantees

The atomicity guarantees vary by data type:

*   **`__half2` and `__nv_bfloat162`**: The atomicity of the add operation is guaranteed separately for each of the two elements. The entire 32-bit access is not guaranteed to be atomic as a single unit [CUDA_C_Programming_Guide:L7789-L7823].
*   **`float2` and `float4`**: The atomicity of the add operation is guaranteed separately for each of the two or four float elements. The entire 64-bit or 128-bit access is not guaranteed to be atomic as a single unit [CUDA_C_Programming_Guide:L7789-L7823].

## Memory Constraints

The `float2` and `float4` floating-point vector versions of `atomicAdd()` are only supported for global memory addresses [CUDA_C_Programming_Guide:L7789-L7823].
