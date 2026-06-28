# Error Handling

Error handling is a key capability of C++. This chapter discusses the unique error handling challenges when offloading work to a device (accelerator) and how these challenges are made fully manageable to us by SYCL.

Detecting and dealing with unexpected conditions and errors can be helpful during application development (think: the other programmer who works on the project who does make mistakes), but more importantly play a critical role in stable and safe production applications and libraries. We devote this chapter to describing the error handling mechanisms available in C++ with SYCL so that we can understand what our options are and how to architect applications if we care about detecting and managing errors.

This chapter overviews synchronous and asynchronous errors in SYCL, describes the behavior of an application if we do nothing in our code to handle errors, and dives into the SYCL-specific mechanisms that allow us to handle asynchronous errors.

## Safety First

A core aspect of C++ error handling is that if we do nothing to handle an error that has been detected (thrown), then the application will terminate and indicate that something went wrong. This behavior allows us to write applications without focusing on error management and still be confident that errors will somehow be signaled to a developer or user. We’re not suggesting that we should ignore error handling, of course! Production applications should be written with error management as a core part of

the architecture, but applications often start development without such a focus. C++ aims to make code which doesn’t handle errors still able to observe many errors, even when they are not dealt with explicitly.

Since SYCL is data parallel C++, the same philosophy holds: if we do nothing in our code to manage errors and an error is detected, an abnormal termination of the program will occur to let us know that something bad happened. Production applications should of course consider error management as a core part of the software architecture, not only reporting but often also recovering from error conditions.

If we don’t add any error management code and an error occurs, we will still see an abnormal program termination which is an indication to dig deeper.

## Types of Errors

C++ provides a framework for notification and handling of errors through its exception mechanism. Heterogeneous programming requires an additional level of error management beyond this because some errors occur on a device or when trying to launch work on a device. These errors are typically decoupled in time from the host program’s execution, and as such they don’t integrate cleanly with regular C++ exception handling mechanisms. To solve this, there are additional mechanisms to make asynchronous errors as manageable and controllable as typical C++ exceptions.

Figure 5-1 shows two components of a typical application: (1) the host code that runs sequentially and submits work to the task graph for future execution and (2) the task graph which runs asynchronously from the host program and executes kernels or other actions on devices when the necessary dependences are met. The example shows a parallel\_for as the operation that executes asynchronously as part of the task graph, but other operations are possible as well as discussed in Chapters 3, 4, and 8.

![](images/eda600d66dfbe326a1e4b4da5c6bf3f674028ad7b7fb64103635f8d7c0231042.jpg)  
Figure 5-1. Separation of host program and task graph executions

The distinction between the left and right (host and task graph) sides of Figure 5-1 is the key to understanding the differences between synchronous and asynchronous errors.

Synchronous errors occur when an error condition can be detected as the host program executes an operation, such as an API call or object construction. They can be detected before an instruction on the left side of the figure completes, and the error can be thrown immediately by the operation that caused the error. We can wrap specific instructions on the left side of the diagram with a try-catch construct, expecting that errors occurring as a result of operations within the try will be detected before the try block ends (and therefore caught). The C++ exception mechanism is designed to handle exactly these types of errors.

Asynchronous errors occur as part of the right side of Figure 5-1, where an error is only detected when an operation in the task graph is executed. By the time that an asynchronous error is detected as part of task graph execution, the host program has typically already moved on with its execution, so there is no code to wrap with a try-catch construct to catch these errors. There is instead an asynchronous exception handling framework in SYCL to handle these errors that occur at seemingly random and uncontrolled times relative to host program execution.

## Let’s Create Some Errors!

As examples for the remainder of this chapter and to allow us to experiment, we’ll create both synchronous and asynchronous errors in the following examples.

![](images/7f08eabf64500e97ec184c36373c0f627fe159c355c8ea7c5f3436a8d237c0a9.jpg)  
Figure 5-2. Creating a synchronous error

## Synchronous Error

In Figure 5-2, a sub-buffer is created from a buffer but with an illegal size (larger than the original buffer). The constructor of the sub-buffer detects this error and throws an exception before the constructor’s execution completes. This is a synchronous error because it occurs as part of (synchronously with) the host program’s execution. The error is detectable before the constructor returns, so the error may be handled immediately at its point of origin or detection in the host program.

