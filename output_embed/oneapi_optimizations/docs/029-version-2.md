```fortran
include "mkl_omp_offload.f90"

subroutine init (a, b, c, m, k, n)
implicit none

real :: a(m, k), b(k,n), c(m,n)
integer m, k, n, i, j

do i = 1, m
    do j = 1, k
        a(i, j) = i
    end do
end do

do i = 1, k
    do j = 1, n
        b(i, j) = j - 1
    end do
end do

do i = 1, m
    do j = 1, n
```

```fortran
c(i, j) = 0.2 + i - j
end do
end do
end subroutine init

program main

#if defined(MKL_ILP64)
    use onemkl_blas_omp_offload_ilp64
#else
    use onemkl_blas_omp_offload_lp64
#endif
    use omp_lib
    use iso_fortran_env
    implicit none

    integer, parameter :: m = 1024
    integer, parameter :: k = 1024
    integer, parameter :: n = 1024
    integer, parameter :: iter = 2000
    real, allocatable :: a(:, :), b(:, :), c(:, :)
    real          :: alpha, beta, sum, total
    integer          :: i, j1, j2
    double precision   :: t0, t1

    !$omp allocators allocate(allocator(omp_target_shared_mem_alloc): a)
    allocate( a(1 : m, 1 : k) )

    !$omp allocators allocate(allocator(omp_target_shared_mem_alloc): b)
    allocate( b(1 : k, 1 : n) )

    !$omp allocators allocate(allocator(omp_target_shared_mem_alloc): c)
    allocate( c(1 : m, 1 : n) )

    ! Initialize.

    alpha = 1.025
    beta = 1.0
    total = 0.0
    call init (a, b, c, m, k, n)

    ! Compute sgemm on the device.

    t0 = omp_get_wtime()

    do i = 1, iter
        ! Update arrays a and b.
        a(:,:, ) = a(:,:, ) + 1
        b(:,:, ) = b(:,:, ) - 1

        ! Compute sgemm on the device.
        !$omp dispatch
        call sgemm('n','n',m,n,k,alpha,a,m,b,k,beta,c,m)

        sum = 0.0
        !$omp target teams distribute parallel do collapse(2) reduction(+:sum)
        do j1 = 1, m
```

```fortran
do j2 = 1, n
sum = sum + c(j1,j2)
enddo
enddo
!\$omp end target teams distribute parallel do

total = total + sum
end do

t1 = omp_get_wtime()

print *, "total = ", total
write (*, 120) " Number of iterations = ", iter
write (*, 130) " Time = ", t1-t0, " seconds"
120 format (A, I4)
130 format (A, F10.3, A)

! Deallocate arrays.
deallocate(a)
deallocate(b)
deallocate(c)

end program main
```

While this version is straightforward to program, it is not the most efficient.

## Version 2

In Version 2 of the program, we allocate the matrices in system memory using plain allocate, and use the map clause to map the matrices to the device.

```txt
allocate( a(1 : m, 1 : k) )
allocate( b(1 : k, 1 : n) )
allocate( c(1 : m, 1 : n) )
...
\$omp target data map(tofrom: a, b, c)
```

Since matrices a and b are updated on the host, we use the OpenMP target update to directive to copy the new values of the matrices from the host to the device.

```txt
a(:,:,)= a(:,:,)+ 1
b(:,:,)= b(:,:,)- 1

! Copy new values of a and b to the device.
!\$omp target update to (a, b)
```

The full Version 2 is shown below.

```fortran
include "mkl_omp_offload.f90"

subroutine init (a, b, c, m, k, n)
implicit none

real :: a(m, k), b(k,n), c(m,n)
integer m, k, n, i, j

do i = 1, m
    do j = 1, k
        a(i, j) = i
```

