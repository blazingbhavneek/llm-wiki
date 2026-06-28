
## Atomics with SLM

## 1. Introduction

The atomic directive in OpenMP ensures that specified sections of code are executed as atomic operations.

To employ the atomic directive, include the #pragma omp atomic in C/C++ or the equivalent directive in Fortran before the code that needs atomic execution. For instance, the directive #pragma omp atomic update followed by x++; ensures that the increment operation on the variable x is atomic, preventing any other thread from modifying x during this operation.

## 2. Atomics with SLM

We demonstrate the use of OpenMP atomic directive with a histogram mini-program.

## 2.1 Base Code

Histograms are crucial for compiling statistics, such as analyzing sales records to identify the most popular items. Consider the following base code:

```txt
#pragma omp target teams distribute parallel for map(to : input[0 : size])
    map(tofrom : result[0 : num_types])
    for (int i = 0; i < size; i++) {
```

```txt
int type = input[i];
    result[type]++;
}
```

This code offloads to the GPU using the OpenMP target directive, where input array contains types of sold items. Each time a type is encountered, the corresponding count in result is incremented. However, this approach can lead to data races when multiple threads concurrently update the same histogram entry (result element), necessitating a mechanism to ensure exclusive access.

## 2.2 critical Directive

To avoid these data races, we can implement a critical section that blocks other threads from updating the same histogram entry concurrently.

One method to enforce this is by using OpenMP critical directive, which ensures that the enclosed commands are executed by only one thread at a time within a team. This mutual exclusion is achieved using compare-exchange loops internally. According to the OpenMP specification, critical directive does not enforce mutual exclusion across teams, so only one team can be used. Here’s how we implement it:

```c
#pragma omp target teams distribute parallel for map(to : input[0 : size])
    map(tofrom : result[0 : num_bins]) num_teams(1)
    for (int i = 0; i < size; i++) {
        int type = input[i];
#pragma omp critical
        result[type]++;
    }
```

## 2.3 atomic Directive

While the histogram updates are now correct, the use of OpenMP critical directive with compare-exchange loops incurs significant overhead. This is especially pronounced on GPUs where numerous threads may simultaneously attempt to update the same target value. Moreover, critical directive can’t use more than one team. To enhance performance, we employ OpenMP atomic directive, which requires hardware support for executing specified atomic operations. In this context, incrementing a scalar by 1 is an atomic operation supported on Intel Data Center GPU Max Series, thus making atomic directive a viable option. Here’s the improved code:

```txt
#pragma omp target teams distribute parallel for map(to : input[0 : size]) \
    map(tofrom : result[0 : num_bins])
    for (int i = 0; i < size; i++) {
        int type = input[i];
#pragma omp atomic update
        result[type]++;
    }
```

Alternatively, we can specify the sequential consistency memory order for atomic directive. Although it makes a minor difference in this scenario, it could have a more substantial impact in other contexts. Here is how we code it:

```txt
#pragma omp target teams distribute parallel for map(to : input[0 : size]) \
    map(tofrom : result[0 : num_bins])
    for (int i = 0; i < size; i++) {
        int type = input[i];
#pragma omp atomic update seq_cst
        result[type]++;
    }
```

OpenMP also supports other memory orders, such as acquire and release. More details can be found in OpenMP API 5.2 Specification.

## 2.4 atomic Directive with SLM

Building on the OpenMP atomic directive, performance can be further enhanced by leveraging Shared Local Memory (SLM). Initially, all accesses to the histogram occur in global memory, which has higher latency. However, threads within the same team can utilize a local histogram in SLM, leading to faster access speeds.

The process involves each team working on a local portion of the histogram and then merging these loca results into the global histogram, thus reducing the frequency of global memory access. The division of data among teams is handled dynamically at runtime based on the number of teams, with each team processing a specific range of data. When merging the local histograms into the global one, atomic directive is necessary to prevent data races:

```lisp
#pragma omp target teams map(to : input[0 : size])
    map(tofrom : result[0 : num_bins])
    {
        // create a local histogram using SLM in the team
        int local_histogram[NUM_BINS] = {0};
        int num_local_histogram = omp_get_num_teams();
        int team_id = omp_get_team_num();
        int chunk_size = size / num_local_histogram;
        int leftover = size % num_local_histogram;
        int local_lb = team_id * chunk_size;
        int local_ub = (team_id + 1) * chunk_size;
        // Add the leftover to last chunk.
        // e.g. 18 iterations and 4 teams -> 4, 4, 4, 6 = 4(last chunk) +
        // 2(leftover)
        if (local_ub + chunk_size > size)
            local_ub += leftover;
        if (local_ub <= size) {
#pragma omp parallel for shared(local_histogram)
            for (int i = local_lb; i < local_ub; i++) {
                int type = input[i];
#pragma omp atomic update
                local_histogram[type]++;
            }

            // Combine local histograms
#pragma omp parallel for
                for (int i = 0; i < num_bins; i++) {
#pragma omp atomic update
                result[i] += local_histogram[i];
            }
        }
    }
```

As with the previous example, we can also use the sequential consistency memory model for this implementation:

```c
#pragma omp target map(to : input[0 : size]) map(tofrom : result[0 : num_bins])
#pragma omp teams
{
    // create a local histogram using SLM in the team
    int local_histogram[NUM_BINS] = {0};
    int num_local_histogram = omp_get_num_teams();
    int team_id = omp_get_team_num();
    int chunk_size = size / num_local_histogram;
    int leftover = size % num_local_histogram;
    int local_lb = team_id * chunk_size;
    int local_ub = (team_id + 1) * chunk_size;
```

