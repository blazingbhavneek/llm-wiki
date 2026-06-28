
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

## Sub-Group Size vs. Maximum Sub-Group Size

So far in our examples, the work-group size is divisible by the sub-group size and both the work-group size and the sub-group size (either required by the user or automatically picked by the compiler are powers of two). The sub-group size and maximum sub-group size are the same if the work-group size is divisible by the maximum sub-group size and both sizes are powers of two. But what happens if the work-group size is not divisible by the sub-group size? Consider the following example:

```rust
auto e = q.submit([&](auto &h) {
    sycl::stream out(65536, 128, h);
    h.parallel_for(sycl::nd_range<1>(7, 7),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
        int i = it.get_global_linear_id();
        auto sg = it.get_sub_group();
        int sgSize = sg.get_local_range()[0];
        int sgMaxSize = sg.get_max_local_range()[0];
        int sId = sg.get_local_id()[0];
        int j = data[i];
        int k = data[i + sgSize];
        out << "globalId = " << i << " sgMaxSize = " << sgMaxSize
            << " sgSize = " << sgSize << " sId = " << sId
            << " j = " << j << " k = " << k << sycl::endl;
        });
});
q.wait();
```

The output of this example looks like this:

```lua
globalId = 0 sgMaxSize = 16 sgSize = 7 sId = 0 j = 0 k = 7
globalId = 1 sgMaxSize = 16 sgSize = 7 sId = 1 j = 1 k = 8
globalId = 2 sgMaxSize = 16 sgSize = 7 sId = 2 j = 2 k = 9
globalId = 3 sgMaxSize = 16 sgSize = 7 sId = 3 j = 3 k = 10
globalId = 4 sgMaxSize = 16 sgSize = 7 sId = 4 j = 4 k = 11
globalId = 5 sgMaxSize = 16 sgSize = 7 sId = 5 j = 5 k = 12
globalId = 6 sgMaxSize = 16 sgSize = 7 sId = 6 j = 6 k = 13
```

The sub-group size is seven, though the maximum sub-group size is still 16! The maximum sub-group size is actually the SIMD width so it does not change, but there are less than eight work-items in the sub-group, so the sub-group size is seven. So be careful when your work-group size is not divisible by the maximum subgroup size. The last sub-group with fewer work-items may need to be specially handled.

## Removing Conditional Checks

In Sub-Groups and SIMD Vectorization, we learned that SIMD divergence can negatively affect performance. If all work items in a sub-group execute the same instruction, the SIMD lanes are maximally utilized. If one or more work items take a divergent path, then both paths have to be executed before they merge.

Divergence is caused by conditional checks, though not all conditional checks cause divergence. Some conditional checks, even when they do not cause SIMD divergence, can still be performance hazards. In general, removing conditional checks can help performance.

## Padding Buffers to Remove Conditional Checks

Look at the convolution example from Shared Local Memory:

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

        oacc[i] = t;
    });
});
```

The nested if-then-else conditional checks are necessary to take care of the first and last 128 elements in the input so indexing will not run out of bounds. If we pad enough 0s before and after the input array, these conditional checks can be safely removed:

```cpp
std::vector<int> input(N + M / 2 + M / 2);
std::vector<int> output(N);
std::vector<int> kernel(M);

srand(2009);
for (size_t i = M / 2; i < N + M / 2; ++i) {
```

```cpp
input[i] = rand();
}

for (size_t i = 0; i < M / 2; ++i) {
    input[i] = 0;
    input[i + N + M / 2] = 0;
}

for (size_t i = 0; i < M; ++i) {
    kernel[i] = rand();
}

{
    sycl::buffer<int> ibuf(input.data(), N + M / 2 + M / 2);
    sycl::buffer<int> obuf(output.data(), N);
    sycl::buffer<int> kbuf(kernel.data(), M);

    auto e = q.submit([&](auto &h) {
        sycl::accessor iacc(ibuf, h, sycl::read_only);
        sycl::accessor oacc(obuf, h);
        sycl::accessor kacc(kbuf, h, sycl::read_only);

        h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{256}),
            [=](sycl::nd_item<1> it) {
                int i = it.get_global_linear_id();
                int t = 0;

                for (size_t j = 0; j < M; ++j) {
                    t += iacc[i + j] * kacc[j];
                }

                oacc[i] = t;
            });
    });
    q.wait();

    size_t kernel_ns = (e.template get_profiling_info<
                        sycl::info::event_profiling::command_end>() -
                        e.template get_profiling_info<
                            sycl::info::event_profiling::command_start>());
    std::cout << "Kernel Execution Time Average: total = " << kernel_ns * 1e-6
           << " msec" << std::endl;
}
```

## Replacing Conditional Checks with Relational Functions

Another way to remove conditional checks is to replace them with relational functions, especially built-in relational functions. It is strongly recommended to use a built-in function if one is available. SYCL provides a rich set of built-in relational functions like select(), min(), max(). In many cases you can use these functions to replace conditional checks and achieve better performance.

Consider the convolution example again. The if-then-else conditional checks can be replaced with built-in functions min() and max().

```cpp
sycl::buffer<int> ibuf(input.data(), N);
sycl::buffer<int> obuf(output.data(), N);
sycl::buffer<int> kbuf(kernel.data(), M);
```

```cpp
auto e = q.submit([&](auto &h) {
    sycl::accessor iacc(ibuf, h, sycl::read_only);
    sycl::accessor oacc(obuf, h);
    sycl::accessor kacc(kbuf, h, sycl::read_only);

    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{256}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            int t = 0;
            int startj = sycl::max<int>(M / 2 - i, 0);
            int endj = sycl::min<int>(M / 2 + N - i, M);
            int startk = sycl::max<int>(i - M / 2, 0);
            for (int j = startj, k = startk; j < endj; j++, k++) {
                t += iacc[k] * kacc[j];
            }
            oacc[i] = t;
        });
});
```
