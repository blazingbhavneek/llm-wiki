
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
