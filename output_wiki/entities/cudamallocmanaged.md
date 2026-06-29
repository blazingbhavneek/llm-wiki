# cudaMallocManaged

`cudaMallocManaged` is the allocation API for CUDA Managed Memory on systems that support it. It allows for the allocation of unified memory.

## Syntax

```c
__host__ cudaError_t cudaMallocManaged(void **devPtr, size_t size);
```

## Description

The `cudaMallocManaged` API is syntactically identical to `cudaMalloc`. It performs the following actions:

*   Allocates `size` bytes of managed memory.
*   Sets the pointer `devPtr` to refer to the newly allocated allocation.

## Deallocation

Memory allocated with `cudaMallocManaged` must be deallocated using `cudaFree`.

## References

- [CUDA_C_Programming_Guide:L20998-L21007]
