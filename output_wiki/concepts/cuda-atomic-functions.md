# CUDA Atomic Functions Overview

CUDA atomic functions perform a read-modify-write atomic operation on one 32-bit, 64-bit, or 128-bit word residing in global or shared memory [CUDA_C_Programming_Guide:L7637-L7650]. In the case of vector types like `float2` or `float4`, the read-modify-write operation is performed on each element of the vector residing in global memory [CUDA_C_Programming_Guide:L7650-L7653]. For example, `atomicAdd()` reads a word at some address in global or shared memory, adds a number to it, and writes the result back to the same address [CUDA_C_Programming_Guide:L7653-L7657].

## Scopes and Ordering

The atomic functions described in the standard API have ordering `cuda::memory_order_relaxed` and are only atomic at a particular scope [CUDA_C_Programming_Guide:L7657-L7659]. The scope is determined by the function suffix:

*   **Device Scope**: Atomic APIs without a suffix (e.g., `atomicAdd`) are atomic at scope `cuda::thread_scope_device` [CUDA_C_Programming_Guide:L7661-L7663].
*   **Block Scope**: Atomic APIs with a `_block` suffix (e.g., `atomicAdd_block`) are atomic at scope `cuda::thread_scope_block` [CUDA_C_Programming_Guide:L7663-L7665].
*   **System Scope**: Atomic APIs with a `_system` suffix (e.g., `atomicAdd_system`) are atomic at scope `cuda::thread_scope_system` if they meet particular conditions [CUDA_C_Programming_Guide:L7659-L7661].

System-wide atomic operations require specific hardware support:
*   Devices with compute capability less than 6.0 only support device-wide atomic operations [CUDA_C_Programming_Guide:L7705-L7707].
*   Tegra devices with compute capability less than 7.2 do not support system-wide atomic operations [CUDA_C_Programming_Guide:L7707-L7709].

## Memory Orders and Builtins (CUDA 12.8+)

CUDA 12.8 and later support CUDA compiler builtin functions for atomic operations with explicit memory order and thread scope [CUDA_C_Programming_Guide:L7709-L7712]. These follow the GNU’s atomic builtin function signature with an extra argument of thread scope [CUDA_C_Programming_Guide:L7712-L7714].

Supported memory orders include:
*   `__NV_ATOMIC_RELAXED`
*   `__NV_ATOMIC_CONSUME` (currently implemented using stronger `__NV_ATOMIC_ACQUIRE`) [CUDA_C_Programming_Guide:L7773-L7775]
*   `__NV_ATOMIC_ACQUIRE`
*   `__NV_ATOMIC_RELEASE`
*   `__NV_ATOMIC_ACQ_REL`
*   `__NV_ATOMIC_SEQ_CST`

Supported thread scopes include:
*   `__NV_THREAD_SCOPE_THREAD` (currently implemented using wider `__NV_THREAD_SCOPE_BLOCK`) [CUDA_C_Programming_Guide:L7775-L7777]
*   `__NV_THREAD_SCOPE_BLOCK`
*   `__NV_THREAD_SCOPE_CLUSTER`
*   `__NV_THREAD_SCOPE_DEVICE`
*   `__NV_THREAD_SCOPE_SYSTEM`

An example signature is:
```c
__device__ T __nv_atomic_load_n(T* ptr, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```
where `T` can be any integral type that is 1, 2, 4, 8, or 16 bytes in size [CUDA_C_Programming_Guide:L7727-L7731].

## Limitations and Constraints

There are several constraints on the use of CUDA atomic functions:

1.  **Memory Type**: Atomic functions cannot operate on local memory. For example, attempting to use `__nv_atomic_load` on a variable defined in local memory within a device function is not permitted [CUDA_C_Programming_Guide:L7731-L7740].
2.  **Scope of Use**: These functions must only be used within the block scope of a `__device__` function [CUDA_C_Programming_Guide:L7740-L7742]. They cannot be used in host functions (`__host__`) [CUDA_C_Programming_Guide:L7742-L7748].
3.  **Address Taking**: The address of atomic functions cannot be taken. This prohibits their use as template default arguments or in constructor initialization lists [CUDA_C_Programming_Guide:L7748-L7773].

## Implementation

Any atomic operation can be implemented based on `atomicCAS()` (Compare And Swap) [CUDA_C_Programming_Guide:L7673-L7675]. For example, `atomicAdd()` for double-precision floating-point numbers is not available on devices with compute capability lower than 6.0 but can be implemented using a CAS loop [CUDA_C_Programming_Guide:L7675-L7693]. The implementation uses integer comparison to avoid hangs in case of NaN values, since NaN is not equal to itself [CUDA_C_Programming_Guide:L7689-L7691].

## Example Usage

The following example demonstrates both CPU and GPU atomically updating an integer value at a managed address:

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
[CUDA_C_Programming_Guide:L7665-L7673]