```txt
// Add the leftover to last chunk.
// e.g. 18 iterations and 4 teams -> 4, 4, 4, 6 = 4(last chunk) +
// 2(leftover)
if (local_ub + chunk_size > size)
    local_ub += leftover;
if (local_ub <= size) {
#pragma omp parallel for shared(local_histogram)
    for (int i = local_lb; i < local_ub; i++) {
        int type = input[i];
#pragma omp atomic update seq_cst
        local_histogram[type]++;
    }

    // Combine local histograms
#pragma omp parallel for
    for (int i = 0; i < num_bins; i++) {
#pragma omp atomic update seq_cst
        result[i] += local_histogram[i];
    }
}
}
```

## 3. Evaluation

The evaluations were conducted using the Intel<sup>®</sup> Data Center GPU Max 1100 and compiled with the Intel<sup>®</sup> OneAPI Toolkit 2024.2.

## 3.1 Compilation Command

```batch
icpx -O3 -fiopenmp -fopenmp-targets=spir64 histogram.cpp -o histogram.out
```

## 3.2 Run Command

```txt
LIBOMPTARGET_PLUGIN_PROFILE=1 ./histogram.out
```

## 3.3 Profiling

The OpenMP profiler was used to measure the execution times of five different kernels. This was enabled by setting LIBOMPTARGET\_PLUGIN\_PROFILE=1. The performance numbers can vary on a different system.

```txt
LIBOMPTARGET_PLUGIN_PROFILE(LEVEL_ZERO) for OMP DEVICE(0) Intel(R) Data Center GPU Max 1100,
Thread 0
-----------------------------------------------------------------
-------------------
Kernel 1                      : __omp_offloading_39_7be84d7a__Z4main_145
Kernel 2                      : __omp_offloading_39_7be84d7a__Z4main_162
Kernel 3                      : __omp_offloading_39_7be84d7a__Z4main_179
Kernel 4                      : __omp_offloading_39_7be84d7a__Z4main_196
Kernel 5                      : __omp_offloading_39_7be84d7a__Z4main_1137
-----------------------------------------------------------------
-------------------------------------------------------------------
-------------------------------------------------------------------
-------------------------------------------------------------------:
-------------------------------------------------------------------: Host Time (msec)                  Device Time (msec)
Name                   : Total   Average      Min     Max    Total   Average
Min       Max    Count
-------------------------------------------------------------------
-------------------------------------------------------------------
```

<table><tr><td>...</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Kernel 1</td><td></td><td></td><td>:</td><td>0.54</td><td>0.54</td><td>0.54</td><td>0.54</td><td>3647.86</td><td>3647.86</td></tr><tr><td>3647.86</td><td>3647.86</td><td>1.00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Kernel 2</td><td></td><td></td><td>:</td><td>0.06</td><td>0.06</td><td>0.06</td><td>0.06</td><td>3.05</td><td>3.05</td></tr><tr><td>3.05</td><td>3.05</td><td>1.00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Kernel 3</td><td></td><td></td><td>:</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.01</td><td>3.04</td><td>3.04</td></tr><tr><td>3.04</td><td>3.04</td><td>1.00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Kernel 4</td><td></td><td></td><td>:</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.11</td><td>0.11</td></tr><tr><td>0.11</td><td>0.11</td><td>1.00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Kernel 5</td><td></td><td></td><td>:</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.01</td><td>0.23</td><td>0.23</td></tr><tr><td>0.23</td><td>0.23</td><td>1.00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>...</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

Kernel description

<table><tr><td>Kernel</td><td>Line</td><td>Description</td></tr><tr><td>1</td><td>45 - 53</td><td>omp critical</td></tr><tr><td>2</td><td>62 - 70</td><td>omp atomic relaxed</td></tr><tr><td>3</td><td>79 - 87</td><td>omp atomic seq_cst</td></tr><tr><td>4</td><td>96 - 128</td><td>omp atomic relaxed with SLM</td></tr><tr><td>5</td><td>137 - 168</td><td>omp atomic seq_cst with SLM</td></tr></table>

An examination of the device assembly revealed that Kernels 2-5, employing atomic relaxed and seq\_cst memory orders, utilized a single device instruction atomic\_iadd.ugm.d32.a64 for the operation result[type]++;. In contrast, Kernel 1, which used critical directive, generated a complex compareexchange loop with over 100 instructions for the identical operation. When utilizing SLM, instructions like atomic\_iadd.slm.d32.a32 were used, significantly speeding up computations within the faster shared local memory. Notably, utilizing SLM resulted in a substantial performance boost, achieving up to a 28x speedup (0.11 ms compared to 3.05 ms). Between atomic relaxed and seq\_cst memory orders, the later is slightly slower as expected since it generates more fences in the assembly.

## 4. Summary

The comparative analysis clearly demonstrates the significant performance disparities between atomic and critical. When the hardware, such as the Intel<sup>®</sup> Data Center GPU Max Series, supports atomic operations, atomic offers a considerable advantage due to its efficiency and reduced instruction complexity. This is particularly true for straightforward atomic operations like additions. Conversely, for more complex operations not directly supported by the hardware, critical directive can still be employed but may require additional optimization to mitigate performance penalties. Furthermore, leveraging SLM in conjunction with atomic directive can enhance performance even further, as it shifts the majority of memory accesses from global to local memory, thereby reducing latency and increasing throughput.
