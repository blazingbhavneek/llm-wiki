## Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_map_tofrom.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

For better performance, the map-type for u and dx should be to, and the map-type for w should be from, as shown in the following modified example.

```txt
#pragma omp target teams distribute parallel for \
    private(b, i, j, k, l) \
    map(to: u[0:SIZE], dx[0:P * P]) \
    map(from: w [0:SIZE])
for (int n = 0; n < SIZE; n++) {
    k = n - (n / P) * P;
    j = (n - k) / P;
    i = (n - (j * P + k)) / (P * P);
    b = n / (P * P * P);

    double ur = 0.;
    double us = 0.;
    double ut = 0.;

    for (l = 0; l < P; l++) {
        ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
        us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
        ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
    }

    w[IDX4(b, i, j, k)] = ur * us * ut;
}
```

Using more specific map-types (to or from, instead of tofrom), reduced the runtime on the particular GPU used (1-stack only):

```txt
tofrom map-types version      : 0.001141 seconds
to or from map-types version : 0.000908 seconds
```

LIBOMPTARGET\_DEBUG=1 output shows that there are unnecessary data transfers between the host and the device when the tofrom map-type is used for u, dx, and w. With tofrom, there are six transfers to copy the values of u, dx, and w from the host to the device and vice-versa:

```txt
$ grep "Libomptarget --> Moving" test_map_tofrom.debug
Libomptarget --> Moving 2048 bytes (hst:0x00007fff1f6ad540) -> (tgt:0xff00fffffffe0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007fff1f66d540) -> (tgt:0xff00fffffffee0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007fff1f62d540) -> (tgt:0xff00ffffff20000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffff20000) -> (hst:0x00007fff1f62d540)
Libomptarget --> Moving 262144 bytes (tgt:0xff00fffffffee0000) -> (hst:0x00007fff1f66d540)
Libomptarget --> Moving 2048 bytes (tgt:0xff00fffffffe0000) -> (hst:0x00007fff1f6ad540)
```

With the more specific map-types (to or from), we see only three data transfers: two transfers to copy the values of u and dx from host to device, and one transfer to copy the values of w from device to host:

```txt
$ grep "Libomptarget --> Moving" test_map_to_or_from.debug
Libomptarget --> Moving 2048 bytes (hst:0x00007ffffc2258fd0) -> (tgt:0xff00fffffffe0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007ffffc2218fd0) -> (tgt:0xff00fffffffee0000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffffff20000) -> (hst:0x00007ffffc21d8fd0)
```

## Do Not Map Read-Only Scalar Variables

The compiler will produce more efficient code if read-only scalar variables in a target construct are not mapped, but are listed in a firstprivate clause on the target construct or not listed in any clause at all. (Note that when a scalar variable is not listed in any clause on the target construct, it will be firstprivate by default.)

Listing a read-only scalar variable on a map(to: ) clause causes unnecessary memory allocation on the device and copying of data from the host to the device. On the other hand, when a read-only scalar is specified to be firstprivate on the target construct, the variable is passed as argument when launching the kernel, and no memory allocation or copying for the variable is required.

In the following example, a loop nest is offloaded onto the GPU. In the target construct, the three scalar variables, s1, s2, and s3, are read-only and are listed in a map(to: ) clause.

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
    double w[SIZE];          /* output */
    double u[SIZE], dx[P * P]; /* input */
    double s1, s2, s3;         /* scalars */
    int b, i, j, k, l;        /* loop counters */
    double start, end;         /* timers */

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

    /* initialize scalars */
    s1 = u[SIZE / 2];
    s2 = scaled_rand();
    s3 = 0.145;

    /* map data to device */
```

```c
#pragma omp target enter data map(to: u[0:SIZE], dx[0:P * P])

start = omp_get_wtime();

/* offload the kernel with collapse clause */
#pragma omp target teams distribute parallel for collapse(4) \
  map(to: s1, s2, s3) private(b, i, j, k, l)
for (b = 0; b < BLOCKS; b++) {
  for (i = 0; i < P; i++) {
    for (j = 0; j < P; j++) {
      for (k = 0; k < P; k++) {
        double ur = 0.;
        double us = 0.;
        double ut = 0.;

        for (l = 0; l < P; l++) {
          ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)] + s1;
          us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)] - s2;
          ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)] * s3;
        }

        w[IDX4(b, i, j, k)] = ur * us * ut;
      }
    }
  }
}

