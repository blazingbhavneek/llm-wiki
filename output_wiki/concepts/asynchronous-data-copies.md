# Asynchronous Data Copies (memcpy_async)

CUDA 11+ API for overlapping computation with data movement. Enables asynchronous global-to-shared memory copies via cuda::barrier, cuda::pipeline, or cooperative_groups::wait. Includes performance guidance on alignment, trivially copyable types, and warp entanglement effects on commit/wait/arrive operations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L9537-L9777

Citation: [CUDA_C_Programming_Guide:L9537-L9777]

````text
## 10.27. Asynchronous Data Copies

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

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

__device__ void compute(int* global_out, int const* shared_in);

__global__ void with_memcpy_async(int* global_out, int const* global_in, size_t size,
size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    assert(size == batch_sz * grid.size()); // Exposition: input size fits batch_sz *
grid_size

    extern __shared__ int shared[]; // block.size() * sizeof(int) bytes

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        size_t block_batch_idx = block.group_index().x * block.size() + grid.size() *
        batch;
        // Whole thread-group cooperatively copies whole batch to shared memory:
        cooperative_groups::memcpy_async(block, shared, global_in + block_batch_idx,
sizeof(int) * block.size());

        cooperative_groups::wait(block); // Joins all threads, waits for all copies to
        complete

        compute(global_out + block_batch_idx, shared);

        block.sync();
    }
}
```

## 10.27.5. Asynchronous Data Copies using cuda::barrier

The cuda::memcpy\_async overload for cuda::barrier enables synchronizing asynchronous data transfers using a barrier. This overloads executes the copy operation as-if performed by another thread bound to the barrier by: incrementing the expected count of the current phase on creation, and decrementing it on completion of the copy operation, such that the phase of the barrier will only advance when all threads participating in the barrier have arrived, and all memcpy\_async bound to the current phase of the barrier have completed. The following example uses a block-wide barrier, where all block threads participate, and swaps the wait operation with a barrier arrive\_and\_wait, while providing the same functionality as the previous example:

```cpp
#include <cooperative_groups.h>
#include <cuda/barrier>
__device__ void compute(int* global_out, int const* shared_in);

