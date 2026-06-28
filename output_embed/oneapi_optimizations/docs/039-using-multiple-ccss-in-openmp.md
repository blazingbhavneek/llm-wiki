## Using Multiple CCSs in OpenMP

In OpenMP, the CCSs in each stack can be exposed as devices to offer fine-grained partitioning and control at the CCS level.

In order to expose CCSs as devices, one of the following two environment variables should be set before running the program:

The following OpenMP program illustrates the use of CCSs in FLAT mode.

First, the program determines the number of devices that are available on the platform by calling omp\_get\_num\_devices(). Then the program offloads kernels to each of the devices, where each kernel initializes a different chunk of array A.

omp\_get\_num\_devices() returns the total number of devices that are available.

The device clause on the target directive is used to specify to which device a kernel should be offloaded.

At runtime the environment variable ONEAPI\_DEVICE\_SELECTOR=”:.\*.\*” (or LIBOMPTARGET\_DEVICES=SUBSUBDEVICE) is set, along with ZEX\_NUMBER\_OF\_CCS, to expose CCSs as devices.

```c
#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

#define SIZE 320

int num_devices = omp_get_num_devices();
int chunksize = SIZE/num_devices;

int main(void)
{
    int *A;
    A = new int[sizeof(int) * SIZE];

    printf ("num_devices = %d\n", num_devices);

    for (int i = 0; i < SIZE; i++)
        A[i] = -9;

    #pragma omp parallel for
    for (int id = 0; id < num_devices; id++) {
        #pragma omp target teams distribute parallel for device(id) \
            map(tofrom: A[id * chunksize : chunksize])
        for (int i = id * chunksize; i < (id + 1) * chunksize; i++) {
            A[i] = i;
        }
    }

    for (int i = 0; i < SIZE; i++)
        if (A[i] != i)
            printf ("Error in: %d\n", A[i]);
        else
            printf ("%d\n", A[i]);
}
```

## Compilation command:

```shell
\$ icpx -fiopenmp -fopenmp-targets=spir64 flat_openmp_02.cpp
```

## Run command:

```shell
$ OMP_TARGET_OFFLOAD=MANDATORY ONEAPI_DEVICE_SELECTOR="*:*.*.*" \
ZEX_NUMBER_OF_CCS="0:4,1:4 ./a.out
```

## Notes:

• The program is identical to the one in the FLAT Mode Example - OpenMP. The only difference is that additional environment variables (ONEAPI\_DEVICE\_SELECTOR and ZEX\_NUMBER\_OF\_CCS) are set before running the program to expose CCSs (instead of stacks) as devices.

• Setting ONEAPI\_DEVICE\_SELECTOR=”:.\*.\*” causes CCSs to be exposed to the application as root devices. Alternatively, LIBOMPTARGET\_DEVICES=SUBSUBDEVICE may be set.

• ZEX\_NUMBER\_OF\_CCS=”0:4,1:4 specifies that the 4 CCSs in stack 0, as well as the 4 CCSs in stack 1, are exposed.

• OMP\_TARGET\_OFFLOAD=MANDATORY is used to make sure that the target region will run on the GPU. The program will fail if a GPU is not found.

• There is no need to specify ZE\_FLAT\_DEVICE\_HIERARCHY=FLAT with the run command, since FLAT mode is the default.

