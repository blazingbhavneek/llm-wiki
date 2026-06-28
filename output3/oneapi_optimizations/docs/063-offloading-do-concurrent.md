## Offloading DO CONCURRENT

The DO CONCURRENT loop was introduced in ISO Fortran 2008 and has been enhanced in more recent ISO standards. This construct tells the compiler that the loop iterations are independent. Independent iterations can be executed sequentially, in parallel, and/or offloaded to accelerators.

## Offloading DO CONCURRENT Loops Using Compiler Flags

The ifx compiler provides two flags for respectively controlling offloading DO CONCURRENT loops and data transfer schemes:

1. -fopenmp-target-do-concurrent: Tells the compiler to offload DO CONCURRENT to the device. In the absence of this flag, the execution takes place on the host.

2. -fopenmp-do-concurrent-maptype-modifier=none|present|always: This is an optional flag that helps control the host-device data transfers. In the absence of this flag, the behavior is equivalent to the behavior of the none modifier explained below. Use one of the following modifiers with this flag:

• present: Tells the compiler that data has already been moved to the device, and no further movement is required. If the data is not present on the device, using this flag will result in a runtime error.

• always: Tells the compiler that data must be moved to the device at the beginning of each region and back to the host at the end of each region.

• none: Behaves like the “present” flag if the data is on the device, otherwise it moves the data to the device at the beginning of the target region and back to the host at the end of the region.

## Example

The following do\_concurrent.f90 example shows the difference in performance using different offloading options.

```fortran
program do_concurrent
    use omp_lib
    implicit none

    integer :: i, outer
    integer, dimension(10000) :: x, y, z
    double precision      :: t0, t1, time
    x = 1
    y = 0
    z = 0
! Dummy offload to warm up the device
!$omp target
!$omp end target

    t0 = omp_get_wtime()
    do outer = 1, 24000
        !call do_work_on_host Parenting_x(x,...)
        do concurrent (i = 1:10000)
            y(i) = x(i) + 1
        enddo

        do concurrent (i = 1:10000)
            z(i) = y(i) + 1
        enddo
!call do_work_on_host using_z(z,...)
enddo
t1 = omp_get_wtime()
time = t1-t0
print *, time
end program do_concurrent
```

The basic flow of the example is as follows:

```txt
Initialize_arrays x,y,z
Dummy target region
Start_time = get_wtime()
Outer do loop
    Call do_work_on_host_updating_x
    First inner DO CONCURRENT loop (computes y based on x)
    Second inner DO CONCURRENT loop (computes z based on y)
```

```txt
Call do_work_on_host_using_z
End_time = get_wtime()
Time = End_time - Start_time
Print Time
```

A dummy target region is used before the timed region to exclude the time overhead of compiling and loading the image from the measurements.

## Compilation command:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=none do_concurrent.f90 -o none.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=present do_concurrent.f90 -o present.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=always do_concurrent.f90 -o always.out
```

## Example run command:

```ignorefile
./none.out
./present.out
./always.out
```

The following table shows the performance results as well as the number of data transfers from the host to the device and from the device to the host.

<table><tr><td>-fopenmp-do-concurrent-maptype-modifier</td><td>Time(ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>none</td><td>11.09</td><td>96k</td><td>96k</td></tr><tr><td>present</td><td>Failed</td><td>n/a</td><td>n/a</td></tr><tr><td>always</td><td>11.37</td><td>96k</td><td>96k</td></tr></table>

The use of the present modifier results in an expected runtime failure, because the data was never copied to the device before the offloaded DO CONCURRENT regions.

The performance using the none modifier is on par with the always modifier. The number of data transfers from the host to the device and from the device to the host is the same. There are 96k transfers each way. These 96k transfers correspond to: 4 copies per outer loop iteration \* 24k iterations

The following table shows all the data transfers per 1 outer loop iteration:

<table><tr><td>Host to Device</td><td>Device to Host</td></tr><tr><td>copy x (line 18)</td><td>copy x (line 20)</td></tr><tr><td>copy y (line 18)</td><td>copy y (line 20)</td></tr><tr><td>copy y (line 22)</td><td>copy y (line 24)</td></tr><tr><td>copy z (line 22)</td><td>copy z (line 24)</td></tr></table>

You don’t need all these transfers for the correct execution of the code. You only need to copy x to the device at the beginning of the first DO CONCURRENT region, and read z back from the device at the end of the second DO CONCURRENT region. This means you need 1 copy per iteration each way, totaling 24k D2M and 24k M2D transfers.

## Hybrid Technique of Offloading DO CONCURRENT Loops

The hybrid technique uses OpenMP target data regions around DO CONCURRENT region(s), and the compiler flags described in the previous section. By using the target data regions, you can control data movement and improve performance. Applying this technique to the code in the previous section will result in the following outer loop region:

```txt
do outer = 1, 24000
    !call do_work_on_host_updating_x(x,...)
    !$omp target data map(to: x) map(alloc: y) map(from: z)
    do concurrent (i = 1:10000)
        y(i) = x(i) + 1
    enddo

    do concurrent (i = 1:10000)
        z(i) = y(i) + 1
    enddo
    !$omp end target data
    !call do_work_on_host_using_z(z,...)
