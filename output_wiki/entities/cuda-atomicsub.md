# atomicSub()

Performs an atomic subtraction operation on 32-bit integers in global or shared memory. Computes (old - val) and returns the old value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7824-L7833

Citation: [CUDA_C_Programming_Guide:L7824-L7833]

````text
## 10.14.1.2 atomicSub()

```c
int atomicSub(int* address, int val);
unsigned int atomicSub(unsigned int* address,
                                unsigned int val);
```

reads the 32-bit word old located at the address address in global or shared memory, computes (old - val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.
````
