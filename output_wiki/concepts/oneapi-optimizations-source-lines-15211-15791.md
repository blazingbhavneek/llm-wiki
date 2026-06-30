# oneapi_optimizations Source Lines 15211-15791

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L15211-L15791

Citation: [oneapi_optimizations:L15211-L15791]

````text
## Multi-GPU and Multi-Stack Architecture and Programming

Intel<sup>®</sup> Data Center GPU Max Series uses a multi-stack GPU architecture, where each GPU contains 1 or 2 stacks. The GPU architecture and products enable multi-GPU and multi-stack computing.

In this chapter, we introduce the following topics:

• Multi-Stack GPU Architecture

• Exposing the Device Hierarchy

• FLAT Mode Programming

• COMPOSITE Mode Programming

• Using Intel® oneAPI Math Kernel Library (oneMKL)

• Using Intel® MPI Library

• Advanced Topics

• Terminology

## Multi-Stack GPU Architecture

Intel<sup>®</sup> Data Center GPU Max Series use a multi-stack GPU architecture with 1 or 2 stacks.

![](images/abe0fd92d9339ac301b20c5428f93457bdee00f026f308b1a65124068f2614c3.jpg)  
Intel® Iris® Xe GPU Multi-Stack Architecture

![](images/464b2415fe159d5ba1b1c5819603388ac1fabea5f72dc57af8edf10ac33b6666.jpg)

The above figure illustrates 1-stack and 2-stack Intel<sup>®</sup> Data Center GPU Max Series products, each with its own dedicated resources:

Vector Engines (VEs) Computation units belong to the stack

<sub>High</sub> <sub>Bandwidth</sub> <sub>Memory</sub> HBM directly connected to the stack (HBM)

Level 2 Cache (L2) Level 2 cache belonging to the stack

For general applications, the most common mode is to use each stack as a device (see next section, Exposing the Device Hierarchy). Intel GPU driver, as well as SYCL and OpenMP parallel language runtimes work together to dispatch kernels to the stack(s) in the GPU.

Stacks are connected with fast interconnect that allows efficient communication between stacks. The following operations are possible:

Any stack is capable of For example, stack 0 may read the local HBM memory of stack 1. In this case, reading and writing to any the interconnect between stack 0 and stack 1 is used for communication. HBM memory in the same GPU card.

Each stack is an The stack can execute workloads on its own. independent entity

Because access to a stack’s local HBM does not involve inter-stack interconnect, it is more efficient than cross-stack HBM access, with lower latency and lower inter-stack bandwidth consumption. Advanced developers can take advantage of memory locality to achieve higher performance.

The default for each stack is to use a single Compute Command Streamer (CCS) that includes all the hardware computing resources on that stack. Most applications will work well in this mode.

It is also possible to statically partition each stack, via the environment variable ZEX\_NUMBER\_OF\_CCS, into a 2-CCS mode or 4-CCS mode configuration, and treat each CCS as an entity to which kernels can be offloaded. For more information, refer to Advanced Topics.

## GPU Memory System

The memory for a general-purpose engine is partitioned into host-side memory and device-side memory as shown in the following figure, using Unified Shared Memory (USM) to move objects between the two sides. Each address hashes to a unique bank. Approximate uniform distribution for sequential, strided, and random addresses.

• Full bandwidth when same number of banks as X<sup>e</sup>-cores (reduced by queuing congestion, hot-spotting, bank congestion).

• TLB misses on virtual address translation increase memory latency. May trigger more memory accesses and cache evictions.

• High miss rate on GPU cache may decrease GPU Memory controller efficiency when presented with highly distributed accesses.

• Compression unit compresses adjacent cache lines. Also supports read/write of fast-clear surfaces. Improves bandwidth but also adds latency.

GPU Memory System  
![](images/3ac04747d9af323eeb03c8fe5359c8611274913f1352395891c05b060af79560.jpg)

## GPU Memory accesses measured at VE:

• Sustained fabric bandwidth \~90% of peak

• GPU cache hit \~150 cycles, cache miss \~300 cycles. TLB miss adds 50-150 cycles

