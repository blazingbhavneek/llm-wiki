## Thread Mapping and GPU Occupancy

The SYCL execution model exposes an abstract view of GPU execution. The SYCL thread hierarchy consists of a 1-, 2-, or 3-dimensional grid of work-items. These work-items are grouped into equal sized thread groups called work-groups. Threads in a work-group are further divided into equal sized vector groups called subgroups (see the illustration that follows).

Work-item A work-item represents one of a collection of parallel executions of a kernel.

Sub-group A sub-group represents a short range of consecutive work-items that are processed together as a SIMD vector of length 8, 16, 32, or a multiple of the native vector length of a CPU with Intel<sup>®</sup> UHD Graphics.

Work-group A work-group is a 1-, 2-, or 3-dimensional set of threads within the thread hierarchy. In SYCL, synchronization across work-items is only possible with barriers for the work-items within the same work-group.

## nd\_range

An nd\_range divides the thread hierarchy into 1-, 2-, or 3-dimensional grids of work-groups. It is represented by the global range, the local range of each work-group.

## Thread Hierarchy

![](images/14acddaf2ae319de26714b79e1a70009e3656312d34fa70115cf9e485a53ab76.jpg)  
The diagram above illustrates the relationship among ND-Range, work-group, sub-group, and work-item.

## Thread Synchronization

SYCL provides two synchronization mechanisms that can be called within a kernel function. Both are only defined for work-items within the same work-group. SYCL does not provide any global synchronization mechanism inside a kernel for all work-items across the entire nd\_range.

• \`\`mem\_fence\`\` inserts a memory fence on global and local memory access across all work-items in a work-group.

• \`\`barrier\`\` inserts a memory fence and blocks the execution of all work-items within the work-group until all work-items have reached its location.

## Mapping Work-Groups to $\mathsf { x e } .$ -cores for Maximum Occupancy

The rest of this chapter explains how to pick a proper work-group size to maximize the occupancy of the GPU resources. The example system is the Tiger Lake processors with X<sup>e</sup>-LP GPU as the execution target. The examples also use the new terminologies X<sup>e</sup>-core (XC) for Dual Subslice, and $\mathsf { X } ^ { \mathsf { e } }$ Vector Engine (XVE) for Execution Unit.

We will use the architecture parameters for X<sup>e</sup>-LP Graphics (TGL) GPU summarized below:

X<sup>e</sup>-LP (TGL) GPU

<table><tr><td></td><td>VEs</td><td>Threads</td><td>Operations</td><td>Maximum Work-Group Size</td></tr><tr><td>Each Xe-core</td><td>16</td><td>7 × 16 = 112</td><td>112 × 8 = 896</td><td>512</td></tr><tr><td>Total</td><td>16 × 6 = 96</td><td>112 × 6 = 672</td><td>896 × 6 = 5376</td><td>512</td></tr></table>

The maximum work-group size is a constraint imposed by the hardware and GPU driver. You can query the maximum work-group size using  
device::get\_info<cl::sycl::info::device::max\_work\_group\_size>() function.

Let’s start with a simple kernel:

```rust
auto command_group =
    [&](auto &cgh) {
        cgh.parallel_for(sycl::range<3>(64, 64, 64), // global range
                [=](item<3> it) {
                    // (kernel code)
                })
    }
