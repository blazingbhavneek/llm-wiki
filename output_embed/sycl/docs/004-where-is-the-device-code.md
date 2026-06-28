## Where Is the Device Code?

There are multiple mechanisms that can be used to define code that will be executed on a device, but a simple example shows how to identify such code. Even if the pattern in the example appears complex at first glance, the pattern remains the same across all device code definitions so quickly becomes second nature.

The code passed as the final argument to the parallel\_for, defined as a lambda expression in Figure 2-18, is the device code to be executed on a device. The parallel\_for in this case is the construct that lets us distinguish device code from host code. The parallel\_for is one of a small set of device dispatch mechanisms, all members of the handler class, that define the code to be executed on a device. A simplified definition of the handler class is given in Figure 2-19.

```javascript
q.submit([&](handler& h) {
  accessor acc{B, h};

  h.parallel_for(size,
              [=](auto& idx) { acc[idx] = idx; });
});
```

Figure 2-18. Submission of device code

```cpp
class handler {
public:
  // Specify event(s) that must be complete before the action
  // defined in this command group executes.
  void depends_on(std::vector<event> & events);

  // Guarantee that the memory object accessed by the accessor
  // is updated on the host after this action executes.
  template <typename AccessorT>
  void update_host(AccessorT acc);

  // Submit a memset operation writing
  // to the specified pointer.
  // Return an event representing this operation.
  event memset(void *ptr, int value, size_t count);

  // Submit a memcpy operation copying from src to dest.
  // Return an event representing this operation.
  event memcpy(void *dest, const void *src, size_t count);

  // Copy to/from an accessor and host memory.
  // Accessors are required to have appropriate correct
  // permissions. Pointer can be a raw pointer or
  // shared_ptr.
  template <typename SrcAccessorT, typename DestPointerT>
  void copy(SrcAccessorT src, DestPointerT dest);

  template <typename SrcPointerT, typename DestAccessorT>
  void copy(SrcPointerT src, DestAccessorT dest);

  // Copy between accessors.
  // Accessors are required to have appropriate correct
  // permissions.
  template <typename SrcAccessorT, typename DestAccessorT>
  void copy(SrcAccessorT src, DestAccessorT dest);

  // Submit different forms of kernel for execution.
  template <typename KernelName, typename KernelType>
  void single_task(KernelType kernel);

  template <typename KernelName, typename KernelType,
      int Dims>
  void parallel_for(range<Dims> num_work_items,
                   KernelType kernel);

  template <typename KernelName, typename KernelType,int Dims>
  void parallel_for(nd_range<Dims> execution_range,
                   KernelType kernel);

  template <typename KernelName, typename KernelType, int Dims>
  void parallel_for_work_group(range<Dims> num_groups,
                       KernelType kernel);

  template <typename KernelName, typename KernelType, int Dims>
  void parallel_for_work_group(range<Dims> num_groups,
                       range<Dims> group_size,
                       KernelType kernel);
};
```

## Figure 2-19. Simplified definition of member functions in the handler class

## Chapter 2 Where Code Executes

In addition to calling members of the handler class to submit device code, there are also members of the queue class that allow work to be submitted. The queue class members shown in Figure 2-20 are shortcuts that simplify certain patterns, and we will see these shortcuts used in future chapters.

```cpp
class queue {
public:
  // Submit a memset operation writing to the specified
  // pointer. Return an event representing this operation.
  event memset(void* ptr, int value, size_t count);

  // Submit a memcpy operation copying from src to dest.
  // Return an event representing this operation.
  event memcpy(void* dest, const void* src, size_t count);

  // Submit different forms of kernel for execution.
  // Return an event representing the kernel operation.
  template <typename KernelName, typename KernelType>
  event single_task(KernelType kernel);

  template <typename KernelName, typename KernelType,
    int Dims>
  event parallel_for(range<Dims> num_work_items,
                   KernelType kernel);

  template <typename KernelName, typename KernelType,
    int Dims>
  event parallel_for(nd_range<Dims> execution_range,
                   KernelType kernel);

  // Submit different forms of kernel for execution.
  // Wait for the specified event(s) to complete
  // before executing the kernel.
  // Return an event representing the kernel operation.
  template <typename KernelName, typename KernelType>
  event single_task(const std::vector<event>& events,
                   KernelType kernel);

  template <typename KernelName, typename KernelType,
    int Dims>
  event parallel_for(range<Dims> num_work_items,
                   const std::vector<event>& events,
                   KernelType kernel);

  template <typename KernelName, typename KernelType,
    int Dims>
  event parallel_for(nd_range<Dims> execution_range,
                   const std::vector<event>& events,
                   KernelType kernel);
};
```

Figure 2-20. Simplified definition of member functions in the queue class that act as shorthand notation for equivalent functions in the handler class

## Actions

