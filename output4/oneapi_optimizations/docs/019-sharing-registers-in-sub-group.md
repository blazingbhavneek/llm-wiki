## Sharing Registers in a Sub-group

Now we increase the histogram bins to 256:

```rust
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
```

```txt
int sgSize = sg.get_local_range()[0];
int sgGroup = sg.get_group_id()[0];

unsigned int
    histogram[NUM_BITS]; // histogram bins take too much storage to be
        // promoted to registers
for (int k = 0; k < NUM_BITS; k++) {
    histogram[k] = 0;
}
for (int k = 0; k < BLOCK_SIZE; k++) {
    unsigned long x = sg.load(
        get_accessor_pointer(macc) + group * gSize * BLOCK_SIZE +
        sgGroup * sgSize * BLOCK_SIZE + sgSize * k);
#pragma unroll
    for (int i = 0; i < 8; i++) {
        unsigned int c = x & 0x1FU;
        histogram[c] += 1;
        x = x >> 8;
    }
}

for (int k = 0; k < NUM_BITS; k++) {
    hacc[k].fetch_add(histogram[k]);
}
});
});
```

With 256 histogram bins, the performance degrades even with smaller data type unsigned integer. The storage of the private bins in each work item is too large for registers.

## Each Work Item Has 256 Private Histogram Bins

![](images/7bcc30f9078138d79425b877f11a5d98a9ae36817dce8b2bdfa4809bd20b56a0.jpg)

If the sub-group size is 16 as requested, we know that 16 work items are packed into one Vector Engine thread. We also know work items in the same sub-group can communicate and share data with each other very efficiently. If the work items in the same sub-group share the private histogram bins, only 256 private bins are needed for the whole sub-group, or 16 private bins for each work item instead.

## Sub-group Has 256 Private Histogram Bins

![](images/96e02ae19f5182824527de6edba7999ca41dc950647be5e8ce0f59533d252d1c.jpg)

To share the histogram bins in the sub-group, each work item broadcasts its input data to every work item in the same sub-group. The work item that owns the corresponding histogram bin does the update.

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
```

```cpp
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
