# Multi-Stage Asynchronous Data Copies using cuda::pipeline

The `cuda::pipeline` feature provides a mechanism for managing a sequence of `memcpy_async` batches, enabling CUDA kernels to overlap memory transfers with computation [CUDA_C_Programming_Guide:L9846-L9934]. This approach addresses the limitation of previous methods using `cooperative_groups::wait` and `cuda::barrier`, where kernel threads immediately wait for data transfers to shared memory to complete, thereby failing to hide the latency of the `memcpy_async` operation by overlapping computation [CUDA_C_Programming_Guide:L9846-L9934].

## Two-Stage Pipeline Implementation

The following example implements a two-stage pipeline that overlaps data-transfer with computation [CUDA_C_Programming_Guide:L9846-L9934]. The process involves four main phases:

1.  **Initialization**: The pipeline shared state is initialized [CUDA_C_Programming_Guide:L9846-L9934].
2.  **Kickstart**: The pipeline is kickstarted by scheduling a `memcpy_async` for the first batch [CUDA_C_Programming_Guide:L9846-L9934].
3.  **Looping**: The kernel loops over all batches, scheduling `memcpy_async` for the next batch, blocking all threads on the completion of the `memcpy_async` for the previous batch, and overlapping the computation on the previous batch with the asynchronous copy of the memory for the next batch [CUDA_C_Programming_Guide:L9846-L9934].
4.  **Draining**: The pipeline is drained by performing the computation on the last batch [CUDA_C_Programming_Guide:L9846-L9934].

## Key Components and Workflow

### Headers and Scope
For interoperability with `cuda::pipeline`, `cuda::memcpy_async` from the `cuda/pipeline` header is used [CUDA_C_Programming_Guide:L9846-L9934]. The pipeline operates within a specific thread scope, typically `cuda::thread_scope::thread_scope_block` [CUDA_C_Programming_Guide:L9846-L9934].

### Shared Memory and State
A two-stage pipeline requires shared memory to hold two batches simultaneously [CUDA_C_Programming_Guide:L9846-L9934]. The shared storage is allocated using `cuda::pipeline_shared_state` [CUDA_C_Programming_Guide:L9846-L9934].

```cpp
__shared__ cuda::pipeline_shared_state<
    cuda::thread_scope::thread_scope_block,
    stages_count
> shared_state;
auto pipeline = cuda::make_pipeline(block, &shared_state);
```

### Producer and Consumer Operations
The pipeline manages producer (copy) and consumer (compute) stages through collective operations:

*   **Producer Acquire/Commit**: Threads collectively acquire the pipeline head stage and commit asynchronous copies [CUDA_C_Programming_Guide:L9846-L9934].
*   **Consumer Wait/Release**: Threads collectively wait for operations committed to the previous stage to complete and then release stage resources [CUDA_C_Programming_Guide:L9846-L9934].

### Code Structure
The core loop manages stage indices for compute and copy operations using modulo arithmetic to alternate between stages [CUDA_C_Programming_Guide:L9846-L9934].

```cpp
// Pipelined copy/compute:
for (size_t batch = 1; batch < batch_sz; ++batch) {
    // Stage indices for the compute and copy stages:
    size_t compute_stage_idx = (batch - 1) % 2;
    size_t copy_stage_idx = batch % 2;

    size_t global_idx = block_batch(batch);

    // Collectively acquire the pipeline head stage from all producer threads:
    pipeline.producer_acquire();

    // Submit async copies to the pipeline's head stage to be
    // computed in the next loop iteration
    cuda::memcpy_async(block, shared + shared_offset[copy_stage_idx], global_in +
    global_idx, sizeof(int) * block.size(), pipeline);
    // Collectively commit (advance) the pipeline's head stage
    pipeline.producer_commit();

    // Collectively wait for the operations committed to the
    // previous `compute` stage to complete:
    pipeline.consumer_wait();

    // Computation overlapped with the memcpy_async of the "copy" stage:
    compute(global_out + global_idx, shared + shared_offset[compute_stage_idx]);

    // Collectively release the stage resources
    pipeline.consumer_release();
}
```

After the loop, the pipeline is drained by waiting for the final batch's computation and releasing the stage [CUDA_C_Programming_Guide:L9846-L9934].

```cpp
// Compute the data fetch by the last iteration
pipeline.consumer_wait();
compute(global_out + block_batch(batch_sz-1), shared + shared_offset[(batch_sz - 1) % 2]);
pipeline.consumer_release();
```

## Prerequisites

*   The input size must fit within `batch_sz * grid_size` [CUDA_C_Programming_Guide:L9846-L9934].
*   Shared memory must be sized to accommodate `stages_count * block.size() * sizeof(int)` bytes [CUDA_C_Programming_Guide:L9846-L9934].

## Caveats

*   The research report for this topic was a deterministic fallback due to a context length error in the original source processing; therefore, the content is strictly derived from the provided source evidence [CUDA_C_Programming_Guide:L9846-L9934].

## See Also

*   `cooperative_groups::wait`
*   `cuda::barrier`
*   `cuda::memcpy_async`

## References

*   CUDA C++ Programming Guide, Section 10.28.2 [CUDA_C_Programming_Guide:L9846-L9934] | [CUDA_C_Programming_Guide:L9935-L9935]