Running on a system with a single GPU card (2 stacks in total):

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY ONEAPI_DEVICE_SELECTOR="*:.*.*.*" \
ZEX_NUMBER_OF_CCS="0:4,1:4 LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 8 devices corresponding to the 8 CCSs (4 CCSs in each of the 2 stacks) have been found.

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 8 root devices, 8 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0.0.0
Target LEVEL_ZERO RTL --> -- 0.0.1
Target LEVEL_ZERO RTL --> -- 0.0.2
Target LEVEL_ZERO RTL --> -- 0.0.3
Target LEVEL_ZERO RTL --> -- 1.0.0
Target LEVEL_ZERO RTL --> -- 1.0.1
Target LEVEL_ZERO RTL --> -- 1.0.2
Target LEVEL_ZERO RTL --> -- 1.0.3
```

## Running on a system with 4 GPU cards (8 stacks in total):

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 32 devices corresponding to the 32 CCSs (4 CCSs in each of the 8 stacks) have been found:

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 32 root devices, 32 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0.0.0
Target LEVEL_ZERO RTL --> -- 0.0.1
Target LEVEL_ZERO RTL --> -- 0.0.2
Target LEVEL_ZERO RTL --> -- 0.0.3
Target LEVEL_ZERO RTL --> -- 1.0.0
Target LEVEL_ZERO RTL --> -- 1.0.1
Target LEVEL_ZERO RTL --> -- 1.0.2
Target LEVEL_ZERO RTL --> -- 1.0.3
Target LEVEL_ZERO RTL --> -- 2.0.0
Target LEVEL_ZERO RTL --> -- 2.0.1
Target LEVEL_ZERO RTL --> -- 2.0.2
Target LEVEL_ZERO RTL --> -- 2.0.3
Target LEVEL_ZERO RTL --> -- 3.0.0
Target LEVEL_ZERO RTL --> -- 3.0.1
Target LEVEL_ZERO RTL --> -- 3.0.2
Target LEVEL_ZERO RTL --> -- 3.0.3
Target LEVEL_ZERO RTL --> -- 4.0.0
Target LEVEL_ZERO RTL --> -- 4.0.1
Target LEVEL_ZERO RTL --> -- 4.0.2
Target LEVEL_ZERO RTL --> -- 4.0.3
Target LEVEL_ZERO RTL --> -- 5.0.0
Target LEVEL_ZERO RTL --> -- 5.0.1
Target LEVEL_ZERO RTL --> -- 5.0.2
Target LEVEL_ZERO RTL --> -- 5.0.3
Target LEVEL_ZERO RTL --> -- 6.0.0
```

```txt
Target LEVEL_ZERO RTL --> -- 6.0.1
Target LEVEL_ZERO RTL --> -- 6.0.2
Target LEVEL_ZERO RTL --> -- 6.0.3
Target LEVEL_ZERO RTL --> -- 7.0.0
Target LEVEL_ZERO RTL --> -- 7.0.1
Target LEVEL_ZERO RTL --> -- 7.0.2
Target LEVEL_ZERO RTL --> -- 7.0.3
```

## Using Multiple CCSs in MPI

A typical use case for running more than 1 CCS per GPU stack is in MPI applications where there are large portions of the application time consumed by non-offloaded code run on the CPU. Running with 4-CCS mode will allow the user to run with MPI ranks numbering four times the number of GPU stacks, allowing the host process to consume more CPU cores.

An example of DGEMMs executed through MPI is shown in the following source:

```c
#include "mkl.h"
#include "mkl_omp_offload.h"
#include <algorithm>
#include <chrono>
#include <limits>
#include <mpi.h>
#include <omp.h>
#define FLOAT double
#define MPI_FLOAT_T MPI_DOUBLE
#define MKL_INT_T MKL_INT
#define index(i, j, ld) (((j) * (ld)) + (i))
#define RAND() ((FLOAT)rand() / (FLOAT)RAND_MAX * 2.0 - 1.0)
#define LD_ALIGN 256
#define LD_BIAS 8
#define HPL_PTR(ptr_, al_) (((size_t)(ptr_) + (al_) - 1) / (al_)) * (al_))
static inline MKL_INT_T getld(MKL_INT_T x) {
    MKL_INT_T ld;
    ld = HPL_PTR(x, LD_ALIGN);
    if (ld - LD_BIAS >= x)
        ld -= LD_BIAS;
    else
        ld += LD_BIAS;
    return ld;
}
int main(int argc, char **argv) {
    if ((argc < 4) || (argc > 4 && argc < 8)) {
        printf("Performs a DGEMM test C = alpha*A*B + beta*C\n");
        printf("A matrix is MxK and B matrix is KxN\n");
        printf("All matrices are stored in column-major format\n");
        printf("Run as ./dgemm <M> <K> <N> [<alpha> <beta> <iterations>]\n");
        printf("Required inputs are:\n");
        printf("      M: number of rows of matrix A\n");
        printf("      K: number of cols of matrix A\n");
        printf("      N: number of cols of matrix B\n");
        printf("Optional inputs are (all must be provided if providing any):\n");
        printf("      alpha: scalar multiplier (default: 1.0)\n");
        printf("      beta: scalar multiplier (default: 0.0)\n");
        printf("      iterations: number of blocking DGEMM calls to perform "
            "(default: 10)\n");
        return EXIT_FAILURE;
    }
    MKL_INT_T HA = (MKL_INT_T)(atoi(argv[1]));
```

