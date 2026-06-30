# 10.14.3.4 __nv_atomic_store_n() (CUDA 12.8)

Non-generic atomic store function introduced in CUDA 12.8. Stores val to ptr. Supports integral types of 1, 2, 4, 8, or 16 bytes. Requires sm_60+ for memory order/scope, sm_70+ for 16-byte types, sm_90+ for cluster scope. Arguments order and scope must be integer literals. order cannot be __NV_ATOMIC_CONSUME, __NV_ATOMIC_ACQUIRE, or __NV_ATOMIC_ACQ_REL.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8247-L8264

Citation: [CUDA_C_Programming_Guide:L8247-L8264]

````text

## 10.14.3.4 \_\_nv\_atomic\_store\_n()

```txt
__device__ void __nv_atomic_store_n(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It stores val to where ptr points to.

This is a non-generic atomic load, which means that T can only be an integral type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_CONSUME, \_\_NV\_ATOMIC\_ACQUIRE or \_\_NV\_ATOMIC\_ACQ\_REL.
````
