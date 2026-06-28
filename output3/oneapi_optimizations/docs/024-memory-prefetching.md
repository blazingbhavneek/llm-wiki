## Prefetch

Access to global memory is one of the most common reasons of execution stall. When application stops and waits for data to reach local registers, it is called memory latency. This is especially costly when access misses cache and must reach HBM memory. GPU tries to hide memory latencies by reordering instructions to execute (out-of-order execution) and switching threads in Vector Engine. If these techniques are not enough and application keeps stalling, yet memory bandwidth is not fully utilized, application developer might use prefetch function to provide hints when to load data into local cache before expected use. When correctly used, next access to memory will successfully hit cache, shortening distance for data to reach registers, lowering memory latency. Prefetch works on Intel<sup>®</sup> Data Center GPU Max Series and later products.

Prefetch is an asynchronous operation. When submitting prefetch, application does not wait for data to reach cache and keeps running. This means prefetch must be submitted way ahead of expected access, so there are enough instructions in between to hide the transfer of data from HBM memory to local cache.

One common use case for prefetch are memory accesses inside loop. In typical use case, compiler tries to apply loop unrolling optimization. This technique gives scheduler more instructions to work with, intertwining loop iterations and hiding memory latencies in the process. If this technique can’t be applied (unknown loop boundaries; high register pressure in larger kernels), prefetch can be used to lower memory latencies by caching data for future iterations.

Intel<sup>®</sup> VTune<sup>TM</sup> Profiler can be used to search for chances to use prefetch. If memory bandwidth is not fully utilized and number of scoreboard stalls is high (execution waits for data to load), there is a good chance that correctly inserted prefetch can speed up execution.

Examples in this section create artificial scenario to simulate case where GPU is unable to hide latencies. First, we run only one work-group, submitting hardware threads only to one Vector Engine. Then, we use pragma to disable loop unrolling. This limits number of available instructions to reschedule in order to hide memory latency.

In first example, kernel reduces array values and saves result to results. values uses indirect indexing, with indices loaded from array indices. Because indices are unknown at compilation time, compiler can’t optimize access to array values. Since loop unrolling is disabled, GPU can’t schedule other work between accessing indices and values and execution stalls until access to indices finishes.

```txt
auto e = q.submit([&](auto &h) {
    h.parallel_for(
        sycl::nd_range(sycl::range{GLOBAL_WORK_SIZE},
            sycl::range{GLOBAL_WORK_SIZE}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(SIMD_SIZE)]] {
            const int i = it.get_global_linear_id();
            const int lane = it.get_sub_group().get_local_id()[0];
            const int subgroup = it.get_sub_group().get_group_id()[0];

            // Index starting position
            int *indexCurrent = indices + lane + subgroup * ITEMS_PER_SUBGROUP;

            float dx = 0.0f;
#pragma unroll(0)
            for (int j = 0; j < ITEMS_PER_LANE; ++j) {
                // Load index for indirect addressing
                int index = *indexCurrent;
                // Waits for load to finish, high latency
                float v = values[index];
                for (int k = 0; k < 64; ++k)
                    dx += sycl::sqrt(v + k);

                indexCurrent += SIMD_SIZE;
            }

            result[i] = dx;
        });
    });
```

In second example, before accessing current value from indices, kernel calls sycl::global\_ptr::prefetch to submit prefetch request of next index, potentially speeding up access on next iteration. Data is not prefetched for first iterations, as there is not enough instructions to hide latency.

```cpp
auto e = q.submit([&](auto &h) {
    h.parallel_for(
        sycl::nd_range(sycl::range{GLOBAL_WORK_SIZE},
            sycl::range{GLOBAL_WORK_SIZE}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(SIMD_SIZE)]] {
            const int i = it.get_global_linear_id();
            const int lane = it.get_sub_group().get_local_id()[0];
            const int subgroup = it.get_sub_group().get_group_id()[0];

            // Index starting position
            int *indexCurrent = indices + lane + subgroup * ITEMS_PER_SUBGROUP;
            int *indexNext = indexCurrent + SIMD_SIZE;

            float dx = 0.0f;
#pragma unroll(0)
            for (int j = 0; j < ITEMS_PER_LANE; ++j) {
                // Prefetch next index to cache
```

```cpp
sycl::global_ptr<int>(indexNext).prefetch(1);
    // Load index, might be cached
    int index = *indexCurrent;
    // Latency might be reduced if index was cached
    float v = values[index];
    for (int k = 0; k < 64; ++k)
        dx += sycl::sqrt(v + k);

    indexCurrent = indexNext;
    indexNext += SIMD_SIZE;
}

result[i] = dx;
});
});
```

sycl::global\_ptr::prefetch takes one argument: number of continuous elements to prefetch. Prefetch is available only for global address space. At the moment this function has multiple limitations that should be taken into consideration:

1. Compiler caches at max 32 bytes total per work item for each prefetch call (even for larger data types).