__global__ void with_barrier(int* global_out, int const* global_in, size_t size, size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    assert(size == batch_sz * grid.size()); // Assume input size fits batch_sz * grid_size

    extern __shared__ int shared[]; // block.size() * sizeof(int) bytes

    // Create a synchronization object (C++20 barrier)
    __shared__ cuda::barrier<cuda::thread_scope::thread_scope_block> barrier;
    if (block.thread_rank() == 0) {
        init(&barrier, block.size()); // Friend function initializes barrier
    }
    block.sync();

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        size_t block_batch_idx = block.group_index().x * block.size() + grid.size() * batch;
        cuda::memcpy_async(block, shared, global_in + block_batch_idx, sizeof(int) * block.size(), barrier);

        barrier.arrive_and_wait(); // Waits for all copies to complete

        compute(global_out + block_batch_idx, shared);

        block.sync();
    }
}
```

## 10.27.6. Performance Guidance for memcpy\_async

For compute capability 8.x, the pipeline mechanism is shared among CUDA threads in the same CUDA warp. This sharing causes batches of memcpy\_async to be entangled within a warp, which can impact performance under certain circumstances.

This section highlights the warp-entanglement efect on commit, wait, and arrive operations. Please refer to Pipeline Interface and the Pipeline Primitives Interface for an overview of the individual operations.

## 10.27.6.1 Alignment

On devices with compute capability 8.0, the cp.async family of instructions allows copying data from global to shared memory asynchronously. These instructions support copying 4, 8, and 16 bytes at a time. If the size provided to memcpy\_async is a multiple of 4, 8, or 16, and both pointers passed to memcpy\_async are aligned to a 4, 8, or 16 alignment boundary, then memcpy\_async can be implemented using exclusively asynchronous memory operations.

Additionally for achieving best performance when using memcpy\_async API, an alignment of 128 Bytes for both shared memory and global memory is required.

For pointers to values of types with an alignment requirement of 1 or 2, it is often not possible to prove that the pointers are always aligned to a higher alignment boundary. Determining whether the cp. async instructions can or cannot be used must be delayed until run-time. Performing such a runtime alignment check increases code-size and adds runtime overhead.

The cuda::aligned\_size\_t<size\_t Align>(size\_t size)Shape can be used to supply a proof that both pointers passed to memcpy\_async are aligned to an Align alignment boundary and that size is a multiple of Align, by passing it as an argument where the memcpy\_async APIs expect a Shape:

cuda::memcpy\_async(group, dst, src, cuda::aligned\_size\_t<16>(N \* block.size()), ,<sub>→</sub>pipeline);

If the proof is incorrect, the behavior is undefined.

## 10.27.6.2 Trivially copyable

On devices with compute capability 8.0, the cp.async family of instructions allows copying data from global to shared memory asynchronously. If the pointer types passed to memcpy\_async do not point to TriviallyCopyable types, the copy constructor of each output element needs to be invoked, and these instructions cannot be used to accelerate memcpy\_async.

## 10.27.6.3 Warp Entanglement - Commit

The sequence of memcpy\_async batches is shared across the warp. The commit operation is coalesced such that the sequence is incremented once for all converged threads that invoke the commit operation. If the warp is fully converged, the sequence is incremented by one; if the warp is fully diverged, the sequence is incremented by 32.

Let PB be the warp-shared pipeline’s actual sequence of batches.

PB = {BP0, BP1, BP2, …, BPL}

▶ Let TB be a thread’s perceived sequence of batches, as if the sequence were only incremented by this thread’s invocation of the commit operation.

TB = {BT0, BT1, BT2, …, BTL}

The pipeline::producer\_commit() return value is from the thread’s perceived batch sequence.

▶ An index in a thread’s perceived sequence always aligns to an equal or larger index in the actual warp-shared sequence. The sequences are equal only when all commit operations are invoked from converged threads.

BTn   BPm where n <= m

For example, when a warp is fully diverged:

The warp-shared pipeline’s actual sequence would be: PB = {0, 1, 2, 3, ..., 31} (PL=31).

▶ The perceived sequence for each thread of this warp would be:

▶ Thread 0: TB = {0} (TL=0)

▶ Thread 1: TB = {0} (TL=0)

▶

Thread 31: TB = {0} (TL=0)

## 10.27.6.4 Warp Entanglement - Wait

A CUDA thread invokes either pipeline\_consumer\_wait\_prior<N>() or pipeline::consumer\_wait() to wait for batches in the perceived sequence TB to complete. Note that pipeline::consumer\_wait() is equivalent to pipeline\_consumer\_wait\_prior<N>(), where N = PL.

The pipeline\_consumer\_wait\_prior<N>() function waits for batches in the actual sequence at least up to and including PL-N. Since TL <= PL, waiting for batch up to and including PL-N includes waiting for batch TL-N. Thus, when TL < PL, the thread will unintentionally wait for additional, more recent batches.

In the extreme fully-diverged warp example above, each thread could wait for all 32 batches.

## 10.27.6.5 Warp Entanglement - Arrive-On

Warp-divergence afects the number of times an arrive\_on(bar) operation updates the barrier. If the invoking warp is fully converged, then the barrier is updated once. If the invoking warp is fully diverged, then 32 individual updates are applied to the barrier.

## 10.27.6.6 Keep Commit and Arrive-On Operations Converged

It is recommended that commit and arrive-on invocations are by converged threads:

▶ to not over-wait, by keeping threads’ perceived sequence of batches aligned with the actual sequence, and

to minimize updates to the barrier object.

When code preceding these operations diverges threads, then the warp should be re-converged, via \_\_syncwarp before invoking commit or arrive-on operations.
````
