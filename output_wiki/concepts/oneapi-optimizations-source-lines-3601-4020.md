# oneapi_optimizations Source Lines 3601-4020

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L3601-L4020

Citation: [oneapi_optimizations:L3601-L4020]

````text
## Considerations for Selecting Work-Group Size

In SYCL you can select the work-group size for nd\_range kernels. The size of work-group has important implications for utilization of the compute resources, vector lanes, and communication among the workitems. The work-items in the same work-group may have access to hardware resources like shared local memory and hardware synchronization capabilities that will allow them to run and communicate more efficiently than work-items across work-groups. So in general you should pick the maximum work-group size supported by the accelerator. The maximum work-group size can be queried by the call device::get\_info<cl::sycl::info::device::max\_work\_group\_size>().

To illustrate the impact of the choice of work-group size, consider the following reduction kernel, which goes through a large vector to add all the elements in it. The function that runs the kernels takes in the workgroup-size and sub-group-size as arguments, which lets you run experiments with different values. The performance difference can be seen from the timings reported when the kernel is called with different values for work-group size.

```cpp
void reduction(sycl::queue &q, std::vector<int> &data, std::vector<int> &flush,
        int iter, int work_group_size) {
    const size_t data_size = data.size();
    const size_t flush_size = flush.size();
    int sum = 0;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
    // int vec_size =
    // q.get_device().get_info<sycl::info::device::native_vector_width_int>();
    int num_work_items = data_size / work_group_size;
    sycl::buffer<int> buf(data.data(), data_size, props);
    sycl::buffer<int> flush_buf(flush.data(), flush_size, props);
    sycl::buffer<int> sum_buf(&sum, 1, props);

    init_data(q, buf, data_size);

    double elapsed = 0;
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(1, [=](auto index) { sum_acc[index] = 0; });
        });
        // flush the cache
        q.submit([&](auto &h) {
            sycl::accessor flush_acc(flush_buf, h, sycl::write_only, sycl::no_init);
            h.parallel_for(flush_size, [=](auto index) { flush_acc[index] = 1; });
        });

        Timer timer;
        // reductionMapToHWVector main begin
        q.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::local_accessor<int, 1> scratch(work_group_size, h);
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
```

```cpp
h.parallel_for(
    sycl::nd_range<1>(num_work_items, work_group_size),
    [=](sycl::nd_item<1> item) [[intel::reqd_sub_group_size(16)]] {
        auto v =
            sycl::atomic_ref<int, sycl::memory_order::relaxed,
                sycl::memory_scope::device,
                sycl::access::address_space::global_space>(
                    sum_acc[0]);
        int sum = 0;
        int glob_id = item.get_global_id();
        int loc_id = item.get_local_id();
        for (unsigned int i = glob_id; i < data_size; i += num_work_items
            sum += buf_acc[i];
        scratch[loc_id] = sum;

        for (int i = work_group_size / 2; i > 0; i >>= 1) {
            item.barrier(sycl::access::fence_space::local_space);
            if (loc_id < i)
                scratch[loc_id] += scratch[loc_id + i];
        }

        if (loc_id == 0)
            v.fetch_add(scratch[0]);
    });
});
q.wait();
elapsed += timer.Elapsed();
sycl::host_accessor h_acc(sum_buf);
sum = h_acc[0];
}
elapsed = elapsed / iter;
std::string msg = "with work-groups=" + std::to_string(work_group_size);
check_result(elapsed, msg, sum);
// reduction end
```

In the code below, the above kernel is called with two different values: 2\*vec-size and the maximum possible work-group size supported by the accelerator. The performance of the kernel when work-group size is equal to 2\*vec-size will be lower than when the work-group size is the maximum possible value.

```rust
int vec_size = 16;
int work_group_size = vec_size;
reduction(q, data, extra, 16, work_group_size);
work_group_size =
    q.get_device().get_info<sycl::info::device::max_work_group_size>();
reduction(q, data, extra, 16, work_group_size);
```

In situations where there are no barriers nor atomics used, the work-group size will not impact the performance. To illustrate this, consider the following vec\_copy kernel where there are no atomics or barriers.

```cpp
void vec_copy(sycl::queue &q, std::vector<int> &src, std::vector<int> &dst,
        std::vector<int> &flush, int iter, int work_group_size) {
    const size_t data_size = src.size();
    const size_t flush_size = flush.size();

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
    int num_work_items = data_size;
    double elapsed = 0;
    {
```

