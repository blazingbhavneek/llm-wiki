# oneapi_optimizations Source Lines 9469-9854

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L9469-L9854

Citation: [oneapi_optimizations:L9469-L9854]

````text
## Ahead-Of-Time (AOT) Compilation

For Ahead-Of-Time (AOT) compilation for Intel<sup>®</sup> Data Center GPU Max Series, you need to specify an additional compiler option (-Xs), as shown below. This option applies to both C/C++ and Fortran.

```txt
-fiopenmp -fopenmp-targets=spir64_gen -Xs "-device pvc"
```

## OpenMP Runtime Routines

The following are some device-related runtime routines:

```ignorefile
omp_target_alloc
omp_target_free
omp_target_memcpy
```

The following runtime routines are supported by the Intel<sup>®</sup> compilers as Intel<sup>®</sup> extensions:

```txt
omp_target_alloc_host
omp_target_alloc_device
omp_target_alloc_shared
```

omp\_target\_free can be called to free up the memory allocated using the above Intel<sup>®</sup> extensions.

For a listing of OpenMP features supported in the icx, icpx, and ifx compilers, see:

• OpenMP Features and Extensions Supported in Intel® oneAPI DPC++/C++ Compiler

• Fortran Language and OpenMP Features Implemented in Intel® Fortran Compiler

## Environment Variables

Below are some environment variables that are useful for debugging or improving the performance of programs.

For additional information on environment variables, see:

• Intel® oneAPI DPC++/C++ Compiler Developer Guide and Reference - Supported Environment Variables

• Intel® oneAPI Programming Guide - Debug Tools

• LLVM/OpenMP Runtimes

• Debugging Variables for Level Zero Plugin

```txt
LIBOMPTARGET_DEBUG=1
```

Enables the display of debugging information from libomptarget.so.

```xml
LIBOMPTARGET_DEVICES=<DeviceKind>
```

Controls how sub-devices are exposed to users.

```txt
<DeviceKind> := DEVICE | SUBDEVICE | SUBSUBDEVICE |
        device | subdevice | subsubdevice
```

DEVICE/device: Only top-level devices are reported as OpenMP devices, and subdevice clause is supported.

SUBDEVICE/subdevice: Only 1st-level sub-devices are reported as OpenMP devices, and subdevice clause is ignored.

SUBSUBDEVICE/subsubdevice: Only second-level sub-devices are reported as OpenMP devices, and subdevice clause is ignored. On Intel<sup>®</sup> GPU using Level Zero backend, limiting the subsubdevice to a single compute slice within a stack also requires setting additional GPU compute runtime environment variable CFESingleSliceDispatchCCSMode=1.

The default is <DeviceKind>=device

```txt
LIBOMPTARGET_INFO=<Num>
```

Allows the user to request different types of runtime information from libomptarget. For details, see:

https://openmp.llvm.org/design/Runtimes.html#libomptarget-info

```txt
LIBOMPTARGET_LEVEL_ZERO_MEMORY_POOL=<Option>
```

Controls how reusable memory pool is configured.

```txt
<Option>          := 0 | <PoolInfoList>
<PoolInfoList> := <PoolInfo>[,<PoolInfoList>]
<PoolInfo>          := <MemType>[,<AllocMax>[,<Capacity>[,<PoolSize>]]]
<MemType>           := all | device | host | shared
<AllocMax>         := positive integer or empty, max allocation size in MB
<Capacity>          := positive integer or empty, number of allocations from
                    a single block
<PoolSize>         := positive integer or empty, max pool size in MB
```

Pool is a list of memory blocks that can serve at least <Capacity> allocations of up to <AllocMax> size from a single block, with total size not exceeding <PoolSize>.

```txt
LIBOMPTARGET_LEVEL_ZERO_STAGING_BUFFER_SIZE=<Num>
```

