# Global Memory Alignment and Size Requirements

Global memory instructions support reading or writing words of size equal to 1, 2, 4, 8, or 16 bytes [CUDA_C_Programming_Guide:L6427-L6433]. Any access (via a variable or a pointer) to data residing in global memory compiles to a single global memory instruction if and only if the size of the data type is 1, 2, 4, 8, or 16 bytes and the data is naturally aligned (i.e., its address is a multiple of that size) [CUDA_C_Programming_Guide:L6433-L6437].

## Coalescing and Performance

If the size and alignment requirement is not fulfilled, the access compiles to multiple instructions with interleaved access patterns that prevent these instructions from fully coalescing [CUDA_C_Programming_Guide:L6439-L6441]. It is therefore recommended to use types that meet this requirement for data that resides in global memory [CUDA_C_Programming_Guide:L6441-L6442].

## Alignment Guarantees and Specifiers

The alignment requirement is automatically fulfilled for the Built-in Vector Types [CUDA_C_Programming_Guide:L6444-L6445].

For structures, the size and alignment requirements can be enforced by the compiler using the alignment specifiers `__align__(8)` or `__align__(16)` [CUDA_C_Programming_Guide:L6447-L6449]. Examples include:

```cpp
struct __align__(8) {
    float x;
    float y;
};
```

```cpp
struct __align__(16) {
    float x;
    float y;
    float z;
};
```

Any address of a variable residing in global memory or returned by one of the memory allocation routines from the driver or runtime API is always aligned to at least 256 bytes [CUDA_C_Programming_Guide:L6451-L6452].

## Risks of Non-Aligned Accesses

Reading non-naturally aligned 8-byte or 16-byte words produces incorrect results (off by a few words), so special care must be taken to maintain alignment of the starting address of any value or array of values of these types [CUDA_C_Programming_Guide:L6453-L6455].

A typical case where this might be easily overlooked is when using some custom global memory allocation scheme, whereby the allocations of multiple arrays (with multiple calls to `cudaMalloc()` or `cuMemAlloc()`) is replaced by the allocation of a single large block of memory partitioned into multiple arrays, in which case the starting address of each array is offset from the block’s starting address [CUDA_C_Programming_Guide:L6455-L6459].
