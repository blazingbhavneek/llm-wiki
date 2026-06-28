The complete Fourier correlation implementation in USM is included below:

```cpp
#include <iostream>
#include <mkl.h>
#include <oneapi/mkl/dft.hpp>
#include <oneapi/mkl/rng.hpp>
#include <oneapi/mkl/vm.hpp>
#include <sycl/sycl.hpp>

int main(int argc, char **argv) {
    unsigned int N = (argc == 1) ? 32 : std::stoi(argv[1]);
```

```cpp
if ((N % 2) != 0)
    N++;
if (N < 32)
    N = 32;

// Initialize SYCL queue
sycl::queue Q(sycl::default_selector_v);
auto sycl_device = Q.get_device();
auto sycl_context = Q.get_context();
std::cout << "Running on: "
       << Q.get_device().get_info<sycl::info::device::name>() << std::endl;

// Initialize signal and correlation arrays
auto sig1 = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);
auto sig2 = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);
auto corr = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);

// Initialize input signals with artificial data
std::uint32_t seed = (unsigned)time(NULL); // Get RNG seed value
oneapi::mkl::rng::mcg31m1 engine(Q, seed); // Initialize RNG engine
                                      // Set RNG distribution
oneapi::mkl::rng::uniform<float, oneapi::mkl::rng::uniform_method::standard>
    rng_distribution(-0.00005, 0.00005);

auto evt1 =
    oneapi::mkl::rng::generate(rng_distribution, engine, N, sig1); // Noise
auto evt2 = oneapi::mkl::rng::generate(rng_distribution, engine, N, sig2);
evt1.wait();
evt2.wait();

Q.single_task<>([=]() {
    sig1[N - N / 4 - 1] = 1.0;
    sig1[N - N / 4] = 1.0;
    sig1[N - N / 4 + 1] = 1.0; // Signal
    sig2[N / 4 - 1] = 1.0;
    sig2[N / 4] = 1.0;
    sig2[N / 4 + 1] = 1.0;
}).wait();

clock_t start_time = clock(); // Start timer

// Initialize FFT descriptor
oneapi::mkl::dft::descriptor<oneapi::mkl::dft::precision::SINGLE,
                             oneapi::mkl::dft::domain::REAL>
    transform_plan(N);
transform_plan.commit(Q);

// Perform forward transforms on real arrays
evt1 = oneapi::mkl::dft::compute_forward(transform_plan, sig1);
evt2 = oneapi::mkl::dft::compute_forward(transform_plan, sig2);

// Compute: DFT(sig1) * CONJG(DFT(sig2))
oneapi::mkl::vm::mulbyconj(
    Q, N / 2, reinterpret_cast<std::complex<float> *>(sig1),
    reinterpret_cast<std::complex<float> *>(sig2),
    reinterpret_cast<std::complex<float> *>(corr), {evt1, evt2})
    .wait();
```

```cpp
// Perform backward transform on complex correlation array
oneapi::mkl::dft::compute_backward(transform_plan, corr).wait();

clock_t end_time = clock(); // Stop timer
std::cout << "The 1D correlation (N = " << N << ") took "
       << float(end_time - start_time) / CLOCKS_PER_SEC << " seconds."
       << std::endl;

// Find the shift that gives maximum correlation value
float max_corr = 0.0;
int shift = 0;
for (unsigned int idx = 0; idx < N; idx++) {
    if (corr[idx] > max_corr) {
        max_corr = corr[idx];
        shift = idx;
    }
}
int _N = static_cast<int>(N);
shift =
    (shift > _N / 2) ? shift - _N : shift; // Treat the signals as circularly
                                      // shifted versions of each other.
std::cout << "Shift the second signal " << shift
       << " elements relative to the first signal to get a maximum, "
       "normalized correlation score of "
       << max_corr / N << "." << std::endl;

// Cleanup
sycl::free(sig1, sycl_context);
sycl::free(sig2, sycl_context);
sycl::free(corr, sycl_context);
}
```

Note that the final step of finding the location of the maximum correlation value is performed on the host. It would be better to do this computation on the device, especially when the input data is large. Fortunately, the maxloc reduction is a common parallel pattern that can be implemented using SYCL. This is left as an exercise for the reader, but Figure 14-11 of Data Parallel C++ provides a suitable example to help you get started.

