# 10.15.2 __isShared()

Address space predicate function. Returns 1 if ptr contains generic address of object in shared memory space, otherwise 0. Unspecified behavior if ptr is null.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8289-L8296

Citation: [CUDA_C_Programming_Guide:L8289-L8296]

````text

## 10.15.2. \_\_isShared()

```c
__device__ unsigned int __isShared(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in shared memory space, otherwise returns 0.
````
