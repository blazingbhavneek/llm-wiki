# oneapi_optimizations Source Lines 13667-14189

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L13667-L14189

Citation: [oneapi_optimizations:L13667-L14189]

````text
## has\_device\_addr

The has\_device\_addr clause appears on a target directive. It indicates that the list items already have valid device addresses, and therefore may be directly accessed from the device.

Each list item must have a valid device address for the device data environment. It can be on any type, including an array section.

The has\_device\_addr clause is especially useful in Fortran, because it can be used with list items of any type (not just C\_PTR) to indicate that the list items have device addresses.

The following Fortran example illustrates the use of the has\_device\_addr clause. In the example, the three arrays A, B, and C are allocated on the device. When the arrays are referenced in a target region, we use the has\_device\_addr(A, B, C) clause to indicate that A, B, and C already have device addresses.

```fortran
program main
  use iso_fortran_env
  use omp_lib
  implicit none

  integer, parameter :: iterations=1000
  integer, parameter :: length=64*1024*1024
  real(kind=REAL64), parameter :: epsilon=1.D-8
  real(kind=REAL64), allocatable :: A(:)
  real(kind=REAL64), allocatable :: B(:)
  real(kind=REAL64), allocatable :: C(:)
  real(kind=REAL64) :: scalar=3.0
  real(kind=REAL64) :: ar, br, cr, asum
  real(kind=REAL64) :: nstream_time, avgtime
  integer :: i, iter

  !
  ! Allocate arrays in device memory
```

```fortran
!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): A)
allocate(A(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): B)
allocate(B(length))

!\$omp allocators allocate(allocator(omp_target_device_mem_alloc): C)
allocate(C(length))

!
! Initialize the arrays

!\$omp target teams distribute parallel do has_device_addr(A, B, C)
do i = 1, length
    A(i) = 2.0
    B(i) = 2.0
    C(i) = 0.0
end do

!
! Perform the computation

nstream_time = omp_get_wtime()
do iter = 1, iterations
    !\$omp target teams distribute parallel do has_device_addr(A, B, C)
    do i = 1, length
        C(i) = C(i) + A(i) + scalar * B(i)
    end do
end do
nstream_time = omp_get_wtime() - nstream_time

!
! Validate and output results

ar = 2.0
br = 2.0
cr = 0.0
do iter = 1, iterations
    do i = 1, length
        cr = cr + ar + scalar * br
    end do
end do

asum = 0.0
!\$omp target teams distribute parallel do reduction(+:asum) has_device_addr(C)
do i = 1, length
    asum = asum + abs(C(i))
end do

if (abs(cr - asum)/asum > epsilon) then
    print *, "Failed Validation on output array:", "Expected =", cr, "Observed =", asum else
    avgtime = nstream_time/iterations
    print *, "Solution validates:", "Checksum =", asum, "Avg time (s) =", avgtime endif

deallocate(A)
deallocate(B)
```

```txt
deallocate(C)
end program main
```

```txt
use_device_addr
```

The use\_device\_addr clause appears on a target data directive. It indicates that each list item already has corresponding storage on the device or is accessible on the device.

If a list item is mapped, then references to the list item in the construct are converted to references to the corresponding list item. If a list item is not mapped, it is assumed to be accessible on the device.

A list item may be an array section.

Just like has\_device\_addr, the use\_device\_addr clause is especially useful in Fortran, because it can be used with list items of any type (not just C\_PTR) to indicate that the list items have device addresses.

The following Fortran example illustrates the use of the use\_device\_addr clause. In the example, array\_d is mapped to the device with the alloc map-type, so storage is allocated for array\_d on the device and no data transfer between the host and the device occurs. We use the use\_device\_addr(array\_d) clause on the target data directive to indicate that array\_d has corresponding storage on the device.

