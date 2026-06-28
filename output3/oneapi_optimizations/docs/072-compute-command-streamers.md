## Advanced Topics

## Compute Command Streamers (CCSs)

Each stack of the Intel<sup>®</sup> Data Center GPU Max contains 4 Compute Command Streamers (CCSs), which can be used to access a pool of Execution Units (EUs).

Hardware allows for the selection of a specific distribution of EUs among the CCSs. The EUs in a stack may be assigned to a single CCS, 2 CCSs, or 4 CCSs in the stack.

• 1-CCS mode (Default): In this mode, 1 CCS in each stack is exposed. The CCS has access to all the EUs in the stack. Other CCSs are disabled.

• 2-CCS mode: In this mode, 2 CCSs in each stack are exposed, each having half of the EUs in the stack assigned to it. If the EUs of one of the CCSs are idle, those EUs cannot be used by the other CCSs.

• 4-CCS mode: In this mode, all 4 CCSs of the stack are exposed, each having a quarter of the EUs in the stack assigned to it. As with the 2-CCS mode, EUs of idle CCSs cannot be used by other CCSs.

The default is 1-CCS mode.

Some applications may benefit from using 1 CCS per stack to access all the EUs in the stack, while other applications may benefit from using 2 or 4 CCSs per stack where a subset of the EUs are assigned to each CCS.

Using 2 or 4 CCSs per stack may be useful when running multiple small kernels concurrently on a stack, and the computations by each of these kernels does not require all the compute resources (EUs) of the stack. In this case, it may be advantageous to submit different kernels to different CCSs in the stack, thus allowing the kernels to run in parallel.

The environment variable ZEX\_NUMBER\_OF\_CCS can be used to specify how many CCSs are exposed in each of the stacks in a GPU card.

The format for ZEX\_NUMBER\_OF\_CCS is a comma-separated list of device-mode pairs, i.e., ZEX\_NUMBER\_OF\_CCS=<Root Device Index>:<CCS Mode>,<Root Device Index>:<CCS Mode>… For instance, in a GPU card with 2 stacks, one would specify the following to set stack 0 in 4-CCS mode, and stack 1 in 1-CCS mode.

```txt
ZEX_NUMBER_OF_CCS=0:4,1:1
```

Below we show examples of exposing CCSs in SYCL, OpenMP and MPI applications.

Using Multiple CCSs in SYCL

In SYCL, one can create a context associated with a CCS (subsubdevice), giving the program fine-grained control at the CCS level. The following example finds all stacks (subdevices) and CCSs (subsubdevices) on a GPU card (device):

```cpp
#include <cstdlib>
#include <iostream>
#include <sycl/sycl.hpp>

int main() {
  // Find all GPU devices
  auto devices = sycl::platform(sycl::gpu_selector_v).get_devices();
  for (size_t n = 0; n < devices.size(); n++) {
    std::cout << "\nGPU" << n << ": "
           << devices[n].get_info<sycl::info::device::name>() << " ("
           << devices[n].get_info<sycl::info::device::max_compute_units>()
           << ")\n";
    std::vector<sycl::device> subdevices;
    std::vector<sycl::device> subsubdevices;
    auto part_prop =
      devices[n].get_info<sycl::info::device::partition_properties>();
    if (part_prop.empty()) {
      std::cout << "No partition_properties\n";
    } else {
      for (size_t i = 0; i < part_prop.size(); i++) {
        // Check if device can be partitioned into Tiles
        if (part_prop[i] ==
          sycl::info::partition_property::partition_by_affinity_domain) {
          auto sub_devices =
            devices[n]
                .create_sub_devices<sycl::info::partition_property::
                    partition_by_affinity_domain>(
                        sycl::info::partition_affinity_domain::numa);
          for (size_t j = 0; j < sub_devices.size(); j++) {
            subdevices.push_back(sub_devices[j]);
            std::cout << "\ntile" << j << ": "
                   << subdevices[j].get_info<sycl::info::device::name>()
                   << " ("
                   << subdevices[j]
                   .get_info<sycl::info::device::max_compute_units>()
                   << ")\n";
            auto part_prop1 =
                subdevices[j]
                .get_info<sycl::info::device::partition_properties>();
            if (part_prop1.empty()) {
                std::cout << "No partition_properties\n";
            } else {
                for (size_t i = 0; i < part_prop1.size(); i++) {
                    // Check if Tile can be partitioned into Slices (CCS)
                    if (part_prop1[i] == sycl::info::partition_property::
                            ext_intel_partition_by_cslice) {
                        auto sub_devices =
                            subdevices[j]
                            .create_sub_devices<
                                sycl::info::partition_property::
                                ext_intel_partition_by_cslice>();
                        for (size_t k = 0; k < sub_devices.size(); k++) {
                            subsubdevices.push_back(sub_devices[k]);
                            std::cout
                                << "slice" << k << ": "
```

