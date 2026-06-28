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
