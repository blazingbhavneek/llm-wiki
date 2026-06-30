# oneapi_optimizations Source Lines 2644-3278

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L2644-L3278

Citation: [oneapi_optimizations:L2644-L3278]

````text
## Bank Conflicts

The SLM is divided into equally sized memory banks that can be accessed simultaneously for high bandwidth. The total number of banks is device-dependent. At the time of writing, 64 consecutive bytes are stored in 16 consecutive banks at 4-byte (32-bit) granularity. Requests for access to different banks can be serviced in parallel, but requests to different addresses in the same bank cause a bank conflict and are serialized. Bank conflicts adversely affect performance. Consider this example:

```cpp
constexpr int N = 32;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([&](auto &h) {
    sycl::local_accessor<int, 1> slm(sycl::range(32 * 64), h);
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            int j = it.get_local_linear_id();

            slm[j * 16] = 0;
            it.barrier(sycl::access::fence_space::local_space);

            for (int m = 0; m < 1024 * 1024; m++) {
                slm[j * 16] += i * m;
                it.barrier(sycl::access::fence_space::local_space);
            }

            data[i] = slm[j * 16];
        });
});
```

If the number of banks is 16, all work-items in the above example will read from and write to different addresses in the same bank. The memory bandwidth is 1/16 of full bandwidth.

The next example instead does not have SLM bank conflicts and achieves full memory bandwidth because every work-item reads from and writes to different addresses in different banks.

```cpp
constexpr int N = 32;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([&](auto &h) {
    sycl::local_accessor<int, 1> slm(sycl::range(32 * 64), h);
```

```cpp
h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
    [=](sycl::nd_item<1> it) {
        int i = it.get_global_linear_id();
        int j = it.get_local_linear_id();

        slm[j] = 0;
        it.barrier(sycl::access::fence_space::local_space);

        for (int m = 0; m < 1024 * 1024; m++) {
            slm[j] += i * m;
            it.barrier(sycl::access::fence_space::local_space);
        }

        data[i] = slm[j];
    });
});
```

## Data Sharing and Work-group Barriers

Let us consider the histogram with 256 bins example from the Optimizing Register Spills once again.

```cpp
constexpr int BLOCK_SIZE = 256;
constexpr int NUM_BINS = 256;

std::vector<unsigned long> hist(NUM_BINS, 0);

sycl::buffer<unsigned long, 1> mbuf(input.data(), N);
sycl::buffer<unsigned long, 1> hbuf(hist.data(), NUM_BINS);

auto e = q.submit([&](auto &h) {
    sycl::accessor macc(mbuf, h, sycl::read_only);
    auto hacc = hbuf.get_access<sycl::access::mode::atomic>(h);
    h.parallel_for(
        sycl::nd_range(sycl::range{N / BLOCK_SIZE}, sycl::range{64}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
            int group = it.get_group()[0];
            int gSize = it.get_local_range()[0];
            auto sg = it.get_sub_group();
            int sgSize = sg.get_local_range()[0];
            int sgGroup = sg.get_group_id()[0];

        unsigned int
            histogram[NUM_BINS / 16]; // histogram bins take too much storage
                                    // to be promoted to registers
        for (int k = 0; k < NUM_BINS / 16; k++) {
            histogram[k] = 0;
        }
        for (int k = 0; k < BLOCK_SIZE; k++) {
            unsigned long x = sg.load(
                get_accessor_pointer(macc) + group * gSize * BLOCK_SIZE +
                sgGroup * sgSize * BLOCK_SIZE + sgSize * k);
// subgroup size is 16
#pragma unroll
            for (int j = 0; j < 16; j++) {
                unsigned long y = sycl::group_broadcast(sg, x, j);
#pragma unroll
                for (int i = 0; i < 8; i++) {
                    unsigned int c = y & 0xFF;
```

```txt
// (c & 0xF) is the workitem in which the bin resides
// (c >> 4) is the bin index
if (sg.get_local_id()[0] == (c & 0xF)) {
    histogram[c >> 4] += 1;
}
y = y >> 8;
}
}
}

for (int k = 0; k < NUM_BINS / 16; k++) {
    hacc[16 * k + sg.get_local_id()[0]].fetch_add(histogram[k]);
}
});
});
```

