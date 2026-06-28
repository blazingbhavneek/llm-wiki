
In OpenMP, the import (prepare) and release are done using the register and unregister APIs provided as an Intel extension to OpenMP. They give the programmer explicit control over the address range and the duration of the import.

## OpenMP Register and Unregister APIs

The interfaces for the OpenMP register and unregister APIs are as follows:

```python
int ompx_target_register_host_pointer
    (void *HostPtr, size_t numBytes, int DeviceNum)

void ompx_target_unregister_host_pointer
    (void *HostPtr, int DeviceNum)
```

See Intel Compiler Extension Routines to OpenMP (C/C++) for a description of the APIs.

The OpenMP register and unregister APIs are similar to the SYCL prepare and release APIs. When using the APIs, the onus is on the user to ensure correctness and safety with respect to the lifetime ranges.

## Notes:

• The register/unregister APIs can be called from Fortran as well as C/C++ code.

## OpenMP Examples

We present below three OpenMP examples (in Fortran) to illustrate the effect of memory allocation on performance.

In the examples, the main computation is done in a loop with iter iterations, where iter is 2000.

A target data directive is used to map matrices a, b, and c to the device before the start of the loop, and copy matrix c from the device to the host at the end of the loop.

In each iteration of the loop, the elements of a and b are updated on the host and the new values are copied to the device using the target update directive. This is followed by a call to sgemm which is computed on the device. sgemm multiplies matrices a and b on the device and stores the result in matrix c on the device.

The main computation is shown in the following snippet of code.

```fortran
!\$omp target data map(to: a, b) map(tofrom: c)

do i = 1, iter
    ! Update arrays a and b on the host.
    a(:,:, ) = a(:,:) + 1
    b(:,:) = b(:,:) - 1

    ! Copy new values of a and b to the device.
    !\$omp target update to (a, b)

    ! Compute sgemm on the device.
    !\$omp dispatch
    call sgemm('n','n',m,n,k,alpha,a,m,b,k,beta,c,m) end do

!\$omp end target data
```

Memory allocation in each of the three OpenMP examples is described below.

## Example 1: Allocate matrices in system memory

In the first OpenMP example, openmp\_system\_mem.f, the matrices a, b, and c are allocated in system memory using the Fortran allocate statement.

```txt
allocate( a(1 : m, 1 : k) )
allocate( b(1 : k, 1 : n) )
allocate( c(1 : m, 1 : n) )
```

Example 2: Allocate matrices in host USM

In the second OpenMP example, openmp\_host\_usm.f, the matrices a, b, and c are allocated in host USM using the OpenMP allocators directive with the allocator omp\_target\_host\_mem\_alloc.

```txt
!\$omp allocators allocate(allocator(omp_target_host_mem_alloc): a)
allocate( a(1 : m, 1 : k) )

!\$omp allocators allocate(allocator(omp_target_host_mem_alloc): b)
allocate( b(1 : k, 1 : n) )

!\$omp allocators allocate(allocator(omp_target_host_mem_alloc): c)
allocate( c(1 : m, 1 : n) )
```

## Example 3: Allocate matrices in system memory and use register/unregister APIs

In the third OpenMP example, openmp\_register\_mem.f, the matrices a, b, and c are allocated in system memory using the Fortran allocate statement, just like in openmp\_system\_mem.f.

```txt
allocate( a(1 : m, 1 : k) )
allocate( b(1 : k, 1 : n) )
allocate( c(1 : m, 1 : n) )
```

Right after the matrices are allocated, the memory for the matrices is registered (imported).

```txt
stat = ompx_target_register_host_pointer(C_LOC(a), &
    sizeof(a), device_num)
stat = ompx_target_register_host_pointer(C_LOC(b), &
    sizeof(b), device_num)
stat = ompx_target_register_host_pointer(C_LOC(c), &
    sizeof(c), device_num)
```

Before the matrices are deallocated, they are unregistered (released).

```txt
call ompx_target_unregister_host_pointer(C_LOC(a), device_num)
call ompx_target_unregister_host_pointer(C_LOC(b), device_num)
call ompx_target_unregister_host_pointer(C_LOC(c), device_num)
```

## Performance Comparison

We compare the performance of the three OpenMP examples openmp\_sys\_usm.f, openmp\_host.f, and openmp\_register\_mem.f.

The compilation and run commands are as follows.

## Compilation commands:

```batch
ifx -03 -fiopenmp -fopenmp-targets=spir64 -qmkl -fpp -free openmp_system_mem.f -o
openmp_system_mem.exe

ifx -03 -fiopenmp -fopenmp-targets=spir64 -qmkl -fpp -free openmp_host_usm.f -o openmp_host_usm.e

ifx -03 -fiopenmp -fopenmp-targets=spir64 -qmkl -fpp -free openmp_register_mem.f -o
openmp_register_mem.exe
```

## Example run commands:

```batch
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 ./openmp_system_mem.exe
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 ./openmp_host_usm.exe
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 ./openmp_register_mem.exe
```

The performance of the three versions when running on the particular GPU used (1-stack only) was as follows.

<table><tr><td>Example</td><td>Total Time (sec)</td></tr><tr><td>openmp_system_mem.f</td><td>5.885</td></tr><tr><td>openmp_host_usm.f</td><td>5.223</td></tr><tr><td>openmp_register_mem.f</td><td>5.225</td></tr></table>

The above table shows that allocating the matrices in host USM (openmp\_host\_usm.f) performs better than allocating the matrices in system memory (openmp\_system\_mem.f).

The performance of the system memory version can be improved (openmp\_register\_mem.f) by calling the APIs, ompx\_target\_register\_host\_pointer() and ompx\_target\_unregister\_host\_pointer(), to register (import) the matrices before the computation in the loop and unregister (release) the matrices after the loop. As a result, the performance of openmp\_register\_mem.f matches that of openmp\_host\_usm.f.

## Performance Recommendations

For repeated data transfers between host and device, we recommend the following approaches:

1. Allocate data that will be the source or destination of repeated data transfers between host and device in host Unified Shared Memory (USM), rather than in system memory. By allocating the data in host USM, the data transfer rate is optimal. To allocate data in host USM:

• In SYCL, use the malloc\_host API.

• In OpenMP C/C++ and Fortran, use the omp\_target\_alloc\_host API.

• Alternatively, in OpenMP Fortran only, use the allocators directive with the allocator omp\_target\_host\_mem\_alloc.

2. If the above approach (1) cannot be applied, then import the system memory using the following APIs:

• In SYCL, use the prepare\_for\_device\_copy and release\_from\_device\_copy APIs shown above.

• In OpenMP (C/C++ and Fortran), use the ompx\_target\_register\_host\_pointer and ompx\_target\_unregister\_host\_pointer APIs shown above.

## References
