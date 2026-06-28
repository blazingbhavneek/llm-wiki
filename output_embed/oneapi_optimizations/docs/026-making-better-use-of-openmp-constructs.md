```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <math.h>
#include <omp.h>

#define P 16
#define BLOCKS 8
#define SIZE (BLOCKS * P * P * P)

#define MAX 100
#define scaled_rand() ((rand() % MAX) / (1.0 * MAX))

#define IDX2(i, j) (i * P + j)
#define IDX4(b, i, j, k) (b * P * P * P + i * P * P + j * P + k)

#pragma omp declare target
double ur[SIZE], us[SIZE], ut[SIZE]; /* work arrays */
#pragma omp end declare target

int main(void) {
    double w[SIZE];          /* output */
    double u[SIZE], dx[P * P]; /* input */
    int b, i, j, k, l;        /* loop counters */
    double start, end;            /* timers */

    omp_set_default_device(0);
```

```c
/* dummy target region, so as not to measure startup time. */
#pragma omp target
{ ; }

/* initialize input with random values */
srand(0);
for (int i = 0; i < SIZE; i++)
    u[i] = scaled_rand();

for (int i = 0; i < P * P; i++)
    dx[i] = scaled_rand();

start = omp_get_wtime();

/* offload the kernel */
#pragma omp target teams distribute parallel for simd simdlen(16) collapse(4)
    map(to:u[0:SIZE],dx[0:P*P]) \
    map(from:w[0:SIZE])          \
    private(b,i,j,k,l)
for (b = 0; b < BLOCKS; b++) {
    for (i = 0; i < P; i++) {
        for (j = 0; j < P; j++) {
            for (k = 0; k < P; k++) {
                w[IDX4(b, i, j, k)] = 0.;
                ur[IDX4(b, i, j, k)] = 0.;
                us[IDX4(b, i, j, k)] = 0.;
                ut[IDX4(b, i, j, k)] = 0.;

                for (l = 0; l < P; l++) {
                    ur[IDX4(b, i, j, k)] += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
                    us[IDX4(b, i, j, k)] += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
                    ut[IDX4(b, i, j, k)] += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
                }

                w[IDX4(b, i, j, k)] = ur[IDX4(b, i, j, k)] * us[IDX4(b, i, j, k)] *
                    ut[IDX4(b, i, j, k)];
            }
        }
    }
}

end = omp_get_wtime();

/* print result */
printf("collapse-clause: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
```

In the above modified example, memory is allocated for arrays ur, us, and ut on the device, but no data transfers for these arrays take place. This is seen by grepping for "Libomptarget --> Moving" in LIBOMPTARGET\_DEBUG=1 output. We no longer see the transfer of 262,144 bytes from host to device for each of the arrays:

```txt
$ grep "Libomptarget --> Moving" test_declare_target.debug
Libomptarget --> Moving 2048 bytes (hst:0x00007ffc546bfec0) -> (tgt:0xff00fffffffee0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007ffc5467fec0) -> (tgt:0xff00ffffff30000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00fffffffef0000) -> (hst:0x00007ffc5463fec0)
```

An alternative approach for allocating memory on the device, without transferring any data between host and device, uses the map(alloc: ) clause instead of the map(to: ) clause, as shown below (lines 51-53).

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <math.h>
#include <omp.h>

#define P 16
#define BLOCKS 8
#define SIZE (BLOCKS * P * P * P)

#define MAX 100
#define scaled_rand() ((rand() % MAX) / (1.0 * MAX))

#define IDX2(i, j) (i * P + j)
#define IDX4(b, i, j, k) (b * P * P * P + i * P * P + j * P + k)

