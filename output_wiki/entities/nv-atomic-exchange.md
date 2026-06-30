# 10.14.1.9 __nv_atomic_exchange() (CUDA 12.8)

Generic atomic exchange function introduced in CUDA 12.8. Reads value at ptr, stores to ret. Reads value at val, stores to ptr. Supports 4, 8, or 16-byte types. Requires sm_60+ for memory order/scope, sm_90+ for 16-byte types and cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7955-L7973

Citation: [CUDA_C_Programming_Guide:L7955-L7973]

````text
## 10.14.1.9 \_\_nv\_atomic\_exchange()

```c
__device__ void __nv_atomic_exchange(T* ptr, T* val, T *ret, int order, int scope = __
->NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It reads the value where ptr points to and stores the value to where ret points to. And it reads the value where val points to and stores the value to where ptr points to.

This is a generic atomic exchange, which means that T can be any data type that is size of 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_90 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.
````
