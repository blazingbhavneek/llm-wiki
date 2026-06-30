# 10.16.2 __cvta_generic_to_shared()

Returns result of executing PTX cvta.to.shared instruction on generic address denoted by ptr.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8365-L8372

Citation: [CUDA_C_Programming_Guide:L8365-L8372]

````text

## 10.16.2. \_\_cvta\_generic\_to\_shared()

```c
__device__ size_t __cvta_generic_to_shared(const void *ptr);
```

Returns the result of executing the PTXcvta.to.shared instruction on the generic address denoted by ptr.
````
