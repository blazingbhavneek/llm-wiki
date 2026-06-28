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

## has\_device\_addr

The has\_device\_addr clause appears on a target directive. It indicates that the list items already have valid device addresses, and therefore may be directly accessed from the device.

Each list item must have a valid device address for the device data environment. It can be on any type, including an array section.

The has\_device\_addr clause is especially useful in Fortran, because it can be used with list items of any type (not just C\_PTR) to indicate that the list items have device addresses.

The following Fortran example illustrates the use of the has\_device\_addr clause. In the example, the three arrays A, B, and C are allocated on the device. When the arrays are referenced in a target region, we use the has\_device\_addr(A, B, C) clause to indicate that A, B, and C already have device addresses.

```fortran
program main
  use iso_fortran_env
  use omp_lib
  implicit none

  integer, parameter :: iterations=1000
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
```

```fortran
!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): A)
allocate(A(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): B)
allocate(B(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): C)
allocate(C(length))

!
! Initialize the arrays

!\$omp target teams distribute parallel do has_device_addr(A, B, C)
do i = 1, length
    A(i) = 2.0
    B(i) = 2.0
    C(i) = 0.0
end do

!
! Perform the computation

nstream_time = omp_get_wtime()
do iter = 1, iterations
    !\$omp target teams distribute parallel do has_device_addr(A, B, C)
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
!\$omp target teams distribute parallel do reduction(+:asum) has_device_addr(C)
do i = 1, length
    asum = asum + abs(C(i))
end do

if (abs(cr - asum)/asum > epsilon) then
    print *, "Failed Validation on output array:", "Expected =", cr, "Observed =", asum else
    avgtime = nstream_time/iterations
    print *, "Solution validates:", "Checksum =", asum, "Avg time (s) =", avgtime endif

deallocate(A)
deallocate(B)
```

```txt
deallocate(C)
end program main
```

```txt
use_device_addr
```

The use\_device\_addr clause appears on a target data directive. It indicates that each list item already has corresponding storage on the device or is accessible on the device.

If a list item is mapped, then references to the list item in the construct are converted to references to the corresponding list item. If a list item is not mapped, it is assumed to be accessible on the device.

A list item may be an array section.

Just like has\_device\_addr, the use\_device\_addr clause is especially useful in Fortran, because it can be used with list items of any type (not just C\_PTR) to indicate that the list items have device addresses.

The following Fortran example illustrates the use of the use\_device\_addr clause. In the example, array\_d is mapped to the device with the alloc map-type, so storage is allocated for array\_d on the device and no data transfer between the host and the device occurs. We use the use\_device\_addr(array\_d) clause on the target data directive to indicate that array\_d has corresponding storage on the device.

```fortran
program target_use_device_addr

use omp_lib
use iso_fortran_env, only : real64
implicit none

integer, parameter :: N1 = 1024
real(kind=real64), parameter :: aval = real(42, real64)
real(kind=real64), allocatable :: array_d(:), array_h(:)
integer :: i,err

! Allocate host data
allocate(array_h(N1), array_d(1))

!$omp target data map (from:array_h(1:N1)) map(alloc:array_d(1:N1))
!$omp target data use_device_addr(array_d)
!$omp target has_device_addr(array_d)
    do i=1, N1
        array_d(i) = aval
        array_h(i) = array_d(i)
    end do
!$omp end target
!$omp end target data
!$omp end target data

! Check result
write (*,*) array_h(1), array_h(N1)
if (any(array_h /= aval)) then
    err = 1
else
    err = 0
end if

deallocate(array_h)
if (err == 1) then
    stop 1
else
```

```fortran
stop 0
end if

end program target_use_device_addr
```

The following table summarizes the properties of the clauses described in this section.

<table><tr><td>Clause</td><td>On which directive</td><td>Type of list item</td><td>Description</td></tr><tr><td>is_device_ptr</td><td>target, dispatch</td><td>C/C++: Pointer, array, or referenceFortran: C_PTR</td><td>Indicates that list item is a device pointer (has valid device address).</td></tr><tr><td>use_device_ptr</td><td>target data</td><td>C/C++: Pointer, array, or referenceFortran: C_PTR</td><td>Indicates that list item is a pointer to an object that has corresponding storage on device or is accessible on device.</td></tr><tr><td>has_device_addr</td><td>target</td><td>Any type (may be array section)</td><td>Indicates that list item has a valid device address.</td></tr><tr><td>use_device_addr</td><td>target data</td><td>Any type (may be array section)</td><td>Indicates that list item has corresponding storage on device or is accessible on the device.</td></tr></table>
