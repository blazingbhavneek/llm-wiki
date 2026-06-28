## Performance Considerations

Both data movement and synchronization are explicit and under the full control of the programmer. Array references are array references on the host, so it has neither the page faults overhead of shared allocations, nor the overloading overhead associated with buffers. Shared allocations only transfer data that the host actually references, with a memory page granularity. In theory, device allocations allow on-demand movement of any granularity. In practice, fine-grained, asynchronous movement of data can be complex and most programmers simply move the entire data structure once. The requirement for explicit data movement and synchronization makes the code more complicated, but device allocations can provide the best performance.

## Avoiding Moving Data Back and Forth between Host and Device

The cost of moving data between host and device is quite high, especially in the case of discrete accelerators. So it is very important to avoid data transfers between host and device as much as possible. In some situations it may be required to bring the data that was computed by a kernel on the accelerator to the host and do some operation on it and send it back to the device for further processing. In such situation we will end up paying for the cost of device to host transfer and then again host to device transfer.

Consider the following example, where one kernel produces data through some operation (in this case vector add) into a new vector. This new vector is then transformed into a third vector by applying a function on each value and this third vector is finally fed as input into another kernel for some additional computation. This form of computation is quite common and occurs in many domains where algorithms are iterative and output from one computation needs to be fed as input into another computation. In machine learning, for example, models are structured as layers of computations, and output of one layer is input to the next layer.

```cpp
double myFunc1(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()};
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessors
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(num_items,
                [=](auto id) { sum_acc[id] = a_acc[id] + b_acc[id]; });
        });
```

```cpp
{
    sycl::host_accessor h_acc(sum_buf);
    for (size_t j = 0; j < a.size(); j++)
        if (h_acc[j] > 10)
            h_acc[j] = 1;
        else
            h_acc[j] = 0;
}

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto id) {
        res_acc[id] = sum_acc[id] * c_acc[id] + d_acc[id];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
} // end myFunc1
```

Instead of bringing the data to the host and applying the function to the data and sending it back to the device, you can create a kernel3 to execute this function on the device, as shown in the following example. The kernel kernel3 operates on the intermediate data in accum\_buf in between kernel1 and kernel2, avoiding the round trip of data transfer between the device and the host.

```cpp
double myFunc2(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()} {
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(num_items,
                [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
```

```cpp
});

// kernel3
q.submit([&](auto &h) {
    sycl::accessor sum_acc(sum_buf, h, sycl::read_write);
    h.parallel_for(num_items, [=](auto id) {
        if (sum_acc[id] > 10)
            sum_acc[id] = 1;
        else
            sum_acc[id] = 0;
    });
});

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto i) {
        res_acc[i] = sum_acc[i] * c_acc[i] + d_acc[i];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
// end myFunc2
```

There are other ways to optimize this example. For instance, the clipping operation in kernel3 can be merged into the computation of kernel1 as shown below. This is kernel fusion and has the added advantage of not launching a third kernel. The SYCL compiler cannot do this kind of optimization. In some specific domains like machine learning, there are graph compilers that operate on the ML models and fuse the operations, which has the same impact.

```cpp
double myFunc3(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()};
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
```

```cpp
// Output accessor
sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

h.parallel_for(num_items, [=](auto i) {
    int t = a_acc[i] + b_acc[i];
    if (t > 10)
        sum_acc[i] = 1;
    else
        sum_acc[i] = 0;
});
});

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto i) {
        res_acc[i] = sum_acc[i] * c_acc[i] + d_acc[i];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
// end myFunc3
```

We can take this kernel fusion one level further and fuse both kernel1 and kernel2 as shown in the code below. This gives very good performance since it avoids the intermediate accum\_buf completely, saving memory in addition to launching an additional kernel. Most of the performance benefit in this case is due to improvement in locality of memory references.

```cpp
double myFunc4(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()}  
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            sycl::accessor c_acc(c_buf, h, sycl::read_only);
            sycl::accessor d_acc(d_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);
```

