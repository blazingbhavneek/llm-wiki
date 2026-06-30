# 10.14.3.5 __nv_atomic_thread_fence() (CUDA 12.8)

Atomic thread fence function introduced in CUDA 12.8. Establishes ordering between memory accesses based on specified memory order. Thread scope parameter specifies observing threads. Requires sm_90+ for cluster scope. Arguments order and scope must be integer literals.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8265-L8276

Citation: [CUDA_C_Programming_Guide:L8265-L8276]

````text

## 10.14.3.5 \_\_nv\_atomic\_thread\_fence()

```c
__device__ void __nv_atomic_thread_fence (int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function establishes an ordering between memory accesses requested by this thread based on the specified memory order. And the thread scope parameter specifies the set of threads that may observe the ordering efect of this operation.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.
````