```cpp
<< subsubdevices[k].get_info<sycl::info::device::name>()
<< " ( "
<< subsubdevices[k]
            .get_info<
                sycl::info::device::max_compute_units>()
<< ")\n";
}
break;
} else {
std::cout << "No ext_intel_partition_by_cslice\n";
}
}
}
break;
// Check if device can be partitioned into Slices (CCS)
} else if (part_prop[i] == sycl::info::partition_property::
                    ext_intel_partition_by_cslice) {
auto sub_devices =
    devices[n]
        .create_sub_devices<sycl::info::partition_property::
                    ext_intel_partition_by_cslice>();
for (size_t k = 0; k < sub_devices.size(); k++) {
subsubdevices.push_back(sub_devices[k]);
std::cout << "slice" << k << ": "
          << subsubdevices[k].get_info<sycl::info::device::name>()
          << " ( "
          << subsubdevices[k]
                .get_info<sycl::info::device::max_compute_units>()
          << ")\n";
}
break;
} else {
std::cout << "No ext_intel_partition_by_cslice or "
                   "partition_by_affinity_domain\n";
}
}
}
}
return 0;
}
```

The SYCL code below demonstrates how multiple kernels can be submitted to multiple CCSs to execute concurrently.

The example code finds all CCSs, creates sycl::queue for each CCS found on GPU device and submits kernels to all CCSs using a for-loop.

```cpp
#include <sycl/sycl.hpp>

static constexpr size_t N = 5280; // global size
static constexpr size_t B = 32;   // WG size

void kernel_compute_mm(sycl::queue &q, float *a, float *b, float *c, size_t n,
                    size_t wg) {
    q.parallel_for(
        sycl::nd_range<2>(sycl::range<2>{n, n}, sycl::range<2>{wg, wg}),
        [=](sycl::nd_item<2> item) {
            const int i = item.get_global_id(0);
```

```cpp
const int j = item.get_global_id(1);
float temp = 0.0f;
for (int k = 0; k < N; k++) {
    temp += a[i * N + k] * b[k * N + j];
}
c[i * N + j] = temp;
});
}

int main() {
    auto start =
        std::chrono::high_resolution_clock::now().time_since_epoch().count();

    // find all CCS / Tiles in GPU
    auto device = sycl::device(sycl::gpu_selector_v);
    std::cout << "\nGPU: " << device.get_info<sycl::info::device::name>() << " ("
            << device.get_info<sycl::info::device::max_compute_units>()
            << ")\n";
    std::vector<sycl::device> subdevices;
    std::vector<sycl::device> subsubdevices;
    auto part_prop = device.get_info<sycl::info::device::partition_properties>();
    if (part_prop.empty()) {
        std::cout << "No partition_properties\n";
    } else {
        for (int i = 0; i < part_prop.size(); i++) {
            // Check if device can be partitioned into Tiles
            if (part_prop[i] ==
                sycl::info::partition_property::partition_by_affinity_domain) {
                auto sub_devices = device.create_sub_devices<
                    sycl::info::partition_property::partition_by_affinity_domain>(
                    sycl::info::partition_affinity_domain::numa);
                for (int j = 0; j < sub_devices.size(); j++) {
                    subdevices.push_back(sub_devices[j]);
                    std::cout
                        << "\nTile" << j << ": "
                        << subdevices[j].get_info<sycl::info::device::name>() << " ("
                        << subdevices[j].get_info<sycl::info::device::max_compute_units>()
                        << ")\n";
                    auto part_prop1 =
                        subdevices[j]
                            .get_info<sycl::info::device::partition_properties>();
                    if (part_prop1.empty()) {
                        std::cout << "No partition_properties\n";
                    } else {
                        for (int i = 0; i < part_prop1.size(); i++) {
                            // Check if Tile can be partitioned into Slices (CCS)
                            if (part_prop1[i] == sycl::info::partition_property::
                                ext_intel_partition_by_cslice) {
                                auto sub_devices = subdevices[j]
                                .create_sub_devices<
                                    sycl::info::partition_property::
                                    ext_intel_partition_by_cslice>();
                                for (int k = 0; k < sub_devices.size(); k++) {
                                    subsubdevices.push_back(sub_devices[k]);
                                    std::cout
                                    << "Slice" << k << ": "
                                    << subsubdevices[k].get_info<sycl::info::device::name>() "
                                    << " ("
```

