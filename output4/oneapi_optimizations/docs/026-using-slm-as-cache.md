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