end = omp_get_wtime();

#pragma omp target exit data map(from: w[0:SIZE])

/* print result */
printf("collapse-clause: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
```

## Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_scalars_map.cpp
```

## Run command:

OMP\_TARGET\_OFFLOAD=MANDATORY ZE\_AFFINITY\_MASK=0 LIBOMPTARGET\_DEBUG=1 ./a.out

It is more efficient to list s1, s2, and s3 in a firstprivate clause on the target construct, as shown in the modified example below, or not list them in any clause at all.

```c
/* offload the kernel with collapse clause */
#pragma omp target teams distribute parallel for collapse(4) \
    firstprivate(s1, s2, s3) private(b, i, j, k, l)
for (b = 0; b < BLOCKS; b++) {
    for (i = 0; i < P; i++) {
        for (j = 0; j < P; j++) {
            for (k = 0; k < P; k++) {
                double ur = 0.;
                double us = 0.;
                double ut = 0.;

                for (l = 0; l < P; l++) {
```

```javascript
ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)] + s1;
        us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)] - s2;
        ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)] * s3;
    }

    w[IDX4(b, i, j, k)] = ur * us * ut;
}
}
}
}
```

Using firstprivate(s1, s2, s3), instead of map(to:s1, s2, s3), reduced the runtime on the particular GPU used (1-stack only):

```python
map(to:s1,s2,s3) version      : 0.001324 seconds
firstprivate(s1,s2,s3) version : 0.000730 seconds
```

LIBOMPTARGET\_DEBUG=1 output shows that data partitioning is the same in both examples with map(to:s1, s2, s3) and with firstprivate(to:s1, s2, s3).

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_9b49d7d8__Z4main_151 with pointer 0x0000000002b295d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x0000000002b295d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_9b49d7dd__Z4main_151 with pointer 0x0000000001f475d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x0000000001f475d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

However, more device memory allocations and host-to-device data transfers occur when the map(to:s1, s2, s3) clause is used.

LIBOMPTARGET\_DEBUG=1 output shows the following data about memory allocations on the device when map(to:s1, s2, s3) clause is used.

```txt
Target LEVEL0 RTL --> Memory usage for device memory, device 0x000000000278e470
Target LEVEL0 RTL --> -- Allocator:      Native,          Pool
Target LEVEL0 RTL --> -- Requested:    1179648,       526360
Target LEVEL0 RTL --> -- Allocated:    1179648,       526528
Target LEVEL0 RTL --> -- Freed     :    1179648,       262336
Target LEVEL0 RTL --> -- InUse    :        0,         264192
Target LEVEL0 RTL --> -- PeakUse   :    1179648,       526528
Target LEVEL0 RTL --> -- NumAllocs:      3,           6
```

Note that the memory allocated is 1,179,648 bytes, and the number of allocations (from the pool) is 6 – for the three arrays (dx, u, and w) and the three scalars (s1, s2, and s3).

In contrast, LIBOMPTARGET\_DEBUG=1 output shows fewer memory allocations on the device when the firstprivate(s1, s2, s3) clause is used. The memory allocated is reduced from 1,179,648 to 1,114,112 bytes (a reduction of 64 kilobytes), and the number of allocations (from the pool) is reduced from 6 to 3, as shown below.

```txt
Target LEVEL0 RTL --> Memory usage for device memory, device 0x0000000001bab440
Target LEVEL0 RTL --> -- Allocator:      Native,          Pool
Target LEVEL0 RTL --> -- Requested:    1114112,       526336
Target LEVEL0 RTL --> -- Allocated:    1114112,       526336
Target LEVEL0 RTL --> -- Freed   :     1114112,       262144
Target LEVEL0 RTL --> -- InUse   :         0,        264192
Target LEVEL0 RTL --> -- PeakUse  :    1114112,       526336
Target LEVEL0 RTL --> -- NumAllocs:      2,          3
```

In addition to more memory allocations, using the map(to: ) clause results in are more data transfers from host to device. This can be seen by grepping for "Libomptarget --> Moving" in the LIBOMPTARGET\_DEBUG=1 output:

```txt
$ grep "Libomptarget --> Moving" test_scalars_map.debug
Libomptarget --> Moving 262144 bytes (hst:0x00007ffdf5526760) -> (tgt:0xff00fffffffef0000)
Libomptarget --> Moving 2048 bytes (hst:0x00007ffdf5566760) -> (tgt:0xff00fffffee0000)
Libomptarget --> Moving 8 bytes (hst:0x00007ffdf55670a0) -> (tgt:0xff00fffffffed0000)
Libomptarget --> Moving 8 bytes (hst:0x00007ffdf55670a8) -> (tgt:0xff00fffffffed0040)
Libomptarget --> Moving 8 bytes (hst:0x00007ffdf55670b0) -> (tgt:0xff00fffffffed0080)
Libomptarget --> Moving 262144 bytes (hst:0x00007ffdf54e6760) -> (tgt:0xff00ffffff30000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffff30000) -> (hst:0x00007ffdf54e6760)
```

In contrast, when the firstprivate(to:s1, s2, s3) clause is used, LIBOMPTARGET\_DEBUG=1 output shows:

```txt
$ grep "Libomptarget --> Moving" test_scalars_fp.debug
Libomptarget --> Moving 262144 bytes (hst:0x00007ffda809c4a0) -> (tgt:0xff00fffffffef0000)
Libomptarget --> Moving 2048 bytes (hst:0x00007ffda80dc4a0) -> (tgt:0xff00fffffee0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007ffda805c4a0) -> (tgt:0xff00ffffff30000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffff30000) -> (hst:0x00007ffda805c4a0)
```

Note that in the example with map(to:s1, s2, s3) we have three additional data transfers, each moving 8 bytes. These transfers are for copying the values of s1, s2, and s3 from host to device.

## Do Not Map Loop Bounds to Get Better ND-Range Partitioning

As mentioned earlier, the compiler will produce more efficient code if read-only scalar variables in a target construct are not mapped, but are listed in a firstprivate clause on the target construct or not listed in any clause at all.

This is especially true when the scalars in question are parallel loop bounds in the target construct. If any of the loop bounds (lower bound, upper bound, or step) are mapped, then this will result in unnecessary memory allocation on the device and copying of data from host to device. Loop partitioning will also be affected, and may result in non-optimal ND-range partitioning that negatively impacts performance.

Consider the following example, where a parallel for loop is offloaded onto the GPU. The upper bound of the for loop is the scalar variable upper, which is mapped by the target construct (on line 53).

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <math.h>
#include <omp.h>
```

```lisp
#define P 16
#define BLOCKS 8
#define SIZE (BLOCKS * P * P * P)

#define MAX 100
#define scaled_rand() ((rand() % MAX) / (1.0 * MAX))

#define IDX2(i, j) (i * P + j)
#define IDX4(b, i, j, k) ((b * P * P * P + i * P * P + j * P + k) % SIZE)

int main(void) {
    double w[SIZE];          /* output */
    double u[SIZE], dx[P * P]; /* input */
    int b, i, j, k, l;         /* loop counters */
    int upper;
    double start, end;          /* timers */

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

    upper = (int)dx[0] + SIZE;

    /* map data to device */
    #pragma omp target enter data map(to: u[0:SIZE], dx[0:P * P])

    start = omp_get_wtime();

    /* offload kernel */
    #pragma omp target teams distribute parallel for private(b, i, j, k, l) \
        map(to: upper)
    for (int n = 0; n < upper; n++) {
        double ur = 0.;
        double us = 0.;
        double ut = 0.;

        k = n - (n / P) * P;
        j = (n - k) / P;
        i = (n - (j * P + k)) / (P * P);
        b = n / (P * P * P);

        for (l = 0; l < P; l++) {
            ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
            us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
            ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
        }

        w[IDX4(b, i, j, k)] = ur * us * ut;
```

```c
}

end = omp_get_wtime();

/* map data from device */
#pragma omp target exit data map(from: w[0:SIZE])

printf("offload: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
}
```

## Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_loop_bounds_map.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

Since upper is mapped, the value of the variable upper on the host may be different from the value on the device. Because of this, when the target region is offloaded at runtime, the number of loop iterations in the offloaded loop is not known on the host. In this case, the runtime (libomptarget.so) will use device and kernel properties to choose ND-range partitioning that fills the whole GPU.

The compiler-generated code for the offloaded loop includes an additional innermost loop (per work-item) inside the offloaded loop. If the global size selected happens to be smaller than the actual number of loop iterations, each work-item will process multiple iterations of the original loop. If the global size selected is larger than the actual number of loop iterations, some of the work-items will not do any work. An if-condition inside the loop generated by the compiler will check this and skip the rest of the loop body.

For the above example (where upper is mapped), LIBOMPTARGET\_DEBUG=1 shows the following ND-range partitioning.

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_1ff4bf1c__Z4main_148 with pointer 0x00000000021175d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x00000000021175d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Group sizes = {1024, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

Note that in the above partitioning, the total number of work-items = 512 x 1024 = 524,288, which is larger than the actual number of loop iterations (32,767). So some of the work-items will not do any work.

Better ND-range partitioning is achieved if the number of loop iterations in the offloaded loop is known on the host. This allows the compiler and runtime to do an ND-range partitioning that matches the number of loop iterations.

To get this better partitioning, we use firstprivate(upper) instead of map(to:upper) on the target construct, as shown in the modified example below. This way, the compiler knows that the value of the variable upper on the host is the same as the value of the variable upper on the device.

```c
#pragma omp target teams distribute parallel for private(b, i, j, k, l) \
    firstprivate(upper)
for (int n = 0; n < upper; n++) {
    double ur = 0.;
    double us = 0.;
    double ut = 0.;

    k = n - (n / P) * P;
```

```txt
j = (n - k) / P;
i = (n - (j * P + k)) / (P * P);
b = n / (P * P * P);

for (l = 0; l < P; l++) {
    ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
    us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
    ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
}

w[IDX4(b, i, j, k)] = ur * us * ut;
}
```

For the modified example (where upper is firstprivate), LIBOMPTARGET\_DEBUG=1 shows the following NDrange partitioning.

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_1fed0edf__Z4main_148 with pointer 0x00000000029b3d08 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x00000000029b3d08...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

Note that in the above partitioning, the total number of work-items = 512 x 64 = 32,767, which exactly matches the actual number of loop iterations.

Using firstprivate(upper) instead of map(to:upper) reduced the runtime on the particular GPU used (1-stack only):

```txt
map(to:upper) version      : 0.000415 seconds
firstprivate(upper) version : 0.000307 seconds
```

## Allocate Memory Directly on the Device

As is known, the map clause determines how an original host variable is mapped to a corresponding variable on the device. However, the map(to: ) clause may not be the most efficient way to allocate memory for a variable on the device.

In the following example, the variables ur, us, and ut are used as work (temporary) arrays in the computations on the device. The arrays are mapped to the device using map(to: ) clauses (lines 51-53).

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
```

```c
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
        map(from:w[0:SIZE])          \
        map(to:ur[0:SIZE])          \
        map(to:us[0:SIZE])          \
        map(to:ut[0:SIZE])          \
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
```

```txt
return 0;
```

## Compilation command:

```batch
icpx -fiopenmp -fopenmp-targets=spir64 test_map_to.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

The amount of data transferred between host and device can be seen in LIBOMPTARGET\_DEBUG=1 output by grepping for "Libomptarget --> Moving". The output shows that the map(to: ) clauses for the arrays ur, us, and ut cause the transfer of 262,144 bytes from host to device for each of the arrays:

```txt
$ grep "Libomptarget --> Moving" test_map_to.debug
Libomptarget --> Moving 262144 bytes (hst:0x00007fffca630880) -> (tgt:0xff00ffffffff30000)
Libomptarget --> Moving 262144 bytes (hst:0x00007fffca670880) -> (tgt:0xff00ffffffff70000)
Libomptarget --> Moving 262144 bytes (hst:0x00007fffca6b0880) -> (tgt:0xff00ffffffffb0000)
Libomptarget --> Moving 2048 bytes (hst:0x00007fffca770880) -> (tgt:0xff00fffffffffee0000)
Libomptarget --> Moving 262144 bytes (hst:0x00007fffca730880) -> (tgt:0xff00ffffffffde0000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffffffef0000) -> (hst:0x00007fffca6f0880)
```

These data transfers are wasteful because the arrays ur, us, and ut are simply used as temporary work arrays on the device. A better approach would be to place the declarations of the arrays between the declare target and end declare target directives. This indicates that the arrays are mapped to the device data environment, but no data transfers for these arrays occur unless the target update directive is used to manage the consistency of the arrays between host and device. This approach is illustrated in the following modified example.
