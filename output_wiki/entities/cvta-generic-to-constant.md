# 10.16.3 __cvta_generic_to_constant()

Returns result of executing PTX cvta.to.const instruction on generic address denoted by ptr.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8373-L8380

Citation: [CUDA_C_Programming_Guide:L8373-L8380]

````text

## 10.16.3. \_\_cvta\_generic\_to\_constant()

```c
__device__ size_t __cvta_generic_to_constant(const void *ptr);
```

Returns the result of executing the PTXcvta.to.const instruction on the generic address denoted by ptr.
````
