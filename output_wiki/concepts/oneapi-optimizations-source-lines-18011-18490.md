# oneapi_optimizations Source Lines 18011-18490

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L18011-L18490

Citation: [oneapi_optimizations:L18011-L18490]

````text
## Intra-Device and Inter-Device Data Transfers for MPI+OpenMP Programs

Some applications are just pure OpenMP programs where a single process uses all available GPU resources. But many other applications use a combination of MPI and OpenMP where multiple MPI ranks are used and each of these MPI ranks uses in turn OpenMP to access some of the GPU resources (either a full GPU or a GPU subdevice).

Typically, such applications will need at some point to exchange data between the GPU resources used by the different ranks. In order to do this, normally, first the data needs to be transferred from the GPU to the CPU that will do the MPI transfer, and once it is received by the target CPU, transferred again to the target GPU.

In principle, transferring data between subdevices of the same GPU should not require to transfer the data first back to the CPU. Also, for systems that use the Intel<sup>®</sup> X<sup>e</sup> Link which allows GPUs to exchange data directly this should not be necessary either.

Besides Intel<sup>®</sup> MPI Library, the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library supports direct transfers between GPUs and GPU subdevices to improve communication efficiency.

The MPI primitives of this library are able to determine whether a pointer points to data that is in the GPU even from the CPU and, therefore, it can activate a different communication path that transfers the data directly between the GPU devices or subdevices without the need of transferring the data through the CPUs.

With this in mind, after installing the library, in order to take advantage of it we need to use OpenMP APIs and directives to obtain device pointers that we can then use in the MPI calls to activate the direct GPU communication path. There are two possible scenarios for this:

1. Data was directly allocated on the device by means of omp\_target\_alloc.

When the data is allocated on the device using the omp\_target\_alloc routine (or a similar routine), the returned pointer is a device pointer that can be used directly in the MPI calls. For example:

double \*dst\_buff = omp\_target\_alloc(device\_id, 1000 \* sizeof(double)); MPI\_Recv(dst\_buff,...);

1. Data that was mapped on the device.

If the data was allocated on the device using a map clause or some of OpenMP implicit mapping rules, then we need to use the use\_device\_ptr or use\_device\_addr clauses of the target data directive to get a device pointer that we can use on the MPI calls. For example:

```txt
#pragma omp target data map(dst_buff)
{
    #pragma omp target data use_device_addr(dst_buff)
    {
        MPI_Recv(dst_buff,...)
    }
}
```

Now take a look at a more complex example which allows the user to select by means of a flag if device pointers (in case the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library is being used) or host pointers should be used in MPI calls. We will also use this code to showcase the performance difference that can be achieved by using device to device transfers. The code just keeps rotating some buffers across a number of MPI ranks while increasing their value.

We are going to control whether to use device to device transfers or regular MPI transfers by means of the mpi\_aware variable.

```c
int mpi_aware = 0;
if ( argc > 1 ) {
    mpi_aware = 1;
    printf("MPI device aware path enabled\n");
} // argc check
```

The application uses two buffers, buf1 and buf2, so we start by mapping them normally on the device by using a target data construct. Next we use a conditional target data construct to convert the addresses of buf1 and buf2 to device addresses only if mpi\_aware is true. So, if mpi\_aware is true, the curr and next pointers will hold device addresses. Otherwise, they will hold host addresses. This can be observed with the printf statement.

```c
#pragma omp target data map(buf1,buf2)
{
    #pragma omp target data use_device_addr(buf1,buf2) if(mpi_aware)
    {
        curr = buf1;
        next = buf2;
    }
    printf("curr=%p next=%p\n",curr,next);
```

If mpi\_aware is false, printf will print values similar to the following which are host addresses:

```txt
curr=0x7ffdffc11850 next=0x7ffdff470650
```

On the other hand, if mpi\_aware is true, printf will print values similar to the following which are device addresses:

```txt
curr=0xff00000000200000 next=0xff00000000a00000
```

Finally before and after the MPI communication calls we use two conditional target update constructs to update the GPU variables only if mpi\_aware was false as this is not needed if device to device transfers are used.

```c
if ( nranks > 1 ) {
    #pragma omp target update from(curr[0:N]) if(!mpi_aware)
    MPI_Request srq;
    MPI_Isend(curr,N,MPI_DOUBLE,next_rank,0,MPI_COMM_WORLD,&srq);
// we need to make sure that the MPI_Isend of the previous
// iteration finished before doing the MPI_Recv of this
// iteration
if ( step > 0 ) MPI_Wait(&psrq,MPI_STATUS_IGNORE);
psrq = srq;
    MPI_Recv(next,N,MPI_DOUBLE,prev_rank,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
    #pragma omp target update to(next[0:N]) if(!mpi_aware)
} // nranks
```

We, first, use this program to evaluate the performance difference in a system with a single GPU which is divided in two subdevices, one for each MPI rank. We can see a significant time difference that is a direct consequence of the reduction of the number of memory operations from the host to the device (M2D operations) and vice versa (D2M operations) which can be obtained with the unitrace tool.

2 MPI ranks

<table><tr><td>Version</td><td>Time (s.)</td><td>M2D operations (per rank)</td><td>D2M operations (per rank)</td></tr><tr><td>mpi_aware = 0</td><td>3.07</td><td>1002</td><td>1002</td></tr><tr><td>mpi_aware = 1</td><td>0.13</td><td>2</td><td>2</td></tr></table>

We can now use the same program to evaluate the performance difference in a system with two GPU devices connected with Intel<sup>®</sup> X<sup>e</sup> Link. In this case, there will be 4 MPI ranks as each GPU will be programmed as two subdevices. We can observe a similar reduction in time and number of memory operations between the host and the device as in the previous case.

4 MPI ranks

<table><tr><td>Version</td><td>Time (s.)</td><td>M2D operations (per rank)</td><td>D2M operations (per rank)</td></tr><tr><td>mpi_aware = 0</td><td>3.45</td><td>1002</td><td>1002</td></tr><tr><td>mpi_aware = 1</td><td>0.44</td><td>2</td><td>2</td></tr></table>

As we have seen a significant improvement in the communication efficiency between GPUs can be achieved when these are connected with the Intel<sup>®</sup> X<sup>e</sup> Link and the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library is used.

Note: Using the mpi\_aware path with an MPI library that does not support device-to-device transfers may result in an abnormal termination of the program.

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
````
