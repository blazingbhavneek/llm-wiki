# 10.14.1.12 __nv_atomic_compare_exchange_n() (CUDA 12.8)

Non-generic atomic compare-and-exchange function introduced in CUDA 12.8. Compares value at ptr with value at expected. If equal, returns true and stores desired to ptr. Otherwise, returns false and stores ptr value to expected. Ignores weak parameter, uses stronger of success/failure orders. Supports integral types of 2, 4, 8, or 16 bytes. Requires sm_60+ for memory order/scope, sm_90+ for 16-byte types, sm_70+ for 2-byte types, and sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8010-L8029

Citation: [CUDA_C_Programming_Guide:L8010-L8029]

````text
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
````