```fortran
program target_use_device_addr

use omp_lib
use iso_fortran_env, only : real64
implicit none

integer, parameter :: N1 = 1024
real(kind=real64), parameter :: aval = real(42, real64)
real(kind=real64), allocatable :: array_d(:), array_h(:)
integer :: i,err

! Allocate host data
allocate(array_h(N1), array_d(1))

!$omp target data map (from:array_h(1:N1)) map(alloc:array_d(1:N1))
!$omp target data use_device_addr(array_d)
!$omp target has_device_addr(array_d)
    do i=1, N1
        array_d(i) = aval
        array_h(i) = array_d(i)
    end do
!$omp end target
!$omp end target data
!$omp end target data

! Check result
write (*,*) array_h(1), array_h(N1)
if (any(array_h /= aval)) then
    err = 1
else
    err = 0
end if

deallocate(array_h)
if (err == 1) then
    stop 1
else
```

```fortran
stop 0
end if

end program target_use_device_addr
```

The following table summarizes the properties of the clauses described in this section.

<table><tr><td>Clause</td><td>On which directive</td><td>Type of list item</td><td>Description</td></tr><tr><td>is_device_ptr</td><td>target, dispatch</td><td>C/C++: Pointer, array, or referenceFortran: C_PTR</td><td>Indicates that list item is a device pointer (has valid device address).</td></tr><tr><td>use_device_ptr</td><td>target data</td><td>C/C++: Pointer, array, or referenceFortran: C_PTR</td><td>Indicates that list item is a pointer to an object that has corresponding storage on device or is accessible on device.</td></tr><tr><td>has_device_addr</td><td>target</td><td>Any type (may be array section)</td><td>Indicates that list item has a valid device address.</td></tr><tr><td>use_device_addr</td><td>target data</td><td>Any type (may be array section)</td><td>Indicates that list item has corresponding storage on device or is accessible on the device.</td></tr></table>

## Prefetching

User-guided data prefetching is a useful technique for hiding latency arising from lower-level cache misses and main memory accesses. OpenMP offload for Intel<sup>®</sup> GPUs now enables this feature using the prefetch pragma, with syntax as follows:

## C OpenMP prefetch:

```txt
#pragma ompx prefetch data([prefetch-hint-modifier:],arrsect, [,arrsect]) [ if
(condition)]
```

## Fortran OpenMP prefetch:

```txt
!\$omp prefetch data( [prefetch-hint-modifier:] arrsect [, arrsect] ) [if (condition)]
```

The prefetch pragma above is an Intel<sup>®</sup> extension, and works for Intel<sup>®</sup> Data Center GPU Max Series and later products. The main aspects of the pragma are:

• Prefetch-hint: The destination for the prefetched data is specified using the optional prefetch-hintmodifier. Valid values are 0 (No-op), 2 (prefetch to L2 only) and 4 (prefetch to L1 and L2). If the value is not specified, the default value is 0.

• Array section: A contiguous array section arrsect is specified using the OpenMP syntax [lower-bound : length] in C, and (lower-bound : upper-bound) in Fortran. For example, to prefetch four elements starting at a[10] or a(10), use a[10:4] in C or a(10:13) in Fortran. Note, at the time of this writing, the compiler generates only single element prefetch requests. The examples above are therefore equivalent to a[10:1] in C, or a(10:10) in Fortran.

• Default prefetch size: Even if a single array element is requested to be prefetched, the hardware will prefetch an entire cache line that contains that element. In Intel<sup>®</sup> Data Center GPU Max Series, the size of a cache line is 64 bytes.

• Faulting: Prefetch instructions in Intel<sup>®</sup> Data Center GPU Max Series are faulting, which means accesses to invalid addresses can cause a segmentation fault. The optional if condition in the pragma can be used for guarding against out-of-bounds accesses.

• Non-blocking: The prefetch pragma does not block, it does not wait for the prefetch to complete.

## Prefetch in C OpenMP

The following example shows a simplified 1-dimension version of an N-body force kernel. The outer for-loop iterates over the particles for which the forces are calculated. The inner loops iterate over the interacting particles, in batches of TILE\_SIZE particles. We can prefetch the next stack of particles during the computations of the current stack of particles. Prefetch always brings in 64 bytes of data as described above. So we need to prefetch only one out of every 16 single-precision floating point values, which is achieved by using if ( (next\_tile % 16) == 0 ). Using this masking condition may not always help, see additional notes after the code snippet below. The prefetch hint used is 4 (prefetch to L1 and L2 cache). Only the offloaded kernel is shown below.

