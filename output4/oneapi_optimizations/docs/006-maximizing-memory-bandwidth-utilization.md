## Maximizing Memory Bandwidth Utilization

Each work item in the above example loads and stores 1 integer or 4 bytes in every loop iteration(data[i + j] = data2[i + j];), or each vectorized memory operation loads/stores 64 bytes(assuming sub-group size 16), leaving the memory bandwidth unsaturated.

Increasing the payload or the size of data each work item loads or stores in one memory operation will result in better bandwidth utilization.

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N / 16}, sycl::range{32}),
        [=](sycl::nd_item<1> it) {
        int i = it.get_global_linear_id();
        auto sg = it.get_sub_group();
        int sgSize = sg.get_local_range()[0];
        i = (i / sgSize) * sgSize * 16 + (i % sgSize) * 4;
        for (int j = 0; j < 4; j++) {
            sycl::vec<int, 4> x;
            sycl::vec<int, 4> *q =
```

```cpp
(sycl::vec<int, 4> *)(&(data2[i + j * sgSize * 4]));
    x = *q;
    sycl::vec<int, 4> *r =
        (sycl::vec<int, 4> *)(&(data[i + j * sgSize * 4]));
    *r = x;
}
});
```

Each work item loads/stores a sycl::vec<int, 4> instead of an integer in every loop iteration. Reading/ writing 256 contiguous bytes(assuming sub-group size 16) of memory, the payload of every vectorized memory operation is quadrupled.

The maximum bandwidth is different from hardware to hardware. One can use Intel<sup>®</sup> VTune Profiler to measure the bandwidth and find the optimal size.

Using a vector type, however, can potentially increase register pressure. It is advised to use long vectors only if registers do not spill. Please refer to the chapter “Registerization and Avoiding Register Spills” for techniques for avoiding register spills.

## Memory Block Load and Store

Intel<sup>®</sup> graphics have instructions optimized for memory block loads/stores. So if work-items in a sub-group access a contiguous block of memory, you can use the sub-group block access functions to take advantage of the block load/store instructions.

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N / 16}, sycl::range{32}),
            [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
        auto sg = it.get_sub_group();
        sycl::vec<int, 8> x;

        int base =
            (it.get_group(0) * 32 +
            sg.get_group_id()[0] * sg.get_local_range()[0]) *
            16;

        x = sg.load<8>(get_multi_ptr(&(data2[base + 0)])));
        sg.store<8>(get_multi_ptr(&(data[base + 0])), x);
        x = sg.load<8>(get_multi_ptr(&(data2[base + 128]])));
        sg.store<8>(get_multi_ptr(&(data[base + 128])), x);
    });
});
```

This example also uses sycl::vec for performance, the integers in x, however, are not contiguous in memory, but with a stride of the sub-group size!

You may have noticed that the sub-group size 16 was explicitly requested. When you use sub-group functions, it is always good to override the compiler choice to make sure the sub-group size always matches what you expect.
