# 10.17 Alloca Function

Allocates size bytes of memory in the stack frame of the caller. Returns 16-byte aligned pointer in device code. Automatically freed on function return. Requires compute capability 5.2+. On Windows, <malloc.h> must be included. May cause stack overflow.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8421-L8436

Citation: [CUDA_C_Programming_Guide:L8421-L8436]

````text

## 10.17. Alloca Function

## 10.17.1. Synopsis

```c
__host__ __device__ void * alloca(size_t size);
```

## 10.17.2. Description

The alloca() function allocates size bytes of memory in the stack frame of the caller. The returned value is a pointer to allocated memory, the beginning of the memory is 16 bytes aligned when the function is invoked from device code. The allocated memory is automatically freed when the caller to alloca() is returned.

Note: On Windows platform, <malloc.h> must be included before using alloca(). Using alloca() may cause the stack to overflow, user needs to adjust stack size accordingly.

It is supported with compute capability 5.2 or higher.
````