Our code example doesn’t do anything to catch and handle C++ exceptions, so the default C++ uncaught exception handler calls std::terminate for us, signaling that something went wrong.

## Asynchronous Error

Generating an asynchronous error is a bit trickier because implementations work hard to detect and report errors synchronously whenever possible. Synchronous errors are easier to debug because they occur at a specific point of origin in the host program, so are preferred by implementations whenever possible. One way to generate an asynchronous error for our demonstration purpose is to throw an exception inside a host task, which executes asynchronously as part of the task graph. Figure 5-3 demonstrates such an exception. Asynchronous errors can occur and be reported in many situations, so note that this host task example shown in Figure 5-3 is only one possibility and in no way a requirement for asynchronous errors.

```cpp
CHAPTER 5 ERROR HANDLING

#include <sycl/sycl.hpp>
using namespace sycl;

// Our example asynchronous handler function
auto handle_async_error = [](exception_list elist) {
    for (auto &e : elist) {
        try {
            std::rethrow_exception(e);
        } catch (...) {
            std::cout << "Caught SYCL ASYNC exception!!\n";
        }
    }
};

void say_device(const queue &Q) {
    std::cout << "Device : "
                    << Q.get_device().get_info<info::device::name>()
                    << "\n";
}

class something_went_wrong {}; // Example exception type

int main() {
    queue q{cpu_selector_v, handle_async_error};
    say_device(q);

    q.submit([&](handler &h) {
        h.host_task([]() { throw(something_went_wrong{}); });
    }).wait();

    return 0;
}

Example output:
Device : Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz
Caught SYCL ASYNC exception!!
```  
Figure 5-3. Creating an asynchronous error

## Application Error Handling Strategy

The C++ exception features are designed to cleanly separate the point in a program where an error is detected from the point where it may be handled, and this concept fits very well with both synchronous and asynchronous errors in SYCL. Through the throw and catch mechanisms, a hierarchy of handlers can be defined which can be important in production applications.

Building an application that can handle errors in a consistent and reliable way requires a strategy up front and a resulting software architecture built for error management. C++ provides flexible tools to implement many alternative strategies, but such architecture is beyond the scope of this chapter. There are many books and other references devoted to this topic, so we encourage looking to them for full coverage of C++ error management strategies.

This said, error detection and reporting doesn’t always need to be production-scale. Errors in a program can be reliably detected and reported through minimal code if the goal is simply to detect errors during execution and to report them (but not necessarily to recover from them). The following sections cover first what happens if we ignore error handling and do nothing (the default behavior isn’t all that bad!), followed by recommended error reporting that is simple to implement in basic applications.

## Ignoring Error Handling

C++ and SYCL are designed to tell us that something went wrong even when we don’t handle errors explicitly. The default result of unhandled synchronous or asynchronous errors is abnormal program termination which an operating system should tell us about. The following two examples mimic the behavior that will occur if we do not handle a synchronous and an asynchronous error, respectively.

Figure 5-4 shows the result of an unhandled C++ exception, which could be an unhandled SYCL synchronous error, for example. We can use this code to test what a particular operating system will report in such a case.

```cpp
CHAPTER 5 ERROR HANDLING

#include <iostream>

class something_went_wrong {}

int main() {
    std::cout << "Hello\n";

    throw(something_went_wrong{});
}

Example output:
Hello
terminate called after throwing an instance of 'something_went_wrong'
Aborted
```  
Figure 5-4. Unhandled exception in C++

Figure 5-5 shows example output from std::terminate being called, which will be the result of an unhandled SYCL asynchronous error in our application. We can use this code to test what a particular operating system will report in such a case.

```cpp
#include <iostream>

int main() {
  std::cout << "Hello\n";

  std::terminate();
}

Example output:
Hello
terminate called without an active exception
Aborted
```

## Figure 5-5. std::terminate is called when a SYCL asynchronous exception isn’t handled

Although we should probably handle errors in our programs, uncaught exceptions will eventually be caught and the program terminated, which is better than exceptions being silently lost!

