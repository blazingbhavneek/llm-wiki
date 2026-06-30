# oneapi_optimizations Source Lines 2075-2643

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L2075-L2643

Citation: [oneapi_optimizations:L2075-L2643]

````text
If the sub-group size is 16 as requested, we know that 16 work items are packed into one Vector Engine thread. We also know work items in the same sub-group can communicate and share data with each other very efficiently. If the work items in the same sub-group share the private histogram bins, only 256 private bins are needed for the whole sub-group, or 16 private bins for each work item instead.

## Sub-group Has 256 Private Histogram Bins

![](images/96e02ae19f5182824527de6edba7999ca41dc950647be5e8ce0f59533d252d1c.jpg)

To share the histogram bins in the sub-group, each work item broadcasts its input data to every work item in the same sub-group. The work item that owns the corresponding histogram bin does the update.

```cpp
constexpr int BLOCK_SIZE = 256;
constexpr int NUM_BINS = 256;

std::vector<unsigned long> hist(NUM_BINS, 0);

sycl::buffer<unsigned long, 1> mbuf(input.data(), N);
sycl::buffer<unsigned long, 1> hbuf(hist.data(), NUM_BINS);

auto e = q.submit([&](auto &h) {
    sycl::accessor macc(mbuf, h, sycl::read_only);
    auto hacc = hbuf.get_access<sycl::access::mode::atomic>(h);
    h.parallel_for(
        sycl::nd_range(sycl::range{N / BLOCK_SIZE}, sycl::range{64}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
            int group = it.get_group()[0];
            int gSize = it.get_local_range()[0];
            auto sg = it.get_sub_group();
            int sgSize = sg.get_local_range()[0];
            int sgGroup = sg.get_group_id()[0];

        unsigned int
            histogram[NUM_BINS / 16]; // histogram bins take too much storage
                                // to be promoted to registers
        for (int k = 0; k < NUM_BINS / 16; k++) {
            histogram[k] = 0;
```

```cpp
}
    for (int k = 0; k < BLOCK_SIZE; k++) {
        unsigned long x = sg.load(
            get_accessor_pointer(macc) + group * gSize * BLOCK_SIZE +
            sgGroup * sgSize * BLOCK_SIZE + sgSize * k);
// subgroup size is 16
#pragma unroll
        for (int j = 0; j < 16; j++) {
            unsigned long y = sycl::group_broadcast(sg, x, j);
#pragma unroll
            for (int i = 0; i < 8; i++) {
                unsigned int c = y & 0xFF;
                // (c & 0xF) is the workitem in which the bin resides
                // (c >> 4) is the bin index
                if (sg.get_local_id()[0] == (c & 0xF)) {
                    histogram[c >> 4] += 1;
                }
                y = y >> 8;
            }
        }
    }

    for (int k = 0; k < NUM_BINS / 16; k++) {
        hacc[16 * k + sg.get_local_id()[0]].fetch_add(histogram[k]);
    }
});
});
```

## Using Sub-group Block Load/Store

