# Use Multicast Mappings

Multicast mappings allow for efficient collective memory operations in CUDA C++ by utilizing multicast (MC) and unicast (UC) memory mappings. To use Multicast Mappings in CUDA C++, it is required to use the `multimem` PTX instructions with Inline PTX Assembly.

## Prerequisites

*   **Compute Capability**: The code must be compiled for compute capability 9.0 or larger. This is typically enforced using `#if __CUDA_ARCH__ >= 900`.

## Implementation Details

### Multicast vs. Unicast Access

When working with multicast mappings, it is critical to manage the ordering between multicast (MC) and unicast (UC) accesses to the same memory location. The `fence.proxy.alias` instruction is used to establish an ordering between memory accesses that may happen through different proxies, specifically referring to memory accesses performed using virtually aliased addresses to the same memory location.

### Example: All-Reduce Norm Barrier

The following example demonstrates an all-reduce norm barrier kernel using multicast mappings. It involves:

1.  **Atomic Reduction**: Using `multimem.red.release.sys.global.add.u32` to atomically add to the multicast arrival counter.
2.  **Synchronization**: Using `fence.proxy.alias` to ensure ordering between MC and UC accesses.
3.  **Spin Wait**: Using a unicast atomic reference to wait for all peers to arrive.
4.  **Atomic Load Reduction**: Using `multimem.ld_reduce.relaxed.sys.global.add.f32` to perform an atomic load reduction from all replicas.

```cpp
__global__ void all_reduce_norm_barrier_kernel(float* l2_norm,
                                float* partial_l2_norm_mc,
                                unsigned int* arrival_counter_uc,
    unsigned int* arrival_counter_mc,
                                const unsigned int expected_count) {
        assert( 1 == blockDim.x * blockDim.y * blockDim.z * gridDim.x * gridDim.y *
        gridDim.z );
        float l2_norm_sum = 0.0;
#if __CUDA_ARCH__ >= 900

        // atomic reduction to all replicas
        // this can be conceptually thought of as __threadfence_system(); atomicAdd_
        system(arrival_counter_mc, 1);
        asm volatile ("multimem.red.release.sys.global.add.u32 [%0], %1;" :: "l"(arrival_
        counter_mc), "n"(1) : "memory");

        // Need a fence between Multicast (mc) and Unicast (uc) access to the same memory
        `arrival_counter_uc` and `arrival_counter_mc`:
        // - fence.proxy instructions establish an ordering between memory accesses that
        may happen through different proxies
        // - Value .alias of the .proxykind qualifier refers to memory accesses performed
        using virtually aliased addresses to the same memory location.
        // from https://docs.nvidia.com/cuda/parallel-thread-execution/#parallel-
        synchronization-and-communication-instructions-membar
        asm volatile ("fence.proxy.alias;" ::: "memory");

        // spin wait with acquire ordering on UC mapping till all peers have arrived in
        this iteration
        // Note: all ranks need to reach another barrier after this kernel, such that it is
        not possible for the barrier to be unblocked by an
        // arrival of a rank for the next iteration if some other rank is slow.
        cuda::atomic_ref<unsigned int,cuda::thread_scope_system> ac(arrival_counter_uc);
        while (expected_count > ac.load(cuda::memory_order_acquire));

        // Atomic load reduction from all replicas. It does not provide ordering so it can
        be relaxed.
        asm volatile ("multimem.ld_reduce.relaxed.sys.global.add.f32 %0, [%1];" : "=f"(l2_
        norm_sum) : "l"(partial_l2_norm_mc) : "memory");

#else
    #error "ERROR: multimem instructions require compute capability 9.0 or larger."
#endif
}
```

## References

*   [CUDA_C_Programming_Guide:L15332-L15380]
