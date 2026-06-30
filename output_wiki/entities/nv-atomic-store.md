# 10.14.3.3 __nv_atomic_store() (CUDA 12.8)

Generic atomic store function introduced in CUDA 12.8. Reads value at val and stores to ptr. Supports 1, 2, 4, 8, or 16-byte types. Requires sm_60+ for memory order/scope, sm_70+ for 16-byte types, sm_90+ for cluster scope. Arguments order and scope must be integer literals. order cannot be __NV_ATOMIC_CONSUME, __NV_ATOMIC_ACQUIRE, or __NV_ATOMIC_ACQ_REL.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8231-L8246

Citation: [CUDA_C_Programming_Guide:L8231-L8246]

````text

## 10.14.3.3 \_\_nv\_atomic\_store()

\_device\_\_ void \_\_nv\_atomic\_store(T\* ptr, T\* val, int order, int scope = \_\_NV\_THREAD\_ , SCOPE\_SYSTEM);

This atomic function is introduced in CUDA 12.8. It reads the value where val points to and stores to where ptr points to.

This is a generic atomic load, which means that T can be any data type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_CONSUME, \_\_NV\_ATOMIC\_ACQUIRE or \_\_NV\_ATOMIC\_ACQ\_REL.
````