```cpp
MKL_INT_T WA = (MKL_INT_T)(atoi(argv[2]));
MKL_INT_T WB = (MKL_INT_T)(atoi(argv[3]));
FLOAT alpha, beta;
int niter;
if (argc > 4) {
    sscanf(argv[4], "%lf", &alpha);
    sscanf(argv[5], "%lf", &beta);
    niter = atoi(argv[6]);
} else {
    alpha = 1.0;
    beta = 0.0;
    niter = 10;
}
MKL_INT_T HB = WA;
MKL_INT_T WC = WB;
MKL_INT_T HC = HA;
MKL_INT_T ldA = getld(HA);
MKL_INT_T ldB = getld(HB);
MKL_INT_T ldC = getld(HC);
double tot_t = 0.0, best_t = std::numeric_limits<double>::max();
FLOAT *A = new FLOAT[ldA * WA];
FLOAT *B, *C, *local_B, *local_C;
MPI_Init(&argc, &argv);
int mpi_rank, mpi_size;
MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);
MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);
if (mpi_rank == 0) {
    B = new FLOAT[ldB * WB];
    C = new FLOAT[ldC * WC];
    srand(2864);
    for (int j = 0; j < WA; j++)
        for (int i = 0; i < HA; i++)
            A[index(i, j, ldA)] = RAND();
    for (int j = 0; j < WB; j++)
        for (int i = 0; i < HB; i++)
            B[index(i, j, ldB)] = RAND();
    if (beta != 0.0) {
        for (int j = 0; j < WC; j++)
            for (int i = 0; i < HC; i++)
                C[index(i, j, ldC)] = RAND();
    } else {
        for (int j = 0; j < WC; j++)
            for (int i = 0; i < HC; i++)
                C[index(i, j, ldC)] = 0.0;
    }
}
size_t sizea = (size_t)ldA * WA;
size_t local_sizeb, local_sizec;
int *displacements_b = new int[mpi_size];
int *send_counts_b = new int[mpi_size];
int *displacements_c = new int[mpi_size];
int *send_counts_c = new int[mpi_size];
int local_WB = WB / mpi_size;
send_counts_b[0] = ldB * (local_WB + WB % mpi_size);
send_counts_c[0] = ldC * (local_WB + WB % mpi_size);
displacements_b[0] = 0;
displacements_c[0] = 0;
for (int i = 1; i < mpi_size; i++) {
```

