# 10.14.2.3 atomicXor()

Atomic bitwise XOR function. Reads 32-bit or 64-bit word at address, computes (old ^ val), stores result back. Returns old value. 64-bit version requires compute capability 5.0 or higher.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8129-L8142

Citation: [CUDA_C_Programming_Guide:L8129-L8142]

````text
## 10.14.2.3 atomicXor()

```c
int atomicXor(int* address, int val);
unsigned int atomicXor(unsigned int* address,
                      unsigned int val);
unsigned long long int atomicXor(unsigned long long int* address,
                       unsigned long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes (old ^ val), and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicXor() is only supported by devices of compute capability 5.0 and higher.
````