```

This kernel contains 262,144 work-items structured as a 3D range of . It leaves the workgroup and sub-group size selection to the compiler. To fully utilize the 5376 parallel operations available in the GPU slice, the compiler must choose a proper work-group size.

The two most important GPU resources are:

• Thread Contexts:: The kernel should have a sufficient number of threads to utilize the GPU’s thread contexts.

• SIMD Units and SIMD Registers:: The kernel should be organized to vectorize the work-items and utilize the SIMD registers.

In a SYCL kernel, the programmer can affect the work distribution by structuring the kernel with proper work-group size, sub-group size, and organizing the work-items for efficient vector execution. Writing efficient vector kernels is covered in a separate section. This chapter focuses on work-group and sub-group size selection.

Thread contexts are easier to utilize than SIMD vector. Therefore, start with selecting the number of threads in a work-group. Each X<sup>e</sup>-core has 112 thread contexts, but usually you cannot use all the threads if the kernel is also vectorized by 8 ( ). From this, we can derive that the maximum number of threads in a work-group is 64 (512 / 8).

SYCL does not provide a mechanism to directly set the number of threads in a work-group. However, you can use work-group size and sub-group size to set the number of threads:

$$
\text {Work - groupsize} = \text {Threads} \times \text {Sub - groupSize}
$$

You can increase the sub-group size as long as there are a sufficient number of registers for the kernel after widening. Note that each VE has 128 SIMD8 registers so there is a lot of room for widening on simple kernels. The effect of increasing sub-group size is similar to loop unrolling: while each VE still executes eigh 32-bit operations per cycle, the amount of work per work-group interaction is doubled/quadrupled. In SYCL, a programmer can explicitly specify sub-group size using intel::reqd\_sub\_group\_size({8|16|32}) to override the compiler’s selection.

The table below summarizes the selection criteria of threads and sub-group sizes to keep all GPU resources occupied for a Intel Iris X<sup>e</sup>-LP GPU:

Configurations to ensure full occupancy

<table><tr><td>Maximum Threads</td><td>Minimum Sub-group Size</td><td>Maximum Sub-group Size</td><td>Maximum Work-group Size</td><td>Constraint</td></tr><tr><td>64</td><td>8</td><td>32</td><td>512</td><td>Threads × Sub - groupSize</td></tr></table>

In general, choosing a larger work-group size has the advantage of reducing the number of rounds of workgroup dispatching. Increasing sub-group size can reduce the number of threads required for a work-group at the expense of longer latency and higher register pressure for each sub-group execution.

Impact of Work-item Synchronization within Work-group

Let’s look at a kernel requiring work-item synchronization:

```cpp
auto command_group =
    [&](auto &cgh) {
        cgh.parallel_for(nd_range(sycl::range(64, 64, 128), // global range
                             sycl::range(1, R, 128)      // local range
                            ),
        [=](sycl::nd_item<3> item) {
            // (kernel code)
            // Internal synchronization
            item.barrier(access::fence_space::global_space);
            // (kernel code)
        })
    }
```

This kernel is similar to the previous example, except it requires work-group barrier synchronization. Workitem synchronization is only available to work-items within the same work-group. You must pick a workgroup local range using nd\_range and nd\_item. All the work-items of a work-group must be allocated to the same X<sup>e</sup>-core, which affects X<sup>e</sup>-core occupancy and kernel performance.

In this kernel, the local range of work-group is given as range(1, R, 128). Assuming the sub-group size is eight, let’s look at how the values of variable R affect VE occupancy. In the case of R=1, the local group range is (1, 1, 128) and work-group size is 128. The X<sup>e</sup>-core allocated for a work-group contains only 16 threads out of 112 available thread contexts (i.e., very low occupancy). However, the system can dispatch 7 workgroups to the same X<sup>e</sup>-core to reach full occupancy at the expense of a higher number of dispatches.

In the case of R>4, the work-group size will exceed the system-supported maximum work-group size of 512, and the kernel will fail to launch. In the case of R=4, an X<sup>e</sup>-core is only 57% occupied (4/7) and the three unused thread contexts are not sufficient to accommodate another work-group, wasting 43% of the available VE capacities. Note that the driver may still be able to dispatch a partial work-group to an unused X<sup>e</sup>-core. However, because of the barrier in the kernel, the partially dispatched work items would not be able to pass the barriers until the rest of the work-group is dispatched. In most cases, the kernel’s performance would not benefit much from the partial dispatch. Hence, it is important to avoid this problem by properly choosing the work-group size.

The table below summarizes the tradeoffs between group size, number of threads, X<sup>e</sup>-core utilization, and occupancy.

Utilization for various configurations

<table><tr><td>Work-items</td><td>Group Size</td><td>Threads</td><td> $X^{e}$ -coreUtilization</td><td> $X^{e}$ -coreOccupancy</td></tr><tr><td colspan="2">64 × 64 × 128 = 524(R=1) 128</td><td>16</td><td>16/112 = 14%</td><td>100% with 7 work-groups</td></tr></table>

```txt
Work-items Group Size Threads Xe-core Utilization Xe-core Occupancy
64 × 64 × 128 = 524888 (R=2) 128 × 2 2 × 16 = 32 32/112 = 28.6% 86% with 3 work-groups
64 × 64 × 128 = 524888 (R=3) 128 × 4 3 × 16 = 48 48/112 = 42.9% 86% with 2 work-groups
64 × 64 × 128 = 524888 (R=4) 128 × 4 4 × 16 = 64 64/112 = 57% 57% maximum
64 × 64 × 128 = 524888 (R>4) 640+ Fail to launch
```

## Impact of Local Memory Within Work-group

Let’s look at an example where a kernel allocates local memory for a work-group:

```rust
auto command_group =
    [&](auto &cgh) {
        // local memory variables shared among work items
        sycl::accessor<int, 1, sycl::access::mode::read_write,
                sycl::access::target::local>
            myLocal(sycl::range(R), cgh);
        cgh.parallel_for(nd_range(sycl::range<3>(64, 64, 128), // global range
                    sycl::range<3>(1, R, 128)      // local range
                ),
            [=](ngroup<3> myGroup) {
                // (work group code)
                myLocal[myGroup.get_local_id()[1]] = ...
            })
        }
