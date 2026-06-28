
In this chapter, we have learned about buffers and accessors. Buffers are an abstraction of data that hides the underlying details of memory management from the programmer. They do this in order to provide a simpler, higher-level abstraction. We went through several examples that showed us the different ways to construct buffers as well as the different optional properties that can be specified to alter their behavior. We learned how to initialize a buffer with data from host memory as well as how to write data back to host memory when we are done with a buffer.

Since we cannot access buffers directly, we learned how to access the data in a buffer by using accessor objects. We learned the difference between device accessors and host accessors. We discussed the different access modes and targets and how they inform the runtime how and where an accessor will be used by the program. We showed the simplest way to use accessors using the default access modes and targets, and we learned how to distinguish between a placeholder accessor and one that is not. We then saw how to further optimize the example program by giving the runtime more information about our accessor usage by adding deduction tags to our accessor declarations. Finally, we covered many of the different ways that accessors can be used in a program.

In the next chapter, we will learn in greater detail how the runtime can use the information we give it through accessors to schedule the execution of different kernels. We will also see how this information informs the runtime about when and how the data in buffers needs to be copied between the host and a device. We will learn how we can explicitly control data movement involving buffers—and USM allocations too.

![](images/a0be8fdb8b600de904d36c20e21c705fedefa87101b252b4f9a77cd47e91ba09.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Scheduling Kernels and Data Movement

We need to discuss our role as the conductor for our parallel programs. The proper orchestration of a parallel program is a thing of beauty—code running full speed without waiting for data, because we have arranged for all data to arrive and depart at the proper times—code carefully constructed to keep the hardware maximally busy. It is the thing that dreams are made of!

Life in the fast lanes—not just one lane!—demands that we take our work as the conductor seriously. In order to do that, we can think of our job in terms of task graphs.

Therefore, in this chapter, we will cover task graphs, the mechanism that is used to run complex sequences of kernels correctly and efficiently. There are two things that need sequencing in an application: kernel executions and data movement. Task graphs are the mechanism that we use to achieve proper sequencing.

First, we will quickly review how we can use dependences to order tasks from Chapter 3. Next, we will cover how the SYCL runtime builds graphs. We will discuss the basic building block of SYCL graphs, the command group. We will then illustrate the different ways we can build graphs of common patterns. We will also discuss how data movement, both explicit and implicit, is represented in graphs. Finally, we will discuss the various ways to synchronize our graphs with the host.

# What Is Graph Scheduling?

In Chapter 3, we discussed data management and ordering the uses of data. That chapter described the key abstraction behind graphs in SYCL: dependences. Dependences between kernels are fundamentally based on what data a kernel accesses. A kernel needs to be certain that it reads the correct data before it can compute its output.

We described the three types of data dependences that are important for ensuring correct execution. The first, Read-after-Write (RAW), occurs when one task needs to read data produced by a different task. This type of dependence describes the flow of data between two kernels. The second type of dependence happens when one task needs to update data after another task has read it. We call that type of dependence a Write-after-Read (WAR) dependence. The final type of data dependence occurs when two tasks try to write the same data. This is known as a Write-after-Write (WAW) dependence.

Data dependences are the building blocks we will use to build graphs. This set of dependences is all we need to express both simple linear chains of kernels and large, complex graphs with hundreds of kernels with elaborate dependences. No matter which types of graph a computation needs, SYCL graphs ensure that a program will execute correctly based on the expressed dependences. However, it is up to the programmer to make sure that a graph correctly expresses all the dependences in a program.

## How Graphs Work in SYCL

A command group can contain three different things: an action, its dependences, and miscellaneous host code. Of these three things, the one that is always required is the action, since without it the command group really doesn’t do anything. Most command groups will also express dependences, but there are cases where they may not. One such example is the first action submitted in a program. It does not depend on anything to begin execution; therefore, we would not specify any dependence. The other thing that can appear inside a command group is arbitrary C++ code that executes on the host. This is perfectly legal and can be useful to help specify the action or its dependences, and this code is executed while the command group is created (not later, when the action is performed based on dependences having been met).

Command groups are typically expressed as a C++ lambda expression passed to the submit method. Command groups can also be expressed through shortcut methods on queue objects that take a kernel and set of event-based dependences.

## Command Group Actions

There are two types of actions that may be performed by a command group: kernel executions and explicit memory operations. A command group may only perform a single action. As we’ve seen in earlier chapters, kernels are defined through calls to a parallel\_for or single\_task method and express computations that we want to perform on our devices. Operations for explicit data movement are the second type of action. Examples from USM include memcpy, memset, and fill operations. Examples from buffers include copy, fill, and update\_host.

## How Command Groups Declare Dependences

The other main component of a command group is the set of dependences that must be satisfied before the action defined by the group can execute. SYCL allows these dependences to be specified in several ways.

If a program uses in-order SYCL queues, the in-order semantics of the queue specify implicit dependences between successively enqueued command groups. One task cannot execute until the previously submitted task has completed.

Event-based dependences are another way to specify what must be complete before a command group may execute. These event-based dependences may be specified in two styles. The first way is used when a command group is specified as a lambda passed to a queue’s submit method. In this case, the programmer invokes the depends\_on method of the command group handler object, passing either an event or vector of events as parameter. The other way is used when a command group is created from the shortcut methods defined on the queue object. When the programmer directly invokes parallel\_for or single\_task on a queue, an event or vector of events may be passed as an extra parameter.

The last way that dependences may be specified is through the creation of accessor objects. Accessors specify how they will be used to read or write data in a buffer object, letting the runtime use this information to determine the data dependences that exist between different kernels. As we reviewed in the beginning of this chapter, examples of data dependences include one kernel reading data that another produces, two kernels writing the same data, or one kernel modifying data after another kernel reads it.

## Examples

Now we will illustrate everything we’ve just learned with several examples. We will present how one might express two different dependence patterns in several ways. The two patterns we will illustrate are linear dependence chains where one task executes after another and a “Y” pattern where two independent tasks must execute before successive tasks.

Graphs for these dependence patterns can be seen in Figures 8-1 and 8-2. Figure 8-1 depicts a linear dependence chain. The first node represents the initialization of data, while the second node presents the reduction operation that will accumulate the data into a single result. Figure 8-2 depicts a “Y” pattern where we independently initialize two different pieces of data. After the data is initialized, an addition kernel will sum the two vectors together. Finally, the last node in the graph accumulates the result into a single value.

![](images/c3836e3c0ce1824411dded9fadf681f62a8d85617f398c432855e062f88b6041.jpg)  
Figure 8-1. Linear dependence chain graph

![](images/651c0870b541a5742637b1a3c7446fa081577bdf663840f852aa06c08e232d2e.jpg)  
Figure 8-2. ${ } ^ { \prime \prime } Y ^ { \prime \prime }$ pattern dependence graph

For each pattern, we will show three different implementations. The first implementation will use in-order queues. The second will use event-based dependences. The last implementation will use buffers and accessors to express data dependences between command groups.

Figure 8-3 shows how to express a linear dependence chain using in-order queues. This example is very simple because the semantics of inorder queues already guarantee a sequential order of execution between command groups. The first kernel we submit initializes the elements of

an array to 1. The next kernel then takes those elements and sums them together into the first element. Since our queue is in order, we do not need to do anything else to express that the second kernel should not execute until the first kernel has completed. Finally, we wait for the queue to finish executing all its tasks, and we check that we obtained the expected result.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q{property::queue::in_order()};

    int *data = malloc_shared<int>(N, q);

    q.parallel_for(N, [=](id<1> i) { data[i] = 1; });

    q.single_task([=]) {
        for (int i = 1; i < N; i++) data[0] += data[i];
    });
    q.wait();

    assert(data[0] == N);
    return 0;
}
```

## Figure 8-3. Linear dependence chain with in-order queues

Figure 8-4 shows the same example using an out-of-order queue and event-based dependences. Here, we capture the event returned by the first call to parallel\_for. The second kernel is then able to specify a dependence on that event and the kernel execution it represents by passing it as a parameter to depends\_on. We will see in Figure 8-6 how we could shorten the expression of the second kernel using one of the shortcut methods for defining kernels.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    int *data = malloc_shared<int>(N, q);

    auto e = q.parallel_for(N, [=](id<1> i) { data[i] = 1; });

    q.submit([&](handler &h) {
        h RobotOn(e);
        hingle_task([=]) {
            for (int i = 1; i < N; i++) data[0] += data[i];
        });
    });
    q.wait();

    assert(data[0] == N);
    return 0;
}
```