```fortran
end do
end do

do i = 1, k
    do j = 1, n
        b(i, j) = j - 1
    end do
end do

do i = 1, m
    do j = 1, n
        c(i, j) = 0.2 + i - j
    end do
end do
end subroutine init

program main

#if defined(MKL_ILP64)
    use onemkl_blas_omp_offload_ilp64
#else
    use onemkl_blas_omp_offload_lp64
#endif
    use omp_lib
    use iso_fortran_env
    implicit none

    integer, parameter :: m = 1024
    integer, parameter :: k = 1024
    integer, parameter :: n = 1024
    integer, parameter :: iter = 2000
    real, allocatable :: a(:, :), b(:, :), c(:, :)
    real          :: alpha, beta, sum, total
    integer          :: i, j1, j2
    double precision   :: t0, t1

    allocate( a(1 : m, 1 : k) )
    allocate( b(1 : k, 1 : n) )
    allocate( c(1 : m, 1 : n) )

    ! Initialize.

    alpha = 1.025
    beta = 1.0
    total = 0.0
    call init (a, b, c, m, k, n)

    ! Compute sgemm on the device.

    t0 = omp_get_wtime()

    !$omp target data map(to: a, b, c)

    do i = 1, iter
        ! Update arrays a and b on the host.
        a(:,:, ) = a(:,:, ) + 1
        b(:,:, ) = b(:,:, ) - 1
```

```fortran
! Copy new values of a and b to the device.
!$omp target update to (a, b)

! Compute sgemm on the device.
!$omp dispatch
call sgemm('n','n',m,n,k,alpha,a,m,b,k,beta,c,m)

sum = 0.0
!$omp target teams distribute parallel do collapse(2) reduction(+:sum)
do j1 = 1, m
    do j2 = 1, n
        sum = sum + c(j1,j2)
    enddo
enddo
!$omp end target teams distribute parallel do

total = total + sum
end do

!$omp end target data

t1 = omp_get_wtime()

print *, "total = ", total
write (*, 120) " Number of iterations = ", iter
write (*, 130) " Time = ", t1-t0, " seconds"
120 format (A, I4)
130 format (A, F10.3, A)

! Deallocate arrays.
deallocate(a)
deallocate(b)
deallocate(c)

end program main
```

## Version 3

In the third version of the program, we consider which matrices are used on the host only, on the device only, or on both the host and the device. We also consider whether the matrix values are updated during the execution of the program. This information is used to decide where to allocate the matrices, how to initialize them, and whether to update their values on the device.

Matrices a and b\`\`are accessed on both the host and the device, so we allocate them in host Unified Shared Memory (USM) then map them to the device using the \`\`map clause.

Matrix c is used as a work matrix on the device (to store the results of calls to sgemm), and it is not accessed on the host. So we allocate it directly on the device.

Since c is allocated on the device, we call init\_d() to initialize the matrix in an OpenMP target construct.

```txt
!\$omp allocators allocate(allocator(omp_target_shared_mem_alloc): a)
allocate( a(1 : m, 1 : k) )

!\$omp allocators allocate(allocator(omp_target_shared_mem_alloc): b)
allocate( b(1 : k, 1 : n) )

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): c)
```

```txt
allocate( c(1 : m, 1 : n) )
...
!$omp target data map(to: a, b)
...
! Copy new values of a and b to the device.
!$omp target update to (a, b)
```

The full Version 3 of the program is shown below.

```fortran
include "mkl_omp_offload.f90"

subroutine init (a, b, m, k, n)
implicit none
real :: a(m, k), b(k,n)
integer m, k, n, i, j

do i = 1, m
    do j = 1, k
        a(i, j) = i
    end do
end do

do i = 1, k
    do j = 1, n
        b(i, j) = j - 1
    end do
end do
end subroutine init

subroutine init_d (c, m, n)
implicit none
real :: c(m, n)
integer m, n, i, j

!\$omp target teams distribute parallel d
do i = 1, m
    do j = 1, n
        c(i, j) = 0.2 + i - j
    end do
end do
end subroutine init_d

program main

#if defined(MKL_ILP64)
    use onemkl_blas_omp_offload_ilp64