• GPU cache line read after write to same cache line adds \~30 cycles

Stacks accessing device memory on a different stack utilize a new GAM-to-GAM High bandwidth interface (“GT Link”) between stacks. The bandwidth of this interface closely matches the memory bandwidth that can be handled by the device memory sub-system of any single stack.

## Loads/Stores/Atomics in VE Threads

VE threads make memory accesses by sending messages to a data-port, the load instruction sends address and receives data, The store instructions send address and data. All VE in X<sup>e</sup>-core share one Memory Load/ Store data-port as shown in the figure below.

• Inside X<sup>e</sup>-core: \~128-256 Bytes per cycle

• Outside X<sup>e</sup>-core: \~64 Bytes per cycle

• Read bandwidth sometimes higher than write bandwidth

## VE thread and Memory Access

![](images/c84ff91ea1b7ddb14c4fec71db41033d2a9571e173cff5fb409a79887709e57c.jpg)

A new memory access can be started every cycle, typical 32b SIMD16 SEND operations complete in 6 cycles plus their memory latency (4-element vectors complete in 12 cycles plus memory latency), and Independent addresses are merged to minimize memory bandwidth. Keep it mind on memory latencies:

Memory latency table

<table><tr><td>Access type</td><td>Latency</td></tr><tr><td>Shared local memory</td><td>~30 cycles</td></tr><tr><td>Xe-core data cache hit</td><td>~50 cycles</td></tr><tr><td>GPU cache hit</td><td>~150 - ~200 cycles</td></tr><tr><td>GPU cache miss</td><td>~300 - ~500 cycles</td></tr></table>

All Loads/Stores are relaxed ordering (ISO C11 memory model; Read and Write) are in-order for the same address from the same thread. Different addresses in the same thread may complete out-of-order, Read/ Write ordering is not maintained between threads nor VEs nor X<sup>e</sup>-cores, so code needs to use atomic and/or fence operations to guarantee additional ordering.

An atomic operation may involve both reading from and then writing to a memory location. Atomic operations apply only to either unordered access views or thread-group shared memory. It is guaranteed that when a thread issues an atomic operation on a memory address, no write to the same address from outside the current atomic operation by any thread can occur between the atomic read and write.

If multiple atomic operations from different threads target the same address, the operations are serialized in an undefined order. This serialization occurs due to L2 serialization rules to the same address. Atomic operations do not imply a memory or thread fence. If the program author/compiler does not make appropriate use of fences, it is not guaranteed that all threads see the result of any given memory operation at the same time, or in any particular order with respect to updates to other memory addresses. However, atomic operations are always stated on a global level (except on shared local memory), and when the atomic operation is complete the final result is always visible to all thread groups. Each generation since Gen7 has increased the capability and performance of atomic operations.

The following SYCL code example performs 1024 same address atomic operations per work item. Each work item use a different (unique) address, compiler generates SIMD32 kernel for each VE thread, which will perform 2 SIMD16 atomic operations on 2 cache-lines, and compiler unrolls loop \~8 times to reduce register dependency stalls as well.

```cpp
#include <sycl/sycl.hpp>
#include <chrono>
#include <iostream>
#include <string>
#include <unistd.h>
#include <vector>

#ifndef SCALE
#define SCALE 1
#endif

#define N      1024*SCALE
#define SG_SIZE 32

constexpr int warm_up_token = -1;

static auto exception_handler = [](sycl::exception_list eList) {
    for (std::exception_ptr const &e : eList) {
        try {
            std::rethrow_exception(e);
        } catch (std::exception const &e) {
            std::cout << "Failure" << std::endl;
            std::terminate();
        }
    }
};

class Timer {
public:
    Timer() : start_(std::chrono::steady_clock::now()) {}

    double Elapsed() {
        auto now = std::chrono::steady_clock::now();
        return std::chrono::duration_cast<Duration>(now - start_).count();
    }

private:
    using Duration = std::chrono::duration<double>;
    std::chrono::steady_clock::time_point start_;
};

#ifdef FLUSH_CACHE
void flush_cache(sycl::queue &q, sycl::buffer<int> &flush_buf) {
    auto flush_size = flush_buf.get_size()/sizeof(int);
    auto ev = q.submit([&](auto &h) {
```

