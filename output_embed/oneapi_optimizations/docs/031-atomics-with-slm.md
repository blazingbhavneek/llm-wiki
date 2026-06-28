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

## OpenMP Interop with SYCL

OpenMP interop construct and the related user API functions allow foreign runtime such as SYCL to operate with the properties or resources exposed by the interop object.

The first example below shows how to create an OpenMP interop for interoperability with SYCL, how to use the API functions to retrieve interop properties, and how to expose the OpenMP device data environment to SYCL.

The example initializes an OpenMP interop object obj with the targetsync type, requesting the SYCL foreign runtime with the prefer\_type(omp\_ifr\_sycl) modifier. Specifying the targetsync type makes the interop object include a synchronization object in the foreign runtime such as SYCL queue. Then, it ensures a valid SYCL interop has been created by checking the interop property value for the omp\_ipr\_fr\_id property and retrieves a handle to the SYCL queue using the targetsync property.

```cpp
// Create an interop object with SYCL queue access.
#pragma omp interp init(prefer_type(omp_ifr_sycl), targetsync : obj)
  if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
    fprintf(stderr, "ERROR: Failed to create interp with SYCL queue access\n");
    exit(1);
  }

  // Access SYCL queue returned by OpenMP interp.
  auto *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));
```

The remaining part of the example invokes simple SYCL kernel which performs vector addition for the given data, and it uses the OpenMP device data environment to simplify the required SYCL operation for allocating device memory and moving data to and from the device memory. This is possible by using the target data construct with the desired mapping and with the use\_device\_ptr clause. The use\_device\_ptr clause converts the reference to the host data to the corresponding device data created by the map clause in the target data construct. Then, the example destroys the interop object with the interop construct and destroy clause. It is highly recommended to destroy an initialized interop to release the resources created by the initialization properly.

```txt
// Use OpenMP target data environment while allowing SYCL code to access the
// device data with "use_device_ptr" clause.
#pragma omp target data map(to : a[0 : num], b[0 : num])
    \ 
    map(from : c[0 : num]) use_device_ptr(a, b, c)
    {
        auto event = q->parallel_for(num, [=](auto i) { c[i] = a[i] + b[i]; });
        event.wait();
    }

    // Release resources associated with "obj".
#pragma omp interop destroy(obj)
```

The full example code is listed below.

```cpp
//
// Code example that uses OpenMP interop and SYCL kernel.
//
// The example shows
// 1) How to create an interop object to access the cooperating SYCL queue
// 2) How to check if the interop object is for SYCL foreign runtime
// 3) How to set up device accessible memory to be used in SYCL code
//
// Compilation command:
// icpx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_1.cpp
//
#include <cstdio>
#include <omp.h>
#include <sycl/sycl.hpp>

int main() {
    constexpr int num = 16384;
```

```c
float *a = new float[num];
float *b = new float[num];
float *c = new float[num];

// Initialize host data.
for (int i = 0; i < num; i++) {
    a[i] = i + 1;
    b[i] = 2 * i;
    c[i] = 0;
}

omp_interop_t obj{omp_interop_none};

// Snippet begin0
// Create an interop object with SYCL queue access.
#pragma omp interp init(prefer_type(omp_ifr_sycl), targetsync : obj)
    if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
        fprintf(stderr, "ERROR: Failed to create interp with SYCL queue access\n");
        exit(1);
    }

    // Access SYCL queue returned by OpenMP interp.
    auto *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));
    // Snippet end0

    // Snippet begin1
    // Use OpenMP target data environment while allowing SYCL code to access the
    // device data with "use_device_ptr" clause.
#pragma omp target data map(to : a[0 : num], b[0 : num]) \
        map(from : c[0 : num]) use_device_ptr(a, b, c)
        {
            auto event = q->parallel_for(num, [=](auto i) { c[i] = a[i] + b[i]; });
            event.wait();
        }

    // Release resources associated with "obj".
#pragma omp interp destroy(obj)
    // Snippet end1

    printf("c[0] = %.3f (%.3f), c[%d] = %.3f (%.3f)\n", c[0], 1.0, num - 1,
                    c[num - 1], 3.0 * (num - 1) + 1);
    delete[] a;
    delete[] b;
    delete[] c;

    return 0;
}
```

## Compilation command:

```batch
icpx -qopenmp -fopenmp-targets=spir64 -fsycl omp_interop_sycl_1.cpp
```

