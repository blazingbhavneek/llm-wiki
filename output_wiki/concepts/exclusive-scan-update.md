# exclusive_scan_update

`exclusive_scan_update` is a function within the CUDA Cooperative Groups library that facilitates dynamic memory allocation patterns. It performs an exclusive prefix sum (scan) on values provided by threads in a tile, returning the offset for each thread's portion of a shared resource. Simultaneously, it atomically updates a provided atomic variable with the total sum of all inputs, ensuring correct synchronization with other tiles or blocks that may be allocating from the same shared buffer.

## Functionality

The function signature generally takes a tile, an atomic variable for the global sum, and the input value for the calling thread. Its behavior can be broken down into two main operations:

1.  **Exclusive Scan**: Computes the sum of all input values from threads in the tile that precede the calling thread. This result is returned as the offset where the current thread should write its data.
2.  **Atomic Update**: Adds the calling thread's input value to the provided atomic variable. This ensures that the atomic variable holds the cumulative sum of all inputs from the tile upon completion, which is critical for coordinating with other groups (e.g., other tiles) that are also allocating space from the same shared memory region.

## Use Case: Dynamic Buffer Allocation

A primary use case for `exclusive_scan_update` is dynamic buffer partitioning in shared memory. Since the amount of memory each thread needs may vary, a standard scan cannot be used if the total size is not known in advance or if multiple tiles need to coordinate their allocations without race conditions.

### Example Implementation

The following example demonstrates how threads in a tile calculate their individual buffer needs, use `exclusive_scan_update` to compute offsets atomically, and then fill their allocated buffer space.

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/scan.h>
namespace cg = cooperative_groups;

// Buffer partitioning is static to make the example easier to follow,
// but any arbitrary dynamic allocation scheme can be implemented by replacing this
// function.
__device__ int calculate_buffer_space_needed(cg::thread_block_tile<32>& tile) {
    return tile.thread_rank() % 2 + 1;
}

__device__ int my_thread_data(int i) {
    return i;
}

__global__ void kernel() {
    __shared__ extern int buffer[];
    __shared__ cuda::atomic<int, cuda::thread_scope_block> buffer_used;

    auto block = cg::this_thread_block();
    auto tile = cg::tiled_partition<32>(block);
    buffer_used = 0;
    block.sync();

    // each thread calculates buffer size it needs
    int buf_needed = calculate_buffer_space_needed(tile);

    // scan over the needs of each thread, result for each thread is an offset
    // of that thread's part of the buffer. buffer_used is atomically updated with
    // the sum of all thread's inputs, to correctly offset other tile's allocations
    int buf_offset =
        cg::exclusive_scan_update(tile, buffer_used, buf_needed);

    // each thread fills its own part of the buffer with thread specific data
    for (int i = 0 ; i < buf_needed ; ++i) {
        buffer[buf_offset + i] = my_thread_data(i);
    }

    block.sync();
    // buffer_used now holds total amount of memory allocated
    // buffer is {0, 0, 1, 0, 0, 1 ...};
}
```

In this example:
- `calculate_buffer_space_needed` determines how many elements each thread requires.
- `cg::exclusive_scan_update` computes the starting index (`buf_offset`) for each thread's data in the shared `buffer` and updates `buffer_used` with the total space consumed by the tile.
- After the loop, `buffer_used` contains the total amount of memory allocated by the tile, allowing other tiles to safely allocate subsequent space.

## References

- [CUDA_C_Programming_Guide:L13107-L13152] Provides the full context and code example for dynamic buffer space allocation using `exclusive_scan_update`.
