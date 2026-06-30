# 10.16.5 __cvta_global_to_generic()

Returns generic pointer obtained by executing PTX cvta.global instruction on rawbits value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8389-L8396

Citation: [CUDA_C_Programming_Guide:L8389-L8396]

````text

## 10.16.5. \_\_cvta\_global\_to\_generic()

```c
__device__ void * __cvta_global_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.global instruction on the value provided by rawbits.
````
