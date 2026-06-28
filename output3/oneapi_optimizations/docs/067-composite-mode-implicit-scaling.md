
As mentioned above, in COMPOSITE mode, the driver and language runtime provide tools that expose each GPU card as a root device. In this mode, a root device is composed of multiple sub-devices, also known as stacks. The stacks form a shared memory space which allows treating a root device as a monolithic device without the requirement of explicit communication between stacks.

This section covers multi-stack programming principles using implicit scaling in COMPOSITE mode.

• Introduction

• Work Scheduling and Memory Distribution

• STREAM Example

• Programming Principles

## Introduction

Implicit scaling applies to multiple stacks inside a single GPU card only.

In COMPOSITE mode, if the program offloads to a device that is the entire card, then the driver and language runtime are, by default, responsible for work distribution and multi-stack memory placement.

For implicit scaling, no change in application code is required. An OpenMP/SYCL kernel submitted to a device will utilize all the stacks on that device. Similarly, memory allocated on the device will be accessible across all the stacks. The driver behavior is described in Work Scheduling and Memory Distribution.

Notes on implicit scaling:

• Set ZE\_FLAT\_DEVICE\_HIERARCHY=COMPOSITE to allow implicit scaling.

• Implicit scaling should not be combined with SYCL/OpenMP sub-device semantics.

• Do not use sub-device syntax in ZE\_AFFINITY\_MASK. That is, instead of exposing stack 0 in root device 0 (ZE\_AFFINITY\_MASK=0.0), you must expose the entire root device to the driver via ZE\_AFFINITY\_MASK=0 or by unsetting ZE\_AFFINITY\_MASK.

## Performance Expectations

In implicit scaling, the resources of all the stacks are exposed to a kernel. When using a root device with 2 stacks, a kernel can achieve 2x compute peak, 2x memory bandwidth, and 2x memory capacity. In the idea case, workload performance increases by 2x. However, cache size and cache bandwidth are increased by 2x as well, which can lead to better-than-linear scaling if the workload fits in the increased cache capacity.

Each stack is equivalent to a NUMA domain and therefore memory access pattern and memory allocation are crucial to achieving optimal implicit scaling performance. Workloads with a concept of locality are expected to work best with this programming model as cross-stack memory accesses are naturally minimized. Note that compute-bound kernels are not impacted by NUMA domains, thus they are expected to easily scale to multiple stacks with implicit scaling. If the algorithm has a lot of cross-stack memory accesses, the performance will be impacted negatively. Minimize cross-stack memory accesses by exploiting locality in algorithm.

MPI applications are more efficient with implicit scaling compared to an explicit scaling approach. A single MPI rank can utilize the entire root device which eliminates explicit synchronization and communication between stacks. Implicit scaling automatically overlaps local memory accesses and cross-stack memory accesses in a single kernel launch.

Implicit scaling improves kernel execution time only. Serial bottlenecks will not speed up. Applications will observe no speedup with implicit scaling if a large serial bottleneck is present. Common serial bottlenecks are:

• high CPU usage

• kernel launch latency

• PCIe transfers

These will become more pronounced as kernel execution time is reduced with implicit scaling. Note that only stack 0 has PCIe connection to the host. On Intel<sup>®</sup> Data Center GPU Max with implicit scaling enabled, kernel launch latency increases by about 3 microseconds.

## Work Scheduling and Memory Distribution

The root device driver uses deterministic heuristics to distribute work-groups and memory pages to all stacks when implicit scaling is used. These heuristics are described in the next two sections.

## Memory Coloring

Any allocation in SYCL/OpenMP that corresponds to a shared or device allocation is colored across all stacks, meaning that allocation is divided into number-of-stacks chunks and distributed round-robin between the stacks. Consider this root device allocation:

OpenMP:

```c
int *a = (int*)omp_target_alloc( sizeof(int)*N, device_id );
```

SYCL:

```txt
int *a = sycl::malloc_device<int>(N, q);
```

For a 2-stack root device, the first half, (elements a[0] to a[N/2-1]), is physically allocated on stack 0. The remaining half, (elements a[N/2] to a[N-1]), is located on stack 1. In future, we will introduce memory allocation APIs that allow user-defined memory coloring.

Note:

• The memory coloring described above is applied at page size-granularity. An allocation containing three pages has two pages resident on stack 0.

• Allocations smaller than or equal to page-size are resident on stack 0 only.

• Using a memory pool that is based on a single allocation will break memory coloring logic. It is recommended that applications create one allocation per object to allow the object data to be distributed among all stacks.

