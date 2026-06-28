## The output will be:

```vba
Device: Intel(R) Gen12HP
globalId = 0 groupId = 0 sgGroupId = 0 sgId = 0 sqSize = 32
globalId = 1 groupId = 0 sgGroupId = 0 sgId = 1 sqSize = 32
globalId = 2 groupId = 0 sgGroupId = 0 sgId = 2 sqSize = 32
globalId = 3 groupId = 0 sgGroupId = 0 sgId = 3 sqSize = 32
globalId = 4 groupId = 0 sgGroupId = 0 sgId = 4 sqSize = 32
globalId = 5 groupId = 0 sgGroupId = 0 sgId = 5 sqSize = 32
globalId = 6 groupId = 0 sgGroupId = 0 sgId = 6 sqSize = 32
globalId = 7 groupId = 0 sgGroupId = 0 sgId = 7 sqSize = 32
globalId = 8 groupId = 0 sgGroupId = 0 sgId = 8 sqSize = 32
globalId = 9 groupId = 0 sgGroupId = 0 sgId = 9 sqSize = 32
globalId = 10 groupId = 0 sgGroupId = 0 sgId = 10 sqSize = 32
globalId = 11 groupId = 0 sgGroupId = 0 sgId = 11 sqSize = 32
globalId = 12 groupId = 0 sgGroupId = 0 sgId = 12 sqSize = 32
globalId = 13 groupId = 0 sgGroupId = 0 sgId = 13 sqSize = 32
globalId = 14 groupId = 0 sgGroupId = 0 sgId = 14 sqSize = 32
globalId = 15 groupId = 0 sgGroupId = 0 sgId = 15 sqSize = 32
globalId = 16 groupId = 0 sgGroupId = 0 sgId = 16 sqSize = 32
globalId = 17 groupId = 0 sgGroupId = 0 sgId = 17 sqSize = 32
globalId = 18 groupId = 0 sgGroupId = 0 sgId = 18 sqSize = 32
globalId = 19 groupId = 0 sgGroupId = 0 sgId = 19 sqSize = 32
globalId = 20 groupId = 0 sgGroupId = 0 sgId = 20 sqSize = 32
globalId = 21 groupId = 0 sgGroupId = 0 sgId = 21 sqSize = 32
globalId = 22 groupId = 0 sgGroupId = 0 sgId = 22 sqSize = 32
globalId = 23 groupId = 0 sgGroupId = 0 sgId = 23 sqSize = 32
globalId = 24 groupId = 0 sgGroupId = 0 sgId = 24 sqSize = 32
globalId = 25 groupId = 0 sgGroupId = 0 sgId = 25 sqSize = 32
globalId = 26 groupId = 0 sgGroupId = 0 sgId = 26 sqSize = 32
globalId = 27 groupId = 0 sgGroupId = 0 sgId = 27 sqSize = 32
globalId = 28 groupId = 0 sgGroupId = 0 sgId = 28 sqSize = 32
globalId = 29 groupId = 0 sgGroupId = 0 sgId = 29 sqSize = 32
globalId = 30 groupId = 0 sgGroupId = 0 sgId = 30 sqSize = 32
globalId = 31 groupId = 0 sgGroupId = 0 sgId = 31 sqSize = 32
```

The valid sub-group sizes are device dependent. You can query the device to get this information:

```cpp
std::cout << "Sub-group Sizes: ";
for (const auto &s :
    q.get_device().get_info<sycl::info::device::sub_group_sizes>()) {
    std::cout << s << " ";
}
std::cout << std::endl;
```

The valid sub-group sizes supported may be:

```txt
Device: Intel(R) Gen12HP
Subgroup Sizes: 8 16 32
```

Next, we will show how to use sub-groups to improve performance.

## Vectorization and Memory Access

The Intel<sup>®</sup> graphics device has multiple VEs. Each VE is a multithreaded SIMD processor. The compiler generates SIMD instructions to pack multiple work-items in a sub-group to execute simultaneously in a VE thread. The SIMD width (thus the sub-group size), selected by the compiler is based on device characteristics and heuristics, or requested explicitly by the kernel, and can be 8, 16, or 32.

Given a SIMD width, maximizing SIMD lane utilization gives optimal instruction performance. If one or more lanes (or kernel instances or work items) diverge, the thread executes both branch paths before the paths merge later, increasing the dynamic instruction count. SIMD divergence negatively impacts performance. The compiler works to minimize divergence, but it helps to avoid divergence in the source code, if possible.

How memory is accessed in work-items affects how memory is accessed in the sub-group or how the SIMD lanes are utilized. Accessing contiguous memory in a work-item is often not optimal. For example:

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([\&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N / 16}, sycl::range{32}),
            [=](sycl::nd_item<1> it) {
                int i = it.get_global_linear_id();
                i = i * 16;
                for (int j = i; j < (i + 16); j++) {
                    data[j] = -1;
                }
            });
});
q.wait();
```

This simple kernel initializes an array of 1024 x 1024 integers. Each work-item initializes 16 contiguous integers. Assuming the sub-group size chosen by the compiler is 16, 256 integers are initialized in each subgroup or thread. However, the stores in 16 SIMD lanes are scattered.

Instead of initializing 16 contiguous integers in a work-item, initializing 16 contiguous integers in one SIMD instruction is more efficient.

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([\&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N / 16}, sycl::range{32}),
            [=](sycl::nd_item<1> it) {
                int i = it.get_global_linear_id();
                auto sg = it.get_sub_group();
                int sgSize = sg.get_local_range()[0];
                i = (i / sgSize) * sgSize * 16 + (i % sgSize);
                for (int j = 0; j < sgSize * 16; j += sgSize) {
                    data[i + j] = -1;
                }
            });
});
```

We use memory writes in our examples, but the same technique is applicable to memory reads as well.

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
memset(data2, 0xFF, sizeof(int) * N);
```

```cpp
auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N / 16}, sycl::range{32}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            i = i * 16;
            for (int j = i; j < (i + 16); j++) {
                data[j] = data2[j];
            }
        });
});
```

This kernel copies an array of 1024 x 1024 integers to another integer array of the same size. Each work item copies 16 contiguous integers. However, the reads from data2 are gathered and stores to data are scattered. It will be more efficient to change the code to read and store contiguous integers in each subgroup instead of each work-item.

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
                i = (i / sgSize) * sgSize * 16 + (i % sgSize);
                for (int j = 0; j < sgSize * 16; j += sgSize) {
                    data[i + j] = data2[i + j];
                }
            });
});
```

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

## Data Sharing
