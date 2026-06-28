
## COMPOSITE Mode Programming

As mentioned earlier, in COMPOSITE mode,each GPU card is exposed as a root device. If the card contains more than one stack, then the stacks on the GPU card are exposed as subdevices.

In COMPOSITE mode, offloading can be done using either explicit or implicit scaling. In the following sections we describe implicit and explicit scaling in more detail.

• Explicit Scaling

• Implicit Scaling

## Explicit Scaling

In explicit scaling, the programmer takes direct control over work group distribution and memory placement.

In this section, we cover:

• Explicit Scaling - SYCL

• Explicit Scaling - OpenMP

• Explicit Scaling Summary

Explicit Scaling - SYCL

In this section we describe explicit scaling in SYCL in COMPOSITE mode provide usage examples.

## Unified shared memory (USM)

Memory allocated against a root device is accessible by all of its subdevices (stacks). So if you are operating on a context with multiple subdevices of the same root device, then you can use malloc\_device on that root device instead of using the slower malloc\_host. Remember that if using malloc\_device you would need an explicit copy out to the host if it necessary to see data on the host. Refer to section Unified Shared Memory Allocations for the details on the three types of USM allocations.

## subdevice

Intel<sup>®</sup> Data Center GPU Max 1350 or 1550 has 2 stacks. The root device, corresponding to the whole GPU, can be partitioned to 2 subdevices, each subdevice corresponding to a physical stack.

```rust
try {
    vector<device> SubDevices = RootDevice.create_sub_devices<
        cl::sycl::info::partition_property::partition_by_affinity_domain>(
        cl::sycl::info::partition_affinity_domain::numa);
}
```

In SYCL, each call to create\_sub\_devices will return exactly the same subdevices.

Note that the partition\_by\_affinity\_domain is the only partitioning supported for Intel GPUs. Similarly, next\_partitionable and numa are the only partitioning properties supported (both doing the same thing).

To control what subdevices are exposed, one can use ONEAPI\_DEVICE\_SELECTOR described in ONEAPI\_DEVICE\_SELECTOR in \_oneAPI DPC++ Compiler documentation.

To control what subdevices are exposed by the Level-Zero User-Mode Driver (UMD) one can use ZE\_AFFINITY\_MASK environment variable described in Affinity Mask in Level Zero Specification Documentation.

In COMPOSITE mode, each subdevice (stack) can be further decomposed to subsubdevices (Compute Command Streamers or CCSs). For more information about subsubdevices, refer to Advanced Topics section.

## Context

A context is used for resources isolation and sharing. A SYCL context may consist of one or multiple devices. Both root devices and subdevices can be within single context, but they all should be of the same SYCL platform. A SYCL program (kernel\_bundle) created against a context with multiple devices will be built for each of the root devices in the context. For a context that consists of multiple subdevices of the same root device only a single build (to that root device) is needed.

## Buffers

SYCL buffers are created against a context and are mapped to the Level-Zero USM allocation discussed above. Current mapping is as follows.

• For an integrated device, the allocations are made on the host, and are accessible by the host and the device without any copying.

• Memory buffers for a context with subdevices of the same root device (possibly including the root device itself) are allocated on that root device. Thus they are readily accessible by all the devices in the context. The synchronization with the host is performed by the SYCL runtime with map/unmap doing implicit copies when necessary.

• Memory buffers for a context with devices from different root devices in it are allocated on the host (thus made accessible to all devices).

## Queues

A SYCL queue is always attached to a single device in a possibly multi-device context. Here are some typica scenarios, in the order of most performant to least performant:

## Context associated with a single subdevice

Creating a context with a single subdevice in it and the queue is attached to that subdevice (stack): In this scheme, the execution/visibility is limited to the single subdevice only, and expected to offer the best performance per stack. See code example:

```txt
try {
    vector<device> SubDevices = ...;
    for (auto &D : SubDevices) {
        // Each queue is in its own context, no data sharing across them.
        auto Q = queue(D);
        Q.submit([&](handler &cgh) { ... });
    }
}
```

## Context associated with multiple subdevices

Creating a context with multiple subdevices (multiple stacks) of the same root device: In this scheme, queues are attached to the subdevices, effectively implementing “explicit scaling”. In this scheme, the root device should not be passed to such a context for better performance. See code example below:

