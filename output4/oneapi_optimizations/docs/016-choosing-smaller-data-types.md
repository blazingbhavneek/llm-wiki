
This example calculates histograms with a bin size of 32. Each work item has 32 private bins of unsigned long data type. Because of the large storage required, the private bins cannot fit in registers, resulting in poor performance.

With BLOCK\_SIZE 256, the maximum value of each private histogram bin will not exceed the maximum value of an unsigned integer. Instead of unsigned long type for private histogram bins, we can use unsigned integers to reduce register pressure so the private bins can fit in registers. This simple change makes significant performance difference.

```cpp
constexpr int BLOCK_SIZE = 256;
constexpr int NUM_BINS = 32;

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

            unsigned int histogram[NUM_BINS]; // histogram bins take less storage
                                    // with smaller data type
            for (int k = 0; k < NUM_BINS; k++) {
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

            for (int k = 0; k < NUM_BINS; k++) {
                hacc[k].fetch_add(histogram[k]);
            }
        });
    });
```