## Synchronous Error Handling

We keep this section very short because SYCL synchronous errors are just C++ exceptions. Most of the additional error mechanisms added in SYCL relate to asynchronous errors which we cover in the next section, but synchronous errors are important because implementations try to detect and report as many errors synchronously as possible, since they are easier to reason about and handle.

Synchronous errors defined by SYCL are of type sycl::exception, a class derived from std::exception, which allows us to catch the SYCL errors specifically though a try-catch structure such as what we see in Figure 5-6.

```cpp
try {
  // Do some SYCL work
} catch (sycl::exception &e) {
  // Do something to output or handle the exception
  std::cout << "Caught sync SYCL exception: " << e.what()
              << "\n";
  return 1;
}
```  
Figure 5-6. Pattern to catch sycl::exception specifically

On top of the C++ error handling mechanisms, SYCL adds a sycl::exception type for the exceptions thrown by the runtime. Everything else is standard C++ exception handling, so will be familiar to most developers.

A slightly more complete example is provided in Figure 5-7, where additional classes of exception are handled.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
  try {
    buffer<int> b{range{16}};

    // ERROR: Create sub-buffer larger than size of parent
    // buffer. An exception is thrown from within the buffer
    // constructor.
    buffer<int> b2(b, id{8}, range{16});

  } catch (sycl::exception &e) {
    // Do something to output or handle the exception
    std::cout << "Caught synchronous SYCL exception: "
                  << e.what() << "\n";
    return 1;
  } catch (std::exception &e) {
    std::cout << "Caught std exception: " << e.what()
                  << "\n";
    return 2;
  } catch (...) {
    std::cout << "Caught unknown exception\n";
    return 3;
  }

  return 0;
}

Example output:
Caught synchronous SYCL exception: Requested sub-buffer
size exceedsthe size of the parent buffer -30
(PI_ERROR_INVALID_VALUE)
```  
Figure 5-7. Pattern to catch exceptions from a block of code

## Asynchronous Error Handling

Asynchronous errors are detected by the SYCL runtime (or an underlying backend), and the errors occur independently of execution of commands in the host program. The errors are stored in lists internal to the SYCL

runtime and only released for processing at specific points that the programmer can control. There are two topics that we need to discuss to cover handling of asynchronous errors:

1. What the handler should do, when invoked on outstanding asynchronous errors to process

2. When the asynchronous handler is invoked

## The Asynchronous Handler

The asynchronous handler is a function that the application defines, which is registered with SYCL contexts and/or queues. At the times defined by the next section, if there are any unprocessed asynchronous exceptions that are available to be handled, then the asynchronous handler is invoked by the SYCL runtime and passed a list of these exceptions.

The asynchronous handler is passed to a context or queue constructor as a std::function and can be defined in ways such as a regular function, lambda expression, or function object, depending on our preference. The handler must accept a sycl::exception\_list argument, such as in the example handler shown in Figure 5-8.

```cpp
// Our simple asynchronous handler function
auto handle_async_error = [](exception_list elist) {
  for (auto& e : elist) {
    try {
      std::rethrow_exception(e);
    } catch (sycl::exception& e) {
      std::cout << "ASYNC EXCEPTION!!\n";
      std::cout << e.what() << "\n";
    }
  }
};
```

Figure 5-8. Example asynchronous handler implementation defined as a lambda

In Figure 5-8, the std::rethrow\_exception followed by catch of a specific exception type provides filtering of the type of exception, in this case to only sycl::exception. We can also use alternative filtering approaches in C++ or just choose to handle all exceptions regardless of the type.

The handler is associated with a queue or context (low-level detail covered more in Chapter 6) at construction time. For example, to register the handler defined in Figure 5-8 with a queue that we are creating, we could write

queue my\_queue{ gpu\_selector\_v, handle\_async\_error };

Likewise, to register the handler defined in Figure 5-8 with a context that we are creating, we could write

context my\_context{ handle\_async\_error };

Most applications do not need contexts to be explicitly created or managed (they are created behind the scenes for us automatically), so if an asynchronous handler is going to be used, most developers should associate such handlers with queues that are being constructed for specific devices (and not explicit contexts).

In defining asynchronous handlers, most developers should define them on queues unless already explicitly managing contexts for other reasons.

If an asynchronous handler is not defined for a queue or the queue’s parent context and an asynchronous error occurs on that queue (or in the context) that must be processed, then the default asynchronous handler is invoked. The default handler operates as if it was coded as shown in Figure 5-9.

```cpp
// Our simple asynchronous handler function
auto handle_async_error = [](exception_list elist) {
  for (auto& e : elist) {
    try {
      std::rethrow_exception(e);
    } catch (sycl::exception& e) {
      // Print information about the asynchronous exception
    } catch (...) {
      // Print information about non-sycl::exception
    }
  }

  // Terminate abnormally to make clear to user that
  // something unhandled happened
  std::terminate();
};

