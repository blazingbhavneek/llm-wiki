The full example code is listed below.

```cpp
//
// Code example similar to the one in the OpenMP API 5.2.2 Examples document.
// The example uses SYCL foreign runtime and MKL.
//
// The example shows
// 1) How to initialize an interop object with SYCL queue access
// 2) How to check if the interop object is for SYCL foreign runtime
// 3) How to allocate SYCL memory object from the interop
// 4) How to use the interop object with the dispatch construct and MKL
//
// Compilation command (requires MKL):
// icpx -qopenmp -fopenmp-targets=spir64 -fsycl -qmkl omp_interop_sycl_2.cpp
//
#include <cstdio>
#include <cstdlib>
#include <mkl.h>
#include <mkl_omp_offload.h>
#include <omp.h>
#include <sycl/sycl.hpp>

#define N 16384

void myVectorSet(int n, float s, float *x) {
    for (int i = 0; i < n; ++i)
        x[i] = s * (i + 1);
}
```

```cpp
void mySscal(int n, float s, float *x) {
  for (int i = 0; i < n; ++i)
    x[i] = s * x[i];
}

int main() {
  const float scalar = 2.0;
  float *x, *y, *d_x, *d_y;
  int dev;

  omp_interop_t obj{omp_interop_none};
  dev = omp_get_default_device();

  // Snippet begin0
  // Create an interop object with SYCL queue access
#pragma omp interop init(prefer_type(omp_ifr_sycl), targetsync : obj) \
    device(dev)

  if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
    fprintf(stderr, "ERROR: Failed to create interop with SYCL queue access\n");
    exit(1);
  }
  sycl::queue *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));

  // Allocate host data.
  x = new float[N];
  y = new float[N];

  // Allocate device data using SYCL queue.
  d_x = sycl::malloc_device<float>(N * sizeof(float), *q);
  d_y = sycl::malloc_device<float>(N * sizeof(float), *q);
  // Snippet end0

  // Snippet begin1
  // Associate device pointers with host pointers
  omp_target_associate_ptr(&x[0], d_x, N * sizeof(float), 0, dev);
  omp_target_associate_ptr(&y[0], d_y, N * sizeof(float), 0, dev);
  // Snippet end1

  // Snippet begin2
  // Initialize host data.
  myVectorSet(N, 1.0, x);
  myVectorSet(N, -1.0, y);

  // Perform SYCL's memory copy operations from host to device.
  q->memcpy(d_x, x, N * sizeof(float));
  q->memcpy(d_y, y, N * sizeof(float));
  q->wait();

  // Invoke MKL's variant function using the dispatch construct, appending the
  // interop object and replacing the host pointers with device pointers for
  // "x" and "y" as specified in the directives used in MKL.
#pragma omp dispatch interop(obj)
  cblas_saxpy(N, scalar, x, 1, y, 1);

  // Perform SYCL's memory copy operation from device to host.
  q->memcpy(y, d_y, N * sizeof(float));
```

```cpp
q->wait();
// Snippet end2

// Snippet begin3
// Update device data for "x" and bring them back to host.
#pragma omp target map(always, from : x[0 : N])
mySscal(N, scalar, x);

printf("(1:16384) %.3f:%.3f\n", y[0], y[N - 1]);
printf("(2:32768) %.3f:%.3f\n", x[0], x[N - 1]);

// Remove the associated device data for the host pointers.
omp_target_disassociate_ptr(&x[0], dev);
omp_target_disassociate_ptr(&y[0], dev);

delete[] x;
delete[] y;
sycl::free(d_x, *q);
sycl::free(d_y, *q);

#pragma omp interop destroy(obj)
// Snippet end3

return 0;
}
```

## Compilation command:

```batch
icpx -qopenmp -fopenmp-targets=spir64 -fsycl -qmkl omp_interop_sycl_2.cpp
```

## Run command:

```txt
./a.out
```

The next example below consists of Fortran code that invokes a variant function with an interop object and C ++ code that implements the invoked variant function using OpenMP and SYCL.

The first part of the Fortran code defines a module that contains an interface for the base routine foo and a variant routine foo\_gpu. foo declares a replacement routine foo\_gpu when it is called within a dispatch construct by using the declare variant directive with the match clause. The directive also uses the append\_args clause to pass the interop object specified in the dispatch construct to the variant routine foo\_gpu.