enddo
```

Comparing with the previous example, the new code adds

• !\$omp target data map(to:x) map(alloc: y) map(from:z) before the first DO CONCURRENT region.

• !\$omp end target data after the second DO CONCURRENT region.

## Compilation command:

```shell
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=none hybrid_do_concurrent.f90 -o none.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=present hybrid_do_concurrent.f90 -o present.out
ifx -fiopenmp -fopenmp-targets=spir64 -fopenmp-target-do-concurrent -fopenmp-do-concurrent-
maptype-modifier=always hybrid_do_concurrent.f90 -o always.out
```

## Example run command:

```ignorefile
./none.out
./present.out
./always.out
```

The following table shows the performance results as well as the number of data transfers from the host to the device and from the device to the host:

<table><tr><td>-fopenmp-do-concurrent-maptype-modifier</td><td>Time(ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>none</td><td>4.28</td><td>24k</td><td>24k</td></tr><tr><td>present</td><td>4.31</td><td>24k</td><td>24k</td></tr><tr><td>always</td><td>13.80</td><td>120k</td><td>120k</td></tr></table>

For both the none modifier and the present modifier, the optimal number of data transfers is achieved, 24k each way.

In terms of timing, compiling hybrid\_do\_concurrent.f90 with the none modifier achieves a speedup of 2.6x compared to the initial version of the code using the same modifier.

Using the always modifier results in a 15% slowdown compared to the initial version of the code using the same modifier. This slowdown is due to the extra data transfers introduced by the added target data region. In this case, the added target data region is adding a copy of x from the host to the device in each outer loop iteration as well as a copy of z from the device to the host at the end of the target data region. This brings the total number of data transfers per outer-loop iteration to 5 transfers, resulting in 120k transfers each way.

Performance comparison for the 2 versions using the present modifier is not possible, since the flag-only version is incorrect in this case as explained above.

## OpenMP 6.0’s “loop” Directive on DO CONCURRENT Loops

OpenMP 6.0 specifications added support for specifying “loop” constructs on DO CONCURRENT. This enables you to offload DO CONCURRENT loops using OpenMP target construct on DO CONCURRENT loops. It also enables you to control the data transfers using OpenMP mapping clauses.

Applying this technique to the initial version of the code will result in the following outer loop region:

```matlab
do outer = 1, 2400
    !call do_work_on_host Parenting_x(x,...)
    !$omp target data map(to: x) map(alloc: y) map(from: z)
    !$omp target teams loop
    do concurrent (i = 1:10000)
        y(i) = x(i) + 1
    enddo
    !$omp target teams loop
    do concurrent (i = 1:10000)
        z(i) = y(i) + 1
    enddo
    !$omp end target data
    !call do_work_on_host using_z(z,...)
enddo
```

As shown above, this new example adds

• !\$omp target data map(to:x) map(alloc: y) map(from:z) at the beginning of the outer loop iteration.

• !\$omp target teams loop before each DO CONCURRENT Loop.

• !\$omp end target data at the end of the outer loop iteration.

## Compilation command:

```batch
ifx -fiopenmp -fopenmp-targets=spir64 omp6_do_concurrent.f90
```

## Example run command:

```txt
./a.out
```

The following table shows the performance results:

<table><tr><td>Flag</td><td>Time (ns)</td><td>H2D</td><td>D2H</td></tr><tr><td>n/a</td><td>4.11</td><td>24,000</td><td>24,000</td></tr></table>

The performance is on par with the best performing version of the hybrid technique and the number of data transfers is 24k each way which is the optimal number of transfers for this code, as explained previously.

## Findings and Recommendations

1. While the first approach can be considered to be the simplest, as it does not require any code modification, it is clear that it is the worst in term of performance and can lead to runtime failure if present is used and the data is not actually on the device.

2. While the hybrid approach using the none or the present maptype modifier was on par with the new openmp 6.0 standard approach of offloading DO CONCURRENT loops, we recommend the latter for the following reasons:

• When using the OpenMP 6.0 new standard you do not have to rely on command-line flags. This provides portability as code written in this way will work with all compilers that support OpenMP standard.

• In the case of multiple DO CONCURRENT regions and more complicated scenarios, you can control which region(s) to offload to. This control is not possible when using compiler flags.