## Boost Matrix Multiplication Performance with Intel® Xe Matrix Extensions

The increasing popularity of Artificial Intelligence (AI) in today’s world demands the introduction of low precision data types and hardware support for these data types to boost application performance. Low precision models are faster in computation and have smaller memory footprints. For the same reason low precision data types are getting highly used for both training and inference in AI / machine learning (ML) even though float32 is the default data type. To optimize and support these low precision data types, special hardware features and instructions are required. Intel provides those in the form of Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions (Intel<sup>®</sup> XMX) in its GPUs. Some of the most used 16-bit formats and 8-bit formats are float16 (fp16), bfloat16 (bf16), 16-bit integer (int16), 8-bit integer (int8) etc. The figure below visualizes the differences between some of these formats.

![](images/63da75d6ddb0956738a45f602cb731d72843b26f5a1a18269fa2cd88d9d29e89.jpg)  
In the above figure, s is the signed bit(the first digit of the binary presentation, 0 implies positive number and 1 implies negative number) and exp is the exponent.

## Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions

Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions (Intel<sup>®</sup> XMX) specializes in executing Dot Product Accumulate Systolic (DPAS) instructions on 2D systolic arrays. A systolic array in parallel computer architecture is a homogeneous network of tightly coupled data processing units. Each unit computes a partial result as a function of data received from its upstream neighbors, stores the result within itself and passes it downstream. Intel<sup>®</sup> XMX supports numerous data types, depending on hardware generation, such as int8, fp16, bf16, and tf32. To understand Intel<sup>®</sup> XMX inside Intel<sup>®</sup> Data Center GPU Max Series, please refer to Intel<sup>®</sup> Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> GPU Architecture section.

## Programming Intel<sup>®</sup> XMX

Users can interact with XMX at many different levels: from deep learning frameworks, dedicated libraries, custom SYCL kernels, down to low-level intrinsics. Programming and running applications using Intel XMX requires Intel<sup>®</sup> oneAPI Base Toolkit.

Using Intel<sup>®</sup> oneAPI Deep Neural Network Library (oneDNN)

To take the maximum advantage of the hardware, oneDNN has enabled Intel<sup>®</sup> XMX support on Intel GPUs (Intel<sup>®</sup> X<sup>e</sup> 4th Generation Scalable processors and later) by default. To uses the data types supported by XMX and oneDNN, the applications needs to be built with GPU support enabled.

The Matrix Multiplication Performance bundled with oneDNN is a good example to learn how to use oneDNN to program Intel XMX.

## Using Intel<sup>®</sup> oneAPI Math Kernel Library (oneMKL)

Like oneDNN, oneMKL also enables Intel<sup>®</sup> XMX by default if we use the supported data types and the code is compiled using the Intel<sup>®</sup> oneAPI DPC++ Compiler.

oneMKL supports several algorithms for accelerating single-precision gemm and gemm\_batch using XMX. The bf16x2 and bf16x3 are 2 such algorithms using bf16 to approximate single-precision gemm.

Internally single-precision input data is converted into bf16 and multiplied with the systolic array. The three variants – bf16, bf16x2, and bf16x3 – allow you to make a tradeoff between accuracy and performance, with bf16 being the fastest and bf16x3 the most accurate (similar to the accuracy of standard single-precision gemm). The example Matrix Multiplication shows how to use these algorithms and the table below compares the performance difference.

<table><tr><td>Precision</td><td>Data type/ Algorithm</td><td>Peak (TF)</td><td>Performance relative totheoretical peak ofsingle precision(%)</td></tr><tr><td>Single</td><td>fp32</td><td>26</td><td>98</td></tr><tr><td>Single</td><td>bf16</td><td>151</td><td>577</td></tr><tr><td>Single</td><td>bf16x2</td><td>74</td><td>280</td></tr><tr><td>Single</td><td>bf16x3</td><td>42</td><td>161</td></tr></table>