```lisp
#define WORKGROUP_SIZE 1024
#define PREFETCH_HINT 4 // 4 = prefetch to L1 and L3;  2 = prefetch to L3
#define TILE_SIZE 64

void nbody_1d_gpu(float *c, float *a, float *b, int n1, int n2) {
#pragma omp target teams distribute parallel for thread_limit(WORKGROUP_SIZE)
    for (int i = 0; i < n1; i++) {
        const float ma0 = 0.269327f, ma1 = -0.0750978f, ma2 = 0.0114808f;
        const float ma3 = -0.00109313f, ma4 = 0.0000605491f, ma5 = -0.00000147177f
        const float eps = 0.01f;

        float dx = 0.0;
        float bb[TILE_SIZE];
        for (int j = 0; j < n2; j += TILE_SIZE) {
            // load tile from b
            for (int u = 0; u < TILE_SIZE; ++u) {
                bb[u] = b[j + u];
#ifdef PREFETCH
                int next_tile = j + TILE_SIZE + u;
                if ((next_tile % 16) == 0) {
#pragma ompx prefetch data(PREFETCH_HINT : b[next_tile]) if (next_tile < n2)
            }
#endif
        }
#pragma unroll(TILE_SIZE)
            for (int u = 0; u < TILE_SIZE; ++u) {
                float delta = bb[u] - a[i];
                float r2 = delta * delta;
                float s0 = r2 + eps;
                float s1 = 1.0f / sqrtf(s0);
                float f =
                    (s1 * s1 * s1) -
                    (ma0 + r2 * (ma1 + r2 * (ma2 + r2 * (ma3 + r2 * (ma4 + ma5)))));
                dx += f * delta;
            }
        }
        c[i] = dx * 0.23f;
    }
}
```

The condition if ( (next\_tile % 16) == 0 ) can save on the prefetch overhead when the array index is not vectorized. In the example above, only the index i is vectorized, so when we prefetch b[] that is indexed using j, it helps to issue a prefetch only once every 16 elements. On the other hand, if we were to prefetch an array over the index i, then the prefetch is vectorized and therefore the masking condition may not offer any benefits. The user will need to experimentally determine the best approach for their application.

## Compilation command:

## Without prefetch:

```batch
icpx -O3 -g -fiopenmp -fopenmp-targets=spir64 -mcmodel=medium nbody_c.cpp -o test_c
```

With prefetch:

```batch
icpx -O3 -g -fiopenmp -fopenmp-targets=spir64 -mcmodel=medium -DPREFETCH nbody_c.cpp -o test_c
```

Run command:

```shell
LIBOMPTARGET_LEVEL_ZERO_COMPILATION_OPTIONS="-cl-strict-aliasing -cl-fast-relaxed-math" \
ZE_AFFINITY_MASK=0 LIBOMPTARGET_PLUGIN_PROFILE=T,usec IGC_ForceOCLSIMDWidth=16 ./test_c
```

The default SIMD width is chosen to be 16 or 32 automatically by the backend device compiler (Intel Graphics Compiler or IGC) on Intel<sup>®</sup> Data Center GPU Max Series by compiler heuristics that take into account factors such as register pressure in the kernel. One can use the IGC environment variable IGC\_ForceOCLSIMDWidth=16 to request the IGC compiler to force a SIMD width of 16. SIMD16 gave a better performance for the above kernel. In the run command, we have also enabled OpenMP’s built-in profiler using LIBOMPTARGET\_PLUGIN\_PROFILE=T,usec. The output from the run without prefetch was as follows below.

