# TMA Multi-Dimensional (2D) Operations

TMA 2D operations facilitate the asynchronous bulk transfer of multi-dimensional data tiles between global memory and shared memory. This mechanism allows a thread block to load a 2D tile from a larger 2D array, modify the data in shared memory, and write the results back to global memory efficiently.

## Key Requirements

*   **Alignment**: The destination shared memory buffer for a bulk tensor operation must be 128-byte aligned [CUDA_C_Programming_Guide:L10491-L10563].
*   **Tensor Map**: A `CUtensorMap` object is required to describe the geometry and layout of the 2D array being accessed [CUDA_C_Programming_Guide:L10491-L10563].
*   **Barrier Synchronization**: Operations rely on `cuda::barrier` to synchronize threads and manage the asynchronous nature of the TMA transfers [CUDA_C_Programming_Guide:L10491-L10563].

## Operational Workflow

The typical workflow for TMA 2D operations involves the following steps:

1.  **Initialization**: Initialize a shared memory barrier with the number of participating threads in the block [CUDA_C_Programming_Guide:L10491-L10563].
2.  **Global to Shared Copy**: Use `cp_async_bulk_tensor_2d_global_to_shared` to initiate an asynchronous copy from global memory to the shared memory buffer [CUDA_C_Programming_Guide:L10491-L10563].
3.  **Synchronization**: Threads arrive at the barrier, specifying the number of bytes expected (using `barrier_arrive_tx`) or simply arriving (using `bar.arrive()`) [CUDA_C_Programming_Guide:L10491-L10563].
4.  **Wait for Data**: The block waits for the data to have arrived in shared memory using `bar.wait()` [CUDA_C_Programming_Guide:L10491-L10563].
5.  **Modification**: The data in shared memory is modified by the threads [CUDA_C_Programming_Guide:L10491-L10563].
6.  **Visibility**: Ensure shared memory writes are visible to the TMA engine using `fence_proxy_async_shared_cta()` and `__syncthreads()` [CUDA_C_Programming_Guide:L10491-L10563].
7.  **Shared to Global Copy**: Use `cp_async_bulk_tensor_2d_shared_to_global` to initiate the copy from shared memory back to global memory [CUDA_C_Programming_Guide:L10491-L10563].
8.  **Commit and Wait**: Commit the async group and wait for the TMA transfer to finish reading from shared memory using `cp_async_bulk_commit_group()` and `cp_async_bulk_wait_group_read<0>()` [CUDA_C_Programming_Guide:L10491-L10563].
9.  **Cleanup**: Destroy the barrier to invalidate its memory region, allowing reuse [CUDA_C_Programming_Guide:L10491-L10563].

## Example Implementation

The following kernel demonstrates loading a 2D tile of size `SMEM_HEIGHT x SMEM_WIDTH` from a larger 2D array, modifying it, and writing it back. The top-left corner of the tile is specified by indices `x` and `y`.

```cpp
#include <cuda.h>          // CUtensorMap
#include <cuda/barrier>
using barrier = cuda::barrier<cuda::thread_scope_block>;
namespace cde = cuda::device::experimental;

__global__ void kernel(const __grid_constant__ CUtensorMap tensor_map, int x, int y) {
  // The destination shared memory buffer of a bulk tensor operation should be
  // 128 byte aligned.
  __shared__ alignas(128) int smem_buffer[SMEM_HEIGHT][SMEM_WIDTH];

  // Initialize shared memory barrier with the number of threads participating in the
  // barrier.
#pragma nv_diag_suppress static_var_with_dynamic_init
  __shared__ barrier bar;

  if (threadIdx.x == 0) {
      // Initialize barrier. All `blockDim.x` threads in block participate.
      init(&bar, blockDim.x);
      // Make initialized barrier visible in async proxy.
      cde::fence_proxy_async_shared_cta();
  }
  // Syncthreads so initialized barrier is visible to all threads.
  __syncthreads();

  barrier::arrival_token token;
  if (threadIdx.x == 0) {
      // Initiate bulk tensor copy.
      cde::cp_async_bulk_tensor_2d_global_to_shared(&smem_buffer, &tensor_map, x, y,
      bar);
      // Arrive on the barrier and tell how many bytes are expected to come in.
      token = cuda::device::barrier_arrive_tx(bar, 1, sizeof(smem_buffer));
  } else {
      // Other threads just arrive.
      token = bar.arrive();
  }
  // Wait for the data to have arrived.
  bar.wait(std::move(token));

  // Symbolically modify a value in shared memory.
  smem_buffer[0][threadIdx.x] += threadIdx.x;

  // Wait for shared memory writes to be visible to TMA engine.
  cde::fence_proxy_async_shared_cta();
  __syncthreads();
  // After syncthreads, writes by all threads are visible to TMA engine.

  // Initiate TMA transfer to copy shared memory to global memory
  if (threadIdx.x == 0) {
      cde::cp_async_bulk_tensor_2d_shared_to_global(&tensor_map, x, y, &smem_buffer);
      // Wait for TMA transfer to have finished reading shared memory.
      // Create a "bulk async-group" out of the previous bulk copy operation.
      cde::cp_async_bulk_commit_group();
      // Wait for the group to have completed reading from shared memory.
      cde::cp_async_bulk_wait_group_read<0>();
  }

  // Destroy barrier. This invalidates the memory region of the barrier. If
  // further computations were to take place in the kernel, this allows the
  // memory location of the shared memory barrier to be reused.
  if (threadIdx.x == 0) {
      (&bar)->~barrier();
  }
}
```

## Related Functions

*   `cp_async_bulk_tensor_2d_global_to_shared`: Initiates an asynchronous bulk tensor copy from global memory to shared memory [CUDA_C_Programming_Guide:L10491-L10563].
*   `cp_async_bulk_tensor_2d_shared_to_global`: Initiates an asynchronous bulk tensor copy from shared memory to global memory [CUDA_C_Programming_Guide:L10491-L10563].
*   `fence_proxy_async_shared_cta`: Ensures shared memory writes are visible to the async proxy [CUDA_C_Programming_Guide:L10491-L10563].
*   `cp_async_bulk_commit_group`: Commits the async group for TMA operations [CUDA_C_Programming_Guide:L10491-L10563].
*   `cp_async_bulk_wait_group_read`: Waits for the async group to complete reading from shared memory [CUDA_C_Programming_Guide:L10491-L10563].