## Figure 8-4. Linear dependence chain with events

Figure 8-5 rewrites our linear dependence chain example using buffers and accessors instead of USM pointers. Here we once again use an outof-order queue but use data dependences specified through accessors instead of event-based dependences to order the execution of the command groups. The second kernel reads the data produced by the first kernel, and the runtime can see this because we declare accessors based on the same underlying buffer object. Unlike the previous examples, we do not wait for the queue to finish executing all its tasks. Instead, we construct a host accessor that defines a data dependence between the output of the second kernel and our assertion that we computed the correct answer on the host. Note that while a host accessor gives us an up-to-date view of data on the host, it does not guarantee that the original host memory has been updated if any was specified when the buffer was created. We can’t

safely access the original host memory unless the buffer is first destroyed or unless we use a more advanced mechanism like the mutex mechanism described in Chapter 7.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    buffer<int> data{range{N}};

    q.submit([&](handler &h) {
        accessor a{data, h};
        h.parallel_for(N, [=](id<1> i) { a[i] = 1; });
    });

    q.submit([&](handler &h) {
        accessor a{data, h};
        h.single_task([=]) {
            for (int i = 1; i < N; i++) a[0] += a[i];
        });
    });

    host_accessor h_a{data};
    assert(h_a[0] == N);
    return 0;
}
```

## Figure 8-5. Linear dependence chain with buffers and accessors

Figure 8-6 shows how to express a “Y” pattern using in-order queues. In this example, we declare two arrays, data1 and data2. We then define two kernels that will each initialize one of the arrays. These kernels do not depend on each other, but because the queue is in order, the kernels must execute one after the other. Note that it would be perfectly legal to swap the order of these two kernels in this example. After the second kernel has executed, the third kernel adds the elements of the second array to those of the first array. The final kernel sums up the elements of the first array to compute the same result we did in our examples for linear dependence chains. This summation kernel depends on the previous kernel, but this linear chain is also captured by the in-order queue. Finally, we wait for all kernels to complete and validate that we successfully computed our magic number.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q{property::queue::in_order Due};

    int *data1 = malloc_shared<int>(N, q);
    int *data2 = malloc_shared<int>(N, q);

    q.parallel_for(N, [=](id<1> i) { data1[i] = 1; });

    q.parallel_for(N, [=](id<1> i) { data2[i] = 2; });

    q.parallel_for(N, [=](id<1> i) { data1[i] += data2[i]; });

    q.single_task([=]) {
        for (int i = 1; i < N; i++) data1[0] += data1[i];

        data1[0] /= 3;
    });
    q.wait();

    assert(data1[0] == N);
    return 0;
}
```

