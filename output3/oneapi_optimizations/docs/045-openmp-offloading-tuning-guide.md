
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
