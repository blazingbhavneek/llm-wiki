
A Note about the -qmkl Compiler Option

Use the -qmkl option (equivalent to -qmkl=parallel) to link with a certain Intel<sup>®</sup> oneAPI Math Kernel Library threading layer depending on the threading option provided:

• For -fiopenmp, the OpenMP threading layer for Intel<sup>®</sup> Compilers

• For -tbb, the Intel<sup>®</sup> Threading Building Blocks (Intel<sup>®</sup> TBB) threading layer

Use -qmkl=sequential to link with the sequential version of Intel<sup>®</sup> oneAPI Math Kernel Library.

Note that -qmkl=parallel/sequential affects threading on the CPU only. Offloaded MKL computations will always be parallelized as appropriate, and will occupy as many Vector Engines on the GPU as possible.

## OpenMP Directives to Offload oneMKL Computations

You can use OpenMP directives to offload oneMKL computations onto the GPU.

dispatch Directive

The recommended way to offload oneMKL computations onto the GPU is to use the OpenMP 5.1 dispatch directive. You would place the call to the oneMKL routine inside a dispatch construct, as shown in the example below.

```txt
#pragma omp target data map(to: A[0:m*k], B[0:k*n]) map(tofrom: C[0:m*n])
{
    #pragma omp dispatch
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                       m, n, k, alpha, A, k, B, n, beta, C, n);
}
```

In the above example, matrices a, b, and c should accessible on the device before the dispatch construct. When the MKL routine cblas\_dgemm is called from the dispatch construct, the corresponding device pointers for a, b, and c will be passed as arguments to the MKL routine, so the device copies of a, b, and c will be used in the computation.

The use\_device\_ptr clause is not needed on the dispatch directive. The list of device pointers needed by the oneMKL routine is given in the oneMKL OpenMP offload header file, mkl\_omp\_offload.h, where the GPU variant function is declared. The user should carefully review the list of device pointers required in the oneMKL header file and make sure that the corresponding matrices are accessible from the device before calling the oneMKL routine.

## Notes

• When using dispatch to offload oneMKL computations onto the GPU, oneMKL routines expect the arrays/ matrices to be accessible on the device before the computation is started. So the user has to map matrices a, b, and c to the device, or allocate the matrices directly on the device, or allocate the matrices in Unified Shared Memory (USM) before calling the oneMKL routine. See ::ref::openmp-bp-memoryallocation-link for more information about memory allocation.

• If a oneMKL routine is not called from a dispatch construct, or if offload is disabled, then the oneMKL computations will be executed on the CPU.

• Only one call to a oneMKL routine can be issued from an OpenMP dispatch construct. If there are two consecutive calls to oneMKL routines, then the calls should be placed in separate dispatch constructs.

• The use\_device\_ptr clause is not needed on the dispatch directive.

• Depending on the version of the compiler you are using, you may need to add the compiler option - fopenmp-version=51 in order for the dispatch directive to be accepted.

## Fortran

When calling oneMKL routines from Fortran code, be sure to add the following include statement:

```txt
include "mkl_omp_offload.f90"
```

Also, if calling oneMKL Fortran API with 32-bit integers, add the following module use statement:

```txt
use onemkl_blas_omp_offload_lp64
```

On the other hand, if calling oneMKL Fortran API with 64-bit integers, add the following module use statement:

```txt
use onemkl_blas_omp_offload_ilp64
```

The following Fortran example illustrates how DGEMM is called from a Fortran program, and the include and use statements mentioned above.

```txt
!\$omp target data map(to: a, b) map(tofrom: c2)
```

!\$omp dispatch

```csv
call DGEMM('N','N',m,n,k,alpha,a,m,b,k,beta,c2,m)
```

```txt
!\$omp end target data
```

