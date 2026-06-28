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
