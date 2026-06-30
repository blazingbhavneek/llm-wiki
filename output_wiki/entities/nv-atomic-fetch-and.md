# 10.14.2.6 __nv_atomic_fetch_and() and __nv_atomic_and() (CUDA 12.8)

Atomic bitwise AND functions introduced in CUDA 12.8. Reads value at ptr, ANDs with val, stores result back to ptr. __nv_atomic_fetch_and returns old value; __nv_atomic_and returns void. Supports integral types of 4 or 8 bytes. Requires sm_60+ for memory order/scope, sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8176-L8192

Citation: [CUDA_C_Programming_Guide:L8176-L8192]

````text

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
````