```fortran
module subs

  interface

    subroutine foo_gpu(c, v1, n, iop1)  !! variant function
      use iso_c_binding
      integer, intent(in)  :: c
      integer, intent(in)  :: n
      integer, intent(out) :: v1(10)
      type(c_ptr), intent(in):: iop1
    end subroutine foo_gpu

    subroutine foo(c, v1, n)  !! base function
      import foo_gpu          ! Need to add this statement
      integer, intent(in)  :: c
      integer, intent(in)  :: n
      integer, intent(out) :: v1(10)
      !$omp declare variant(foo:foo_gpu) &
```

```fortran
!\$omp& match(construct={dispatch}) append_args(interop(targetsync))
end subroutine foo

end interface

end module subs
```

The main program in the Fortran code initializes data, creates an interop object iop1 with SYCL queue access, and invokes the routine foo using the dispatch directive with iop1 specified in the interop clause. iop1 is passed as an additional argument when the variant routine foo\_gpu is invoked.

```fortran
program p
  use subs
  use omp_lib
  integer c
  integer v1(10)
  integer i, n, d
  integer (kind=omp_interop_kind) :: iop1

  c = 2
  n = 10
  do i = 1, n
    v1(i) = i
  enddo

  d = omp_get_default_device()

  !$omp interop init(prefer_type(omp_ifr_sycl), targetsync:iop1) device(d)

  !$omp dispatch device(d) interop(iop1)
  call foo(c, v1, n)

  !$omp interop destroy(iop1)

  print *, "v1(1) = ", v1(1), " (2), v1(10) = ", v1(10), " (20)"
end program
```

The C++ part of the example implements the functions that may be invoked by the Fortran program. The Fortran program calls the replacement routine foo\_gpu, so the routine foo is defined with a print stating it should not be called. The routine foo\_gpu performs simple vector multiplication using the SYCL queue retrieved from the interop object passed as the last argument to the routine. It accesses the SYCL queue and invokes SYCL code within the OpenMP device data environment as presented in the previous C/C++ examples.

```c
#include <omp.h>
#include <stdio.h>
#include <sycl/sycl.hpp>

#define EXTERN_C extern "C"

EXTERN_C void foo_(int *c, int *v1, int *n) {
    printf("ERROR: Base function foo should not be called\n");
}

EXTERN_C void foo_gpu_(int *c, int *v1, int *n, omp_interop_t obj) {
    int c_val = *c;
    int n_val = *n;

    if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
```

```cpp
printf("Compute on host\n");
    for (int i = 0; i < n_val; i++)
        v1[i] = c_val * v1[i];
    return;
}

auto *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));

printf("Compute on device\n");
#pragma omp target data map(tofrom : v1[0 : n_val]) use_device_ptr(v1)
    q->parallel_for(n_val, [=](auto i) { v1[i] = c_val * v1[i]; });
    q->wait();
}
```

## Compilation command:

```shell
icpx -qopenmp -fopenmp-targets=spir64 -fsycl -c omp_interop_sycl_3b.cpp
ifx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_3a.f90 \
    omp_interop_sycl_3b.o
```

## Run command:

```txt
./a.out
```

The final example invokes OpenMP code and equivalent SYCL code using interop and compares the performance of the two versions. The first part of the code is SAXPY code parallelized with the OpenMP directives. Execution of the directive includes memory allocation on the device and copy operations between host and device as directed by the map clause.

```lisp
// OpenMP saxpy
void saxpy_omp(float a, float *x, float *y, size_t n) {
#pragma omp target teams distribute parallel for map(to : x[0 : n])
    map(tofrom : y[0 : n])
    for (size_t i = 0; i < n; i++)
        y[i] = a * x[i] + y[i];
}
```

The next part of the code is the same SAXPY code parallelized with SYCL, and it contains SYCL memory allocation and copy operations equivalent to the effect of the OpenMP map clause.

```cpp
// SYCL saxpy
void saxpy_sycl(float a, float *x, float *y, size_t n, sycl::queue &q) {
    size_t data_size = n * sizeof(float);
    float *d_x = sycl::malloc_device<float>(data_size, q);
    float *d_y = sycl::malloc_device<float>(data_size, q);
    q.memcpy(d_x, x, data_size);
    q.memcpy(d_y, y, data_size);
    q.wait();
    q.parallel_for(n, [=](auto i) { d_y[i] = a * d_x[i] + d_y[i]; });
    q.wait();
    q.memcpy(y, d_y, data_size);
    q.wait();
    sycl::free(d_x, q);
    sycl::free(d_y, q);
}
```

