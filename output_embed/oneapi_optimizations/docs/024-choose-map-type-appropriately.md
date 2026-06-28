You can reduce the copying of data from host to device and vice versa by using the target enter data and target exit data directives as shown in this modified example.

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <math.h>
#include <omp.h>

#define P 16
#define BLOCKS 8
#define SIZE (BLOCKS * P * P * P)
```

```c
#define MAX 100
#define scaled_rand() ((rand() % MAX) / (1.0 * MAX))

#define IDX2(i, j) (i * P + j)
#define IDX4(b, i, j, k) (b * P * P * P + i * P * P + j * P + k)

int main(void) {
    double w[SIZE];          /* output */
    double u[SIZE], dx[P * P]; /* input */
    int b, i, j, k, l;         /* loop counters */
    double start, end;           /* timers */

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

    /* map data to device. alloc for w avoids map(tofrom: w[0:SIZE]
        on target by default. */
    #pragma omp target enter data map(to: u[0:SIZE], dx[0:P * P]) \
        map(alloc: w[0:SIZE])

    /* offload kernel #1 */
    #pragma omp target teams distribute parallel for collapse(4) \
        private(b, i, j, k, l)
    for (b = 0; b < BLOCKS; b++) {
        for (i = 0; i < P; i++) {
            for (j = 0; j < P; j++) {
                for (k = 0; k < P; k++) {
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
            }
        }
    }

    /* offload kernel #2 */
    #pragma omp target teams distribute parallel for collapse(4) \
```

```c
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

#pragma omp target exit data map(from: w[0:SIZE])

end = omp_get_wtime();

/* print result */
printf("target region: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
}
```

In the modified example, when the target enter data directive (on line 48) is encountered:

• Since arrays dx and u appear in a map clause with the to map-type, storage is allocated for arrays dx and u on the device, and the values of arrays dx and u on the host are copied to the corresponding arrays on the device.

• Since array w appears in a map clause with the alloc map-type, uninitialized storage is allocated for array w on the device.

When the first target construct (on line 52) is encountered:

• The runtime checks whether storage corresponding to arrays dx, u, and w already exists on the device. Since it does, no data transfer occurs.

At the end of the first target region:

• The runtime will recognize that the storage for arrays dx, u, and w should remain on the device, and no copy back from the device to the host occurs.

When the second target construct (on line 75) is encountered:

• Again no data transfer from the host to the device occurs.

At the end of the second target region:

• The runtime will recognize that the storage for the arrays dx, u, and w should remain on the device, and no copy back from device to host will occur.

When the target exit data directive (on line 97) is encountered:

• Since array w appears in a map clause with the from map-type, the values of array w on the device are copied to the original array w on the host.

Using the target enter data and target exit data pair of directives reduced the runtime on the particular GPU used (1-stack only):

```txt
No target enter/exit data version : 0.001204 seconds
target enter/exit data version      : 0.000934 seconds
```

LIBOMPTARGET\_DEBUG=1 output shows that data partitioning is the same in both examples (with and without target enter data and target exit data).

```txt
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007ffd899939c0, Size=2048)...
Libomptarget --> Mapping exists with HstPtrBegin=0x00007ffd899939c0,
TgtPtrBegin=0xff00fffffffee0000, Size=2048, DynRefCount=2 (update suppressed), HoldRefCount=0
Libomptarget --> Obtained target argument (Begin: 0xff00fffffffee0000, Offset: 0) from host
pointer 0x00007ffd899939c0
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007ffd899539c0, Size=262144)...
Libomptarget --> Mapping exists with HstPtrBegin=0x00007ffd899539c0,
TgtPtrBegin=0xff00ffffffef0000, Size=262144, DynRefCount=2 (update suppressed), HoldRefCount=0
Libomptarget --> Obtained target argument (Begin: 0xff00ffffffef0000, Offset: 0) from host
pointer 0x00007ffd899539c0
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007ffd899139c0, Size=262144)...
```

```lua
Libomptarget --> Launching target execution __omp_offloading_3d_fadb4d__Z4main_147 with pointer 0x0000000002b9c5d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x0000000002b9c5d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

The improvement in performance when using target enter data and target exit data came from the reduction of data transfers, where we now have the following three data transfers:

```txt
$ grep "Libomptarget --> Moving" test_target_enter_exit_data.debug
Libomptarget --> Moving 262144 bytes (hst:0x00007ffd899539c0) -> (tgt:0xff00fffffffef0000)
Libomptarget --> Moving 2048 bytes (hst:0x00007ffd899939c0) -> (tgt:0xff00fffffee0000)
Libomptarget --> Moving 262144 bytes (tgt:0xff00ffffff30000) -> (hst:0x00007ffd899139c0)
```

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
