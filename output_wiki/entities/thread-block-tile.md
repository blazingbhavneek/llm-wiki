# thread_block_tile

`thread_block_tile` is a templated version of a tiled group where the template parameter specifies the size of the tile. Because the size is known at compile time, there is potential for more optimal execution compared to dynamic group sizes [[CUDA_C_Programming_Guide:L12204-L12314]].

## Definition and Construction

The class is defined as follows:

```cpp
template <unsigned int Size, typename ParentT = void>
class thread_block_tile;
```

It is constructed using the `tiled_partition` function:

```cpp
template <unsigned int Size, typename ParentT>
_CG_QUALIFIER thread_block_tile<Size, ParentT> tiled_partition(const ParentT& g)
```

### Parameters
- **Size**: Must be a power of 2 and less than or equal to 1024 [[CUDA_C_Programming_Guide:L12204-L12314]].
- **ParentT**: The parent-type from which this group was partitioned. It is automatically inferred, but a value of `void` stores this information in the group handle rather than in the type [[CUDA_C_Programming_Guide:L12204-L12314]].

## Public Member Functions

### Synchronization and Identification
- `void sync() const`: Synchronize the threads named in the group [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned long long num_threads() const`: Returns the total number of threads in the group [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned long long thread_rank() const`: Returns the rank of the calling thread within `[0, num_threads)` [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned long long meta_group_size() const`: Returns the number of groups created when the parent group was partitioned [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned long long meta_group_rank() const`: Returns the linear rank of the group within the set of tiles partitioned from a parent group (bounded by `meta_group_size`) [[CUDA_C_Programming_Guide:L12204-L12314]].

### Shuffle Operations
- `T shfl(T var, unsigned int src_rank) const`: Refer to Warp Shuffle Functions. For sizes larger than 32, all threads in the group must specify the same `src_rank`, otherwise the behavior is undefined [[CUDA_C_Programming_Guide:L12204-L12314]].
- `T shfl_up(T var, int delta) const`: Refer to Warp Shuffle Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].
- `T shfl_down(T var, int delta) const`: Refer to Warp Shuffle Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].
- `T shfl_xor(T var, int delta) const`: Refer to Warp Shuffle Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].

### Vote and Match Functions
- `int any(int predicate) const`: Refer to Warp Vote Functions [[CUDA_C_Programming_Guide:L12204-L12314]].
- `int all(int predicate) const`: Refer to Warp Vote Functions [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned int ballot(int predicate) const`: Refer to Warp Vote Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned int match_any(T val) const`: Refer to Warp Match Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].
- `unsigned int match_all(T val, int &pred) const`: Refer to Warp Match Functions. Available only for sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].

### Legacy Aliases
- `unsigned long long size() const`: Alias of `num_threads()` [[CUDA_C_Programming_Guide:L12204-L12314]].

## Type Constraints for Shuffle

When compiled with C++11 or later, `shfl`, `shfl_up`, `shfl_down`, and `shfl_xor` functions accept objects of any type, provided they satisfy the following constraints:
1. The type qualifies as trivially copyable (`std::is_trivially_copyable<T>::value == true`) [[CUDA_C_Programming_Guide:L12204-L12314]].
2. `sizeof(T) <= 32` for tile sizes lower or equal to 32 [[CUDA_C_Programming_Guide:L12204-L12314]].
3. `sizeof(T) <= 8` for larger tiles [[CUDA_C_Programming_Guide:L12204-L12314]].

## Memory Requirements

On hardware with Compute Capability 7.5 or lower, tiles of size larger than 32 require a small amount of memory reserved for them. This is handled using the `cooperative_groups::block_tile_memory` struct template, which must reside in either shared or global memory [[CUDA_C_Programming_Guide:L12204-L12314]].

```cpp
template <unsigned int MaxBlockSize = 1024>
struct block_tile_memory;
```

- **MaxBlockSize**: Specifies the maximal number of threads in the current thread block. This parameter can be used to minimize the shared memory usage of `block_tile_memory` in kernels launched only with smaller thread counts [[CUDA_C_Programming_Guide:L12204-L12314]].

To use `block_tile_memory`, it must be passed into `cooperative_groups::this_thread_block`. The overload of `this_thread_block` accepting `block_tile_memory` is a collective operation and must be called with all threads in the thread block [[CUDA_C_Programming_Guide:L12204-L12314]].

On hardware with Compute Capability 8.0 or higher, large tiles do not require `block_tile_memory`. However, `block_tile_memory` can still be used on CC 8.0+ to write one source targeting multiple different Compute Capabilities; it consumes no memory when instantiated in shared memory in cases where it is not required [[CUDA_C_Programming_Guide:L12204-L12314]].

## Examples

### Basic Partitioning
The following code creates two sets of tiled groups, of size 32 and 4, respectively. The latter has the provenance encoded in the type, while the first stores it in the handle [[CUDA_C_Programming_Guide:L12204-L12314]].

```cpp
thread_block block = this_thread_block();
thread_block_tile<32> tile32 = tiled_partition<32>(block);
thread_block_tile<4, thread_block> tile4 = tiled_partition<4>(block);
```

### Warp-Synchronous Code Pattern
Developers who previously made implicit assumptions about warp size in warp-synchronous code must now specify it explicitly. Tiled subgroups evenly partition a parent group into adjacent sets of threads [[CUDA_C_Programming_Guide:L12315-L12337]].

```cpp
__global__ void cooperative_kernel(...) {
    // obtain default "current thread block" group
    thread_block my_block = this_thread_block();

    // subdivide into 32-thread, tiled subgroups
    // Tiled subgroups evenly partition a parent group into
    // adjacent sets of threads - in this case each one warp in size
    auto my_tile = tiled_partition<32>(my_block);

    // This operation will be performed by only the
    // first 32-thread tile of each block
    if (my_tile.meta_group_rank() == 0) {
        // ...
        my_tile.sync();
    }
}
```

### Using block_tile_memory for CC 7.5 and Lower
The following code creates tiles of size 128 on all Compute Capabilities. On CC 8.0 or higher, `block_tile_memory` can be omitted [[CUDA_C_Programming_Guide:L12204-L12314]].

```cpp
__global__ void kernel(...) {
    // reserve shared memory for thread_block_tile usage,
    // specify that block size will be at most 256 threads.
    __shared__ block_tile_memory<256> shared;
    thread_block thb = this_thread_block(shared);

    // Create tiles with 128 threads.
    auto tile = tiled_partition<128>(thb);

    // ...
}
```