Example output:
Device : Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz
terminate called without an active exception
Aborted
```  
Figure 5-9. Example of how the default asynchronous handler behaves

The default handler should display some information to the user on any errors in the exception list and then will end the application through std::terminate, which should cause the operating system to report that termination was abnormal.

What we put within an asynchronous handler is up to us. It can range from logging of an error to application termination to recovery of the error condition so that an application can continue executing normally. The common case is to report any details of the error available by calling sycl::exception::what(), followed by termination of the application.

Although it’s up to us to decide what an asynchronous handler does internally, a common mistake is to print an error message (that may be missed in the noise of other messages from the program), followed by completion of the handler function. Unless we have error management principles in place that allow us to recover a known program state and to be confident that it’s safe to continue execution, we should consider terminating the application within our asynchronous handler function(s). This reduces the chance that incorrect results will appear from a program where an error was detected, but where the application was inadvertently allowed to continue with execution regardless. In many programs, abnormal termination is the preferred result once we have detected an asynchronous exception.

Consider terminating applications within an asynchronous handler, after outputting information about the error, if comprehensive error recovery and management mechanisms are not in place.

## Invocation of the Handler

The asynchronous handler is called by the runtime at specific times. Errors aren’t reported immediately as they occur because management of errors and safe application programming (particularly multithreaded) would become more difficult and expensive (e.g., additional synchronizations between host and device) if that was the case. The asynchronous handler is instead called at the following very specific times:

1. When the host program calls queue::throw\_ asynchronous() on a specific queue

2. When the host program calls queue::wait\_and\_ throw() on a specific queue

3. When the host program calls event::wait\_and\_ throw() on a specific event

4. When a queue is destroyed

5. When a context is destroyed

Methods 1–3 provide a mechanism for a host program to control when asynchronous exceptions are handled, so that thread safety and other details specific to an application can be managed. They effectively provide controlled points at which asynchronous exceptions enter the host program control flow and can be processed almost as if they were synchronous errors.

If a user doesn’t explicitly call one of the methods 1–3, then asynchronous errors are commonly reported during program teardown when queues and contexts are destroyed. This is often enough to signal to a user that something went wrong and that program results shouldn’t be trusted.

Relying on error detection during program teardown doesn’t work in all cases, though. For example, if a program will only terminate when some algorithm convergence criteria are achieved and if those criteria are only achievable by successful execution of device kernels, then an asynchronous exception may signal that the algorithm will never converge and begin the teardown (where the error would be noticed). In these cases, and also in production applications where more complete error handling strategies are in place, it makes sense to invoke throw\_asynchronous() or wait\_and\_throw() at regular and controlled points in the program (e.g., before checking whether algorithm convergence has occurred).

## Errors on a Device

The error detection and handling mechanisms discussed in this chapter have been host-based. They are mechanisms through which the host program can detect and deal with something that may have gone wrong either in the host program or potentially during execution of kernels on devices. What we have not covered is how to signal, from within the device code that we write, that something has gone wrong. This omission is not a mistake, but quite intentional.

## Chapter 5 Error Handling

SYCL explicitly disallows C++ exception handling mechanisms (such as throw) within device code, because there are performance costs for some types of devices that we usually don’t want to pay. If we detect that something has gone wrong within our device code, we should signal the error using existing non-exception-based techniques. For example, we could write to a buffer that logs errors or returns some invalid result from our numeric calculation that we define to mean that an error occurred. The right strategy in these cases is very application specific.

## Summary

In this chapter, we introduced synchronous and asynchronous errors, covered the default behavior to expect if we do nothing to manage errors that might occur, and covered the mechanisms used to handle asynchronous errors at controlled points in our application. Error management strategies are a major topic in software engineering and a significant percentage of the code written in many applications. SYCL integrates with the C++ knowledge that we already have when it comes to error handling and provides flexible mechanisms to integrate with whatever our preferred error management strategy is.

![](images/f9013f66c676ef1ffe56db0d321b4b3de756c3815763eee4eb059f379f985b53.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Unified Shared Memory

The next two chapters provide a deeper look into how to manage data. There are two different approaches that complement each other: Unified Shared Memory (USM) and buffers. USM exposes a different level of abstraction for memory than buffers—USM uses pointers, and buffers are a higher-level interface. This chapter focuses on USM. The next chapter will focus on buffers.

Unless we specifically know that we want to use buffers, USM is a good place to start. USM is a pointer-based model that allows memory to be read and written through regular C++ pointers.

## Why Should We Use USM?

Since USM is based on C++ pointers, it is a natural place to start for existing pointer-based C++ codes. Existing functions that take pointers as parameters continue to work without modification. In the majority of cases, the only changes required are to replace existing calls to malloc or new with USM-specific allocation routines that we will discuss later in this chapter.

## Allocation Types

While USM is based on C++ pointers, not all pointers are created equal. USM defines three different types of allocations, each with unique semantics. A device may not support all types (or even any type) of USM allocation. We will learn how to query what a device supports later. The three types of allocations and their characteristics are summarized in Figure 6-1.

<table><tr><td>Type</td><td>Description</td><td>Accessible on host?</td><td>Accessible on device?</td><td>Located on</td></tr><tr><td>device</td><td>Allocations in device memory</td><td>x</td><td>✓</td><td>device</td></tr><tr><td>host</td><td>Allocations in host memory</td><td>✓</td><td>✓</td><td>host</td></tr><tr><td>shared</td><td>Allocations shared between host and device</td><td>✓</td><td>✓</td><td>Can migrate between host and device</td></tr></table>

Figure 6-1. USM allocation types

## Device Allocations

This first type of allocation is what we need in order to have a pointer into a device’s attached memory, such as (G)DDR or HBM. Device allocations can be read from or written to by kernels running on a specific device, but they cannot be directly accessed from code executing on the host (and usually not by devices either). Trying to access a device allocation on the host can result in either incorrect data or a program crashing due to an error. We must copy data between host and device using the explicit USM memcpy mechanisms, which specify how much data must be copied between two places, that will be covered later in this chapter.

## Host Allocations

This second type of allocation is easier to use than device allocations since we do not have to manually copy data between the host and the device. Host allocations are allocations in host memory that are accessible on both the host and the device. These allocations, while accessible on the device, cannot migrate to the device’s attached memory. Instead, kernels may remotely read from or write to this memory, often over a slower bus such as PCI Express (or really not differently at all if it’s a CPU device or integrated GPU device). This trade-off between convenience and performance is something that we must take into consideration. Despite the higher access costs that host allocations can incur, there are still valid reasons to use them. Examples include rarely accessed data, large data sets that cannot fit inside device-attached memory, or that a device may not support alternatives like shared allocations which are described next.

## Shared Allocations

The final type of allocation combines attributes of both device and host allocations, combining the programmer convenience of host allocations with the greater performance afforded by device allocations. Like host allocations, shared allocations are accessible on both the host and device. The difference between them is that shared allocations are free to migrate between host memory and device-attached memory, automatically, without our intervention. If an allocation has migrated to the device, any kernel executing on that device accessing it will do so with greater performance than remotely accessing it from the host. However, shared allocations do not give us all the benefits without any drawbacks.

Automatic migration can be implemented in a variety of ways. No matter which way the runtime chooses to implement shared allocations, they usually pay a price of increased latency. With device allocations, we know exactly how much memory needs to be copied and can schedule the copy to begin as early as possible. The automatic migration mechanisms cannot see the future and, in some cases, do not begin moving data until a kernel tries to access it. The kernel must then wait, or block, until the data movement has completed before it can continue executing. In other cases, the runtime may not know exactly how much data the kernel will access and might conservatively move a larger amount of data than is required, also increasing latency for the kernel.

We should also note that while shared allocations can migrate, it does not necessarily mean that all implementations of SYCL will migrate them. We expect most implementations to implement shared allocations with migration, but some devices may prefer to implement them identically to host allocations. In such an implementation, the allocation is still visible on both host and device, but we may not see the performance gains that a migrating implementation could provide.

## Allocating Memory

USM allows us to allocate memory in a variety of different ways that cater to different needs and preferences. However, before we go over all the methods in greater detail, we should discuss how USM allocations differ from regular C++ allocations.

## What Do We Need to Know?

Regular C++ programs can allocate memory in multiple ways: new, malloc, or allocators. No matter which syntax we prefer, memory allocation is ultimately performed by the system allocator in the host operating system. When we allocate memory in C++, the only concerns are “How much memory do we need?” and “How much memory is available to allocate?” However, USM requires extra information before an allocation can be performed.

First, USM allocation needs to specify which type of allocation is desired: device, host, or shared. It is important to request the right type of allocation in order to obtain the desired behavior. Next, every USM allocation must specify a context object against which the allocation will be made. Most of the examples in the book instead pass a queue object (which then provides the context). The context object hasn’t had a lot of discussion in this book up to this point, so it’s worth saying a little about it here. A context represents a device or set of devices on which we can execute kernels. We can think of a context as a convenient place for the runtime to stash some state about what it’s doing. Programmers are not likely to directly interact with contexts outside of passing them around in most SYCL programs. We do offer a few tips regarding contexts in Chapter 13.

USM allocations are not guaranteed to be usable across different contexts—it is important that all USM allocations, queues, and kernels share the same context object. Typically, we can obtain this context from the queue being used to submit work to a device.

Finally, device allocations (and some shared allocations) also require that we specify which device will provide the memory for the allocation. This is important since we do not want to oversubscribe the memory of our devices (unless the device is able to support this—we will say more about that later in the chapter when we discuss migration of data). USM allocation routines can be distinguished from their C++ analogues by the addition of these extra parameters.

## Multiple Styles

Sometimes, trying to please everyone with a single option proves to be an impossible task, just as some people prefer coffee over tea, or emacs over vi. If we ask programmers what an allocation interface should look like, we will get several different answers back. USM embraces this diversity of choice and provides several different flavors of allocation interfaces. These different flavors are C-style, C++-style, and C++ allocator–style. We will now discuss each and point out their similarities and differences.

## Allocations à la C

The first style of allocation functions (listed in Figure 6-2, later used in examples shown in Figures 6-6 and 6-7) is modeled after memory allocation in C: malloc functions that take a number of bytes to allocate and return a void \* pointer. This style of function is type agnostic. We must specify the total number of bytes to allocate, which means if we want to allocate N objects of type X, one must ask for N \* sizeof(X) total bytes. The returned pointer is of type void \*, which means that we must then cast it to an appropriate pointer to type X. This style is very simple but can be verbose due to the size calculations and typecasting required.

We can further divide this style of allocation into two categories: named functions and single function. The distinction between these two flavors is how we specify the desired type of USM allocation. With the named functions (malloc\_device, malloc\_host, and malloc\_shared), the type of USM allocation is encoded in the function name. The single function malloc requires the type of USM allocation to be specified as an additional parameter. Neither flavor is better than the other, and the choice of which to use is governed by our preference.

We cannot move on without briefly mentioning alignment. Each version of malloc also has an aligned\_alloc counterpart. The malloc functions return memory aligned to the default behavior of our device. On success it will return a legal pointer with a valid alignment, but there may be cases where we would prefer to manually specify an alignment. In these cases, we should use one of the aligned\_alloc variants that also require us to specify the desired alignment for the allocation. Legal alignments are powers of two. It’s worth noting that on many devices, allocations are maximally aligned to correspond to features of the hardware, so while we may ask for allocations to be 4-, 8-, 16-, or 32-byte aligned, we might in practice see larger alignments that give us what we ask for and then some.

```c
// Named Functions
void *malloc_device(size_t size, const device &dev,
                    const context &ctxt);
