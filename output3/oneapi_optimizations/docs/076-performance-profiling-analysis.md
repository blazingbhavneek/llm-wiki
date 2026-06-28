## Performance Profiling and Analysis

Understanding the behavior of your system is critical to making informed decisions about optimization choices. Some tools like profilers, analyzers, or debuggers are full-featured. Other tools like interval timers, kernel timers, and print statements are lighter weight. But all of them serve an important purpose in the optimization process.

This section covers topics related to these tools’ use for software optimization.

• Using the Timers

• Intel<sup>®</sup> VTune<sup>TM</sup> Profiler

• Intel<sup>®</sup> Advisor

• Intel<sup>®</sup> Intercept Layer for OpenCL<sup>TM</sup> Applications

• Performance Tools in Intel<sup>®</sup> Profiling Tools Interfaces for GPU

## Using the Timers

The standard C++ chrono library can be used for tracking times with varying degrees of precision in SYCL. The following example shows how to use the chrono timer class to time kernel execution from the host side.

```cpp
#include <sycl/sycl.hpp>
#include <iostream>
using sycl;

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;

double VectorAdd(queue &q, const IntArray &a, const IntArray &b, IntArray &sum) {
    range<1> num_items{a.size()};

    buffer a_buf(a);
    buffer b_buf(b);
    buffer sum_buf(sum.data(), num_items);

    auto t1 = std::chrono::steady_clock::now();   // Start timing

    q.submit([&](handler &h) {
        // Input accessors
        auto a_acc = a_buf.get_access<access::mode::read>(h);
        auto b_acc = b_buf.get_access<access::mode::read>(h);

        // Output accessor
        auto sum_acc = sum_buf.get_access<access::mode::write>(h);

        h.parallel_for(num_items, [=](id<1> i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    }).wait();

    auto t2 = std::chrono::steady_clock::now();   // Stop timing

    return(std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count());
}

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++) a[i] = i;
}

int main() {
    default_selector d_selector;

    IntArray a, b, sum;

    InitializeArray(a);
    InitializeArray(b);

    queue q(d_selector);

    std::cout << "Running on device: "
            << q.get_device().get_info<info::device::name>() << "\n";
    std::cout << "Vector size: " << a.size() << "\n";

    double t = VectorAdd(q, a, b, sum);
```

```cpp
std::cout << "Vector add successfully completed on device in " << t << " microseconds\n";
return 0;
}
```

Note that this timing is purely from the host side. The actual execution of the kernel on the device may start much later, after the submission of the kernel by the host. SYCL provides a profiling capability that let you keep track of the time it took to execute kernels.

```cpp
#include <sycl/sycl.hpp>
#include <array>
#include <iostream>
using namespace sycl;

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;

double VectorAdd(queue &q, const IntArray &a, const IntArray &b, IntArray &sum) {
    range<1> num_items{a.size()};

    buffer a_buf(a);
    buffer b_buf(b);
    buffer sum_buf(sum.data(), num_items);

    event e = q.submit([&](handler &h) {
        // Input accessors
        auto a_acc = a_buf.get_access<access::mode::read>(h);
        auto b_acc = b_buf.get_access<access::mode::read>(h);

        // Output accessor
        auto sum_acc = sum_buf.get_access<access::mode::write>(h);

        h.parallel_for(num_items, [=](id<1> i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    });
    q.wait();
    return(e.template get_profiling_info<info::event_profiling::command_end>() -
        e.template get_profiling_info<info::event_profiling::command_start>());
}

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++) a[i] = i;
}

int main() {
    default_selector d_selector;

    IntArray a, b, sum;

    InitializeArray(a);
    InitializeArray(b);

    queue q(d_selector, property::queue::enable_profiling{});

    std::cout << "Running on device: "
        << q.get_device().get_info<info::device::name>() << "\n";
    std::cout << "Vector size: " << a.size() << "\n";

    double t = VectorAdd(q, a, b, sum);
```