The code in Figure 2-18 contains a parallel\_for, which defines work to be performed on a device. The parallel\_for is within a command group (CG) submitted to a queue, and the queue defines the device on which the work is to be performed. Within the command group, there are two categories of code:

1. Host code that sets up dependences defining when it is safe for the runtime to start execution of the work defined in (2), such as creation of accessors to buffers (described in Chapter 3)

2. At most one call to an action that either queues device code for execution or performs a manual memory operation such as copy

The handler class contains a small set of member functions that define the action to be performed when a task graph node is executed. Figure 2-21 summarizes these actions.

<table><tr><td>Work Type</td><td>Actions (handler class methods)</td><td>Summary</td></tr><tr><td rowspan="2">Device code execution</td><td>single_task</td><td>Execute a single instance of a device function.</td></tr><tr><td>parallel_for</td><td>Multiple forms are available to launch device code with different combinations of work sizes.</td></tr><tr><td rowspan="3">Explicit memory operation</td><td>copy</td><td>Copy data between locations specified by accessor, pointer, and/or shared_ptr. The copy occurs as part of the SYCL task graph (described later), including dependence tracking.</td></tr><tr><td>update_host</td><td>Trigger update of host data backing of a buffer object.</td></tr><tr><td>fill</td><td>Initialize data in a buffer to a specified value.</td></tr></table>

Figure 2-21. Actions that invoke device code or perform explicit memory operations

At most one action from Figure 2-21 may be called within a command group (it is an error to call more than one), and only a single command group can be submitted to a queue per submit call. The result of this is that a single (or potentially no) operation from Figure 2-21 exists per task graph node, to be executed when the node dependences are met and the runtime determines that it is safe to execute.

## A command group must have at most one action within it, such as a kernel launch or explicit memory operation.

The idea that code is executed asynchronously in the future is the critical difference between code that runs on the CPU as part of the host program and device code that will run in the future when dependences are satisfied. A command group usually contains code from each category, with the code that defines dependences running as part of the host program (so that the runtime knows what the dependences are) and device code running in the future once the dependences are satisfied.

There are three classes of code in Figure 2-22:

1. Host code: Drives the application, including creating and managing data buffers and submitting work to queues to form new nodes in the task graph for asynchronous execution.

2. Host code within a command group: This code is run on the processor that the host code is executing on and executes immediately, before the submit call returns. This code sets up the node dependences by creating accessors, for example. Any arbitrary CPU code can execute here, but best practice is to restrict it to code that configures the node dependences.

3. An action: Any action listed in Figure 2-21 can be included in a command group, and it defines the work to be performed asynchronously in the future when node requirements are met (set up by (2)).

```cpp
#include <array>
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    constexpr int size = 16;
    std::array<int, size> data;
    buffer B{data};

    queue q{}; // Select any device for this queue

    std::cout << "Selected device is: "
        << q.get_device().get_info<info::device::name>()
        << "\n";

    q.submit([&](handler& h) {
        accessor acc{B, h};
        h.parallel_for(size,
                [=](auto& idx) { acc[idx] = idx; });
    });

    return 0;
}
```  
Figure 2-22. Submission of device code

To understand when code in an application will run, note that anything passed to an action listed in Figure 2-21 that initiates device code execution, or an explicit memory operation listed in Figure 2-21, will execute asynchronously in the future when the SYCL task graph (described later) node dependences have been satisfied. All other code runs as part of the host program immediately, as expected in typical C++ code.

It is important to note that although device code can start running (asynchronously) when task graph node dependences have been met, device code is not guaranteed to start running at that point. The only way to be sure that device code will start executing is to have the host program wait for (block on) results from the device code execution, through mechanisms such as host accessors or queue wait operations, which we cover in later chapters. Without such host blocking operations, the SYCL and lower-level runtimes make decisions on when to start execution of device code, possibly optimizing for objectives other than “run as soon as possible” such as optimizing for power or congestion.

## Host tasks

In general, the code executed by an action submitted to a queue (such as through parallel\_for) is device code, following a few language restrictions that allow it to run efficiently on many architectures. There is one important deviation, though, which is accessed through a handler method named host\_task. This method allows arbitrary C++ code to be submitted as an action in the task graph, to be executed on the host once any task graph dependences have been satisfied.

Host tasks are important in some programs for two reasons:

1. Arbitrary C++ can be included, even std::cout or printf. This can be important for easy debugging, interoperability with lower-level APIs such as OpenCL, or for incrementally enabling the use of accelerators in existing code.

2. Host tasks execute asynchronously as part of the task graph, instead of synchronously with the host program. Although a host program can launch additional threads or use other task parallelism approaches, host tasks integrate with the dependence tracking mechanisms of the SYCL runtime. This can be very convenient and may result in higher performance when device and host code need to be interspersed.