void *malloc_device(size_t size, const queue &q);
void *aligned_alloc_device(size_t alignment, size_t size,
                   const device &dev,
                   const context &ctxt);
void *aligned_alloc_device(size_t alignment, size_t size,
                   const queue &q);

void *malloc_host(size_t size, const context &ctxt);
void *malloc_host(size_t size, const queue &q);
void *aligned_alloc_host(size_t alignment, size_t size,
                   const context &ctxt);
void *aligned_alloc_host(size_t alignment, size_t size,
                   const queue &q);

void *malloc_shared(size_t size, const device &dev,
                   const context &ctxt);
void *malloc_shared(size_t size, const queue &q);
void *aligned_alloc_shared(size_t alignment, size_t size,
                   const device &dev,
                   const context &ctxt);
void *aligned_alloc_shared(size_t alignment, size_t size,
                   const queue &q);

// Single Function
void *malloc(size_t size, const device &dev,
               const context &ctxt, usm::alloc kind);
void *malloc(size_t size, const queue &q, usm::alloc kind);
void *aligned_alloc(size_t alignment, size_t size,
                   const device &dev, const context &ctxt,
                   usm::alloc kind);
void *aligned_alloc(size_t alignment, size_t size,
                   const queue &q, usm::alloc kind);
```

## Figure 6-2. C-style USM allocation functions

## Allocations à la C++

The next flavor of USM allocation functions (listed in Figure 6-3) is very similar to the first but with more of a C++ look and feel. We once again have both named and single function versions of the allocation routines as well as our default and user-specified alignment versions. The difference is that now our functions are C++ templated functions that allocate Count objects of type T and return a pointer of type T \*. Taking advantage of modern C++ simplifies things, since we no longer need to manually calculate the total size of the allocation in bytes or cast the returned pointer to the appropriate type. This also tends to yield a more compact and less error-prone expression in code. However, we should note that unlike “new” in C++, malloc-style interfaces do not invoke constructors for the objects being allocated—we are simply allocating enough bytes to fit that type.

This flavor of allocation is a good place to start for new codes written with USM in mind. The previous C-style is a good starting point for existing C++ codes that already make heavy use of C or C++ malloc, to which we will add the use of USM.

```c
// Named Functions
template <typename T>
T *malloc_device(size_t Count, const device &Dev,
                    const context &Ctxt);
