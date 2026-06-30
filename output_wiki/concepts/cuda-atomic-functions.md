# Atomic Functions

Overview of CUDA atomic read-modify-write operations on global or shared memory, including scope definitions (device, block, system), memory ordering, and CUDA 12.8+ builtin function signatures.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7637-L7785

Citation: [CUDA_C_Programming_Guide:L7637-L7785]

````text
## 10.14. Atomic Functions

An atomic function performs a read-modify-write atomic operation on one 32-bit, 64-bit, or 128-bit word residing in global or shared memory. In the case of float2 or float4, the read-modify-write operation is performed on each element of the vector residing in global memory. For example, atomicAdd() reads a word at some address in global or shared memory, adds a number to it, and writes the result back to the same address. Atomic functions can only be used in device functions.

The atomic functions described in this section have ordering cuda::memory\_order\_relaxed and are only atomic at a particular scope:

Atomic APIs with \_system sufix (example: atomicAdd\_system) are atomic at scope cuda::thread\_scope\_system if they meet particular conditions.

1 Atomic APIs without a sufix (example: atomicAdd) are atomic at scope cuda::thread\_scope\_device.

▶ Atomic APIs with \_block sufix (example: atomicAdd\_block) are atomic at scope cuda::thread\_scope\_block.

In the following example both the CPU and the GPU atomically update an integer value at address addr:

```c
__global__ void mykernel(int *addr) {
    atomicAdd_system(addr, 10);          // only available on devices with compute
    capability 6.x
}

void foo() {
    int *addr;
    cudaMallocManaged(&addr, 4);
    *addr = 0;

    mykernel<<<...>>>(addr);
    __sync_fetch_and_add(addr, 10);  // CPU atomic operation
}
```

Note that any atomic operation can be implemented based on atomicCAS() (Compare And Swap). For example, atomicAdd() for double-precision floating-point numbers is not available on devices with compute capability lower than 6.0 but it can be implemented as follows:

```c
#if __CUDA_ARCH__ < 600
__device__ double atomicAdd(double* address, double val)
{
    unsigned long long int* address_as_ull =
        (unsigned long long int*)address;
    unsigned long long int old = *address_as_ull, assumed;

    do {
        assumed = old;
        old = atomicCAS(address_as_ull, assumed,
            __double_as_longlong(val +
                __longlong_as_double(assumed)));

    // Note: uses integer comparison to avoid hang in case of NaN (since NaN != NaN)
    } while (assumed != old);

    return __longlong_as_double(old);
}
#endif
```

There are system-wide and block-wide variants of the following device-wide atomic APIs, with the following exceptions:

▶ Devices with compute capability less than 6.0 only support device-wide atomic operations,

▶ Tegra devices with compute capability less than 7.2 do not support system-wide atomic operations.

CUDA 12.8 and later support CUDA compiler builtin functions for atomic operations with memory order and thread scope. We follows the GNU’s atomic built-in function signature with an extra argument of thread scope. We use the following atomic operation memory orders and thread scopes:

```c
enum {
    __NV_ATOMIC_RELAXED,
    __NV_ATOMIC_CONSUME,
    __NV_ATOMIC_ACQUIRE,
    __NV_ATOMIC_RELEASE,
    __NV_ATOMIC_ACQ_REL,
```

(continues on next page)

```c
__NV_ATOMIC_SEQ_CST
};

enum {
    __NV_THREAD_SCOPE_THREAD,
    __NV_THREAD_SCOPE_BLOCK,
    __NV_THREAD_SCOPE_CLUSTER,
    __NV_THREAD_SCOPE_DEVICE,
    __NV_THREAD_SCOPE_SYSTEM
};
```

(continued from previous page)

Example:

```c
__device__ T __nv_atomic_load_n(T* ptr, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

T can be any integral type that is size of 1, 2, 4, 8 and 16 bytes.

These atomic functions cannot operate on local memory. For example:

```c
__device__ void foo() {
    int a = 1; // defined in local memory
    int b;
    __nv_atomic_load(&a, &b, __NV_ATOMIC_RELAXED, __NV_THREAD_SCOPE_SYSTEM);
}
```

These functions must only be used within the block scope of a \_\_device\_\_ function. For example:

```c
__device__ void foo() {
    __shared__ unsigned int u1 = 1;
    __shared__ unsigned int u2 = 2;
    __nv_atomic_load(&u1, &u2, __NV_ATOMIC_RELAXED, __NV_THREAD_SCOPE_SYSTEM);
}
```

And these functions’ address cannot be taken. Here are three unsupported examples:

```txt
// Not permitted to be used in a host function
__host__ void bar() {
    __shared__ unsigned int u1 = 1;
    __shared__ unsigned int u2 = 2;
    __nv_atomic_load(&u1, &u2, __NV_ATOMIC_RELAXED, __NV_THREAD_SCOPE_SYSTEM);
}

// Not permitted to be used as a template default argument.
// The function address cannot be taken.
template<void *F = __nv_atomic_load_n>
class X {
    void *f = F;
};

// Not permitted to be called in a constructor initialization list.
class Y {
    int a;
public:
    __device__ Y(int *b): a(__nv_atomic_load_n(b, __NV_ATOMIC_RELAXED)) {}
};
```

The memory order corresponds to C++ standard atomic operation’s memory order. And for thread scope, we follows cuda::thread\_scope’s definition.

\_\_NV\_ATOMIC\_CONSUME memory order is currently implemented using stronger \_\_NV\_ATOMIC\_ACQUIRE memory order.

\_\_NV\_THREAD\_SCOPE\_THREAD thread scope is currently implemented using wider \_\_NV\_THREAD\_SCOPE\_BLOCK thread scope.

For the supported data types, please refer to the corresponding section of diferent atomic operations.
````
