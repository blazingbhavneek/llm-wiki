# oneapi_optimizations Source Lines 1320-1753

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L1320-L1753

Citation: [oneapi_optimizations:L1320-L1753]

````text
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

## Replacing Conditional Checks with Relational Functions

Another way to remove conditional checks is to replace them with relational functions, especially built-in relational functions. It is strongly recommended to use a built-in function if one is available. SYCL provides a rich set of built-in relational functions like select(), min(), max(). In many cases you can use these functions to replace conditional checks and achieve better performance.

Consider the convolution example again. The if-then-else conditional checks can be replaced with built-in functions min() and max().

```cpp
sycl::buffer<int> ibuf(input.data(), N);
sycl::buffer<int> obuf(output.data(), N);
sycl::buffer<int> kbuf(kernel.data(), M);
```

```cpp
auto e = q.submit([&](auto &h) {
    sycl::accessor iacc(ibuf, h, sycl::read_only);
    sycl::accessor oacc(obuf, h);
    sycl::accessor kacc(kbuf, h, sycl::read_only);

    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{256}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            int t = 0;
            int startj = sycl::max<int>(M / 2 - i, 0);
            int endj = sycl::min<int>(M / 2 + N - i, M);
            int startk = sycl::max<int>(i - M / 2, 0);
            for (int j = startj, k = startk; j < endj; j++, k++) {
                t += iacc[k] * kacc[j];
            }
            oacc[i] = t;
        });
});
```

## Registers and Performance

The register is the fastest storage in the memory hierarchy. Keeping data in registers as long as possible is critical to performance. But unfortunately, register space is limited and much smaller than memory space. The Intel<sup>®</sup> Data Center GPU Max Series product, for example, has 64KB general-purpose register file (GRF) space for each vector engine, or 128 general-purpose registers, each 64 bytes wide, for each XVE thread in small register mode.

Thus, the register space can be allocated only to a small set of variables at any point during execution. Fortunately, A given register can hold different variables at different times because different sets of variables are needed at different times.

In SYCL, the compiler allocates registers to private variables in work items. Multiple work items in a subgroup are packed into one XVE thread. The compiler aims to assign as many variables to registers as possible. By default, the compiler uses register pressure as one of the heuristics to choose SIMD width or sub-group size. High register pressures can result in smaller sub-group size (for example 16 instead of 32) if a sub-group size is not explicitly requested. It can also cause register spilling, i.e., moving some variables currently in registers to memory to make room for other variables, or cause certain variables not to be promoted to registers.

The hardware may not be fully utilized if sub-group size or SIMD width is not the maximum the hardware supports. Memory traffic can be increased if register spills or accesses to not-promoted-to-register variables occur inside hot loops. In both cases, performance can be significantly degraded.

Though the compiler uses intelligent algorithms to allocate variables in registers and to minimize register spills, optimizations by developers can help the compiler to do a better job and often make a big performance difference.

• Finding Kernels with Register Spills

• Small Register Mode vs. Large Register Mode

• Optimizing Register Spills

• Porting Code with High Register Pressure to Intel<sup>®</sup> Max GPUs

## Finding Kernels with Register Spills

The compiler outputs a warning if a kernel is compiled ahead of time and has register spills:

```shell
$ icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc"
app.cpp
```

```txt
Compilation from IR - skipping loading of FCL

warning: kernel _ZTSZ4mainEUlt_E0_ compiled SIMD32 allocated 128 regs and spilled around 396

Build succeeded.
```

However, the compiler does not report if a kernel has one or more private variables that are not prompted to registers.

The open source tool unitrace reports both kernels with register spills and kernels with not-prompted-toregister private variable(s). Plus, it works for both ahead-of-time compilation and just-in-time compilation:

```txt
$ icpx -fsycl app.cpp
$ unitrace -d ./a.out

...

== L0 Backend ==

Kernel, Calls, Time(ns), Time(%), Average(ns), Min(ns), Max(ns)
main::{lambda(auto:1)#4}, 100, 91349596800, 99.896, 913495968, 913304160, 913975360
main::{lambda(auto:1)#3}, 100, 77196960, 0.084, 771969, 2080, 76974560
main::{lambda(auto:1)#5}, 500, 4981120, 0.005, 9962, 1440, 42880
main::{lambda(auto:1)#7}, 500, 4600000, 0.005, 9200, 1440, 38720
main::{lambda(auto:1)#6}, 500, 4590880, 0.005, 9181, 1440, 39040
main::{lambda(auto:1)#1}, 100, 3494400, 0.003, 34944, 1760, 3305120
main::{lambda(auto:1)#2}, 100, 189280, 0.000, 1892, 1440, 31360

=== Kernel Properties ===

Kernel, Private Memory Per Thread, Spill Memory Per Thread
main::{lambda(auto:1)#4}, 16384, 0
main::{lambda(auto:1)#3}, 0, 8192
main::{lambda(auto:1)#5}, 0, 0
main::{lambda(auto:1)#7}, 0, 0
main::{lambda(auto:1)#6}, 0, 0
main::{lambda(auto:1)#1}, 0, 0
main::{lambda(auto:1)#2}, 0, 0
```

A non-zero value in bytes of the Spill Memory Per Thread indicates the kernel spills registers and a nonzero value in bytes of the Private Memory Per Thread indicates the kernel has at least one private variable that is not prompted to registers.

The tool also reports timing statistics for kernels executed on the device. These statistics can be helpful to developers to evaluate the performance impact of register spills and to prioritize the kernels to be optimized.

## Small Register Mode vs Large Register Mode

Intel<sup>®</sup> Data Center GPU Max Series products support two GRF modes: small GRF mode and large GRF mode. Each XVE has a total of 64 KB of register space In Small GRF mode, a single hardware thread can access 128 GRF registers, each of which is 64B wide. In this mode, 8 hardware threads are available per XVE. In Large GRF mode, a single hardware thread can access 256 GRF registers, each of which is 64B wide. In this mode, 4 hardware threads are available per XVE.

There are two ways to control how Intel<sup>®</sup> Graphics Compiler (IGC) selects between these two modes: (1) command line and (2) per-kernel specification. In this chapter, we provide a step-by-step guideline on how users can provide this control for both SYCL and OpenMP applications.

```shell
icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:large
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will force large GRF mode for all kernels

icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:auto
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis

icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:small
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will automatically use small GRF mode for all kernels
```

```shell
icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:large
test.cpp
// IGC will force large GRF mode for all kernels

icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:auto
test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis

icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:small
test.cpp
// IGC will automatically use small GRF mode for all kernels
```

## GRF Mode Specification at Command Line

The -ftarget-register-alloc-mode=<arg> compiler option provides the ability to guide GRF mode selection in the IGC graphics compiler. The format of <arg> is Device0:Mode0[,Device1:Mode1...]. Currently the only supported Device is pvc. The supported modes are:

Provide no specification to IGC on the register file mode to select. Currently, IGC always chooses small register file mode with no specification.

Forces IGC to select small register file mode for ALL kernels

Forces IGC to select large register file mode for ALL kernels

Enables IGC to select small/large GRF mode on a per-kernel basis based on heuristics

If this option is not specified, IGC selects a GRF mode on a per-kernel basis based on heuristics on Linux for the Intel Data Center GPU Max Series and small GRF mode otherwise.

## OpenMP - GRF Mode Selection (AOT)

Following are the various commands that can be used to specify the requisite backend option during AOT compilation for OpenMP backends. Here, test.cpp can be any valid program:

## OpenMP - GRF Mode Selection (JIT)

Following are the various commands that can be used to specify the requisite backend option during JIT compilation for OpenMP backends. Here, test.cpp can be any valid program:

## SYCL – GRF Mode Selection (AOT)

Following are the various commands that can be used to specify the requisite backend option during AOT compilation for SYCL backends. Here, test.cpp can be any valid SYCL program:

```txt
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:large
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will force large GRF mode for all kernels
```

```shell
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:auto
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis
```

```txt
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:small
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will automatically use small GRF mode for all kernels
```

## SYCL – GRF Mode Selection (JIT)

Following are the various commands that can be used to specify the requisite backend option during JIT compilation for SYCL backends. Here, test.cpp can be any valid SYCL program:

```batch
icpx -fsycl
-ftarget-register-alloc-mode=pvc:large
test.cpp
// IGC will force large GRF mode for all kernels
```

```txt
icpx -fsycl
-ftarget-register-alloc-mode=pvc:auto
test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis
```

```batch
icpx -fsycl
-ftarget-register-alloc-mode=pvc:small
test.cpp
// IGC will automatically use small GRF mode for all kernels
```