template <typename T>
T *malloc_device(size_t Count, const queue &Q);
template <typename T>
T *aligned_alloc_device(size_t Alignment, size_t Count,
                    const device &Dev,
                    const context &Ctxt);
template <typename T>
T *aligned_alloc_device(size_t Alignment, size_t Count,
                    const queue &Q);

template <typename T>
T *malloc_host(size_t Count, const context &Ctxt);
template <typename T>
T *malloc_host(size_t Count, const queue &Q);
template <typename T>
T *aligned_alloc_host(size_t Alignment, size_t Count,
                    const context &Ctxt);
template <typename T>
T *aligned_alloc_host(size_t Alignment, size_t Count,
                    const queue &Q);

template <typename T>
T *malloc_shared(size_t Count, const device &Dev,
                    const context &Ctxt);
template <typename T>
T *malloc_shared(size_t Count, const queue &Q);
template <typename T>
T *aligned_alloc_shared(size_t Alignment, size_t Count,
                    const device &Dev,
                    const context &Ctxt);
template <typename T>
T *aligned_alloc_shared(size_t Alignment, size_t Count,
                    const queue &Q);

// Single Function
template <typename T>
T *malloc(size_t Count, const device &Dev,
                    const context &Ctxt, usm::alloc Kind);
template <typename T>
T *malloc(size_t Count, const queue &Q, usm::alloc Kind);
template <typename T>
T *aligned_alloc(size_t Alignment, size_t Count,
                    const device &Dev, const context &Ctxt,
                    usm::alloc Kind);