To compile and link the above Fortran example with 32-bit integers:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -qmk1 -fpp -free -c dgemm_dispatch_f.f90
ifx -fiopenmp -fopenmp-targets=spir64 -qmk1 -fsycl -L\${MKLROOT}/lib/intel64 -liomp5 -lsycl -
lOpenCL -lstdc++ -lpthread -lm -ldl -lmkl_sycl dgemm_dispatch_f.o
```

To compile and link the above Fortran example with 64-bit integers:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -m64 -DMKL_ILP64 -i8 -fpp -free -c
dgemm_dispatch_f.f90
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -fsycl -L\${MKLROOT}/lib/intel64 -liomp5 -lsycl -
lOpenCL -lstdc++ -lpthread -lm -ldl -lmkl_sycl dgemm_dispatch_f.o
```

After generating the executable (a.out), from a C/C++ or Fortran program, you can run the executable under unitrace and look for the heading “Device Timing Results” in the generated trace. Below that heading we should see the oneMKL kernels listed. This way we confirm that oneMKL computations have been offloaded onto the GPU.

Example run command:

```shell
OMP_TARGET_OFFLOAD=MANDATORY ZE_AFFINITY_MASK=0 unitrace -h -d ./a.out
```

## Batching of oneMKL GEMM Calls

The oneMKL library includes “batch” routines that allow the user to batch several oneMKL calls into a single oneMKL call. At runtime, oneMKL will intelligently execute all of the matrix operations to optimize overall performance.

For example, the cblas\_dgemm routine computes a matrix-matrix product of two general matrices a and b, returning the result in a matrix c. The cblas\_dgemm interface is shown below.

```c
void cblas_dgemm (const CBLAS_LAYOUT layout,
const CBLAS_TRANSPOSE transa, const CBLAS_TRANSPOSE transb,
const MKL_INT m, const MKL_INT n, const MKL_INT k,
const double alpha, const double *a,
const MKL_INT lda, const double *b,
const MKL_INT ldb, const double beta,
double *c, const MKL_INT ldc);
```

The cblas\_dgemm\_batch routine is similar to the cblas\_dgemm routine, but the cblas\_dgemm\_batch routine performs matrix-matrix operations on groups of matrices, processing a number of groups at once.

The cblas\_dgemm\_batch interface is shown below. Note that the interface resembles the cblas\_dgemm interface. However, it involves passing matrix arguments as arrays of pointers to matrices, and passing parameters as arrays of parameters.

```txt
void cblas_dgemm_batch (const CBLAS_LAYOUT layout,
const CBLAS_TRANSPOSE* transa_array, const CBLAS_TRANSPOSE* transb_array,
const MKL_INT* m_array, const MKL_INT* n_array, const MKL_INT* k_array,
const double* alpha_array, const double **a_array,
const MKL_INT* lda_array, const double **b_array,
const MKL_INT* ldb_array, const double* beta_array,
double **c_array, const MKL_INT* ldc_array,
const MKL_INT group_count, const MKL_INT* group_size);
```

The batch operation is defined as follows:

```python
idx = 0
for i = 0 .. group_count - 1
    alpha and beta in alpha_array[i] and beta_array[i]
    for j = 0 .. group_size[i] - 1
        a, b, and c matrices in a_array[idx], b_array[idx], and c_array[idx], respectively
        c := alpha*op(a)*op(b) + beta*c,
        idx = idx + 1
    end for
end for
```

where:

• op(X) is one of op(X) = X, or op(X) = XT, or op(X) = XH,

• alpha and beta are scalar elements of alpha\_array and beta\_array,

• a, b and c are matrices such that for m, n, and k which are elements of m\_array, n\_array, and k\_array:

• op(a) is an m-by-k matrix,

• op(b) is a k-by-n matrix,

• C is an m-by-n matrix.

• a, b, and c represent matrices stored at addresses pointed to by a\_array, b\_array, and c\_array, respectively. The number of entries in a\_array, b\_array, and c\_array, or total\_batch\_count, is equal to the sum of all of the group\_size entries.

It is possible to batch the multiplications of different shapes and parameters by packaging them into groups, where each group consists of multiplications of matrices of the same shapes (same m, n, and k) and the same parameters.

The basic assumption for the batch API are that all operations in a batch (whether in the same group or different groups) are independent of one another. So oneMKL does not guarantee any particular ordering between operations in a batch, and will try to execute multiple operations in parallel.

In general, the larger you can make the batch size, the better. This allows oneMKL to better parallelize the operations and distribute the work across the GPU.