Sets the staging buffer size to <Num> KB. Staging buffer is used to optimize copy operation between host and device when host memory is not Unified Shared Memory (USM). The staging buffer is only used for discrete devices. The default staging buffer size is 16 KB.

```txt
LIBOMPTARGET_LEVEL_ZERO_USE_IMMEDIATE_COMMAND_LIST=<Value>
```

Enables/disables using immediate command list for kernel submission and/or memory copy operations.

```txt
<True> := 1 | T | t
<False> := 0 | F | f
<Bool> := <True> | <False>
<Value> := <Bool> | compute | COMPUTE | copy | COPY | all | ALL
```

• compute: Enables immediate command list for kernel submission.

• copy: Enables immediate command list for memory copy operations.

• all: Enables immediate command list for kernel submission and memory copy operations.

• <True>: Equivalent to compute’

• <False>: Immediate command list is disabled.

```txt
LIBOMPTARGET_PLUGIN=<Name>
```

Designates the offload plugin name to use.

```txt
<Name> := LEVEL_ZERO | OPENCL | X86_64 |
        level_zero | opencl | x86_64
```

By default, the offload plugin is LEVEL\_ZERO.

```txt
LIBOMPTARGET_PLUGIN_PROFILE=<Enable>[,<Unit>]
```

Enables basic plugin profiling and displays the result when the program finishes.

```txt
<Enable> := 1 | T
<Unit>   := usec | unit_usec
```

By default, plugin profiling is disabled.

if <Unit> is not specified, microsecond (usec) is the default unit

OMP\_TARGET\_OFFLOAD=MANDATORY

Specifies that program execution is terminated if a device construct or device memory routine is encountered and the device is not available or is not supported by the implementation.

Environment Variables to Control Implicit and Explicit Scaling

To disable implicit scaling and use one GPU stack only, set: ZE\_AFFINITY\_MASK=0

To enable explicit scaling, set: LIBOMPTARGET\_DEVICES=subdevice

On Intel<sup>®</sup> Data Center GPU Max Series, implicit scaling is on by default.

Environment Variables for SYCL

There are several SYCL\_PI\_LEVEL\_ZERO environment variables that are useful for the development and debugging of SYCL programs (not just OpenMP). They are documented at:

https://github.com/intel/llvm/blob/sycl/sycl/doc/EnvironmentVariables.md

## References

1. OpenMP Features and Extensions Supported in Intel® oneAPI DPC++/C++ Compiler

2. Fortran Language and OpenMP Features Implemented in Intel® Fortran Compiler

3. Intel® oneAPI DPC++/C++ Compiler Developer Guide and Reference - Supported Environment Variables

4. Intel® oneAPI Programming Guide - Debug Tools

5. LLVM/OpenMP Runtimes

6. Debugging Variables for Level Zero Plugin

7. Environment variables that effect DPC++ compiler and runtime

Offloading oneMKL Computations onto the GPU

The Intel<sup>®</sup> oneAPI Math Kernel Library (oneMKL) improves performance with math routines for software applications that solve large computational problems. oneMKL provides BLAS, Sparse BLAS, and LAPACK linear algebra routines, fast Fourier transforms, vectorized math functions, random number generation functions, and other functionality.

The oneMKL distribution includes an examples directory which contains examples of various calls to oneMKL routines.

For more information about the Intel<sup>®</sup> oneAPI Math Kernel Library, see:

• Developer Reference for Intel® oneAPI Math Kernel Library - C

• Developer Reference for Intel® oneAPI Math Kernel Library - Fortran

• Introducing Batch GEMM Operations

## Compilation Commands when Using oneMKL OpenMP Offload

The information in this section is specific to Linux.

The compilation command for a C/C++ or Fortran program that uses OpenMP threading and calls oneMKL API is as follows:

```makefile
C/C++: icx/icpx -fiopenmp -fopenmp-targets=spir64 -qmkl source.cpp
```

