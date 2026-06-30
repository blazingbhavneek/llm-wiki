# 10.14.1.16 __nv_atomic_fetch_max() and __nv_atomic_max() (CUDA 12.8)

Atomic maximum functions introduced in CUDA 12.8. Reads value at ptr, compares with val, stores larger value back to ptr. __nv_atomic_fetch_max returns old value; __nv_atomic_max returns void. Supports unsigned int, int, unsigned long long, or long long. Requires sm_60+ for memory order/scope, sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8081-L8097

Citation: [CUDA_C_Programming_Guide:L8081-L8097]

````text

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
````
