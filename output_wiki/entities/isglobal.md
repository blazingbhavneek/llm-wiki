# 10.15.1 __isGlobal()

Address space predicate function. Returns 1 if ptr contains generic address of object in global memory space, otherwise 0. Unspecified behavior if ptr is null.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8277-L8288

Citation: [CUDA_C_Programming_Guide:L8277-L8288]

````text

## 10.15. Address Space Predicate Functions

The functions described in this section have unspecified behavior if the argument is a null pointer.

## 10.15.1. \_\_isGlobal()

```c
__device__ unsigned int __isGlobal(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in global memory space, otherwise returns 0.
````
