# 10.16.8 __cvta_local_to_generic()

Returns generic pointer obtained by executing PTX cvta.local instruction on rawbits value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8413-L8420

Citation: [CUDA_C_Programming_Guide:L8413-L8420]

````text

## 10.16.8. \_\_cvta\_local\_to\_generic()

```c
__device__ void * __cvta_local_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.local instruction on the value provided by rawbits.
````