```cpp
std::cout << "Vector add successfully completed on device in " << t << " nanoseconds\n";
return 0;
}
```

When these examples are run, it is quite possible that the time reported by chrono is much larger than the time reported by the SYCL profiling class. This is because the SYCL profiling does not include any data transfer times between the host and the offload device.

## Intel® VTuneTM Profiler

The Intel<sup>®</sup> VTune<sup>TM</sup> Profiler is a performance analysis tool for optimizing CPU, GPU, and other accelerator applications. It helps developers find performance bottlenecks in their applications and identify where and how the applications can be optimized to benefit most from available hardware resources. In terms of GPU performance, it can:

• Find out if the application is CPU or GPU-bound

• Calculate hardware utilization

• Report XVE stalls

• Report locations of stalls, and types of stalls in Intel<sup>®</sup> Data Center GPU Max Series

• Identify hot computing tasks or kernels that could be candidates for further optimizations

• Analyze data transfers and bandwidth utilization

• Identify memory/cache units that bottleneck the performance

• Find inefficient data access patterns in your algorithm and memory access that cause significant stalls

• Determine efficiencies of SIMD instructions generated by the compiler

• Provide quick insights into data collected from multiple GPUs using Application Performance Snapshot

For details and techniques on optimizing GPU performance using VTune Profiler, please see

Software Optimization for Intel® GPUs

Optimize Applications for Intel® GPUs with Intel® VTune™ Profiler

## Intel® Advisor

The Intel<sup>®</sup> Advisor is a tool for assisting developers to design and optimize high-performing applications. In terms of GPU performance, it provides:

• Offload Modeling

• Roofline and Performance Insights

Offload Modeling produces upper-bound speedup estimates using a bound-and-bottleneck performance model. It takes CPU metrics and application characteristics as input and applies an analytical model to estimate execution time and characteristics on a target GPU. It can:

• Identify code regions that benefit from offloading

• Find performance bottlenecks

• Project performance gains with offloading

• Project performance gains if existing code executes on next-generation GPUs

• Provide optimization guidance

Roofline and Performance Insights visualize the actual performance of GPU kernels and inherent hardwareimposed performance ceilings, and determine the main performance limiting factors even on a multi-tile/ multi-card GPU system. It helps developers to find:

• The maximum achievable performance with the current hardware resources

• If the current implementation performs optimally on current hardware

• The best candidates to optimize if the current implementation is not optimal

• The limiting performance factors such as memory bandwidth, compute capacity for each candidate

For details and techniques on optimizing GPU performance using Intel<sup>®</sup> Advisor, please see

Intel® Advisor Performance Optimization Cookbook

## Intel® Intercept Layer for OpenCLTM Applications

The Intercept Layer for OpenCL Applications is a command-line tool for tracing and analyzing OpenCL applications. It has a set of features for logging host and device activities, dumping and disassembling kernel binaries, etc. If your oneAPI applications use OpenCL backend, you may find this tool is helpful for performance tuning.

More information including the source code is available at the github repository Intercept Layer for OpenCL Applications.

## Performance Tools in Intel® Profiling Tools Interfaces for GPU

Intel® Profiling Tools Interfaces for GPU has a set of tracing and profiling tools for Intel<sup>®</sup> oneAPI applications in the tools folder. These lightweight command-line tools support both Level Zero and OpenCL backends.

In addition to device activities, the tools are capable of tracing host activities from Level Zero or OpenCL runtime layer all the way up to MPI layer. You can use the tools to quickly identify bottlenecks on device and host. You can also use the tools to profile GPU hardware performance counters , for example, thread occupancies, memory traffic, cache utilization and function unit utilization etc.. Furthermore, You can run the tool unitrace to profile GPU kernels at instruction level, pinpoint instructions that stalls the execution unit or the vector engine and report reasons of the stalls.

The performance data generated in JSON format can be viewed in a browser using a trace viewer such as https://ui.perfetto.dev.

Please check the tools folder for detailed information and the source code of each tool.
