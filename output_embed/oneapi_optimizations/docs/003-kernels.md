## Kernels

A kernel is the unit of computation in the oneAPI offload model. By submitting a kernel on an iteration space, you are requesting that the computation be applied to the specified data objects.

In this section we cover topics related to the coding, submission, and execution of kernels.

• Sub-Groups and SIMD Vectorization

• Removing Conditional Checks

• Registers and Performance

• Shared Local Memory

• Pointer Aliasing and the Restrict Directive

• Synchronization among Threads in a Kernel

• Considerations for Selecting Work-Group Size

• Prefetch

• Reduction

• Kernel Launch

• Executing Multiple Kernels on the Device at the Same Time

• Submitting Kernels to Multiple Queues

• Avoiding Redundant Queue Constructions

• Programming Intel<sup>®</sup> XMX Using SYCL Joint Matrix Extension

• Doing I/O in the Kernel

• Optimizing Explicit SIMD Kernels

## Sub-Groups and SIMD Vectorization

The index space of an ND-Range kernel is divided into work-groups, sub-groups, and work-items. A workitem is the basic unit. A collection of work-items form a sub-group, and a collection of sub-groups form a work-group. The mapping of work-items and work-groups to hardware vector engines (VE) is implementation-dependent. All the work-groups run concurrently but may be scheduled to run at different times depending on availability of resources. Work-group execution may or or may not be preempted depending on the capabilities of underlying hardware. Work-items in the same work-group are guaranteed to run concurrently. Work-items in the same sub-group may have additional scheduling guarantees and have access to additional functionality.

A sub-group is a collection of contiguous work-items in the global index space that execute in the same VE thread. When the device compiler compiles the kernel, multiple work-items are packed into a sub-group by vectorization so the generated SIMD instruction stream can perform tasks of multiple work-items simultaneously. Properly partitioning work-items into sub-groups can make a big performance difference.

Let’s start with a simple example illustrating sub-groups:

```cpp
q.submit([&](auto &h) {
    sycl::stream out(65536, 256, h);
    h.parallel_for(sycl::nd_range(sycl::range{32}, sycl::range{32}),
        [=](sycl::nd_item<1> it) {
            int groupId = it.get_group(0);
            int globallId = it.get_global_linear_id();
            auto sg = it.get_sub_group();
            int sqSize = sg.get_local_range()[0];
            int sgGroupId = sg.get_group_id()[0];
            int sgId = sg.get_local_id()[0];
```

```typescript
out << "globalId = " << sycl::setw(2) << globalId
            << " groupId = " << groupId
            << " sgGroupId = " << sgGroupId << " sgiId = " << sgiId
            << " sgSize = " << sycl::setw(2) << sgiSize
            << sycl::endl;
        });
});
```

The output of this example may look like this:

```vba
Device: Intel(R) Gen12HP
globalId = 0 groupId = 0 sgGroupId = 0 sgId = 0 sgSize = 16
globalId = 1 groupId = 0 sgGroupId = 0 sgId = 1 sgSize = 16
globalId = 2 groupId = 0 sgGroupId = 0 sgId = 2 sgSize = 16
globalId = 3 groupId = 0 sgGroupId = 0 sgId = 3 sgSize = 16
globalId = 4 groupId = 0 sgGroupId = 0 sgId = 4 sgSize = 16
globalId = 5 groupId = 0 sgGroupId = 0 sgId = 5 sgSize = 16
globalId = 6 groupId = 0 sgGroupId = 0 sgId = 6 sgSize = 16
globalId = 7 groupId = 0 sgGroupId = 0 sgId = 7 sgSize = 16
globalId = 16 groupId = 0 sgGroupId = 1 sgId = 0 sgSize = 16
globalId = 17 groupId = 0 sgGroupId = 1 sgId = 1 sgSize = 16
globalId = 18 groupId = 0 sgGroupId = 1 sgId = 2 sgSize = 16
globalId = 19 groupId = 0 sgGroupId = 1 sgId = 3 sgSize = 16
globalId = 20 groupId = 0 sgGroupId = 1 sgId = 4 sgSize = 16
globalId = 21 groupId = 0 sgGroupId = 1 sgId = 5 sgSize = 16
globalId = 22 groupId = 0 sgGroupId = 1 sgId = 6 sgSize = 16
globalId = 23 groupId = 0 sgGroupId = 1 sgId = 7 sgSize = 16
globalId = 8 groupId = 0 sgGroupId = 0 sgId = 8 sgSize = 16
globalId = 9 groupId = 0 sgGroupId = 0 sgId = 9 sgSize = 16
globalId = 10 groupId = 0 sgGroupId = 0 sgId = 10 sgSize = 16
globalId = 11 groupId = 0 sgGroupId = 0 sgId = 11 sgSize = 16
globalId = 12 groupId = 0 sgGroupId = 0 sgId = 12 sgSize = 16
globalId = 13 groupId = 0 sgGroupId = 0 sgId = 13 sgSize = 16
globalId = 14 groupId = 0 sgGroupId = 0 sgId = 14 sgSize = 16
globalId = 15 groupId = 0 sgGroupId = 0 sgId = 15 sgSize = 16
globalId = 24 groupId = 0 sgGroupId = 1 sgId = 8 sgSize = 16
globalId = 25 groupId = 0 sgGroupId = 1 sgId = 9 sgSize = 16
globalId = 26 groupId = 0 sgGroupId = 1 sgId = 10 sgSize = 16
globalId = 27 groupId = 0 sgGroupId = 1 sgId = 11 sgSize = 16
globalId = 28 groupId = 0 sgGroupId = 1 sgId = 12 sgSize = 16
globalId = 29 groupId = 0 sgGroupId = 1 sgId = 13 sgSize = 16
globalId = 30 groupId = 0 sgGroupId = 1 sgId = 14 sgSize = 16
globalId = 31 groupId = 0 sgGroupId = 1 sgId = 15 sgSize = 16
```

Each sub-group in this example has 16 work-items, or the sub-group size is 16. This means each thread simultaneously executes 16 work-items and 32 work-items are executed by two VE threads.

By default, the compiler selects a sub-group size using device-specific information and a few heuristics. The user can override the compiler’s selection using the kernel attribute intel::reqd\_sub\_group\_size to specify the maximum sub-group size. Sometimes, not always, explicitly requesting a sub-group size may help performance.

```cpp
q.submit([&](auto &h) {
    sycl::stream out(65536, 256, h);
    h.parallel_for(sycl::nd_range(sycl::range{32}, sycl::range{32}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(32)]] {
            int groupId = it.get_group(0);
            int globallId = it.get_global_linear_id();
            auto sg = it.get_sub_group();
            int sgSize = sg.get_local_range()[0];
```

```txt
int sgGroupId = sg.get_group_id()[0];
int sgId = sg.get_local_id()[0];

out << "globalId = " << sycl::setw(2) << globalId
    << " groupId = " << groupId
    << " sgGroupId = " << sgGroupId << " sgId = " << sgId
    << " sgSize = " << sycl::setw(2) << sgSize
    << sycl::endl;
});
```

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