```txt
try {
  vector<device> SubDevices = ...;
  auto C = context(SubDevices);
  for (auto &D : SubDevices) {
    // All queues share the same context, data can be shared across
    // queues.
    auto Q = queue(C, D);
    Q.submit([&](handler &cgh) { ... });
  }
}
```

## Context associated with a single root device

Creating a context with a single root device in it and the queue is attached to that root device: In this scheme, the work will be automatically distributed across all subdevices/stacks via “implicit scaling” by the GPU driver, which is the most simple way to enable multi-stack hardware but does not offer the possibility to target specific stacks. See code example below:

```txt
try {
  // The queue is attached to the root-device, driver distributes to
  // sub - devices, if any.
  auto D = device(gpu_selector{});
  auto Q = queue(D);
  Q.submit([&](handler &cgh) { ... });
}
```

## Context associated with multiple root devices

Creating Contexts with multiple root devices (multi-card): This scheme, the most nonrestrictive context with queues attached to different root devices, offers more sharing possibilities at the cost of slow access through host memory or explicit copies needed. See a code example:

```txt
try {
    auto P = platform(gpu_selector{});
    auto RootDevices = P.get_devices();
```

```txt
auto C = context(RootDevices);
for (auto &D : RootDevices) {
    // Context has multiple root-devices, data can be shared across
    // multi - card(requires explicit copying)
    auto Q = queue(C, D);
    Q.submit([&](handler &cgh) { ... });
}
}
```

Depending on the chosen explicit subdevices usage described and the algorithm used, make sure to do proper memory allocation/synchronization. The following program is a full example using explicit subdevices - one queue per stack:

```cpp
#include <sycl/sycl.hpp>
#include <algorithm>
#include <cassert>
#include <cfloat>
#include <iostream>
#include <string>
using namespace sycl;

constexpr int num_runs = 10;
constexpr size_t scalar = 3;

cl_ulong triad(size_t array_size) {

    cl_ulong min_time_ns0 = DBL_MAX;
    cl_ulong min_time_ns1 = DBL_MAX;

    device dev = device(gpu_selector_v);

    auto part_prop =
        dev.get_info<sycl::info::device::partition_properties>();
    if (part_prop.empty()) {
        std::cout << "Device cannot be partitioned to subdevices\n";
        exit(1);
    }

    std::vector<device> subdev = {};
    subdev = dev.create_sub_devices<sycl::info::partition_property::
        partition_by_affinity_domain>(sycl::info::partition_affinity_domain::numa);

    queue q[2] = {queue(subdev[0], property::queue::enable_profiling{}),
        queue(subdev[1], property::queue::enable_profiling{})|};

    std::cout << "Running on device: " <<
        q[0].get_device().get_info<info::device::name>() << "\n";
    std::cout << "Running on device: " <<
        q[1].get_device().get_info<info::device::name>() << "\n";

    double *A0 = malloc_shared<double>(array_size/2 * sizeof(double), q[0]);
    double *B0 = malloc_shared<double>(array_size/2 * sizeof(double), q[0]);
    double *C0 = malloc_shared<double>(array_size/2 * sizeof(double), q[0]);

    double *A1 = malloc_shared<double>(array_size/2 * sizeof(double), q[1]);
    double *B1 = malloc_shared<double>(array_size/2 * sizeof(double), q[1]);
    double *C1 = malloc_shared<double>(array_size/2 * sizeof(double), q[1]);
```

