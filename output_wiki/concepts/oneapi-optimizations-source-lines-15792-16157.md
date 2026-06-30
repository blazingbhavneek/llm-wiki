# oneapi_optimizations Source Lines 15792-16157

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L15792-L16157

Citation: [oneapi_optimizations:L15792-L16157]

````text
## Notes:

• OMP\_TARGET\_OFFLOAD=MANDATORY is used to make sure that the target region will run on the GPU. The program will fail if a GPU is not found.

• There is no need to specify ZE\_FLAT\_DEVICE\_HIERARCHY=FLAT with the run command, since FLAT mode is the default.

Running on a system with a single GPU card (2 stacks in total):

sycl-ls shows that there are 2 devices (corresponding to the 2 stacks):

```txt
\$ sycl-ls
[level_zero:gpu][level_zero:0] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:1] ... Intel(R) Data Center GPU Max 1550 1.3
[opencl:gpu][opencl:0] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:1] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
```

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 2 devices (corresponding to the 2 stacks) have been found.

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 2 root devices, 2 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0
Target LEVEL_ZERO RTL --> -- 1
```

Running on a system with 4 GPU cards (8 stacks in total)

sycl-ls shows that there are 8 devices (corresponding to the 8 stacks):

```txt
\$ sycl-ls
[level_zero:gpu][level_zero:0] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:1] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:2] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:3] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:4] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:5] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:6] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:7] ... Intel(R) Data Center GPU Max 1550 1.3
[opencl:gpu][opencl:0] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:1] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:2] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:3] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:4] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:5] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:6] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:7] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
```

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 8 devices (corresponding to the 8 stacks) have been found:

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 8 root devices, 8 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0
Target LEVEL_ZERO RTL --> -- 1
Target LEVEL_ZERO RTL --> -- 2
Target LEVEL_ZERO RTL --> -- 3
Target LEVEL_ZERO RTL --> -- 4
Target LEVEL_ZERO RTL --> -- 5
Target LEVEL_ZERO RTL --> -- 6
Target LEVEL_ZERO RTL --> -- 7
```

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
````
