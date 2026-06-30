# oneapi_optimizations Source Lines 12184-12619

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L12184-L12619

Citation: [oneapi_optimizations:L12184-L12619]

````text
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
````