```

Because work-group local variables are shared among its work-items, they are allocated in a X<sup>e</sup>-core’s SLM. Therefore, this work-group must be allocated to a single X<sup>e</sup>-core, same as the intra-group synchronization. In addition, you must also weigh the sizes of local variables under different group size options such that the local variables fit within an X<sup>e</sup>-core’s 128KB SLM capacity limit.

## A Detailed Example

Before concluding this section, let’s look at the hardware occupancies from the variants of a simple vector add example. Using Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> graphics from TGL platform as the underlying hardware with the resource parameters specified.

```cpp
auto d_selector = sycl::default_selector_v;

// Array type and data size for this example.
constexpr size_t array_size = 3 * 5 * 7 * (1 << 17);
typedef std::array<int, array_size> IntArray;

#define mysize (1 << 17)

int VectorAdd1(sycl::queue &q, const IntArray &a, const IntArray &b,
                   IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
```

```cpp
auto start = std::chrono::steady_clock::now();
auto e = q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto i) {
        for (int j = 0; j < iter; j++)
            sum_acc[i] = a_acc[i] + b_acc[i];
    });
});
q.wait();
auto end = std::chrono::steady_clock::now();
return ((end - start).count());
} // end VectorAdd1

template <int groups>
int VectorAdd2(sycl::queue &q, const IntArray &a, const IntArray &b,
                   IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = groups;
    size_t wg_size = 512;
    // get the max wg_sie instead of 512 size_t wg_size = 512;
    auto start = std::chrono::steady_clock::now();
    q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(
            sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(32)]] {
                size_t grp_id = index.get_group()[0];
                size_t loc_id = index.get_local_id();
                size_t start = grp_id * mysize;
                size_t end = start + mysize;
                for (int j = 0; j < iter; j++)
                    for (size_t i = start + loc_id; i < end; i += wg_size) {
                        sum_acc[i] = a_acc[i] + b_acc[i];
                    }
                });
});
q.wait();
auto end = std::chrono::steady_clock::now();
return ((end - start).count());
} // end VectorAdd2

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++)
        a[i] = i;
```

```cpp
void Initialize(IntArray &a) {
  for (size_t i = 0; i < a.size(); i++)
    a[i] = 0;
}
IntArray a, b, sum;

