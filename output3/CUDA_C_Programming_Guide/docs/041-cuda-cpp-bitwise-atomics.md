## 10.14.2. Bitwise Functions

10.14.2.1 atomicAnd()

```c
int atomicAnd(int* address, int val);
unsigned int atomicAnd(unsigned int* address,
                      unsigned int val);
unsigned long long int atomicAnd(unsigned long long int* address,
                       unsigned long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes (old & val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicAnd() is only supported by devices of compute capability 5.0 and higher.

## 10.14.2.2 atomicOr()

```c
int atomicOr(int* address, int val);
unsigned int atomicOr(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicOr(unsigned long long int* address,
                    unsigned long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes (old | val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicOr() is only supported by devices of compute capability 5.0 and higher.

## 10.14.2.3 atomicXor()

```c
int atomicXor(int* address, int val);
unsigned int atomicXor(unsigned int* address,
                      unsigned int val);
unsigned long long int atomicXor(unsigned long long int* address,
                       unsigned long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes (old ^ val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicXor() is only supported by devices of compute capability 5.0 and higher.

## 10.14.2.4 \_\_nv\_atomic\_fetch\_or() and \_\_nv\_atomic\_or()

```c
__device__ T __nv_atomic_fetch_or (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_or (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, or with val, and stores the result back to where ptr points to. \_\_nv\_atomic\_fetch\_or returns the old value where ptr points to. \_\_nv\_atomic\_or does not have return value.

T can only be an integral type that is size of 4 or 8 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

## 10.14.2.5 \_\_nv\_atomic\_fetch\_xor() and \_\_nv\_atomic\_xor()

```c
__device__ T __nv_atomic_fetch_xor (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_xor (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, xor with val, and stores the result back to where ptr points to. \_\_nv\_atomic\_fetch\_xor returns the old value where ptr points to. \_\_nv\_atomic\_xor does not have return value.

T can only be an integral type that is size of 4 or 8 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.

## 10.14.2.6 \_\_nv\_atomic\_fetch\_and() and \_\_nv\_atomic\_and()

```c
__device__ T __nv_atomic_fetch_and (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_and (T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

These two atomic functions are introduced in CUDA 12.8. It reads the value where ptr points to, and with val, and stores the result back to where ptr points to. \_\_nv\_atomic\_fetch\_and returns the old value where ptr points to. \_\_nv\_atomic\_and does not have return value.

T can only be an integral type that is size of 4 or 8 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.
