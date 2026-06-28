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