## Static Partitioning

Scheduling of work-groups to stacks is deterministic and referred to as static partitioning. The partitioning follows a simple rule: the slowest moving dimension is divided in number-of-stacks chunks and distributed round-robin between stacks. Let’s look the following at 1-dimensional kernel launch on the root device:

OpenMP:

```txt
#pragma omp target teams distribute parallel for simd
for (int i = 0; i < N; ++i)
{
    //
}
```

SYCL:

```javascript
q.parallel_for(N, [=] (auto i) {
    //
});
```

Since there is only a single dimension it is, automatically the slowest moving dimension and partitioned between stacks by the driver. For a 2-stack root device, iterations 0 to N/2-1 are executed on stack 0. The remaining iterations N/2 to N-1 are executed on stack 1.

For OpenMP, the slowest moving dimension is the outermost loop when the collapse clause is used. For SYCL, the slowest moving dimension is the first element of global range. For example, consider this 3D kernel launch:

## OpenMP:

```lisp
#pragma omp target teams distribute parallel for simd collapse(3)
for (int z = 0; z < nz; ++z)
{
    for (int y = 0; y < ny; ++y)
    {
        for (int x = 0; x < nx; ++x)
        {
            // 
        }
    }
}
```

## SYCL:

```txt
range<3> global{nz, ny, nx};
range<3> local{1, 1, 16};

cgh.parallel_for(nd_range<3>(global, local), [=](nd_item<3> item) {
    // 
});
```

The slowest moving dimension is z and is partitioned between the stacks. That is, for a 2-stack root device, all iterations from z = 0 to z = nz/2 - 1 are executed on stack 0. The remaining iterations from z = nz/2 to z = nz-1 are executed on stack 1.

In case the slowest moving dimension cannot be divided evenly between the stacks and there is a load imbalance that is larger than 5%, the driver will partition the next dimension if it leads to less load imbalance. This impacts kernels with odd dimensions smaller than 19 only. Examples for different kernel launches can be seen in the table below (assuming local range {1,1,16}):

Work-Group Partition to Stacks

<table><tr><td>nz</td><td>ny</td><td>nx</td><td>Partitioned Dimension</td></tr><tr><td>512</td><td>512</td><td>512</td><td>z</td></tr><tr><td>21</td><td>512</td><td>512</td><td>z</td></tr><tr><td>19</td><td>512</td><td>512</td><td>y</td></tr><tr><td>18</td><td>512</td><td>512</td><td>z</td></tr><tr><td>19</td><td>19</td><td>512</td><td>x</td></tr></table>

In case of multi-dimensional local range in SYCL, the partitioned dimension can change. For example, for global range {38,512,512} with local range {2,1,8} the driver would partition the y-dimension, while for local range {1,1,16} the driver would partition the z-dimension.

OpenMP can only have a 1-dimensional local range which is created from the innermost loop, and thus does not impact static partitioning heuristics. OpenMP kernels created with a collapse level larger than 3 correspond to a 1-dimensional kernel with all the for loops linearized. The linearized loop will be partitioned following 1D kernel launch heuristics.

Notes:

• Static partitioning happens at work-group granularity. This implies that all work-items in a work-group are scheduled to the same stack.

• A kernel with a single work-group is resident on stack 0 only.

STREAM Example

For a given kernel:

OpenMP:

```c
int *a = (int *)omp_target_alloc(sizeof(int) * N, device_id);

#pragma omp target teams distribute parallel for simd
for (int i = 0; i < N; ++i)
{
    a[i] = i;
}
```

SYCL:

```c
int *a = sycl::malloc_device<int>(N, q);

q.parallel_for(N, [=] (auto i) {
    a[i] = i;
});
```

Implicit scaling guarantees 100% local memory accesses. The behavior of static partitioning and memory coloring is visualized below:

![](images/1eaf54f351aff8e6b94abef7c2ce32e0df20b6f2c83ce141f5f2e5696d68d5ba.jpg)

In this section, we demonstrate implicit scaling performance for STREAM benchmark using 1D and 3D kerne launches on Intel Data Center GPU Max.

## STREAM

Consider the STREAM benchmark written in OpenMP. The main kernel is on line 44-48:

```cpp
// Code for STREAM:
#include <iostream>
#include <omp.h>
#include <cstdlib>

// compile via:
// icpx -O2 -fiopenmp -fopenmp-targets=spir64 ./stream.cpp

int main()
{
    constexpr int64_t N = 256 * 1e6;
    constexpr int64_t bytes = N * sizeof(int64_t);

    int64_t *a = static_cast<int64_t *>(malloc(bytes));
    int64_t *b = static_cast<int64_t *>(malloc(bytes));
    int64_t *c = static_cast<int64_t *>(malloc(bytes));

    #pragma omp target enter data map(alloc:a[0:N])
    #pragma omp target enter data map(alloc:b[0:N])
    #pragma omp target enter data map(alloc:c[0:N])

    for (int i = 0; i < N; ++i)
    {
        a[i] = i + 1;
        b[i] = i - 1;
    }

    #pragma omp target update to(a[0:N])
    #pragma omp target update to(b[0:N])

    const int no_max_rep = 100;
    double time;
    for (int irep = 0; irep < no_max_rep + 10; ++irep)
    {
        if (irep == 10)
            time = omp_get_wtime();

        #pragma omp target teams distribute parallel for simd
```

```cpp
for (int i = 0; i < N; ++i)
{
    c[i] = a[i] + b[i];
}
}
time = omp_get_wtime() - time;
time = time / no_max_rep;

#pragma omp target update from(c[0:N])

for (int i = 0; i < N; ++i)
{
    if (c[i] != 2 * i)
    {
        std::cout << "wrong results!" << std::endl;
        exit(1);
    }
}

const int64_t streamed_bytes = 3 * N * sizeof(int64_t);

std::cout << "bandwidth = " << (streamed_bytes / time) * 1E-9
    << " GB/s" << std::endl;
}
```

In COMPOSITE mode, the benchmark runs on the entire root-device (GPU card with 2 stacks) by implicit scaling. No code changes are required. The heuristics of static partitioning and memory coloring guarantee that each stack accesses local memory only. On a 2-stack Intel<sup>®</sup> Data Center GPU Max system we measure 2x speed-up for STREAM compared to a single stack. Measured bandwidth is reported in table below.

Measured Bandwidth with 1D Kernel Launch

<table><tr><td>Array Size [MB]</td><td>1-stack Bandwidth [GB/s]</td><td>Implicit Scaling (2-stack) Bandwidth [GB/s]</td><td>Implicit Scaling Speed-up over 1-stack</td></tr><tr><td>512</td><td>1056</td><td>2074</td><td>1.96x</td></tr><tr><td>1024</td><td>1059</td><td>2127</td><td>2x</td></tr><tr><td>2048</td><td>1063</td><td>2113</td><td>1.99x</td></tr></table>

## 3D STREAM

The STREAM benchmark can be modified to use 3D kernel launch via the collapse clause in OpenMP. The intent here is to show performance in case driver heuristics are used to partition the 3D kernel launches between the stacks. The kernel is on line 59-70:

```cpp
// Code for 3D STREAM
#include <iostream>
#include <omp.h>
#include <cassert>

// compile via:
// icpx -O2 -fiopenmp -fopenmp-targets=spir64 ./stream_3D.cpp

int main()
{
    const int device_id = omp_get_default_device();
```

```cpp
const int desired_total_size = 32 * 512 * 16384;
const std::size_t bytes = desired_total_size * sizeof(int64_t);

std::cout << "memory footprint = " << 3 * bytes * 1E-9 << " GB"
    << std::endl;

int64_t *a = static_cast<int64_t*>(omp_target_alloc_device(bytes, device_id));
int64_t *b = static_cast<int64_t*>(omp_target_alloc_device(bytes, device_id));
int64_t *c = static_cast<int64_t*>(omp_target_alloc_device(bytes, device_id));

const int min = 64;
const int max = 32768;

for (int lx = min; lx < max; lx *= 2)
{
    for (int ly = min; ly < max; ly *= 2)
    {
        for (int lz = min; lz < max; lz *= 2)
        {
            const int total_size = lx * ly * lz;
            if (total_size != desired_total_size)
                continue;

            std::cout << "lx=" << lx << " ly=" << ly << " lz="
                << lz << ", ";

            #pragma omp target teams distribute parallel for simd
            for (int i = 0; i < total_size; ++i)
            {
                a[i] = i + 1;
                b[i] = i - 1;
                c[i] = 0;
            }

            const int no_max_rep = 40;
            const int warmup = 10;
            double time;
            for (int irep = 0; irep < no_max_rep + warmup; ++irep)
            {
                if (irep == warmup) time = omp_get_wtime();

                #pragma omp target teams distribute parallel for simd collapse(3
                for (int iz = 0; iz < lz; ++iz)
                {
                    for (int iy = 0; iy < ly; ++iy)
                    {
                        for (int ix = 0; ix < lx; ++ix)
                        {
                            const int index = ix + iy * lx + iz * lx * ly;
                            c[index] = a[index] + b[index];
                        }
                    }
                }
            }
            time = omp_get_wtime() - time;
            time = time / no_max_rep;

            const int64_t streamed_bytes = 3 * total_size * sizeof(int64_t);
```