We illustrate how two calls to cblas\_dgemm can be replaced with one call to cblas\_dgemm\_batch. The following example includes two calls to cblas\_dgemm.

```c
#pragma omp target data \
    map(to: A1[0:m*k], B1[0:k*n], A2[0:m*k], B2[0:k*n]) \
    map(tofrom: C1[0:m*n], C2[0:m*n])
{
    #pragma omp dispatch
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                    m, n, k, alpha, A1, k, B1, n, beta, C1, n);

    #pragma omp dispatch
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                    m, n, k, alpha, A2, k, B2, n, beta, C2, n);
}
```

The two calls to cblas\_dgemm in the above example can be batched together, resulting in one call to cblas\_dgemm\_batch, as shown in the following example. Note that the batch is composed of one group of size 2, since we have two matrix multiplications with the same set of parameters (layout, transa, transb, m, n, k, alpha, lda, ldb, beta, and ldc). total\_batch\_size in this case is 2.

```txt
// Call cblas_dgemm_batch
#pragma omp target enter data \
  map(to: A1[0:m*k], B1[0:k*n], C1[0:m*n]) \
  map(to: A2[0:m*k], B2[0:k*n], C2[0:m*n])
```

```c
#pragma omp target data use_device_ptr(A1, B1, C1, A2, B2, C2)
{
    a_array[0] = A1, a_array[1] = A2;
    b_array[0] = B1, b_array[1] = B2;
    c_array[0] = C1, c_array[1] = C2;
}

#pragma omp target data \
    map(to:a_array[0:2], b_array[0:2], c_array[0:2])
{
    #pragma omp dispatch
        cblas_dgemm_batch (
            CblasRowMajor,
            transa_array,
            transb_array,
            m_array,
            n_array,
            k_array,
            alpha_array,
            (const double **)a_array,
            lda_array,
            (const double **)b_array,
            ldb_array,
            beta_array,
            c_array,
            ldc_array,
            group_count,
            group_sizes);
} // end target data map

#pragma omp target exit data \
    map(from: C1[0:m*n], C2[0:m*n])
```

The performance of the above two examples when running on the particular GPU used (1-stack only) was as follows:

```txt
dgemm_example_01_c.cpp (two calls to cblas_dgemm): 2.976183 seconds
dgemm_batch_example_01_c.cpp (one call to cblas_dgemm_batch): 1.881641 seconds
```

A more complex example of batching is shown below. In this example, we have a batch composed of 3 groups (GROUP\_COUNT=3). The size of each group is a randomly chosen number between 1 and 10. Several parameters (layout, transA, transB, m, n, and k) are chosen randomly, but in each group the parameters are the same for all the multiplications. The total\_batch\_size is equal to the sum of all the group sizes.

```txt
double *a, *b, *c;
for (i = 0; i < total_batch_size; i++) {
    a = a_array[i];
    b = b_array[i];
    c = c_array[i];
#pragma omp target enter data map(to:a[0:sizea_array[i]],b[0:sizeb_array[i]],c[0:sizec_array[i]])
#pragma omp target data use_device_ptr(a,b,c)
    {
        a_array_dev[i] = a;
        b_array_dev[i] = b;
        c_array_dev[i] = c;
    }
}
#pragma omp target data map(to:a_array_dev[0:total_batch_size], \
    b_array_dev[0:total_batch_size], \
```

```txt
c_array_dev[0:total_batch_size]) device(dnum)
{
#pragma omp dispatch
    cblas_dgemm_batch(layout, transA, transB, m, n, k, alpha, (const double **) a_array_dev,
lda, (const double **) b_array_dev, ldb, beta, c_array_dev, ldc, GROUP_COUNT, group_size);
}
for (i = 0; i < total_batch_size; i++) {
    a = a_array[i];
    b = b_array[i];
    c = c_array[i];
#pragma omp target exit data
map(from:a[0:sizea_array[i]],b[0:sizeb_array[i]],c[0:sizec_array[i]])
}
```

## Speeding Up Independent, Consecutive GEMM Calls

