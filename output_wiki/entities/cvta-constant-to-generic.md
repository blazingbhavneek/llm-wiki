# 10.16.7 __cvta_constant_to_generic()

Returns generic pointer obtained by executing PTX cvta.const instruction on rawbits value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8405-L8412

Citation: [CUDA_C_Programming_Guide:L8405-L8412]

````text

## 10.16.7. \_\_cvta\_constant\_to\_generic()

```c
__device__ void * __cvta_constant_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.const instruction on the value provided by rawbits.
````