```cpp
std::cout << "bandwidth = " << (streamed_bytes / time) * 1E-9
        << " GB/s" << std::endl;

#pragma omp target teams distribute parallel for simd
for (int i = 0; i < total_size; ++i)
{
    assert(c[i] == 2 * i);
}
}
}

omp_target_free(a, device_id);
omp_target_free(b, device_id);
omp_target_free(c, device_id);
}
```

Note that the inner-most loop has stride-1 memory access pattern. If the z- or y-loop were the innermost loop, performance would decrease due to the generation of scatter loads and stores leading to poor cache line utilization. On a 2-stack Intel<sup>®</sup> Data Center GPU Max with 2 Gigabytes array size, we measure the performance shown below.

Measured Bandwidth with 3D Kernel Launch

<table><tr><td>nx</td><td>ny</td><td>nz</td><td>1-stack Bandwidth [GB/s]</td><td>Implicit Scaling Bandwidth [GB/s]</td><td>Implicit Scaling Speed-up over 1-stack</td></tr><tr><td>64</td><td>256</td><td>16834</td><td>1040</td><td>2100</td><td>2.01x</td></tr><tr><td>16834</td><td>64</td><td>256</td><td>1040</td><td>2077</td><td>1.99x</td></tr><tr><td>256</td><td>16834</td><td>64</td><td>1037</td><td>2079</td><td>2x</td></tr></table>

As described in Static Partitioning, for these loop bounds the driver partitions the slowest moving dimension, i.e. the z-dimension, between both stacks. This guarantees that each stack accesses local memory only, leading to close to 2x speed-up with implicit scaling compared to using a single stack.

## Programming Principles

To achieve good performance with implicit scaling, cross-stack memory accesses must be minimized, but it is not required to eliminate all cross-stack accesses. A certain amount of cross-stack traffic can be handled by stack-to-stack interconnect if performed concurrently with local memory accesses. For a memory bandwidth bound workload the amount of acceptable cross-stack accesses is determined by the ratio of local memory bandwidth and cross-stack bandwidth (see Cross-Stack Traffic).

The following principles should be embraced by workloads that use implicit scaling:

• The kernel must have enough work-items to utilize both stacks.

• The minimal number of work-items needed to utilize both stacks is , where VE refers to Vector Engine or Execution Unit.

• 2-stack Intel<sup>®</sup> Data Center GPU Max with 1024 VE and SIMD32 requires at least 262,144 work-items.

• Device time must dominate runtime to observe whole application scaling.

• Minimize cross-stack memory accesses by exploiting locality in algorithm.

• The slowest moving dimension should be large to avoid stack load imbalance.

• Cross-stack memory accesses and local memory accesses should be interleaved.

• Avoid stride-1 memory accesses in slowest moving dimension for 2D and 3D kernel launches.

• If the memory access pattern changes dynamically over time, a sorting step should be performed every Nth iteration to minimize cross-stack memory accesses.

• Don’t use a memory pool based on a single allocation (see Memory Coloring).

Many applications naturally have a concept of locality. These applications are expected to be a good fit for using implicit scaling due to low cross-stack traffic. To illustrate this concept, we use a stencil kernel as an example. A stencil operates on a grid which can be divided into blocks where the majority of stencil computations within a block use stack local data. Only stencil operations that are at the border of the block require data from another block, i.e. on another stack. The amount of these cross-stack/cross-border accesses are suppressed by halo to local volume ratio. This concept is illustrated below.

![](images/721e3359cc4079e3d9b72927c9d098c0e81e6c39a611473a300fa3f98afae275.jpg)

## Cross-Stack Traffic

As mentioned in the previous section, it is crucial to minimize cross-stack traffic. To guide how much traffic can be tolerated without significantly impacting application performance, we can benchmark the STREAM kernel with varying amounts of cross-stack traffic and compare to stack-local STREAM performance. The worst case is 100% cross-stack traffic. This is generated by reversing the loop order in STREAM kernel (see STREAM):

```lisp
#pragma omp target teams distribute parallel for simd
for (int i = N - 1; i <= 0; --i)
{
    c[i] = a[i] + b[i];
}
```