## Figure 8-6. “Y” pattern with in-order queues

Figure 8-7 shows our “Y” pattern example with out-of-order queues instead of in-order queues. Since the dependences are no longer implicit due to the order of the queue, we must explicitly specify the dependences between command groups using events. As in Figure 8-6, we begin by defining two independent kernels that have no initial dependences. We represent these kernels by two events, e1 and e2. When we define our third kernel, we must specify that it depends on the first two kernels.

We do this by saying that it depends on events e1 and e2 to complete before it may execute. However, in this example, we use a shortcut form to specify these dependences instead of the handler’s depends\_on method. Here, we pass the events as an extra parameter to parallel\_for. Since we want to pass multiple events at once, we use the form that accepts a std::vector of events, but luckily modern C++ simplifies this for us by automatically converting the expression {e1, e2} into the appropriate vector.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    int *data1 = malloc_shared<int>(N, q);
    int *data2 = malloc_shared<int>(N, q);

    auto e1 =
        q.parallel_for(N, [=](id<1> i) { data1[i] = 1; });

    auto e2 =
        q.parallel_for(N, [=](id<1> i) { data2[i] = 2; });

    auto e3 = q.parallel_for(
        range{N}, {e1, e2},
        [=](id<1> i) { data1[i] += data2[i]; });

    q.single_task(e3, [=]() {
        for (int i = 1; i < N; i++) data1[0] += data1[i];

        data1[0] /= 3;
    });
    q.wait();

    assert(data1[0] == N);
    return 0;
}
```

Figure 8-7. “Y” pattern with events

In our final example, seen in Figure 8-8, we again replace USM pointers and events with buffers and accessors. This example represents the two arrays data1 and data2 as buffer objects. Our kernels no longer use the shortcut methods for defining kernels since we must associate accessors with a command group handler. Once again, the third kernel must capture the dependence on the first two kernels. Here this is accomplished by declaring accessors for our buffers. Since we have previously declared accessors for these buffers, the runtime is able to properly order the execution of these kernels. Additionally, we also provide extra information to the runtime here when we declare accessor b. We add the access tag read\_only to let the runtime know that we’re only going to read this data, not produce new values. As we saw in our buffer and accessor example for linear dependence chains, our final kernel orders itself by updating the values produced in the third kernel. We retrieve the final value of our computation by declaring a host accessor that will wait for the final kernel to finish executing before moving the data back to the host where we can read it and assert we computed the correct result.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    buffer<int> data1{range{N}};
    buffer<int> data2{range{N}};

    q.submit([&](handler &h) {
        accessor a{data1, h};
        h.parallel_for(N, [=](id<1> i) { a[i] = 1; });
    });

    q.submit([&](handler &h) {
        accessor b{data2, h};
        h.parallel_for(N, [=](id<1> i) { b[i] = 2; });
    });

    q.submit([&](handler &h) {
        accessor a{data1, h};
        accessor b{data2, h, read_only};
        h.parallel_for(N, [=](id<1> i) { a[i] += b[i]; });
    });

    q.submit([&](handler &h) {
        accessor a{data1, h};
        h.single_task([=]) {
            for (int i = 1; i < N; i++) a[0] += a[i];

            a[0] /= 3;
        });
    });

    host_accessor h_a{data1};
    assert(h_a[0] == N);
    return 0;
}
```

