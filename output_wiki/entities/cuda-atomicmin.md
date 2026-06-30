# atomicMin()

Performs an atomic minimum operation on 32-bit and 64-bit signed/unsigned integers in global or shared memory. Returns the old value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7864-L7879

Citation: [CUDA_C_Programming_Guide:L7864-L7879]

````text

## 10.14.1.4 atomicMin()

```c
int atomicMin(int* address, int val);
unsigned int atomicMin(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicMin(unsigned long long int* address,
                    unsigned long long int val);
long long int atomicMin(long long int* address,
                    long long int val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory, computes the minimum of old and val, and stores the result back to memory at the same address. These three operations are performed in one atomic transaction. The function returns old.

The 64-bit version of atomicMin() is only supported by devices of compute capability 5.0 and higher.
````
