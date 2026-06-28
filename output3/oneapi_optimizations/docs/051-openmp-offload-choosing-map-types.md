## Choose map-type Appropriately

For improved performance, it is important that the map-type for a mapped variable matches how the variable is used in the target construct.

In the following example, arrays u and dx are read only in the target construct, and array w is written to in the target construct. However, the map-types for all these variables is (inefficiently) specified to be tofrom.

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
```

```c
#define scaled_rand() ((rand() % MAX) / (1.0 * MAX))

#define IDX2(i, j) (i * P + j)
#define IDX4(b, i, j, k) ((b * P * P * P + i * P * P + j * P + k) % SIZE)

int main(void) {
    double w[SIZE];          /* output */
    double u[SIZE], dx[P * P]; /* input */
    int b, i, j, k, l;         /* loop counters */
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

    start = omp_get_wtime();

    #pragma omp target teams distribute parallel for \
        private(b, i, j, k, l) \
        map(tofrom: u[0:SIZE], dx[0:P * P]) \
        map(tofrom: w [0:SIZE])
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

    end = omp_get_wtime();

    printf("offload: w[0]=%lf time=%lf\n", w[0], end - start);

    return 0;
}
```

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