```javascript
h.parallel_for(num_items, [=](auto i) {
    int t = a_acc[i] + b_acc[i];
    if (t > 10)
        res_acc[i] = c_acc[i] + d_acc[i];
    else
        res_acc[i] = d_acc[i];
});
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
} // end myFunc4
```

## Optimizing Data Transfers

## Introduction

The previous section discussed minimizing data transfers between host and device. This section discusses ways to speed up data transfers when there is a need to move data between host and device.

When moving data repeatedly between host and device, the data transfer rate is maximized when both the source and destination are in Unified Shared Memory (USM).

In this section, we show how performance can be improved by calling SYCL and OpenMP APIs to use host Unified Shared Memory (USM), instead of system memory (such as memory allocated using malloc or new).

## Optimizing Data Transfers in SYCL

In SYCL, data transfers between host and device may be explicit via the use of the SYCL memcpy function, or implicit via the use of SYCL buffers and accessors.

## Case 1: Data transfers using buffers

In the case of SYCL buffers constructed with a pointer to pre-allocated system memory, the SYCL runtime has the capability to use host USM at buffer creation, and to release the host USM at buffer destruction. To enable this capability, a buffer has to be created with a host pointer, for example:

```c
int* hostptr = (int*)malloc(4*sizeof(int));
buffer<int, 1> Buffer(hostptr,4);
```

and then the environment variable SYCL\_USM\_HOSTPTR\_IMPORT=1 should be set at runtime.

## Case 2: Data transfers using SYCL data movement APIs

When the host data allocation is under user control, and the allocated pointer is going to be used in a data transfer API, the user may use USM functions such as malloc\_host to allocate host USM memory instead of system memory.

If the source code where memory is allocated is not available or cannot be modified then, for efficient data transfers, system memory can be imported (prepared for device copy) before the first data transfer, and released after all uses and data transfers are completed.

A set of APIs are provided for import (prepare) and release. They give the programmer explicit control over the address range and the duration of the import.

## SYCL Experimental Prepare and Release APIs

The interfaces for the SYCL prepare and release APIs are as follows:

```cpp
void* sycl::prepare_for_device_copy
    (void* ptr, size_t numBytes, sycl::context& syclContext)

void* sycl::prepare_for_device_copy
    (void* ptr, size_t numBytes, sycl::queue& syclQueue)

void sycl::release_from_device_copy
    (void* ptr, sycl::context& syclContext)

void sycl::release_from_device_copy
    (void* ptr, sycl::queue& syclQueue)
```

See sycl\_ext\_oneapi\_copy\_optimize for a description of the APIs.

The APIs are simple to use, but the onus is on the user to ensure correctness and safety with respect to the lifetime of the memory ranges.

## Notes:

• If the numBytes argument is not the same as the size of the malloc’ed memory block (for example, if the malloc’ed memory is 1024 bytes, but numBytes is 512 or 2048), the guidance here would be to use a size for the import (prepare) that matches the data transfer size. If the true allocation is bigger, then importing less than the true allocation has no ill effects. Importing more than the true allocation is a user error.

• The prepare/release APIs are experimental and are subject to change.

## SYCL Example

The following example, sycl\_prepare\_bench.cpp, measures the rate of data transfer between host and device. The data transfer size can be varied. The program prints device-to-host and host-to-device data transfer rate, measured in Gigabytes per second. Switches passed to the program are used to control data transfer direction, whether or not the SYCL prepare API is used, and a range of transfer sizes. The switches are listed in the example source.

In the program, the import (prepare) is done once at the beginning, and the release is done once at the end, using the following calls:

```cpp
sycl::ext::oneapi::experimental::prepare_for_device_copy(
    hostp, transfer_upper_limit, dq);

sycl::ext::oneapi::experimental::release_from_device_copy(hostp, dq);
```

In between the above calls, there is a loop that repeatedly does memcpy involving the pointer hostp.

```cpp
#include <math.h>
#include <stdlib.h>
#include <chrono>
#include <time.h>
#include <unistd.h>
#include <sycl/sycl.hpp>

using namespace sycl;

static const char *usage_str =
    "\n ze_bandwidth [OPTIONS]"
    "\n"
    "\n OPTIONS:"
    "\n -t, string selectively run a particular test:"
    "\n h2d or H2D run only Host-to-Device tests"
```

