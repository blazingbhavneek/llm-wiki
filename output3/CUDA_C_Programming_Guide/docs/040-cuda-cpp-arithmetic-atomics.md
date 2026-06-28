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

## 10.14.1.2 atomicSub()

```c
int atomicSub(int* address, int val);
unsigned int atomicSub(unsigned int* address,
                                unsigned int val);
```

reads the 32-bit word old located at the address address in global or shared memory, computes (old - val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

## 10.14.1.3 atomicExch()

```txt
int atomicExch(int* address, int val);
unsigned int atomicExch(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicExch(unsigned long long int* address,
                    unsigned long long int val);
float atomicExch(float* address, float val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory and stores val back to memory at the same address. These two operations are performed in one atomic transaction. The function returns old.

```txt
template<typename T> T atomicExch(T* address, T val);
```

reads the 128-bit word old located at the address address in global or shared memory and stores val back to memory at the same address. These two operations are performed in one atomic transaction. The function returns old. The type T must meet the following requirements:

```cpp
sizeof(T) == 16
alignof(T) >= 16
std::is_trivially_copyable<T>::value == true
// for C++03 and older
std::is_default_constructible<T>::value == true
```

So, T must be 128-bit and properly aligned, be trivially copyable, and on C++03 or older, it must also be default constructible.

The 128-bit atomicExch() is only supported by devices of compute capability 9.x and higher.

## 10.14.1.4 atomicMin()

```c
int atomicMin(int* address, int val);
unsigned int atomicMin(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicMin(unsigned long long int* address,
                    unsigned long long int val);
long long int atomicMin(long long int* address,
                    long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes the minimum of old and val, and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicMin() is only supported by devices of compute capability 5.0 and higher.

## 10.14.1.5 atomicMax()

```txt
int atomicMax(int* address, int val);
unsigned int atomicMax(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicMax(unsigned long long int* address,
                    unsigned long long int val);
long long int atomicMax(long long int* address,
                    long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes the maximum of old and val, and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicMax() is only supported by devices of compute capability 5.0 and higher.

## 10.14.1.6 atomicInc()

```txt
unsigned int atomicInc(unsigned int* address,
                                unsigned int val);
```

reads the 32-bit word old located at the address address in global or shared memory, computes ((old >= val) ? 0 : (old+1)), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

## 10.14.1.7 atomicDec()

```txt
unsigned int atomicDec(unsigned int* address,
                                unsigned int val);
```

reads the 32-bit word old located at the address address in global or shared memory, computes (((old == 0) || (old > val)) ? val : (old-1) ), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

## 10.14.1.8 atomicCAS()

```c
int atomicCAS(int* address, int compare, int val);
unsigned int atomicCAS(unsigned int* address,
                    unsigned int compare,
                    unsigned int val);
unsigned long long int atomicCAS(unsigned long long int* address,
                            unsigned long long int compare,
                            unsigned long long int val);
unsigned short int atomicCAS(unsigned short int *address,
```

(continues on next page)

(continued from previous page)

```txt
unsigned short int compare,
unsigned short int val);
```

reads the 16-bit, 32-bit or 64-bit word old located at the address address in global or shared memory, computes (old == compare ? val : old), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old (Compare And Swap).

template<typename T> T atomicCAS(T\* address, T compare, T val);

reads the 128-bit word old located at the address address in global or shared memory, computes (old == compare ? val : old), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old (Compare And Swap). The type T must meet the following requirements:

```cpp
sizeof(T) == 16
alignof(T) >= 16
std::is_trivially_copyable<T>::value == true
// for C++03 and older
std::is_default_constructible<T>::value == true
```

So, T must be 128-bit and properly aligned, be trivially copyable, and on C++03 or older, it must also be default constructible.

The 128-bit atomicCAS() is only supported by devices of compute capability 9.x and higher.

## 10.14.1.9 \_\_nv\_atomic\_exchange()

```c
__device__ void __nv_atomic_exchange(T* ptr, T* val, T *ret, int order, int scope = __
->NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It reads the value where ptr points to and stores the value to where ret points to. And it reads the value where val points to and stores the value to where ptr points to.

This is a generic atomic exchange, which means that T can be any data type that is size of 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_90 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

10.14.1.10 \_\_nv\_atomic\_exchange\_n()

```txt
__device__ T __nv_atomic_exchange_n(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It reads the value where ptr points to and use this value as the return value. And it stores val to where ptr points to.

This is a non-generic atomic exchange, which means that T can only be an integral type that is size of 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_90 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

10.14.1.11 \_\_nv\_atomic\_compare\_exchange()

\_device\_\_ bool \_\_nv\_atomic\_compare\_exchange (T\* ptr, T\* expected, T\* desired, bool ,<sub>→</sub>weak, int success\_order, int failure\_order, int scope = \_\_NV\_THREAD\_SCOPE\_SYSTEM);

This atomic function is introduced in CUDA 12.8. It reads the value where ptr points to and compare it with the value where expected points to. If they are equal, the return value is true and the value where desired points to is stored to where ptr points to. Otherwise, it returns false and the value where ptr points to is stored to where expected points to. The parameter weak is ignored and it picks the stronger memory order between success\_order and failure\_order to execute the compareand-exchange operation.

This is a generic atomic compare-and-exchange, which means that T can be any data type that is size of 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_90 and higher.

2-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

10.14.1.12 \_\_nv\_atomic\_compare\_exchange\_n()

```c
__device__ bool __nv_atomic_compare_exchange_n (T* ptr, T* expected, T desired, bool
weak, int success_order, int failure_order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It reads the value where ptr points to and compare it with the value where expected points to. If they are equal, the return value is true and desired is stored to where ptr points to. Otherwise, it returns false and the value where ptr points to is stored to where expected points to. The parameter weak is ignored and it picks the stronger memory order between success\_order and failure\_order to execute the compare-and-exchange operation.

This is a non-generic atomic compare-and-exchange, which means that T can only be an integral type that is size of 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_90 and higher.

2-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

## 10.14.1.13 \_\_nv\_atomic\_fetch\_add() and \_\_nv\_atomic\_add()

```c
__device__ T __nv_atomic_fetch_add (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_add (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, adds with val, and stores the result back to where ptr points to. \_\_nv\_atomic\_fetch\_add returns the old value where ptr points to. \_\_nv\_atomic\_add does not have return value.

T can only be unsigned int, int, unsigned long long, float or double.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

## 10.14.1.14 \_\_nv\_atomic\_fetch\_sub() and \_\_nv\_atomic\_sub()

```c
__device__ T __nv_atomic_fetch_sub (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_sub (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, subtracts with val, and stores the result back to where ptr points to. \_\_nv\_atomic\_fetch\_sub returns the old value where ptr points to. \_\_nv\_atomic\_sub does not have return value.

T can only be unsigned int, int, unsigned long long, float or double.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

10.14.1.15 \_\_nv\_atomic\_fetch\_min() and \_\_nv\_atomic\_min()

```c
__device__ T __nv_atomic_fetch_min (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_min (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, compares with val, and stores the smaller value back to where ptr points to. \_\_nv\_atomic\_fetch\_min returns the old value where ptr points to. \_\_nv\_atomic\_min does not have return value.

T can only be unsigned int, int, unsigned long long or long long.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

10.14.1.16 \_\_nv\_atomic\_fetch\_max() and \_\_nv\_atomic\_max()

```c
__device__ T __nv_atomic_fetch_max (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_max (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, compares with val, and stores the bigger value back to where ptr points to. \_\_nv\_atomic\_fetch\_max returns the old value where ptr points to. \_\_nv\_atomic\_max does not have return value.

T can only be unsigned int, int, unsigned long long or long long.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.
