## OpenMP Offload Best Practices

In this chapter we present best practices for improving the performance of applications that offload onto the GPU. We organize the best practices into the following categories, which are described in the sections that follow:

• Using More GPU Resources

• Minimizing Data Transfers and Memory Allocations

• Making Better Use of OpenMP Constructs

• Memory Allocation

• Fortran Example

• Clauses: is\_device\_ptr, use\_device\_ptr, has\_device\_addr, use\_device\_addr

• Prefetching

• Atomics with SLM

• OpenMP Interop with SYCL

• Offloading DO CONCURRENT

## Note:

Used the following when collecting OpenMP performance numbers:

• 2-stack Intel<sup>®</sup> GPU

• One GPU stack only (no implicit or explicit scaling).

• Intel<sup>®</sup> compilers, runtimes, and GPU drivers

• Level-Zero plugin

• Introduced a dummy target construct at the beginning of a program, so as not to measure startup time.

• Just-In-Time (JIT) compilation mode.

## Using More GPU Resources

The performance of offloaded code can be improved by using a larger number of work-items that can run in parallel, thus utilizing more GPU resources (filling up the GPU).

## Note:

• ND-range partitioning of loop iterations is decided by compiler and runtime heuristics, and also depends on the GPU driver and the hardware configuration. So it can change over time. However, the methodology of figuring out the partitioning based on LIBOMPTARGET\_DEBUG=1 output will remain the same.

## Collapse Clause

One way to increase parallelism in a loop nest is to use the collapse clause to collapse two or more loops in the loop nest. Collapsing results in a larger number of iterations that can run in parallel, thus using more work-items on the GPU.

In the following example, a loop nest composed of four perfectly nested loops is offloaded onto the GPU. The parallel for directive indicates that the outermost loop (on line 53) is parallel. The number of iterations in the loop is BLOCKS, which is equal to 8.

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

    /* map data to device */
    #pragma omp target enter data map(to: u[0:SIZE], dx[0:P * P])
```

```c
start = omp_get_wtime();

/* offload the kernel with no collapse clause */
#pragma omp target teams distribute parallel for \
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

end = omp_get_wtime();

#pragma omp target exit data map(from: w[0:SIZE])

/* print result */
printf("no-collapse-clause: w[0]=%lf time=%lf\n", w[0], end - start);

return 0;
```

## Compilation command:

```batch
icx -fiopenmp -fopenmp-targets=spir64 test_no_collapse.cpp
```

## Run command:

```txt
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=1 ./a.out
```

libomptarget.so debug information (emitted at runtime when the environment variable LIBOMPTARGET\_DEBUG=1) shows the ND-range partitioning of loop iterations and how parallelism is increased by using the collapse clause. In the output, Lb and Ub refer to the parallel loop lower bound and upper bound, respectively, in each dimension of the partitioning.

Without the collapse clause, LIBOMPTARGET\_DEBUG=1 output shows the following information about the target region on line 50.

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_9b5f515d__Z4main_145 with pointer 0x000000000143d5d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x000000000143d5d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 7, Stride = 1
Target LEVEL0 RTL --> Group sizes = {1, 1, 1}
Target LEVEL0 RTL --> Group counts = {8, 1, 1}
```

Note that without the collapse clause, the number of parallel loop iterations = 8, since the upper bound of the outermost loop (BLOCKS) = 8. In this case, we end up with 8 work-groups, with one work-item each (total work-group count = 8 x 1 x 1 = 8, and each work-group size = 1 x 1 x 1 = 1 work-item). The kernel is vectorized using SIMD 32, which means every 32 work-items in a work-group are combined into one subgroup. Since we have only one work-item per work-group, it follows that each work-group has only one subgroup where only one SIMD lane is active.

We can increase parallelism and hence the number of work-items used on the GPU by adding a collapse clause on the parallel for directive. We start by adding the collapse(2) clause, as shown in the following modified example.

```txt
/* offload the kernel with collapse clause */
#pragma omp target teams distribute parallel for collapse(2) \
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
```