```cpp
sycl::accessor flush_acc(flush_buf, h, sycl::write_only, sycl::noinit);
h.parallel_for(flush_size, [=](auto index) { flush_acc[index] = 1; });
});
ev.wait_and_throw();
}
#endif

void atomicLatencyTest(sycl::queue &q, sycl::buffer<int> inbuf,
            sycl::buffer<int>, int &res, int iter) {
sycl::buffer<int> sum_buf(&res, 1);

double elapsed = 0;

for (int k = warm_up_token; k < iter; k++) {
#ifdef FLUSH_CACHE
    flush_cache(q, flush_buf);
#endif

    Timer timer;

    q.submit([&](auto &h) {
        sycl::accessor buf_acc(inbuf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(sycl::nd_range<1>(sycl::range<>{N}, sycl::range<>{SG_SIZE}), [=]
(sycl::nd_item<1> item)
            [[intel::reqd_sub_group_size(SG_SIZE)]] {
        int i = item.get_global_id(0);
        for (int ii = 0; ii < 1024; ++ii) {
        auto v =
            #ifdef ATOMIC_RELAXED
            sycl::atomic_ref<int, sycl::memory_order::relaxed,
                    sycl::memory_scope::device,
                    sycl::access::address_space::global_space>(buf_acc[i]);
        #else
            sycl::atomic_ref<int, sycl::memory_order::acq_rel,
                    sycl::memory_scope::device,
                    sycl::access::address_space::global_space>(buf_acc[i]);
        #endif
        v.fetch_add(1);
    }
});
});
q.wait();
elapsed += (iter == warm_up_token) ? 0 : timer.Elapsed();
}
std::cout << "SUCCESS: Time atomicLatency = " << elapsed << "s" << std::endl;
}

int main(void) {
sycl::queue q{sycl::gpu_selector_v, exception_handler};
std::cout << q.get_device().get_info<sycl::info::device::name>() << std::endl;

std::vector<int> data(N);
std::vector<int> extra(N);

for (size_t i = 0; i < N ; ++i) {
    data[i] = 1;
    extra[i] = 1;
```

```cpp
}
int res=0;

const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
sycl::buffer<int> buf(data.data(), data.size(), props);
sycl::buffer<int> flush_buf(extra.data(), extra.size(), props);
atomicLatencyTest(q, buf, flush_buf, res, 16);
}
```

In real workloads with atomics, users need to understand memory access behaviors and data set sizes when selecting an atomic operation to achieve optimal bandwidth.

## Exposing the Device Hierarchy

A multi-stack GPU card can be exposed as a single root device, or each stack can be exposed as a root device. This can be controlled via the environment variable ZE\_FLAT\_DEVICE\_HIERARCHY. The allowed values for ZE\_FLAT\_DEVICE\_HIERARCHY are FLAT, COMPOSITE, or COMBINED.

Our focus in this Guide is on FLAT and COMPOSITE modes.

Note that, in a system with one stack per GPU card, FLAT and COMPOSITE are the same.

## ZE\_FLAT\_DEVICE\_HIERARCHY=FLAT (Default)

The FLAT mode is the default mode if ZE\_FLAT\_DEVICE\_HIERARCHY is not set. In FLAT mode, each stack is exposed as a root device. The recommendation is to use FLAT mode. The FLAT mode performs well for most applications.

In FLAT mode, the driver and language runtime provide tools that expose each stack as a root device that can be programmed independently of all the other stacks.

In FLAT mode, offloading is done using explicit scaling.

On a single or multiple GPU card system, the user can use all the stacks in all the GPU cards in FLAT mode, and offload to all the stacks (devices) simultaneously.

In OpenMP, the device clause on the target construct can be used to specify to which stack (device) the kernel should be offloaded.

In SYCL, platform::get\_devices() can be called to get the stacks (devices) exposed.

For more information about the FLAT mode, refer to the FLAT Mode Programming section.

