# sycl Source Lines 1884-2427

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L1884-L2427

Citation: [sycl:L1884-L2427]

````text
## Accessing Memory Through Pointers

Since not all memories are created equal when a system contains both host memory and some number of device-attached local memories, USM defines three different types of allocations: device, host, and shared. All types of allocations are performed on the host. Figure 3-3 summarizes the characteristics of each allocation type.

<table><tr><td>Allocation Type</td><td>Description</td><td>Accessible on host?</td><td>Accessible on device?</td><td>Located on</td></tr><tr><td>device</td><td>Allocations in device memory</td><td>×</td><td>✓</td><td>device</td></tr><tr><td>host</td><td>Allocations in host memory</td><td>✓</td><td>✓</td><td>host</td></tr><tr><td>shared</td><td>Allocations shared between host and device</td><td>✓</td><td>✓</td><td>can migrate back and forth</td></tr></table>

Figure 3-3. USM allocation types

A device allocation occurs in device-attached memory. Such an allocation can be read from and written to on a device but is not directly accessible from the host. We must use explicit copy operations to move data between regular allocations in host memory and device allocations.

A host allocation occurs in host memory that is accessible both on the host and on a device. This means the same pointer value is valid both in host code and in device kernels. However, when such a pointer is accessed, the data always comes from host memory. If it is accessed on a device, the data does not migrate from the host to device-local memory. Instead, data is typically sent over a bus, such as PCI Express (PCI-E), that connects the device to the host.

A shared allocation is accessible on both the host and the device. In this regard, it is very similar to a host allocation, but it differs in that data can now migrate between host memory and device-local memory. This means that accesses on a device, after the migration has occurred, happen from much faster device-local memory instead of remotely accessing host memory though a higher-latency connection. Typically, this is accomplished through mechanisms inside the runtime and lower-level drivers that are hidden from us.

## USM and Data Movement

USM supports both explicit and implicit data movement strategies, and different allocation types map to different strategies. Device allocations require us to explicitly move data between host and device, while host and shared allocations provide implicit data movement.

## Explicit Data Movement in USM

Explicit data movement with USM is accomplished with device allocations and a special memcpy() found in the queue and handler classes. We enqueue memcpy() operations (actions) to transfer data either from the host to the device or from the device to the host.

Figure 3-4 contains one kernel that operates on a device allocation. Data is copied between host\_array and device\_array before and after the kernel executes using memcpy() operations. Calls to wait() on the queue ensure that the copy to the device has completed before the kernel executes and ensure that the kernel has completed before the data is copied back to the host. We will learn how we can eliminate these calls later in this chapter.

```cpp
#include <array>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    std::array<int, N> host_array;
    int *device_array = malloc_device<int>(N, q);

    for (int i = 0; i < N; i++) host_array[i] = N;

    // We will learn how to simplify this example later
    q.submit([&](handler &h) {
        // copy host_array to device_array
        hmemcpy(device_array, &host_array[0], N * sizeof(int));
    });
    q.wait();

    q.submit([&](handler &h) {
        h.parallel_for(N, [=](id<1> i) { device_array[i]++;
    });
    }
    q.wait();

    q.submit([&](handler &h) {
        // copy device_array back to host_array
        hmemcpy(&host_array[0], device_array, N * sizeof(int));
    });
    q.wait();

    free(device_array, q);
    return 0;
}
```

## Figure 3-4. USM explicit data movement

## Implicit Data Movement in USM