## Chapter 2 Where Code Executes

```cpp
#include <array>
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 4;

int main() {
    queue q;
    int* A = malloc_shared<int>(N, q);

    std::cout << "Selected device: "
                    << q.get_device().get_info<info::device::name>()
                    << "\n";

    // Initialize values in the shared allocation
    auto eA = q.submit([&](handler& h) {
        h.parallel_for(N, [=](auto& idx) { A[idx] = idx; });
    });

    // Use a host task to output values on the host as part of
    // task graph. depends_on is used to define a dependence
    // on previous device code having completed. Here the host
    // task is defined as a lambda expression.
    q.submit([&](handler& h) {
        h Robotts_on(eA);
        h.host_task([=]) {
            for (int i = 0; i < N; i++)
                std::cout << "host_task @ " << i << " = " << A[i]
                    << "\n";
        });
    });

    // Wait for work to be completed in the queue before
    // accessing the shared data in the host program.
    q.wait();

    for (int i = 0; i < N; i++)
        std::cout << "main @ " << i << " = " << A[i] << "\n";

    free(A, q);

    return 0;
}

Example Output:
Selected device: NVIDIA GeForce RTX 3060
host_task @ 0 = 0
host_task @ 1 = 1
host_task @ 2 = 2
host_task @ 3 = 3
main @ 0 = 0
main @ 1 = 1
main @ 2 = 2
main @ 3 = 3
```

## Figure 2-23. A simple host\_task

Figure 2-23 demonstrates a simple host task, which outputs text using std::cout when the task graph dependences have been met. Remember that the host task is executed asynchronously from the rest of the host program. This is a powerful part of the task graph mechanism in which the SYCL runtime schedules work when it is safe to do so, without interaction from the host program which may instead continue with other work. Also note that the code body of the host task does not need to follow any restrictions that are imposed on device code (described in Chapter 10).

The example in Figure 2-23 is based on events (described in Chapter 3) to create a dependence between the device code submission and a later host task, but host tasks can also be used with accessors (also covered in Chapter 3) through a special accessor template parameterization of target::host\_task (Chapter 7).

## Summary

In this chapter we provided an overview of queues, selection of the device with which a queue will be associated, and how to create custom device selectors. We also overviewed the code that executes on a device asynchronously when dependences are met vs. the code that executes as part of the C++ application host code. Chapter 3 describes how to control data movement.

## Chapter 2 Where Code Executes