There are various ways to speed up the execution of consecutive GEMM calls that can be executed independently. One way is to batch the GEMM calls by calling the batch version of GEMM as shown above.

Another way is to enclose the calls to GEMM by an OpenMP parallel construct, so each OpenMP thread executing the parallel region dispatches one of the GEMM calls. This parallel approach is illustrated in the following example.

```cpp
#pragma omp target data \
    map(to: A1[0:m*k], B1[0:k*n], A2[0:m*k], B2[0:k*n]) \
    map(tofrom: C1[0:m*n], C2[0:m*n])
{
    #pragma omp parallel num_threads(2)
    {
        int id = omp_get_thread_num();

        if (id == 0) {
            #pragma omp dispatch
            cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                             m, n, k, alpha, A1, k, B1, n, beta, C1, n);
        }
        else if (id == 1) {
            #pragma omp dispatch
            cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                             m, n, k, alpha, A2, k, B2, n, beta, C2, n);
        }
    }
}
```

Yet another way to speed up the execution of independent, consecutive GEMM calls is to use the nowait clause on the dispatch construct so the host thread does not have to wait for a dispatched GEMM call to complete before dispatching the next one. After the last GEMM call, we insert an OpenMP taskwait directive to guarantee that all the dispatched MKL calls complete before the host thread proceeds any further. This nowait approach is illustrated in the following example.

```txt
#pragma omp target data \
    map(to: A1[0:m*k], B1[0:k*n], A2[0:m*k], B2[0:k*n]) \
    map(tofrom: C1[0:m*n], C2[0:m*n])
{
    #pragma omp dispatch nowait
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
```

```txt
m, n, k, alpha, A1, k, B1, n, beta, C1, n);

#pragma omp dispatch nowait
cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
m, n, k, alpha, A2, k, B2, n, beta, C2, n);

#pragma omp taskwait
}
```

## Padding of Matrices Used in GEMM Computations

GEMM calls can be sped up by padding the leading dimensions, lda, ldb, and ldc, of the matrices a, b, and c, respectively.

The leading dimension of a matrix depends on the layout of the matrix in memory:

• Column major layout (C/C++): The leading dimension of a matrix is the number of columns of the matrix. • Row major layout (Fortran): The leading dimension of a matrix is the number of rows of the matrix.

There are two rules to keep in mind for choosing the sizes of matrices passed to DGEMM calls.

Rule 1: For best performance, the leading dimensions of matrices passed to GEMM calls should be a multiple of 64 bytes (full cache line size). For single precision data, this means the leading dimension should be a multiple of (64 / sizeof(float)), which is equal to 16. For double precision data, this means the leading dimension should be a multiple of (64 / sizeof(double)), which is equal to 8.

Preferably, all matrices (a, b, and c) should be padded. However, padding matrix c is less important than padding a and b.

Rule 2: For best performance, leading dimensions should not be a multiple of a large power of 2 (e.g. 4096 bytes). Increasing the leading dimension slightly (e.g. from 4096 bytes to 4096+64 bytes) can improve performance in some cases.

## Padding Example (Fortran)

The following Fortran example illustrates how matrices passed to DGEMM calls may be padded for improved performance.

```fortran
include "mkl_omp_offload.f90"

! This subroutine reads command line arguments m1, k1, and n1.
  subroutine get_arguments (m1, k1, n1)
    implicit none
    integer          :: m1, k1, n1
    character(len=32) :: m1_char, k1_char, n1_char

! First, make sure that the right number of command line arguments
! have been provided.
    if (command_argument_count() .ne. 3) then
      print *, "ERROR: Three command-line arguments expected; stopping."
      stop
    endif

! Get command line arguments.
    call get_command_argument(1, m1_char)
    call get_command_argument(2, k1_char)
    call get_command_argument(3, n1_char)

! Convert arguments to integers.
    read (m1_char,*) m1
```

