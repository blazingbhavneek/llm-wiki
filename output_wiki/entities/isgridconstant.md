# 10.15.4 __isGridConstant()

Address space predicate function. Returns 1 if ptr contains generic address of kernel parameter annotated with __grid_constant__, otherwise 0. Only supported for compute architectures >= 7.x. Unspecified behavior if ptr is null.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8305-L8312

Citation: [CUDA_C_Programming_Guide:L8305-L8312]

````text

## 10.15.4. \_\_isGridConstant()

```txt
__device__ unsigned int __isGridConstant(const void *ptr);
```

Returns 1 if ptr contains the generic address of a kernel parameter annotated with \_\_grid\_constant\_\_, otherwise returns 0. Only supported for compute architectures greater than or equal to 7.x or later.
````
