## Optimizing Register Spills

The following techniques can reduce register pressure:

• Keep live ranges of private variables as short as possible.

Though the compiler schedules instructions and optimizes the distances, in some cases moving the loading and using the same variable closer or removing certain dependencies in the source can help the compiler do a better job.

• Avoid excessive loop unrolling.

Loop unrolling exposes opportunities for instruction scheduling optimization by the compiler and thus can improve performance. However, temporary variables introduced by unrolling may increase pressure on register allocation and cause register spilling. It is always a good idea to compare the performance with and without loop unrolling and different times of unrolls to decide if a loop should be unrolled or how many times to unroll it.

• Prefer USM pointers.

A buffer accessor takes more space than a USM pointer. If you can choose between USM pointers and buffer accessors, choose USM pointers.

• Recompute cheap-to-compute values on-demand that otherwise would be held in registers for a long time.

• Avoid big arrays or large structures, or break an array of big structures into multiple arrays of small structures.

For example, an array of sycl::float4:

```txt
``sycl::float4 v[8];
```

can be broken into 4 arrays of float:

```txt
``float x[8];
float y[8];
float z[8];
float w[8];``
```

All or part of the 4 arrays of float have a better chance to be allocated in registers than the array of sycl::float4.

• Break a large loop into multiple small loops to reduce the number of simultaneously live variables.

• Choose smaller sized data types if possible.

• Do not declare private variables as volatile.

• Do not take address of a private variable and later dereference the pointer

• Share registers in a sub-group.

• Use sub-group block load/store if possible.

• Use shared local memory.

The list here is not exhaustive.

The rest of this chapter shows how to apply these techniques, especially the last five, in real examples.

## Choosing Smaller Data Types

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

            unsigned long
                histogram[NUM_BINS]; // histogram bins take too much storage to be
                                // promoted to registers
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