## Run command:

./a.out

The following example is semantically equivalent to this OpenMP example, but it uses SYCL foreign runtime and Intel<sup>®</sup> Math Kernel Library (Intel<sup>®</sup> MKL). Note that the example was simplified to make the program perform with clear expected behavior. The example shows how to allocate/use SYCL memory objects valid between OpenMP and SYCL, and how to use the interop object with the dispatch construct, in addition to the operations presented in the previous example.

The first part of the example obtains the SYCL queue handle by initializing an interop with the interop construct on the interop object obj as is done in the previous example. Then, it allocates the host data (x and y) and the device data (d\_x and d\_y) using the SYCL’s memory allocation API function sycl::malloc\_device.

```c
// Create an interop object with SYCL queue access
#pragma omp interop init(prefer_type(omp_ifr_sycl), targetsync : obj)
    \ device(dev)

if (omp_ifr_sycl != omp_get_interop_int(obj, omp_ipr_fr_id, nullptr)) {
    fprintf(stderr, "ERROR: Failed to create interop with SYCL queue access\n");
    exit(1);
}
sycl::queue *q = static_cast<sycl::queue *>(    omp_get_interop_ptr(obj, omp_ipr_targetsync, nullptr));

// Allocate host data.
x = new float[N];
y = new float[N];

// Allocate device data using SYCL queue.
d_x = sycl::malloc_device<float>(N * sizeof(float), *q);
d_y = sycl::malloc_device<float>(N * sizeof(float), *q);
```

The next part of the code invokes OpenMP API functions omp\_target\_associate\_ptr to associate the host data to the desired device data, enabling use of the host pointers in OpenMP regions where the corresponding device pointers are used instead if applicable. This is similar to the effect of the map clause, but data movement should be done explicitly.

```c
// Associate device pointers with host pointers
omp_target_associate_ptr(&x[0], d_x, N * sizeof(float), 0, dev);
omp_target_associate_ptr(&y[0], d_y, N * sizeof(float), 0, dev);
```

The next part of the example invokes a SYCL kernel to perform SAXPY operation on the data x and y. First, it initializes the host data and copies it to the device using the SYCL’s memory copy API memcpy. Then, it invokes an Intel MKL kernel cblas\_saxpy using the dispatch construct with the interop object obj specified in the interop clause. The host pointers x and y can be used directly in the dispatch construct since the Intel MKL code ensures that the associated device pointers d\_x and d\_y are used instead, as specified by the declare variant directive with the adjust\_args clause. The interop object obj is also passed as an additional argument when the variant function is invoked in Intel MKL. The effect of the call cblas\_saxpy is the modification of the device data d\_y, so the example copies the data back to the host data y.

```c
// Initialize host data.
myVectorSet(N, 1.0, x);
myVectorSet(N, -1.0, y);

// Perform SYCL's memory copy operations from host to device.
q->memcpy(d_x, x, N * sizeof(float));
q->memcpy(d_y, y, N * sizeof(float));
q->wait();

// Invoke MKL's variant function using the dispatch construct, appending the
// interop object and replacing the host pointers with device pointers for
// "x" and "y" as specified in the directives used in MKL.
```

```c
#pragma omp dispatch interop(obj)
  cblas_saxpy(N, scalar, x, 1, y, 1);

  // Perform SYCL's memory copy operation from device to host.
  q->memcpy(y, d_y, N * sizeof(float));
  q->wait();
```

The example also updates the device data d\_x and copies it back to the host using the target construct with the map clause. Note that the always modifier is specified to force data movement since user-created mapping with omp\_target\_associate\_ptr does not incur any data movement. Finally, the code removes the data association for x and y, releases the host and the device data, and destroys the interop object obj.

```cpp
// Update device data for "x" and bring them back to host.
#pragma omp target map(always, from : x[0 : N])
  mySscal(N, scalar, x);

  printf("(1:16384) %.3f:%.3f\n", y[0], y[N - 1]);
  printf("(2:32768) %.3f:%.3f\n", x[0], x[N - 1]);

  // Remove the associated device data for the host pointers.
  omp_target_disassociate_ptr(&x[0], dev);
  omp_target_disassociate_ptr(&y[0], dev);

  delete[] x;
  delete[] y;
  sycl::free(d_x, *q);
  sycl::free(d_y, *q);

#pragma omp interop destroy(obj)
```
