# oneapi_optimizations Source Lines 8909-9468

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L8909-L9468

Citation: [oneapi_optimizations:L8909-L9468]

````text
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

Intel<sup>®</sup> LLVM-based C/C++ and Fortran compilers, icx, icpx, and ifx, support OpenMP offloading onto GPUs. When using OpenMP, the programmer inserts device directives in the code to direct the compiler to offload certain parts of the application onto the GPU. Offloading compute-intensive code can yield better performance.

This section covers various topics related to OpenMP offloading, and how to improve the performance of offloaded code.

• OpenMP Directives

• OpenMP Execution Model

• Terminology

• Compiling and Running an OpenMP Application

• Offloading oneMKL Computations onto the GPU

• Tools for Analyzing Performance of OpenMP Applications

• OpenMP Offload Best Practices

## OpenMP Directives

Intel<sup>®</sup> compilers, icx, icpx, and ifx support various OpenMP directives that control the offloading of computations and mapping of data onto a device. These include:

• target

• teams

• distribute

• target data

• target enter data

• target exit data

• target update

• declare target

• dispatch

• interop

The target construct specifies that a specific part of the code is to be executed on the device and how data is to be mapped to the device.

The teams construct creates a number of thread teams, where each team is composed of a master thread and a number of worker threads. If teams is specified without the num\_teams clause, then the number of teams is implementation defined.

The distribute construct distributes iterations of a loop among the master threads of the teams, so each master thread executes a subset of the iterations.

The target data construct maps variables to a device data environment. Variables are mapped for the extent of the target data region, according to any map clauses.

The target enter data directive specifies that variables are mapped to a device. With this directive, the map-type specified in map clauses must be either to or alloc.

The target exit data directive specifies that variables are unmapped from the device. With this directive, the map-type specified in map clauses must be from, release, or delete.

The target update directive makes the values of variables on the device consistent with their original host variables, according to the specified motion clauses.

The declare target directive specifies that variables, functions (C, C++ and Fortran), and subroutines (Fortran) are mapped to a device.

The declare variant directive declares a specialized variant of a base function and specifies the context in which that specialized variant is used.

The dispatch construct controls whether variant substitution occurs for a given function call.

The interop construct retrieves interoperability properties from the OpenMP implementation to enable interoperability with foreign execution contexts.

The map clause determines how an original host variable is mapped to a corresponding variable on the device. Map-types include:

• to: The value of the original host variable is copied to the device on entry to the target region.

• from: The value of the variable on the device is copied from the device to the original host variable on exit from the target region.

• tofrom: The value of the original host variable is copied to the device on entry to the target region, and copied back to the host on exit from the target region.

• alloc: Allocate an uninitialized copy of the original host variable on the device (values are not copied from the host to the device).

Directives can be combined. For example, the following combined directives may be used:

• target teams

• target teams distribute

• target teams distribute parallel for

• target teams distribute parallel for simd

It is recommended that combined directives be used where possible because they allow the compiler and runtime to decide how to best partition the iterations of an offloaded loop for execution on the GPU.

## OpenMP Execution Model

The OpenMP execution model has a single host device but multiple target devices. A device is a logical execution engine with its own local storage and data environment.

When executing on Intel<sup>®</sup> Data Center GPU Max Series, the entire GPU (which may have multiple stacks) can be considered as a device, or each stack can be considered as a device.

OpenMP starts executing on the host. When a host thread encounters a target construct, data is transferred from the host to the device (if specified by map clauses, for example), and code in the construct is offloaded onto the device. At the end of the target region, data is transferred from the device to the host (if so specified).

By default, the host thread that encounters the target construct waits for the target region to finish before proceeding further. nowait on a target construct specifies that the host thread does not need to wait for the target region to finish. In other words, the nowait clause allows the asynchronous execution of the target region.

Synchronizations between regions of the code executing asynchronously can be achieved via the taskwait directive, depend clauses, (implicit or explicit) barriers, or other synchronization mechanisms.

## Terminology

In this chapter, OpenMP and SYCL terminology is used interchangeably to describe the partitioning of iterations of an offloaded parallel loop.

As described in the “SYCL Thread Hierarchy and Mapping” chapter, the iterations of a parallel loop (execution range) offloaded onto the GPU are divided into work-groups, sub-groups, and work-items. The ND-range represents the total execution range, which is divided into work-groups of equal size. A work-group is a 1-, 2-, or 3-dimensional set of work-items. Each work-group can be divided into sub-groups. A sub-group represents a short range of consecutive work-items that are processed together as a SIMD vector.

The following table shows how SYCL concepts map to OpenMP and CUDA concepts.

<table><tr><td>SYCL</td><td>OpenMP</td><td>CUDA</td></tr><tr><td>Work-item</td><td>OpenMP thread or SIMD lane</td><td>CUDA thread</td></tr><tr><td>Work-group</td><td>Team</td><td>Thread block</td></tr><tr><td>Work-group size</td><td>Team size</td><td>Thread block size</td></tr><tr><td>Number of work-groups</td><td>Number of teams</td><td>Number of thread blocks</td></tr><tr><td>Sub-group</td><td>SIMD chunk (simdlen = 8, 16, 32)</td><td>Warp (size = 32)</td></tr><tr><td>Maximum number of work-items per work-group</td><td>Thread limit</td><td>Maximum number of of CUDA threads per thread block</td></tr></table>

## Compiling and Running an OpenMP Application

Use the following compiler options to enable OpenMP offload onto Intel<sup>®</sup> GPUs. These options apply to both C/C++ and Fortran.

```batch
-fiopenmp -fopenmp-targets=spir64
```

By default the Intel<sup>®</sup> compiler converts the program into the intermediate language representation, SPIR-V, and stores that in the binary produced by the compilation process. The code can be run on any hardware platform by translating the SPIR-V code into the assembly code of the platform at runtime. This process is called Just-In-Time (JIT) compilation.

To enable the output of the compiler optimization report, add the following options:

```txt
-qopt-report=3 -03
```

## Note:

• The -qopenmp compiler option is equivalent to -fiopenmp, and the two options can be used interchangeably.
````