Memory loads/stores are vectorized. Each lane of a vector load/store instruction has its own address and data. Both addresses and data take register space. For example:

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
            [=](sycl::nd_item<1> it) {
                int i = it.get_global_linear_id();
                data[i] = data2[i];
            });
});
```

The memory loads and stores in the statement:

```txt
``data[i] = data2[i];``
```

are vectorized and each vector lane has its own address. Assuming the SIMD width or the sub-group size is 16, total register space for addresses of the 16 lanes is 128 bytes. If each GRF register is 32-byte wide, 4 GRF registers are needed for the addresses.

Noticing the addresses are contiguous, we can use sub-group block load/store built-ins to save register space for addresses:

```c
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
```

```cpp
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
        auto sg = it.get_sub_group();

        int base =
            (it.get_group(0) * 32 +
            sg.get_group_id()[0] * sg.get_local_range()[0]);

        auto load_ptr = get_multi_ptr(&(data2[base + 0]));
        int x = sg.load(load_ptr);

        auto store_ptr = get_multi_ptr(&(data[base + 0]));
        sg.store(store_ptr, x);
    });
});
```

The statements:

```javascript
` ` x = sg.load(global_ptr(&(data2[base + 0])), sg.store(global_ptr(&(data[base + 0])), x);``
```

each loads/stores a contiguous block of memory and the compiler will compile these 2 statements into special memory block load/store instructions. And because it is a contiguous memory block, we only need the starting address of the block. So 8, instead of 128, bytes of actual register space, or at most 1 register, is used for the address for each block load/store.

## Using Shared Local Memory

If the number of histogram bins gets larger than, for example, 1024, there will not be enough register space for private bins even the private bins are shared in the same sub-group. To reduce memory traffic, the loca histogram bins can be allocated in the shared local memory and shared by work items in the same workgroup. Refer to the “Shared Local Memory” chapter and see how it is done in the histogram example there.

## Porting Code with High Register Pressure to Intel® Max GPUs

When migrating code from CUDA to SYCL, it may happen that the resulting SYCL code does not perform well on Intel<sup>®</sup> Data Center GPUs (e.g. the Intel<sup>®</sup> Data Center GPU Max 1550) despite showing good performance on NVIDIA GPUs. In some cases this is due to register spills on Intel<sup>®</sup> GPUs which do not occur on NVIDIA GPUs due to the different sizes of the general-purpose register files (GRF). Possible ways to handle these register spills without changes to the code is discussed in what follows. Further optimization techniques for reducing the overall register pressure can be found in Optimizing Register Spills.

## A Simple Code Example with High Register Pressure

The example used for this demonstration is inspired by code performing automatic differentiation utilizing multivariate dual numbers. No knowledge about dual numbers is required to understand the following example. For more information on dual numbers we refer to the Wikipedia page and this book.

```cpp
#include <chrono>
#include <iostream>
#include <sycl/sycl.hpp>

#define NREGISTERS 80

#ifndef SIMD16
#define SIMD_SIZE 32
```

```cpp
#else
#define SIMD_SIZE 16
#endif

class my_type {
public:
    my_type(double x0, double x1, double x2, double x3, double x4, double x5,
        double x6, double x7)
        : x0_(x0), x1_(x1), x2_(x2), x3_(x3), x4_(x4), x5_(x5), x6_(x6), x7_(x7) {
}

    my_type(double const *const vals)
        : x0_(vals[0]), x1_(vals[1]), x2_(vals[2]), x3_(vals[3]), x4_(vals[4]),
        x5_(vals[5]), x6_(vals[6]), x7_(vals[7]) {}

    my_type operator+(const my_type &rhs) {
        return my_type(rhs.x0_ + x0_, rhs.x1_ + x1_, rhs.x2_ + x2_, rhs.x3_ + x3_,
            rhs.x4_ + x4_, rhs.x5_ + x5_, rhs.x6_ + x6_, rhs.x7_ + x7_);
    }

    void WriteBack(double *const vals) {
        vals[0] += x0_;
        vals[1] += x1_;
        vals[2] += x2_;
        vals[3] += x3_;
        vals[4] += x4_;
        vals[5] += x5_;
        vals[6] += x6_;
        vals[7] += x7_;
    }

private:
    double x0_, x1_, x2_, x3_, x4_, x5_, x6_, x7_;
};

int main(int argc, char **) {
    sycl::queue Q(sycl::gpu_selector_v);
    size_t nsubgroups;
    if (argc > 1)
        nsubgroups = 10;
    else
        nsubgroups = 8;

    const size_t ARR_SIZE = nsubgroups * SIMD_SIZE * NREGISTERS;
    double *val_in = sycl::malloc_shared<double>(ARR_SIZE, Q);
    double *val_out = sycl::malloc_shared<double>(ARR_SIZE, Q);

    std::cout << "Using simd size " << SIMD_SIZE << std::endl;

    Q.parallel_for(ARR_SIZE, [=](auto it) {
        val_in[it.get_id()] = argc * it.get_id();
    }).wait();

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int rep = 0; rep < 1000; rep++) {
        Q.parallel_for(sycl::nd_range<1>(nsubgroups * SIMD_SIZE, SIMD_SIZE),
            [=](auto it) [[intel::reqd_sub_group_size(SIMD_SIZE)]] {
```

```cpp
const size_t id = it.get_global_linear_id();

double const *const val_offs = val_in + id * NREGISTERS;

my_type v0(val_offs + 0);
my_type v1(val_offs + 8);
my_type v2(val_offs + 16);
my_type v3(val_offs + 24);
my_type v4(val_offs + 32);
my_type v5(val_offs + 40);
my_type v6(val_offs + 48);
my_type v7(val_offs + 56);
my_type v8(val_offs + 64);
my_type v9(val_offs + 72);

my_type p0 = v0 + v5;
my_type p1 = v1 + v6;
my_type p2 = v2 + v7;
my_type p3 = v3 + v8;
my_type p4 = v4 + v9;

p0 = p0 + p1 + v5;
p2 = p2 + p3 + v6;
p4 = p4 + p1 + v7;
p3 = p3 + p2 + v8;
p2 = p0 + p4 + v9;
p1 = p1 + v0;

double *const vals_out_offs = val_out + id * NREGISTERS;
p0.WriteBack(vals_out_offs);
p1.WriteBack(vals_out_offs + 8);
p2.WriteBack(vals_out_offs + 16);
p3.WriteBack(vals_out_offs + 24);
p4.WriteBack(vals_out_offs + 32);
v0.WriteBack(vals_out_offs + 40);
v1.WriteBack(vals_out_offs + 48);
v2.WriteBack(vals_out_offs + 56);
v3.WriteBack(vals_out_offs + 64);
v4.WriteBack(vals_out_offs + 72);
})
.wait();
}
auto end_time = std::chrono::high_resolution_clock::now();

std::cout << "Took "
<< std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time)
.count()
<< " microseconds" << std::endl;