```txt
Obtained output = 222700231.430
Expected output = 222700339.016

Total time =      205.4 milliseconds

================—the
LIBOMPTARGET_PLUGIN_PROFILE(LEVEL_ZERO) for OMP DEVICE(0) Intel(R) Graphics [0x0bd6], Thread 0
-------------------------------------------------
-------------------
Kernel 0                          : __omp_offloading_46_3c0d785c__Z12nbody_1d_gpuPfS_S_ii_115
Kernel 1                          : __omp_offloading_46_3c0d785c__Z15clean_cache_gpuPdi_169
Kernel 2                          : __omp_offloading_46_3c0d785c__Z4main_198
-------------------------------------------------
-------------------
-----------------------------------
-----------------------------------:
-----------------------------------:
Name                             : Host Time (usec)
Min                   : Total   Average     Min       Max    Total   Average
Max         Count
-----------------------------------------------------------------------
-------------------
Compiling                         : 598283.05 598283.05 598283.05 598283.05      0.00      0.00
0.00        0.00      1.00
DataAlloc                         : 9578.23   798.19      0.00   8728.03      0.00      0.00
0.00        0.00      12.00
DataRead (Device to Host) :   77.01   77.01   77.01   77.01   5.68      5.68
5.68        5.68      1.00
DataWrite (Host to Device):   713.11   356.55   179.05   534.06   15.76      7.88
5.04        10.72      2.00
Kernel 0                          : 205292.22   2052.92   2033.95   2089.98 203572.32   2035.72
1984.96   2073.12    100.00
Kernel 1                          : 109194.28   1091.94   1076.94   1681.09 107051.52   1070.52
1062.40   1107.04    100.00
Kernel 2                          : 1746.89   1746.89   1746.89   1746.89      3.84      3.84
3.84        3.84      1.00
Linking                         :   0.00      0.00      0.00      0.00      0.00      0.00
0.00        0.00      1.00
OffloadEntriesInit          : 2647.88   2647.88   2647.88   2647.88      0.00      0.00
0.00        0.00      1.00
```

```txt
Obtained output = 222700231.430
Expected output = 222700339.016

Total time =      185.9 milliseconds

-----------------------------------------------------------------------
LIBOMPTARGET_PLUGIN_PROFILE(LEVEL_ZERO) for OMP DEVICE(0) Intel(R) Graphics [0x0bd6], Thread 0
-----------------------------------------------------------------------
Kernel 0                      : __omp_offloading_43_3c0d785c__Z12nbody_1d_gpuPfS_S_ii_115
Kernel 1                      : __omp_offloading_43_3c0d785c__Z15clean_cache_gpuPdi_169
Kernel 2                      : __omp_offloading_43_3c0d785c__Z4main_198
-----------------------------------------------------------------------
-----------------------------------------------------------------------
Name                  : Host Time (usec)                 Device Time (usec)
Min         : Total   Average     Min    Max    Total    Average
Max       Count
-----------------------------------------------------------------------
Compiling              : 499351.98 499351.98 499351.98 499351.98      0.00      0.00
0.00        0.00      1.00
DataAlloc             : 9609.94     800.83      0.00     8740.19      0.00      0.00
0.00        0.00      12.00
DataRead (Device to Host) :   77.01     77.01     77.01     77.01     4.96     4.96
4.96        4.96      1.00
DataWrite (Host to Device):   722.17     361.08     185.01     537.16     16.40      8.20
5.44        10.96      2.00
Kernel 0                   : 185793.88     1857.94     1839.88     1919.03 184075.20      1840.75
1824.00   1874.56     100.00
Kernel 1                   : 109442.95     1094.43     1076.94     1590.01 107334.56      1073.35
1062.40   1115.68     100.00
Kernel 2                   : 1821.99     1821.99     1821.99     1821.99      3.84      3.84
3.84        3.84      1.00
Linking              :   0.00      0.00      0.00      0.00      0.00      0.00
0.00        0.00      1.00
OffloadEntriesInit          : 2493.14     2493.14     2493.14     2493.14      0.00      0.00
0.00        0.00      1.00
-----------------------------------------------------------------------
-----------------------------------------------------------------------
```