```c
"\n     d2h or D2H                  run only Device-to-Host tests "
"\n                   [default: both]"
"\n -q                  minimal output"
"\n                   [default: disabled]"
"\n -v                  enable verificaton"
"\n                   [default: disabled]"
"\n -i                  set number of iterations per transfer"
"\n                   [default: 500]"
"\n -s                  select only one transfer size (bytes) "
"\n -sb                  select beginning transfer size (bytes)"
"\n                   [default: 1]"
"\n -se                  select ending transfer size (bytes)"
"\n                   [default: 2^28]"
"\n -l                  use SYCL prepare_for_device_copy/release_from_device_copy APIs"
"\n                   [default: disabled]"
"\n -h, --help          display help message"
"\n";

static uint32_t sanitize_ulong(char *in) {
  unsigned long temp = strtoul(in, NULL, 0);
  if (ERANGE == errno) {
    fprintf(stderr, "%s out of range of type ulong\n", in);
  } else if (temp > UINT32_MAX) {
    fprintf(stderr, "%ld greater than UINT32_MAX\n", temp);
  } else {
    return static_cast<uint32_t>(temp);
  }
  return 0;
}

size_t transfer_lower_limit = 1;
size_t transfer_upper_limit = (1 << 28);
bool verify = false;
bool run_host2dev = true;
bool run_dev2host = true;
bool verbose = true;
bool prepare = false;
uint32_t ntimes = 500;

// kernel latency
int main(int argc, char **argv) {
  for (int i = 1; i < argc; i++) {
    if ((strcmp(argv[i], "-h") == 0) || (strcmp(argv[i], "--help") == 0)) {
      std::cout << usage_str;
      exit(0);
    } else if (strcmp(argv[i], "-q") == 0) {
      verbose = false;
    } else if (strcmp(argv[i], "-v") == 0) {
      verify = true;
    } else if (strcmp(argv[i], "-l") == 0) {
      prepare = true;
    } else if (strcmp(argv[i], "-i") == 0) {
      if ((i + 1) < argc) {
        ntimes = sanitize_ulong(argv[i + 1]);
        i++;
      }
    } else if (strcmp(argv[i], "-s") == 0) {
      if ((i + 1) < argc) {
```

```cpp
transfer_lower_limit = sanitize_ulong(argv[i + 1]);
transfer_upper_limit = transfer_lower_limit;
i++;
}
} else if (strcmp(argv[i], "-sb") == 0) {
if ((i + 1) < argc) {
transfer_lower_limit = sanitize_ulong(argv[i + 1]);
i++;
}
} else if (strcmp(argv[i], "-se") == 0) {
if ((i + 1) < argc) {
transfer_upper_limit = sanitize_ulong(argv[i + 1]);
i++;
}
} else if ((strcmp(argv[i], "-t") == 0)) {
run_host2dev = false;
run_dev2host = false;

if ((i + 1) >= argc) {
std::cout << usage_str;
exit(-1);
}
if ((strcmp(argv[i + 1], "h2d") == 0) ||
(strcmp(argv[i + 1], "H2D") == 0)) {
run_host2dev = true;
i++;
} else if ((strcmp(argv[i + 1], "d2h") == 0) ||
(strcmp(argv[i + 1], "D2H") == 0)) {
run_dev2host = true;
i++;
} else {
std::cout << usage_str;
exit(-1);
}
} else {
std::cout << usage_str;
exit(-1);
}
}

queue dq;
device dev = dq.get_device();
size_t max_compute_units = dev.get_info<info::device::max_compute_units>();
const auto &sycl_be = dq.get_device().get_backend();
auto BE = (sycl_be == sycl::backend::ext_oneapi_level_zero)
        ? "L0"
        : (sycl_be == sycl::backend::opencl) ? "OpenCL"
                : "Unknown";
if (verbose)
std::cout << "Device name " << dev.get_info<info::device::name>() << " "
              << "max_compute units"
              << " " << max_compute_units << ", Backend " << BE << "\n";

void *hostp;
posix_memalign(&hostp, 4096, transfer_upper_limit);
memset(hostp, 1, transfer_upper_limit);

if (prepare) {
```

