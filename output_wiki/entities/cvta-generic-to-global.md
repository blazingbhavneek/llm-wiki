# 10.16.1 __cvta_generic_to_global()

Returns result of executing PTX cvta.to.global instruction on generic address denoted by ptr.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8357-L8364

Citation: [CUDA_C_Programming_Guide:L8357-L8364]

````text

## 10.16.1. \_\_cvta\_generic\_to\_global()

```c
__device__ size_t __cvta_generic_to_global(const void *ptr);
```

Returns the result of executing the PTXcvta.to.global instruction on the generic address denoted by ptr.
````