```txt
send_counts_b[i] = ldB * local_WB;
send_counts_c[i] = ldC * local_WB;
displacements_b[i] = displacements_b[i - 1] + send_counts_b[i - 1];
displacements_c[i] = displacements_b[i - 1] + send_counts_c[i - 1];
}
if (mpi_rank == 0) {
local_WB += WB % mpi_size;
}
local_sizeb = ldB * local_WB;
local_sizec = ldC * local_WB;
local_B = new FLOAT[local_sizeb];
local_C = new FLOAT[local_sizec];
MPI_Bcast(A, sizea, MPI_FLOAT_T, 0, MPI_COMM_WORLD);
MPI_Scatterv(B, send_counts_b, displacements_b, MPI_FLOAT_T, local_B,
    local_sizeb, MPI_FLOAT_T, 0, MPI_COMM_WORLD);
MPI_Scatterv(C, send_counts_c, displacements_c, MPI_FLOAT_T, local_C,
    local_sizec, MPI_FLOAT_T, 0, MPI_COMM_WORLD);
#if defined(OMP_AFFINITIZATION)
#if OMP_AFFINITIZATION == 1
int ndev = omp_get_num_devices();
int dnum = mpi_rank % ndev;
omp_set_default_device(dnum);
#endif
#endif
#pragma omp target data map(to : A[0 : sizea], local_B[0 : local_sizeb]) \
map(tofrom : local_C[0 : local_sizec])
{
#pragma omp dispatch
dgemm("N", "N", &HA, &local_WB, &WA, &alpha, A, &ldA, local_B, &ldB, &beta,
    local_C, &ldC);
for (int i = 0; i < niter; i++) {
auto start_t = std::chrono::high_resolution_clock::now();
#pragma omp dispatch
dgemm("N", "N", &HA, &local_WB, &WA, &alpha, A, &ldA, local_B, &ldB,
    &beta, local_C, &ldC);
MPI_Barrier(MPI_COMM_WORLD);
auto end_t = std::chrono::high_resolution_clock::now();
std::chrono::duration<double> diff = end_t - start_t;
tot_t += diff.count();
best_t = std::min(best_t, diff.count());
}
}
MPI_Gatherv(local_C, local_sizec, MPI_FLOAT_T, C, send_counts_c,
    displacements_c, MPI_FLOAT_T, 0, MPI_COMM_WORLD);
delete[] local_B;
delete[] local_C;
delete[] displacements_b;
delete[] displacements_c;
delete[] send_counts_b;
delete[] send_counts_c;
MPI_Allreduce(MPI_IN_PLACE, &tot_t, 1, MPI_FLOAT_T, MPI_MAX, MPI_COMM_WORLD);
MPI_Allreduce(MPI_IN_PLACE, &best_t, 1, MPI_FLOAT_T, MPI_MAX, MPI_COMM_WORLD);
if (mpi_rank == 0) {
double tflop_count = (double)2.0 * HA * WB * WA;
if (beta != 0.0)
tflop_count += (double)HA * WB;
tflop_count *= 1.E-12;
printf("Total runtime for %d iterations: %f seconds.\n", niter, tot_t);
```

```m4
printf("Mean TFLOP/s: %f\n", (double)niter * tflop_count / tot_t);
    printf("Best TFLOP/s: %f\n", (double)tflop_count / best_t);
    delete[] B;
    delete[] C;
}
delete[] A;
MPI_Finalize();
return EXIT_SUCCESS;
}
```

In this example, the DGEMMs are Intel<sup>®</sup> Math Kernel Library (Intel<sup>®</sup> MKL) calls executed through OpenMP offload. The matrices are statically partitioned among the MPI ranks.

In order to build the binary, execute:

```txt
$ cd examples/MPI/02_omp_mpi_onemkl_dgemm
$ make
```

With Intel<sup>®</sup> MPI, each process can bind to one or multiple GPU stacks. If more than one process is allocated to a GPU stack, the GPU driver will enqueue a kernel to one of the CCS associated with the stack. We can rely on the environment variable I\_MPI\_OFFLOAD\_CELL\_LIST to specify the device stacks used.

For example to run the application in 4-CCS mode, with the four MPI ranks being allocated to the first device’s first stack:

```txt
$ export ZEX_NUMBER_OF_CCS=0:4
$ export I_MPI_OFFLOAD_CELL_LIST=0,0,0,0
$ mpirun -n 4 ./dgemm 8192 8192 8192
```