```cpp
for (size_t i = 0; i < array_size/2; i++) {
    A0[i]= 1.0; B0[i]= 2.0; C0[i]= 0.0;
    A1[i]= 1.0; B1[i]= 2.0; C1[i]= 0.0;
}

for (int i = 0; i< num_runs; i++) {
    auto q0_event = q[0].submit([&](handler& h) {
        h.parallel_for(array_size/2, [=](id<1> idx) {
            C0[idx] = A0[idx] + B0[idx] * scalar;
        });
    });
    auto q1_event = q[1].submit([&](handler& h) {
        h.parallel_for(array_size/2, [=](id<1> idx) {
            C1[idx] = A1[idx] + B1[idx] * scalar;
        });
    });
    q[0].wait();
    q[1].wait();

    cl_ulong exec_time_ns0 =
        q0_event.get_profiling_info<info::event_profiling::command_end>() -
        q0_event.get_profiling_info<info::event_profiling::command_start>();

    std::cout << "Tile-0 Execution time (iteration " << i << ") [sec]: "
       << (double)exec_time_ns0 * 1.0E-9 << "\n";
    min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);

    cl_ulong exec_time_ns1 =
        q1_event.get_profiling_info<info::event_profiling::command_end>() -
        q1_event.get_profiling_info<info::event_profiling::command_start>();

    std::cout << "Tile-1 Execution time (iteration " << i << ") [sec]: "
       << (double)exec_time_ns1 * 1.0E-9 << "\n";
    min_time_ns1 = std::min(min_time_ns1, exec_time_ns1);
}

// Check correctness
bool error = false;
for (size_t i = 0; i < array_size/2; i++) {
    if ((C0[i] != A0[i] + scalar * B0[i]) || (C1[i] != A1[i] + scalar * B1[i])) {
        std::cout << "\nResult incorrect (element " << i << " is " << C0[i] << ")!\n";
        error = true;
    }
}

sycl::free(A0, q[0]);
sycl::free(B0, q[0]);
sycl::free(C0, q[0]);

sycl::free(A1, q[1]);
sycl::free(B1, q[1]);
sycl::free(C1, q[1]);

if (error) return -1;

std::cout << "Results are correct!\n\n";
```

```cpp
return std::max(min_time_ns0, min_time_ns1);
}

int main(int argc, char *argv[]) {

  size_t array_size;
  if (argc > 1) {
    array_size = std::stoi(argv[1]);
  }
  else {
    array_size = 128;
    std::cout << "Use default array size 128" << std::endl;
  }
  std::cout << "Running with stream size of " << array_size
    << " elements (" << (array_size * sizeof(double))/(double)1024/1024 << "MB)\n";

  cl_ulong min_time = triad(array_size);

  if (min_time == static_cast<cl_ulong>(-1)) return 1;
  size_t triad_bytes = 3 * sizeof(double) * array_size;
  std::cout << "Triad Bytes: " << triad_bytes << "\n";
  std::cout << "Time in sec (fastest run): " << min_time * 1.0E-9 << "\n";
  double triad_bandwidth = 1.0E-09 * triad_bytes/(min_time*1.0E-9);
  std::cout << "Bandwidth of fastest run in GB/s: " << triad_bandwidth << "\n";
  return 0;
}
```

The build command using Ahead-Of-Time or AOT compilation is:

```batch
icpx -fsycl -fsycl-targets=spir64_gen -O2 -ffast-math -Xs "-device pvc" explicit-subdevice.cpp -o run.exe
```

## References

1. Affinity Mask in Level Zero Specification Documentation

2. ONEAPI\_DEVICE\_SELECTOR in \_oneAPI DPC++ Compiler documentation

## Explicit Scaling - OpenMP

In this section we describe explicit scaling in OpenMP in COMPOSITE mode provide usage examples. Remember to set the environment variable ZE\_FLAT\_DEVICE\_HIERARCHY=COMPOSITE to enable COMPOSITE mode.

## Unified Shared Memory (USM)

Three OpenMP APIs as Intel extensions for USM memory allocations have been added: omp\_target\_alloc\_host, omp\_target\_alloc\_device, and omp\_target\_alloc\_shared.

Please refer to OpenMP USM Allocation API section for details.

## Offloading to multiple subdevices

In this scheme, we have multiple subdevices on which the code will run, and queues are attached to the subdevices. This effectively results in “explicit scaling”. See code example below:

```c
#define DEVKIND 0 // Stack

int root_id = omp_get_default_device();
```

```txt
#pragma omp parallel for
for (int id = 0; id < NUM_SUBDEVICES; ++id) {

#pragma omp target teams distribute parallel for device(root_id)
    subdevice(DEVKIND, id) map(...)
    for (int i = lb(id), i < ub(id); i++) {
        ...
    }
}
```