sycl::free(val_in, Q);
sycl::free(val_out, Q);

return 0;
}
```

The code shows a class my\_type, which represents a dimension 7 dual number and which wraps 8 doubles and includes overloads of arithmetic operators. The main function of the program initializes some data and then launches a specific GPU kernel 1000 times (for loop in line 70, kernel launch in line 72). These repeated launches are purely for the purpose of getting more accurate performance numbers and do not influence the register spills under consideration. The kernel uses the data to initialize several my\_type dual numbers and then performs several arithmetic operations with them in such a way that they produce high register pressure.

More precisely, the SYCL code compiled for an NVIDIA A100 GPU with oneAPI for NVIDIA GPUs and the following command

```shell
clang++ -O2 -Xcuda-ptxas -v -fsycl -fsycl-targets=nvidia_gpu_sm_80 --cuda-path=/opt/hpc_software/
compilers/nvidia/cuda-12.0 main.cpp -o exec_cuda.out
```

shows that 168 registers are allocated, and none are spilled with the following output

```txt
ptxas info : Used 168 registers, 380 bytes cmem[0]
```

Compiling the code for PVC, on the other hand, using ahead-of-time (AOT) compilation (cf. Ahead-Of-Time Compilation) with oneAPI 2023.2.0 with the following command

```batch
icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc"
main.cpp -o exec_jit.out
```

results in register spills as indicated by a compiler warning such as the following

```txt
warning: kernel _ZTSZ4mainEU1T_E0_ compiled SIMD32 allocated 128 regs and spilled around 396
```

The execution time of the code on an A100 80GB GPU and a single stack of the Intel<sup>®</sup> Data Center GPU Max 1550 is shown in the following table.

Execution time on a single stack of Intel<sup>®</sup> Max 1550 vs NVIDIA A100 80GB

<table><tr><td>Hardware</td><td>Time (ms), lower is better</td><td>Register Spills</td></tr><tr><td>A100 80GB</td><td>21.5</td><td>No</td></tr><tr><td>1T Max 1550</td><td>36.1</td><td>Yes</td></tr></table>

It is evident that the execution time on the Intel<sup>®</sup> GPU is significantly longer than on the NVIDIA GPU. Based on the information above, it is reasonable to expect that the difference is related to the register allocations. To understand the underlying cause, the following section points out the differences in the register files.

## Registers on an Intel<sup>®</sup> Data Center GPU Max 1550

The difference in the register allocation is due to the different sizes of the general-purpose register files (GRF). More precisely, a NVIDIA A100 GPU provides up to 256 32-bit wide registers per work-item whereas the Intel<sup>®</sup> Data Center GPU Max 1550 provides by default 64 32-bit wide registers (assuming the same number of 32 work-items per sub-group as NVIDIA, cf. Intel® Xe GPU Architecture), i.e., a quarter of the NVIDIA GPU. There are two possibilities to adjust the available number of registers: the large GRF mode (cf. Small Register Mode vs. Large Register Mode) and a reduced sub-group size (cf. Sub-Groups and SIMD Vectorization). The impact of these two options on the above example are discussed in the following section.

GRF on Intel<sup>®</sup> GPU Max 1550 with and without large GRF and different SIMD widths.

<table><tr><td>Hardware</td><td>SIMD width</td><td>GRF mode</td><td>Registers per work-item</td></tr><tr><td>A100 80GB</td><td>32</td><td>N.A</td><td>256 x 32-bit</td></tr><tr><td>1T Max 1550</td><td>32</td><td>default</td><td>64 x 32-bit</td></tr><tr><td>1T Max 1550</td><td>32</td><td>large GRF</td><td>128 x 32-bit</td></tr><tr><td>1T Max 1550</td><td>16</td><td>default</td><td>128 x 32-bit</td></tr><tr><td>1T Max 1550</td><td>16</td><td>large GRF</td><td>256 x 32-bit</td></tr></table>

## Increasing the Number of Registers per Work-item

The above example requires 168 registers. Based on the discussion in the previous section, large GRF mode and a reduced SIMD width of 16 together should therefore avoid register spills. In what follows we check the three remaining combinations of the GRF mode and the SIMD width and we will see that, indeed, large GRF mode and SIMD 16 is required to avoid all register spills.

First, compiling the code again with large GRF, using

```batch
icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc -options -ze-opt-large-register-file" main.cpp -o exec_largegrf.out
```

still shows the following warning about register spills, although significantly less than before.

```txt
warning: kernel _ZTSZ4mainEUlT_E0_ compiled SIMD32 allocated 256 regs and spilled around 206
```

This is expected considering that only 128 32-bit wide registers are now available for the 168 required registers.

The second option to reduce the register spills is to reduce the SIMD width from 32 to 16 through a small change in the code. This can be done in this case by compiling the code with the following command

```batch
icpx -DSIMD16 -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc" main.cpp -o exec_simd16.out
```

Using the default GRF mode with SIMD width 16 again shows a warning about register spills.

```txt
warning: kernel _ZTSZ4mainEUlT_E0_ compiled SIMD16 allocated 128 regs and spilled around 112
```

Using both, a reduced SIMD width of 16 and large GRF mode, removes all register spills and no warning is given by the compiler, which is in line with the initial expectations.

The execution times for the four configurations are shown in the following table.

Execution times on a single stack of Intel<sup>®</sup> Data Center GPU Max 1550 with the different settings.

<table><tr><td>GRF mode</td><td>SIMD width</td><td>Register Spills</td><td>Time (ms), lower is better</td></tr><tr><td>default</td><td>32</td><td>Yes</td><td>36.1</td></tr><tr><td>large GRF</td><td>32</td><td>Yes</td><td>32.2</td></tr><tr><td>default</td><td>16</td><td>Yes</td><td>30.3</td></tr><tr><td>large GRF</td><td>16</td><td>No</td><td>27.7</td></tr></table>

Clearly, the best performance is achieved in the case where no register spills happen. It is interesting to note that SIMD width 16 is preferable to large GRF mode. This is not surprising considering that with large GRF mode each XVE has 4 threads.

## Special Considerations When Porting to SIMD 16

There are certain cases where the above methods may not be suitable or require special attention. On the one hand, as indicated above, with large GRF mode, 4 instead of 8 threads are available on each XVE. This may result in worse performance for certain cases.

On the other hand, switching from SIMD 32 to SIMD 16 may require special attention since it may lead to wrong results. An example is shown in the following code.

```cpp
#include <chrono>
#include <iostream>
#include <sycl/sycl.hpp>

