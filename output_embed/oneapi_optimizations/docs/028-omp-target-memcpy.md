## omp\_target\_memcpy

The following example shows how the runtime routine omp\_target\_memcpy may be used to copy memory from host to device, and from device to host. First arrays h\_A, h\_B, and h\_C are allocated in system memory using plain malloc, and then initialized. Corresponding arrays d\_A, d\_B, and d\_C are allocated on the device using omp\_target\_alloc.

Before the start of the target construct on line 104, the values in h\_A, h\_B, and h\_C are copied to d\_A, d\_B, and d\_C by calling omp\_target\_memcpy. After the target region, new d\_C values computed on the device are copied to h\_C by calling omp\_target\_memcpy.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>

#define iterations 100
#define length      64*1024*1024

int main(void)
{
    int device_id = omp_get_default_device();
    int host_id = omp_get_initial_device();
    size_t bytes = length*sizeof(double);
    double * __restrict h_A;
    double * __restrict h_B;
    double * __restrict h_C;
    double * __restrict d_A;
    double * __restrict d_B;
    double * __restrict d_C;
    double scalar = 3.0;
    double nstream_time = 0.0;

    // Allocate arrays h_A, h_B, and h_C on the host using plain malloc()

    h_A = (double *) malloc(bytes);
    if (h_A == NULL){
        printf(" ERROR: Cannot allocate space for h_A using plain malloc().\n");
        exit(1);
    }

    h_B = (double *) malloc(bytes);
    if (h_B == NULL){
        printf(" ERROR: Cannot allocate space for h_B using plain malloc().\n");
        exit(1);
    }

    h_C = (double *) malloc(bytes);
    if (h_C == NULL){
        printf(" ERROR: Cannot allocate space for h_C using plain malloc().\n");
        exit(1);
    }
```

```c
// Allocate arrays d_A, d_B, and d_C on the device using omp_target_alloc()

d_A = (double *) omp_target_alloc(bytes, device_id);
if (d_A == NULL){
    printf(" ERROR: Cannot allocate space for d_A using omp_target_alloc().\n");
    exit(1);
}

d_B = (double *) omp_target_alloc(bytes, device_id);
if (d_B == NULL){
    printf(" ERROR: Cannot allocate space for d_B using omp_target_alloc().\n");
    exit(1);
}

d_C = (double *) omp_target_alloc(bytes, device_id);
if (d_C == NULL){
    printf(" ERROR: Cannot allocate space for d_C using omp_target_alloc().\n");
    exit(1);
}

// Initialize the arrays on the host

#pragma omp parallel for
for (size_t i=0; i<length; i++) {
    h_A[i] = 2.0;
    h_B[i] = 2.0;
    h_C[i] = 0.0;
}

// Call omp_target_memcpy() to copy values from host to device

int rc = 0;
rc = omp_target_memcpy(d_A, h_A, bytes, 0, 0, device_id, host_id);
if (rc) {
    printf("ERROR: omp_target_memcpy(A) returned %d\n", rc);
    exit(1);
}

rc = omp_target_memcpy(d_B, h_B, bytes, 0, 0, device_id, host_id);
if (rc) {
    printf("ERROR: omp_target_memcpy(B) returned %d\n", rc);
    exit(1);
}

rc = omp_target_memcpy(d_C, h_C, bytes, 0, 0, device_id, host_id);
if (rc) {
    printf("ERROR: omp_target_memcpy(C) returned %d\n", rc);
    exit(1);
}

// Perform the computation

nstream_time = omp_get_wtime();
for (int iter = 0; iter<iterations; iter++) {
    #pragma omp target teams distribute parallel for \
        is_device_ptr(d_A,d_B,d_C)
    for (size_t i=0; i<length; i++) {
```

```c
d_C[i] += d_A[i] + scalar * d_B[i];
}
}
nstream_time = omp_get_wtime() - nstream_time;

// Call omp_target_memcpy() to copy values from device to host

rc = omp_target_memcpy(h_C, d_C, bytes, 0, 0, host_id, device_id);
if (rc) {
    printf("ERROR: omp_target_memcpy(A) returned %d\n", rc);
    exit(1);
}

// Validate and output results

double ar = 2.0;
double br = 2.0;
double cr = 0.0;
for (int iter = 0; iter<iterations; iter++) {
    for (int i=0; i<length; i++) {
        cr += ar + scalar * br;
    }
}

double asum = 0.0;
#pragma omp parallel for reduction(+:asum)
for (size_t i=0; i<length; i++) {
    asum += fabs(h_C[i]);
}

free(h_A);
free(h_B);
free(h_C);
omp_target_free(d_A, device_id);
omp_target_free(d_B, device_id);
omp_target_free(d_C, device_id);

double epsilon=1.e-8;
if (fabs(cr - asum)/asum > epsilon) {
    printf("Failed Validation on output array\n"
            "       Expected checksum: %lf\n"
            "       Observed checksum: %lf\n"
            "ERROR: solution did not validate\n", cr, asum);
    return 1;
} else {
    printf("Solution validates\n");
    double avgtime = nstream_time/iterations;
    printf("Checksum = %lf; Avg time (s): %lf\n", asum, avgtime);
}

return 0;
}
```

## Performance Considerations

In the above examples (using the map clause, omp\_target\_alloc, omp\_target\_alloc\_device, omp\_target\_alloc\_host, omp\_target\_alloc\_shared, omp\_target\_memcpy), the main kernel is the target construct that computes the values of array C. To get more accurate timings, this target construct is enclosed in a loop, so the offload happens iterations number of times (where iterations = 100). The average kernel time is computed by dividing the total time taken by the iterations loop by 100.

```c
// Perform the computation 'iterations' number of times

