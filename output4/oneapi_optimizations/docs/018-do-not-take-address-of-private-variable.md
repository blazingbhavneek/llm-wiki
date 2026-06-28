## Do Not Take Address of a Private Variable and Later Dereference the Pointer

Now we make more changes to the code example:

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
```

```txt
sycl::nd_range(sycl::range{N / BLOCK_SIZE}, sycl::range{64}),
[=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
    int group = it.get_group()[0];
    int gSize = it.get_local_range()[0];
    auto sg = it.get_sub_group();
    int sgSize = sg.get_local_range()[0];
    int sgGroup = sg.get_group_id()[0];

    unsigned int histogram[NUM_BITS]; // histogram bins take less storage
                                      // with smaller data type
    for (int k = 0; k < NUM_BITS; k++) {
        histogram[k] = 0;
    }
    for (int k = 0; k < BLOCK_SIZE; k++) {
        unsigned long x = sg.load(
            macc.template get_multi_ptr<sycl::access::decorated::yes>() +
            group * gSize * BLOCK_SIZE + sgGroup * sgSize * BLOCK_SIZE +
            sgSize * k);
        unsigned long *p = &x;
#pragma unroll
        for (int i = 0; i < 8; i++) {
            unsigned int c = (*p & 0x1FU);
            histogram[c] += 1;
            *p = (*p >> 8);
        }
    }

    for (int k = 0; k < NUM_BITS; k++) {
        hacc[k].fetch_add(histogram[k]);
    }
});
});
```

The address of private variable x is taken and stored in pointer p and later p is dereferenced to access x. Because its address is used, the variable x now has to reside in memory even there is room for it in registers.