#define NREGISTERS 80

#ifndef SIMD16
#define SIMD_SIZE 32
#else
#define SIMD_SIZE 16
#endif

class my_type {
public:
    my_type(double x0, double x1, double x2, double x3, double x4, double x5,
        double x6, double x7)
        : x0_(x0), x1_(x1), x2_(x2), x3_(x3), x4_(x4), x5_(x5), x6_(x6), x7_(x7)
    }

    my_type(double const *const vals)
        : x0_(vals[0]), x1_(vals[1]), x2_(vals[2]), x3_(vals[3]), x4_(vals[4]),
        x5_(vals[5]), x6_(vals[6]), x7_(vals[7]) {}

    my_type operator+(const my_type &rhs) {
        return my_type(rhs.x0_ + x0_, rhs.x1_ + x1_, rhs.x2_ + x2_, rhs.x3_ + x3_,
            rhs.x4_ + x4_, rhs.x5_ + x5_, rhs.x6_ + x6_, rhs.x7_ + x7_);
    }

    void WriteBack(double *const vals) {
        vals[0] += x0_;
        vals[1] += x1_;
        vals[2] += x2_;
        vals[3] += x3_;
        vals[4] += x4_;
        vals[5] += x5_;
        vals[6] += x6_;
        vals[7] += x7_;
    }

    void Load(double const *const vals) {
        x0_ = vals[0];
        x1_ = vals[1];
        x2_ = vals[2];
        x3_ = vals[3];
        x4_ = vals[4];
        x5_ = vals[5];
        x6_ = vals[6];
        x7_ = vals[7];
    }

