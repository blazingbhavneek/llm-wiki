# 10.16.4 __cvta_generic_to_local()

Returns result of executing PTX cvta.to.local instruction on generic address denoted by ptr.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8381-L8388

Citation: [CUDA_C_Programming_Guide:L8381-L8388]

````text

## 10.16.4. \_\_cvta\_generic\_to\_local()

```c
__device__ size_t __cvta_generic_to_local(const void *ptr);
```

Returns the result of executing the PTXcvta.to.local instruction on the generic address denoted by ptr.
````
