# 10.16.6 __cvta_shared_to_generic()

Returns generic pointer obtained by executing PTX cvta.shared instruction on rawbits value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8397-L8404

Citation: [CUDA_C_Programming_Guide:L8397-L8404]

````text

## 10.16.6. \_\_cvta\_shared\_to\_generic()

```c
__device__ void * __cvta_shared_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.shared instruction on the value provided by rawbits.
````