private:
    double x0_, x1_, x2_, x3_, x4_, x5_, x6_, x7_;
};

int main(int argc, char **) {
    sycl::queue Q(sycl::gpu_selector_v);
```

```cpp
size_t nsubgroups;
if (argc > 1)
    nsubgroups = 10;
else
    nsubgroups = 8;

const size_t ARR_SIZE = nsubgroups * SIMD_SIZE * NREGISTERS;
double *val_in = sycl::malloc_shared<double>(ARR_SIZE, Q);
double *val_out = sycl::malloc_shared<double>(ARR_SIZE, Q);

std::cout << "Using simd size " << SIMD_SIZE << std::endl;

Q.parallel_for(ARR_SIZE, [=](auto it) {
    val_in[it.get_id()] = argc * it.get_id();
}).wait();

auto start_time = std::chrono::high_resolution_clock::now();

for (int rep = 0; rep < 1000; rep++) {
    Q.submit([&](auto &h) {
        sycl::local_accessor<double, 1> slm(sycl::range(32 * 8), h);

        h.parallel_for(sycl::nd_range<1>(nsubgroups * SIMD_SIZE, 32),
            [=](auto it) [[intel::reqd_sub_group_size(SIMD_SIZE)]] {
            const int id = it.get_global_linear_id();
            const int local_id = it.get_local_id(0);
            for (int i = 0; i < 8; i++) {
                slm[i + local_id * 8] = 0.0;
            }
#ifdef SIMD16
            it.barrier(sycl::access::fence_space::local_space);
#endif

            double const *const val_offs = val_in + id * NREGISTERS;

            my_type v0(val_offs + 0);
            my_type v1(val_offs + 8);
            my_type v2(val_offs + 16);
            my_type v3(val_offs + 24);
            my_type v4(val_offs + 32);
            my_type v5(val_offs + 40);
            my_type v6(val_offs + 48);
            my_type v7(val_offs + 56);
            my_type v8(val_offs + 64);
            my_type v9(val_offs + 72);

            my_type p0 = v0 + v5;
            v0.WriteBack(&slm[local_id * 8]);
#ifdef SIMD16
            it.barrier(sycl::access::fence_space::local_space);
#endif

            v0.Load(&slm[32 * 8 - 8 - local_id * 8]);
            my_type p1 = v1 + v6;
            my_type p2 = v2 + v7;
            my_type p3 = v3 + v8;
            my_type p4 = v4 + v9;

            p0 = p0 + p1 + v5;
```

```cpp
p2 = p2 + p3 + v6;
p4 = p4 + p1 + v7;
p3 = p3 + p2 + v8;
p2 = p0 + p4 + v9;

p1 = p1 + v0;

double *const vals_out_offs = val_out + id * NREGISTERS;
p0.WriteBack(vals_out_offs);
p1.WriteBack(vals_out_offs + 8);
p2.WriteBack(vals_out_offs + 16);
p3.WriteBack(vals_out_offs + 24);
p4.WriteBack(vals_out_offs + 32);
v0.WriteBack(vals_out_offs + 40);
v1.WriteBack(vals_out_offs + 48);
v2.WriteBack(vals_out_offs + 56);
v3.WriteBack(vals_out_offs + 64);
v4.WriteBack(vals_out_offs + 72);
});
}).wait();
}
auto end_time = std::chrono::high_resolution_clock::now();

std::cout << "Took "
    << std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time)
        .count()
    << " microseconds" << std::endl;

sycl::free(val_in, Q);
sycl::free(val_out, Q);

