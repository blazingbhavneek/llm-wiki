# TMA Alignment and Bounds Handling

This page details the constraints for bounds checking and memory alignment when performing multi-dimensional bulk tensor asynchronous copy operations in Compute Capability 9.0.

## Bounds Handling

Tensor Memory Access (TMA) operations handle out-of-bounds accesses differently depending on the direction of the copy.

### Global to Shared Memory Reads
When reading from global memory to shared memory, the top-left corner indices of the tile may be negative. If part of the tile is out of bounds, the corresponding area in shared memory is zero-filled [CUDA_C_Programming_Guide:L10564-L10570].

### Shared to Global Memory Writes
When writing from shared memory to global memory, parts of the tile may be out of bounds. However, the top-left corner of the tile cannot have any negative indices [CUDA_C_Programming_Guide:L10564-L10570].

## Alignment and Stride Requirements

### Definitions
*   **Size**: The number of elements along one dimension. All sizes must be greater than one [CUDA_C_Programming_Guide:L10564-L10570].
*   **Stride**: The number of bytes between elements of the same dimension [CUDA_C_Programming_Guide:L10564-L10570].

### Alignment Constraints
The following table summarizes the alignment requirements for multi-dimensional bulk tensor asynchronous copy operations in Compute Capability 9.0 [CUDA_C_Programming_Guide:L10564-L10570]:

| Address / Size | Alignment Requirement |
| :--- | :--- |
| Global memory address | Must be 16 byte aligned. |
| Global memory sizes | Must be greater than or equal to one. Does not have to be a multiple of 16 bytes. |
| Global memory strides | Must be multiples of 16 bytes. |
| Shared memory address | Must be 128 byte aligned. |
| Shared memory barrier address | Must be 8 byte aligned (this is guaranteed by `cuda::barrier`). |
| Size of transfer | Must be a multiple of 16 bytes. |

### Example: Row-Major Padding
Due to alignment requirements, a row-major matrix may require padding. For instance, a 4x3 row-major matrix of integers must have strides of 4 and 16 bytes. Although the logical width is 3 elements (12 bytes), the stride is 16 bytes. This ensures that each row is padded with 4 extra bytes so that the start of the next row is aligned to 16 bytes [CUDA_C_Programming_Guide:L10564-L10570].