![](images/bf7a9cb8dd402e5c289b65e5e65d4eb404bc7c9dbe92556e21e824ca827edbd9.jpg)  
The test is performed on a Intel<sup>®</sup> Xeon<sup>®</sup> 8480+ with512 GB DDR5-4800 + Intel<sup>®</sup> Data Center GPU Max 1550 running Ubuntu 22.04.

This table shows the Performance of bf16, bf16x2 and bf16x3 far outweigh the theoretical peak of single precision. If the accuracy tradeoff is acceptable, bf16, followed by bf16x2 and then bf16x3, is highly recommended.

## References

1. Matrix Multiplication Performance

2. Matrix Multiplication

## Host/Device Memory, Buffer and USM

Accelerators have access to a rich memory hierarchy. Utilizing the right level in the hierarchy is critical to getting the best performance.

In this section we cover topics related to declaration, movement, and access to the memory hierarchy.

The API allows sharing of memory objects across different device processes. Since each process has its own virtual address space, there is no guarantee that the same virtual address will be available when the memory object is shared in new process. There are a set of APIs that make it easier to share the memory objects.

To learn more about using the oneAPI Level Zero API for memory sharing, see Inter-Process Communication in the Level Zero Specification.

• Unified Shared Memory Allocations

• Performance Impact of USM and Buffers

• Avoiding Moving Data Back and Forth between Host and Device

• Optimizing Data Transfers

• Avoiding Declaring Buffers in a Loop

• Buffer Accessor Modes

## Unified Shared Memory Allocations

Unified Shared Memory (USM) allows a program to use C/C++ pointers for memory access. There are three ways to allocate memory in SYCL:

## malloc\_device:

• Allocation can only be accessed by the specified device but not by other devices in the context nor by host.

• The data stays on the device all the time and thus is the fastest choice for kernel execution.

• Explicit copy is needed to transfer data to the host or other devices in the context.

## malloc\_host:

• Allocation can be accessed by the host and any other device in the context.

• The data stays on the host all the time and is accessed via PCI from the devices.

• No explicit copy is needed for synchronizing of the data with the host or devices.

## malloc\_shared:

• Allocation can be accessed by the host and the specified device only.

• The data can migrate (operated by the Level-Zero driver) between the host and the device for faster access.

• No explicit copy is necessary for synchronizing between the host and the device, but it is needed for other devices in the context.

The three kinds of memory allocations and their characteristics are summarized in the table below.

Memory allocation types and characteristics

<table><tr><td>Memory allocation types</td><td>Description</td><td>Host accessible</td><td>Device accessible</td><td>Location</td></tr><tr><td>host</td><td>allocated in host memory</td><td>yes</td><td>yes, remotely through PCIe or fabric link</td><td>host</td></tr><tr><td>device</td><td>allocated in device memory</td><td>no</td><td>yes</td><td>device</td></tr><tr><td>shared</td><td>allocated shared between host and device</td><td>yes</td><td>yes</td><td>dynamically migrate between host and device</td></tr></table>

In a multi-stack, multi-C-slice GPU environment, it is important to note that device and shared USM allocations are associated with the root device. Hence, they are accessible by all the stacks and C-slices on the same device. A program should use root device for malloc\_device and malloc\_shared allocations to avoid confusion.

## OpenMP USM Allocation API

To align with SYCL USM model, we added three new OpenMP APIs as Intel extensions for users to perform memory allocations based on application, memory size and performance requirements. Their semantics and performance characteristics are detailed in the following subsections.

## Host Memory Allocation

This host allocation is easier to use than device allocations since we do not have to manually copy data between the host and the device. Host allocations are allocations in host memory that are accessible on both the host and the device. These allocations, while accessible on the device, cannot migrate to the device’s attached memory. Instead, offloading regions that read from or write to this memory do it remotely through either PCIe bus or fabric link. This tradeoff between convenience and performance is something that we must take into consideration. Despite the higher access costs that host allocations can incur, there are still valid reasons to use them. Examples include rarely accessed data or large data sets that cannot fit inside device attached memory. The API to perform host memory allocation is:

```txt
extern void *omp_target_alloc_host(size_t size, int device_num)
```

## Device Memory Allocation