LIBOMPTARGET\_DEBUG=1 output shows the following partitioning when collapse(2) is used.

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_9b5f515f__Z4main_145 with pointer 0x00000000017f45d8 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x00000000017f45d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 15, Stride = 1
Target LEVEL0 RTL --> Level 1: Lb = 0, Ub = 7, Stride = 1
Target LEVEL0 RTL --> Group sizes = {1, 1, 1}
Target LEVEL0 RTL --> Group counts = {16, 8, 1}
```

Note that with collapse(2), the number of parallel loop iterations = BLOCKS x P = 8 x 16 = 128. In this case, we end up with 128 work-groups, and each work-group has 1 work-item (total work-group count = 16 x 8 x 1 = 128, and each work-group size = 1 x 1 x 1 = 1 work-item). The kernel is vectorized using SIMD 32, which means every 32 work-items in a work-group are combined into one sub-group. Since we have only one work-item per work-group, it follows that each work-group has only one sub-group where only one SIMD lane is active.

On the other hand, if we use the collapse(3) clause, LIBOMPTARGET\_DEBUG=1 output shows the following partitioning.

```txt
Libomptarget --> Launching target execution __omp_offloading_3d_9b5f5160__Z4main_145 with pointer 0x0000000001728d08 (index=1).
Target LEVEL0 RTL --> Executing a kernel 0x0000000001728d08...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
```

```txt
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 15, Stride = 1
Target LEVEL0 RTL --> Level 1: Lb = 0, Ub = 15, Stride = 1
Target LEVEL0 RTL --> Level 2: Lb = 0, Ub = 7, Stride = 1
Target LEVEL0 RTL --> Group sizes = {8, 1, 1}
Target LEVEL0 RTL --> Group counts = {2, 16, 8}
```

With collapse(3), the number of resulting parallel loop iterations = BLOCKS x P x P = 8 x 16 x 16 = 2048. In this case, we end up with 256 work-groups, and each work-group has 8 work-items (total work-group count = 2 x 16 x 8 = 256, and each work-group size = 8 x 1 x 1 = 8 work-items). The kernel is vectorized using SIMD 32, which means every 32 work-items in a work-group are combined into one sub-group. Since we have only 8 work-items per work-group, it follows that we have only one sub-group where only 8 SIMD lanes are active.

If we were to use the collapse(4) clause, instead of collapse(3), LIBOMPTARGET\_DEBUG=1 output shows the following partitioning.

```lua
Target LEVEL0 RTL --> Executing a kernel 0x0000000001aab5d8...
Target LEVEL0 RTL --> Assumed kernel SIMD width is 32
Target LEVEL0 RTL --> Preferred group size is multiple of 64
Target LEVEL0 RTL --> Level 0: Lb = 0, Ub = 32767, Stride = 1
Target LEVEL0 RTL --> Group sizes = {64, 1, 1}
Target LEVEL0 RTL --> Group counts = {512, 1, 1}
```

With collapse(4), the number of resulting parallel loop iterations = BLOCKS x P x P x P = 8 x 16 x 16 x 16 = 32768. In this case, we have 512 work-groups, and each work-group has 64 work-items (total work-group count = 512 x 1 x 1 = 512, and each work-group size = 64 x 1 x 1 = 64 work-items). The kernel is vectorized using SIMD 32, which means every 32 work-items are combined into one sub-group. It follows that each work-group has 2 sub-groups.

Using the collapse clause significantly reduces the runtime of the loop nest. The performance of the various versions when running on the particular GPU used (1-stack only) was as follows:

```txt
no collapse version : 0.002430 seconds
collapse(2) version : 0.000839 seconds
collapse(3) version : 0.000321 seconds
collapse(4) version : 0.000325 seconds
```

The above timings show that adding the collapse(3) or collapse(4) clause gives a performance boost of about 7.5x. (0.000321 seconds versus 0.002430 seconds).

## Notes:

• On the GPU, the collapse clause may not result in any actual loop collapsing at all, but the clause conveys to the compiler and runtime the degree of parallelism in the loop nest and is used in determine the ND-range partitioning.

• To take advantage of vector loads and stores, it is recommended that the innermost loop in a loop nest not be included in the collapsing so it can be vectorized. Best performance is achieved when the innermost loop has unit stride and its number of iterations is at least as large as the SIMD width.

## Minimizing Data Transfers and Memory Allocations