```cpp
if (verbose)
    std::cout << "Doing L0 Import\n";
    sycl::ext::oneapi::experimental::prepare_for_device_copy(
        hostp, transfer_upper_limit, dq);
}

void *destp =
    malloc_device<char>(transfer_upper_limit, dq.get_device(), dq.get_context())
dq.submit([&](handler &cgh) { cgh.memset(destp, 2, transfer_upper_limit); });
dq.wait();

if (run_host2dev) {
    if (!verbose)
        printf("SYCL USM API (%s)\n", BE);
        for (size_t s = transfer_lower_limit; s <= transfer_upper_limit; s <<= 1) {
            auto start_time = std::chrono::steady_clock::now();
            for (size_t i = 0; i < ntimes; ++i) {
                dq.submit([&](handler &cgh) { cgh.memcpy(destp, hostp, s); });
                dq.wait();
            }
            auto end_time = std::chrono::steady_clock::now();
            std::chrono::duration<double> seconds = end_time - start_time;

            if (verbose)
                printf("HosttoDevice: %8lu bytes, %7.3f ms, %8.3g GB/s\n", s,
                    1000 * seconds.count() / ntimes,
                    1e-9 * s / (seconds.count() / ntimes));
            else
                printf("%10.6f\n", 1e-9 * s / (seconds.count() / ntimes));
        }
}

if (run_dev2host) {
    if (!verbose)
        printf("SYCL USM API (%s)\n", BE);
        for (size_t s = transfer_lower_limit; s <= transfer_upper_limit; s <<= 1) {
            auto start_time = std::chrono::steady_clock::now();
            for (size_t i = 0; i < ntimes; ++i) {
                dq.submit([&](handler &cgh) { cgh.memcpy(hostp, destp, s); });
                dq.wait();
            }
            auto end_time = std::chrono::steady_clock::now();
            std::chrono::duration<double> seconds = end_time - start_time;

            if (verbose)
                printf("DeviceToHost: %8lu bytes, %7.3f ms, %8.3g GB/s\n", s,
                    seconds.count(), 1e-9 * s / (seconds.count() / ntimes));
            else
                printf("%10.6f\n", 1e-9 * s / (seconds.count() / ntimes));
        }
}

if (prepare)
    sycl::ext::oneapi::experimental::release_from_device_copy(hostp, dq);

free(hostp);
free(destp, dq.get_context());
```

## Compilation command:

```batch
icpx -fsycl sycl_prepare_bench.cpp
```

## Example run command:

```batch
a.out -p -t h2d -s 256000000
```

The above run command specifies doing the prepare (-p), host-to-device (-t h2d), and transferring 256 million bytes (-s 256000000).

## Date Transfer Rate Measurements

We use the program, sycl\_prepare\_bench.cpp, to measure the rate of data transfer between host and device (with and without prepare/release).

The transfer rate for a data size of 256 million bytes when running on the particular GPU used (1-stack only) was as follows.

<table><tr><td>Run Command</td><td>Transfer Direction</td><td>Use prepare/ release</td><td>API?</td><td>Tr an sfe r Ra te</td><td>(GB/sec)</td></tr><tr><td>a.out -t h2d -s 256000000</td><td>host to device</td><td>No</td><td></td><td>26.9</td><td></td></tr><tr><td>a.out -p -t h2d -s 256000000</td><td>host to device</td><td>Yes</td><td></td><td>45.4</td><td></td></tr><tr><td>a.out -t d2h -s 256000000</td><td>device to host</td><td>No</td><td></td><td>33.2</td><td></td></tr><tr><td>a.out -p -t d2h -s 256000000</td><td>device to host</td><td>Yes</td><td></td><td>48.0</td><td></td></tr></table>