2. Compiler prefers for argument (number of continuous elements to prefetch) to be constant at compilation time.

3. There is no control over to what cache data will be fetched. Current implementation loads data only to L3 cache.

Lack of cache control heavily limits scenarios where sycl::global\_ptr::prefetch can give meaningful performance gains. When running second example, user might even see performance loss. Prefetch gives best results if data is loaded to L1 cache. At the moment on Intel<sup>®</sup> Data Center GPU Max Series this is possible only with dedicated functions. First, include these declarations in your code:

```lisp
#include <sycl/sycl.hpp>

enum LSC_LDCC {
  LSC_LDCC_DEFAULT,
  LSC_LDCC_L1UC_L3UC, // 1 // Override to L1 uncached and L3 uncached
  LSC_LDCC_L1UC_L3C, // 2 // Override to L1 uncached and L3 cached
  LSC_LDCC_L1C_L3UC, // 3 // Override to L1 cached and L3 uncached
  LSC_LDCC_L1C_L3C, // 4 // Override to L1 cached and L3 cached
  LSC_LDCC_L1S_L3UC, // 5 // Override to L1 streaming load and L3 uncached
  LSC_LDCC_L1S_L3C, // 6 // Override to L1 streaming load and L3 cached
  LSC_LDCC_L1IAR_L3C, // 7 // Override to L1 invalidate-after-read, and L3
        // cached
};

extern "C" {
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uchar(const __attribute__((opencl_global))
                      uint8_t *base,
                      int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ushort(const __attribute__((opencl_global))
                      uint16_t *base,
                      int immElemOff, enum LSC_LDCC cacheOpt)
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uint(const __attribute__((opencl_global))
                      uint32_t *base,
                      int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uint2(const __attribute__((opencl_global))
```

```lisp
uint32_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uint3(const __attribute__((opencl_global))
uint32_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uint4(const __attribute__((opencl_global))
uint32_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_uint8(const __attribute__((opencl_global))
uint32_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ulong(const __attribute__((opencl_global))
uint64_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ulong2(const __attribute__((opencl_global))
uint64_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ulong3(const __attribute__((opencl_global))
uint64_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ulong4(const __attribute__((opencl_global))
uint64_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
SYCL_EXTERNAL void
__builtin_IB_lsc_prefetch_global_ulong8(const __attribute__((opencl_global))
uint64_t *base,
int immElemOff, enum LSC_LDCC cacheOpt);
}
```

Argument cacheOpt selects target cache. sycl::global\_ptr::prefetch maps to LSC\_LDCC\_L1UC\_L3C. In most scenarios value LSC\_LDCC\_L1C\_L3C is expected to give the best results. Argument immElemOff can be used to offset base pointer, but in most cases base pointer is set to correct address to fetch, and immElemOff is set to 0.

Prefetch to L1 does not support safe out-of-bounds access. When using this type of prefetch, application must take full ownership of bounds checking, otherwise any out-of-bounds access will end with undefined behavior.

Third example shows L1 prefetch in action, including bounds checking:

```rust
auto e = q.submit([&](auto &h) {
    h.parallel_for(
        sycl::nd_range(sycl::range{GLOBAL_WORK_SIZE},
            sycl::range{GLOBAL_WORK_SIZE}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(SIMD_SIZE)]] {
            const int i = it.get_global_linear_id();
            const int lane = it.get_sub_group().get_local_id()[0];
            const int subgroup = it.get_sub_group().get_group_id()[0];

            // Index starting position
            int *indexCurrent = indices + lane + subgroup * ITEMS_PER_SUBGROUP;
            int *indexNext = indexCurrent + SIMD_SIZE;
```

```lisp
float dx = 0.0f;
#pragma unroll(0)
    for (int j = 0; j < ITEMS_PER_LANE; ++j) {
        // Prefetch next index to cache
#if __SYCL_DEVICE_ONLY__
        if (j < ITEMS_PER_LANE - 1)
            __builtin_IB_lsc_prefetch_global_uint(
                (const __attribute__((opencl_global)) uint32_t *)indexNext, 0,
                LSC_LDCC_L1C_L3C);
#endif
        // Load index, might be cached
        int index = *indexCurrent;
        // Latency might be reduced if index was cached
        float v = values[index];
        for (int k = 0; k < 64; ++k)
            dx += sycl::sqrt(v + k);

        indexCurrent = indexNext;
        indexNext += SIMD_SIZE;
    }

    result[i] = dx;
});
});
```

When manually fetching data to cache, remember that memory fences might flush cache, so it might be required to repeat prefetch to refill it back.

Presented examples give only an idea how to use prefetch and don’t represent real-life use cases. In short kernels like these normal optimization methods like loop unrolling are enough to hide memory latencies. Prefetch hints are expected to give performance gains in larger kernels, where ordinary optimization methods applied by compiler might not be sufficient.