Implicit data movement with USM is accomplished with host and shared allocations. With these types of allocations, we do not need to explicitly insert copy operations to move data between host and device. Instead, we simply access the pointers inside a kernel, and any required data movement is performed automatically without programmer intervention (as long as your device supports these allocations). This greatly simplifies porting of existing codes: at most we need to simply replace any malloc or new with the appropriate USM allocation functions (as well as the calls to free to deallocate memory), and everything should just work.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;
    int *host_array = malloc_host<int>(N, q);
    int *shared_array = malloc_shared<int>(N, q);

    for (int i = 0; i < N; i++) {
        // Initialize host_array on host
        host_array[i] = i;
    }

    // We will learn how to simplify this example later
    q.submit([&](handler &h) {
        h.parallel_for(N, [=](id<1> i) {
            // access shared_array and host_array on device
            shared_array[i] = host_array[i] + 1;
        });
    });
    q.wait();

    for (int i = 0; i < N; i++) {
        // access shared_array on host
        host_array[i] = shared_array[i];
    }

    free(shared_array, q);
    free(host_array, q);
    return 0;
}
```

## Figure 3-5. USM implicit data movement

In Figure 3-5, we create two arrays, host\_array and shared\_array, that are host and shared allocations, respectively. While both host and shared allocations are directly accessible in host code, we only initialize host\_array here. Similarly, it can be directly accessed inside the kernel, performing remote reads of the data. The runtime ensures that shared\_ array is available on the device before the kernel accesses it and that it is moved back when it is later read by the host code, all without programmer intervention.

## Buffers

The other abstraction provided for data management is the buffer object. Buffers are a data abstraction that represent one or more objects of a given C++ type. Elements of a buffer object can be a scalar data type (such as an int, float, or double), a vector data type (Chapter 11), or a user-defined class or structure. SYCL 2020 defines a new notion, device copyable, that expands upon the notion of trivially copyable with additions to the set of permissible types. In particular, if the templated types in common C++ classes such as std::array, std::pair, std::tuple, or std::span are themselves device copyable, then those C++ class specializations built using those types are also device copyable. Take care that your data types are device copyable before using them with buffers!

While a buffer itself is a single object, the C++ type encapsulated by the buffer could be an array that contains multiple objects. Buffers represent data objects rather than specific memory addresses, so they cannot be directly accessed like regular C++ arrays. Indeed, a buffer object might map to multiple different memory locations on several different devices, or even on the same device, for performance reasons. Instead, we use accessor objects to read and write to buffers.

A more detailed description of buffers can be found in Chapter 7.

## Creating Buffers

Buffers can be created in a variety of ways. The simplest method is to simply construct a new buffer with a range that specifies the size of the buffer. However, creating a buffer in this fashion does not initialize its data, meaning that we must first initialize the buffer through other means before attempting to read useful data from it.

Buffers can also be created from existing data on the host. This is done by invoking one of the several constructors that take either a pointer to an existing host allocation, a set of InputIterators, or a container that has certain properties. Data is copied during buffer construction from the existing host allocation into the buffer object’s host memory. A buffer may also be created from a backend-specific object using SYCL interoperability features (e.g., from an OpenCL cl\_mem object). See the chapter on interoperability for more details on how to do this.

## Accessing Buffers

Buffers may not be directly accessed by the host and device (except through advanced and infrequently used mechanisms not described here). Instead, we must create accessors in order to read and write to buffers. Accessors provide the runtime with information about how we plan to use the data in buffers, allowing it to correctly schedule data movement.

```cpp
#include <array>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    std::array<int, N> my_data;
    for (int i = 0; i < N; i++) my_data[i] = 0;

    {
        queue q;
        buffer my_buffer(my_data);

        q.submit([&](handler &h) {
            // create an accessor to update
            // the buffer on the device
            accessor my_accessor(my_buffer, h);

            h.parallel_for(N, [=](id<1> i) { my_accessor[i]++;
        });

        // create host accessor
        host_accessor host_accessor(my_buffer);

        for (int i = 0; i < N; i++) {
            // access myBuffer on host
            std::cout << host_accessor[i] << " ";
        }
        std::cout << "\n";
    }

    // myData is updated when myBuffer is
    // destroyed upon exiting scope
    for (int i = 0; i < N; i++) {
        std::cout << my_data[i] << " ";
    }
    std::cout << "\n";
}
```  
Figure 3-6. Buffers and accessors

<table><tr><td>Access Mode</td><td>Description</td></tr><tr><td>read</td><td>Read-only access.</td></tr><tr><td>write</td><td>Write-only access.Previous contents are not discarded in case of partial writes.</td></tr><tr><td>read_write</td><td>Read and write access.</td></tr></table>

Figure 3-7. Buffer access modes

## Access Modes

When creating an accessor, we can inform the runtime how we are going to use it to provide more information for optimizations. We do this by specifying an access mode. Access modes are defined in the access\_mode enum class described in Figure 3-7. In the code example shown in Figure 3-6, the accessor my\_accessor is created with the default access mode, access\_mode::read\_write. This lets the runtime know that we intend to both read and write to the buffer through my\_accessor. Access modes are how the runtime is able to optimize implicit data movement. For example, access\_mode::read tells the runtime that the data needs to be available on the device before this kernel can begin executing. If a kernel only reads data through an accessor, there is no need to copy data back to the host after the kernel has completed as we haven’t modified it. Likewise, access\_mode::write lets the runtime know that we will modify the contents of a buffer and may need to copy the results back after computation has ended.

Creating accessors with the proper modes gives the runtime more information about how we use data in our program. The runtime uses accessors to order the uses of data, but it can also use this data to optimize scheduling of kernels and data movement. The access modes and optimization tags are described in greater detail in Chapter 7.

## Ordering the Uses of Data

Kernels can be viewed as asynchronous tasks that are submitted for execution. These tasks must be submitted to a queue where they are scheduled for execution on a device. In many cases, kernels must execute in a specific order so that the correct result is computed. If obtaining the correct result requires task A to execute before task B, we say that a dependence<sup>1</sup> exists between tasks A and B.

However, kernels are not the only form of task that must be scheduled. Any data that is accessed by a kernel needs to be available on the device before the kernel can start executing. These data dependences can create additional tasks in the form of data transfers from one device to another. Data transfer tasks may be either explicitly coded copy operations or more commonly implicit data movements performed by the runtime.

If we take all the tasks in a program and the dependences that exist between them, we can use this to visualize the information as a graph. This task graph is specifically a directed acyclic graph (DAG) where the nodes are the tasks and the edges are the dependences. The graph is directed because dependences are one-way: task A must happen before task B. The graph is acyclic because it cannot contain any cycles or paths from a node that lead back to itself.

In Figure 3-8, task A must execute before tasks B and C. Likewise, B and C must execute before task D. Since B and C do not have a dependence between each other, the runtime is free to execute them in any order (or even in parallel) as long as task A has already executed. Therefore, the possible legal orderings of this graph are $\mathtt { A } \Rightarrow \mathtt { B } \Rightarrow \mathtt { C } \Rightarrow \mathtt { D } , \mathtt { A } \Rightarrow \mathtt { C } \Rightarrow \mathtt { B } \Rightarrow \mathtt { D } _ { \mathtt { i } }$ and even $\mathsf { A } \Rightarrow \{ \mathsf { B } , \mathsf { C } \} \Rightarrow \mathsf { D } \ i \mathrm { f } \mathsf { B }$ and C can concurrently execute.

![](images/f79d9b3aeb8a782f9625c159d7c63dc2c6cb72921bbe0f6f754003146b23e7bd.jpg)  
Figure 3-8. Simple task graph

Tasks may have a dependence with a subset of all tasks. In these cases, we only want to specify the dependences that matter for correctness. This flexibility gives the runtime latitude to optimize the execution order of the task graph. In Figure 3-9, we extend the earlier task graph from Figure 3-8 to add tasks E and F where E must execute before F. However, tasks E and F have no dependences with nodes A, B, C, and D. This allows the runtime to choose from many possible legal orderings to execute all the tasks.

![](images/f5ab65a7225673e3393688ae7f6285c9676e598fe1372e6e662d4ec13fb9c765.jpg)  
Figure 3-9. Task graph with disjoint dependences

There are two different ways to model the execution of tasks, such as a launch of a kernel, in a queue: the queue could either execute tasks in the order of submission, or it could execute tasks in any order subject to any dependences that we define. There are several mechanisms for us to define the dependences needed for correct ordering.

## In-order Queues

The simplest option to order tasks is to submit them to an in-order queue object. An in-order queue executes tasks in the order in which they were submitted as seen in Figure 3-10. Their intuitive task ordering means that in-order queues an advantage of simplicity but a disadvantage of serializing tasks even if no dependences exist between independent tasks. In-order queues are useful when bringing up applications because they are simple, intuitive, deterministic on execution ordering, and suitable for many codes.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 4;

int main() {
    queue q{property::queue::in_order();

    q.submit([&](handler& h) {
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task A
    });
    q.submit([&](handler& h) {
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task B
    });
    q.submit([&](handler& h) {
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task C
    });

    return 0;
}
```

Figure 3-10. In-order queue usage

## Out-of-Order Queues

Since queue objects are out-of-order queues (unless created with the inorder queue property), they must provide ways to order tasks submitted to them. Queues order tasks by letting us inform the runtime of dependences between them. These dependences can be specified, either explicitly or implicitly, using command groups. We will consider them separately in the following sections.

A command group is an object that specifies a task and its dependences. Command groups are typically written as C++ lambda expressions passed as an argument to the submit() method of a queue object. This lambda’s only parameter is a reference to a handler object. The handler object is used inside the command group to specify actions, create accessors, and specify dependences.

## Explicit Dependences with Events

Explicit dependences between tasks look like the examples we have seen (Figure 3-8) where task A must execute before task B. Expressing dependences in this way focuses on explicit ordering based on the computations that occur rather than on the data accessed by the computations. Note that expressing dependences between computations is primarily relevant for codes that use USM since codes that use buffers express most dependences via accessors. In Figures 3-4 and 3-5, we simply tell the queue to wait for all previously submitted tasks to finish before we continue. Instead, we can express task dependences through event objects. When submitting a command group to a queue, the submit() method returns an event object. These events can then be used in two ways.

First, we can synchronize through the host by explicitly calling the wait() method on an event. This forces the runtime to wait for the task that generated the event to finish executing before host program execution may continue. Explicitly waiting on events can be very

useful for debugging an application but wait() can overly constrain the asynchronous execution of tasks since it halts all execution on the host thread. Similarly, one could also call wait() on a queue object, which would block execution on the host until all enqueued tasks have completed. This can be a useful tool if we do not want to keep track of all the events returned by enqueued tasks.

This brings us to the second way that events can be used. The handler class contains a method named depends\_on(). This method accepts either a single event or a vector of events and informs the runtime that the command group being submitted requires the specified events to complete before the action within the command group may execute. Figure 3-11 shows an example of how depends\_on() may be used to order tasks.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 4;

int main() {
    queue q;

    auto eA = q.submit([&](handler &h) {
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task A });
    });
    eA.wait();
    auto eB = q.submit([&](handler &h) {
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task B });
    });
    auto eC = q.submit([&](handler &h) {
        h Robot_on(eB);
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task C });
    });
    auto eD = q.submit([&](handler &h) {
        h Robot_on({eB, eC});
        h.parallel_for(N, [=](id<1> i) { /*...*/ }); // Task D });
    });

    return 0;
}
```  
Figure 3-11. Using events and depends\_on

## Implicit Dependences with Accessors

Implicit dependences between tasks are created from data dependences. Data dependences between tasks take three forms, shown in Figure 3-12.

<table><tr><td>Dependence Type</td><td>Description</td></tr><tr><td>Read-after-Write (RAW)</td><td>Occurs when task B needs to read data computed by task A.</td></tr><tr><td>Write-after-Read (WAR)</td><td>Occurs when task B writes over data after it has been read by task A.</td></tr><tr><td>Write-after-Write(WAW)</td><td>Occurs when task B also writes over data written by task A.</td></tr></table>

Figure 3-12. Three forms of data dependences

Data dependences are expressed to the runtime in two ways: accessors and program order. Both must be used for the runtime to properly compute data dependences. This is illustrated in Figures 3-13 and 3-14.

```cpp
#include <array>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    std::array<int, N> a, b, c;
    for (int i = 0; i < N; i++) {
        a[i] = b[i] = c[i] = 0;
    }

    queue q;

    // We will learn how to simplify this example later
    buffer a_buf{a};
    buffer b_buf{b};
    buffer c_buf{c};

    q.submit([&](handler &h) {
        accessor a(a_buf, h, read_only);
        accessor b(b_buf, h, write_only);
        h.parallel_for(  // computeB
            N, [=](id<1> i) { b[i] = a[i] + 1; });
    });

    q.submit([&](handler &h) {
        accessor a(a_buf, h, read_only);
        h.parallel_for(  // readA
            N, [=](id<1> i) {
                // Useful only as an example
                int data = a[i];
            });
    });

    q.submit([&](handler &h) {
        // RAW of buffer B
        accessor b(b_buf, h, read_only);
        accessor c(c_buf, h, write_only);
        h.parallel_for(  // computeC
            N, [=](id<1> i) { c[i] = b[i] + 2; });
    });

    // read C on host
    host_accessor host_acc_c(c_buf, read_only);
    for (int i = 0; i < N; i++) {
        std::cout << host_acc_c[i] << " ";
    }
    std::cout << "\n";
    return 0;
}
```

## Figure 3-13. Read-after-Write

![](images/ebf3f6db318ace3085343b892a454b38b3a47e5863dc7d4f5347611108f014c0.jpg)  
Figure 3-14. RAW task graph

In Figures 3-13 and 3-14, we execute three kernels—computeB, readA, and computeC—and then read the final result back on the host. The command group for kernel computeB creates two accessors, a and b. These accessors use access tags read\_only and write\_only for optimization to specify that we do not use the default access mode, access\_mode::read\_ write. We will learn more about access tags in Chapter 7. Kernel computeB reads buffer a\_buf and writes to buffer b\_buf. Buffer a\_buf must be copied from the host to the device before the kernel begins execution.

Kernel readA also creates a read-only accessor for buffer a\_buf. Since kernel readA is submitted after kernel computeB, this creates a Read-after-Read (RAR) scenario. However, RARs do not place extra restrictions on the runtime, and the kernels are free to execute in any order. Indeed, a runtime might prefer to execute kernel readA before kernel computeB or even execute both at the same time. Both require buffer a\_buf to be copied to the device, but kernel computeB also requires buffer b\_buf to be copied in case any existing values are not overwritten by computeB and which might be used by later kernels. This means that the runtime could execute kernel readA while the data transfer for buffer b\_buf occurs and also shows that

even if a kernel will only write to a buffer, the original content of the buffer may still be moved to the device because there is no guarantee that all values in the buffer will be written by a kernel (see Chapter 7 for tags that let us optimize in these cases).

Kernel computeC reads buffer b\_buf, which we computed in kernel computeB. Since we submitted kernel computeC after we submitted kernel computeB, this means that kernel computeC has a RAW data dependence on buffer b\_buf. RAW dependences are also called true dependences or flow dependences, as data needs to flow from one computation to another in order to compute the correct result. Finally, we also create a RAW dependence on buffer c\_buf between kernel computeC and the host since the host wants to read C after the kernel has finished. This forces the runtime to copy buffer c\_buf back to the host. Since there were no writes to buffer a\_buf on devices, the runtime does not need to copy that buffer back to the host because the host has an up-to-date copy already.

```cpp
#include <array>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    std::array<int, N> a, b;
    for (int i = 0; i < N; i++) {
        a[i] = b[i] = 0;
    }

    queue q;
    buffer a_buf{a};
    buffer b_buf{b};

    q.submit([&](handler &h) {
        accessor a(a_buf, h, read_only);
        accessor b(b_buf, h, write_only);
        h.parallel_for(  // computeB
            N, [=](id<1> i) { b[i] = a[i] + 1; });
    });

    q.submit([&](handler &h) {
        // WAR of buffer A
        accessor a(a_buf, h, write_only);
        h.parallel_for(  // rewriteA
            N, [=](id<1> i) { a[i] = 21 + 21; });
    });

    q.submit([&](handler &h) {
        // WAW of buffer B
        accessor b(b_buf, h, write_only);
        h.parallel_for(  // rewriteB
            N, [=](id<1> i) { b[i] = 30 + 12; });
    });

    host_accessor host_acc_a(a_buf, read_only);
    host_accessor host_acc_b(b_buf, read_only);
    for (int i = 0; i < N; i++) {
        std::cout << host_acc_a[i] << " " << host_acc_b[i]
            << " ";
    }
    std::cout << "\n";
    return 0;
}
```

Figure 3-15. Write-after-Read and Write-after-Write

![](images/ee94aad66b9d15de1130168a5cb7ab9bd4f5aa4c383df728af45b5ca8cb35f1e.jpg)  
Figure 3-16. WAR and WAW task graph

In Figures 3-15 and 3-16, we again execute three kernels: computeB, rewriteA, and rewriteB. Kernel computeB once again reads buffer a\_buf and writes to buffer b\_buf, kernel rewriteA writes to buffer a\_buf, and kernel rewriteB writes to buffer b\_buf. Kernel rewriteA could theoretically execute earlier than kernel computeB since less data needs to be transferred before the kernel is ready, but it must wait until after kernel computeB finishes since there is a WAR dependence on buffer a\_buf.

In this example, kernel computeB requires the original value of A from the host, and it would read the wrong values if kernel rewriteA executed before kernel computeB. WAR dependences are also called antidependences. RAW dependences ensure that data properly flows in the correct direction, while WAR dependences ensure existing values are not overwritten before they are read. The WAW dependence on buffer b\_buf found in kernel rewrite functions similarly. If there were any reads of buffer b\_buf submitted in between kernels computeB and rewriteB, they would result in RAW and WAR dependences that would properly order the tasks. However, there is an implicit dependence between kernel rewriteB and the host in this example since the final data must be written back to the host. We will learn more about what causes this writeback in Chapter 7. The WAW dependence, also called an output dependence, ensures that the final output will be correct on the host.

# Choosing a Data Management Strategy

Selecting the right data management strategy for our applications is largely a matter of personal preference. Indeed, we may begin with one strategy and switch to another as our program matures. However, there are a few useful guidelines to help us to pick a strategy that will serve our needs.

The first decision to make is whether we want to use explicit or implicit data movement since this greatly affects what we need to do to our program. Implicit data movement is generally an easier place to start because all the data movement is handled for us, letting us focus on expression of the computation.

If we decide that we’d rather have full control over all data movement from the beginning, then explicit data movement using USM device allocations is where we want to start. We just need to be sure to add all the necessary copies between host and devices!

When selecting an implicit data movement strategy, we still have a choice of whether to use buffers or USM host or shared pointers. Again, this choice is a matter of personal preference, but there are a few questions that could help guide us to one over the other. If we’re porting an existing C/C++ program that uses pointers, USM might be an easier path since most code won’t need to change. If data representation hasn’t guided us to a preference, another question we can ask is how we would like to express our dependences between kernels. If we prefer to think about data dependences between kernels, choose buffers. If we prefer to think about dependences as performing one computation before another and want to express that using an in-order queue or with explicit events or waiting between kernels, choose USM.

When using USM pointers (with either explicit or implicit data movement), we have a choice of which type of queue we want to use. Inorder queues are simple and intuitive, but they constrain the runtime and may limit performance. Out-of-order queues are more complex, but they give the runtime more freedom to reorder and overlap execution. The outof-order queue class is the right choice if our program will have complex dependences between kernels. If our program simply runs many kernels one after another, then an in-order queue will be a better option for us.

## Handler Class: Key Members

We have shown a number of ways to use the handler class. Figures 3-17 and 3-18 provide a more detailed explanation of the key members of this very important class. We have not yet used all these members, but they will be used later in the book. This is as good a place as any to lay them out.

A closely related class, the queue class, is similarly explained at the end of Chapter 2.

## Chapter 3 Data Managem ent

```cpp
class handler {
    ...
        // Specifies event(s) that must be complete before the
        // action defined in this command group executes.
        void depends_on({event / std::vector<event> & });

