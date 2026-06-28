
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
