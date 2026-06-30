# 10.14.1.15 __nv_atomic_fetch_min() and __nv_atomic_min() (CUDA 12.8)

Atomic minimum functions introduced in CUDA 12.8. Reads value at ptr, compares with val, stores smaller value back to ptr. __nv_atomic_fetch_min returns old value; __nv_atomic_min returns void. Supports unsigned int, int, unsigned long long, or long long. Requires sm_60+ for memory order/scope, sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8064-L8080

Citation: [CUDA_C_Programming_Guide:L8064-L8080]

````text

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
````
