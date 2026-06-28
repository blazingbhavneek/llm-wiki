## Do Not Declare Private Variables as Volatile

Now we make a small change to the code example:

```cpp
constexpr int BLOCK_SIZE = 256;
constexpr int NUM_BITS = 32;

std::vector<unsigned long> hist(NUM_BITS, 0);

sycl::buffer<unsigned long, 1> mbuf(input.data(), N);
sycl::buffer<unsigned long, 1> hbuf(hist.data(), NUM_BITS);
```

```cpp
auto e = q.submit([&](auto &h) {
    sycl::accessor macc(mbuf, h, sycl::read_only);
    auto hacc = hbuf.get_access<sycl::access::mode::atomic>(h);
    h.parallel_for(sycl::nd_range(sycl::range{N / BLOCK_SIZE}, sycl::range{64}), [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
        int group = it.get_group()[0];
        int gSize = it.get_local_range()[0];
        auto sg = it.get_sub_group();
        int sgSize = sg.get_local_range()[0];
        int sgGroup = sg.get_group_id()[0];

        volatile unsigned int
            histogram[NUM_BINS]; // volatile variables will not
                                        // be assigned to any registers

        for (int k = 0; k < NUM_BINS; k++) {
            histogram[k] = 0;
        }
        for (int k = 0; k < BLOCK_SIZE; k++) {
            unsigned long x = sg.load(
                macc.get_pointer() + group * gSize * BLOCK_SIZE +
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

The private histogram array is qualified as a volatile array. Volatile variables are not prompted to registers because their values may change between two different load operations.

There is really no reason for the private histogram array to be volatile, because it is only accessible by the local execution thread. In fact, if a private variable really needs to be volatile, it is not private any more.
