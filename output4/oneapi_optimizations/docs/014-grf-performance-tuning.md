
## Performance Tuning Using GRF Mode Selection

This section discusses the impact of GRF mode selection on device code performance. The examples shown in this section use the OpenMP offloading model and JIT compilation flow. Two of the main features that govern GRF mode selection are the following: (1) Register pressure for kernel code (2) Number of parallel execution threads. Following is a code snippet containing an OpenMP offload region and this will be used in the forthcoming analysis.

```c
#pragma omp target teams distribute thread_limit(ZDIM *NX1 *NX1)
    for (int e = 0; e < nelt; e++) {
        double s_u[NX1 * NX1 * NX1];
        double s_D[NX1 * NX1];
        // SLM used for the three arrays here
        double s_ur[NX1 * NX1 * NX1];
        double s_us[NX1 * NX1 * NX1];
        double s_ut[NX1 * NX1 * NX1];

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
```

```txt
int k = inner / (NX1 * NX1);
    int j = (inner - k * NX1 * NX1) / NX1;
    int i = inner - k * NX1 * NX1 - j * NX1;
    if (k == 0)
        s_D[I2(i, j)] = D[I2(i, j)];
    for (; k < NX1; k += ZDIM) {
        s_u[I3(i, j, k)] = u[I4(i, j, k, e)];
    }
}

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
        int k = inner / (NX1 * NX1);
        int j = (inner - k * NX1 * NX1) / NX1;
        int i = inner - k * NX1 * NX1 - j * NX1;

        double r_G00, r_G01, r_G02, r_G11, r_G12, r_G22;

        for (; k < NX1; k += ZDIM) {
            double r_ur, r_us, r_ut;
            r_ur = r_us = r_ut = 0;
#ifdef FORCE_UNROLL
#pragma unroll NX1
#endif

        for (int m = 0; m < NX1; m++) {
            r_ur += s_D[I2(i, m)] * s_u[I3(m, j, k)];
            r_us += s_D[I2(j, m)] * s_u[I3(i, m, k)];
            r_ut += s_D[I2(k, m)] * s_u[I3(i, j, m)];
        }

        const unsigned gbase = 6 * I4(i, j, k, e);
        r_G00 = g[gbase + 0];
        r_G01 = g[gbase + 1];
        r_G02 = g[gbase + 2];
        s_ur[I3(i, j, k)] = r_G00 * r_ur + r_G01 * r_us + r_G02 * r_ut;
        r_G11 = g[gbase + 3];
        r_G12 = g[gbase + 4];
        s_us[I3(i, j, k)] = r_G01 * r_ur + r_G11 * r_us + r_G12 * r_ut;
        r_G22 = g[gbase + 5];
        s_ut[I3(i, j, k)] = r_G02 * r_ur + r_G12 * r_us + r_G22 * r_ut;
    }
}

#pragma omp parallel for
    for (int inner = 0; inner < innerub; inner++) {
        int k = inner / (NX1 * NX1);
        int j = (inner - k * NX1 * NX1) / NX1;
        int i = inner - k * NX1 * NX1 - j * NX1;
        for (; k < NX1; k += ZDIM) {
            double wr = 0.0;
            for (int m = 0; m < NX1; m++) {
                double s_D_i = s_D[I2(m, i)];
                double s_D_j = s_D[I2(m, j)];
                double s_D_k = s_D[I2(m, k)];
                wr += s_D_i * s_ur[I3(m, j, k)] + s_D_j * s_us[I3(i, m, k)] +
                    s_D_k * s_ut[I3(i, j, m)];
            }
            w[I4(i, j, k, e)] = wr;
```

```json
}
    }
}
```

There are two parameters that can be modified here: (1) Unroll factor of inner loop in line number 36 (2) Number of OpenMP teams specified in line number 1. The unroll factor can be used to control register pressure. Greater the unroll factor, higher will be the register pressure. Number of OpenMP teams can be used to control the number of parallel threads. In this discussion, kernel execution time on the device is used as metric for performance. Actual numbers are not provided as they may vary based on user environments and device settings. Following are some observations:

```txt
When unrolling is turned off, use of small GRF mode is found to provide better performance. This implies that the register pressure is not high enough to get any benefits out of using large GRF mode.

When unrolling is turned on, use of large GRF mode is found to provide better performance. This implies that the register pressure is high and large GRF mode is required to accommodate this pressure.

Increase in number of teams tends to result in better performance for larger (higher register pressure) workloads when using small GRF mode.
```