The main program initializes an interop object obj, invokes the OpenMP version of SAXPY and the SYCL version of SAXPY using the interop object 1000 times. There is also warm-up code to exclude the device initialization part, for example Just-in-Time (JIT) compilation, from the time measurement. Full example code is listed below.

```cpp
#include <cstdio>
#include <cstdlib>
#include <omp.h>
#include <sycl/sycl.hpp>

// Snippet begin0
// OpenMP saxpy
void saxpy_omp(float a, float *x, float *y, size_t n) {
#pragma omp target teams distribute parallel for map(to : x[0 : n])
    map(tofrom : y[0 : n])
    for (size_t i = 0; i < n; i++)
        y[i] = a * x[i] + y[i];
}
// Snippet end0

// Snippet begin1
// SYCL saxpy
void saxpy_sycl(float a, float *x, float *y, size_t n, sycl::queue &q) {
    size_t data_size = n * sizeof(float);
    float *d_x = sycl::malloc_device<float>(data_size, q);
    float *d_y = sycl::malloc_device<float>(data_size, q);
    q.memcpy(d_x, x, data_size);
    q.memcpy(d_y, y, data_size);
    q.wait();
    q.parallel_for(n, [=](auto i) { d_y[i] = a * d_x[i] + d_y[i]; });
    q.wait();
    q.memcpy(y, d_y, data_size);
    q.wait();
    sycl::free(d_x, q);
    sycl::free(d_y, q);
}
// Snippet end1

// Snippet begin2
int main() {
    constexpr size_t num = (64 << 10);
    constexpr size_t repeat = 1000;

    omp_interop_t obj{omp_interop_none};

#pragma omp interop init(prefer_type(omp_ifr_sycl), targetsync : obj)

    if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
        printf("ERROR: Cannot access SYCL queue with OpenMP interop\n");
        return EXIT_FAILURE;
    }

    sycl::queue *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));

    float *x = new float[num];
    float *y = new float[num];

    auto init = [=]() {
```

```c
for (auto i = 0; i < num; i++) {
    x[i] = i + 1;
    y[i] = i;
}
};

saxpy_omp(3, x, y, num); // Warm up
init();
double omp_sec = omp_get_wtime();
for (size_t i = 0; i < repeat; i++)
    saxpy_omp(3, x, y, num);
omp_sec = omp_get_wtime() - omp_sec;
printf("OpenMP y[%d] = %.3e, y[%zu] = %.3e\n", 0, y[0], num - 1, y[num - 1]);

saxpy_sycl(3, x, y, num, *q); // Warm up
init();
double sycl_sec = omp_get_wtime();
for (size_t i = 0; i < repeat; i++)
    saxpy_sycl(3, x, y, num, *q);
sycl_sec = omp_get_wtime() - sycl_sec;
printf(" SYCL y[%d] = %.3e, y[%zu] = %.3e\n", 0, y[0], num - 1, y[num - 1]);

printf("OpenMP took %.3f msec\n", omp_sec * 1e3);
printf(" SYCL took %.3f msec\n", sycl_sec * 1e3);

delete[] x;
delete[] y;

#pragma omp interop destroy(obj)

return EXIT_SUCCESS;
}
// Snippet end2
```

Execution of this code shows that the performance of the two versions written in SYCL and OpenMP are nearly identical, giving you a choice without scarifying performance.

## Compilation command:

```batch
icpx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_4.cpp
```

## Run command:

```txt
./a.out
OpenMP y[0] = 3.000e+03, y[65535] = 1.967e+08
    SYCL y[0] = 3.000e+03, y[65535] = 1.967e+08
OpenMP took 112.489 msec
    SYCL took 111.001 msec
```

## Offloading DO CONCURRENT

The DO CONCURRENT loop was introduced in ISO Fortran 2008 and has been enhanced in more recent ISO standards. This construct tells the compiler that the loop iterations are independent. Independent iterations can be executed sequentially, in parallel, and/or offloaded to accelerators.

## Offloading DO CONCURRENT Loops Using Compiler Flags

The ifx compiler provides two flags for respectively controlling offloading DO CONCURRENT loops and data transfer schemes:

