# Asynchronous Barrier (cuda::barrier)

The NVIDIA C++ standard library introduces a GPU implementation of `std::barrier` via the `cuda::barrier` class. This implementation allows users to specify the scope of barrier objects and provides extensions for advanced synchronization patterns such as temporal splitting, spatial partitioning, and completion functions. Devices with compute capability 8.0 or higher provide hardware acceleration for barrier operations and integration with the `memcpy_async` feature. On devices with compute capability below 8.0 but starting from 7.0, these barriers are available without hardware acceleration. The older `nvcuda::experimental::awbarrier` is deprecated in favor of `cuda::barrier` [CUDA_C_Programming_Guide:L9152-L9157].

## Simple Synchronization Pattern

Without the arrive/wait barrier, synchronization is typically achieved using `__syncthreads()` to synchronize all threads in a block or `group.sync()` when using Cooperative Groups. This traditional pattern involves three stages: code before the synchronization point, the synchronization point itself, and code after the synchronization point. Threads are blocked at the synchronization point until all threads have reached it. Memory updates that happened before the synchronization point are guaranteed to be visible to all threads in the block after the synchronization point, equivalent to `atomic_thread_fence(memory_order_seq_cst, thread_scope_block)` [CUDA_C_Programming_Guide:L9158-L9185].

## Temporal Splitting and Five Stages of Synchronization

The `cuda::barrier` enables a temporally-split synchronization pattern where the single synchronization point is split into an arrive point (`bar.arrive()`) and a wait point (`bar.wait()`). A thread begins participating in a `cuda::barrier` with its first call to `bar.arrive()`. The `arrive()` call does not block a thread; it can proceed with other work that does not depend upon memory updates that happen before other participating threads' calls to `bar.arrive()`. When a thread calls `bar.wait()`, it is blocked until participating threads have completed `bar.arrive()` the expected number of times [CUDA_C_Programming_Guide:L9186-L9236].

This pattern consists of five stages which may be iteratively repeated:
1. Code before `arrive` performs memory updates that will be read after the `wait`.
2. `Arrive` point with implicit memory fence (equivalent to `atomic_thread_fence(memory_order_seq_cst, thread_scope_block)`).
3. Code between `arrive` and `wait`.
4. `Wait` point.
5. Code after the `wait`, with visibility of updates that were performed before the `arrive` [CUDA_C_Programming_Guide:L9186-L9236].

## Bootstrap Initialization, Expected Arrival Count, and Participation

Initialization must happen before any thread begins participating in a `cuda::barrier`. The barrier must be initialized using `init()` with an expected arrival count, which specifies the number of times `bar.arrive()` will be called by participating threads before a participating thread is unblocked from its call to `bar.wait()` [CUDA_C_Programming_Guide:L9237-L9268].

This poses a bootstrapping challenge: threads must synchronize before participating in the `cuda::barrier`, but threads are creating a `cuda::barrier` in order to synchronize. In practice, threads that will participate are often part of a cooperative group and use `block.sync()` to bootstrap initialization. For example, a single thread initializes the barrier with the block size, followed by a `block.sync()` to ensure all threads see the initialized barrier [CUDA_C_Programming_Guide:L9237-L9268].

`cuda::barrier` is flexible in specifying how threads participate and which threads participate. In contrast, `this_thread_block.sync()` from cooperative groups or `__syncthreads()` is applicable to whole-thread-block synchronization, and `__syncwarp(mask)` is for a specified subset of a warp. If the intention is to synchronize a full thread block or a full warp, it is recommended to use `__syncthreads()` and `__syncwarp(mask)` respectively for performance reasons [CUDA_C_Programming_Guide:L9237-L9268].

## A Barrier’s Phase: Arrival, Countdown, Completion, and Reset