    // Enqueues a memcpy from Src to Dest.
    // Count bytes are copied.
    void memcpy(void* Dest, const void* Src, size_t Count);

    // Enqueues a memcpy from Src to Dest.
    // Count elements are copied.
    template <typename T>
    void copy(const T* Src, T* Dest, size_t Count);

    // Enqueues a memset operation on the specified pointer.
    // Writes the first byte of Value into Count bytes.
    void memset(void* Ptr, int Value, size_t Count)

        // Enques a fill operation on the specified pointer.
        // Fills Pattern into Ptr Count times.
        template <typename T>
        void fill(void* Ptr, const T& Pattern, size_t Count);

    // Submits a kernel of one work-item for execution.
    template <typename KernelName, typename KernelType>
    void single_task(KernelType KernelFunc);

    // Submits a kernel with NumWork-items work-items for
    // execution.
    template <typename KernelName, typename KernelType,
            int Dims>
    void parallel_for(range<Dims> NumWork - items,
            KernelType KernelFunc);

    // Submits a kernel for execution over the supplied
    // nd_range.
    template <typename KernelName, typename KernelType,
            int Dims>
    void parallel_for(nd_range<Dims> ExecutionRange,
            KernelType KernelFunc);
    ...
};
```

## Figure 3-17. Simplified definition of the non-accessor members of the handler class

```cpp
class handler {
...
// Specifies event(s) that must be complete before the
// action. Copy to/from an accessor.
// Valid combinations:
// Src: accessor,   Dest: shared_ptr
// Src: accessor,   Dest: pointer
// Src: shared_ptr  Dest: accessor
// Src: pointer      Dest: accessor
// Src: accessor   Dest: accessor
template <typename T_Src, typename T_Dst, int Dims,
       access::mode AccessMode,
       access::target AccessTarget,
       access::placeholder IsPlaceholder =
         access::placeholder::false_t>
void copy(accessor<T_Src, Dims, AccessMode,
           AccessTarget, IsPlaceholder> Src,
       shared_ptr_class<T_Dst> Dst);
void copy(shared_ptr_class<T_Src> Src,
       accessor<T_Dst, Dims, AccessMode, AccessTarget,
           IsPlaceholder>
           Dst);
void copy(accessor<T_Src, Dims, AccessMode, AccessTarget,
           IsPlaceholder> Src,
       T_Dst *Dst);
void copy(const T_Src *Src,
       accessor<T_Dst, Dims, AccessMode, AccessTarget,
           IsPlaceholder> Dst);
template <typename T_Src, int Dims_Src,
       access::mode AccessMode_Src,
       access::target AccessTarget_Src, typename T_Dst,
       int Dims_Dst, access::mode AccessMode_Dst,
       access::target AccessTarget_Dst,
       access::placeholder IsPlaceholder_Src =
          access::placeholder::false_t,
       access::placeholder IsPlaceholder_Dst =
          access::placeholder::false_t>
void copy(accessor<T_Src, Dims_Src, AccessMode_Src,
           AccessTarget_Src, IsPlaceholder_Src> Src,
       accessor<T_Dst, Dims_Dst, AccessMode_Dst,
           AccessTarget_Dst, IsPlaceholder_Dst> Dst);

// Provides a guarantee that the memory object accessed by
// the accessor is updated on the host after this action
// executes.
template <typename T, int Dims, access::mode AccessMode,
       access::target AccessTarget,
       access::placeholder IsPlaceholder =
         access::placeholder::false_t>
void update_host(accessor<T, Dims, AccessMode,
               AccessTarget, IsPlaceholder> Acc);
...
```

Figure 3-18. Simplified definition of the accessor members of the handler class

## Summary

In this chapter, we have introduced the mechanisms that address the problems of data management and how to order the uses of data. Managing access to different memories is a key challenge when using accelerator devices, and we have different options to suit our needs.

We provided an overview of the different types of dependences that can exist between the uses of data, and we described how to provide information about these dependences to queues so that they properly order tasks.

This chapter provided an overview of Unified Shared Memory and buffers. We explore all the modes and behaviors of USM in greater detail in Chapter 6. Chapter 7 explores buffers more deeply, including all the different ways to create buffers and control their behavior. Chapter 8 revisits the scheduling mechanisms for queues that control the ordering of kernel executions and data movements.

![](images/cf2dc683e61d8404c18cd191b29a9ff1f49210d0cceadb4df8a82dad8d009983.jpg)

Open Access This chapter is licensed under the terms of the Creative Commons Attribution 4.0 International License

(https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