## ZE\_FLAT\_DEVICE\_HIERARCHY=COMPOSITE

In COMPOSITE mode, each GPU card is exposed as a root device. If the card contains more than one stack, then the stacks on the GPU card are exposed as subdevices.

In COMPOSITE mode, offloading can be done using either explicit or implicit scaling.

Note that in earlier GPU drivers, the default was COMPOSITE mode and implicit scaling. Now the default is FLAT mode.

## Explicit Scaling in COMPOSITE Mode:

In COMPOSITE mode, the driver and language runtime provide tools that expose each GPU card as a root device and the stacks as subdevices that can be programmed independently.

In OpenMP, the device and subdevice clauses on the target construct can be used to specify to which stack (subdevice) the kernel should be offloaded. (Note that the subdevice clause is an Intel extension to OpenMP.)

In SYCL, the device::create\_sub\_devices() can be called to get the subdevices or the stacks on each card device.

For more information about explicit scaling in COMPOSITE mode, refer to the Explicit Scaling section.

## Implicit Scaling in COMPOSITE Mode:

In COMPOSITE mode, if the program offloads to a device that is the entire card, then the driver and language runtime are, by default, responsible for work distribution and multi-stack memory placement.

The recommendation is to use explicit scaling. However, if the memory requirement is more than what is available in a single stack, then implicit scaling may be used.

For more information about implicit scaling in COMPOSITE mode, refer to the Implicit Scaling section.

## MPI Considerations

In an MPI application, each MPI rank may be configured to run on a GPU card or a GPU stack. Each rank can use OpenMP and SYCL to use the assigned GPU cards or stacks.

The table below shows common device configurations for MPI + OpenMP applications.

Configurations for MPI + OpenMP (N Cards with 2 Stacks Each)

<table><tr><td>FLAT or COMPOSITE</td><td>Device Exposed</td><td>MPI Rank Assignment</td><td>OpenMP Devices(s) View</td><td>Implicit Scaling?</td><td>Recommended?</td></tr><tr><td>FLAT</td><td>Stack</td><td>1 rank per stack, 2*N ranks in total</td><td>1 stack as device0</td><td>No</td><td>Yes</td></tr><tr><td>COMPOSITE</td><td>Card</td><td>1 rank per stack, 2*N ranks in total</td><td>1 stack as device0</td><td>No</td><td>For expert users</td></tr><tr><td>COMPOSITE</td><td>Card</td><td>1 rank per card, N ranks in total</td><td>2 stacks as device0 and device1</td><td>No</td><td>Yes</td></tr><tr><td>COMPOSITE</td><td>Card</td><td>1 rank per card, N ranks in total</td><td>1 card as device0</td><td>Yes</td><td>If single stack memory is not sufficient</td></tr></table>

## Obtaining System and Debugging Information

The following two schemes can be used to obtain information about the system and devices.

• Before you run an application, it is recommended that you run the sycl-ls command on the command line to find out which devices are available on the platform. This information is especially useful when doing performance measurements.

Note that sycl-ls shows devices seen or managed by all backends. For example, running on a system with a single GPU card with 2 stacks in total, sycl-ls shows that there are 2 devices (corresponding to the 2 stacks) managed by either the Level Zero or OpenCL backend.

```txt
\$ sycl-ls
[level_zero:gpu][level_zero:0] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:1] ... Intel(R) Data Center GPU Max 1550 1.3
[opencl:gpu][opencl:0] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:1] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
```

• Set the environment variable LIBOMPTARGET\_DEBUG to 1 so the runtime would display debugging information, including information about which devices were found and used. Note that LIBOMPTARGET\_DEBUG is OpenMP-specific (it does not apply to SYCL). See example in the FLAT Mode Example - OpenMP section.

## Environment Variables to Control Device Exposure

The following environment variables can be used to control the hardware or devices that are exposed to the application.

• ZE\_FLAT\_DEVICE\_HIERARCHY=FLAT or COMPOSITE (default is FLAT). See Device Hierarchy in Level Zero Specification Documentation.