From the output above, the average device time for the GPU kernel execution (Kernel 0) is 2036 microseconds. If we run the binary with prefetch enabled, the average kernel device time observed was 1841 microseconds, as shown below:

Please note that the achieved performance depends on the hardware and the software stack used, so users may see different performance numbers at their end.

## Prefetch in Fortran OpenMP

The same nbody1d kernel is shown in Fortran below. The prefetch pragma is inserted in the same location as before, with prefetch hint of value 4, and again prefetching only one out of every 16 elements.

```txt
#define WORKGROUP_SIZE 1024
#define PREFETCH_HINT 4      ! 4 = prefetch to L1 and L3;  2 = prefetch to L3
#define TILE_SIZE 64

    module gpu_kernels
    contains
    subroutine nbody_1d_gpu(c, a, b, n1, n2)
```

```txt
implicit none
integer n1, n2
real a(0:n1-1), b(0:n2-1), c(0:n1-1)
real dx, bb(0:TILE_SIZE-1), delta, r2, s0, s1, f
integer i,j,u,next
real ma0, ma1, ma2, ma3, ma4, ma5, eps
parameter (ma0=0.269327, ma1=-0.0750978, ma2=0.0114808)
parameter (ma3=-0.00109313, ma4=0.0000605491, ma5=-0.00000147177)
parameter (eps=0.01)

!\$omp target teams distribute parallel do thread_limit(WORKGROUP_SIZE)
!\$omp& private(i,dx,j,u,bb,next,delta,r2,s0,s1,f)
do i = 0, n1-1
dx = 0.0
do j = 0, n2-1, TILE_SIZE
! load tile from b
do u = 0, TILE_SIZE-1
bb(u) = b(j+u)
#ifdef PREFETCH
next = j + TILE_SIZE + u
if (mod(next,16).eq.0) then
!\$omp prefetch data(PREFETCH_HINT:b(next:next))if(next<n2)
endif
#endif
enddo
! compute
!DIR\$ unroll(TILE_SIZE)
do u = 0, TILE_SIZE-1
delta = bb(u) - a(i)
r2 = delta*delta
s0 = r2 + eps
s1 = 1.0 / sqrt(s0)
f = (s1*s1*s1)-(ma0+r2*(ma1+r2*(ma2+r2*(ma3+r2*(ma4+ma5)))))
dx = dx + f*delta
enddo
enddo
c(i) = dx*0.23
enddo
end subroutine
```

## Compilation command:

## Without prefetch:

```shell
ifx -O3 -g -fiopenmp -fopenmp-targets=spir64 -fpconstant -fpp -ffast-math \
-fno-sycl-instrument-device-code -mcmodel=medium nbody_f.f -o test_f
```

## With prefetch:

```shell
ifx -O3 -g -fiopenmp -fopenmp-targets=spir64 -fpconstant -fpp -ffast-math \
-fno-sycl-instrument-device-code -mcmodel=medium -DPREFETCH nbody_f.f -o test_f
```

## Run command:

```shell
LIBOMPTARGET_LEVEL_ZERO_COMPILATION_OPTIONS="-cl-strict-aliasing -cl-fast-relaxed-math" \
ZE_AFFINITY_MASK=0 LIBOMPTARGET_PLUGIN_PROFILE=T,usec IGC_ForceOCLSIMDWidth=16 ./test_f
```

The output is not shown here since it looks like the output of the C example. The average kernel time without and with prefetch were respectively, 2017 us and 1823 us. Again, please note that users may see different performance numbers, depending on the actual hardware and the software stack used.

## Prefetch in C OpenMP SIMD

OpenMP offload also supports a SIMD programming model wherein all computations are specified in terms of EU threads that comprise 16 or 32 SIMD lanes in Intel<sup>®</sup> Data Center GPU Max Series. Correspondingly, even the thread\_limit() clause in OpenMP takes on a modified meaning, and now specifies the number of EU threads per work-group. The OpenMP SIMD version of the nbody1d kernel is listed below. We need to explicitly specify the SIMD width, which is VECLEN=16. At the time of this writing, the prefetch pragma is recommended to be used outside the scope of the simd clause, which means only one SIMD lane will issue a prefetch instruction. In this example, 1 out of 16 lanes will carry out prefetch, which is exactly what we need – so we no longer need if ( (next\_tile % 16) == 0 ) that we had used in the previous examples above.

