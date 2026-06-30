# Tensor Map Alignment and Properties

Covers negative indices, out-of-bounds handling, size/stride definitions, and alignment requirements for multi-dimensional bulk tensor asynchronous copy operations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L10564-L10570

Citation: [CUDA_C_Programming_Guide:L10564-L10570]

````text
Negative indices and out of bounds. When part of the tile that is being read from global to shared memory is out of bounds, the shared memory that corresponds to the out of bounds area is zerofilled. The top-left corner indices of the tile may also be negative. When writing from shared to global memory, parts of the tile may be out of bounds, but the top left corner cannot have any negative indices.

Size and stride. The size of a tensor is the number of elements along one dimension. All sizes must be greater than one. The stride is the number of bytes between elements of the same dimension. For instance, a 4 x 4 matrix of integers has sizes 4 and 4. Since it has 4 bytes per element, the strides are 4 and 16 bytes. Due to alignment requirements, a 4 x 3 row-major matrix of integers must have strides of 4 and 16 bytes as well. Each row is padded with 4 extra bytes to ensure that the start of the next row is aligned to 16 bytes. For more information regarding alignment, refer to Table 10.

Table 10: Alignment requirements for multi-dimensional bulk tensor asynchronous copy operations in Compute Capability 9.0.

<table><tr><td>Address / Size</td><td>Alignment</td></tr><tr><td>Global memory address</td><td>Must be 16 byte aligned.</td></tr><tr><td>Global memory sizes</td><td>Must be greater than or equal to one. Does not have to be a multiple of 16 bytes.</td></tr><tr><td>Global memory strides</td><td>Must be multiples of 16 bytes.</td></tr><tr><td>Shared memory address</td><td>Must be 128 byte aligned.</td></tr><tr><td>Shared memory barrier address</td><td>Must be 8 byte aligned (this is guaranteed by cuda::barrier).</td></tr><tr><td>Size of transfer</td><td>Must be a multiple of 16 bytes.</td></tr></table>
````
