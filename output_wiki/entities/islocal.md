# 10.15.5 __isLocal()

Address space predicate function. Returns 1 if ptr contains generic address of object in local memory space, otherwise 0. Unspecified behavior if ptr is null.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8313-L8320

Citation: [CUDA_C_Programming_Guide:L8313-L8320]

````text

## 10.15.5. \_\_isLocal()

```c
__device__ unsigned int __isLocal(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in local memory space, otherwise returns 0.
````