• ONEAPI\_DEVICE\_SELECTOR. This environment variable is OpenMP-specific (does not apply in SYCL). The environment variable controls what hardware is exposed to the application. For details, see ONEAPI\_DEVICE\_SELECTOR in \_oneAPI DPC++ Compiler documentation.

• ZE\_AFFINITY\_MASK. This environment variable control what hardware is exposed by the Level-Zero User-Mode Driver (UMD). For details, see Affinity Mask in Level Zero Specification Documentation.

• LIBOMPTARGET\_DEVICES=DEVICE or SUBDEVICE or SUBSUBDEVICE. This environment variable is OpenMP-specific (does not apply in SYCL). It can be used to map an OpenMP “device” to a GPU card (device), a stack (subdevice), or a Compute Command Streamer (subsubdevice). See Compiling and Running an OpenMP Application in oneAPI GPU Optimization Guide.

• ZEX\_NUMBER\_OF\_CCS. See example in the Advanced Topics section.

## References

1. Device Hierarchy in Level Zero Specification Documentation

2. Affinity Mask in Level Zero Specification Documentation

3. ONEAPI\_DEVICE\_SELECTOR in \_oneAPI DPC++ Compiler documentation

4. Compiling and Running an OpenMP Application in oneAPI GPU Optimization Guide

## FLAT Mode Programming

As mentioned previously, the FLAT mode is the default mode on Intel<sup>®</sup> Data Center GPU Max Series. In FLAT mode, each stack is exposed as a root device. In this section, we present SYCL and OpenMP examples to demonstrate offloading in FLAT mode.

## Memory in FLAT Mode

Each stack has its own memory. A kernel offloaded to a stack will run on that stack and use the memory allocated on that stack.

A kernel running on a stack can access memory on other stacks in the same GPU card. However, accessing memory on a stack other than the stack it is running on will be slower.

• FLAT Mode Example - SYCL

• FLAT Mode Example - OpenMP

## FLAT Mode Example - SYCL

In this section, we use a simple vector addition example to show how to scale the performance using multiple devices in FLAT mode.

## Offloading to a single device (stack)

A first look at adding 2 vectors using one device or stack:

```txt
float *da;
    float *db;
    float *dc;
```

```cpp
da = (float *)sycl::malloc_device<float>(gsize, q);
db = (float *)sycl::malloc_device<float>(gsize, q);
dc = (float *)sycl::malloc_device<float>(gsize, q);
q.memcpy(da, ha, gsize);
q.memcpy(db, hb, gsize);

q.wait();

std::cout << "Offloading work to 1 device" << std::endl;

for (int i = 0; i < 16; i ++) {
    q.parallel_for(sycl::nd_range<1>(gsize, 1024),[=](auto idx) {
        int ind = idx.get_global_id();
        dc[ind] = da[ind] + db[ind];
    });
}

q.wait();

std::cout << "Offloaded work completed" << std::endl;

q.memcpy(hc, dc, gsize);
```

The above example adds two float vectors ha and hb and then saves the result in vector hc\`.

The example first allocates device memory for the 3 vectors, then copies the data from the host to the device before launching the kernels on the device to do vector addition. After the computation on the device completes, the result in vector dc on the device is copied to the vector hc on the host.

## Compilation and run commands:

```shell
$ icpx -fsycl flat_sycl_vec_add_single_device.cpp -o flat_sycl_vec_add_single_device
$ ./flat_sycl_vec_add_single_device
```

## Offloading to multiple devices (stacks)

We can scale up the performance of the above example if multiple devices are available.

The following example starts with enumerating all devices on the platform to make sure that at least 2 devices are available.

```cpp
auto plat = sycl::platform(sycl::gpu_selector_v);
auto devs = plat.get_devices();
auto ctxt = sycl::context(devs);

if (devs.size() < 2) {
    std::cerr << "No 2 GPU devices found" << std::endl;
    return -1;
}

