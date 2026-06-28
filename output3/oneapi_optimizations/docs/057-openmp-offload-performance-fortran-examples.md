
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