template <typename T>
T *aligned_alloc(size_t Alignment, size_t Count,
                    const queue &Q, usm::alloc Kind);
```

## Figure 6-3. C++-style USM allocation functions

## C++ Allocators

The final flavor of USM allocation (Figure 6-4) embraces modern C++ even more than the previous flavor. This flavor is based on the C++ allocator interface, which defines objects that are used to perform memory allocations either directly or indirectly inside a container such as std::vector. This allocator flavor is most useful if our code makes heavy use of container objects that can hide the details of memory allocation and deallocation from the user, simplifying code and reducing the opportunity for bugs.

```cpp
template <typename T, usm::alloc AllocKind,
        size_t Alignment = 0>
class usm_allocator {
public:
    using value_type = T;
    using propagate_on_container_copy_assignment =
        std::true_type;
    using propagate_on_container_move_assignment =
        std::true_type;
    using propagate_on_container_swap = std::true_type;

public:
    template <typename U>
    struct rebind {
        typedef usm_allocator<U, AllocKind, Alignment> other;
    };

    usm_allocator() = delete;
    usm_allocator(const context& syclContext,
                       const device& syclDevice,
                       const property_list& propList = {};
    usm_allocator(const queue& syclQueue,
                       const property_list& propList = {};
    usm_allocator(const usm_allocator& other);
    usm_allocator(usm_allocator&&) noexcept;
    usm_allocator& operator=(const usm_allocator&);
    usm_allocator& operator=(usm_allocator&&);

    template <class U>
    usm_allocator(usm_allocator<U, AllocKind,
                          Alignment> const&) noexcept;

    /// Allocate memory
    T* allocate(size_t count);

    /// Deallocate memory
    void deallocate(T* Ptr, size_t count);

    /// Equality Comparison
    ///
    /// Allocators only compare equal if they are of the same
    /// USM kind, alignment, context, and device
    template <class U, usm::alloc AllocKindU,
           size_t AlignmentU>
    friend bool operator==( 
        const usm_allocator<T, AllocKind, Alignment>&,
        const usm_allocator<U, AllocKindU, AlignmentU>&);

    /// Inequality Comparison
    /// Allocators only compare unequal if they are not of the
    /// same USM kind, alignment, context, or device
    template <class U, usm::alloc AllocKindU,
           size_t AlignmentU>
    friend bool operator!=( 
        const usm_allocator<T, AllocKind, Alignment>&,
        const usm_allocator<U, AllocKindU, AlignmentU>&);
};
```

## Figure 6-4. C++ allocator–style USM allocation functions

## Deallocating Memory

Whatever a program allocates must eventually be deallocated. USM defines a free method to deallocate memory allocated by one of the malloc or aligned\_malloc functions. This free method also takes the context in which the memory was allocated as an extra parameter. The queue can also be substituted for the context. If memory was allocated with a C++ allocator object, it should also be deallocated using that object.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    // Allocate N floats

    // C-style
    float *f1 = static_cast<float *>(malloc_shared(
        N * sizeof(float), q.get_device(), q.get_context());

    // C++-style
    float *f2 = malloc_shared<float>(N, q);

    // C++-allocator-style
    usm_allocator<float, usm::alloc::shared> alloc(q);
    float *f3 = alloc.allocate(N);

    // Free our allocations
    free(f1, q.get_context());
    free(f2, q);
    alloc.deallocate(f3, N);

    return 0;
}
```  
Figure 6-5. Three styles for allocation

## Allocation Example

In Figure 6-5, we show how to perform the same allocation using the three styles just described. In this example, we allocate N single-precision floating-point numbers as shared allocations. The first allocation f1 uses the C-style void \* returning malloc routines. For this allocation, we explicitly pass the device and context that we obtain from the queue. We must also cast the result back to a float \*. The second allocation f2 does the same thing but using the C++-style templated malloc. Since we pass the type of our elements, float, to the allocation routine, we only need to specify how many floats we want to allocate, and we do not need to cast the result. We also use the form that takes the queue instead of the device and context, yielding a very simple and compact statement. The third allocation f3 uses the USM C++ allocator class. We instantiate an allocator object of the proper type and then perform the allocation using that object. Finally, we show how to properly deallocate each allocation.