int main(void) {
    double w[SIZE];                      /* output */
    double u[SIZE], dx[P * P];          /* input */
    double ur[SIZE], us[SIZE], ut[SIZE]; /* work arrays */
    int b, i, j, k, l;                    /* loop counters */
    double start, end;                     /* timers */

    omp_set_default_device(0);

    /* dummy target region, so as not to measure startup time. */
    #pragma omp target
    { ; }

    /* initialize input with random values */
    srand(0);
    for (int i = 0; i < SIZE; i++)
        u[i] = scaled_rand();

    for (int i = 0; i < P * P; i++)
        dx[i] = scaled_rand();

    start = omp_get_wtime();

    /* offload the kernel */
    #pragma omp target teams distribute parallel for simd simdlen(16) collapse(4) \
        map(to:u[0:SIZE],dx[0:P*P]) \
        map(from:w[0:SIZE])         \
        map(alloc:ur[0:SIZE])         \
        map(alloc:us[0:SIZE])         \
        map(alloc:ut[0:SIZE])         \
        private(b,i,j,k,l)
    for (b = 0; b < BLOCKS; b++) {
        for (i = 0; i < P; i++) {
            for (j = 0; j < P; j++) {
                for (k = 0; k < P; k++) {
                    w[IDX4(b, i, j, k)] = 0.;
                    ur[IDX4(b, i, j, k)] = 0.;
                    us[IDX4(b, i, j, k)] = 0.;
                    ut[IDX4(b, i, j, k)] = 0.;
```

```c
for (l = 0; l < P; l++) {
    ur[IDX4(b, i, j, k)] += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
    us[IDX4(b, i, j, k)] += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
    ut[IDX4(b, i, j, k)] += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
}

w[IDX4(b, i, j, k)] = ur[IDX4(b, i, j, k)] * us[IDX4(b, i, j, k)] *
        ut[IDX4(b, i, j, k)];
}
}
}
}

end = omp_get_wtime();

/* print result */
printf("collapse-clause: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
}
```

In the above example, the map(alloc: ) clauses for arrays ur, us, and ut cause memory to be allocated for ur, us, and ut on the device, and no data transfers occur – as in the declare target and end declare target case:

```txt
$ grep "Libomptarget --> Moving" test_map_alloc.debug
Libomptarget --> Moving 2048 bytes (hst:0x00007ffd46f256c0) -> (tgt:0xff00fffffffee0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007ffd46ee56c0) -> (tgt:0xff00ffffffde0000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00fffffffef0000) -> (hst:0x00007ffd46ea56c0)
```

The performance of the various versions when running on the particular GPU used (1-stack only) was as follows:

```txt
map(to: ) version                      : 0.001430 seconds
declare target / end declare target version : 0.000874 seconds
map(alloc: ) version                       : 0.000991 seconds
```

## Making Better Use of OpenMP Constructs

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

## Memory Allocation

This section looks at various ways of allocating memory, and the types of allocations that are supported. A pointer on the host has the same size as a pointer on the device.

Host allocations are owned by the host and are intended to be allocated out of system memory. Host allocations are accessible by the host and all supported devices. Therefore, the same pointer to a host allocation may be used on the host and all supported devices. Host allocations are not expected to migrate between system memory and device-local memory. When a pointer to a host allocation is accessed on a device, data is typically sent over a bus, such as PCI-Express, that connects the device to the host.

Device allocations are owned by a specific device and are intended to be allocated out of device-local memory. Storage allocated can be read from and written to on that device, but is not directly accessible from the host or any other supported devices.

Shared allocations are accessible by the host and all supported devices. So the same pointer to a shared allocation may be used on the host and all supported devices, like in a host allocation. Shared allocations, however, are not owned by any particular device, but are intended to migrate between the host and one or more devices. This means that accesses on a device, after the migration has occurred, happen from much faster device-local memory instead of remotely accessing system memory though the higher-latency bus connection.

Shared-system allocations are a sub-class of shared allocations, where the memory is allocated by a system allocator (such as malloc or new) rather than by an allocation API (such as the OpenMP memory allocation API). Shared-system allocations have no associated device; they are inherently cross-device. Like other shared allocations, Shared-system allocations are intended to migrate between the host and supported devices, and the same pointer to a shared-system allocation may be used on the host and all supported devices.

## Note:

• Currently, shared-system allocations are not supported on Intel<sup>®</sup> Data Center GPU Max Series systems. However, shared allocations where memory is allocated by an allocation API are supported.

The following table summarizes the characteristics of the various types of memory allocation.

<table><tr><td>Type of allocation</td><td>Initial location</td><td>Accessible on host?</td><td>Accessible on device?</td></tr><tr><td>Host</td><td>Host</td><td>Yes</td><td>Yes</td></tr><tr><td>Device</td><td>Device</td><td>No</td><td>Yes</td></tr><tr><td>Shared</td><td>Host, Device, or Unspecified</td><td>Yes</td><td>Yes</td></tr><tr><td>Shared-System</td><td>Host</td><td>Yes</td><td>Yes</td></tr></table>

Host allocations offer wide accessibility (can be accessed directly from the host and all supported devices), but have potentially high per-access costs because data is typically sent over a bus such as PCI Express\*.

Shared allocations also offer wide accessibility, but the per-access costs are potentially lower than host allocations, because data is migrated to the accessing device.

Device allocations have access limitations (cannot be accessed directly from the host or other supported devices), but offer higher performance because accesses are to device-local memory.

## OpenMP Runtime Routines for Memory Allocation

Intel compilers support a number of OpenMP runtime routines for performing memory allocations. These routines are shown in the table below.

<table><tr><td>OpenMP memory allocation routine</td><td>Intel extension?</td><td>Type of allocation</td></tr><tr><td>omp_target_alloc</td><td>No</td><td>Device</td></tr><tr><td>omp_target_alloc_device</td><td>Yes</td><td>Device</td></tr><tr><td>omp_target_alloc_host</td><td>Yes</td><td>Host</td></tr><tr><td>omp_target_alloc_shared</td><td>Yes</td><td>Shared</td></tr></table>

Note that the three routines omp\_target\_alloc\_device, omp\_target\_alloc\_host, and omp\_target\_alloc\_shared are Intel extensions to the OpenMP specification.

The following examples use the above OpenMP memory allocation routines. Compare those to the ones using map clauses.

For more information about memory allocation, see:

• Data Parallel C++, by James Reinders et al.

• SYCL 2020 Specification

• oneAPI Level Zero Specification

• The SYCL part of this guide

## Using the map Clause

The first example uses map clauses to allocate memory on a device and copy data between the host and the device.

In the following example, arrays A, B, and C are allocated in system memory by calling the C/C++ standard library routine, malloc.

The target construct on line 58 is the main kernel that computes the values of array C on the device. The map(tofrom: C[0:length) clause is specified on this target construct since the values of C need to be transferred from the host to the device before the computation, and from the device to the host at the end of the computation. The map(to: A[0:length], B[0:length]) is specified for arrays\`\`A\`\` and B since the values of these arrays need to be transferred from the host to the device, and the device only reads these values. Under the covers, the map clauses cause storage for the arrays to be allocated on the device and data to be copied from the host to the device, and vice versa.

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
    size_t bytes = length*sizeof(double);
    double * __restrict A;
    double * __restrict B;
    double * __restrict C;
    double scalar = 3.0;
    double nstream_time = 0.0;

    // Allocate arrays on the host using plain malloc()

    A = (double *) malloc(bytes);
    if (A == NULL) {
        printf(" ERROR: Cannot allocate space for A using plain malloc().\n");
        exit(1);
    }

    B = (double *) malloc(bytes);
    if (B == NULL) {
        printf(" ERROR: Cannot allocate space for B using plain malloc().\n");
        exit(1);
    }

    C = (double *) malloc(bytes);
    if (C == NULL) {
        printf(" ERROR: Cannot allocate space for C using plain malloc().\n");
        exit(1);
```

```c
}

// Initialize the arrays

#pragma omp parallel for
for (size_t i=0; i<length; i++) {
    A[i] = 2.0;
    B[i] = 2.0;
    C[i] = 0.0;
}

// Perform the computation

nstream_time = omp_get_wtime();
for (int iter = 0; iter<iterations; iter++) {
    #pragma omp target teams distribute parallel for \
        map(to: A[0:length], B[0:length]) \
        map(tofrom: C[0:length])
    for (size_t i=0; i<length; i++) {
        C[i] += A[i] + scalar * B[i];
    }
}
nstream_time = omp_get_wtime() - nstream_time;

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
    asum += fabs(C[i]);
}

free(A);
free(B);
free(C);

double epsilon=1.e-8;
if (fabs(cr - asum)/asum > epsilon) {
    printf("Failed Validation on output array\n"
            "      Expected checksum: %lf\n"
            "      Observed checksum: %lf\n"
            "ERROR: solution did not validate\n", cr, asum);
    return 1;
} else {
    printf("Solution validates\n");
    double avgtime = nstream_time/iterations;
    printf("Checksum = %lf; Avg time (s): %lf\n", asum, avgtime);
}
```

```scss
return 0;
}
```

Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_target_map.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```