```batch
Fortran: ifx -fiopenmp -fopenmp-targets=spir64 -qmkl source.cpp
```

## A Note About Fortran

The Intel<sup>®</sup> oneMKL LP64 libraries index arrays with the 32-bit integer type; whereas the Intel<sup>®</sup> oneMKL ILP64 libraries use the 64-bit integer type (necessary for indexing large arrays, with more than 2<sup>31</sup> - 1 elements).

In a Fortran program, if indexing arrays with 32-bit integer type, include the following use statement in the program:

$$
\text {use onemkl\_blas\_omp\_offload\_lp64}
$$

On the other hand, if indexing arrays with 64-bit integer type, include the following use statement in the program:

```txt
use onemkl_blas_omp_offload_ilp64
```

A Note about the -qmkl Compiler Option

Use the -qmkl option (equivalent to -qmkl=parallel) to link with a certain Intel<sup>®</sup> oneAPI Math Kernel Library threading layer depending on the threading option provided:

• For -fiopenmp, the OpenMP threading layer for Intel<sup>®</sup> Compilers

• For -tbb, the Intel<sup>®</sup> Threading Building Blocks (Intel<sup>®</sup> TBB) threading layer

Use -qmkl=sequential to link with the sequential version of Intel<sup>®</sup> oneAPI Math Kernel Library.

Note that -qmkl=parallel/sequential affects threading on the CPU only. Offloaded MKL computations will always be parallelized as appropriate, and will occupy as many Vector Engines on the GPU as possible.

## OpenMP Directives to Offload oneMKL Computations

You can use OpenMP directives to offload oneMKL computations onto the GPU.

dispatch Directive

The recommended way to offload oneMKL computations onto the GPU is to use the OpenMP 5.1 dispatch directive. You would place the call to the oneMKL routine inside a dispatch construct, as shown in the example below.

```txt
#pragma omp target data map(to: A[0:m*k], B[0:k*n]) map(tofrom: C[0:m*n])
{
    #pragma omp dispatch
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                       m, n, k, alpha, A, k, B, n, beta, C, n);
}
```

In the above example, matrices a, b, and c should accessible on the device before the dispatch construct. When the MKL routine cblas\_dgemm is called from the dispatch construct, the corresponding device pointers for a, b, and c will be passed as arguments to the MKL routine, so the device copies of a, b, and c will be used in the computation.

The use\_device\_ptr clause is not needed on the dispatch directive. The list of device pointers needed by the oneMKL routine is given in the oneMKL OpenMP offload header file, mkl\_omp\_offload.h, where the GPU variant function is declared. The user should carefully review the list of device pointers required in the oneMKL header file and make sure that the corresponding matrices are accessible from the device before calling the oneMKL routine.

## Notes

• When using dispatch to offload oneMKL computations onto the GPU, oneMKL routines expect the arrays/ matrices to be accessible on the device before the computation is started. So the user has to map matrices a, b, and c to the device, or allocate the matrices directly on the device, or allocate the matrices in Unified Shared Memory (USM) before calling the oneMKL routine. See ::ref::openmp-bp-memoryallocation-link for more information about memory allocation.

• If a oneMKL routine is not called from a dispatch construct, or if offload is disabled, then the oneMKL computations will be executed on the CPU.

• Only one call to a oneMKL routine can be issued from an OpenMP dispatch construct. If there are two consecutive calls to oneMKL routines, then the calls should be placed in separate dispatch constructs.

• The use\_device\_ptr clause is not needed on the dispatch directive.

• Depending on the version of the compiler you are using, you may need to add the compiler option - fopenmp-version=51 in order for the dispatch directive to be accepted.

## Fortran

When calling oneMKL routines from Fortran code, be sure to add the following include statement:

```txt
include "mkl_omp_offload.f90"
```

Also, if calling oneMKL Fortran API with 32-bit integers, add the following module use statement:

```txt
use onemkl_blas_omp_offload_lp64
```