This kind of allocation is what users need in order to have a pointer into a device’s attached memory, such as (G)DDR, or HBM on the device. Device allocations can be read from or written to by offloading regions running on a device, but they cannot be directly accessed from code executing on the host. Trying to access a device allocation on the host can result in either incorrect data or a program crashing. The API to perform device memory allocation is:

```c
extern void *omp_target_alloc_device(size_t size, int device_num)
```

## Shared Memory Allocation

Like host allocations, shared allocations are accessible on both the host and the device. The difference between them is that shared allocations are free to migrate between host memory and device attached memory, automatically, without our intervention. If an allocation has migrated to the device, any offloading region executing on that device accessing it will do so with greater performance than remotely accessing it from the host. However, shared allocations do not give us all the benefits without any drawbacks such as page migration cost and ping-pong effects:

extern void \*omp\_target\_alloc\_shared(size\_t size, int device\_num)

USM Support for omp\_target\_alloc API

The OpenMP API for target memory allocation maps to:

```c
extern void *omp_target_alloc_device(size_t size, int device_num)
```

## Performance Impact of USM and Buffers

SYCL offers several choices for managing memory on the device. This section discusses the performance tradeoffs, briefly introducing the concepts. For an in-depth explanation, see Data Parallel C++.

As with other language features, the specification defines the behavior but not the implementation, so performance characteristics can change between software versions and devices. This guide provide best practices.

Buffers. A buffer is a container for data that can be accessed from a device and the host. The SYCL runtime manages memory by providing APIs for allocating, reading, and writing memory. The runtime is responsible for moving data between host and device, and synchronizing access to the data.

Unified Shared Memory (USM). USM allows reading and writing of data with conventional pointers, in contrast to buffers where access to data is exclusively by API. USM has two commonly-used variants. Device allocations can only be accessed from the device and therefore require explicit movement of data between host and device. Shared allocations can be referenced from device or host, with the runtime automatically moving memory.

We illustrate the tradeoffs between choices by showing the same example program written with the three models. To highlight the issues, we use a program where a GPU and the host cooperatively compute, and therefore need to ship data back and forth.

We start by showing the serial computation below. Assume that we want to perform the loop at line 9 on the GPU and the loop on line 14 on the CPU. Both loops read and write the data array so data must move between host and GPU for each iteration of the loop in line 8.

```txt
void serial(int stride) {
  // Allocate and initialize data
  float *data = new float[data_size];
  init(data);

  timer it;

  for (int i = 0; i < time_steps; i++) {
    for (int j = 0; j < data_size; j++) {
      for (int k = 0; k < device_steps; k++)
        data[j] += 1.0;
    }

    for (int j = 0; j < data_size; j += stride)
      data[j] += 1.0;
  }
  put_elapsed_time(it);

  check(data);

  delete[] data;
} // serial
```

## Buffers

Below, we show the same computation using buffers to manage data. A buffer is created at line 3 and initialized by the init function. The init function is not shown. It accepts an accessor or a pointer. The parallel\_for executes the kernel defined on line 13. The kernel uses the device\_dataaccessor to read and write data in buffer\_data.

Note that the code does not specify the location of data. An accessor indicates when and where the data is needed, and the SYCL runtime moves the data to the device (if necessary) and then launches the kernel. The host\_accessor on line 21 indicates that the data will be read/written on the host. Since the kernel is also read/writing buffer\_data, the host\_accessor constructor waits for the kernel to complete and moves data to the host to perform the read/write on line 23. In the next iteration of the loop the accessor constructor on line 11 waits until the until the data is moved back to the device, which effectively delays launching the kernel.

```cpp
void buffer_data(int stride) {
  // Allocate buffer, initialize on host
  sycl::buffer<float> buffer_data{data_size};
  init(sycl::host_accessor(buffer_data, sycl::write_only, sycl::no_init));

  timer it;
  for (int i = 0; i < time_steps; i++) {

    // Compute on device
    q.submit([&](auto &h) {
      sycl::accessor device_data(buffer_data, h);

      auto compute = [=](auto id) {
        for (int k = 0; k < device_steps; k++)
          device_data[id] += 1.0;
      };
      h.parallel_for(data_size, compute);
```