Here, each stack has 100% cross-stack memory traffic as work-groups on stack-0 access array elements N-1 to N/2 which are located in stack-1 memory. This kernel essentially benchmarks stack-to-stack bi-directional bandwidth. This approach can be generalized to interpolate between 0% cross-stack accesses and 100% cross-stack accesses by the modified STREAM below:

```cpp
// Code for cross stack stream
#include <iostream>
#include <omp.h>

// compile via:
// icpx -O2 -fiopenmp -fopenmp-targets=spir64 ./stream_cross_stack.cpp
// run via:
// ZE_AFFINITY_MASK=0 ./a.out

template <int cross_stack_fraction>
void cross_stack_stream() {

    constexpr int64_t size = 256*1e6;
    constexpr int64_t bytes = size * sizeof(int64_t);

    int64_t *a = static_cast<int64_t*>(malloc( bytes ));
    int64_t *b = static_cast<int64_t*>(malloc( bytes ));
```

```c
int64_t *c = static_cast<int64_t*>(malloc( bytes ));
#pragma omp target enter data map( alloc:a[0:size] )
#pragma omp target enter data map( alloc:b[0:size] )
#pragma omp target enter data map( alloc:c[0:size] )

for ( int i = 0; i < size; ++i ) {

    a[i] = i + 1;
    b[i] = i - 1;
    c[i] = 0;
}

#pragma omp target update to( a[0:size] )
#pragma omp target update to( b[0:size] )
#pragma omp target update to( c[0:size] )

const int num_max_rep = 100;

double time;

for ( int irep = 0; irep < num_max_rep+10; ++irep ) {

    if ( irep == 10 ) time = omp_get_wtime();

    #pragma omp target teams distribute parallel for simd
    for ( int j = 0; j < size; ++j ) {

        const int cache_line_id = j / 16;

        int i;

        if ( (cache_line_id%cross_stack_fraction) == 0 ) {

            i = (j+size/2)%size;
        }
        else {

            i = j;
        }

        c[i] = a[i] + b[i];
    }
}
time = omp_get_wtime() - time;
time = time/num_max_rep;

#pragma omp target update from( c[0:size] )

for ( int i = 0; i < size; ++i ) {

    if ( c[i] != 2*i ) {

        std::cout << "wrong results!" << std::endl;
        exit(1);
    }
}

const int64_t streamed_bytes = 3 * size * sizeof(int64_t);
```

```cpp
std::cout << "cross_stack_percent = " << (1/(double)cross_stack_fraction)*100
        << "% , bandwidth = " << (streamed_bytes/time) * 1E-9 << " GB/s" << std::endl;
}

int main() {

    cross_stack_stream< 1>();
    cross_stack_stream< 2>();
    cross_stack_stream< 4>();
    cross_stack_stream< 8>();
    cross_stack_stream<16>();
    cross_stack_stream<32>();
}
```

The kernel on line 48-65 accesses every cross\_stack\_fraction'th cache line cross-stack by offsetting array access with (j+N/2)%N. For cross\_stack\_fraction==1, we generate 100% cross-stack memory accesses. By doubling cross\_stack\_fraction we decrease cross-stack traffic by a factor of 2. Note that this kernel is written such that cross-stack and local memory accesses are interleaved within work-groups to maximize hardware utilization. Measured performance on 2-stack Intel<sup>®</sup> Data Center GPU Max with 2 Gigabytes array size can be seen below:

Measured Bandwidth with Cross-Stack Accesses

<table><tr><td>Partial cross-stack STREAM bandwidth [GB/s]</td><td>cross_stack_fraction</td><td>% of cross-stack accesses</td><td>% of max local 2-stack STREAM bandwidth</td></tr><tr><td>355</td><td>1</td><td>100%</td><td>17%</td></tr><tr><td>696</td><td>2</td><td>50%</td><td>33%</td></tr><tr><td>1223</td><td>4</td><td>25%</td><td>58%</td></tr><tr><td>1450</td><td>8</td><td>12.5%</td><td>69%</td></tr><tr><td>1848</td><td>16</td><td>6.25%</td><td>87%</td></tr><tr><td>2108</td><td>32</td><td>3.125%</td><td>99%</td></tr></table>

As seen in the above table, applications should try to limit cross-stack traffic to be less than 10% of all memory traffic to avoid a significant drop in sustained memory bandwidth. For STREAM with of 12.5% crossstack accesses we measure about 69% of the bandwidth of a local STREAM benchmark. These numbers can be used to estimate the impact of cross-stack memory accesses on application kernel execution time.