This example has been optimized to use the integer data type instead of long and to share registers in the sub-group so that the private histogram bins can fit in registers for optimal performance. If you need a larger bin size (e.g., 1024), it is inevitable that the private histogram bins will spill to global memory.

The histogram bins can be shared by work-items in a work-group as long as each bin is updated atomically.

```cpp
constexpr int NUM_BINS = 1024;
constexpr int BLOCK_SIZE = 256;

std::vector<unsigned long> hist(NUM_BINS, 0);
sycl::buffer<unsigned long, 1> mbuf(input.data(), N);
sycl::buffer<unsigned long, 1> hbuf(hist.data(), NUM_BINS);

auto e = q.submit([&](auto &h) {
    sycl::accessor macc(mbuf, h, sycl::read_only);
    sycl::accessor hacc(hbuf, h, sycl::read_write);
    sycl::local_accessor<unsigned int, 1> local_histogram(sycl::range(NUM_BINS),
                                h);
    h.parallel_for(
        sycl::nd_range(sycl::range{N / BLOCK_SIZE}, sycl::range{64}),
        [=](sycl::nd_item<1> it) {
            int group = it.get_group()[0];
            int gSize = it.get_local_range()[0];
            auto sg = it.get_sub_group();
            int sgSize = sg.get_local_range()[0];
            int sgGroup = sg.get_group_id()[0];

            int factor = NUM_BINS / gSize;
            int local_id = it.get_local_id()[0];
            if ((factor <= 1) && (local_id < NUM_BINS)) {
                sycl::atomic_ref<unsigned int, sycl::memory_order::relaxed,
                    sycl::memory_scope::device,
                    sycl::access::address_space::local_space>
                    local_bin(local_histogram[local_id]);
                local_bin.store(0);
            } else {
                for (int k = 0; k < factor; k++) {
                    sycl::atomic_ref<unsigned int, sycl::memory_order::relaxed,
                        sycl::memory_scope::device,
                        sycl::access::address_space::local_space>
                    local_bin(local_histogram[gSize * k + local_id]);
                local_bin.store(0);
            }
```

```cpp
}
it.barrier(sycl::access::fence_space::local_space);

for (int k = 0; k < BLOCK_SIZE; k++) {
    unsigned long x = sg.load(
        get_accessor_pointer(macc) + group * gSize * BLOCK_SIZE +
        sgGroup * sgSize * BLOCK_SIZE + sgSize * k);
#pragma unroll
    for (std::uint8_t shift : {0, 16, 32, 48}) {
        constexpr unsigned long mask = 0x3FFU;
        sycl::atomic_ref<unsigned int, sycl::memory_order::relaxed,
                    sycl::memory_scope::device,
                    sycl::access::address_space::local_space>
            local_bin(local_histogram[(x >> shift) & mask]);
        local_bin += 1;
    }
}
it.barrier(sycl::access::fence_space::local_space);

if ((factor <= 1) && (local_id < NUM_BINS)) {
    sycl::atomic_ref<unsigned int, sycl::memory_order::relaxed,
                    sycl::memory_scope::device,
                    sycl::access::address_space::local_space>
        local_bin(local_histogram[local_id]);
    sycl::atomic_ref<unsigned long, sycl::memory_order::relaxed,
                    sycl::memory_scope::device,
                    sycl::access::address_space::global_space>
            global_bin(hacc[local_id]);
    global_bin += local_bin.load();
} else {
    for (int k = 0; k < factor; k++) {
        sycl::atomic_ref<unsigned int, sycl::memory_order::relaxed,
                sycl::memory_scope::device,
                sycl::access::address_space::local_space>
            local_bin(local_histogram[gSize * k + local_id]);
        sycl::atomic_ref<unsigned long, sycl::memory_order::relaxed,
                sycl::memory_scope::device,
                sycl::access::address_space::global_space>
            global_bin(hacc[gSize * k + local_id]);
        global_bin += local_bin.load();
    }
}
});
});
```

When the work-group is started, each work-item in the work-group initializes a portion of the histogram bins in SLM to 0 (code in lines 24-38 in the above example). You could designate one work-item to initialize all the histogram bins, but it is usually more efficient to divide the job among all work-items in the work-group.

