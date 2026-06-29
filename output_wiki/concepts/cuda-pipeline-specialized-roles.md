# Specialized Producer/Consumer Roles in cuda::pipeline

The `cuda::pipeline` primitive provides flexibility in how threads within a block participate in asynchronous memory operations. While previous examples may have used all threads for both roles, the pipeline supports assigning specific subsets of threads as producers, consumers, or both [CUDA_C_Programming_Guide:L10009-L10134].

## Thread Role Assignment

Threads can be distinguished by their rank within the thread block to assign specific roles using `cuda::pipeline_role` [CUDA_C_Programming_Guide:L10009-L10134]. For example, threads with an "even" thread rank can act as producers, while threads with an "odd" rank act as consumers [CUDA_C_Programming_Guide:L10009-L10134].

This is achieved by passing the role to `cuda::make_pipeline` along with the block cooperative group and shared state [CUDA_C_Programming_Guide:L10009-L10134]:

```cpp
// Determine role based on thread rank
const cuda::pipeline_role thread_role
    = block.thread_rank() % 2 == 0? cuda::pipeline_role::producer : cuda::pipeline_role::consumer;

// Initialize pipeline with specific role
cuda::pipeline pipeline = cuda::make_pipeline(block, &shared_state, thread_role);
```

## Producer and Consumer Operations

Once roles are assigned, threads execute specific pipeline methods corresponding to their role [CUDA_C_Programming_Guide:L10009-L10134]:

*   **Producers**: Use `pipeline.producer_acquire()` before initiating asynchronous memory copies (e.g., `cuda::memcpy_async`) and `pipeline.producer_commit()` after [CUDA_C_Programming_Guide:L10009-L10134].
*   **Consumers**: Use `pipeline.consumer_wait()` before reading data and `pipeline.consumer_release()` after computation [CUDA_C_Programming_Guide:L10009-L10134].

Example producer logic:
```cpp
if (thread_role == cuda::pipeline_role::producer) {
    pipeline.producer_acquire();
    // ... perform memcpy_async ...
    pipeline.producer_commit();
}
```

Example consumer logic:
```cpp
if (thread_role == cuda::pipeline_role::consumer) {
    pipeline.consumer_wait();
    // ... perform compute ...
    pipeline.consumer_release();
}
```

## Optimization: Thread Scope Pipeline

The general `pipeline<thread_scope_block>` implementation stores and uses a set of barriers in shared memory for synchronization, which incurs overhead if not all threads participate or if roles are specialized [CUDA_C_Programming_Guide:L10009-L10134].

For the specific case where all threads in the block participate in the pipeline, a more efficient approach uses `pipeline<thread_scope_thread>` combined with `__syncthreads()` [CUDA_C_Programming_Guide:L10009-L10134]. This avoids the overhead of the shared memory barrier set used by the block-scoped pipeline [CUDA_C_Programming_Guide:L10009-L10134].

In this optimized pattern:
1.  Each thread manages its own asynchronous copy using `cuda::make_pipeline()` without a shared state object [CUDA_C_Programming_Guide:L10009-L10134].
2.  `pipeline.producer_acquire()` and `pipeline.producer_commit()` are called for each thread's individual copy [CUDA_C_Programming_Guide:L10009-L10134].
3.  `__syncthreads()` (or `block.sync()`) is used to ensure all asynchronous copies for the current stage have completed before proceeding to computation [CUDA_C_Programming_Guide:L10009-L10134].
4.  `pipeline.consumer_wait()` and `pipeline.consumer_release()` manage the logical pipeline stages [CUDA_C_Programming_Guide:L10009-L10134].

If the compute operation only reads shared memory written to by other threads in the same warp, `__syncwarp()` may suffice instead of `__syncthreads()` [CUDA_C_Programming_Guide:L10009-L10134].

## Related Concepts

*   [Pipeline Interface](concept/cuda-pipeline-interface)

## References

*   CUDA C++ Programming Guide, Section 10.28.3. Pipeline Interface [CUDA_C_Programming_Guide:L10135-L10135]
*   CUDA C++ Programming Guide, Specialized Staging Example [CUDA_C_Programming_Guide:L10009-L10134]