nstream_time = omp_get_wtime();
for (int iter = 0; iter<iterations; iter++) {
    #pragma omp target teams distribute parallel for \
        is_device_ptr(A,B,C)
    for (size_t i=0; i<length; i++) {
        C[i] += A[i] + scalar * B[i];
    }
}
nstream_time = omp_get_wtime() - nstream_time;
```

LIBOMPTARGET\_DEBUG=1 output shows that all the above examples have the same ND\_range partitioning.

```txt
Target LEVEL0 RTL --> Allocated a device memory 0xff00000020200000
Libomptarget --> omp_target_alloc returns device ptr 0xff00000020200000
Libomptarget --> Call to omp_target_alloc for device 0 requesting 536870912 bytes
Libomptarget --> Call to omp_get_num_devices returning 1
Libomptarget --> Call to omp_get_initial_device returning 1
Libomptarget --> Checking whether device 0 is ready.
Libomptarget --> Is the device 0 (local ID 0) initialized? 1
Libomptarget --> Device 0 is ready to use.
```

The following table shows the average times taken by the kernel in the various versions when running on the particular GPU used (1-stack only).

<table><tr><td>Version</td><td>Time (seconds)</td></tr><tr><td>map</td><td>0.183604</td></tr><tr><td>map + target data</td><td>0.012757</td></tr><tr><td>omp_target_alloc</td><td>0.002501</td></tr><tr><td>omp_target_alloc_device</td><td>0.002499</td></tr><tr><td>omp_target_alloc_host</td><td>0.074412</td></tr><tr><td>omp_target_alloc_shared</td><td>0.012491</td></tr><tr><td>omp_target_memcpy</td><td>0.011072</td></tr></table>

The above performance numbers show that the map version is the slowest version (0.183604 seconds). This is because of the data transfers that occur at the beginning and end of each kernel launch. The main kernel is launched 100 times. At the beginning of each kernel launch, storage for arrays A, B and C is allocated on the device, and the values of these arrays are copied from the host to the device. At the end of the kernel, the values of array C are copied from the device to the host. Putting the whole iterations loop inside a target data construct with map clauses reduced the runtime to 0.012757 seconds, because the transfers occur once at the launch of the first kernel in the iterations loop, and again after the last kernel in that loop.

The omp\_target\_alloc and omp\_target\_alloc\_device versions have the best performance (0.002501 and 0.002499 seconds, respectively). In these versions, storage for A, B, and C is allocated directly in device memory, so accesses on the device happen from device-local memory. This is a useful model for applications that use scratch arrays on the device side. These arrays never need to be accessed on the host. In such cases, the recommendation is to allocate the scratch arrays on the device and not worry about data transfers, as illustrated in this example.

The omp\_target\_alloc\_shared version also performs well, but is somewhat slower (0.012491 seconds). In this version, storage for A, B, and C is allocated in shared memory. So the data can migrate between the host and the device. There is the overhead of migration but, after migration, accesses on the device happen from much faster device-local memory. In this version, the initialization of the arrays happens on the host. At the first kernel launch, the arrays are migrated to the device, and the kernels access the arrays locally on the device. Finally, before the host performs the reduction computation, the entire C array is migrated back to the host.

The omp\_target\_alloc\_host version (0.074412 seconds) takes almost 6x more time than the omp\_target\_alloc\_shared version. This is because data allocated in host memory does not migrate from the host to the device. When the kernel tries to access the data, the data is typically sent over a bus, such as PCI Express, that connects the device to the host. This is slower than accessing local device memory. If the device accesses only a small part of an array infrequently, then that array may be allocated in host memory using omp\_target\_alloc\_host. However, if the array is accessed frequently on the device side, then it should be kept in device memory. Keeping the data in host memory and accessing it over the PCI will degrade performance.

Finally, a note regarding data transfers: The amount of data transferred in the map version can be seen in LIBOMPTARGET\_DEBUG=1 output by grepping for "Libomptarget --> Moving". Notice that each launch of the main kernel yields the following data transfers:

```txt
$ grep "Libomptarget --> Moving" test_target_map.debug
Libomptarget --> Moving 536870912 bytes (hst:0x00007f1a5fc8b010) -> (tgt:0xff00000000200000)
Libomptarget --> Moving 536870912 bytes (hst:0x00007f1a9fc8d010) -> (tgt:0xff00000020200000)
Libomptarget --> Moving 536870912 bytes (hst:0x00007f1a7fc8c010) -> (tgt:0xff00000040200000)
Libomptarget --> Moving 536870912 bytes (tgt:0xff00000000200000) -> (hst:0x00007f1a5fc8b010)
```

On the other hand, data transfers in the omp\_target\_alloc\_... versions are handled by a lower layer of the runtime system. So grepping for "Libomptarget --> Moving" in LIBOMPTARGET\_DEBUG=1 output for these versions will not show the data transfers that took place.

## Fortran Examples

The Fortran version of the example using target data and map clauses is shown below.

```fortran
program main
use iso_fortran_env
use omp_lib
implicit none

