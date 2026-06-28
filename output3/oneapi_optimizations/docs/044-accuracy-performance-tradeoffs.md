
In the following example (a modified STREAM Triad) we have the classic STREAM Triad with several multiply and add operations where the variable multiplier and the number of multiply-add operations are determined by an input variable.

Below is a snippet of the original kernel code run on the device. The runtime variable inner\_loop\_size is used to set the loop upper bound.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    h.parallel_for<non_specialized_kernel>(array_size / 2, [=](auto idx) {
        // set trip count to runtime variable
        auto runtime_trip_count_const = inner_loop_size;
        auto accum = 0;
        for (size_t j = 0; j < runtime_trip_count_const; j++) {
            auto multiplier = scalar * j;
            accum = accum + A0[idx] + B0[idx] * multiplier;
        }
        C0[idx] = accum;
    });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

In order to improve performance, we use the specialization constant feature to specialize the variable inner\_loop\_size. Below is a snippet of the kernel code run on the device - using a specialization constant.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    // set specialization constant using runtime variable
    h.set_specialization_constant<trip_sc>(inner_loop_size);
    h.parallel_for<specialized_kernel>(
        array_size / 2, [=](auto idx, sycl::kernel_handler kh) {
            // set trip count to the now known specialization constant
            auto runtime_trip_count_const =
                kh.get_specialization_constant<trip_sc>();
            auto accum = 0;
            for (size_t j = 0; j < runtime_trip_count_const; j++) {
                auto multiplier = scalar * j;
                accum = accum + A0[idx] + B0[idx] * multiplier;
            }
            C0[idx] = accum;
        });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

We finally compare the specialization trip count value with the following example that uses a regular constant value. Below is a snippet of the kernel code run on the device using a regular constant.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    h.parallel_for<regular_constant_kernel>(array_size / 2, [=](auto idx) {
        // set trip count to known regular constant
        size_t runtime_trip_count_const = 10;
        auto accum = 0;
        for (size_t j = 0; j < runtime_trip_count_const; j++) {
            auto multiplier = scalar * j;
            accum = accum + A0[idx] + B0[idx] * multiplier;
        }
        C0[idx] = accum;
    });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

Timings from the runs of the three different versions are displayed below. The stream size represents the size of arrays A0, B0, and C0. The inner trip count represents the value of the runtime\_trip\_count\_const variable set using the specialization constant.

Displayed below are timing outputs for example runs of the different versions using a stream size of 134217728 elements (1024 MB) and an inner trip count of 10 as inputs.

Run with runtime variable: Time in sec (fastest run): 0.00161008

Run with specialization constant: Time in sec (fastest run): 0.00156256

Run with constant value: Time in sec (fastest run): 0.00155104

The results, as expected, show that using the specialization constant improves the performance of the computation on the device from the execution time seen with the runtime variable to one that more closely matches the execution time seen with the constant value. Furthermore, analysis of the generated code shows the specialized version of the application unrolls the main loop due to it’s added capability to specialize the loop trip count & JIT compile it as a known constant. We witness about inner\_loop\_size times (thus 10 times in this example) as many floating-point add instructions in the main loop of the program using specialization constants as compared to the one using a runtime variable.

## Accuracy Versus Performance Tradeoffs in Floating-Point Computations

Programmers of floating-point applications typically aim for the following two objectives:

• Accuracy: Produce results that are “close” to the result of the exact calculation.

• Performance: Produce an application that runs as fast as possible.

The two objectives usually conflict. However, good programming practices and judicious use of compiler options allow you to control the tradeoffs.

For more information, see the article: Consistency of Floating-Point Results using the Intel Compiler or Why doesn’t my application always give the same answer?, by Dr. Martyn J. Corden and David Kreitzer (2018)

In this section, we present some mechanisms (compiler options and source-level changes) that allow the programmer to control the semantics (and hence the accuracy and performance) of floating-point computations on the host as well as on the device. We describe compiler options for OpenMP and SYCL programs, and describe source-level changes in SYCL.

## OpenMP

In OpenMP, the following -fp-model options may be used to control the semantics of floating-point computations on the host as well as on the device.

1. -fp-model=precise

This option tells the compiler to strictly adhere to value-safe optimizations when implementing floating-point calculations. It disables optimizations (such as re-association, multiply by reciprocal, and zero folding) that can change the result of floating-point calculations. The increased accuracy that comes with -fpmodel=precise may result in lower performance.

