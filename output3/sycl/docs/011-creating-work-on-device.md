
## Figure 2-16. Custom selector for a specific Intel Arria FPGA accelerator board

Chapter 12 has more discussion and examples for device selection and discusses the get\_info method in more depth.

## Creating Work on a Device

Applications usually contain a combination of both host code and device code. There are a few class members that allow us to submit device code for execution, and because these work dispatch constructs are the only way to submit device code, they allow us to easily distinguish device code from host code.

The remainder of this chapter introduces some of the work dispatch constructs, with the goal to help us understand and identify the division between device code and host code that executes natively on the host processor.

## Introducing the Task Graph

A fundamental concept in the SYCL execution model is a graph of nodes. Each node (unit of work) in this graph contains an action to be performed on a device, with the most common action being a data-parallel device kernel invocation. Figure 2-17 shows an example graph with four nodes, where each node can be thought of as a device kernel invocation.

![](images/a324a84517cf0d13e205f3ff0c987823eb9fea1666eb4663c54b8b3c94844a6c.jpg)  
Figure 2-17. The task graph defines actions to perform (asynchronously from the host program) on one or more devices and also dependences that determine when an action is safe to execute

The nodes in Figure 2-17 have dependence edges defining when it is legal for a node’s work to begin execution. The dependence edges are most commonly generated automatically from data dependences, although there are ways for us to manually add additional custom dependences when we want to. Node B in the graph, for example, has a dependence edge from node A. This edge means that node A must complete execution, and most likely (depending on specifics of the dependence) make generated data available on the device where node B will execute before node B’s action is started. The runtime controls resolution of dependences and triggering of node executions completely asynchronously from the

host program’s execution. The graph of nodes defining an application will be referred to in this book as the task graph and is covered in more detail in Chapter 3.

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