integer, parameter :: iterations=100
integer, parameter :: length=64*1024*1024
real(kind=REAL64), parameter :: epsilon=1.D-8
real(kind=REAL64), allocatable :: A(:)
real(kind=REAL64), allocatable :: B(:)
real(kind=REAL64), allocatable :: C(:)
real(kind=REAL64) :: scalar=3.0
real(kind=REAL64) :: ar, br, cr, asum
real(kind=REAL64) :: nstream_time, avgtime
integer :: err, i, iter
```

```fortran
!
! Allocate arrays on the host using plain allocate
allocate( A(length), stat=err )
if (err .ne. 0) then
    print *, "Allocation of A returned ", err
    stop 1
endif

allocate( B(length), stat=err )
if (err .ne. 0) then
    print *, "Allocation of B returned ", err
    stop 1
endif

allocate( C(length), stat=err )
if (err .ne. 0) then
    print *, "Allocation of C returned ", err
    stop 1
endif

!
! Initialize the arrays

!\$omp parallel do
do i = 1, length
    A(i) = 2.0
    B(i) = 2.0
    C(i) = 0.0
end do

!
! Perform the computation

nstream_time = omp_get_wtime()
!\$omp target data map(to: A, B) map(tofrom: C)

do iter = 1, iterations
    !\$omp target teams distribute parallel do
    do i = 1, length
        C(i) = C(i) + A(i) + scalar * B(i)
    end do
end do

!\$omp end target data
nstream_time = omp_get_wtime() - nstream_time

!
! Validate and output results

ar = 2.0
br = 2.0
cr = 0.0
do iter = 1, iterations
    do i = 1, length
        cr = cr + ar + scalar * br
    end do
```

```txt
end do

asum = 0.0
!$omp parallel do reduction(+:asum)
do i = 1, length
    asum = asum + abs(C(i))