std::cout << devs.size() << " GPU devices are found and 2 will be used" << std::endl;
sycl::queue q[2];
q[0] = sycl::queue(ctxt, devs[0], {sycl::property::queue::in_order()});
q[1] = sycl::queue(ctxt, devs[1], {sycl::property::queue::in_order()});
```

Next, the example allocates the vectors ha and hb on the host and partitions each vector into 2 parts. Then the first halves of the vectors ha and hb are copied to the first device, and the second halves are copied to the second device.

```lisp
constexpr size_t gsize = 1024 * 1024 * 1024L;
float *ha = (float *)(malloc(gsize * sizeof(float)));
float *hb = (float *)(malloc(gsize * sizeof(float)));
```

```c
float *hc = (float *)(malloc(gsize * sizeof(float)));

for (size_t i = 0; i < gsize; i++) {
    ha[i] = float(i);
    hb[i] = float(i + gsize);
}

float *da[2];
float *db[2];
float *dc[2];

size_t lsize = gsize / 2;

da[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
db[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
dc[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
q[0].memcpy(da[0], ha, lsize);
q[0].memcpy(db[0], hb, lsize);

da[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
db[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
dc[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
q[1].memcpy(da[1], ha + lsize, lsize + gsize % 2);
q[1].memcpy(db[1], hb + lsize, lsize + gsize % 2);

q[0].wait();
q[1].wait();
```

Once the data is available on the two devices, the vector addition kernels are launched on each device and the devices execute the kernels in parallel. After the computations on both devices complete, the results are copied from both the devices to the host.

```cpp
for (int i = 0; i < 16; i ++) {
    q[0].parallel_for(sycl::nd_range<1>(lsize, 1024), [=] (auto idx) {
        int ind = idx.get_global_id();
        dc[0][ind] = da[0][ind] + db[0][ind];
    });
    q[1].parallel_for(sycl::nd_range<1>(lsize + gsize % 2, 1024), [=] (auto idx) {
        int ind = idx.get_global_id();
        dc[1][ind] = da[1][ind] + db[1][ind];
    });
}

q[0].wait();
q[1].wait();

std::cout << "Offloaded work completed" << std::endl;

q[0].memcpy(hc, dc[0], lsize);
q[1].memcpy(hc + lsize, dc[1], lsize + gsize % 2);

q[0].wait();
q[1].wait();
```

Compilation and run commands:

```shell
$ icpx -fsycl flat_sycl_vec_add.cpp -o flat_sycl_vec_add
$ ./flat_sycl_vec_add
```

Note that this example uses 2 devices. It can easily be extended to use more than 2 devices if more than 2 devices are available. We leave this as an exercise.

## FLAT Mode Example - OpenMP

As previously mentioned, in FLAT mode, the stacks are exposed as devices.

Offloading to a single device (stack)

In this scheme, the default root device which is device 0 is used to offload. See code example below:

```c
int device_id = omp_get_default_device();

#pragma omp target teams distribute parallel for device(device_id) map(...)
for (int i = 0, i < N; i++) {
    ...
}
```

## Offloading to multiple devices (stacks)

In this scheme, we have multiple root devices (stacks) on which the code will run; the stacks may belong to one or more GPU cards. See code example below:

```txt
int num_devices = omp_get_num_devices();

#pragma omp parallel for
for (int device_id = 0; device_id < num_devices; device_id++) {

    #pragma omp target teams distribute parallel for device(device_id) map(...)
    for (int i = lb(device_id); I < ub(device_id); i++) {
        ...
    }
}
```

We present below a full OpenMP program that offloads to multiple devices (stacks) in FLAT mode.

## OpenMP Example

In the following program, flat\_openmp\_01.cpp, the array A is initialized on the device. First, we determine the number of devices (stacks) available, and then use the devices (stacks) to initialize different chunks of the array. The OpenMP device clause on the target pragma is used to specify which stack to use for a particular chunk. (If no device clause is specified, then the code will run on stack 0.)

omp\_get\_num\_devices() returns the total number of devices (stacks) that are available. For example, on a 4-card system with 2 stacks each, the routine will return 8.

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
```

```c
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
```

Compilation command:

```shell
\$ icpx -fiopenmp -fopenmp-targets=spir64 flat_openmp_01.cpp
```

## Run command:

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY ./a.out
```
````