```cpp
<< subsubdevices[k]
            .get_info<sycl::info::device::max_compute_units>()
        << "\n";
    }
    break;
} else {
    std::cout << "No ext_intel_partition_by_cslice\n";
}
}
}
break;
// Check if device can be partitioned into Slices (CCS)
} else if (part_prop[i] == sycl::info::partition_property::
                    ext_intel_partition_by_cslice) {
    auto sub_devices = device.create_sub_devices<
        sycl::info::partition_property::ext_intel_partition_by_cslice>();
    for (int k = 0; k < sub_devices.size(); k++) {
        subsubdevices.push_back(sub_devices[k]);
        std::cout << "Slice" << k << ": "
                << subsubdevices[k].get_info<sycl::info::device::name>()
                << " ("
                << subsubdevices[k]
                    .get_info<sycl::info::device::max_compute_units>()
                << "\n";
    }
    break;
} else {
    std::cout << "No ext_intel_partition_by_cslice or "
                    "partition_by_affinity_domain\n";
}
}
}

// Set devices to submit compute kernel
std::vector<sycl::device> devices(1, device);
if (subsubdevices.size())
    devices = subsubdevices;
else if (subdevices.size())
    devices = subdevices;
auto num_devices = devices.size();

// Define matrices
float *matrix_a[num_devices];
float *matrix_b[num_devices];
float *matrix_c[num_devices];

float v1 = 2.f;
float v2 = 3.f;
for (int n = 0; n < num_devices; n++) {
    matrix_a[n] = static_cast<float *>(malloc(N * N * sizeof(float)));
    matrix_b[n] = static_cast<float *>(malloc(N * N * sizeof(float)));
    matrix_c[n] = static_cast<float *>(malloc(N * N * sizeof(float)));

    // Initialize matrices with values
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
        matrix_a[n][i * N + j] = v1++;
```

```cpp
matrix_b[n][i * N + j] = v2++;
 matrix_c[n][i * N + j] = 0.f;
 }
}

float *da[num_devices];
float *db[num_devices];
float *dc[num_devices];

std::vector<sycl::queue> q(num_devices);

// create queues for each device
std::cout << "\nSubmitting Compute Kernel to Devices:\n";
for (int i = 0; i < num_devices; i++) {
    q[i] = sycl::queue(devices[i]);
    std::cout
        << "Device" << i << ": "
        << q[i].get_device().get_info<sycl::info::device::name>() << " ("
        << q[i].get_device().get_info<sycl::info::device::max_compute_units>()
        << ")\n";
}

// device mem alloc for matrix a,b,c for each device
for (int i = 0; i < num_devices; i++) {
    da[i] = sycl::malloc_device<float>(N * N, q[i]);
    db[i] = sycl::malloc_device<float>(N * N, q[i]);
    dc[i] = sycl::malloc_device<float>(N * N, q[i]);
}

// warm up: kernel submit with zero size
for (int i = 0; i < num_devices; i++)
    kernel_compute_mm(q[i], da[i], db[i], dc[i], 0, 0);

// kernel sync
for (int i = 0; i < num_devices; i++)
    q[i].wait();

// memcpy for matrix and b to device alloc
for (int i = 0; i < num_devices; i++) {
    q[i].memcpy(&da[i][0], &matrix_a[i][0], N * N * sizeof(float));
    q[i].memcpy(&db[i][0], &matrix_b[i][0], N * N * sizeof(float));
}

// wait for copy to complete
for (int i = 0; i < num_devices; i++)
    q[i].wait();

// submit matrix multiply kernels to all devices
for (int i = 0; i < num_devices; i++)
    kernel_compute_mm(q[i], da[i], db[i], dc[i], N, B);

// wait for compute complete
for (int i = 0; i < num_devices; i++)
    q[i].wait();

// copy back result to host
for (int i = 0; i < num_devices; i++)
    q[i].memcpy(&matrix_c[i][0], &dc[i][0], N * N * sizeof(float));
```

```shell
$ export ONEAPI_DEVICE_SELECTOR="*:*.*.*"
or
$ LIBOMPTARGET_DEVICES=SUBSUBDEVICE
```

```cpp
// wait for copy to complete
for (int i = 0; i < num_devices; i++)
    q[i].wait();

// print first element of result matrix
std::cout << "\nMatrix Multiplication Complete\n";
for (int i = 0; i < num_devices; i++)
    std::cout << "device" << i << ": matrix_c[0][0]=" << matrix_c[i][0] << "\n";

for (int i = 0; i < num_devices; i++) {
    free(matrix_a[i]);
    free(matrix_b[i]);
    free(matrix_c[i]);
    sycl::free(da[i], q[i]);
    sycl::free(db[i], q[i]);
    sycl::free(dc[i], q[i]);
}

auto duration =
    std::chrono::high_resolution_clock::now().time_since_epoch().count() -
    start;
std::cout << "Compute Duration: " << duration / 1e+9 << " seconds\n";
return 0;
```

To build the examples, run:

```shell
$ icpx -fsycl -o ccs ccs.cpp
$ icpx -fsycl -o ccs_matrixmul ccs_matrixmul.cpp
```

The number of CCSs found in ccs and the number of kernels executing in parallel in ccs\_matrixmul depend on the setting of the environment variable ZEX\_NUMBER\_OF\_CCS.

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