1. -fopenmp-target-do-concurrent: Tells the compiler to offload DO CONCURRENT to the device. In the absence of this flag, the execution takes place on the host.

2. -fopenmp-do-concurrent-maptype-modifier=none|present|always: This is an optional flag that helps control the host-device data transfers. In the absence of this flag, the behavior is equivalent to the behavior of the none modifier explained below. Use one of the following modifiers with this flag:

• present: Tells the compiler that data has already been moved to the device, and no further movement is required. If the data is not present on the device, using this flag will result in a runtime error.

• always: Tells the compiler that data must be moved to the device at the beginning of each region and back to the host at the end of each region.

• none: Behaves like the “present” flag if the data is on the device, otherwise it moves the data to the device at the beginning of the target region and back to the host at the end of the region.

## Example

The following do\_concurrent.f90 example shows the difference in performance using different offloading options.

```fortran
program do_concurrent
    use omp_lib
    implicit none

    integer :: i, outer
    integer, dimension(10000) :: x, y, z
    double precision      :: t0, t1, time
    x = 1
    y = 0
    z = 0
! Dummy offload to warm up the device
!$omp target
!$omp end target

    t0 = omp_get_wtime()
    do outer = 1, 24000
        !call do_work_on_host Parenting_x(x,...)
        do concurrent (i = 1:10000)
            y(i) = x(i) + 1
        enddo

        do concurrent (i = 1:10000)
            z(i) = y(i) + 1
        enddo
!call do_work_on_host using_z(z,...)
enddo
t1 = omp_get_wtime()
time = t1-t0
print *, time
end program do_concurrent
```

The basic flow of the example is as follows:

```txt
Initialize_arrays x,y,z
Dummy target region
Start_time = get_wtime()
Outer do loop
    Call do_work_on_host_updating_x
    First inner DO CONCURRENT loop (computes y based on x)
    Second inner DO CONCURRENT loop (computes z based on y)
```

```txt
Call do_work_on_host_using_z
End_time = get_wtime()
Time = End_time - Start_time
Print Time
```

A dummy target region is used before the timed region to exclude the time overhead of compiling and loading the image from the measurements.

## Compilation command:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=none do_concurrent.f90 -o none.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=present do_concurrent.f90 -o present.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=always do_concurrent.f90 -o always.out
```

## Example run command:

```ignorefile
./none.out
./present.out
./always.out
```

The following table shows the performance results as well as the number of data transfers from the host to the device and from the device to the host.

<table><tr><td>-fopenmp-do-concurrent-maptype-modifier</td><td>Time(ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>none</td><td>11.09</td><td>96k</td><td>96k</td></tr><tr><td>present</td><td>Failed</td><td>n/a</td><td>n/a</td></tr><tr><td>always</td><td>11.37</td><td>96k</td><td>96k</td></tr></table>

The use of the present modifier results in an expected runtime failure, because the data was never copied to the device before the offloaded DO CONCURRENT regions.

The performance using the none modifier is on par with the always modifier. The number of data transfers from the host to the device and from the device to the host is the same. There are 96k transfers each way. These 96k transfers correspond to: 4 copies per outer loop iteration \* 24k iterations

The following table shows all the data transfers per 1 outer loop iteration:

<table><tr><td>Host to Device</td><td>Device to Host</td></tr><tr><td>copy x (line 18)</td><td>copy x (line 20)</td></tr><tr><td>copy y (line 18)</td><td>copy y (line 20)</td></tr><tr><td>copy y (line 22)</td><td>copy y (line 24)</td></tr><tr><td>copy z (line 22)</td><td>copy z (line 24)</td></tr></table>

You don’t need all these transfers for the correct execution of the code. You only need to copy x to the device at the beginning of the first DO CONCURRENT region, and read z back from the device at the end of the second DO CONCURRENT region. This means you need 1 copy per iteration each way, totaling 24k D2M and 24k M2D transfers.

## Hybrid Technique of Offloading DO CONCURRENT Loops

The hybrid technique uses OpenMP target data regions around DO CONCURRENT region(s), and the compiler flags described in the previous section. By using the target data regions, you can control data movement and improve performance. Applying this technique to the code in the previous section will result in the following outer loop region:

```txt
do outer = 1, 24000
    !call do_work_on_host_updating_x(x,...)
    !$omp target data map(to: x) map(alloc: y) map(from: z)
    do concurrent (i = 1:10000)
        y(i) = x(i) + 1
    enddo

    do concurrent (i = 1:10000)
        z(i) = y(i) + 1
    enddo
    !$omp end target data
    !call do_work_on_host_using_z(z,...)
