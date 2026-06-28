## OpenMP Interop with SYCL

OpenMP interop construct and the related user API functions allow foreign runtime such as SYCL to operate with the properties or resources exposed by the interop object.

The first example below shows how to create an OpenMP interop for interoperability with SYCL, how to use the API functions to retrieve interop properties, and how to expose the OpenMP device data environment to SYCL.

The example initializes an OpenMP interop object obj with the targetsync type, requesting the SYCL foreign runtime with the prefer\_type(omp\_ifr\_sycl) modifier. Specifying the targetsync type makes the interop object include a synchronization object in the foreign runtime such as SYCL queue. Then, it ensures a valid SYCL interop has been created by checking the interop property value for the omp\_ipr\_fr\_id property and retrieves a handle to the SYCL queue using the targetsync property.

```cpp
// Create an interop object with SYCL queue access.
#pragma omp interp init(prefer_type(omp_ifr_sycl), targetsync : obj)
  if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
    fprintf(stderr, "ERROR: Failed to create interp with SYCL queue access\n");
    exit(1);
  }

  // Access SYCL queue returned by OpenMP interp.
  auto *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));
```

The remaining part of the example invokes simple SYCL kernel which performs vector addition for the given data, and it uses the OpenMP device data environment to simplify the required SYCL operation for allocating device memory and moving data to and from the device memory. This is possible by using the target data construct with the desired mapping and with the use\_device\_ptr clause. The use\_device\_ptr clause converts the reference to the host data to the corresponding device data created by the map clause in the target data construct. Then, the example destroys the interop object with the interop construct and destroy clause. It is highly recommended to destroy an initialized interop to release the resources created by the initialization properly.

```txt
// Use OpenMP target data environment while allowing SYCL code to access the
// device data with "use_device_ptr" clause.
#pragma omp target data map(to : a[0 : num], b[0 : num])
    \ 
    map(from : c[0 : num]) use_device_ptr(a, b, c)
    {
        auto event = q->parallel_for(num, [=](auto i) { c[i] = a[i] + b[i]; });
        event.wait();
    }

    // Release resources associated with "obj".
#pragma omp interop destroy(obj)
```

The full example code is listed below.

```cpp
//
// Code example that uses OpenMP interop and SYCL kernel.
//
// The example shows
// 1) How to create an interop object to access the cooperating SYCL queue
// 2) How to check if the interop object is for SYCL foreign runtime
// 3) How to set up device accessible memory to be used in SYCL code
//
// Compilation command:
// icpx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_1.cpp
//
#include <cstdio>
#include <omp.h>
#include <sycl/sycl.hpp>

int main() {
    constexpr int num = 16384;
```

```c
float *a = new float[num];
float *b = new float[num];
float *c = new float[num];

// Initialize host data.
for (int i = 0; i < num; i++) {
    a[i] = i + 1;
    b[i] = 2 * i;
    c[i] = 0;
}

omp_interop_t obj{omp_interop_none};

// Snippet begin0
// Create an interop object with SYCL queue access.
#pragma omp interp init(prefer_type(omp_ifr_sycl), targetsync : obj)
    if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
        fprintf(stderr, "ERROR: Failed to create interp with SYCL queue access\n");
        exit(1);
    }

    // Access SYCL queue returned by OpenMP interp.
    auto *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));
    // Snippet end0

    // Snippet begin1
    // Use OpenMP target data environment while allowing SYCL code to access the
    // device data with "use_device_ptr" clause.
#pragma omp target data map(to : a[0 : num], b[0 : num]) \
        map(from : c[0 : num]) use_device_ptr(a, b, c)
        {
            auto event = q->parallel_for(num, [=](auto i) { c[i] = a[i] + b[i]; });
            event.wait();
        }

    // Release resources associated with "obj".
#pragma omp interp destroy(obj)
    // Snippet end1

    printf("c[0] = %.3f (%.3f), c[%d] = %.3f (%.3f)\n", c[0], 1.0, num - 1,
                    c[num - 1], 3.0 * (num - 1) + 1);
    delete[] a;
    delete[] b;
    delete[] c;

    return 0;
}
```

## Compilation command:

```batch
icpx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_1.cpp
```

## Run command:

./a.out

The following example is semantically equivalent to this OpenMP example, but it uses SYCL foreign runtime and Intel<sup>®</sup> Math Kernel Library (Intel<sup>®</sup> MKL). Note that the example was simplified to make the program perform with clear expected behavior. The example shows how to allocate/use SYCL memory objects valid between OpenMP and SYCL, and how to use the interop object with the dispatch construct, in addition to the operations presented in the previous example.

The first part of the example obtains the SYCL queue handle by initializing an interop with the interop construct on the interop object obj as is done in the previous example. Then, it allocates the host data (x and y) and the device data (d\_x and d\_y) using the SYCL’s memory allocation API function sycl::malloc\_device.

```c
// Create an interop object with SYCL queue access
#pragma omp interop init(prefer_type(omp_ifr_sycl), targetsync : obj)
    \ device(dev)

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
```

The next part of the code invokes OpenMP API functions omp\_target\_associate\_ptr to associate the host data to the desired device data, enabling use of the host pointers in OpenMP regions where the corresponding device pointers are used instead if applicable. This is similar to the effect of the map clause, but data movement should be done explicitly.

```c
// Associate device pointers with host pointers
omp_target_associate_ptr(&x[0], d_x, N * sizeof(float), 0, dev);
omp_target_associate_ptr(&y[0], d_y, N * sizeof(float), 0, dev);
```

The next part of the example invokes a SYCL kernel to perform SAXPY operation on the data x and y. First, it initializes the host data and copies it to the device using the SYCL’s memory copy API memcpy. Then, it invokes an Intel MKL kernel cblas\_saxpy using the dispatch construct with the interop object obj specified in the interop clause. The host pointers x and y can be used directly in the dispatch construct since the Intel MKL code ensures that the associated device pointers d\_x and d\_y are used instead, as specified by the declare variant directive with the adjust\_args clause. The interop object obj is also passed as an additional argument when the variant function is invoked in Intel MKL. The effect of the call cblas\_saxpy is the modification of the device data d\_y, so the example copies the data back to the host data y.

```c
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
```

```c
#pragma omp dispatch interop(obj)
  cblas_saxpy(N, scalar, x, 1, y, 1);

  // Perform SYCL's memory copy operation from device to host.
  q->memcpy(y, d_y, N * sizeof(float));
  q->wait();
```

The example also updates the device data d\_x and copies it back to the host using the target construct with the map clause. Note that the always modifier is specified to force data movement since user-created mapping with omp\_target\_associate\_ptr does not incur any data movement. Finally, the code removes the data association for x and y, releases the host and the device data, and destroys the interop object obj.

```cpp
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
```

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
