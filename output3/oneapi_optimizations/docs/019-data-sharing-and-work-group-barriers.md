
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