```lisp
#define WORKGROUP_SIZE 1024
#define PREFETCH_HINT 4 // 4 = prefetch to L1 and L3;  2 = prefetch to L3
#define TILE_SIZE 64

void nbody_1d_gpu(float *c, float *a, float *b, int n1, int n2) {
#pragma omp target teams distribute parallel for thread_limit(WORKGROUP_SIZE / \
                          VECLEN)
    for (int i = 0; i < n1; i += VECLEN) {
        const float ma0 = 0.269327f, ma1 = -0.0750978f, ma2 = 0.0114808f;
        const float ma3 = -0.00109313f, ma4 = 0.0000605491f, ma5 = -0.00000147177f;
        const float eps = 0.01f;

        float dx[VECLEN];
        float aa[VECLEN], bb[TILE_SIZE];
#pragma omp simd simdlen(VECLEN)
#pragma unroll(0)
        for (int v = 0; v < VECLEN; ++v) {
            dx[v] = 0.0f;
            aa[v] = a[i + v];
        }
        for (int j = 0; j < n2; j += TILE_SIZE) {
            // load tile from b
            for (int u = 0; u < TILE_SIZE; u += VECLEN) {
#pragma omp simd simdlen(VECLEN)
#pragma unroll(0)
                for (int v = 0; v < VECLEN; ++v)
                    bb[u + v] = b[j + u + v];
#ifdef PREFETCH
#pragma ompx prefetch data(
    PREFETCH_HINT : b[j + TILE_SIZE + u]) if ((j + TILE_SIZE + u) < n2)
#endif
    }
// compute current tile
#pragma omp simd simdlen(VECLEN)
#pragma unroll(0)
    for (int v = 0; v < VECLEN; ++v) {
#pragma unroll(TILE_SIZE)
                for (int u = 0; u < TILE_SIZE; ++u) {
                    float delta = bb[u] - aa[v];
                    float r2 = delta * delta;
                    float s0 = r2 + eps;
                    float s1 = 1.0f / sqrtf(s0);
                    float f =
                        (s1 * s1 * s1) -
                        (ma0 + r2 * (ma1 + r2 * (ma2 + r2 * (ma3 + r2 * (ma4 + ma5)))));
                    dx[v] += f * delta;
                }
```

```txt
}
}
#pragma omp simd simdlen(VECLEN)
#pragma unroll(0)
    for (int v = 0; v < VECLEN; ++v) {
        c[i + v] = dx[v] * 0.23f;
    }
}
}
```

## Compilation command:

We need to use an additional compilation switch -fopenmp-target-simd to enable the SIMD programming model. The compilation command is therefore as follows:

Without prefetch:

```shell
icpx -O3 -g -fiopenmp -fopenmp-targets=spir64 -mcmodel=medium \
-fopenmp-target-simd nbody_c_simd.cpp -o test_c_simd
```

With prefetch:

```batch
icpx -O3 -g -fiopenmp -fopenmp-targets=spir64 -mcmodel=medium -DPREFETCH \
-fopenmp-target-simd nbody_c_simd.cpp -o test_c_simd
```

## Run command:

```shell
LIBOMPTARGET_LEVEL_ZERO_COMPILATION_OPTIONS="-cl-strict-aliasing -cl-fast-relaxed-math" \
ZE AFFINITY_MASK=0 LIBOMPTARGET_PLUGIN_PROFILE=T,usec ./test_c_simd
```

Notice that we no longer need the environment variable IGC\_ForceOCLSIMDWidth=16, because the SIMD width has been explicitly specified in the OpenMP code.

The output looks like the previous examples, so it is not shown. The average kernel time without and with prefetch are respectively, 2008 us and 1810 us. As noted earlier, users may see different performance numbers, depending on the actual hardware and the software stack used.
````