# When Are the Parts of a Command Group Executed?

Since task graphs are asynchronous, it makes sense to wonder when exactly command groups are executed. By now, it should be clear that kernels may be executed as soon as their dependences have been satisfied, but what happens with the host portion of a command group?

When a command group is submitted to a queue, it is executed immediately on the host (before the submit call returns). This host portion of the command group is executed only once. Any kernel or explicit data operation defined in the command group is enqueued for execution on the device.

## Data Movement

Data movement is another very important aspect of graphs in SYCL that is essential for understanding application performance. However, it can often be accidentally overlooked if data movement happens implicitly in a program, either using buffers and accessors or using USM shared allocations. Next, we will examine the different ways that data movement can affect graph execution in SYCL.

## Explicit Data Movement

Explicit data movement has the advantage that it appears explicitly in a graph, making it obvious to programmers what goes on within execution of a graph. We will separate explicit data operations into those for USM and those for buffers.

As we learned in Chapter 6, explicit data movement in USM occurs when we need to copy data between device allocations and the host. This is done with the memcpy method, found in both the queue and handler classes. Submitting the action or command group returns an event that can be used to order the copy with other command groups.

Explicit data movement with buffers occurs by invoking either the copy or update\_host method of the command group handler object. The copy method can be used to manually exchange data between host memory and an accessor object on a device. This can be done for a variety of reasons. A simple example is checkpointing a long-running sequence of computations. With the copy method, data can be written from the device to arbitrary host memory in a one-way fashion. If this were done using buffers, most cases (i.e., those where the buffer was not created with use host\_ptr) would require the data to first be copied to the host and then from the buffer’s memory to the desired host memory.

The update\_host method is a very specialized form of copy. If a buffer was created around a host pointer, this method will copy the data represented by the accessor back to the original host memory. This can be useful if a program manually synchronizes host data with a buffer that was created with the special use\_mutex property. However, this use case is not likely to occur in most programs.

## Implicit Data Movement

Implicit data movement can have hidden consequences for command groups and task graphs in SYCL. With implicit data movement, data is copied between host and device either by the SYCL runtime or by some combination of hardware and software. In either case, copying occurs without explicit input from the user. Let’s again look separately at the USM and buffer cases.

With USM, implicit data movement occurs with host and shared allocations. As we learned in Chapter 6, host allocations do not really move data so much as access it remotely, and shared allocations may migrate between host and device. Since this migration happens automatically, there is really nothing to think about with USM implicit data movement and command groups. However, there are some nuances with shared allocations worth keeping in mind.

The prefetch operation works in a similar fashion to memcpy in order to let the runtime begin migrating shared allocations before a kernel attempts to use them. However, unlike memcpy where data must be copied in order to ensure correct results, prefetches are often treated as hints to the runtime to increase performance, and prefetches do not invalidate pointer values in memory (as a copy would when copying to a new address range). The program will still execute correctly if a prefetch has not completed before a kernel begins executing, and so many codes may choose to make command groups in a graph not depend on prefetch operations since they are not a functional requirement.

Buffers also carry some nuance. When using buffers, command groups must construct accessors for buffers that specify how the data will be used. These data dependences express the ordering between different command groups and allow us to construct task graphs. However, command groups with buffers sometimes fill another purpose: they specify the requirements on data movement.

Accessors specify that a kernel will read or write to a buffer. The corollary from this is that the data must also be available on the device, and if it is not, the runtime must move it there before the kernel may begin executing. Consequently, the SYCL runtime must keep track of where the current version of a buffer resides so that data movement operations can be scheduled. Accessor creation effectively creates an extra, hidden node in the graph. If data movement is necessary, the runtime must perform it first. Only then may the kernel being submitted execute.

