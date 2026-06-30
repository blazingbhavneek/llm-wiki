# oneapi_optimizations Source Lines 7286-7658

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L7286-L7658

Citation: [oneapi_optimizations:L7286-L7658]

````text
## Optimizing Data Transfers in OpenMP

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

1. sycl\_ext\_oneapi\_copy\_optimize

2. Intel Compiler Extension Routines to OpenMP (C/C++)

3. Environment Variables — oneAPI DPC++ Compiler Documentation

## Avoiding Declaring Buffers in a Loop

When kernels are repeatedly launched inside a for-loop, you can prevent repeated allocation and freeing of a buffer by declaring the buffer outside the loop. Declaring a buffer inside the loop introduces repeated hostto-device and device-to-host memory copies.

In the following example, the kernel is repeatedly launched inside a for-loop. The buffer C is used as a temporary array, where it is used to hold values in an iteration, and the values assigned in one iteration are not used in any other iteration. Since the buffer C is declared inside the for-loop, it is allocated and freed in every loop iteration. In addition to the allocation and freeing of the buffer, the memory associated with the buffer is redundantly transferred from host to device and device to host in each iteration.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 25;
constexpr int STEPS = 100000;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Create 2 buffers, each holding N integers
    sycl::buffer<int> ABuf(&AData[0], N);
    sycl::buffer<int> BBuf(&BData[0], N);

    Q.submit([&](auto &h) {
        // Create device accessors.
        // The property no_init lets the runtime know that the
        // previous contents of the buffer can be discarded.
        sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
        sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(N, [=](auto i) {
```

```cpp
aA[i] = 10;
aB[i] = 20;
});
});

for (int j = 0; j < STEPS; j++) {
    sycl::buffer<int> CBuf(&CData[0], N);
    Q.submit([&](auto &h) {
        // Create device accessors.
        sycl::accessor aA(ABuf, h);
        sycl::accessor aB(BBuf, h);
        sycl::accessor aC(CBuf, h);
        h.parallel_for(N, [=](auto i) {
            aC[i] = (aA[i] < aB[i]) ? -1 : 1;
            aA[i] += aC[i];
            aB[i] -= aC[i];
        });
    });
} // end for

// Create host accessors.
const sycl::host_accessor haA(ABuf);
const sycl::host_accessor haB(BBuf);
printf("%d %d\n", haA[N / 2], haB[N / 2]);

return 0;
}
```

A better approach would be to declare the buffer C before the for-loop, so that it is allocated and freed only once, resulting in improved performance by avoiding the redundant data transfers between host and device. The following kernel shows this change.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 25;
constexpr int STEPS = 100000;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Create 3 buffers, each holding N integers
    sycl::buffer<int> ABuf(&AData[0], N);
    sycl::buffer<int> BBuf(&BData[0], N);
    sycl::buffer<int> CBuf(&CData[0], N);

    Q.submit([&](auto &h) {
        // Create device accessors.
        // The property no_init lets the runtime know that the
        // previous contents of the buffer can be discarded.
        sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
        sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(N, [=](auto i) {
            aA[i] = 10;
```

```cpp
aB[i] = 20;
});
});

for (int j = 0; j < STEPS; j++) {
    Q.submit([&](auto &h) {
        // Create device accessors.
        sycl::accessor aA(ABuf, h);
        sycl::accessor aB(BBuf, h);
        sycl::accessor aC(CBuf, h);
        h.parallel_for(N, [=](auto i) {
            aC[i] = (aA[i] < aB[i]) ? -1 : 1;
            aA[i] += aC[i];
            aB[i] -= aC[i];
        });
    });
} // end for

// Create host accessors.
const sycl::host_accessor haA(ABuf);
const sycl::host_accessor haB(BBuf);
printf("%d %d\n", haA[N / 2], haB[N / 2]);

return 0;
}
```

## Buffer Accessor Modes

In SYCL, a buffer provides an abstract view of memory that can be accessed by the host or a device. A buffer cannot be accessed directly through the buffer object. Instead, we must create an accessor object that allows us to access the buffer’s data.

The access mode describes how we intend to use the memory associated with the accessor in the program. The accessor’s access modes are used by the runtime to create an execution order for the kernels and perform data movement. This will ensure that kernels are executed in an order intended by the programmer. Depending on the capabilities of the underlying hardware, the runtime can execute kernels concurrently if the dependencies do not give rise to dependency violations or race conditions.

For better performance, make sure that the access modes of accessors reflect the operations performed by the kernel. The compiler will flag an error when a write is done on an accessor which is declared as read\_only. But the compiler does not change the declaration of an accessor form read\_write to read if no write is done in the kernel.

The following example shows three kernels. The first kernel initializes the A, B, and C buffers, so we specify that the access modes for these buffers is write\_only. The second kernel reads the A and B buffers, and reads and writes the C buffer, so we specify that the access mode for the A and B buffers is read\_only, and the access mode for the C buffer is read\_write.

The read\_only access mode informs the runtime that the data needs to be available on the device before the kernel can begin executing, but the data need not be copied from the device to the host at the end of the computation.

If this second kernel were to use read\_write for A and B instead of read\_only, then the memory associated with A and B is copied from the device to the host at the end of kernel execution, even though the data has not been modified by the device. Moreover, read\_write creates unnecessary dependencies. If another kernel that reads A or B is submitted within this block, this new kernel cannot start until the second kernel has completed.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Kernel1
    {
        // Create 3 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);
        sycl::buffer<int> CBuf(&CData[0], N);

        Q.submit([&](auto &h) {
            // Create device accessors.
            // The property no_init lets the runtime know that the
            // previous contents of the buffer can be discarded.
            sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aC(CBuf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(N, [=](auto i) {
                aA[i] = 11;
                aB[i] = 22;
                aC[i] = 0;
            });
        });
    } // end Kernel1

    // Kernel2
    {
        // Create 3 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);
        sycl::buffer<int> CBuf(&CData[0], N);

        Q.submit([&](auto &h) {
            // Create device accessors
            sycl::accessor aA(ABuf, h, sycl::read_only);
            sycl::accessor aB(BBuf, h, sycl::read_only);
            sycl::accessor aC(CBuf, h);
            h.parallel_for(N, [=](auto i) { aC[i] += aA[i] + aB[i]; });
        });
    } // end Kernel2

    // Buffers are destroyed and so CData is updated and can be accessed
```

```c
for (int i = 0; i < N; i++) {
    printf("%d\n", CData[i]);
}

return 0;
}
```
````