![](images/bc70cb060227dfe782e8d94052f32fe1f5bc770f8b316db52f153067c6e93905.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter's Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter's Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Data Management

Supercomputer architects often lament the need to “feed the beast.” The phrase “feed the beast” refers to the “beast” of a computer we create when we use lots of parallelism and feeding data to it becomes a key challenge to solve.

Feeding a SYCL program on a heterogeneous machine requires some care to ensure data is where it needs to be when it needs to be there. In a large program, that can be a lot of work. In a preexisting C++ program, it can be a nightmare just to sort out how to manage all the data movements needed.

We will carefully explain the two ways to manage data: Unified Shared Memory (USM) and buffers. USM is pointer based, which is familiar to C++ programmers. Buffers offer a higher-level abstraction. Choice is good.

We need to control the movement of data, and this chapter covers options to do exactly that.

In Chapter 2, we studied how to control where code executes. Our code needs data as input and produces data as output. Since our code may run on multiple devices and those devices do not necessarily share memory, we need to manage data movement. Even when data is shared, such as with USM, synchronization and coherency are concepts we need to understand and manage.

A logical question might be “Why doesn’t the compiler just do everything automatically for us?” While a great deal can be handled for us automatically, performance is usually suboptimal if we do not assert ourselves as programmers. In practice, for best performance, we will need to concern ourselves with code placement (Chapter 2) and data movement (this chapter) when writing heterogeneous programs.

This chapter provides an overview of managing data, including controlling the ordering of data usage. It complements the prior chapter, which showed us how to control where code runs. This chapter helps us efficiently make our data appear where we have asked the code to run, which is important not only for correct execution of our application but also to minimize execution time and power consumption.

## Introduction

Compute is nothing without data. The whole point of accelerating a computation is to produce an answer more quickly. This means that one of the most important aspects of data-parallel computations is how they access data and introducing accelerator devices into a machine further complicates the picture. In traditional single-socket CPU-based systems, we have a single memory. Accelerator devices often have their own attached memories that cannot be directly accessed from the host. Consequently, parallel programming models that support discrete devices must provide mechanisms to manage these multiple memories and move data between them.

In this chapter, we present an overview of the various mechanisms for data management. We introduce Unified Shared Memory and the buffer abstractions for data management and describe the relationship between kernel execution and data movement.

## The Data Management Problem

Historically, one of the advantages of shared memory models for parallel programming is that they provide a single, shared view of memory. Having this single view of memory simplifies life. We are not required to do anything special to access memory from parallel tasks (aside from proper synchronization to avoid data races). While some types of accelerator devices (e.g., integrated GPUs) share memory with a host CPU, many discrete accelerators have their own local memories separate from that of the CPU as seen in Figure 3-1.

![](images/1e5067834aacf59a0e7ae8f662da0c96f61c1f62f6bf2a06745f2ac0bd28a6f9.jpg)  
Figure 3-1. Multiple discrete memories

## Device Local vs. Device Remote

Programs running on a device generally perform better when reading and writing data using memory attached directly to the device rather than remote memories. We refer to accesses to a directly attached memory as local accesses. Accesses to another device’s memory are remote accesses. Remote accesses tend to be slower than local accesses because they must travel over data links with lower bandwidth and/or higher latency. This means that it is often advantageous to colocate both a computation and the data that it will use. To accomplish this, we must somehow ensure that data is copied or migrated between different memories in order to move it closer to where computation occurs.

![](images/8c9cfa9d00cb04d710465d3e4b70e38ab9fc5b4bbe059f165a092733bbc1e079.jpg)  
Figure 3-2. Data movement and kernel execution

## Managing Multiple Memories

Managing multiple memories can be accomplished, broadly, in two ways: explicitly through our program or implicitly by the SYCL runtime library. Each method has its advantages and drawbacks, and we may choose one or the other depending on circumstances or personal preference.

## Explicit Data Movement

One option for managing multiple memories is to explicitly copy data between different memories. Figure 3-2 shows a system with a discrete accelerator where we must first copy any data that a kernel will require from the host memory to accelerator memory. After the kernel computes results, we must copy these results back to the host before the host program can use that data.

The primary advantage of explicit data movement is that we have full control over when data is transferred between different memories. This is important because overlapping computation with data transfer can be essential to obtain the best performance on some hardware.

The drawback of explicit data movement is that specifying all data movements can be tedious and error prone. Transferring an incorrect amount of data or not ensuring that all data has been transferred before a kernel begins computing can lead to incorrect results. Getting all of the data movement correct from the beginning can be a very timeconsuming task.

## Implicit Data Movement

The alternative to program-controlled explicit data movements are implicit data movements controlled by a parallel runtime or driver. In this case, instead of requiring explicit copies between different memories, the parallel runtime is responsible for ensuring that data is transferred to the appropriate memory before it is used.

The advantage of implicit data movement is that it requires less effort to get an application to take advantage of faster memory attached directly to the device. All the heavy lifting is done automatically by the runtime. This also reduces the opportunity to introduce errors into the program since the runtime will automatically identify both when data transfers must be performed and how much data must be transferred.

The drawback of implicit data movement is that we have less or no control over the behavior of the runtime’s implicit mechanisms. The runtime will provide functional correctness but may not move data in an optimal fashion that ensures maximal overlap of computation with data transfer, and this could have a negative impact on program performance.

## Selecting the Right Strategy

Picking the best strategy for a program can depend on many different factors. Different strategies might be appropriate for different phases of program development. We could even decide that the best solution is to mix and match the explicit and implicit methods for different pieces of the program. We might choose to begin using implicit data movement to simplify porting an application to a new device. As we begin tuning the application for performance, we might start replacing implicit

data movement with explicit in performance-critical parts of the code. Future chapters will cover how data transfers can be overlapped with computation in order to optimize performance.

## USM, Buffers, and Images

There are three abstractions for managing memory: Unified Shared Memory (USM), buffers, and images. USM is a pointer-based approach that should be familiar to C/C++ programmers. One advantage of USM is easier integration with existing C++ code that operates on pointers. Buffers, as represented by the buffer template class, describe one-, two-, or threedimensional arrays. They provide an abstract view of memory that can be accessed on either the host or a device. Buffers are not directly accessed by the program and are instead used through accessor objects. Images act as a special type of buffer that provides extra functionality specific to image processing. This functionality includes support for special image formats, reading of images using sampler objects, and more. Buffers and images are powerful abstractions that solve many problems but rewriting all interfaces in existing code to accept buffers or accessors can be time-consuming. Since the interface for buffers and images is largely the same, the rest of this chapter will only focus on USM and buffers.

## Unified Shared Memory

USM is one tool available to us for data management. USM is a pointerbased approach that should be familiar to C and C++ programmers who use malloc or new to allocate data. USM simplifies life when porting existing C/C++ code that makes heavy use of pointers. Devices that support USM support a unified virtual address space. Having a unified virtual address space means that any pointer value returned by a USM allocation routine on the host will be a valid pointer value on the device. We do not have to manually translate a host pointer to obtain the “device version”—we see the same pointer value on both the host and device.

A more detailed description of USM can be found in Chapter 6.
