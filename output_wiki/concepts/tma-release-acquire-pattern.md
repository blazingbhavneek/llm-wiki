# TMA Tensor Map Release-Acquire Pattern

The TMA Tensor Map Release-Acquire Pattern is a synchronization mechanism required when using a tensor map stored in global memory that has been modified by one thread and subsequently used by another. Unlike tensor maps passed as `const __grid_constant__` kernel parameters, which are immutable and visible to all threads, modified tensor maps require explicit establishment of a release-acquire pattern to ensure that updates to the map's metadata are visible and correctly ordered across threads.

## Release Phase

The release phase is performed by the thread that modifies the tensor map. It ensures that the updated tensor map data is committed to memory and visible to other threads. This is accomplished using the `cuda::ptx::tensormap.cp_fenceproxy` function [CUDA_C_Programming_Guide:L10999-L11048].

## Acquire Phase

The acquire phase is performed by the thread that intends to use the modified tensor map. It ensures that the thread sees the most recent version of the tensor map before issuing copy operations. This is accomplished using the `cuda::ptx::fence_proxy_tensormap_generic` function, which wraps the `fence.proxy.tensormap::generic.acquire` PTX instruction [CUDA_C_Programming_Guide:L10999-L11048].

### Scope Selection

The scope of the acquire fence depends on the location of the threads involved:

*   **Same Device:** If the thread performing the release and the thread performing the acquire are on the same device, the `.gpu` scope suffices [CUDA_C_Programming_Guide:L10999-L11048].
*   **Different Devices:** If the threads are on different devices, the `.sys` scope must be used [CUDA_C_Programming_Guide:L10999-L11048].

## Thread Block Constraints

The thread that uses the tensor map and the thread that performs the fence acquire must be in the same thread block [CUDA_C_Programming_Guide:L10999-L11048].

Synchronization APIs such as `cooperative_groups::cluster`, `grid_group::sync()`, or stream-order synchronization do **not** suffice to establish ordering for tensor map updates if the threads are in different thread blocks (e.g., different blocks of the same cluster, same grid, or different kernel) [CUDA_C_Programming_Guide:L10999-L11048]. In such cases, threads in other blocks must still acquire the tensor map proxy at the appropriate scope before using the updated tensor map [CUDA_C_Programming_Guide:L10999-L11048].

## Usage Example

Once a tensor map has been acquired by one thread, it can be used by other threads in the block after sufficient synchronization, such as `__syncthreads()` [CUDA_C_Programming_Guide:L10999-L11048]. If there are no intermediate modifications to the tensor map, the fence does not need to be repeated before each `cp.async.bulk.tensor` instruction [CUDA_C_Programming_Guide:L10999-L11048].

The following example demonstrates the consumer side of the pattern, where the tensor map is acquired and then used for an asynchronous bulk copy:

```cpp
// Consumer of tensor map in global memory:
__global__ void consume_tensor_map(CUtensorMap* tensor_map) {
    // Fence acquire tensor map:
    ptx::n32_t<128> size_bytes;
    ptx::fence_proxy_tensorsgammaGeneric(ptx::sem_acquire, ptx::scope_sys, tensor_map,
size_bytes);
    // Safe to use tensor_map after fence..

    __shared__ uint64_t bar;
    __shared__ alignas(128) char smem_buf[4][128];

    if (threadIdx.x == 0) {
        // Initialize barrier
        ptx::mbarrier_init(&bar, 1);
        // Make barrier init visible in async proxy, i.e., to TMA engine
        ptx::fence_proxy_async(ptx::space_shared);
        // Issue TMA request
        ptx::cp_async_bulk_tensor(ptx::space_cluster, ptx::space_global, smem_buf, tensor_
map, {0, 0}, &bar);

        // Arrive on barrier. Expect 4 * 128 bytes.
        ptx::mbarrier_arrive_expect_tx(ptx::sem_release, ptx::scope_cta, ptx::space_
shared, &bar, sizeof(smem_buf));
    }
    const int parity = 0;
    // Wait for load to have completed
    while (!ptx::mbarrier_try_wait_parity(&bar, parity)) {}

    // print items:
    printf("Got:\n\n");
    for (int j = 0; j < 4; ++j) {
        for (int i = 0; i < 128; ++i) {
            printf("%3d ", smem_buf[j][i]);
            if (i % 32 == 31) { printf("\n"); };
        }
        printf("\n");
    }
}
```

## See Also

*   `cuda::ptx::tensormap.cp_fenceproxy`
*   `cuda::ptx::fence_proxy_tensormap_generic`
*   Tensor Map Usage in CUDA
