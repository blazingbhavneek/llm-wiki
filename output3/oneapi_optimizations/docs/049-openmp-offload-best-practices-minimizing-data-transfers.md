
When offloading computations onto the GPU, it is important to minimize data transfers between the host and the device, and reduce memory allocations on the device. There are various ways to achieve this, as described below.

## Use target enter data and target exit data Directives

When variables are used by multiple target constructs, the target enter data and target exit data pair of directives can be used to minimize data transfers between host and device.

Place the target enter data directive before the first target construct to transfer data from host to device, and place the target exit data directive after the last target construct to transfer data from device to host.

Consider the following example where we have two target constructs (on lines 47 and 71), and each target construct reads arrays dx and u and and writes to array w.

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
    int b, i, j, k, l;         /* loop counters */
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

    start = omp_get_wtime();

    /* offload kernel #1 */
    #pragma omp target teams distribute parallel for collapse(4) \
        map(to: u[0:SIZE], dx[0:P * P]) map(from: w[0:SIZE]) \
        private(b, i, j, k, l)
    for (b = 0; b < BLOCKS; b++) {
        for (i = 0; i < P; i++) {
            for (j = 0; j < P; j++) {
                for (k = 0; k < P; k++) {
                    double ur = 0.;
                    double us = 0.;
                    double ut = 0.;

                    for (l = 0; l < P; l++) {
```

```c
ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
        us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
        ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
    }

    w[IDX4(b, i, j, k)] = ur * us * ut;
}
}
}

/* offload kernel #2 */
#pragma omp target teams distribute parallel for collapse(4) \
  map(to: u[0:SIZE], dx[0:P * P]) map(tofrom: w[0:SIZE]) \
  private(b, i, j, k, l)
for (b = 0; b < BLOCKS; b++) {
  for (i = 0; i < P; i++) {
    for (j = 0; j < P; j++) {
      for (k = 0; k < P; k++) {
        double ur = b + i + j - k;
        double us = b + i + j - k;
        double ut = b + i + j - k;

        for (l = 0; l < P; l++) {
          ur += dx[IDX2(i, l)] * u[IDX4(b, l, j, k)];
          us += dx[IDX2(k, l)] * u[IDX4(b, i, l, k)];
          ut += dx[IDX2(j, l)] * u[IDX4(b, i, j, l)];
        }

        w[IDX4(b, i, j, k)] += ur * us * ut;
    }
  }
}
}

end = omp_get_wtime();

/* print result */
printf("target region: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
}
```

## Compilation command:

```shell
icx-cl -fiopenmp -fopenmp-targets=spir64 test_no_target_enter_exit_data.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

When the first target construct (on line 47) is encountered:

• Since arrays dx and u appear in a map clause with the to map-type, storage is allocated for the arrays on the device, and the values of dx and u on the host are copied to the corresponding arrays on the device.

• Since array w appears in a map clause with the from map-type, uninitialized storage is allocated for array w on the device.

At the end of the first target region:

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_15ece5c8__Z4main_142 with pointer 0x00000000024cb5d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x00000000024cb5d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}

Target LEVEL0 RTL --> Executing a kernel 0x0000000002b9c5e0...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
Target LEVEL0 RTL --> Kernel Pointer argument 0 (value: 0xff00fffffee0000) was set successfully for device 0.
```

• Since array w appears in a map clause with the from map-type, the values of array w on the device are copied to the original array w on the host.

When the second target construct (on line 71) is encountered:

• Since arrays dx, u, and w appear in a map clause with the to map-type, storage is allocated for arrays dx, u, and w on the device and the values of arrays dx, u, and w on the host are copied to the corresponding arrays on the device.

At the end of the second target region:

• Since array w appears in a map clause with the from map-type, the values of array w on the device are copied to the original array w on the host.
