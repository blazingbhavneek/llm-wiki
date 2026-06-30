# Memory Type (CUDA 10.2+)

Introduction to user-controlled memory allocation via cuMemCreate and CUmemAllocationProp::allocFlags.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15097-L15100

Citation: [CUDA_C_Programming_Guide:L15097-L15100]

````text
## 14.3.2. Memory Type

Before CUDA 10.2, applications had no user-controlled way of allocating any special type of memory that certain devices may support. With cuMemCreate, applications can additionally specify memory type requirements using the CUmemAllocationProp::allocFlags to opt into any specific memory features. Applications must also ensure that the requested memory type is supported on the device of allocation.
````
