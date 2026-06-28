
## Reduce Synchronizations Using nowait

If appropriate, use the nowait clause on the target construct to reduce synchronizations.

By default, there is an implicit barrier at the end of a target region, which ensures that the host thread that encountered the target construct cannot continue until the target region is complete.

Adding the nowait clause on the target construct eliminates this implicit barrier, so the host thread that encountered the target construct can continue even if the target region is not complete. This allows the target region to execute asynchronously on the device without requiring the host thread to idly wait for the target region to complete.

Consider the following example, which computes the product of two vectors, v1 and v2, in a parallel region (line 48). Half of the computations are performed on the host by the team of threads executing the parallel region. The other half of the computations are performed on the device. The master thread of the team launches a target region to do the computations on the device.

By default, the master thread of the team has to wait for the target region to complete before proceeding and participating in the computations (worksharing for loop) on the host.

```c
/*
 * This test is taken from OpenMP API 5.0.1 Examples (June 2020)
 * https://www.openmp.org/wp-content/uploads/openmp-examples-5-0-1.pdf
 * (4.13.2 nowait Clause on target Construct)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define N 100000 // N must be even

void init(int n, float *v1, float *v2) {
  int i;

  for(i=0; i<n; i++){
    v1[i] = i * 0.25;
    v2[i] = i - 1.25;
  }
}

int main() {
  int i, n=N;
  float v1[N],v2[N],vxv[N];
  double start,end; // timers

  init(n, v1, v2);

  /* Dummy parallel and target regions, so as not to measure startup
    time. */
  #pragma omp parallel
  {
    #pragma omp master
    #pragma omp target
      {;}
  }

  start=omp_get_wtime();

  #pragma omp parallel
  {
    #pragma omp master
    #pragma omp target teams distribute parallel for \
      map(to: v1[0:n/2])
      map(to: v2[0:n/2])
      map(from: vxv[0:n/2])
    for(i=0; i<n/2; i++){
      vxv[i] = v1[i]*v2[i];
    }
    /* Master thread will wait for target region to be completed
      before proceeding beyond this point. */

    #pragma omp for
    for(i=n/2; i<n; i++) {
```

```c
vxv[i] = v1[i]*v2[i];
}
/* Implicit barrier at end of worksharing for. */
}

end=omp_get_wtime();

printf("vxv[0]=%f, vxv[n-1]=%f, time=%lf\n", vxv[0], vxv[n-1], end-start);
return 0;
}
```

## Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_target_no_nowait.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

Performance could be improved if a nowait clause is specified on the target construct, so the master thread does not have to wait for the target region to complete and can proceed to work on the worksharing for loop. The target region is guaranteed to complete by the synchronization in the implicit barrier at the end of the worksharing for loop.

```c
/*
 * This test is taken from OpenMP API 5.0.1 Examples (June 2020)
 * https://www.openmp.org/wp-content/uploads/openmp-examples-5-0-1.pdf
 * (4.13.2 nowait Clause on target Construct)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define N 100000 // N must be even

void init(int n, float *v1, float *v2) {
  int i;

  for(i=0; i<n; i++){
    v1[i] = i * 0.25;
    v2[i] = i - 1.25;
  }
}

int main() {
  int i, n=N;
  float v1[N],v2[N],vxv[N];
  double start,end; // timers

  init(n, v1,v2);

  /* Dummy parallel and target (nowait) regions, so as not to measure startup time. */
  #pragma omp parallel
  {
    #pragma omp master
    #pragma omp target nowait
```

```txt
{;}
}

start=omp_get_wtime();

#pragma omp parallel
{
    #pragma omp master
    #pragma omp target teams distribute parallel for nowait \
        map(to: v1[0:n/2]) \
        map(to: v2[0:n/2]) \
        map(from: vxv[0:n/2])
    for(i=0; i<n/2; i++) {
        vxv[i] = v1[i]*v2[i];
    }

    #pragma omp for
    for(i=n/2; i<n; i++) {
        vxv[i] = v1[i]*v2[i];
    }
    /* Implicit barrier at end of worksharing for. Target region is guaranteed to be completed by this point. */
}

end=omp_get_wtime();

printf("vxv[1]=%f, vxv[n-1]=%f, time=%lf\n", vxv[1], vxv[n-1], end-start);
return 0;
}
```

The performance of the two versions when running on one of our lab machines was as follows:

```txt
no nowait version          : 0.008220 seconds
nowait on target version : 0.002110 seconds
```

## Fortran

The same nowait example shown above may be written in Fortran as follows.

```fortran
!
! This test is from OpenMP API 5.0.1 Examples (June 2020)
! https://www.openmp.org/wp-content/uploads/openmp-examples-5-0-1.pdf
!(4.13.2 nowait Clause on target Construct)
!
subroutine init(n, v1, v2)
integer :: i, n
real :: v1(n), v2(n)

do i = 1, n
    v1(i) = i * 0.25
    v2(i) = i - 1.25
end do
end subroutine init

program test_target_nowait
use omp_lib
use iso_fortran_env
implicit none
```

```fortran
integer, parameter :: NUM=100000 ! NUM must be even
real :: v1(NUM), v2(NUM), vxv(NUM)
integer :: n, i
real(kind=REAL64) :: start, end

n = NUM
call init(n, v1, v2)

! Dummy parallel and target (nowait) regions, so as not to measure
! startup time.
!$omp parallel
    !$omp master
        !$omp target nowait
        !$omp end target
    !$omp end master
!$omp end parallel

start=omp_get_wtime()

!$omp parallel

    !$omp master
        !$omp target teams distribute parallel do nowait &
        !$omp& map(to: v1(1:n/2)) &
        !$omp& map(to: v2(1:n/2)) &
        !$omp& map(from: vxv(1:n/2))
        do i = 1, n/2
            vxv(i) = v1(i)*v2(i)
        end do
    !$omp end master

    !$omp do
    do i = n/2+1, n
        vxv(i) = v1(i)*v2(i)
    end do

!$omp end parallel

end=omp_get_wtime()

write(*,110) "vxv(1)="", vxv(1), ", vxv(n-1)="", vxv(n-1), ", time=", end-start
110 format (A, F10.6, A, F17.6, A, F10.6)

end program test_target_nowait
```
