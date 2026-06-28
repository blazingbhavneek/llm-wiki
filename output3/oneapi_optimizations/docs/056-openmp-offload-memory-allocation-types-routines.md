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

The map clauses on the target construct inside the iterations loop cause data (values of A, B, C) to be transferred from the host to the device at the beginning of each target region, and cause data (values of C) to be transferred from the device to the host at the end of each target region. These data transfers incur a significant performance overhead. A better approach using map clauses would be to put the whole iterations loop inside a target data construct with the map clauses. This causes the transfers to occur once at the beginning of the iterations loop, and another time at the end of the iterations loop. The modified example using target data and map clauses is shown below.

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
    }

    // Initialize the arrays
```

```txt
#pragma omp parallel for
for (size_t i=0; i<length; i++) {
    A[i] = 2.0;
    B[i] = 2.0;
    C[i] = 0.0;
}

// Perform the computation

nstream_time = omp_get_wtime();
#pragma omp target data map(to: A[0:length], B[0:length]) \
    map(tofrom: C[0:length])
{
    for (int iter = 0; iter<iterations; iter++) {
        #pragma omp target teams distribute parallel for
        for (size_t i=0; i<length; i++) {
            C[i] += A[i] + scalar * B[i];
        }
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
        "       Expected checksum: %lf\n"
        "       Observed checksum: %lf\n"
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

```txt
omp_target_alloc
```

Next, the example above is modified to use device allocations instead of map clauses. Storage for arrays A, B, and C is directly allocated on the device by calling the OpenMP runtime routine omp\_target\_alloc. The routine takes two arguments: the number of bytes to allocate on the device, and the number of the device on which to allocate the storage. The routine returns a device pointer that references the device address of the storage allocated on the device. If the call to omp\_target\_alloc returns NULL, then this indicates that the allocation was not successful.

To access the allocated memory in a target construct, the device pointer returned by a call to

omp\_target\_alloc is listed in an is\_device\_ptr clause on the target construct. This ensures that there is no data transfer before and after kernel execution since the kernel operates on data that is already on the device.

At the end of the program, the runtime routine omp\_target\_free is used to deallocate the storage for A, B, and C on the device.

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
    size_t bytes = length*sizeof(double);
    double * __restrict A;
    double * __restrict B;
    double * __restrict C;
    double scalar = 3.0;
    double nstream_time = 0.0;

    // Allocate arrays in device memory

    A = (double *) omp_target_alloc(bytes, device_id);
    if (A == NULL) {
        printf(" ERROR: Cannot allocate space for A using omp_target_alloc().\n");
        exit(1);
    }

    B = (double *) omp_target_alloc(bytes, device_id);
    if (B == NULL) {
        printf(" ERROR: Cannot allocate space for B using omp_target_alloc().\n");
        exit(1);
    }

    C = (double *) omp_target_alloc(bytes, device_id);
    if (C == NULL) {
        printf(" ERROR: Cannot allocate space for C using omp_target_alloc().\n");
        exit(1);
```

```txt
}

// Initialize the arrays

#pragma omp target teams distribute parallel for \
    is_device_ptr(A,B,C)
for (size_t i=0; i<length; i++) {
    A[i] = 2.0;
    B[i] = 2.0;
    C[i] = 0.0;
}

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
#pragma omp target teams distribute parallel for reduction(+:asum) \
    map(tofrom: asum) is_device_ptr(C)
for (size_t i=0; i<length; i++) {
    asum += fabs(C[i]);
}

omp_target_free(A, device_id);
omp_target_free(B, device_id);
omp_target_free(C, device_id);

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
```

```scss
return 0;
}
```

## Notes:

• When calling omp\_target\_alloc, the device number specified must be one of the supported devices, other than the host device. This will be the device on which storage will be allocated.

• Since the arrays A, B, and C are not accessible from the host, the initialization of the arrays, kernel execution, and summation of elements of C all need to be done inside OpenMP target regions.

• A device allocation can only be accessed by the device specified in the omp\_target\_alloc call, but may be copied to memory allocated on the host or other devices by calling omp\_target\_memcpy.

```txt
omp_target_alloc_device
```

The Intel extension omp\_target\_alloc\_device is similar to omp\_target\_alloc. It is also called with two arguments: the number of bytes to allocate on the device, and the number of the device on which to allocate the storage. The routine returns a device pointer that references the device address of the storage allocated on the device. If the call to omp\_target\_alloc\_device returns NULL, then this indicates that the allocation was not successful.

The above omp\_target\_alloc example can be rewritten using omp\_target\_alloc\_device by simply replacing the call to omp\_target\_alloc with a call to omp\_targer\_alloc\_device as shown below.

At the end of the program, the runtime routine omp\_target\_free is used to deallocate the storage for A, B, and C on the device.

```c
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
```

## Note:

• All of the above Notes that apply to omp\_target\_alloc also apply to omp\_target\_alloc\_device.

```txt
omp_target_alloc_host
```

The above example can also be rewritten by doing a host allocation for A, B, and C. This allows the memory to be accessible to the host and all supported devices.

In the following modified example, the omp\_target\_alloc\_host runtime routine (an Intel extension) is called to allocate storage for each of the arrays A, B, and C. The routine takes two arguments: the number of bytes to allocate, and a device number. The device number must be one of the supported devices, other than the host device. The routine returns a pointer to a storage location in host memory. If the call to omp\_target\_alloc\_host returns NULL, this indicates that the allocation was not successful.

Note the directive requires unified\_address is specified at the top of the program. This requires that the implementation guarantee that all devices accessible through OpenMP API routines and directives use a unified address space. In this address space, a pointer will always refer to the same location in memory from all devices, and the is\_device\_ptr clause is not necessary to obtain device addresses from device pointers for use inside target regions. When using Intel compilers, the requires unified\_address directive is actually not needed, since unified address space is guaranteed by default. However, for portability the code includes the directive.

The pointer returned by a call to omp\_target\_alloc\_host can be used to access the storage from the host and all supported devices. No map clauses and no is\_device\_ptr clauses are needed on a target construct to access the memory from a device since a unified address space is used.

At the end of the program, the runtime routine omp\_target\_free is used to deallocate the storage for A, B, and C.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <omp.h>

#pragma omp requires unified_address

#define iterations 100
#define length      64*1024*1024

int main(void)
{
    int device_id = omp_get_default_device();
    size_t bytes = length*sizeof(double);
    double * __restrict A;
    double * __restrict B;
    double * __restrict C;
    double scalar = 3.0;
    double nstream_time = 0.0;

    // Allocate arrays in host memory

    A = (double *) omp_target_alloc_host(bytes, device_id);
    if (A == NULL) {
        printf(" ERROR: Cannot allocate space for A using omp_target_alloc_host().\n");
        exit(1);
    }

    B = (double *) omp_target_alloc_host(bytes, device_id);
    if (B == NULL) {
        printf(" ERROR: Cannot allocate space for B using omp_target_alloc_host().\n");
        exit(1);
    }

    C = (double *) omp_target_alloc_host(bytes, device_id);
    if (C == NULL) {
```

```txt
printf(" ERROR: Cannot allocate space for C using omp_target_alloc_host().\n");
    exit(1);
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
    #pragma omp target teams distribute parallel for
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
    printf("Solution validates\n");
    double avgtime = nstream_time/iterations;
    printf("Checksum = %lf; Avg time (s): %lf\n", asum, avgtime);
}
```

```scss
return 0;
}
```

## Notes:

• When calling omp\_target\_alloc\_host, the device number specified must be one of the supported devices, other than the host device.

• Since the arrays A, B, and C are accessible from the host and device, the initialization of the arrays and summation of elements of C may be done either on the host (outside of a target construct) or on the device (inside a target construct).

• Intel<sup>®</sup> Data Center GPU Max Series does not support atomic operations (or algorithms that use atomic operations, such as some reductions) on host allocations (i.e., memory allocated via omp\_target\_alloc\_host). Use atomic operations on memory allocated via omp\_target\_alloc\_device, instead.

## omp\_target\_alloc\_shared

The above example is modified so that shared allocations are used instead of host allocations. The omp\_target\_alloc\_shared runtime routine is called to allocate storage for each of arrays A, B, and C. The routine takes two arguments: the number of bytes to allocate on the device, and a device number. The device number must be one of the supported devices, other than the host device. The routine returns a pointer to a storage location in shared memory. If the call to omp\_target\_alloc\_shared returns NULL, then this indicates that the allocation was not successful.

Note the requires unified\_address directive is specified at the top of the program, for portability.

The pointer returned by a call to omp\_target\_alloc\_shared can be used to access the storage from the host and all supported devices. No map clauses and no is\_device\_ptr clauses are needed on a target construct to access the memory from a device since a unified address space is used.

At the end of the program, the runtime routine omp\_target\_free is used to deallocate the storage for A, B, and C.

```c
// Allocate arrays in shared memory

A = (double *) omp_target_alloc_shared(bytes, device_id);
if (A == NULL) {
    printf(" ERROR: Cannot allocate space for A using omp_target_alloc_shared().\n");
    exit(1);
}

B = (double *) omp_target_alloc_shared(bytes, device_id);
if (B == NULL) {
    printf(" ERROR: Cannot allocate space for B using omp_target_alloc_shared().\n");
    exit(1);
}

C = (double *) omp_target_alloc_shared(bytes, device_id);
if (C == NULL) {
    printf(" ERROR: Cannot allocate space for C using omp_target_alloc_shared().\n");
    exit(1);
}
```

## Notes:

• When calling omp\_target\_alloc\_shared, the device number specified must be one of the supported devices, other than the host device.

• Since the arrays are accessible from the host and device, the initialization and verification may be done either on the host or on the device (inside a target construct).

• Concurrent access from host and device to memory allocated via omp\_target\_alloc\_shared is not supported.

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