The work-group barrier after initialization at line 39 guarantees that all histogram bins are initialized to 0 before any work-item updates any bins.

Because the histogram bins in SLM are shared among all work-items, updates to any bin by any work-item has to be atomic.

The global histograms are updated once the local histograms in the work-group is completed. But before reading the local SLM bins to update the global bins, a work-group barrier is again called at line 43 to make sure all work-items have completed their work.

When SLM data is shared, work-group barriers are often required for work-item synchronization. The barrier has a cost and the cost may increase with a larger work-group size. It is always a good idea to try different work-group sizes to find the best one for your application.

You can find an example of an SLM version of a histogram with 256 bins in the Examples folder. You can compare its performance with the performance of the version using registers. You may get some surprising results, and think about further optimizations that can be done.

## Using SLM as Cache

You may sometimes find it more desirable to have the application manage caching of some hot data than to have the hardware do it automatically. With the application managing data caching directly, whenever the data is needed, you know exactly where the data is and the cost to access it. The SLM can be used for this purpose.

Consider the following 1-D convolution example:

```cpp
sycl::buffer<int> ibuf(input.data(), N);
sycl::buffer<int> obuf(output.data(), N);
sycl::buffer<int> kbuf(kernel.data(), M);

auto e = q.submit([&](auto &h) {
    sycl::accessor iacc(ibuf, h, sycl::read_only);
    sycl::accessor oacc(obuf, h);
    sycl::accessor kacc(kbuf, h, sycl::read_only);

    h.parallel_for(sycl::nd_range<1>(sycl::range{N}, sycl::range{256}),
        [=](sycl::nd_item<1> it) {
        int i = it.get_global_linear_id();
        int group = it.get_group()[0];
        int gSize = it.get_local_range()[0];

        int t = 0;
        int _M = static_cast<int>(M);
        int _N = static_cast<int>(N);

        if ((group == 0) || (group == _N / gSize - 1)) {
            if (i < _M / 2) {
                for (int j = _M / 2 - i, k = 0; j < _M; ++j, ++k) {
                    t += iacc[k] * kacc[j];
                }
            } else {
                if (i + _M / 2 >= _N) {
                    for (int j = 0, k = i - _M / 2;
                        j < _M / 2 + _N - i; ++j, ++k) {
                        t += iacc[k] * kacc[j];
                    }
                } else {
                    for (int j = 0, k = i - _M / 2; j < _M; ++j, ++k) {
                        t += iacc[k] * kacc[j];
                    }
                }
            }
        } else {
            for (int j = 0, k = i - _M / 2; j < _M; ++j, ++k) {
                t += iacc[k] * kacc[j];
            }
        }
    }
}
```

```javascript
oacc[i] = t;
        });
});
```

The example convolves an integer array of 8192 x 8192 elements using a kernel array of 257 elements and writes the result to an output array. Each work-item convolves one element. To convolve one element, however, up to 256 neighboring elements are needed.

Noticing each input element is used by multiple work-items, you can preload all input elements needed by a whole work-group into SLM. Later, when an element is needed, it can be loaded from SLM instead of global memory.

```cpp
sycl::buffer<int> ibuf(input.data(), N);
sycl::buffer<int> obuf(output.data(), N);
sycl::buffer<int> kbuf(kernel.data(), M);

auto e = q.submit([&](auto &h) {
    sycl::accessor iacc(ibuf, h, sycl::read_only);
    sycl::accessor oacc(obuf, h);
    sycl::accessor kacc(kbuf, h, sycl::read_only);
    sycl::local_accessor<int, 1> ciacc(sycl::range(256 + (M / 2) * 2), h);

    h.parallel_for(
        sycl::nd_range(sycl::range{N}, sycl::range{256}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            int group = it.get_group()[0];
            int gSize = it.get_local_range()[0];
            int local_id = it.get_local_id()[0];
            int _M = static_cast<int>(M);

            ciacc[local_id + M / 2] = iacc[i];

            if (local_id == 0) {
                if (group == 0) {
                    for (int j = 0; j < _M / 2; ++j) {
                        ciacc[j] = 0;
                    }
                } else {
                    for (int j = 0, k = i - _M / 2; j < _M / 2; ++j, ++k) {
                        ciacc[j] = iacc[k];
                    }
                }
            }
            if (local_id == gSize - 1) {
                if (group == static_cast<int>(it.get_group_range()[0]) - 1) {
                    for (int j = gSize + _M / 2; j < gSize + _M / 2 + _M / 2; ++j) {
                        ciacc[j] = 0;
                    }
                } else {
                    for (int j = gSize + _M / 2, k = i + 1;
                        j < gSize + _M / 2 + _M / 2; ++j, ++k) {
                        ciacc[j] = iacc[k];
                    }
                }
            }

            it.barrier(sycl::access::fence_space::local_space);
```