If we want to run the application with the first four MPI ranks being allocated to the first device’s first stack, and second four MPI ranks being allocated to the first device’s second stack. The expectation is that this will have double the FLOP/s as the previous run:

```txt
$ export ZEX_NUMBER_OF_CCS=0:4,1:4
$ export I_MPI_OFFLOAD_CELL_LIST=0,0,0,0,1,1,1,1
$ mpirun -n 8 ./dgemm 8192 8192 8192
```

Note that the following Intel<sup>®</sup> MPI environment variables are default, but may be useful to specify or modify in some cases:

```powershell
$ export I_MPI_OFFLOAD_CELL=tile #Associated MPI ranks with GPU tiles
$ export I_MPI_OFFLOAD=1 #Enable MPI work with device pointers
$ export I_MPI_OFFLOAD_TOPOLIB=level_zero #Use Level Zero for topology detection (GPU pinning)
```

With MPICH, MPI ranks associate with a GPU stack explicitly through the environment variable ZE\_AFFINITY\_MASK. The driver will subsequently associate the rank to a CCS on the stack.

The same example application can be built with MPICH, if an appropriate MPICH installation is loaded. An example script to bind MPI ranks in a similar matter is provided in:

```shell
#!/bin/bash

if [ -z \${NCCS} ]; then
    NCCS=1
fi

if [ -z \${NGPUS} ]; then
    NGPUS=1
fi

if [ -z \${NSTACKS} ]; then
    NSTACKS=1
```

<table><tr><td>Term</td><td>Abbreviation</td><td>Definition</td></tr><tr><td>Blitter</td><td>BLT</td><td>Block Image Transferrer</td></tr><tr><td>Child Thread</td><td></td><td>A branch-node or a leaf-node thread that is created by another thread. It is a kind of thread associated with the media fixed function pipeline. A child thread is originated from a thread (the</td></tr></table>

```shell
fi

subdevices=\$((NGPU*NSTACK))

export ZE_AFFINITY_MASK=\$(((MPI_LOCALRANKID/NCCS)%subdevices))

echo MPI_LOCALRANKID = \$MPI_LOCALRANKID  ZE_AFFINITY_MASK = \$ZE_AFFINITY_MASK
exec \$@
```

Assuming that a node has 6 GPUs, each GPU has 2 stacks, and you want to run with 4 CCS per stack, usage of this script is as follows:

```shell
$ export NGPUS=6
$ export NSTACKS=2
$ export NCCS=4
$ export ZEX_NUMBER_OF_CCS=0:${NCCS},1:${NCCS}
$ mpiexec -n 48 ./gpu_rank_bind.sh ./dgemm 8192 8192 8192
```

Since the DGEMM is handled through OpenMP offload, we can also associate the MPI ranks explicitly with specific CCSs through OpenMP. Some mixed MPI/OpenMP offload applications use this strategy.

```lisp
#if OMP_AFFINITIZATION == 1
    int ndev = omp_get_num_devices();
    dnum = mpi_rank % ndev;
    omp_set_default_device(dnum);
#endif
...
#pragma omp target data map(to:A[0:sizea],local_B[0:local_sizeb])
map(tofrom:local_C[0:local_sizec])
{
...
#pragma omp dispatch
    dgemm("N","N",&HA,&local_WB,&WA,&alpha,A,&ldA,local_B,&ldB,&beta,local_C,&ldC);
...
}
```

This mode of the binary can be built by using the following options:

```shell
$ cd examples/MPI/02_omp_mpi_onemkl_dgemm
$ make OMP AFFINITIZATION=1
```

We can then run the application without explicitly specifying device affinity.

```shell
$ export ZEX_NUMBER_OF_CCS=0:4,1:4
$ export LIBOMPTARGET_DEVICES=SUBSUBDEVICE
$ mpirun -n 8 ./dgemm.out
```
