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