int main() {

  sycl::queue q(d_selector);

  InitializeArray(a);
  InitializeArray(b);

  std::cout << "Running on device: "
           << q.get_device().get_info<sycl::info::device::name>() << "\n";
  std::cout << "Vector size: " << a.size() << "\n";

  // check results
  Initialize(sum);
  VectorAdd1(q, a, b, sum, 1);

  for (int i = 0; i < mysize; i++)
    if (sum[i] != 2 * i) {
      std::cout << "add1 Did not match\n";
    }

  Initialize(sum);
  VectorAdd2<1>(q, a, b, sum, 1);
  for (int i = 0; i < mysize; i++)
    if (sum[i] != 2 * i) {
      std::cout << "add2 Did not match\n";
    }

  // time the kernels
  std::stringstream ss;

  Initialize(sum);
  int t = VectorAdd1(q, a, b, sum, 1000);
  ss << "Execution times (u-secs) on "
       << q.get_device().get_info<sycl::info::device::name>()
       << " device:" << std::endl;
  ss << " VectorAdd1 : " << t << std::endl;
  Initialize(sum);
  t = VectorAdd2<1>(q, a, b, sum, 1000);
  ss << " VectorAdd2<1> : " << t << std::endl;
  t = VectorAdd2<2>(q, a, b, sum, 1000);
  ss << " VectorAdd2<2> : " << t << std::endl;
  t = VectorAdd2<3>(q, a, b, sum, 1000);
  ss << " VectorAdd2<3> : " << t << std::endl;
  t = VectorAdd2<4>(q, a, b, sum, 1000);
  ss << " VectorAdd2<4> : " << t << std::endl;
  t = VectorAdd2<5>(q, a, b, sum, 1000);
  ss << " VectorAdd2<5> : " << t << std::endl;
  t = VectorAdd2<6>(q, a, b, sum, 1000);
  ss << " VectorAdd2<6> : " << t << std::endl;
  t = VectorAdd2<7>(q, a, b, sum, 1000);
```

```cpp
ss << " VectorAdd2<7> : " << t << std::endl;
t = VectorAdd2<8>(q, a, b, sum, 1000);
ss << " VectorAdd2<8> : " << t << std::endl;
t = VectorAdd2<12>(q, a, b, sum, 1000);
ss << " VectorAdd2<12>: " << t << std::endl;
t = VectorAdd2<16>(q, a, b, sum, 1000);
ss << " VectorAdd2<16>: " << t << std::endl;
t = VectorAdd2<20>(q, a, b, sum, 1000);
ss << " VectorAdd2<20>: " << t << std::endl;
t = VectorAdd2<24>(q, a, b, sum, 1000);
ss << " VectorAdd2<24>: " << t << std::endl;
t = VectorAdd2<28>(q, a, b, sum, 1000);
ss << " VectorAdd2<28>: " << t << std::endl;
t = VectorAdd2<32>(q, a, b, sum, 1000);
ss << " VectorAdd2<32>: " << t << std::endl;

std::cout << ss.str();
return 0;
} // end of codeblock
```

The VectorAdd1 section of the program above lets the compiler select the work-group size and SIMD width. In this case, the compiler selects a work-group size of 512 and a SIMD width of 32 because the kernel’s register pressure is low.

```cpp
int VectorAdd2(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = groups;
    size_t wg_size = 512;
    // get the max wg_sie instead of 512 size_t wg_size = 512;
    auto start = std::chrono::steady_clock::now();
    q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(
            sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(32)]] {
                size_t grp_id = index.get_group()[0];
                size_t loc_id = index.get_local_id();
                size_t start = grp_id * mysize;
                size_t end = start + mysize;
                for (int j = 0; j < iter; j++)
                    for (size_t i = start + loc_id; i < end; i += wg_size) {
                        sum_acc[i] = a_acc[i] + b_acc[i];
                    }
                });
});
q.wait();
```

```cpp
auto end = std::chrono::steady_clock::now();
    return ((end - start).count());
} // end VectorAdd2
```

The VectorAdd2 example above explicitly specifies the work-group size of 512, SIMD width of 32, and a variable number of work-groups as a function parameter groups.

Dividing the number of threads by the number of available thread contexts in the GPU gives us an estimate of the GPU hardware occupancy. The following table calculates the GPU hardware occupancy using the TGL Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> architecture parameters for each of the above two kernels with various arguments.

Occupancy

<table><tr><td>Program Occupancy</td><td>Work-groups</td><td>Work-items</td><td>Work-group Size</td><td>SIMD</td><td>Threads Work-group</td><td>Threads</td><td>Occupancy</td></tr><tr><td>VectorAdd 1</td><td>53760</td><td>27.5M</td><td>512</td><td>32</td><td>16</td><td>860K</td><td>100%</td></tr><tr><td>VectorAdd 2&lt;1&gt;</td><td>1</td><td>512</td><td>512</td><td>32</td><td>16</td><td>16</td><td>16/672 = 2.4%</td></tr><tr><td>VectorAdd 2&lt;2&gt;</td><td>2</td><td>1024</td><td>512</td><td>32</td><td>16</td><td>32</td><td>32/672 = 4.8%</td></tr><tr><td>VectorAdd 2&lt;3&gt;</td><td>3</td><td>1536</td><td>512</td><td>32</td><td>16</td><td>48</td><td>48/672 = 7.1%</td></tr><tr><td>VectorAdd 2&lt;4&gt;</td><td>4</td><td>2048</td><td>512</td><td>32</td><td>16</td><td>64</td><td>64/672 = 9.5%</td></tr><tr><td>VectorAdd 2&lt;5&gt;</td><td>5</td><td>2560</td><td>512</td><td>32</td><td>16</td><td>80</td><td>80/672 = 11.9%</td></tr><tr><td>VectorAdd 2&lt;6&gt;</td><td>6</td><td>3072</td><td>512</td><td>32</td><td>16</td><td>96</td><td>96/672 = 14.3%</td></tr><tr><td>VectorAdd 2&lt;7&gt;</td><td>7</td><td>3584</td><td>512</td><td>32</td><td>16</td><td>112</td><td>112/672 = 16.7%</td></tr><tr><td>VectorAdd 2&lt;8&gt;</td><td>8</td><td>4096</td><td>512</td><td>32</td><td>16</td><td>128</td><td>128/672 = 19%</td></tr><tr><td>VectorAdd 2&lt;12&gt;</td><td>12</td><td>6144</td><td>512</td><td>32</td><td>16</td><td>192</td><td>192/672 = 28.6%</td></tr><tr><td>VectorAdd 2&lt;16&gt;</td><td>16</td><td>8192</td><td>512</td><td>32</td><td>16</td><td>256</td><td>256/672 = 38.1%</td></tr><tr><td>VectorAdd 2&lt;20&gt;</td><td>20</td><td>10240</td><td>512</td><td>32</td><td>16</td><td>320</td><td>320/672 = 47.7%</td></tr><tr><td>VectorAdd 2&lt;24&gt;</td><td>24</td><td>12288</td><td>512</td><td>32</td><td>16</td><td>384</td><td>384/672 = 57.1%</td></tr><tr><td>VectorAdd 2&lt;28&gt;</td><td>28</td><td>14336</td><td>512</td><td>32</td><td>16</td><td>448</td><td>448/672 = 66.7%</td></tr><tr><td>VectorAdd 2&lt;32&gt;</td><td>32</td><td>16384</td><td>512</td><td>32</td><td>16</td><td>512</td><td>512/672 = 76.2%</td></tr><tr><td>VectorAdd 2&lt;36&gt;</td><td>36</td><td>18432</td><td>512</td><td>32</td><td>16</td><td>576</td><td>576/672 = 85.7%</td></tr><tr><td>VectorAdd 2&lt;40&gt;</td><td>40</td><td>20480</td><td>512</td><td>32</td><td>16</td><td>640</td><td>640/672 = 95.2%</td></tr><tr><td>VectorAdd 2&lt;42&gt;</td><td>42</td><td>21504</td><td>512</td><td>32</td><td>16</td><td>672</td><td>672/672 = 100%</td></tr><tr><td>VectorAdd 2&lt;44&gt;</td><td>44</td><td>22528</td><td>512</td><td>32</td><td>16</td><td>704</td><td>100% then 4.7%</td></tr><tr><td>VectorAdd 2&lt;48&gt;</td><td>48</td><td>24576</td><td>512</td><td>32</td><td>16</td><td>768</td><td>100% then 14.3%</td></tr></table>

The following VTune analyzer chart for VectorAdd2 with various work-group sizes confirms the accuracy of our estimate. The numbers in the grid view vary slightly from the estimate because the grid view gives an average across the entire execution.

Occupancy for VectorAdd2 as Shown in VTune

<table><tr><td rowspan="2">Computing Task</td><td colspan="2">Work Size</td><td colspan="2"></td><td colspan="2">Computing</td></tr><tr><td>Global</td><td>Local</td><td>Total Time</td><td>Average Time</td><td>Time</td><td>Insta</td></tr><tr><td>[Outside any task]</td><td></td><td></td><td>0s</td><td></td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)1&gt;(int, cl::sycl::queue&amp;, std::a</td><td>512</td><td>512</td><td>0.046s</td><td>0.046s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)2&gt;(int, cl::sycl::queue&amp;, std::a</td><td>1024</td><td>512</td><td>0.056s</td><td>0.056s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)3&gt;(int, cl::sycl::queue&amp;, std::a</td><td>1536</td><td>512</td><td>0.080s</td><td>0.080s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)4&gt;(int, cl::sycl::queue&amp;, std::a</td><td>2048</td><td>512</td><td>0.087s</td><td>0.087s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)5&gt;(int, cl::sycl::queue&amp;, std::a</td><td>2560</td><td>512</td><td>0.089s</td><td>0.089s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)6&gt;(int, cl::sycl::queue&amp;, std::a</td><td>3072</td><td>512</td><td>0.094s</td><td>0.094s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)7&gt;(int, cl::sycl::queue&amp;, std::a</td><td>3584</td><td>512</td><td>0.101s</td><td>0.101s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)8&gt;(int, cl::sycl::queue&amp;, std::a</td><td>4096</td><td>512</td><td>0.111s</td><td>0.111s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)12&gt;(int, cl::sycl::queue&amp;, std::</td><td>6144</td><td>512</td><td>0.243s</td><td>0.243s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)16&gt;(int, cl::sycl::queue&amp;, std::</td><td>8192</td><td>512</td><td>0.416s</td><td>0.416s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)20&gt;(int, cl::sycl::queue&amp;, std::</td><td>10240</td><td>512</td><td>0.599s</td><td>0.599s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)24&gt;(int, cl::sycl::queue&amp;, std::</td><td>12288</td><td>512</td><td>0.842s</td><td>0.842s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)28&gt;(int, cl::sycl::queue&amp;, std::</td><td>14336</td><td>512</td><td>0.944s</td><td>0.944s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)32&gt;(int, cl::sycl::queue&amp;, std::</td><td>16384</td><td>512</td><td>1.177s</td><td>1.177s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)36&gt;(int, cl::sycl::queue&amp;, std::</td><td>18432</td><td>512</td><td>1.336s</td><td>1.336s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)40&gt;(int, cl::sycl::queue&amp;, std::</td><td>20480</td><td>512</td><td>1.467s</td><td>1.467s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)48&gt;(int, cl::sycl::queue&amp;, std::</td><td>24576</td><td>512</td><td>1.783s</td><td>1.783s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)44&gt;(int, cl::sycl::queue&amp;, std::</td><td>22528</td><td>512</td><td>1.648s</td><td>1.648s</td><td></td><td></td></tr><tr><td>VectorAdd2&lt;(int)42&gt;(int, cl::sycl::queue&amp;, std::</td><td>21504</td><td>512</td><td>1.568s</td><td>1.568s</td><td></td><td></td></tr></table>

The following timeline view gives the occupancy over a period of time. Note that the occupancy metric is accurate for a large part of the kernel execution and tapers off towards the end, due to the varying times at which each of the threads finish their execution.

## VectorAdd2 Timeline View

![](images/5285ae1c7a8aba81f75b52ba43cdefb4133658402be16a8b6a47edd3693eb54d.jpg)  
The kernel VectorAdd3 shown below is similar to the kernels above with two important differences.

1. It can be instantiated with the number of work-groups, work-group size, and sub-group size as template parameters. This allows us to do experiments to investigate the impact of number of subgroups and work-groups on thread occupancy.

The amount of work done inside the kernel is dramatically increased to ensure that these kernels are resident in the execution units doing work for a substantial amount of time.

```cpp
template <int groups, int wg_size, int sg_size>
int VectorAdd3(sycl::queue &q, const IntArray &a, const IntArray &b,
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
            [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(sg_size)]] {
                size_t grp_id = index.get_group()[0];
                size_t loc_id = index.get_local_id();
                size_t start = grp_id * mysize;
                size_t end = start + mysize;
                for (int j = 0; j < iter; j++)
                    for (size_t i = start + loc_id; i < end; i += wg_size) {
```

```cpp
sum_acc[i] = a_acc[i] + b_acc[i];
    }
});
});
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "VectorAdd3<" << groups << "> completed on device - took "
       << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd3
```

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
