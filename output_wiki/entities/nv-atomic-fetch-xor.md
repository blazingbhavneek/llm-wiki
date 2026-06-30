# 10.14.2.5 __nv_atomic_fetch_xor() and __nv_atomic_xor() (CUDA 12.8)

Atomic bitwise XOR functions introduced in CUDA 12.8. Reads value at ptr, XORs with val, stores result back to ptr. __nv_atomic_fetch_xor returns old value; __nv_atomic_xor returns void. Supports integral types of 4 or 8 bytes. Requires sm_60+ for memory order/scope, sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8159-L8175

Citation: [CUDA_C_Programming_Guide:L8159-L8175]

````text

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
````