```javascript
int t = 0;
for (int j = 0, k = local_id; j < _M; ++j, ++k) {
    t += ciacc[k] * kacc[j];
}

oacc[i] = t;
});
```

When the work-group starts, all input elements needed by each work-item are loaded into SLM. Each workitem, except the first one and the last one, loads one element into SLM. The first work-item loads neighbors on the left of the first element and the last work item loads neighbors on the right of the last element in the SLM. If no neighbors exist, elements in SLM are filled with 0s.

Before convolution starts in each work-item, a local barrier is called to make sure all input elements are loaded into SLM.

The convolution in each work-item is straightforward. All neighboring elements are loaded from the faster SLM instead of global memory.

## Troubleshooting SLM Errors

A PI\_ERROR\_OUT\_OF\_RESOURCES error may occur when a kernel uses more shared local memory than the amount available on the hardware. When this occurs, you will see an error message similar to this:

```txt
$ ./myapp
:
terminate called after throwing an instance of 'sycl::_V1::runtime_error'
what(): Native API failed. Native API returns: -5
(PI_ERROR_OUT_OF_RESOURCES) -5 (PI_ERROR_OUT_OF_RESOURCES)
Aborted (core dumped)
$
```

To see how much memory was being requested and the actual hardware limit, set debug keys:

```typescript
export PrintDebugMessages=1
export NEOReadDebugKeys=1
```

This will change the output to:

```txt
$ ./myapp
:
Size of SLM (656384) larger than available (131072)
terminate called after throwing an instance of 'sycl::_V1::runtime_error'
what(): Native API failed. Native API returns: -5
(PI_ERROR_OUT_OF_RESOURCES) -5 (PI_ERROR_OUT_OF_RESOURCES)
Aborted (core dumped)
$
```

## Pointer Aliasing and the Restrict Directive

Kernels typically operate on arrays of elements that are provided as pointer arguments. When the compiler cannot determine whether these pointers alias each other, it will conservatively assume that they do, in which case it will not reorder operations on these pointers. Consider the following vector-add example, where each iteration of the loop has two loads and one store.

```cpp
size_t VectorAdd(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
  sycl::range num_items{a.size()};

  sycl::buffer a_buf(a);
```

```cpp
sycl::buffer b_buf(b);
sycl::buffer sum_buf(sum.data(), num_items);

auto start = std::chrono::steady_clock::now();
for (int i = 0; i < iter; i++) {
    auto e = q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(num_items,
                [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add completed on device - took " << (end - start).count()
       << " u-secs\n";
return ((end - start).count());
} // end VectorAdd
```

In this case, the programmer leaves all the choices about vector length and the number of work-groups to the compiler. In most cases the compiler does a pretty good job of selecting these parameters to get good performance. In some situations it may be better to explicitly choose the number of work-groups and workgroup sizes to get good performance and provide hints to the compiler to get better-performing code.

The kernel below is written to process multiple elements of the array per work-item and explicitly chooses the number of work-groups and work-group size. The intel::kernel\_args\_restrict on line 25 tells the compiler that the buffer accessors in this kernel do not alias each other. This will allow the compiler to hoist the loads and stores, thereby providing more time for the instructions to complete and getting better instruction scheduling. The pragma on line 27 directs the compiler to unroll the loop by a factor of two.

