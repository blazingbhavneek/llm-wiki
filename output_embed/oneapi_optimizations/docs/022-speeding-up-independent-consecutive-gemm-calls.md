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

In the above example, the array bounds (m1, k1, and n1) are input as command line arguments. The matrices a1(1:m1, 1:k1), b1(1:k1, 1:n1), and c1(1:m1, 1:n1) are allocated and initialized.

Also, the padded matrices a2(1:m2, 1:k2), b2(1:k2, 1:n2), and c1(1:m2, 1:n2) are allocated and initialized. m2 is the smallest multiple of 8 that is >= m1. Similarly, k2 is the smallest multiple of 8 that is >= k1, and n2 is the smallest multiple of 8 that is >= n1.

The program compares the time taken by the DGEMM computation on a1, b1, and c1 versus the time taken by the DGEMM computation on a2, b2, and c2.

The compilation, link and run commands used are shown below.

```txt
Compile:
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -fpp -free -c dgemm_pad_f_01.f
Link:
ifx -fiopenmp -fopenmp-targets=spir64 -qmkl -lOpenCL dgemm_pad_f_01.o
```

```javascript
Run:
ZE_AFFINITY_MASK=0 LIBOMPTARGET_DEBUG=0 ./a.out 12001 12001 12001
```

The output on the particular GPU used (1-stack only) was as follows:

```txt
ALPHA =    1.0250   BETA =    0.7500

M1 =12001  N1 =12001  K1 =12001
Time (non-padded arrays)  =    0.2388 sec

M2 =12008  N2 =12008  K2 =12008
Time (padded arrays) =    0.1648 sec
```

The above shows that padding arrays a, b, and c, the time taken by the DGEMM calls was reduced from 0.2388 seconds to 0.1648 seconds.

## References

1. Developer Reference for Intel® oneAPI Math Kernel Library - C

2. Developer Reference for Intel® oneAPI Math Kernel Library - Fortran

3. Developer Reference for Intel® oneAPI Math Kernel Library - Fortran (Matrix Arguments)

4. Introducing Batch GEMM Operations

5. Intel® oneAPI Math Kernel Library Link Line Advisor