#else
    use onemkl_blas_omp_offload_lp64
#endif
    use omp_lib
    use iso_fortran_env
    implicit none

    integer, parameter  :: m = 1024
    integer, parameter  :: k = 1024
```

```fortran
integer, parameter  :: n = 1024
integer, parameter  :: iter = 2000
real, allocatable   :: a(:, :), b(:, :), c(:, :)
real             :: alpha, beta, sum, total
integer            :: i, j1, j2
double precision    :: t0, t1

!\$omp allocators allocate(allocator(omp_target_host_mem_alloc): a)
allocate( a(1 : m, 1 : k) )

!\$omp allocators allocate(allocator(omp_target_host_mem_alloc): b)
allocate( b(1 : k, 1 : n) )

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): c)
allocate( c(1 : m, 1 : n) )

! Initialize.

alpha = 1.025
beta  = 1.0
total = 0.0
call init (a, b, m, k, n)
call init_d (c, m, n)

! Compute sgemm on the device.

t0 = omp_get_wtime()

!\$omp target data map(to: a, b)

do i = 1, iter
    ! Update arrays a and b on the host.
    a(:,:, ) = a(:,:, ) + 1
    b(:,:, ) = b(:,:, ) - 1

    ! Copy new values of a and b to the device.
    !\$omp target update to (a, b)

    ! Compute sgemm on the device.
    !\$omp dispatch
    call sgemm('n','n',m,n,k,alpha,a,m,b,k,beta,c,m)

    sum = 0.0
    !\$omp target teams distribute parallel do collapse(2) reduction(+:sum)
    do j1 = 1, m
        do j2 = 1, n
            sum = sum + c(j1,j2)
        enddo
    enddo
    !\$omp end target teams distribute parallel do

    total = total + sum
end do

!\$omp end target data

t1 = omp_get_wtime()
```

```fortran
print *, "total = ", total
    write (*, 120) " Number of iterations = ", iter
    write (*, 130) " Time = ", t1-t0, " seconds"
format (A, I4)
format (A, F10.3, A)

! Deallocate arrays.
deallocate(a)
deallocate(b)
deallocate(c)

end program main
```

## Performance Comparison

The following commands were used to compile and run the various versions. In the commands, substitute the source filename for “TEST”.

```makefile
Compile:
ifx -O3 -fiopenmp -fopenmp-targets=spir64 -qmk1 -fpp -free TEST.f -o TEST.exe

