# Unified Pipeline Loop Pattern

The Unified Pipeline Loop Pattern is a coding structure in CUDA that demonstrates a more concise way to implement multi-stage pipeline execution by merging the prolog and epilog phases of the loop with the loop body itself [CUDA_C_Programming_Guide:L9936-L10003]. This pattern utilizes a nested loop structure where the inner loop handles filling the pipeline with asynchronous copy operations, and the outer loop manages computation and the release of completed stages [CUDA_C_Programming_Guide:L9936-L10003].

## Pipeline Mechanics

A pipeline object functions as a double-ended queue with a head and a tail, processing work in a first-in first-out (FIFO) order [CUDA_C_Programming_Guide:L9936-L10003]. Producer threads commit work to the pipeline’s head, while consumer threads pull work from the pipeline’s tail [CUDA_C_Programming_Guide:L9936-L10003]. In the context of this pattern, all threads typically act as both producer and consumer threads [CUDA_C_Programming_Guide:L9936-L10003].

### Producer Operations
Committing work to a pipeline stage involves a collective sequence among producer threads:
1.  Acquiring the pipeline head using `pipeline.producer_acquire()` [CUDA_C_Programming_Guide:L9936-L10003].
2.  Submitting `memcpy_async` operations to the pipeline head [CUDA_C_Programming_Guide:L9936-L10003].
3.  Collectively committing (advancing) the pipeline head using `pipeline.producer_commit()` [CUDA_C_Programming_Guide:L9936-L10003].

### Consumer Operations
Using a previously committed stage involves:
1.  Collectively waiting for the stage to complete, typically using `pipeline.consumer_wait()` on the tail (oldest) stage [CUDA_C_Programming_Guide:L9936-L10003].
2.  Collectively releasing the stage using `pipeline.consumer_release()` [CUDA_C_Programming_Guide:L9936-L10003].

The `cuda::pipeline_shared_state<scope, count>` encapsulates the finite resources allowing a pipeline to process up to `count` concurrent stages. If all resources are in use, `pipeline.producer_acquire()` blocks producer threads until consumer threads release the resources of the next pipeline stage [CUDA_C_Programming_Guide:L9936-L10003].

## Unified Loop Implementation

The unified pattern simplifies the standard pipeline structure by integrating the initialization (prolog) and cleanup (epilog) logic directly into the main execution loop [CUDA_C_Programming_Guide:L9936-L10003]. This is achieved through a nested loop structure:

*   **Outer Loop**: Iterates over the computation of batches. It handles the waiting for previous stages to complete (`consumer_wait`), executing the computation, and releasing the stage (`consumer_release`) [CUDA_C_Programming_Guide:L9936-L10003].
*   **Inner Loop**: Iterates over memory transfers, ensuring the pipeline is always full. It acquires the producer stage, performs asynchronous memory copies (`memcpy_async`), and commits the stage [CUDA_C_Programming_Guide:L9936-L10003].

### Example Code

The following example demonstrates the unified pipeline loop pattern using cooperative groups and asynchronous memory copies:

```cpp
template <size_t stages_count = 2 /* Pipeline with stages_count stages */>
__global__ void with_staging_unified(int* global_out, int const* global_in, size_t
size, size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    assert(size == batch_sz * grid.size()); // Assume input size fits batch_sz * grid_
size

    extern __shared__ int shared[]; // stages_count * block.size() * sizeof(int) bytes
    size_t shared_offset[stages_count];
    for (int s = 0; s < stages_count; ++s) shared_offset[s] = s * block.size();

    __shared__ cuda::pipeline_shared_state<
        cuda::thread_scope::thread_scope_block,
        stages_count
    > shared_state;
    auto pipeline = cuda::make_pipeline(block, &shared_state);

    auto block_batch = [&](size_t batch) -> int {
        return block.group_index().x * block.size() + grid.size() * batch;
    };

    // compute_batch: next batch to process
    // fetch_batch: next batch to fetch from global memory
    for (size_t compute_batch = 0, fetch_batch = 0; compute_batch < batch_sz;
++compute_batch) {
        // The outer loop iterates over the computation of the batches
        for (; fetch_batch < batch_sz && fetch_batch < (compute_batch + stages_count);
++fetch_batch) {
            // This inner loop iterates over the memory transfers, making sure that the
pipeline is always full
            pipeline.producer_acquire();
            size_t shared_idx = fetch_batch % stages_count;
            size_t batch_idx = fetch_batch;
            size_t block_batch_idx = block_batch(batch_idx);
            cuda::memcpy_async(block, shared + shared_offset[shared_idx], global_in +
block_batch_idx, sizeof(int) * block.size(), pipeline);
            pipeline.producer_commit();
        }
        pipeline.consumer_wait();
        int shared_idx = compute_batch % stages_count;
        int batch_idx = compute_batch;
        compute(global_out + block_batch(batch_idx), shared + shared_offset[shared_
idx]);
        pipeline.consumer_release();
    }
}
```

In this implementation, threads first commit `memcpy_async` operations to fetch the next batch while waiting on the previous batch of `memcpy_async` operations to complete [CUDA_C_Programming_Guide:L9936-L10003]. The nested loop structure ensures that the pipeline remains full during the computation phase, maximizing overlap between memory transfers and processing [CUDA_C_Programming_Guide:L9936-L10003].
