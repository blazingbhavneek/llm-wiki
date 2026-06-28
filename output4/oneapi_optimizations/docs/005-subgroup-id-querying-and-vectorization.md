
The kernel VectorAdd4 is similar to the kernel VectorAdd3 above except that it has a barrier synchronization at the beginning and end of the kernel execution. This barrier is functionally not needed, but will significantly impact the way in which threads are scheduled on the hardware.

```cpp
template <int groups, int wg_size, int sg_size>
int VectorAdd4(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum, int iter) {
  sycl::range num_items{a.size()};

  sycl::buffer a_buf(a);
  sycl::buffer b_buf(b);
  sycl::buffer sum_buf(sum.data(), num_items);
  size_t num_groups = groups;
  auto start = std::chrono::steady_clock::now();
  q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(
      sycl::nd_range<1>(num_groups * wg_size, wg_size),
      [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(sg_size)]]
        index.barrier(sycl::access::fence_space::local_space);
        size_t grp_id = index.get_group()[0];
        size_t loc_id = index.get_local_id();
        size_t start = grp_id * mysize;
        size_t end = start + mysize;
        for (int j = 0; j < iter; j++) {
          for (size_t i = start + loc_id; i < end; i += wg_size) {
            sum_acc[i] = a_acc[i] + b_acc[i];
          }
        }
      });
  });
  q.wait();
  auto end = std::chrono::steady_clock::now();
  std::cout << "VectorAdd4<" << groups << "> completed on device - took "
              << (end - start).count() << " u-secs\n";
  return ((end - start).count());
} // end VectorAdd4
```

To show how threads are scheduled, the above two kernels are called with 8 work-groups, sub-group size of 8 and work-group size of 320 as shown below. Based on the choice of work-group size and sub-group size, 40 threads per work-group need to be scheduled by the hardware.

```c
Initialize(sum);
VectorAdd3<8, 320, sgsize>(q, a, b, sum, 10000);
Initialize(sum);
VectorAdd4<8, 320, sgsize>(q, a, b, sum, 10000);
```

The chart from VTune below shows that the measured GPU occupancy for VectorAdd3 and VectorAdd4 kernels.

## GPU Occupancy for VectorAdd3 and VectorAdd4 Kernels

![](images/d49315cd99bc0294fb29602c428207419347e8e4f5d1bee2f4c2a95260fad57e.jpg)

For the VectorAdd3 kernel, there are two phases for occupancies: 33.3% (224 threads occupancy) and 14.3% (96 threads occupancy) on a TGL machine that has a total of 672 threads. Since there are a total of eight work-groups, with each work-group having 40 threads, there are two X<sup>e</sup>-cores (each of which have 112 threads) into which the threads of six work-groups are scheduled. This means that 40 threads each from four work-groups are scheduled, and 32 threads each from two other work-groups are scheduled in the first phase. Then in the second phase, 40 threads from the remaining two work-groups are scheduled for execution.

As seen in the VectorAdd4 kernel, there are three phases of occupancies: 45.3% (304 threads), 39.3% (264 threads), and 11.9% (80 threads). In the first phase, all eight work-groups are scheduled together on 3 X<sup>e</sup>-cores, with two X<sup>e</sup>-cores getting 112 threads each (80 from two work-groups and 32 from one workgroup) and one X<sup>e</sup>-core getting 80 threads (from two work-groups). In the second phase, one work-group completed execution, which gives us occupancy of (304-40=264). In the last phase, the remaining eight threads of two work-groups are scheduled and these complete the execution.

The same kernels as above when run with a work-group size that is a multiple of the number of threads in a X<sup>e</sup>-core and lot more work-groups gets good utilization of the hardware achieving close to 100% occupancy, as shown below.

```c
Initialize(sum);
VectorAdd3<24, 224, sgsize>(q, a, b, sum, 10000);
Initialize(sum);
VectorAdd4<24, 224, sgsize>(q, a, b, sum, 10000);
```

This kernel execution has a different thread occupancy since we have many more threads and also the workgroup size is a multiple of the number of threads in a X<sup>e</sup>-core. This is shown below in the thread occupancy metric on the VTune timeline.

## Thread Occupancy Metric in VTune

![](images/680b6f85b333c6e83ab78707fe0af4cf21b91f9edfa3f171e1574eee8d44fd4f.jpg)

Note that the above schedule is a guess based on the different occupancy numbers, since we do not yet have a way to examine the per slice based occupancy numbers.

You can run different experiments with the above kernels to gain better understanding of how the GPU hardware schedules the software threads on the Execution Units. Be careful about the work-group and subgroup sizes, in addition to a large number of work-groups, to ensure effective utilization of the GPU hardware.

## Intel<sup>®</sup> GPU Occupancy Calculator

In summary, a SYCL work-group is typically dispatched to an X<sup>e</sup>-core. All the work-items in a work-group share the same SLM of an X<sup>e</sup>-core for intra work-group thread barriers and memory fence synchronization. Multiple work-groups can be dispatched to the same X<sup>e</sup>-core if there are sufficient VE ALUs, SLM, and thread contexts to accommodate them.

You can achieve higher performance by fully utilizing all available X<sup>e</sup>-cores. Parameters affecting a kernel’s GPU occupancy are work-group size and SIMD sub-group size, which also determines the number of threads in the work-group.

The Intel® GPU Occupancy Calculator can be used to calculate the occupancy on an Intel<sup>®</sup> GPU for a given kernel, and its work-group parameters.

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
