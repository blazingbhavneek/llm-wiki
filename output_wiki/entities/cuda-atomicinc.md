# atomicInc()

Performs an atomic increment operation on a 32-bit unsigned integer in global or shared memory. Returns the old value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7896-L7904

Citation: [CUDA_C_Programming_Guide:L7896-L7904]

````text

## 10.14.1.6 atomicInc()

```txt
unsigned int atomicInc(unsigned int* address,
                                unsigned int val);
```

reads the 32-bit word old located at the address address in global or shared memory, computes ((old >= val) ? 0 : (old+1)), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.
````
