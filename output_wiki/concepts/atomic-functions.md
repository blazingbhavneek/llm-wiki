# Atomic Functions

CUDA provides a comprehensive set of atomic functions for performing read-modify-write operations on memory locations in a thread-safe manner. These functions are essential for parallel programming on GPUs, allowing multiple threads to update shared data without race conditions.

## Generic and Non-Generic Atomic Functions (CUDA 12.8+)

Introduced in CUDA 12.8, the `__nv_atomic_*` family of functions provides generic and non-generic variants of atomic operations. These functions support memory ordering and thread scope parameters, enabling fine-grained control over memory visibility and synchronization across different thread scopes (thread, block, cluster, system) [CUDA_C_Programming_Guide:L7955-L8630].

### General Requirements

*   **Memory Order and Scope:** The atomic operations with memory order and thread scope are supported on architectures sm_60 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **Cluster Scope:** The thread scope of cluster is supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **Literal Arguments:** The arguments `order` and `scope` must be integer literals; they cannot be variables [CUDA_C_Programming_Guide:L7955-L8630].

### Exchange Operations

#### Generic Exchange: `__nv_atomic_exchange`

```c
__device__ void __nv_atomic_exchange(T* ptr, T* val, T *ret, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This function reads the value where `ptr` points to and stores it to `ret`. It then reads the value where `val` points to and stores it to `ptr` [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be any data type that is 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].

#### Non-Generic Exchange: `__nv_atomic_exchange_n`

```c
__device__ T __nv_atomic_exchange_n(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This function reads the value where `ptr` points to and returns it. It then stores `val` to where `ptr` points to [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can only be an integral type that is 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].

### Compare-Exchange Operations

#### Generic Compare-Exchange: `__nv_atomic_compare_exchange`

```c
__device__ bool __nv_atomic_compare_exchange(T* ptr, T* expected, T* desired, bool weak, int success_order, int failure_order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This function compares the value at `ptr` with the value at `expected`. If they are equal, it returns `true` and stores the value at `desired` to `ptr`. Otherwise, it returns `false` and stores the value at `ptr` to `expected` [CUDA_C_Programming_Guide:L7955-L8630].

*   **Weak Parameter:** The `weak` parameter is ignored; the stronger memory order between `success_order` and `failure_order` is used [CUDA_C_Programming_Guide:L7955-L8630].
*   **Type Support:** `T` can be any data type that is 2, 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **2-byte Support:** 2-byte data types are supported on architectures sm_70 and higher [CUDA_C_Programming_Guide:L7955-L8630].

#### Non-Generic Compare-Exchange: `__nv_atomic_compare_exchange_n`

```c
__device__ bool __nv_atomic_compare_exchange_n(T* ptr, T* expected, T desired, bool weak, int success_order, int failure_order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This function compares the value at `ptr` with the value at `expected`. If they are equal, it returns `true` and stores `desired` to `ptr`. Otherwise, it returns `false` and stores the value at `ptr` to `expected` [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can only be an integral type that is 2, 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **2-byte Support:** 2-byte data types are supported on architectures sm_70 and higher [CUDA_C_Programming_Guide:L7955-L8630].

### Arithmetic Operations

#### Add

```c
__device__ T __nv_atomic_fetch_add(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_add(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_add` adds `val` to the value at `ptr` and returns the old value. `__nv_atomic_add` performs the same operation but does not return a value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be `unsigned int`, `int`, `unsigned long long`, `float`, or `double` [CUDA_C_Programming_Guide:L7955-L8630].

#### Subtract

```c
__device__ T __nv_atomic_fetch_sub(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_sub(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_sub` subtracts `val` from the value at `ptr` and returns the old value. `__nv_atomic_sub` performs the same operation but does not return a value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be `unsigned int`, `int`, `unsigned long long`, `float`, or `double` [CUDA_C_Programming_Guide:L7955-L8630].

#### Min/Max

```c
__device__ T __nv_atomic_fetch_min(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_min(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);

__device__ T __nv_atomic_fetch_max(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_max(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_min` stores the smaller of the value at `ptr` and `val`, returning the old value. `__nv_atomic_min` performs the same operation without returning a value. Similarly, `__nv_atomic_fetch_max` and `__nv_atomic_max` store the larger value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be `unsigned int`, `int`, `unsigned long long`, or `long long` [CUDA_C_Programming_Guide:L7955-L8630].

### Bitwise Operations

#### OR

```c
__device__ T __nv_atomic_fetch_or(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_or(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_or` performs a bitwise OR between the value at `ptr` and `val`, storing the result and returning the old value. `__nv_atomic_or` performs the same operation without returning a value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can only be an integral type that is 4 or 8 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].

#### XOR

```c
__device__ T __nv_atomic_fetch_xor(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_xor(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_xor` performs a bitwise XOR between the value at `ptr` and `val`, storing the result and returning the old value. `__nv_atomic_xor` performs the same operation without returning a value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can only be an integral type that is 4 or 8 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].

#### AND

```c
__device__ T __nv_atomic_fetch_and(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_and(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_fetch_and` performs a bitwise AND between the value at `ptr` and `val`, storing the result and returning the old value. `__nv_atomic_and` performs the same operation without returning a value [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can only be an integral type that is 4 or 8 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].

### Load and Store Operations

#### Atomic Load

```c
__device__ void __nv_atomic_load(T* ptr, T* ret, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ T __nv_atomic_load_n(T* ptr, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_load` reads the value at `ptr` and writes it to `ret`. `__nv_atomic_load_n` reads the value at `ptr` and returns it [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be any data type that is 1, 2, 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_70 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **Order Restrictions:** The `order` argument cannot be `__NV_ATOMIC_RELEASE` or `__NV_ATOMIC_ACQ_REL` [CUDA_C_Programming_Guide:L7955-L8630].

#### Atomic Store

```c
__device__ void __nv_atomic_store(T* ptr, T* val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
__device__ void __nv_atomic_store_n(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

`__nv_atomic_store` reads the value at `val` and stores it to `ptr`. `__nv_atomic_store_n` stores `val` directly to `ptr` [CUDA_C_Programming_Guide:L7955-L8630].

*   **Type Support:** `T` can be any data type that is 1, 2, 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7955-L8630].
*   **16-byte Support:** 16-byte data types are supported on architectures sm_70 and higher [CUDA_C_Programming_Guide:L7955-L8630].
*   **Order Restrictions:** The `order` argument cannot be `__NV_ATOMIC_CONSUME`, `__NV_ATOMIC_ACQUIRE`, or `__NV_ATOMIC_ACQ_REL` [CUDA_C_Programming_Guide:L7955-L8630].

### Thread Fence

```c
__device__ void __nv_atomic_thread_fence(int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This function establishes an ordering between memory accesses requested by the current thread based on the specified memory order. The `scope` parameter specifies the set of threads that may observe the ordering effect [CUDA_C_Programming_Guide:L7955-L8630].

*   **Cluster Scope:** Supported on architectures sm_90 and higher [CUDA_C_Programming_Guide:L7955-L8630].

## Legacy Bitwise Functions

The legacy bitwise atomic functions `atomicAnd`, `atomicOr`, and `atomicXor` perform atomic read-modify-write operations using bitwise AND, OR, and XOR, respectively. These functions return the old value located at the address [CUDA_C_Programming_Guide:L7955-L8630].

### atomicAnd

```c
int atomicAnd(int* address, int val);
unsigned int atomicAnd(unsigned int* address, unsigned int val);
unsigned long long int atomicAnd(unsigned long long int* address, unsigned long long int val);
```

Computes `(old & val)` and stores the result. The 64-bit version is supported by devices with compute capability 5.0 and higher [CUDA_C_Programming_Guide:L7955-L8630].

### atomicOr

```c
int atomicOr(int* address, int val);
unsigned int atomicOr(unsigned int* address, unsigned int val);
unsigned long long int atomicOr(unsigned long long int* address, unsigned long long int val);
```

Computes `(old | val)` and stores the result. The 64-bit version is supported by devices with compute capability 5.0 and higher [CUDA_C_Programming_Guide:L7955-L8630].

### atomicXor

```c
int atomicXor(int* address, int val);
unsigned int atomicXor(unsigned int* address, unsigned int val);
unsigned long long int atomicXor(unsigned long long int* address, unsigned long long int val);
```

Computes `(old ^ val)` and stores the result. The 64-bit version is supported by devices with compute capability 5.0 and higher [CUDA_C_Programming_Guide:L7955-L8630].

## Address Space Predicate Functions

These functions return 1 if the pointer contains the generic address of an object in the specified memory space, and 0 otherwise. Behavior is unspecified if the argument is a null pointer [CUDA_C_Programming_Guide:L7955-L8630].

*   `__isGlobal(const void *ptr)`: Returns 1 if `ptr` is in global memory space [CUDA_C_Programming_Guide:L7955-L8630].
*   `__isShared(const void *ptr)`: Returns 1 if `ptr` is in shared memory space [CUDA_C_Programming_Guide:L7955-L8630].
*   `__isConstant(const void *ptr)`: Returns 1 if `ptr` is in constant memory space [CUDA_C_Programming_Guide:L7955-L8630].
*   `__isGridConstant(const void *ptr)`: Returns 1 if `ptr` is a kernel parameter annotated with `__grid_constant__`. Supported for compute architectures >= 7.x [CUDA_C_Programming_Guide:L7955-L8630].
*   `__isLocal(const void *ptr)`: Returns 1 if `ptr` is in local memory space [CUDA_C_Programming_Guide:L7955-L8630].

## Address Space Conversion Functions

These functions convert CUDA C++ pointers from and to other representations, such as raw addresses for specific memory spaces. This is useful for interoperating with PTX instructions or optimizing data structure sizes [CUDA_C_Programming_Guide:L7955-L8630].

### Generic to Specific

*   `__cvta_generic_to_global(const void *ptr)`: Returns the result of executing the PTX `cvta.to.global` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_generic_to_shared(const void *ptr)`: Returns the result of executing the PTX `cvta.to.shared` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_generic_to_constant(const void *ptr)`: Returns the result of executing the PTX `cvta.to.const` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_generic_to_local(const void *ptr)`: Returns the result of executing the PTX `cvta.to.local` instruction [CUDA_C_Programming_Guide:L7955-L8630].

### Specific to Generic

*   `__cvta_global_to_generic(size_t rawbits)`: Returns the generic pointer obtained by executing the PTX `cvta.global` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_shared_to_generic(size_t rawbits)`: Returns the generic pointer obtained by executing the PTX `cvta.shared` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_constant_to_generic(size_t rawbits)`: Returns the generic pointer obtained by executing the PTX `cvta.const` instruction [CUDA_C_Programming_Guide:L7955-L8630].
*   `__cvta_local_to_generic(size_t rawbits)`: Returns the generic pointer obtained by executing the PTX `cvta.local` instruction [CUDA_C_Programming_Guide:L7955-L8630].

A roundtrip from a generic pointer to its 32-bit integer representation (for shared, local, and const spaces) and back is guaranteed to return an equivalent pointer [CUDA_C_Programming_Guide:L7955-L8630].

## Alloca Function

```c
__host__ __device__ void * alloca(size_t size);
```

Allocates `size` bytes of memory in the stack frame of the caller. The returned pointer is 16-byte aligned when invoked from device code. The memory is automatically freed when the caller returns [CUDA_C_Programming_Guide:L7955-L8630].

*   **Platform Note:** On Windows, `<malloc.h>` must be included before using `alloca()` [CUDA_C_Programming_Guide:L7955-L8630].
*   **Stack Overflow:** Using `alloca()` may cause stack overflow; users should adjust stack size accordingly [CUDA_C_Programming_Guide:L7955-L8630].
*   **Compute Capability:** Supported with compute capability 5.2 or higher [CUDA_C_Programming_Guide:L7955-L8630].

## Compiler Optimization Hint Functions

These functions provide additional information to the compiler optimizer [CUDA_C_Programming_Guide:L7955-L8630].

### __builtin_assume_aligned

```c
void * __builtin_assume_aligned (const void *exp, size_t align);
void * __builtin_assume_aligned (const void *exp, size_t align, integral type offset);
```

Allows the compiler to assume that the argument pointer is aligned to at least `align` bytes. The three-parameter version assumes that `(char *)exp - offset` is aligned [CUDA_C_Programming_Guide:L7955-L8630].

### __builtin_assume / __assume

```c
void __builtin_assume(bool exp);
void __assume(bool exp);
```

Allows the compiler to assume that the Boolean argument is true. If the argument is false at runtime, the behavior is undefined. If the argument has side effects, the behavior is unspecified [CUDA_C_Programming_Guide:L7955-L8630].

*   **Restriction:** `__assume()` is only supported when using the `cl.exe` host compiler [CUDA_C_Programming_Guide:L7955-L8630].

### __builtin_expect

```c
long __builtin_expect (long exp, long c);
```

Indicates to the compiler that `exp == c` is expected, typically used for branch prediction [CUDA_C_Programming_Guide:L7955-L8630].

### __builtin_unreachable

```c
void __builtin_unreachable(void);
```

Indicates to the compiler that control flow never reaches this point. The program has undefined behavior if control flow does reach this point at runtime [CUDA_C_Programming_Guide:L7955-L8630].

### Restrictions

If the host compiler does not support these functions, they must be invoked from within the body of a `__device__`/`__global__` function, or only when the `__CUDA_ARCH__` macro is defined [CUDA_C_Programming_Guide:L7955-L8630].

## Warp Vote Functions

Warp vote functions allow threads in a warp to perform a reduction-and-broadcast operation. The deprecated functions `__any`, `__all`, and `__ballot` have been replaced by their `_sync` variants [CUDA_C_Programming_Guide:L7955-L8630].

### Sync Variants

*   `__all_sync(unsigned mask, int predicate)`: Returns non-zero if and only if `predicate` is non-zero for all non-exited threads in `mask` [CUDA_C_Programming_Guide:L7955-L8630].
*   `__any_sync(unsigned mask, int predicate)`: Returns non-zero if and only if `predicate` is non-zero for any non-exited thread in `mask` [CUDA_C_Programming_Guide:L7955-L8630].
*   `__ballot_sync(unsigned mask, int predicate)`: Returns an integer where the Nth bit is set if `predicate` is non-zero for the Nth active thread in `mask` [CUDA_C_Programming_Guide:L7955-L8630].
*   `__activemask()`: Returns a 32-bit integer mask of all currently active threads in the calling warp [CUDA_C_Programming_Guide:L7955-L8630].

### Requirements

*   A mask must be passed specifying the threads participating in the call. Each calling thread must have its own bit set in the mask [CUDA_C_Programming_Guide:L7955-L8630].
*   All non-exited threads named in the mask must execute the same intrinsic with the same mask, or the result is undefined [CUDA_C_Programming_Guide:L7955-L8630].
*   These intrinsics do not imply a memory barrier or guarantee memory ordering [CUDA_C_Programming_Guide:L7955-L8630].

## Warp Match Functions

`__match_any_sync` and `__match_all_sync` perform a broadcast-and-compare operation of a variable between threads within a warp. Supported by devices with compute capability 7.x or higher [CUDA_C_Programming_Guide:L7955-L8630].

### Synopsis

```c
unsigned int __match_any_sync(unsigned mask, T value);
unsigned int __match_all_sync(unsigned mask, T value, int *pred);
```

`T` can be `int`, `unsigned int`, `long`, `unsigned long`, `long long`, `unsigned long long`, `float`, or `double` [CUDA_C_Programming_Guide:L7955-L8630].

### Description

*   `__match_any_sync`: Returns a mask of threads that have the same value as `value` within the `mask` [CUDA_C_Programming_Guide:L7955-L8630].
*   `__match_all_sync`: Returns the `mask` if all threads in `mask` have the same value for `value`; otherwise returns 0. The predicate `pred` is set to true if all threads have the same value, otherwise false [CUDA_C_Programming_Guide:L7955-L8630].

### Requirements

*   A mask must be passed specifying the threads participating in the call. Each calling thread must have its own bit set in the mask [CUDA_C_Programming_Guide:L7955-L8630].
*   All non-exited threads named in the mask must execute the same intrinsic with the same mask, or the result is undefined [CUDA_C_Programming_Guide:L7955-L8630].
*   These intrinsics do not imply a memory barrier or guarantee memory ordering [CUDA_C_Programming_Guide:L7955-L8630].