On the other hand, if calling oneMKL Fortran API with 64-bit integers, add the following module use statement:

```txt
use onemkl_blas_omp_offload_ilp64
```

The following Fortran example illustrates how DGEMM is called from a Fortran program, and the include and use statements mentioned above.

```txt
!\$omp target data map(to: a, b) map(tofrom: c2)
```

!\$omp dispatch

```csv
call DGEMM('N','N',m,n,k,alpha,a,m,b,k,beta,c2,m)
```

```txt
!\$omp end target data
```

To compile and link the above Fortran example with 32-bit integers:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -qmk1 -fpp -free -c dgemm_dispatch_f.f90
ifx -fiopenmp -fopenmp-targets=spir64 -qmk1 -fsycl -L\${MKLROOT}/lib/intel64 -liomp5 -lsycl -
lOpenCL -lstdc++ -lpthread -lm -ldl -lmkl_sycl dgemm_dispatch_f.o
```

To compile and link the above Fortran example with 64-bit integers:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -m64 -DMKL_ILP64 -i8 -fpp -free -c
dgemm_dispatch_f.f90
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -fsycl -L\${MKLROOT}/lib/intel64 -liomp5 -lsycl -
lOpenCL -lstdc++ -lpthread -lm -ldl -lmkl_sycl dgemm_dispatch_f.o
```

After generating the executable (a.out), from a C/C++ or Fortran program, you can run the executable under unitrace and look for the heading “Device Timing Results” in the generated trace. Below that heading we should see the oneMKL kernels listed. This way we confirm that oneMKL computations have been offloaded onto the GPU.

Example run command:

```shell
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 unitrace -h -d ./a.out
```

## Batching of oneMKL GEMM Calls

The oneMKL library includes “batch” routines that allow the user to batch several oneMKL calls into a single oneMKL call. At runtime, oneMKL will intelligently execute all of the matrix operations to optimize overall performance.

For example, the cblas\_dgemm routine computes a matrix-matrix product of two general matrices a and b, returning the result in a matrix c. The cblas\_dgemm interface is shown below.

```c
void cblas_dgemm (const CBLAS_LAYOUT layout,
const CBLAS_TRANSPOSE transa, const CBLAS_TRANSPOSE transb,
const MKL_INT m, const MKL_INT n, const MKL_INT k,
const double alpha, const double *a,
const MKL_INT lda, const double *b,
const MKL_INT ldb, const double beta,
double *c, const MKL_INT ldc);
```

The cblas\_dgemm\_batch routine is similar to the cblas\_dgemm routine, but the cblas\_dgemm\_batch routine performs matrix-matrix operations on groups of matrices, processing a number of groups at once.

The cblas\_dgemm\_batch interface is shown below. Note that the interface resembles the cblas\_dgemm interface. However, it involves passing matrix arguments as arrays of pointers to matrices, and passing parameters as arrays of parameters.

```txt
void cblas_dgemm_batch (const CBLAS_LAYOUT layout,
const CBLAS_TRANSPOSE* transa_array, const CBLAS_TRANSPOSE* transb_array,
const MKL_INT* m_array, const MKL_INT* n_array, const MKL_INT* k_array,
const double* alpha_array, const double **a_array,
const MKL_INT* lda_array, const double **b_array,
const MKL_INT* ldb_array, const double* beta_array,
double **c_array, const MKL_INT* ldc_array,
const MKL_INT group_count, const MKL_INT* group_size);
```

The batch operation is defined as follows:

```python
idx = 0
for i = 0 .. group_count - 1
    alpha and beta in alpha_array[i] and beta_array[i]
    for j = 0 .. group_size[i] - 1
        a, b, and c matrices in a_array[idx], b_array[idx], and c_array[idx], respectively
        c := alpha*op(a)*op(b) + beta*c,
        idx = idx + 1
    end for
end for
```
````