end do

if (abs(cr - asum)/asum > epsilon) then
    write(*,110) "Failed Validation on output array: Expected =", cr, ", Observed =", asum else
    avgtime = nstream_time/iterations
    write(*,120) "Solution validates: Checksum =", asum, ", Avg time (s) =",  avgtime endif

110 format (A, F20.6, A, F20.6)
120 format (A, F20.6, A, F10.6)

deallocate(A)
deallocate(B)
deallocate(C)

end program main
```

The Fortran version of the example using omp\_target\_alloc\_device is shown below. In this example, allocate directives, with the allocator omp\_target\_device\_mem\_alloc, are used to allocate arrays A, B, and C on the device. The use\_device\_addr(A, B, C) clause is used on the target data directive (line 37) to indicate that the arrays have device addresses, and these addresses should be used in the target region.

```fortran
use iso_fortran_env
use omp_lib
implicit none

integer, parameter :: iterations=100
integer, parameter :: length=64*1024*1024
real(kind=REAL64), parameter :: epsilon=1.D-8
real(kind=REAL64), allocatable :: A(:)
real(kind=REAL64), allocatable :: B(:)
real(kind=REAL64), allocatable :: C(:)
real(kind=REAL64) :: scalar=3.0
real(kind=REAL64) :: ar, br, cr, asum
real(kind=REAL64) :: nstream_time, avgtime
integer :: i, iter

!
! Allocate arrays in device memory

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): A)
allocate(A(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): B)
allocate(B(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): C)
allocate(C(length))

!
```

```fortran
! Begin target data

!\$omp target data use_device_addr(A, B, C)

!
! Initialize the arrays

!\$omp target teams distribute parallel do
do i = 1, length
    A(i) = 2.0
    B(i) = 2.0
    C(i) = 0.0
end do

!
! Perform the computation

nstream_time = omp_get_wtime()
do iter = 1, iterations
    !\$omp target teams distribute parallel do
    do i = 1, length
        C(i) = C(i) + A(i) + scalar * B(i)
    end do
end do
nstream_time = omp_get_wtime() - nstream_time

!
! Validate and output results

ar = 2.0
br = 2.0
cr = 0.0
do iter = 1, iterations
    do i = 1, length
        cr = cr + ar + scalar * br
    end do
end do

asum = 0.0
!\$omp target teams distribute parallel do reduction(+:asum) &
!\$omp map(tofrom: asum)
do i = 1, length
    asum = asum + abs(C(i))
end do

!
! End target data

!\$omp end target data

if (abs(cr - asum)/asum > epsilon) then
    write(*,110) "Failed Validation on output array: Expected =", cr, ", Observed =", asum else
    avgtime = nstream_time/iterations
    write(*,120) "Solution validates: Checksum =", asum, ", Avg time (s) =", avgtime endif

110 format (A, F20.6, A, F20.6)
```

```txt
120 format (A, F20.6, A, F10.6)

    deallocate(A)
    deallocate(B)
    deallocate(C)

    end program main
```

## Fortran Example

We will use an OpenMP Fortran example to illustrate how choosing memory allocations appropriately can avoid redundant data transfers and boost performance.

The example first allocates three matrices, a, b, and c. Then in each iteration of loop i, a and b are updated, sgemm is computed on the GPU with the result saved c, and a reduction computation is offloaded to the GPU.

Since matrices a and b are updated in every iteration of the loop, we need to make sure that the values of these matrices on the GPU are consistent with their values on the host before calling sgemm.

## Version 1

In the first (naive) version of the program, we allocate all three matrices in shared Unified Shared Memory (USM) using the allocate directive.

```txt
!\$omp allocators allocate(allocator(omp_target_shared_mem_alloc): a)
allocate( a(1 : m, 1 : k) )

!\$omp allocators allocate(allocator(omp_target_shared_mem_alloc): b)
allocate( b(1 : k, 1 : n) )

!\$omp allocators allocate(allocator(omp_target_shared_mem_alloc): c)
allocate( c(1 : m, 1 : n) )
```

Shared allocations are accessible by the host and the device, and automatically migrate between the host and the device as needed. So the same pointer to a Shared allocation may be used on the host and device.

The full Version 1 is shown below.
