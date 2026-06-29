# Single-Stage Asynchronous Data Copies using cuda::pipeline

The `cuda::pipeline` API provides a mechanism to schedule asynchronous data transfers, such as `memcpy_async`, using a single stage. This approach allows computation to overlap with memory copies, improving performance by hiding latency. This method builds upon previous examples using `cooperative_groups` and `cuda::barrier` for asynchronous transfers [CUDA_C_Programming_Guide:L9786-L9789].

## Implementation Details

The single-stage pipeline is implemented within a CUDA kernel where threads cooperate to manage shared memory and pipeline stages. The following steps outline the typical workflow:

### 1. Initialization

The pipeline requires shared memory to store its state. A `cuda::pipeline_shared_state` is declared in shared memory, configured for a specific thread scope (e.g., `thread_scope_block`) and a fixed number of stages (in this case, one) [CUDA_C_Programming_Guide:L9810-L9816].

```cpp
constexpr size_t stages_count = 1; // Pipeline with one stage
extern __shared__ int shared[]; // block.size() * sizeof(int) bytes

__shared__ cuda::pipeline_shared_state<
    cuda::thread_scope::thread_scope_block,
    stages_count
> shared_state;
auto pipeline = cuda::make_pipeline(block, &shared_state);
```

### 2. The Processing Loop

The kernel iterates over batches of data. For each batch, the following sequence occurs:

1.  **Acquire Stage**: Producer threads collectively acquire the head stage of the pipeline [CUDA_C_Programming_Guide:L9822-L9823].
2.  **Submit Copy**: An asynchronous copy (`cuda::memcpy_async`) is submitted to the pipeline's head stage. This initiates the transfer from global memory to shared memory [CUDA_C_Programming_Guide:L9825-L9826].
3.  **Commit Stage**: The head stage is committed (advanced) [CUDA_C_Programming_Guide:L9828-L9829].
4.  **Wait for Previous Stage**: Consumer threads wait for the operations committed to the previous stage (the computation stage) to complete. This ensures the data is ready for processing [CUDA_C_Programming_Guide:L9831-L9833].
5.  **Compute**: Computation is performed on the data now residing in shared memory. This computation overlaps with the `memcpy_async` of the next iteration's "copy" stage [CUDA_C_Programming_Guide:L9835-L9836].
6.  **Release Stage**: The stage resources are collectively released, making them available for the next iteration [CUDA_C_Programming_Guide:L9838-L9839].

### Example Code

The following snippet illustrates the complete kernel structure for a single-stage pipeline:

```cpp
#include <cooperative_groups/memcpy_async.h>
#include <cuda/pipeline>

__device__ void compute(int* global_out, int const* shared_in);

__global__ void with_single_stage(int* global_out, int const* global_in, size_t size,
                                  size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();
    
    // Assume input size fits batch_sz * grid_size
    assert(size == batch_sz * grid.size()); 

    constexpr size_t stages_count = 1; // Pipeline with one stage
    extern __shared__ int shared[]; // block.size() * sizeof(int) bytes

    // Allocate shared storage for a single stage cuda::pipeline
    __shared__ cuda::pipeline_shared_state<
        cuda::thread_scope::thread_scope_block,
        stages_count
    > shared_state;
    auto pipeline = cuda::make_pipeline(block, &shared_state);

    // Each thread processes `batch_sz` elements.
    // Compute offset of the batch `batch` of this thread block in global memory
    auto block_batch = [&](size_t batch) -> int {
        return block.group_index().x * block.size() + grid.size() * batch;
    };

    for (size_t batch = 0; batch < batch_sz; ++batch) {
        size_t global_idx = block_batch(batch);

        // Collectively acquire the pipeline head stage from all producer threads
        pipeline.producer_acquire();

        // Submit async copies to the pipeline's head stage to be
        // computed in the next loop iteration
        cuda::memcpy_async(block, shared, global_in + global_idx, sizeof(int) * block.size(), pipeline);
        
        // Collectively commit (advance) the pipeline's head stage
        pipeline.producer_commit();

        // Collectively wait for the operations committed to the
        // previous `compute` stage to complete
        pipeline.consumer_wait();

        // Computation overlapped with the memcpy_async of the "copy" stage
        compute(global_out + global_idx, shared);

        // Collectively release the stage resources
        pipeline.consumer_release();
    }
}
```

## Caveats

-   **Shared Memory Constraints**: The entire batch must fit within the available shared memory for the block [CUDA_C_Programming_Guide:L9808-L9809].
-   **Deterministic Fallback**: The source documentation for this specific example is derived from a deterministic fallback due to research agent limitations; however, the code and API usage remain valid as presented in the CUDA C Programming Guide [CUDA_C_Programming_Guide:L9786-L9844].

## See Also

-   `cuda::pipeline`
-   `cuda::memcpy_async`
-   `cooperative_groups`
-   Multi-stage overlapped compute and copy (expansion of this example)