In COMPOSITE mode, each subdevice (stack) can be further decomposed to subsubdevices (Compute Command Streamers or CCSs). For more information about subsubdevices, refer to Advanced Topics section.

## Offloading to a single root device

In this scheme, we have a single root device and a queue attached to the root device. The work will be automatically distributed across all subdevices/stacks via “implicit scaling” by the GPU driver. This is the most simple way to enable multi-stack utilization, without targeting specific stacks. See code example below:

```c
int root_id = omp_get_default_device();

#pragma omp target teams distribute parallel for device(root_id) map(...)
for (int i = 0, i < N; i++) {
    ...
}
```

## Offloading to multiple root devices

In this scheme, we have multiple root devices, where each root device is a GPU card. The queues are attached to the root devices, which offers more sharing possibilities but at the cost of slow access through host memory or explicit copying of data. See code example:

```txt
int num_devices = omp_get_num_devices();

#pragma omp parallel for
for (int root_id = 0; root_id < num_devices; root_id++) {

#pragma omp target teams distribute parallel for device(root_id) map(...)
    for (int i = lb(root_id); I < ub(root_id); i++) {
        ...
    }
}
```

Program: Offloading to subdevices (stacks) in COMPOSITE mode

Depending on the chosen devices or subdevices used, as well as the algorithm used, be sure to do proper memory allocation/synchronization. The following is a full OpenMP program that offloads to multiple subdevices (stacks) in COMPOSITE mode.

```c
#include <assert.h>
#include <iostream>
#include <omp.h>
#include <stdint.h>
#ifndef NUM_SUBDEVICES
#define NUM_SUBDEVICES 1
#endif

#ifndef DEVKIND
#define DEVKIND 0 // Stack
```

```txt
#endif

template <int num_subdevices> struct mptr {
  float *p[num_subdevices];
};

int main(void) {
  constexpr int SIZE = 8e6;
  constexpr int SIMD_SIZE = 32;
  constexpr std::size_t TOTAL_SIZE = SIZE * SIMD_SIZE;
  constexpr int num_subdevices = NUM_SUBDEVICES;

  mptr<num_subdevices> device_ptr_a;
  mptr<num_subdevices> device_ptr_b;
  mptr<num_subdevices> device_ptr_c;

  const int default_device = omp_get_default_device();
  std::cout << "default_device = " << default_device << std::endl;

  for (int sdev = 0; sdev < num_subdevices; ++sdev) {
    device_ptr_a.p[sdev] =
      static_cast<float *>(malloc(TOTAL_SIZE * sizeof(float)));
    device_ptr_b.p[sdev] =
      static_cast<float *>(malloc(TOTAL_SIZE * sizeof(float)));
    device_ptr_c.p[sdev] =
      static_cast<float *>(malloc(TOTAL_SIZE * sizeof(float)));

#pragma omp target enter data map(
      alloc : device_ptr_a.p[sdev][0 : TOTAL_SIZE]) device(default_device)
      subdevice(DEVKIND, sdev)

#pragma omp target enter data map(
      alloc : device_ptr_b.p[sdev][0 : TOTAL_SIZE]) device(default_device)
      subdevice(DEVKIND, sdev)

#pragma omp target enter data map(
      alloc : device_ptr_c.p[sdev][0 : TOTAL_SIZE]) device(default_device)
      subdevice(DEVKIND, sdev)
  } // for (int sdev ...

  std::cout << "memory footprint per GPU = "
          << 3 * (std::size_t)(TOTAL_SIZE) * sizeof(float) * 1E-9 << " GB"
          << std::endl;

#pragma omp parallel for
  for (int sdev = 0; sdev < num_subdevices; ++sdev) {
    float *a = device_ptr_a.p[sdev];
    float *b = device_ptr_b.p[sdev];

#pragma omp target teams distribute parallel for device(default_device)
    subdevice(DEVKIND, sdev)
    for (size_t i = 0; i < TOTAL_SIZE; ++i) {
      a[i] = i + 0.5;
      b[i] = i - 0.5;
    }
  }

  const int no_max_rep = 200;
```