```cpp
sycl::buffer<int> src_buf(src.data(), data_size, props);
sycl::buffer<int> dst_buf(dst.data(), data_size, props);
sycl::buffer<int> flush_buf.flush.data(), flush_size, props);

for (int i = 0; i < iter; i++) {
    // flush the cache
    q.submit([&](auto &h) {
        sycl::accessor flush_acc_flush_buf, h, sycl::write_only, sycl::no_init);
        h.parallel_for.flush_size, [=](auto index) { flush_acc[index] = 1; });
    });

    Timer timer;
    q.submit([&](auto &h) {
        sycl::accessor src_acc(src_buf, h, sycl::read_only);
        sycl::accessor dst_acc(dst_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(sycl::nd_range<1>(num_work_items, work_group_size),
            [=](sycl::nd_item<1> item)
                [[intel::reqd_sub_group_size(16)]] {
                    int glob_id = item.get_global_id();
                    dst_acc[glob_id] = src_acc[glob_id];
                });
    });
    q.wait();
    elapsed += timer.Elapsed();
}
elapsed = elapsed / iter;
std::string msg = "with work-group-size=" + std::to_string(work_group_size);
check_result(elapsed, msg, dst);
// vec_copy end
```

In the code below, the above kernel is called with different work-group sizes. All the above calls to the kerne will have similar run times which indicates that there is no impact of work-group size on performance. The reason for this is that the threads created within a work-group and threads from different work-groups behave in a similar manner from the scheduling and resourcing point of view when there are no barriers nor shared memory in the work-groups.

```c
int vec_size = 16;
int work_group_size = vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 2 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 4 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 8 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 16 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
```

In some accelerators, a minimum sub-group size is needed to obtain good performance due to the way in which threads are scheduled among the processing elements. In such a situation you may see a big performance difference when the number of sub-groups is less than the minimum. The call to the kernel on line 3 above has only one sub-group, while the call on line 5 has two sub-groups. There will be a significant performance difference in the timings for these two kernel invocations on an accelerator that performs scheduling of of two sub-groups at a time.

## Tuning Kernels with Local and Global Work-group Sizes in OpenMP Offload Mode

The approach of tuning kernel performance on accelerator devices as explained above for SYCL, is also applicable for implementations via OpenMP in offload mode. It is possible to customize an application kernel along with the use of OpenMP directives to make use of appropriate work-group sizes. However, this may require significant modifications to the code. The OpenMP implementation provides an option to custom tune kernels with the use of environment variables. The local and global work-group sizes for kernels in an app can be customized with the the use of two environment variables – OMP\_THREAD\_LIMIT and OMP\_NUM\_TEAMS help in setting up the local work-group size (LWS) and global work-group size (GWS) as shown below:

```txt
LWS = OMP_THREAD_LIMIT
GWS = OMP_THREAD_LIMIT * OMP_NUM_TEAMS
```

With the help of following reduction kernel example, we show the use of LWS and GWS in tuning kernel performance on accelerator device.

```c
int N = 2048;

double* A = make_array(N, 0.8);
double* B = make_array(N, 0.65);
double* C = make_array(N*N, 2.5);
if ((A == NULL) || (B == NULL) || (C == NULL))
    exit(1);

int i, j;
double val = 0.0;

#pragma omp target map(to:A[0:N],B[0:N],C[0:N*N]) map(tofrom:val)
{

#pragma omp teams distribute parallel for collapse(2) reduction(+ : val)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            val += C[i * N + j] * A[i] * B[j];
        }
    }
}

printf("val = %f10.3\n", val);

free(A);
free(B);
free(C);
```

e.g. by choosing OMP\_THREAD\_LIMIT = 1024 and OMP\_NUM\_TEAMS = 120, the LWS and GWS parameters are set to 1024 and 122880, respectively.

![](images/cb2e531f1415f628ccaeed5f4aa1df661b61b84cacbcc312ddae33a701465d87.jpg)  
The figure above shows that the best performance for this kernel comes with LWS = 1024 and GWS = 30720 which corresponds to OMP\_THREAD\_LIMIT = 1024 and OMP\_NUM\_TEAMS = 30. These environment variables will set the LWS and GWS values to a fixed numbers for all kernels offloaded via OpenMP. However, these environment variables will not affect the LWS and GWS used by highly tuned library kernels like OneMKL.

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
````