1. -fp-model=fast

This option is the default for both host and device compilations at -O2 and above. The option tells the compiler to use more aggressive optimizations when implementing floating-point calculations. These optimizations increase speed but may affect the accuracy or reproducibility of floating-point computations.

In C/C++, the -fp-model=fast option is equivalent to the -ffast-math option. With this option (at -O2 and above), all 7 fast-math flags (nnan, ninf, nsz, arcp, contract, afn, reassoc) are set by the C/C++ front-end. (See https://llvm.org/docs/LangRef.html#fast-math-flags for a description of the fast-math flags in LLVM.)

In Fortran, on the other hand, the language rules dictate that we cannot set the nnan flag (No NaNs) by default. So the -fp-model=fast option (at -O2 and above) only sets the other 6 fast-math flags (ninf, nsz, arcp, contract, afn, reassoc). To set all 7 fast-math flags in Fortran, use the -ffast-math option.

```batch
1. -Xopenmp-target-backend "-options -cl-fast-relaxed-math"
```

The -fp-model=fast (or -ffast-math) option does not enable native math instructions on the Intel GPU (Intel<sup>®</sup> Data Center GPU Max Series). You need to compile with -Xopenmp-target-backend “-options - cl-fast-relaxed-math” to get native math instructions on the GPU. Native math instructions give even lower accuracy than what is allowed with -fp-model=fast.

-Xopenmp-target-backend “-options -cl-fast-relaxed-math” passes the -cl-fast-relaxed-math option to the backend in the compilation tool chain for the device. -cl-fast-relaxed-math relaxes the precision of commonly used math functions on the device. It offers a quick way to get performance gains for kernels with many math library function calls, as long as the accuracy requirements are satisfied by what is provided through native math instructions.

The -cl-fast-relaxed-math option affects the compilation of the entire program and does not permit fine control of the resulting numeric accuracy.

Note that Intel GPUs support native for single precision (float, real) only.

## Notes (OpenMP):

• When -fp-model is specified on the compilation command line (outside of the -fopenmptargets=spir64=”…” set of options), the -fp-model option applies to both the host and the device compilations. For example, the following compilation command specifies -fp-model=precise for both the host and the device compilations:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -fp-model=precise
```

You can specify different \`\`-fp-model\`\` keywords for the host and the device compilations as shown below.

• To specify -fp-model=fast for the host compilation, and -fp-model=precise for the device compilation:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64="-fp-model=precise" -fp-model=fast
Or:
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64="-fp-model=precise"
(No need to specify ``-fp-model=fast`` since it is the default at -O2 or higher.)
```

• To specify -fp-model=precise for the host compilation, and -fp-model=fast for the device compilation:

```shell
icx/icpx/ifx -O3 -fiopenmp -fopenmp-targets=spir64="-fp-model=fast" -fp-model=precise
```

• To specify -fp-model=fast for the host compilation, and relaxed-math for the device compilation:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -Xopenmp-target-backend "-options -cl-fast-relaxed-math" -fp-model=fast
Or:
icx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -Xopenmp-target-backend "-options -cl-fast-relaxed-math"
(No need to explicitly specify ``-fp-model=fast`` since it is the default at -O2 or higher.)
```

• You can combine the fast, precise, and relaxed-math options with -fimf-precision=low (medium or high) option to fine-tune precision on the host side. The -fimf-precision option is not supported on the device side currently.

The following table shows a summary of how to set the various options (precise, fast-math, relaxed math) in OpenMP to (a) both the host and the device (second column); (b) to the host only (third column); and (c) to the device only (fourth column).

OpenMP - Summary of Options

<table><tr><td>Floating Point Semantics</td><td>Apply to Host and Device Compilations</td><td>Apply to Host Compilation Only</td><td>Apply to Device Compilation Only</td></tr><tr><td>Precise</td><td>-fp-model=precise</td><td>-fp-model=precise, and specify ``-fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=fast&quot;</td><td>-fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=precise&quot;</td></tr><tr><td>Fast-math</td><td>-fp-model=fast (default)</td><td>-fp-model=fast, and specify -fiopenmp -fopenmp-targets=spir64=&quot;-fp-model= precise&quot;</td><td>-fp-model=precise, and specify -fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=fast&quot;</td></tr><tr><td>Relaxed-math (native instructions)</td><td>Applies to device only</td><td>Applies to device only</td><td>-Xopenmp-target-backend &quot;-options -cl-fast-relaxed-math&quot;</td></tr></table>

## SYCL

In SYCL, as in OpenMP, the -fp-model=fast and -fp-model=precise options may be used for both host and device compilations.

In SYCL, -fp-model=fast option is equivalent to the -ffast-math option, and is the default for both host and device compilations at -O2 and above.

To specify relaxed-math for device compilation, use the compiler option -Xsycl-target-backend “- options -cl-fast-relaxed-math”. You need to compile with this option to get native math instructions on the GPU.

Note that SYCL (and Intel GPUs) support native for single precision (float, real) only.

## Notes (SYCL):

• When -fp-model is specified on the compilation command line (outside of any -Xsycl-target option), the -fp-model option applies to both the host and the device compilations. For example, the following compilation command specifies -fp-model=precise for both the host and the device compilations:

```txt
icx/icpx/ifx -fsycl -fp-model=precise

You can specify different ``-fp-model`` keywords for the host and device compilations as shown below.
```

• To specify -fp-model=fast for the host compilation, and -fp-model=precise for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=precise" -fp-model=fast
Or:
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=precise"
(No need to specify ``-fp-model=fast`` since it is the default at -02 or higher.)
```

• To specify -fp-model=precise for the host compilation, and -fp-model=fast for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=fast" -fp-model=precise
```

• To specify -fp-model=fast for the host compilation, and relaxed-math for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-backend "-options -cl-fast-relaxed-math" -fp-model=fast
Or:
icx/icpx -fsycl -Xsycl-target-backend "-options -cl-fast-relaxed-math"
(No need to specify ``-fp-model=fast`` since it is the default at -02 or higher.)
```

The following table shows a summary of how to set the various options (math, fast-math, relaxed math) in SYCL to (a) both the host and the device (second column); (b) to the host only (third column); and (c) to the device only (fourth column).

SYCL - Summary of Options

<table><tr><td>Floating Point Semantics</td><td>Apply to Host and Device Compilations</td><td>Apply to Host Compilation Only</td><td>Apply to Device Compilation Only</td></tr><tr><td>Precise</td><td>-fp-model=precise</td><td>-fp-model=precise, and specify -Xsycl-target-frontend &quot;-fp-mode=fast&quot;</td><td>-Xsycl-target-frontend &quot;-fp-model=precise&quot;</td></tr><tr><td>Fast-math</td><td>-fp-model=fast (default)</td><td>-fp-model=fast, and specify -Xsycl-target-frontend &quot;-fp-model=precise&quot;</td><td>-fp-model=precise, and specify -Xsycl-target-frontend &quot;-fp-model=fast&quot;</td></tr><tr><td>Relaxed-math (native instructions)</td><td>Applies to device only</td><td>Applies to device only</td><td>-Xsycl-target-backend &quot;-options -cl-fast-relaxed-math&quot;</td></tr></table>

## Guidelines

In general, here are some guidelines for which options to use:

• Do not specify inconsistent options. The result will be unpredictable.

• The most commonly used option is -fp-model=fast for both host and device.

• Use relaxed-math for best performance on the device.

• Use -fp-model=precise for highest precision.

## Example: The log Function

The math library (a component of a programming language’s standard library) contains functions (or subroutines) for the most common mathematical functions, such as exponential, logarithmic, power, and trigonometric functions.

Different implementations of the math library functions may not have the same accuracy or be rounded in the same way. The value returned by a math library function may vary between one compiler release and another, due to algorithmic and optimization changes.

The accuracy of a math library function can be controlled via compiler options or via the source code. We use the log (natural logarithm) math function as an example to illustrate this.

## OpenMP / C++ (test\_log\_omp.cpp)

The following is an OpenMP C++ program that calls the std::log function on the device (from inside OpenMP target regions). The program includes the cmath header file which contains definitions for common math functions.

```cpp
#include <iostream>
#include <assert.h>
#include <chrono>
#include <cmath>

#if FP_SIZE == 32
    typedef float FP_TYPE;
    static constexpr FP_TYPE VALIDATION_THRESHOLD = 1e-3;
#elif FP_SIZE == 64
    typedef double FP_TYPE;
    static constexpr FP_TYPE VALIDATION_THRESHOLD = 1e-6;
#endif

template<typename T>
void do_work (unsigned NELEMENTS, unsigned NREPETITIONS, T initial_value, T *res)
{
    #pragma omp target teams distribute parallel for map(present,alloc:res[0:NELEMENTS])
    for (unsigned j = 0; j < NELEMENTS; j++)
    {
        T tmp = initial_value;
        for (unsigned i = 0; i < NREPETITIONS; ++i)
            tmp += std::log(tmp);
        res[j] = tmp;
    }
}

int main ()
{
    static constexpr unsigned NELEMENTS = 64*1024*1024;
    static constexpr unsigned NREPETITIONS = 1024;

    #pragma omp target
    { }

    FP_TYPE initial_value = 2;
    FP_TYPE ref_res = initial_value;
    for (unsigned i = 0; i < NREPETITIONS; ++i)
        ref_res += std::log(ref_res);
    std::cout << "reference result = " << ref_res << std::endl;

    {
        FP_TYPE * std_res = new FP_TYPE[NELEMENTS];
```

```cpp
assert (std_res != nullptr);

std::chrono::duration<float, std::micro> elapsed;
#pragma omp target data map(std_res[0:NELEMENTS])
{
    auto tbegin = std::chrono::system_clock::now();
    do_work<FP_TYPE> (NELEMENTS, NREPETITIONS, initial_value, std_res);
    auto tend = std::chrono::system_clock::now();
    elapsed = tend - tbegin;
}
std::cout << "std::log result[0] = " << std_res[0] << std::endl;

bool allequal = true;
for (unsigned i = 1; i < NELEMENTS; ++i)
    allequal = allequal and std_res[0] == std_res[i];
if (allequal)
{
    if (std::abs(ref_res - std_res[0])/std::abs(ref_res) < std::abs(VALIDATION_THRESHOLD))
        std::cout << "std::log validates. Total execution time is " << elapsed.count() << " us." << std::endl;
    else
        std::cout << "std::log does not validate (ref=" << ref_res << " std_res=" << std_res[0] << " mix=" << std::abs(ref_res - std_res[0])/std::abs(ref_res) << ")" << std::endl;
    }
    else
        std::cout << "std::log does not validate, results are not equal." << std::endl;

delete [] std_res;
}

return 0;
}
```

Sample compilation and run commands for test\_log\_omp.cpp:

```txt
icpx -O2 -fiopenmp -fopenmp-targets=spir64 test_log_omp.cpp \
    -DREAL_ELEMENT -DFP_SIZE=64 -fp-model=fast -fopenmp-version=51

OMP_TARGET_OFFLOAD=MANDATORY ./a.out
```

## OpenMP / Fortran (test\_log\_omp\_f\_mod.f90)

The following is a OpenMP Fortran module that calls the Fortran intrinsic math function, log, on the device (from inside OpenMP target regions):

```fortran
MODULE test

    USE ISO_C_BINDING

CONTAINS

    SUBROUTINE log_real_sp (nelements, nrepetitions, initial_value, res) bind(C,NAME='log_real_sp')
    IMPLICIT NONE
    INTEGER(KIND=C_INT), VALUE :: nelements, nrepetitions
    REAL(C_FLOAT), VALUE :: initial_value
    REAL(C_FLOAT) :: res(0:nelements-1), tmp
    INTEGER :: i, j

    !$OMP TARGET TEAMS DISTRIBUTE PARALLEL DO PRIVATE(tmp)
```

```txt
DO j = 0, nelements-1
    tmp = initial_value
    DO i = 0, nrepetitions-1
        tmp = tmp + log(tmp)
    END DO
    res(j) = tmp
END DO
RETURN
END SUBROUTINE log_real_sp

SUBROUTINE log_real_dp (nelements, nrepetitions, initial_value, res) bind(C,NAME='log_real_dp')
    IMPLICIT NONE
    INTEGER(KIND=C_INT), VALUE :: nelements, nrepetitions
    REAL(C_DOUBLE), VALUE :: initial_value
    REAL(C_DOUBLE) :: res(0:nelements-1), tmp
    INTEGER :: i, j

    !$OMP TARGET TEAMS DISTRIBUTE PARALLEL DO PRIVATE(tmp)
    DO j = 0, nelements-1
        tmp = initial_value
        DO i = 0, nrepetitions-1
            tmp = tmp + log(tmp)
        END DO
        res(j) = tmp
    END DO
    RETURN
END SUBROUTINE log_real_dp

END MODULE test
```

Sample compilation command for test\_log\_omp\_f.f90:

```txt
ifx -c -O2 -fiopenmp -fopenmp-targets=spir64 test_log_omp_f_mod.f90
```

## SYCL (test\_log\_sycl.cpp)

In SYCL, you can control floating point semantics at the source-level by choosing which math function to call. For example, the SYCL program below calls the following three different versions of the log function:

• std::log : Refers to the log function in the C++ standard library. The particular implementation chosen will be according to what the compiler options (-fp-model and -cl-fast-relaxed-math) prescribe. For example, to get the implementation that uses native math instructions, you need to compile with the - cl-fast-relaxed-math option.

• sycl::log : Refers to the log function in the sycl namespace that is provided by SYCL. This function may use native instructions, even when the -cl-fast-relaxed-math option is not specified. Precision is spelled out by the SYCL specification.

• sycl::native::log : Refers to the native log function in the sycl namespace that is provided by SYCL. This function uses native math instructions, and the -cl-fast-relaxed-math option is not needed. Note that SYCL (and Intel GPUs) support native for single precision (float, real) only. Precision is spelled out by the SYCL specification.

```cpp
#include <sycl/sycl.hpp>
#include <iostream>
#include <assert.h>
#include <chrono>
#include <cmath>

#if FP_SIZE == 32
    typedef float FP_TYPE;
```

```cpp
static constexpr FP_TYPE VALIDATION_THRESHOLD = 1e-3;
#elif FP_SIZE == 64
typedef double FP_TYPE;
static constexpr FP_TYPE VALIDATION_THRESHOLD = 1e-6;
#endif

template<typename T>
void do_work_std (sycl::queue &q, unsigned NELEMENTS, unsigned NREPETITIONS, T initial_value, T *res)
{
    q.submit([&](sycl::handler& h) {
        h.parallel_for(NELEMENTS, [=] (auto j)
        {
            FP_TYPE tmp = initial_value;
            for (unsigned i = 0; i < NREPETITIONS; ++i)
                tmp += std::log(tmp);
            res[j] = tmp;
        });
    }).wait();
}

template<typename T>
void do_work_sycl (sycl::queue &q, unsigned NELEMENTS, unsigned NREPETITIONS, T initial_value, T *res)
{
    q.submit([&](sycl::handler& h) {
        h.parallel_for(NELEMENTS, [=] (auto j)
        {
            FP_TYPE tmp = initial_value;
            for (unsigned i = 0; i < NREPETITIONS; ++i)
                tmp += sycl::log(tmp);
            res[j] = tmp;
        });
    }).wait();
}
# if FP_SIZE == 32
template<typename T>
void do_work_sycl_native (sycl::queue &q, unsigned NELEMENTS, unsigned NREPETITIONS, T initial_value, T *res)
{
    q.submit([&](sycl::handler& h) {
        h.parallel_for(NELEMENTS, [=] (auto j)
        {
            FP_TYPE tmp = initial_value;
            for (unsigned i = 0; i < NREPETITIONS; ++i)
                tmp += sycl::native::log(tmp);
            res[j] = tmp;
        });
    }).wait();
}
# endif

int main ()
{
    static constexpr unsigned NELEMENTS = 64*1024*1024;
    static constexpr unsigned NREPETITIONS = 1024;

    sycl::device d (sycl::gpu_selector_v);
```

```cpp
sycl::queue q (d);

q.submit([&](sycl::handler& h) {
    h.single_task ([=]() { });
}).wait();

FP_TYPE initial_value = 2;
FP_TYPE ref_res = initial_value;
for (unsigned i = 0; i < NREPETITIONS; ++i)
    ref_res += std::log(ref_res);
std::cout << "reference result = " << ref_res << std::endl;

{
    FP_TYPE * std_res = new FP_TYPE[NELEMENTS];
    assert (std_res != nullptr);

    std::chrono::duration<float, std::micro> elapsed;

    {
        auto * res = sycl::malloc_device<FP_TYPE>(NELEMENTS, q);
        auto tbegin = std::chrono::system_clock::now();
        do_work_std<FP_TYPE>(q, NELEMENTS, NREPETITIONS, initial_value, res);
        auto tend = std::chrono::system_clock::now();
        elapsed = tend - tbegin;
        q.memcpy (std_res, res, NELEMENTS*sizeof(FP_TYPE)).wait();
        sycl::free (res, q);
    }
    std::cout << "std::log result[0] = " << std_res[0] << std::endl;

    bool allequal = true;
    for (unsigned i = 1; i < NELEMENTS; ++i)
        allequal = allequal and std_res[0] == std_res[i];
    if (allequal)
    {
        if (std::abs(ref_res - std_res[0])/std::abs(ref_res) < std::abs(VALIDATION_THRESHOLD))
            std::cout << "std::log validates. Total execution time is " << elapsed.count() << " us." << std::endl;
        else
            std::cout << "std::log does not validate (ref=" << ref_res << " std_res=" << std_res[0] << " mix=" << std::abs(ref_res - std_res[0])/std::abs(ref_res) << ")" << std::endl;
    }
    else
        std::cout << "std::log does not validate, results are not equal." << std::endl;

    delete [] std_res;
}

{
    FP_TYPE * sycl_res = new FP_TYPE[NELEMENTS];
    assert (sycl_res != nullptr);

    std::chrono::duration<float, std::micro> elapsed;

    {
        auto * res = sycl::malloc_device<FP_TYPE>(NELEMENTS, q);
        auto tbegin = std::chrono::system_clock::now();
        do_work_sycl<FP_TYPE>(q, NELEMENTS, NREPETITIONS, initial_value, res);
```

```cpp
auto tend = std::chrono::system_clock::now();
elapsed = tend - tbegin;
qmemcpy (sycl_res, res, NELEMENTS*sizeof(FP_TYPE)).wait();
sycl::free (res, q);
}
std::cout << "sycl::log result[0] = " << sycl_res[0] << std::endl;

bool allequal = true;
for (unsigned i = 1; i < NELEMENTS; ++i)
    allequal = allequal and sycl_res[0] == sycl_res[i];
if (allequal)
{
    if (std::abs(ref_res - sycl_res[0])/std::abs(ref_res) < std::abs(VALIDATION_THRESHOLD))
        std::cout << "sycl::log validates. Total execution time is " << elapsed.count() << " us." << std::endl;
    else
        std::cout << "sycl::log does not validate (ref=" << ref_res << " sycl_res=" << sycl_res[0] << " mix=" << std::abs(ref_res - sycl_res[0])/std::abs(ref_res) << ")" << std::endl;
    }
    else
        std::cout << "sycl::log does not validate, results are not equal." << std::endl;

delete [] sycl_res;
}
# if FP_SIZE == 32
{
    FP_TYPE * sycl_native_res = new FP_TYPE[NELEMENTS];
    assert (sycl_native_res != nullptr);

    std::chrono::duration<float, std::micro> elapsed;

    {
        auto * res = sycl::malloc_device<FP_TYPE>(NELEMENTS, q);
        auto tbegin = std::chrono::system_clock::now();
        do_work_sycl_native<FP_TYPE>(q, NELEMENTS, NREPETITIONS, initial_value, res);
        auto tend = std::chrono::system_clock::now();
        elapsed = tend - tbegin;
        qmemcpy (sycl_native_res, res, NELEMENTS*sizeof(FP_TYPE)).wait();
        sycl::free (res, q);
    }
    std::cout << "sycl::native::log result[0] = " << sycl_native_res[0] << std::endl;

    bool allequal = true;
    for (unsigned i = 1; i < NELEMENTS; ++i)
        allequal = allequal and sycl_native_res[0] == sycl_native_res[i];
    if (allequal)
    {
        if (std::abs(ref_res - sycl_native_res[0])/std::abs(ref_res) < std::abs(VALIDATION_THRESHOLD))
            std::cout << "sycl::native::log validates. Total execution time is " << elapsed.count() << " us." << std::endl;
        else
            std::cout << "sycl::native::log does not validate (ref=" << ref_res << " sycl_native_res=" << sycl_native_res[0] << " mix=" << std::abs(ref_res - sycl_native_res[0])/std::abs(ref_res) << ")" << std::endl;
    }
    else
```

```cpp
std::cout << "sycl::native::log does not validate, results are not equal." << std::endl;

        delete [] sycl_native_res;
    }
# endif // FP_SIZE == 32

    return 0;
}
```

Sample compilation and run commands for test\_log\_sycl.cpp:

```batch
icpx -fsycl -O2 test_log_sycl.cpp -DREAL_ELEMENT -DFP_SIZE=64 -fp-model=fast
```

```batch
OMP_TARGET_OFFLOAD=MANDATORY ./a.out
```

## Performance Experiments

We present performance results when running the different programs (OpenMP C++, OpenMP Fortran and SYCL) that call the log function. On the particular Intel<sup>®</sup> Data Center GPU Max Series used (1-stack only), the performance of the log function, in single-precision was as follows.

Performance of log - Default Precision (Fast-math)

<table><tr><td>Version</td><td>Time (sec)</td></tr><tr><td>OpenMP/C++ (std::log)</td><td>93,118</td></tr><tr><td>OpenMP/Fortran (log)</td><td>94,342</td></tr><tr><td>SYCL (std::log)</td><td>31,835</td></tr><tr><td>SYCL (sycl::log)</td><td>31,644</td></tr><tr><td>SYCL (sycl::native::log)</td><td>31,684</td></tr></table>

Performance of log - Fast-math

<table><tr><td>Version</td><td>Time (sec)</td></tr><tr><td>OpenMP/C++ (std::log)</td><td>93,181</td></tr><tr><td>OpenMP/Fortran (log)</td><td>94,467</td></tr><tr><td>SYCL (std::log)</td><td>31,657</td></tr><tr><td>SYCL (sycl::log)</td><td>32,064</td></tr><tr><td>SYCL (sycl::native::log)</td><td>31,452</td></tr></table>

Performance of log - Precise

<table><tr><td>Version</td><td>Time (sec)</td></tr><tr><td>OpenMP/C++ (std::log)</td><td>92,971</td></tr><tr><td>OpenMP/Fortran (log)</td><td>94,444</td></tr><tr><td>SYCL (std::log)</td><td>94,592</td></tr><tr><td>SYCL (sycl::log)</td><td>94,852</td></tr><tr><td>SYCL (sycl::native::log)</td><td>40,778</td></tr></table>

Performance of log - Relaxed-math

<table><tr><td>Version</td><td>Time (sec)</td></tr><tr><td>OpenMP/C++ (std::log)</td><td>35,251</td></tr><tr><td>OpenMP/Fortran (log)</td><td>35,787</td></tr><tr><td>SYCL (std::log)</td><td>31,314</td></tr><tr><td>SYCL (sycl::log)</td><td>32,077</td></tr><tr><td>SYCL (sycl::native::log)</td><td>32,141</td></tr></table>

## Observations:

• In OpenMP (C and Fortran): std::log follows what the compiler options (-fp-model, -cl-relaxedmath) prescribe. The -cl-relaxed-math option is needed to use native instructions for std::log.

• In SYCL: sycl::log may use native instructions, even with just -fp-model=fast.

• In SYCL: sycl::native::log will always use native machine instructions. The -cl-relaxed-math option is not needed.

• In OpenMP and SYCL: When the -cl-relaxed-math option is specified, native machine instructions will be used for the log function on the device.

• -fp-model=precise produces more accurate results, but the performance will be lower.

## References

1. Consistency of Floating-Point Results using the Intel Compiler or Why doesn’t my application always

give the same answer?, by Dr. Martyn J. Corden and David Kreitzer (2018)

2. LLVM Language Reference Manual - Fast-Math Flags

3. Intel® oneAPI DPC++ Compiler documentation - User’s Manual

4. Intel® oneAPI DPC++/C++ Compiler Developer Guide and Reference - Alphabetical Option List

5. Intel oneAPI DPC++/C++ Compiler Developer Guide and Reference - Xopenmp-target

6. OpenCL Developer Guide for Intel® Core and Intel® Xeon Processors

7. Intel® SDK for OpenCL Applications Developer Guide

8. Target Toolchain Options

9. SYCL 2020 Specification - Math functions

10. SYCL 2020 Specification - SYCL built-in functions for SYCL host and device

11. The OpenCL Specification, Version 1.2, Khronos OpenCL Working Group

12. OpenCL™Developer Guide for Intel® Processor Graphics

## OpenMP Offloading Tuning Guide