return 0;
}
```

It is similar to the first example above but introduces a shared local memory array (SLM, cf. Shared Local Memory) which is utilized to transpose the values stored in v0 within each work-group (which coincides with the sub-groups when using SIMD 32), as illustrated in the following figure and table.

The figure illustrates how the SLM is used in the second code example. The v0 value of each work-item in the work-group is stored in SLM. Each v0 consists of eight double values x0 - x7.

```asm
x0 x1 x2 x3 x4 x5 x6 x7 x0 x1 x2 x3 x4 x5 x6 x7
v0, local_id = 0 v0, local_id = 1
... x0 x1 x2 x3 x4 x5 x6 x7
v0, local_id = 31
```

After storing the v0 values in SLM, they are read in reverse order.

<table><tr><td>work-item local id store to SLM</td><td>work-item local id load from SLM</td></tr><tr><td>0</td><td>31</td></tr><tr><td>1</td><td>30</td></tr><tr><td>2</td><td>29</td></tr><tr><td>...</td><td>...</td></tr><tr><td>29</td><td>2</td></tr><tr><td>30</td><td>1</td></tr><tr><td>31</td><td>0</td></tr></table>

In the present case, the switch from SIMD 32 to SIMD 16 produces in general wrong results. The reason is that the synchronization between 32 work-items accessing the SLM is not guaranteed in the SIMD 16 case. This is not an issue in the SIMD 32 case since the work-items are in the same sub-group, which are processed together (cf. Sub-Groups and SIMD Vectorization). Thus, in the SIMD 16 case it may happen that a value in SLM is read and used (line 120) before it is actually written (line 116). To solve this issue, a SLM barrier needs to be added, as shown in line 118, to ensure that all values are written before any are read. Note that these barriers may negatively impact the computing time. The computing times for this example in the four configurations, are shown in the following table.

Execution times of the SLM example on a single stack of Intel<sup>®</sup> Data Center GPU Max 1550 with the different settings.

<table><tr><td>GRF mode</td><td>SIMD width</td><td>Register Spills</td><td>Time (ms), lower is better</td></tr><tr><td>default</td><td>32</td><td>Yes</td><td>38.0</td></tr><tr><td>large GRF</td><td>32</td><td>Yes</td><td>33.7</td></tr><tr><td>default</td><td>16</td><td>Yes</td><td>31.3</td></tr><tr><td>large GRF</td><td>16</td><td>No</td><td>29.7</td></tr></table>

To summarize, when porting high-register-pressure code from NVIDIA GPUs to Intel<sup>®</sup> GPUs, the code may show sub-optimal performance due to register spills induced by the different GRF sizes. In such a case, there are simple ways to increase the GRF size to better align the performance on the different devices with minimal code adjustments.

## Shared Local Memory

Often work-items need to share data and communicate with each other. On one hand, all work-items in all work-groups can access global memory, so data sharing and communication can occur through global memory. However, due to its lower bandwidth and higher latency, sharing and communication through global memory is less efficient. On the other hand, work-items in a sub-group executing simultaneously in a vector engine (VE) thread can share data and communicate with each other very efficiently, but the number of work-items in a sub-group is usually small and the scope of data sharing and communication is very limited. Memory with higher bandwidth and lower latency accessible to a bigger scope of work-items is very desirable for data sharing communication among work-items. The shared local memory (SLM) in Intel<sup>®</sup> GPUs is designed for this purpose.

Each X<sup>e</sup>-core of Intel GPUs has its own SLM. Access to the SLM is limited to the VEs in the X<sup>e</sup>-core or workitems in the same work-group scheduled to execute on the VEs of the same X<sup>e</sup>-core. It is local to a X<sup>e</sup>-core (or work-group) and shared by VEs in the same X<sup>e</sup>-core (or work-items in the same work-group), so it is called SLM. Because it is on-chip in each X<sup>e</sup>-core, the SLM has much higher bandwidth and much lower latency than global memory. Because it is accessible to all work-items in a work-group, the SLM can accommodate data sharing and communication among hundreds of work-items, depending on the workgroup size.

It is often helpful to think of SLM as a work-group managed cache. When a work-group starts, work-items in the work-group can explicitly load data from global memory into SLM. The data stays in SLM during the lifetime of the work-group for faster access. Before the work-group finishes, the data in the SLM can be explicitly written back to the global memory by the work-items. After the work-group completes execution, the data in SLM is also gone and invalid. Data consistency between the SLM and the global memory is the program’s responsibility. Properly using SLM can make a significant performance difference.

## Shared Local Memory Size and Work-group Size

Because it is on-chip, the SLM has limited size. How much memory is available to a work-group is devicedependent and can be obtained by querying the device, e.g.:

```cpp
std::cout << "Local Memory Size: "
          << q.get_device().get_info<sycl::info::device::local_mem_size>()
          << std::endl;
```

The output may look like:

```txt
Local Memory Size: 65536
```

The unit of the size is a byte. So this GPU device has 65,536 bytes or 64KB SLM for each work-group.

It is important to know the maximum SLM size a work-group can have. In a lot of cases, the total size of SLM available to a work-group is a non-constant function of the number of work-items in the work-group. The maximum SLM size can limit the total number of work-items in a group, i.e. work-group size. For example, if the maximum SLM size is 64KB and each work-item needs 512 bytes of SLM, the maximum work-group size cannot exceed 128.
````