```cpp
});

// Compute on host
sycl::host_accessor host_data(buffer_data);
for (int i = 0; i < data_size; i += stride)
    host_data[i] += 1.0;
}
put_elapsed_time(it);

const sycl::host_accessor h(buffer_data);
check(h);
} // buffer_data
```

## Performance Considerations

The data access on lines 15 and 23 appear to be simple array references, but they are implemented by the SYCL runtime with C++ operator overloading. The efficiency of accessor array references depends on the implementation. In practice, device code pays no overhead for overloading compared to direct memory references. The runtime does not know in advance which part of the buffer is accessed, so it must ensure all the data is on the device before the kernel begins. This is true today, but may change over time.

The same is not currently true for the host\_accessor. The runtime does not move all the data to the host. The array references are implemented with more complex code and are significantly slower than native C++ array references. While it is acceptable to reference a small amount of data, computationally intensive algorithms using host\_accessor pay a large performance penalty and should be avoided.

Another concern is concurrency. A host\_accessor can block kernels that reference the same buffer from launching, even if the accessor is not actively being used to read/write data. Limit the scope that contains the host\_accessor to the minimum possible. In this example, the host accessor on line 4 is destroyed after the init function returns and the host accessor on line 21 is destroyed at the end of each loop iteration.

## Shared Allocations

Next we show the same algorithm implemented with shared allocations. Data is allocated on line 2. Accessors are not needed because USM-allocated data can be referenced with conventional allows pointers. Therefore, the array references on lines 10 and 15 can be implemented with simple indexing. The parallel\_for on line 12 ends with a wait to ensure the kernel finishes before the host accesses data on line 15. Similar to buffers, the SYCL runtime ensures that all the data is resident on the device before launching a kernel. And like buffers, shared allocations are not copied to the host unless it is referenced. The first time the host references data, there is an operating system page fault, a page of data is copied from device to host, and execution continues. Subsequent references to data on the same page execute at full speed. When a kernel is launched, all of the host-resident pages are flushed back to the device.

```cpp
void shared_usm_data(int stride) {
    float *data = sycl::malloc_shared<float>(data_size, q);
    init(data);

    timer it;

    for (int i = 0; i < time_steps; i++) {
        auto compute = [=](auto id) {
            for (int k = 0; k < device_steps; k++)
                data[id] += 1.0;
        };
        q.parallel_for(data_size, compute).wait();

        for (int k = 0; k < data_size; k += stride)
            data[k] += 1.0;
```

```cpp
}
q.wait();
put_elapsed_time(it);

check(data);

sycl::free(data, q);
} // shared_usm_data
```

## Performance Considerations

Compared to buffers, data references are simple pointers and perform well. However, servicing page faults to bring data to the host incurs overhead in addition to the cost of transferring data. The impact on the application depends on the reference pattern. Sparse random access has the highest overhead and linear scans through data have lower impact from page faults.

Since all synchronization is explicit and under programmer control, concurrency is not an issue for a well designed program.

## Device Allocations

The same program with device allocation can be found below. With device allocation, data can only be directly accessed on the device and must be explicitly copied to the host, as is done on line 21. All synchronization between device and host are explicit. Line 21 ends with a wait so the host code will not execute until the asynchronous copy finishes. The queue definition is not shown but uses an in-order queue so the memcpy on line 21 waits for the parallel\_for on line 18 to complete.

```cpp
void device_usm_data(int stride) {
  // Allocate and initialize host data
  float *host_data = new float[data_size];
  init(host_data);

  // Allocate device data
  float *device_data = sycl::malloc_device<float>(data_size, q);

  timer it;

  for (int i = 0; i < time_steps; i++) {
    // Copy data to device and compute
    q.memcpy(device_data, host_data, sizeof(float) * data_size);
    auto compute = [=](auto id) {
      for (int k = 0; k < device_steps; k++)
        device_data[id] += 1.0;
    };
    q.parallel_for(data_size, compute);

    // Copy data to host and compute
    q.memcpy(host_data, device_data, sizeof(float) * data_size).wait();
    for (int k = 0; k < data_size; k += stride)
      host_data[k] += 1.0;
  }
  q.wait();
  put_elapsed_time(it);

  check(host_data);
```

```cpp
sycl::free(device_data, q);
    delete[] host_data;
} // device_usm_data
```