```cpp
size_t VectorAdd2(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    // size_t num_groups =
    // q.get_device().get_info<sycl::info::device::max_compute_units>();
    // wg_size =
    // q.get_device().get_info<sycl::info::device::max_work_group_size>();
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(
                    16)]] [[intel::kernel_args_restrict]] {
```

```cpp
size_t loc_id = index.get_local_id();
// unroll with a directive
#pragma unroll(2)
    for (size_t i = loc_id; i < mysize; i += wg_size) {
        sum_acc[i] = a_acc[i] + b_acc[i];
    }
});
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add2 completed on device - took "
       << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd2
```

The kernel below illustrates manually unrolling of the loop instead of the compiler directive (the compiler may or may not honor the directive depending on its internal heuristic cost model). The advantage of unrolling is that fewer instructions are executed because the loop does not have to iterate as many times, thereby saving on the compare and branch instructions.

```cpp
size_t VectorAdd3(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index)
                [[intel::reqd_sub_group_size(16)]] {
                    // Manual unrolling
                    size_t loc_id = index.get_local_id();
                    for (size_t i = loc_id; i < mysize; i += 32) {
                        sum_acc[i] = a_acc[i] + b_acc[i];
                        sum_acc[i + 16] = a_acc[i + 16] + b_acc[i + 16];
                    }
                });
            });
        }
        q.wait();
        auto end = std::chrono::steady_clock::now();
        std::cout << "Vector add3 completed on device - took "
               << (end - start).count() << " u-secs\n";
        return ((end - start).count());
    } // end VectorAdd3
```

The kernel below shows how to reorder the loads and stores so that all loads are issued before any operations on them are done. Typically, there can be many outstanding loads for every thread in the GPU. It is always better to issue the loads before any operations on them are done. This will allow the loads to complete before the data are actually needed for computation.

```cpp
size_t VectorAdd4(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index)
                [[intel::reqd_sub_group_size(16)]] {
                    // Manual unrolling
                    size_t loc_id = index.get_local_id();
                    for (size_t i = loc_id; i < mysize; i += 32) {
                        int t1 = a_acc[i];
                        int t2 = b_acc[i];
                        int t3 = a_acc[i + 16];
                        int t4 = b_acc[i + 16];
                        sum_acc[i] = t1 + t2;
                        sum_acc[i + 16] = t3 + t4;
                    }
                });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add4 completed on device - took "
              << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd4
```

The following kernel has a restrict directive, which provides a hint to the compiler that there is no aliasing among the vectors accessed inside the loop and the compiler can hoist the load over the store just like it was done manually in the previous example.

```cpp
size_t VectorAdd5(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
```

```cpp
for (int i = 0; i < iter; i++) {
    q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(
                16)]] [[intel::kernel_args_restrict]] {
            // compiler needs to hoist the loads
            size_t loc_id = index.get_local_id();
            for (size_t i = loc_id; i < mysize; i += 32) {
                sum_acc[i] = a_acc[i] + b_acc[i];
                sum_acc[i + 16] = a_acc[i + 16] + b_acc[i + 16];
            }
        });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add5 completed on device - took "
           << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd5
```

## Synchronization among Threads in a Kernel

There are a variety of ways in which the work-items in a kernel can synchronize to exchange data, update data, or cooperate with each other to accomplish a task in a specific order. These are:

Accessor classes specify acquisition and release of buffer and image data structures. Depending on where they are created and destroyed, the runtime generates appropriate data transfers and synchronization primitives.

Atomic operations

SYCL devices support a restricted subset of C++ atomics.

Fences

Fence primitives are used to order loads and stores. Fences can have acquire semantics, release semantics, or both.

<sup>•</sup> Barriers

Barriers are used to synchronize sets of work-items within individual groups.

Hierarchical parallel dispatch

In the hierarchical parallelism model of describing computations, synchronization within the work-group is made explicit through multiple instances of the parallel\_for\_work\_item function call, rather than through the use of explicit work-group barrier operations.

```txt
- Device event
```

Events are used inside kernel functions to wait for asynchronous operations to complete.

In many cases, any of the preceding synchronization events can be used to achieve the same functionality, but with significant differences in efficiency and performance.

• Atomic Operations

• Local Barriers vs Global Atomics
````
