
CUDA 11 introduces Asynchronous Data operations with memcpy\_async API to allow device code to explicitly manage the asynchronous copying of data. The memcpy\_async feature enables CUDA kernels to overlap computation with data movement.

## 10.27.1. memcpy\_async API

The memcpy\_async APIs are provided in the cuda∕barrier, cuda∕pipeline, and cooperative\_groups∕memcpy\_async.h header files.

The cuda::memcpy\_async APIs work with cuda::barrier and cuda::pipeline synchronization primitives, while the cooperative\_groups::memcpy\_async synchronizes using cooperative\_groups::wait.

These APIs have very similar semantics: copy objects from src to dst as-if performed by another thread which, on completion of the copy, can be synchronized through cuda::pipeline, cuda::barrier, or cooperative\_groups::wait.

The complete API documentation of the cuda::memcpy\_async overloads for cuda::barrier and cuda::pipeline is provided in the libcudacxx API documentation along with some examples.

The API documentation of cooperative\_groups::memcpy\_async is provided in the Cooperative Groups section.

The memcpy\_async APIs that use cuda::barrier and cuda::pipeline require compute capability 7.0 or higher. On devices with compute capability 8.0 or higher, memcpy\_async operations from global to shared memory can benefit from hardware acceleration.

## 10.27.2. Copy and Compute Pattern - Staging Data Through Shared Memory

CUDA applications often employ a copy and compute pattern that:

▶ fetches data from global memory,

▶ stores data to shared memory, and

▶ performs computations on shared memory data, and potentially writes results back to global memory.

The following sections illustrate how this pattern can be expressed without and with the memcpy\_async feature:

▶ Without memcpy\_async introduces an example that does not overlap computation with data movement and uses an intermediate register to copy data.

With memcpy\_async improves the previous example by introducing the memcpy\_async and the cuda::memcpy\_async APIs to directly copy data from global to shared memory without using intermediate registers.

Asynchronous Data Copies using cuda::barrier shows memcpy with cooperative groups and barrier.

Single-Stage Asynchronous Data Copies using cuda::pipeline shows memcpy with single stage pipeline.

▶ Multi-Stage Asynchronous Data Copies using cuda::pipeline shows memcpy with multi stage pipeline.

## 10.27.3. Without memcpy\_async

Without memcpy\_async, the copy phase of the copy and compute pattern is expressed as shared[local\_idx] = global[global\_idx]. This global to shared memory copy is expanded to a read from global memory into a register, followed by a write to shared memory from the register.

When this pattern occurs within an iterative algorithm, each thread block needs to synchronize after the shared[local\_idx] = global[global\_idx] assignment, to ensure all writes to shared memory have completed before the compute phase can begin. The thread block also needs to synchronize again after the compute phase, to prevent overwriting shared memory before all threads have completed their computations. This pattern is illustrated in the following code snippet.

```cpp
#include <cooperative_groups.h>
__device__ void compute(int* global_out, int const* shared_in) {
    // Computes using all values of current batch from shared memory.
    // Stores this thread's result back to global memory.
}

__global__ void without_memcpy_async(int* global_out, int const* global_in, size_t size, size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    assert(size == batch_sz * grid.size()); // Exposition: input size fits batch_sz * grid_size

    extern __shared__ int shared[]; // block.size() * sizeof(int) bytes

    size_t local_idx = block.thread_rank();

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        // Compute the index of the current batch for this block in global memory:
        size_t block_batch_idx = block.group_index().x * block.size() + grid.size() * batch;
        size_t global_idx = block_batch_idx + threadIdx.x;
        shared[local_idx] = global_in[global_idx];

        block.sync(); // Wait for all copies to complete

        compute(global_out + block_batch_idx, shared); // Compute and write result to global memory

        block.sync(); // Wait for compute using shared memory to finish
    }
}
```

## 10.27.4. With memcpy\_async

With memcpy\_async, the assignment of shared memory from global memory

```javascript
shared[local_idx] = global_in[global_idx];
```

is replaced with an asynchronous copy operation from cooperative groups

```cpp
cooperative_groups::memcpy_async(group, shared, global_in + batch_idx, sizeof(int) * block.size());
```

The cooperative\_groups::memcpy\_async API copies sizeof(int) \* block.size() bytes from global memory starting at global\_in + batch\_idx to the shared data. This operation happens as-if performed by another thread, which synchronizes with the current thread’s call to cooperative\_groups::wait after the copy has completed. Until the copy operation completes, modifying the global data or reading or writing the shared data introduces a data race.

On devices with compute capability 8.0 or higher, memcpy\_async transfers from global to shared memory can benefit from hardware acceleration, which avoids transferring the data through an intermediate register.