Let us take another look at Figure 8-8. In this example, our first two kernels will require buffers data1 and data2 to be copied to the device; the runtime implicitly creates extra graph nodes to perform the data movement. When the third kernel’s command group is submitted, it is likely that these buffers will still be on the device, so the runtime will not need to perform any extra data movement. The fourth kernel’s data is also likely to not require any extra data movement, but the creation of the host accessor requires the runtime to schedule a movement of buffer data1 back to the host before the accessor is available for use.

## Synchronizing with the Host

The last topic we will discuss is how to synchronize graph execution with the host. We have already touched on this throughout the chapter, but we will now examine all the different ways a program can do this.

The first method for host synchronization is one we’ve used in many of our previous examples: waiting on a queue. Queue objects have two methods, wait and wait\_and\_throw, that block host execution until every command group that was submitted to the queue has completed. This is a very simple method that handles many common cases. However, it is worth pointing out that this method is very coarse-grained. If finergrained synchronization is desired (to possibly improve performance, for example), one of the other approaches we will discuss may be better suit an application’s needs.

The next method for host synchronization is to synchronize on events. This gives more flexibility over synchronizing on a queue since it lets an application only synchronize on specific actions or command groups. This is done by either invoking the wait method on an event or invoking the static method wait on the event class, which can accept a vector of events.

We have seen the next method used in Figures 8-5 and 8-8: host accessors. Host accessors perform two functions. First, they make data available for access on the host, as their name implies. Second, they synchronize the device and the host by defining a new dependence between the currently accessing graph and the host. This ensures that the data that gets copied back to the host has the correct value of the computation the graph was performing. However, we once again note that if the buffer was constructed from existing host memory, this original memory is not guaranteed to contain the updated values.

Note that host accessors are blocking. Execution on the host may not proceed past the creation of the host accessor until the data is available. Likewise, a buffer cannot be used on a device while a host accessor exists and keeps its data available. A common pattern is to create host accessors inside additional C++ scopes in order to free the data once the host accessor is no longer needed. This is an example of the next method for host synchronization.

Certain objects in SYCL have special behaviors when they are destroyed, and their destructors are invoked. We just learned how host accessors can make data remain on the host until they are destroyed. Buffers and images also have special behavior when they are destroyed or leave scope. When a buffer is destroyed, it waits for all command groups that use that buffer to finish execution. Once a buffer is no longer being used by any kernel or memory operation, the runtime may have to copy data back to the host. This copy occurs either if the buffer was initialized with a host pointer or if a host pointer was passed to the method set\_ final\_data. The runtime will then copy back the data for that buffer and update the host pointer before the object is destroyed.

The final option for synchronizing with the host involves an uncommon feature first described in Chapter 7. Recall that the constructors for buffer objects optionally take a property list. One of the valid properties that may be passed when creating a buffer is use\_mutex. When a buffer is created in this fashion, it adds the requirement that the memory owned by the buffer can be shared with the host application. Access to this memory is governed by the mutex used to initialize the buffer. The host is able to obtain the lock on the mutex when it is safe to access the memory shared with the buffer. If the lock cannot be obtained, the user may need to enqueue memory movement operations to synchronize the data with the host. This use is very specialized and unlikely to be found in the majority of DPC++ applications.

## Summary

In this chapter, we have learned about graphs and how they are built, scheduled, and executed in SYCL. We went into detail on what command groups are and what function they serve. We discussed the three things that can be within a command group: dependences, an action, and miscellaneous host code. We reviewed how to specify dependences between tasks using events as well as through data dependences described by accessors. We learned that the single action in a command group may be either a kernel or an explicit memory operation, and we then looked at several examples that showed the different ways we can construct common execution graph patterns. Next, we reviewed how data movement is an important part of SYCL graphs, and we learned how it can appear either explicitly or implicitly in a graph. Finally, we looked at all the ways to synchronize the execution of a graph with the host.

Understanding the program flow can enable us to understand the sort of debug information that can be printed if we have runtime failures to debug. Chapter 13 has a table in the section “Debugging Runtime Failures” that will make a little more sense given the knowledge we have gained by this point in the book. However, this book does not attempt to discuss these advanced compiler dumps in detail.

Hopefully this has left you feeling like a graph expert who can construct graphs that range in complexity from linear chains to enormous graphs with hundreds of nodes and complex data and task dependences! In the next chapter, we’ll begin to dive into low-level details that are useful for improving the performance of an application on a specific device.

![](images/84ac042d40705cb975448922eb4f5fbd0c1ec037db0d4ffab86363cf940930a6.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
