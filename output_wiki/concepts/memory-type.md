# Memory Type

Before CUDA 10.2, applications had no user-controlled way of allocating any special type of memory that certain devices may support [CUDA_C_Programming_Guide:L15097-L15100].

With the introduction of `cuMemCreate`, applications can additionally specify memory type requirements using the `CUmemAllocationProp::allocFlags` to opt into any specific memory features [CUDA_C_Programming_Guide:L15097-L15100]. Applications must also ensure that the requested memory type is supported on the device of allocation [CUDA_C_Programming_Guide:L15097-L15100].
