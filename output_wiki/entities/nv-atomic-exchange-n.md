# 10.14.1.10 __nv_atomic_exchange_n() (CUDA 12.8)

Non-generic atomic exchange function introduced in CUDA 12.8. Reads value at ptr, returns it. Stores val to ptr. Supports integral types of 4, 8, or 16 bytes. Requires sm_60+ for memory order/scope, sm_90+ for 16-byte types and cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7974-L7990

Citation: [CUDA_C_Programming_Guide:L7974-L7990]

````text
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
````
