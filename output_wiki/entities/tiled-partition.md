# tiled_partition

The `tiled_partition` function is a collective operation that partitions a parent group into a one-dimensional, row-major tiling of subgroups. It allows threads within a block or tile to organize themselves into smaller, manageable groups for coordinated execution.

## Syntax

The function provides two overloads:

```cpp
template <unsigned int Size, typename ParentT>
thread_block_tile<Size, ParentT> tiled_partition(const ParentT& g);

thread_group tiled_partition(const thread_group& parent, unsigned int tilesz);
```

## Parameters

- **ParentT / parent**: The parent group to be partitioned. Valid parent groups are `thread_block` or `thread_block_tile`.
- **Size / tilesz**: The size of the resulting subgroups. This value must evenly divide the size of the parent group.

## Requirements and Constraints

### Group Size Constraints
- The parent group size must be evenly divisible by the `Size` parameter.
- The size of the parent group (`cg::size(parent)`) must be greater than the `Size` parameter.

### Supported Sizes
- **Native Hardware Sizes**: 1, 2, 4, 8, 16, 32.
- **Larger Sizes**: 64, 128, 256, 512 are supported via the templated version.

### Compute Capability and Compiler Requirements
- **Minimum Compute Capability**: 5.0.
- **C++ Standard**: C++11 is required for partition sizes larger than 32.
- **Compute Capability 7.5 or Lower**: Additional steps may be required when using sizes 64, 128, 256, or 512. Refer to the *Thread Block Tile* documentation for details on these requirements.

## Execution Behavior

The implementation may cause the calling thread to wait until all members of the parent group have invoked the operation before resuming execution. This ensures deterministic synchronization across the partitioned subgroups.

## Example

The following example demonstrates creating a 32-thread tile from a block, and then partitioning that tile into smaller groups of 4 threads.

```cpp
/// The following code will create a 32-thread tile
thread_block block = this_thread_block();
thread_block_tile<32> tile32 = tiled_partition<32>(block);

// We can partition each of these groups into even smaller groups, each of size 4 threads:
auto tile4 = tiled_partition<4>(tile32);
// or using a general group
// thread_group tile4 = tiled_partition(tile32, 4);
```

If the following code is executed within the `tile4` context:

```cpp
if (tile4.thread_rank()==0) printf("Hello from tile4 rank 0\n");
```

The statement will be printed by every fourth thread in the block. Specifically, it is printed by the threads with rank 0 in each `tile4` group, which correspond to threads with ranks 0, 4, 8, 12, etc., in the original block group.

## References

- CUDA C++ Programming Guide: [CUDA_C_Programming_Guide:L12464-L12503]
