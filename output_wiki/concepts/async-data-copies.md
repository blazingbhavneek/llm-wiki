# Asynchronous Data Copies (memcpy_async)

Asynchronous Data Copies, exposed via the `memcpy_async` API, were introduced in CUDA 11 to allow device code to explicitly manage the asynchronous copying of data [CUDA_C_Programming_Guide:L9538-L9554]. This feature enables CUDA kernels to overlap computation with data movement, addressing performance bottlenecks in the common "copy and compute" pattern [CUDA_C_Programming_Guide:L9538-L9554][CUDA_C_Programming_Guide:L9555-L9576].

## Overview and Headers

The `memcpy_async` APIs are provided in three header files:
* `cuda/barrier`
* `cuda/pipeline`
* `cooperative_groups/memcpy_async.h` [CUDA_C_Programming_Guide:L9538-L9554]

The `cuda::memcpy_async` APIs work with `cuda::barrier` and `cuda::pipeline` synchronization primitives, while `cooperative_groups::memcpy_async` synchronizes using `cooperative_groups::wait` [CUDA_C_Programming_Guide:L9538-L9554]. These APIs share similar semantics: they copy objects from a source (`src`) to a destination (`dst`) as if performed by another thread, which can be synchronized upon completion [CUDA_C_Programming_Guide:L9538-L9554].

### Hardware Requirements

* **Compute Capability 7.0+**: Required for `memcpy_async` APIs using `cuda::barrier` and `cuda::pipeline` [CUDA_C_Programming_Guide:L9538-L9554].
* **Compute Capability 8.0+**: On devices with compute capability 8.0 or higher, `memcpy_async` operations from global to shared memory benefit from hardware acceleration [CUDA_C_Programming_Guide:L9538-L9554][CUDA_C_Programming_Guide:L9613-L9663]. This acceleration avoids transferring data through an intermediate register [CUDA_C_Programming_Guide:L9613-L9663].

## The Copy and Compute Pattern

CUDA applications often employ a "copy and compute" pattern that involves:
1. Fetching data from global memory.
2. Storing data to shared memory.
3. Performing computations on the shared memory data.
4. Potentially writing results back to global memory [CUDA_C_Programming_Guide:L9555-L9576].

### Without memcpy_async

Without `memcpy_async`, the copy phase is expressed as a direct assignment, e.g., `shared[local_idx] = global[global_idx]` [CUDA_C_Programming_Guide:L9577-L9612]. This operation is expanded by the compiler to a read from global memory into a register, followed by a write to shared memory from that register [CUDA_C_Programming_Guide:L9577-L9612].

In iterative algorithms, this approach requires explicit synchronization:
* A block-wide synchronization is needed after the copy assignment to ensure all writes to shared memory have completed before the compute phase begins [CUDA_C_Programming_Guide:L9577-L9612].
* Another synchronization is required after the compute phase to prevent overwriting shared memory before all threads have finished their computations [CUDA_C_Programming_Guide:L9577-L9612].

```cpp
// Simplified example of the traditional pattern
for (size_t batch = 0; batch < batch_sz; ++batch) {
    shared[local_idx] = global_in[global_idx];
    block.sync(); // Wait for all copies to complete
    compute(global_out + block_batch_idx, shared);
    block.sync(); // Wait for compute to finish
}
```

### With memcpy_async

Using `memcpy_async`, the assignment is replaced with an asynchronous copy operation [CUDA_C_Programming_Guide:L9613-L9663]. This allows the copy to proceed asynchronously, potentially overlapping with other operations, while ensuring data consistency through specific synchronization primitives [CUDA_C_Programming_Guide:L9613-L9663].

#### Cooperative Groups Example

The `cooperative_groups::memcpy_async` API copies data from global to shared memory. This operation happens as-if performed by another thread, which synchronizes with the current thread's call to `cooperative_groups::wait` after the copy completes [CUDA_C_Programming_Guide:L9613-L9663]. Modifying global data or reading/writing shared data before the copy completes introduces a data race [CUDA_C_Programming_Guide:L9613-L9663].

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

__global__ void with_memcpy_async(int* global_out, int const* global_in, size_t size,
                                  size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    extern __shared__ int shared[];

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        size_t block_batch_idx = block.group_index().x * block.size() + grid.size() * batch;
        // Whole thread-group cooperatively copies whole batch to shared memory
        cooperative_groups::memcpy_async(block, shared, global_in + block_batch_idx,
                                         sizeof(int) * block.size());

        cooperative_groups::wait(block); // Joins all threads, waits for all copies to complete
        compute(global_out + block_batch_idx, shared);
        block.sync();
    }
}
```

#### cuda::barrier Example

The `cuda::memcpy_async` overload for `cuda::barrier` enables synchronizing asynchronous data transfers using a C++20-style barrier [CUDA_C_Programming_Guide:L9664-L9699]. This overload executes the copy operation as if performed by another thread bound to the barrier [CUDA_C_Programming_Guide:L9664-L9699]. It increments the expected count of the current phase on creation and decrements it on completion, ensuring the barrier phase only advances when all participating threads have arrived and all `memcpy_async` operations bound to that phase have completed [CUDA_C_Programming_Guide:L9664-L9699].

```cpp
#include <cooperative_groups.h>
#include <cuda/barrier>

__global__ void with_barrier(int* global_out, int const* global_in, size_t size, size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    extern __shared__ int shared[];

    // Create a synchronization object (C++20 barrier)
    __shared__ cuda::barrier<cuda::thread_scope::thread_scope_block> barrier;
    if (block.thread_rank() == 0) {
        init(&barrier, block.size());
    }
    block.sync();

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        size_t block_batch_idx = block.group_index().x * block.size() + grid.size() * batch;
        cuda::memcpy_async(block, shared, global_in + block_batch_idx,
                           sizeof(int) * block.size(), barrier);

        barrier.arrive_and_wait(); // Waits for all copies to complete
        compute(global_out + block_batch_idx, shared);
        block.sync();
    }
}
```

## See Also

* Single-Stage Asynchronous Data Copies using `cuda::pipeline`
* Multi-Stage Asynchronous Data Copies using `cuda::pipeline`
