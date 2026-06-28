## Data Sharing

Because the work-items in a sub-group execute in the same thread, it is more efficient to share data between work-items, even if the data is private to each work-item. Sharing data in a sub-group is more efficient than sharing data in a work-group using shared local memory, or SLM. One way to share data among work-items in a sub-group is to use shuffle functions.

```cpp
constexpr size_t BLOCK_SIZE = 16;
sycl::buffer<uint, 2> m(matrix.data(), sycl::range<2>(N, N));

auto e = q.submit([&](auto &h) {
    sycl::accessor marr(m, h);
    sycl::local_accessor<uint, 2> barr1(
        sycl::range<2>(BLOCK_SIZE, BLOCK_SIZE), h);
    sycl::local_accessor<uint, 2> barr2(
        sycl::range<2>(BLOCK_SIZE, BLOCK_SIZE), h);

    h.parallel_for(
        sycl::nd_range<2>(sycl::range<2>(N / BLOCK_SIZE, N),
            sycl::range<2>(1, BLOCK_SIZE)),
        [=](sycl::nd_item<2> it) [[intel::reqd_sub_group_size(16)]] {
            int gi = it.get_group(0);
            int gj = it.get_group(1);

            auto sg = it.get_sub_group();
            uint sgId = sg.get_local_id()[0];

            uint bcol[BLOCK_SIZE];
            int ai = BLOCK_SIZE * gi;
            int aj = BLOCK_SIZE * gj;

            for (uint k = 0; k < BLOCK_SIZE; k++) {
                bcol[k] = sg.load(get_accessor_pointer(marr) + (ai + k) * N + aj);
            }

            uint tcol[BLOCK_SIZE];
            for (uint n = 0; n < BLOCK_SIZE; n++) {
                if (sgId == n) {
                    for (uint k = 0; k < BLOCK_SIZE; k++) {
                        tcol[k] = sycl::select_from_group(sg, bcol[n], k);
                    }
                }
            }

            for (uint k = 0; k < BLOCK_SIZE; k++) {
                sg.store(get_accessor_pointer(marr) + (ai + k) * N + aj, tcol[k]);
            }
        });
});
```

This kernel transposes a 16 x 16 matrix. It looks more complicated than the previous examples, but the idea is simple: a sub-group loads a 16 x 16 sub-matrix, then the sub-matrix is transposed using the sub-group shuffle functions. There is only one sub-matrix and the sub-matrix is the matrix so only one sub-group is needed. A bigger matrix, say 4096 x 4096, can be transposed using the same technique: each sub-group loads a sub-matrix, then the sub-matrices are transposed using the sub-group shuffle functions. This is left to the reader as an exercise.

SYCL has multiple variants of sub-group shuffle functions available. Each variant is optimized for its specific purpose on specific devices. It is always a good idea to use these optimized functions (if they fit your needs) instead of creating your own.
