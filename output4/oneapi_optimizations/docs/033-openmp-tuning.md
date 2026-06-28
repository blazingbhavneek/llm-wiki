## Tuning Kernels with Local and Global Work-group Sizes in OpenMP Offload Mode

The approach of tuning kernel performance on accelerator devices as explained above for SYCL, is also applicable for implementations via OpenMP in offload mode. It is possible to customize an application kernel along with the use of OpenMP directives to make use of appropriate work-group sizes. However, this may require significant modifications to the code. The OpenMP implementation provides an option to custom tune kernels with the use of environment variables. The local and global work-group sizes for kernels in an app can be customized with the the use of two environment variables – OMP\_THREAD\_LIMIT and OMP\_NUM\_TEAMS help in setting up the local work-group size (LWS) and global work-group size (GWS) as shown below:

```txt
LWS = OMP_THREAD_LIMIT
GWS = OMP_THREAD_LIMIT * OMP_NUM_TEAMS
```

With the help of following reduction kernel example, we show the use of LWS and GWS in tuning kernel performance on accelerator device.

```c
int N = 2048;

double* A = make_array(N, 0.8);
double* B = make_array(N, 0.65);
double* C = make_array(N*N, 2.5);
if ((A == NULL) || (B == NULL) || (C == NULL))
    exit(1);

int i, j;
double val = 0.0;

#pragma omp target map(to:A[0:N],B[0:N],C[0:N*N]) map(tofrom:val)
{

#pragma omp teams distribute parallel for collapse(2) reduction(+ : val)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            val += C[i * N + j] * A[i] * B[j];
        }
    }
}

printf("val = %f10.3\n", val);

free(A);
free(B);
free(C);
```

e.g. by choosing OMP\_THREAD\_LIMIT = 1024 and OMP\_NUM\_TEAMS = 120, the LWS and GWS parameters are set to 1024 and 122880, respectively.

![](images/cb2e531f1415f628ccaeed5f4aa1df661b61b84cacbcc312ddae33a701465d87.jpg)  
The figure above shows that the best performance for this kernel comes with LWS = 1024 and GWS = 30720 which corresponds to OMP\_THREAD\_LIMIT = 1024 and OMP\_NUM\_TEAMS = 30. These environment variables will set the LWS and GWS values to a fixed numbers for all kernels offloaded via OpenMP. However, these environment variables will not affect the LWS and GWS used by highly tuned library kernels like OneMKL.