Run:
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 ./TEST.exe
```

We compared the performance of the three versions on the particular GPU used (1-stack only). The run times were as follows:

```txt
Version 1 (test-SharedMem.f: 4.583 seconds
Version 2 (test-Map-UpdateTo.f): 2.157 seconds
Version 3 (test-DeviceMem-Map-UpdateTo.f): 1.340 seconds
```

## Clauses: is\_device\_ptr, use\_device\_ptr, has\_device\_addr, use\_device\_addr

The OpenMP clauses is\_device\_ptr, use\_device\_ptr, has\_device\_addr, and use\_device\_addr can be used to convey information about variables referenced in target, target data, or dispatch constructs. These clauses are described as follows.

## is\_device\_ptr

The is\_device\_ptr clause appears on a target or dispatch directive. It indicates that the list items are device pointers. So each list item is privatized inside the construct and the new list item is initialized to the device address to which the original list item refers.

• In C, each list item should be of type pointer or array.

• In C++, each list item should be of type pointer, array, reference to pointer, or reference to array.

• In Fortran, each list item should be of type C\_PTR.

The following C/C++ example illustrates the use of the is\_device\_ptr clause. The omp\_target\_alloc\_device routine allocates memory on the device and returns a device pointer for that memory which is saved in the host variable arr\_device. On the target directive, we use the is\_device\_ptr(arr\_device) clause to indicate that arr\_device points to device memory. So inside the target construct arr\_device is privatized and initialized to the device address to which arr\_device refers.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>
```

```c
#define N 100

int main(void)
{
    int *arr_host = NULL;
    int *arr_device = NULL;

    arr_host = (int *) malloc(N * sizeof(int));
    arr_device = (int *) omp_target_alloc_device(N * sizeof(int),
                             omp_get_default_device());

    #pragma omp target is_device_ptr(arr_device) map(from: arr_host[0:N])
    {
        for (int i = 0; i < N; ++i) {
            arr_device[i] = i;
            arr_host[i] = arr_device[i];
        }
    }

    printf ("%d, %d, %d \n", arr_host[0], arr_host[N/2], arr_host[N-1]);
}
```

## use\_device\_ptr

The use\_device\_ptr clause appears on a target data directive. It indicates that each list item is a pointer to an object that has corresponding storage on the device or is accessible on the device.

If a list item is a pointer to an object that is mapped to the device, then references to the list item in the construct are converted to references to a device pointer that is local to the construct and that refers to the device address of the corresponding object.

If the list item does not point to a mapped object, it must contain a valid device address, and the list item references are converted to references to a local device pointer that refers to this device address.

Each list item must be a pointer for which the value is the address of an object that has corresponding storage in the device data environment or is accessible on the target device.

In C, each list item should be of type pointer or array.

In C++, each list item should be of type pointer, array, reference to pointer, or reference to array.

In Fortran, each list item should be of type C\_PTR.

The following C/C++ example illustrates the use of the use\_device\_ptr clause. The omp\_target\_alloc\_device routine is called three times to allocate memory on the device. The addresses of the memory allocated is saved in the pointer variables A, B, and C on the host. We use the use\_device\_ptr(A, B,C) clause on the target data directive to indicate that A, B, and C contain valid device addresses.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>

#define length 65536

int main(void)
{
    int device_id = omp_get_default_device();
```

```c
size_t bytes = length*sizeof(double);
double * __restrict A;
double * __restrict B;
double * __restrict C;
double scalar = 3.0;
double ar;
double br;
double cr;
double asum;

// Allocate arrays in device memory

A = (double *) omp_target_alloc_device(bytes, device_id);
if (A == NULL) {
    printf(" ERROR: Cannot allocate space for A using omp_target_alloc_device().\n");
    exit(1);
}

B = (double *) omp_target_alloc_device(bytes, device_id);
if (B == NULL) {
    printf(" ERROR: Cannot allocate space for B using omp_target_alloc_device().\n");
    exit(1);
}

C = (double *) omp_target_alloc_device(bytes, device_id);
if (C == NULL) {
    printf(" ERROR: Cannot allocate space for C using omp_target_alloc_device().\n");
    exit(1);
}

#pragma omp target data use_device_ptr(A,B,C)
{
    // Initialize the arrays

    #pragma omp target teams distribute parallel for
    for (size_t i=0; i<length; i++) {
        A[i] = 2.0;
        B[i] = 2.0;
        C[i] = 0.0;
    }

    // Perform the computation

    #pragma omp target teams distribute parallel for
    for (size_t i=0; i<length; i++) {
        C[i] += A[i] + scalar * B[i];
    }

    // Validate and output results

    ar = 2.0;
    br = 2.0;
    cr = 0.0;
    for (int i=0; i<length; i++) {
        cr += ar + scalar * br;
    }

    asum = 0.0;
```

```c
#pragma omp target teams distribute parallel for reduction(+:asum)
    for (size_t i=0; i<length; i++) {
        asum += fabs(C[i]);
    }

} // end target data

omp_target_free(A, device_id);
omp_target_free(B, device_id);
omp_target_free(C, device_id);

double epsilon=1.e-8;
if (fabs(cr - asum)/asum > epsilon) {
    printf("Failed Validation on output array\n"
            "      Expected checksum: %lf\n"
            "      Observed checksum: %lf\n"
            "ERROR: solution did not validate\n", cr, asum);
    return 1;
} else {
    printf("Solution validates. Checksum = %lf\n", asum);
}

return 0;
}
```