```cpp
double time = 0.0;
for (int irep = 0; irep < no_max_rep + 1; ++irep) {
    if (irep == 1)
        time = omp_get_wtime();

#pragma omp parallel for num_threads(num_subdevices)
    for (int sdev = 0; sdev < num_subdevices; ++sdev) {
        float *a = device_ptr_a.p[sdev];
        float *b = device_ptr_b.p[sdev];
        float *c = device_ptr_c.p[sdev];

#pragma omp target teams distribute parallel for device(default_device) \
    subdevice(DEVKIND, sdev)
        for (size_t i = 0; i < TOTAL_SIZE; ++i) {
            c[i] = a[i] + b[i];
        }
    }
}

time = omp_get_wtime() - time;
time = time / no_max_rep;

const std::size_t streamed_bytes =
    3 * (std::size_t)(TOTAL_SIZE)*num_subdevices * sizeof(float);
std::cout << "bandwidth = " << (streamed_bytes / time) * 1E-9 << " GB/s"
       << std::endl;
std::cout << "time = " << time << " s" << std::endl;
std::cout.precision(10);

for (int sdev = 0; sdev < num_subdevices; ++sdev) {
#pragma omp target update from(device_ptr_c.p[sdev][ : TOTAL_SIZE]) \
    device(default_device) subdevice(DEVKIND, sdev)
    std::cout << "-GPU: device id = : " << sdev << std::endl;
    std::cout << "target result:" << std::endl;
    std::cout << "c[" << 0 << "] = " << device_ptr_c.p[sdev][0] << std::endl;
    std::cout << "c[" << SIMD_SIZE - 1
           << "] = " << device_ptr_c.p[sdev][SIMD_SIZE - 1] << std::endl;
    std::cout << "c[" << TOTAL_SIZE / 2
           << "] = " << device_ptr_c.p[sdev][TOTAL_SIZE / 2] << std::endl;
    std::cout << "c[" << TOTAL_SIZE - 1
           << "] = " << device_ptr_c.p[sdev][TOTAL_SIZE - 1] << std::endl;
}

for (int sdev = 0; sdev < num_subdevices; ++sdev) {
    for (size_t i = 0; i < TOTAL_SIZE; ++i) {
        assert((int)(device_ptr_c.p[sdev][i]) ==
            (int)(device_ptr_c.p[sdev][i] +
                device_ptr_a.p[sdev][i] * device_ptr_b.p[sdev][i]));
    }
}

for (int sdev = 0; sdev < num_subdevices; ++sdev) {
#pragma omp target exit data map(
    release : device_ptr_a.p[sdev][ : TOTAL_SIZE]) device(default_device) \
    subdevice(DEVKIND, sdev)
#pragma omp target exit data map(
    release : device_ptr_b.p[sdev][ : TOTAL_SIZE]) device(default_device) \
    subdevice(DEVKIND, sdev)
```

```txt
#pragma omp target exit data map(
    release : device_ptr_a.p[sdev][ : TOTAL_SIZE]) device(default_device) \
    subdevice(DEVKIND, sdev)
}
}
```

Compilation command:

```shell
$ icpx -ffp-contract=fast -O2 -ffast-math -DNUM_SUBDEVICES=2 \
-fiopenmp -fopenmp-targets=spir64 openmp_explicit_subdevice.cpp
```

Run command:

```txt
$ ZE_FLAT_DEVICE_HIERARCHY=COMPOSITE OMP_TARGET_OFFLOAD=MANDATORY ./a.out
```

This OpenMP program achieves linear scaling \~2x on an Intel<sup>®</sup> Data Center GPU Max system.

## Explicit Scaling Summary

Performance tuning for a multi-stack GPU imposes a tedious process given the parallelism granularity is at a finer level. However, the fundamentals are similar to CPU performance tuning. To understand performance scaling dominators, one needs to pay attention to:

• VE utilization efficiency - how kernels utilize the execution resources of different stacks

• Data placement - how allocations are spread across the HBM of different stacks

• Thread-data affinity: where data “located” and how they are accessed in the system

In addition, there are several critical programming model concepts for application developers to keep in mind in order to select their favorite scaling scheme for productivity, portability and performance.

• Sub-devices (numa\_domains) and Sub-sub-devices (subnuma\_domains)

• Explicit and implicit scaling

• Contexts and queues

• Environment variables and program language APIs or constructs

## Implicit Scaling
