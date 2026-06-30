# 10.15.3 __isConstant()

Address space predicate function. Returns 1 if ptr contains generic address of object in constant memory space, otherwise 0. Unspecified behavior if ptr is null.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8297-L8304

Citation: [CUDA_C_Programming_Guide:L8297-L8304]

````text

## 10.15.3. \_\_isConstant()

```txt
__device__ unsigned int __isConstant(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in constant memory space, otherwise returns 0.
````