enddo
```

Comparing with the previous example, the new code adds

• !\$omp target data map(to:x) map(alloc: y) map(from:z) before the first DO CONCURRENT region.

• !\$omp end target data after the second DO CONCURRENT region.

## Compilation command:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=none hybrid_do_concurrent.f90 -o none.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=present hybrid_do_concurrent.f90 -o present.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=always hybrid_do_concurrent.f90 -o always.out
```

## Example run command:

```ignorefile
./none.out
./present.out
./always.out
```

The following table shows the performance results as well as the number of data transfers from the host to the device and from the device to the host:

<table><tr><td>-fopenmp-do-concurrent-maptype-modifier</td><td>Time(ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>none</td><td>4.28</td><td>24k</td><td>24k</td></tr><tr><td>present</td><td>4.31</td><td>24k</td><td>24k</td></tr><tr><td>always</td><td>13.80</td><td>120k</td><td>120k</td></tr></table>

For both the none modifier and the present modifier, the optimal number of data transfers is achieved, 24k each way.

In terms of timing, compiling hybrid\_do\_concurrent.f90 with the none modifier achieves a speedup of 2.6x compared to the initial version of the code using the same modifier.

Using the always modifier results in a 15% slowdown compared to the initial version of the code using the same modifier. This slowdown is due to the extra data transfers introduced by the added target data region. In this case, the added target data region is adding a copy of x from the host to the device in each outer loop iteration as well as a copy of z from the device to the host at the end of the target data region. This brings the total number of data transfers per outer-loop iteration to 5 transfers, resulting in 120k transfers each way.

Performance comparison for the 2 versions using the present modifier is not possible, since the flag-only version is incorrect in this case as explained above.

## OpenMP 6.0’s “loop” Directive on DO CONCURRENT Loops

OpenMP 6.0 specifications added support for specifying “loop” constructs on DO CONCURRENT. This enables you to offload DO CONCURRENT loops using OpenMP target construct on DO CONCURRENT loops. It also enables you to control the data transfers using OpenMP mapping clauses.

Applying this technique to the initial version of the code will result in the following outer loop region:

```matlab
do outer = 1, 2400
    !call do_work_on_host Parenting_x(x,...)
    !$omp target data map(to: x) map(alloc: y) map(from: z)
    !$omp target teams loop
    do concurrent (i = 1:10000)
        y(i) = x(i) + 1
    enddo
    !$omp target teams loop
    do concurrent (i = 1:10000)
        z(i) = y(i) + 1
    enddo
    !$omp end target data
    !call do_work_on_host using_z(z,...)
enddo
```

As shown above, this new example adds

• !\$omp target data map(to:x) map(alloc: y) map(from:z) at the beginning of the outer loop iteration.

• !\$omp target teams loop before each DO CONCURRENT Loop.

• !\$omp end target data at the end of the outer loop iteration.

## Compilation command:

```batch
ifx -fiopenmp -fopenmp-targets=spir64 omp6_do_concurrent.f90
```

## Example run command:

```txt
./a.out
```

The following table shows the performance results:

<table><tr><td>Flag</td><td>Time (ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>n/a</td><td>4.11</td><td>24,000</td><td>24,000</td></tr></table>

The performance is on par with the best performing version of the hybrid technique and the number of data transfers is 24k each way which is the optimal number of transfers for this code, as explained previously.

## Findings and Recommendations

1. While the first approach can be considered to be the simplest, as it does not require any code modification, it is clear that it is the worst in term of performance and can lead to runtime failure if present is used and the data is not actually on the device.

2. While the hybrid approach using the none or the present maptype modifier was on par with the new openmp 6.0 standard approach of offloading DO CONCURRENT loops, we recommend the latter for the following reasons:

• When using the OpenMP 6.0 new standard you do not have to rely on command-line flags. This provides portability as code written in this way will work with all compilers that support OpenMP standard.

• In the case of multiple DO CONCURRENT regions and more complicated scenarios, you can control which region(s) to offload to. This control is not possible when using compiler flags.
