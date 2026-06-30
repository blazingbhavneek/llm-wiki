# 10.14.3.1 __nv_atomic_load() (CUDA 12.8)

Generic atomic load function introduced in CUDA 12.8. Loads value at ptr and writes to ret. Supports 1, 2, 4, 8, or 16-byte types. Requires sm_60+ for memory order/scope, sm_70+ for 16-byte types, sm_90+ for cluster scope. Arguments order and scope must be integer literals. order cannot be __NV_ATOMIC_RELEASE or __NV_ATOMIC_ACQ_REL.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8193-L8212

Citation: [CUDA_C_Programming_Guide:L8193-L8212]

````text

## 10.14.3. Other atomic functions

## 10.14.3.1 \_\_nv\_atomic\_load()

```c
__device__ void __nv_atomic_load(T* ptr, T* ret, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It loads the value where ptr points to and writes the value to where ret points to.

This is a generic atomic load, which means that T can be any data type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_RELEASE or \_\_NV\_ATOMIC\_ACQ\_REL.
````