```fortran
read (k1_char,*) k1
    read (n1_char,*) n1
end subroutine get_arguments

! This function returns the smallest multiple of 8 that is >= n.
! Examples:
! if n = 3, then get_mul8 = 8
! if n = 9, then get_mul8 = 16
! if n = 30, then get_mul8 = 32
! if n = 80, then get_mul8 = 8
integer function get_mul8 (n)
    implicit none
    integer :: n
    integer :: mod
    if (mod(n,8) .eq. 0) then
        get_mul8 = n
    else
        get_mul8 = ((n/8) + 1) * 8
    endif
end function get_mul8

! This subroutine initializes matrices.
subroutine init_matrix (m, k, n, a, b, c)
implicit none
integer          :: m, k, n
double precision :: a(m,k), b(k,n), c(m,n)
integer          :: i, j

do i = 1, m
    do j = 1, k
        a(i,j) = (i-1) - (0.25 * k)
    end do
end do

do i = 1, k
    do j = 1, n
        b(i,j) = -((i-1) + j)
    end do
end do

do i = 1, m
    do j = 1, n
        c(i,j) = 0.2 + i - j
    end do
end do
end subroutine init_matrix

program DGEMM_MAIN
#if defined(MKL_ILP64)
    use onemkl_blas_omp_offload_ilp64
#else
    use onemkl_blas_omp_offload_lp64
#endif
    use omp_lib
```

```fortran
use iso_fortran_env
implicit none

interface
    integer function get_mul8 (n)
        implicit none
        integer :: n
    end function get_mul8
end interface

double precision :: alpha, beta
integer :: m1, k1, n1, m2, k2, n2
double precision, allocatable :: a1(:,:)
double precision, allocatable :: b1(:,:)
double precision, allocatable :: c1(:,)

double precision, allocatable :: a2(:,:)
double precision, allocatable :: b2(:,:)
double precision, allocatable :: c2(:,)

double precision :: start_t1, end_t1
double precision :: start_t2, end_t2

! Read command line arguments m1, k1, and n1.

call get_arguments (m1, k1, n1)

!
! Initialize alpha, beta, and m2, k2, n2

alpha = 1.025
beta = 0.75

m2 = get_mul8(m1)
k2 = get_mul8(k1)
n2 = get_mul8(n1)

!
! Allocate and initialize matrices.
!
allocate( a1(1:m1,1:k1) )
allocate( b1(1:k1,1:n1) )
allocate( c1(1:m1,1:n1) )
allocate( a2(1:m2,1:k2) )
allocate( b2(1:k2,1:n2) )
allocate( c2(1:m2,1:n2) )
call init_matrix (m1, k1, n1, a1, b1, c1)
call init_matrix (m2, k2, n2, a2, b2, c2)

!\$omp target data map(to: a1, b1, a2, b2) map(tofrom: c1, c2)

! Warm up run on device
!\$omp dispatch
call DGEMM('N','N',m1,n1,k1,alpha,a1,m1,b1,k1,beta,c1,m1)
```

```fortran
! Run DGEMM on device (using matrices a1, b1, and c1)
!
    start_t1 = omp_get_wtime()

    !$omp dispatch
    call DGEMM('N','N',m1,n1,k1,alpha,a1,m1,b1,k1,beta,c1,m1)

    end_t1 = omp_get_wtime()

! Warm up run on device
    !$omp dispatch
    call DGEMM('N','N',m2,n2,k2,alpha,a2,m2,b2,k2,beta,c2,m2)

!
! Run DGEMM on device (using padded matrices a2, b2, and c2)
!
    start_t2 = omp_get_wtime()

    !$omp dispatch
    call DGEMM('N','N',m2,n2,k2,alpha,a2,m2,b2,k2,beta,c2,m2)

    end_t2 = omp_get_wtime()

    !$omp end target data

    print 100, alpha, beta
    print *
    print 101, m1, n1, k1
    print 111, (end_t1 - start_t1)
    print *
    print 102, m2, n2, k2
    print 112, (end_t2 - start_t2)

100 format(7x, "ALPHA =", f10.4, " BETA =",f10.4)
101 format(7x, "M1 =", i5," N1 =", i5, " K1 =",i5)
111 format(7x, "Time (non-padded arrays) =", f10.4, " sec")
102 format(7x, "M2 =", i5," N2 =", i5, " K2 =",i5)
112 format(7x, "Time (padded arrays) =", f10.4, " sec")

end
```