## Performance Tuning Using GRF Mode Selection

This section discusses the impact of GRF mode selection on device code performance. The examples shown in this section use the OpenMP offloading model and JIT compilation flow. Two of the main features that govern GRF mode selection are the following: (1) Register pressure for kernel code (2) Number of parallel execution threads. Following is a code snippet containing an OpenMP offload region and this will be used in the forthcoming analysis.

```c
#pragma omp target teams distribute thread_limit(ZDIM *NX1 *NX1)
    for (int e = 0; e < nelt; e++) {
        double s_u[NX1 * NX1 * NX1];
        double s_D[NX1 * NX1];
        // SLM used for the three arrays here
        double s_ur[NX1 * NX1 * NX1];
        double s_us[NX1 * NX1 * NX1];
        double s_ut[NX1 * NX1 * NX1];

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
```

```txt
int k = inner / (NX1 * NX1);
    int j = (inner - k * NX1 * NX1) / NX1;
    int i = inner - k * NX1 * NX1 - j * NX1;
    if (k == 0)
        s_D[I2(i, j)] = D[I2(i, j)];
    for (; k < NX1; k += ZDIM) {
        s_u[I3(i, j, k)] = u[I4(i, j, k, e)];
    }
}

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
        int k = inner / (NX1 * NX1);
        int j = (inner - k * NX1 * NX1) / NX1;
        int i = inner - k * NX1 * NX1 - j * NX1;

        double r_G00, r_G01, r_G02, r_G11, r_G12, r_G22;

        for (; k < NX1; k += ZDIM) {
            double r_ur, r_us, r_ut;
            r_ur = r_us = r_ut = 0;
#ifdef FORCE_UNROLL
#pragma unroll NX1
#endif

        for (int m = 0; m < NX1; m++) {
            r_ur += s_D[I2(i, m)] * s_u[I3(m, j, k)];
            r_us += s_D[I2(j, m)] * s_u[I3(i, m, k)];
            r_ut += s_D[I2(k, m)] * s_u[I3(i, j, m)];
        }

        const unsigned gbase = 6 * I4(i, j, k, e);
        r_G00 = g[gbase + 0];
        r_G01 = g[gbase + 1];
        r_G02 = g[gbase + 2];
        s_ur[I3(i, j, k)] = r_G00 * r_ur + r_G01 * r_us + r_G02 * r_ut;
        r_G11 = g[gbase + 3];
        r_G12 = g[gbase + 4];
        s_us[I3(i, j, k)] = r_G01 * r_ur + r_G11 * r_us + r_G12 * r_ut;
        r_G22 = g[gbase + 5];
        s_ut[I3(i, j, k)] = r_G02 * r_ur + r_G12 * r_us + r_G22 * r_ut;
    }
}

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
        int k = inner / (NX1 * NX1);
        int j = (inner - k * NX1 * NX1) / NX1;
        int i = inner - k * NX1 * NX1 - j * NX1;
        for (; k < NX1; k += ZDIM) {
            double wr = 0.0;
            for (int m = 0; m < NX1; m++) {
                double s_D_i = s_D[I2(m, i)];
                double s_D_j = s_D[I2(m, j)];
                double s_D_k = s_D[I2(m, k)];
                wr += s_D_i * s_ur[I3(m, j, k)] + s_D_j * s_us[I3(i, m, k)] +
                    s_D_k * s_ut[I3(i, j, m)];
            }
            w[I4(i, j, k, e)] = wr;
```

```json
}
    }
}
```

There are two parameters that can be modified here: (1) Unroll factor of inner loop in line number 36 (2) Number of OpenMP teams specified in line number 1. The unroll factor can be used to control register pressure. Greater the unroll factor, higher will be the register pressure. Number of OpenMP teams can be used to control the number of parallel threads. In this discussion, kernel execution time on the device is used as metric for performance. Actual numbers are not provided as they may vary based on user environments and device settings. Following are some observations:

```txt
When unrolling is turned off, use of small GRF mode is found to provide better performance. This implies that the register pressure is not high enough to get any benefits out of using large GRF mode.

When unrolling is turned on, use of large GRF mode is found to provide better performance. This implies that the register pressure is high and large GRF mode is required to accommodate this pressure.

Increase in number of teams tends to result in better performance for larger (higher register pressure) workloads when using small GRF mode.
```
````