A `cuda::barrier` counts down from the expected arrival count to zero as participating threads call `bar.arrive()`. When the countdown reaches zero, the barrier is complete for the current phase. When the last call to `bar.arrive()` causes the countdown to reach zero, the countdown is automatically and atomically reset to the expected arrival count, moving the barrier to the next phase [CUDA_C_Programming_Guide:L9269-L9284].

A token object of class `cuda::barrier::arrival_token`, returned from `token=bar.arrive()`, is associated with the current phase. A call to `bar.wait(std::move(token))` blocks the calling thread while the barrier is in the current phase. If the phase is advanced before the call to `bar.wait()`, the thread does not block; if the phase is advanced while the thread is blocked, the thread is unblocked [CUDA_C_Programming_Guide:L9269-L9284].

Usage rules include:
1. A thread’s calls to `token=bar.arrive()` and `bar.wait(std::move(token))` must be sequenced such that `arrive()` occurs during the current phase, and `wait()` occurs during the same or next phase.
2. A thread’s call to `bar.arrive()` must occur when the barrier’s counter is non-zero. After initialization, if a thread’s call causes the countdown to reach zero, a call to `bar.wait()` must happen before the barrier can be reused for a subsequent call to `bar.arrive()` [CUDA_C_Programming_Guide:L9269-L9284].
3. `bar.wait()` must only be called using a token object of the current phase or the immediately preceding phase. For any other values, the behavior is undefined [CUDA_C_Programming_Guide:L9269-L9284].

## Spatial Partitioning (Warp Specialization)

A thread block can be spatially partitioned such that warps are specialized to perform independent computations. This is used in producer/consumer patterns where one subset of threads produces data that is concurrently consumed by another disjoint subset. This pattern requires two one-sided synchronizations to manage a data buffer between the producer and consumer [CUDA_C_Programming_Guide:L9285-L9372].

For full producer/consumer concurrency, this pattern typically uses double buffering, where each buffer requires two `cuda::barriers` (one for "ready to be filled" and one for "filled"). Producer threads wait for consumer threads to signal that the buffer is ready to be filled, while consumer threads wait for producer threads to signal that the buffer is filled. Producer threads do not wait for the "filled" signal, and consumer threads do not wait for the "ready" signal [CUDA_C_Programming_Guide:L9285-L9372].

The `arrive_and_wait()` method combines `bar.wait(bar.arrive())` for simplicity. In a typical implementation, the first warp might be specialized as the producer and the remaining warps as the consumer. All producer and consumer threads participate in each of the four barriers, so the expected arrival counts are equal to the block size [CUDA_C_Programming_Guide:L9285-L9372].

## Early Exit (Dropping out of Participation)

When a thread participating in a sequence of synchronizations must exit early, it must explicitly drop out of participation before exiting. The `bar.arrive_and_drop()` operation arrives on the barrier to fulfill the thread's obligation for the current phase and then decrements the expected arrival count for the next phase, so the thread is no longer expected to arrive [CUDA_C_Programming_Guide:L9373-L9407]. The remaining participating threads can proceed normally with subsequent `cuda::barrier` arrive and wait operations [CUDA_C_Programming_Guide:L9373-L9407].

## Completion Function

The `CompletionFunction` of `cuda::barrier<Scope, CompletionFunction>` is executed once per phase, after the last thread arrives and before any thread is unblocked from the wait. Memory operations performed by the threads that arrived at the barrier during the phase are visible to the thread executing the `CompletionFunction`, and all memory operations performed within the `CompletionFunction` are visible to all threads waiting at the barrier once they are unblocked [CUDA_C_Programming_Guide:L9408-L9466].

Because the completion function may not be default-constructible (e.g., if it captures variables), the barrier may not be default-constructible. In such cases, placement new or `std::aligned_storage` can be used to initialize the barrier in shared memory. For example, in a parallel sum reduction, the completion function can perform a reduction on shared memory data after all threads have arrived, ensuring shared memory is safe to reuse in the next iteration [CUDA_C_Programming_Guide:L9408-L9466].
