# Where Code Executes

Parallel programming is not really about driving in the fast lane. It is actually about driving fast in all the lanes. This chapter is all about enabling us to put our code everywhere that we can. We choose to enable all the compute resources in a heterogeneous system whenever it makes sense. Therefore, we need to know where those compute resources are hiding (find them) and put them to work (execute our code on them).

We can control where our code executes—in other words, we can control which devices are used for which kernels. C++ with SYCL provides a framework for heterogeneous programming in which code can execute on a mixture of a host CPU and devices. The mechanisms which determine where code executes are important for us to understand and use.

This chapter describes where code can execute, when it will execute, and the mechanisms used to control the locations of execution. Chapter 3 will describe how to manage data so it arrives where we are executing our code, and then Chapter 4 returns to the code itself and discusses the writing of kernels.

## Single-Source

C++ with SYCL programs are single-source, meaning that the same translation unit (typically a source file and its headers) contains both the code that defines the compute kernels to be executed on SYCL devices and also the host code that orchestrates execution of those kernels. Figure 2-1 shows these two code paths graphically, and Figure 2-2 provides an example application with the host and device code regions marked.

Combining both device and host code into a single-source file (or translation unit) can make it easier to understand and maintain a heterogeneous application. The combination also provides improved language type safety and can lead to more compiler optimizations of our code.

![](images/349494919898921bd715fc1e5aac18651536acca197744c7575e1a43e1035549.jpg)  
Figure 2-1. Single-source code contains both host code (runs on CPU) and device code (runs on SYCL devices)

```cpp
#include <array>
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
  constexpr int size = 16;
  std::array<int, size> data;

  // Create queue on implementation-chosen default device
  queue q;

  // Create buffer using host allocated "data" array
  buffer B{data};

  q.submit([&](handler& h) {

    accessor A{B, h};
    h.parallel_for(size, [=](auto& idx) {

      A[idx] = idx;

    });
  });

  // Obtain access to buffer on the host
  // Will wait for device kernel to execute to generate data
  host_accessor A{B};
  for (int i = 0; i < size; i++)
    std::cout << "data[" << i << "] = " << A[i] << "\n";

  return 0;
}
```  
Figure 2-2. Simple SYCL program

## Host Code

Applications contain C++ host code, which is executed by the CPU(s) on which the operating system has launched the application. Host code is the backbone of an application that defines and controls assignment of work to available devices. It is also the interface through which we define the data and dependences that should be managed by the SYCL runtime.

Host code is standard C++ augmented with SYCL-specific constructs and classes that may be implementable as a C++ library. This makes it easier to reason about what is allowed in host code (anything that is allowed in C++) and can simplify integration with build systems.

The host code in an application orchestrates data movement and compute offload to devices but can also perform compute-intensive work itself and can use libraries like any C++ application.

## Device Code

Devices correspond to accelerators or processors that are conceptually independent from the CPU that is executing host code. An implementation may also expose the host processor as a device, as described later in this chapter, but the host processor and devices should be thought of as logically independent from each other. The host processor runs native C++ code, while devices run device code which includes some additional features and restrictions.

Queues are the mechanism through which work is submitted to a device for future execution. There are three important properties of device code to understand:

1. It executes asynchronously from the host code. The host program submits device code to a device, and the runtime tracks and starts that work only when all dependences for execution are satisfied (more on this in Chapter 3). The host program execution carries on before the submitted work is started on a device, providing the property that execution on devices is asynchronous to host program execution, unless we explicitly tie the two together. As a side effect of this asynchronous execution, work on a device isn’t guaranteed to start until the host program forces execution to begin through various mechanisms that we cover in later chapters, such as host accessors and blocking queue wait operations.

2. There are restrictions on device code to make it possible to compile and achieve performance on accelerator devices. For example, dynamic memory allocation and runtime type information (RTTI) are not supported within device code, because they would lead to performance degradation on many accelerators. The small set of device code restrictions is covered in detail in Chapter 10.

3. Some functions and queries defined by SYCL are available only within device code, because they only make sense there, for example, work-item identifier queries that allow an executing instance of device code to query its position in a larger dataparallel range (described in Chapter 4).

In general, we will refer to work that is submitted to queues as actions. Actions include execution of device code on a device, but in Chapter 3 we will learn that actions also include memory movement commands. In this chapter, since we are concerned with the device code aspect of actions, we will be specific in mentioning device code much of the time.
