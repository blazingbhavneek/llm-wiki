## Data Management

Now that we understand how to allocate memory using USM, we will discuss how data is managed. We can look at this in two pieces: data initialization and data movement.

## Initialization

Data initialization concerns filling our memory with values before we perform computations on it. One example of a common initialization pattern is to fill an allocation with zeroes before it is used. If we were to do this using USM allocations, we could do it in a variety of ways. First, we could write a kernel to do this. If our data set is particularly large or the initialization requires complex calculations, this is a reasonable way to

go since the initialization can be performed in parallel (and it makes the initialized data ready to go on the device). Second, we could implement this as a loop in host code over all the elements of an allocation that sets each to zero. However, there is potentially a problem with this approach. A loop would work fine for host and shared allocations since these are accessible on the host. However, since device allocations are not accessible on the host, a loop in host code would not be able to write to them. This brings us to the third option.

The memset function is designed to efficiently implement this initialization pattern. USM provides a version of memset that is a member function of both the handler and queue classes. It takes three arguments: the pointer representing the base address of the memory we want to set, a byte value representing the byte pattern to set, and the number of bytes to set to that pattern. Unlike a loop on the host, memset happens in parallel and also works with device allocations.

While memset is a useful operation, the fact that it only allows us to specify a byte pattern to fill into an allocation is rather limiting. USM also provides a fill method (as a member of the handler and queue classes) that lets us fill memory with an arbitrary pattern. The fill method is a function templated on the type of the pattern we want to write into the allocation. Template it with an int, and we can fill an allocation with the 32-bit integer number “42”. Similar to memset, fill takes three arguments: the pointer to the base address of the allocation to fill, the value to fill, and the number of times we want to write that value into the allocation.

## Data Movement

Data movement is probably the most important aspect of USM to understand. If the right data is not in the right place at the right time, our program will produce incorrect results. USM defines two strategies that we can use to manage data: explicit and implicit. The choice of which strategy we want to use is related to the types of USM allocations our hardware supports or that we want to use.

## Explicit

The first strategy USM offers is explicit data movement (Figure 6-6). Here, we must explicitly copy data between the host and device. We can do this by invoking the memcpy method, found on both the handler and queue classes. The memcpy method takes three arguments: a pointer to the destination memory, a pointer to the source memory, and the number of bytes to copy between host and device. We do not need to specify in which direction the copy is meant to happen—this is implicit in the source and destination pointers.

The most common usage of explicit data movement is copying to or from device allocations in USM since they are not accessible on the host. Having to insert explicit copying of data does require effort on our part. Additionally, it can be a source of bugs: copies could be accidentally omitted, an incorrect amount of data could be copied, or the source or destination pointer could be incorrect.

However, explicit data movement does not only come with disadvantages. It gives us large advantage: total control over data movement. Control over both how much data is copied and when the data gets copied is very important for achieving the best performance in some applications. Ideally, we can overlap computation with data movement whenever possible, ensuring that the hardware runs with high utilization.

The other types of USM allocations, host and shared, are both accessible on host and device and do not need to be explicitly copied to the device. This leads us to the other strategy for data movement in USM.

```cpp
CHAPTER 6 UNIFIED SHARED MEMORY

#include <array>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    std::array<int, N> host_array;
    int* device_array = malloc_device<int>(N, q);
    for (int i = 0; i < N; i++) host_array[i] = N;

    q.submit([&](handler& h) {
        // copy host_array to device_array
        hmemcpy(device_array, &host_array[0], N * sizeof(int));
    });
    q.wait(); // needed for now (we learn a better way later)

    q.submit([&](handler& h) {
        h.parallel_for(N, [=](id<1> i) { device_array[i]++;
    });
    q.wait(); // needed for now (we learn a better way later)

    q.submit([&](handler& h) {
        // copy device_array back to host_array
        hmemcpy(&host_array[0], device_array, N * sizeof(int));
    });
    q.wait(); // needed for now (we learn a better way later)

    free(device_array, q);
    return 0;
}
```

Figure 6-6. USM explicit data movement example

## Implicit

The second strategy that USM provides is implicit data movement (example usage shown in Figure 6-7). In this strategy, data movement happens implicitly, that is, without requiring input from us. With implicit data movement, we do not need to insert calls to memcpy since we can directly access the data through the USM pointers wherever we want to use it. Instead, it becomes the job of the system to ensure that the data will be available in the correct location when it is being used.

With host allocations, one could argue whether they really cause data movement. Since, by definition, they always remain pointers to host memory, the memory represented by a given host pointer cannot be stored on the device. However, data movement does occur as host allocations are accessed on the device. Instead of the memory being migrated to the device, the values we read or write are transferred over the appropriate interface to or from the kernel. This can be useful for streaming kernels where the data does not need to remain resident on the device.

Implicit data movement mostly concerns USM shared allocations. This type of allocation is accessible on both host and device and, more importantly, can migrate between host and device. The key point is that this migration happens automatically, or implicitly, simply by accessing the data in a different location. Next, we will discuss several things to think about when it comes to data migration for shared allocations.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    int* host_array = malloc_host<int>(N, q);
    int* shared_array = malloc_shared<int>(N, q);
    for (int i = 0; i < N; i++) host_array[i] = i;

    q.submit([&](handler& h) {
        h.parallel_for(N, [=](id<1> i) {
            // access shared_array and host_array on device
            shared_array[i] = host_array[i] + 1;
        });
    });
    q.wait();

    free(shared_array, q);
    free(host_array, q);
    return 0;
}
```  
Figure 6-7. USM implicit data movement example

## Migration

With explicit data movement, we control how much data movement occurs. With implicit data movement, the system handles this for us, but it might not do it as efficiently. The SYCL runtime is not an oracle—it cannot predict what data an application will access before it does it. Additionally, pointer analysis remains a very difficult problem for compilers, which may not be able to accurately analyze and identify every allocation that might be used inside a kernel. Consequently, implementations of the mechanisms for implicit data movement may make different decisions based on the capabilities of the device that supports USM, which affects both how shared allocations can be used and how they perform.

If a device is very capable, it might be able to migrate memory on demand. In this case, data movement would occur after the host or

device attempts to access an allocation that is not currently in the desired location. On-demand data greatly simplifies programming as it provides the desired semantic that a USM shared pointer can be accessed anywhere and just work. If a device cannot support on-demand migration (Chapter 12 explains how to query a device for capabilities), it might still be able to guarantee the same semantics with extra restrictions on how shared pointers can be used.

The restricted form of USM shared allocations governs when and where shared pointers may be accessed and how large shared allocations can be. If a device cannot migrate memory on demand, that means the runtime must be conservative and assume that a kernel might access any allocation in its device-attached memory. This brings a couple of consequences.

First, it means that the host and device should not try to access a shared allocation at the same time. Applications should instead alternate access in phases. The host can access an allocation, then a kernel can compute using that data, and finally the host can read the results. Without this restriction, the host is free to access different parts of an allocation than a kernel is currently touching. Such concurrent access typically happens at the granularity of a device memory page. The host could access one page, while the device accesses another. Atomically accessing the same piece of data will be covered in Chapter 19. Programmers may query whether a device is limited by this restriction, and we will learn more about the device query mechanism later.

The next consequence of this restricted form of shared allocations is that allocations are limited by the total amount of memory attached to a device. If a device cannot migrate memory on demand, it cannot migrate data to the host to make room to bring in different data. If a device does support on-demand migration, it is possible to oversubscribe its attached memory, allowing a kernel to compute on more data than the device’s memory could normally contain, although this flexibility may come with a performance penalty due to extra data movement.

## Fine-Grained Control

When a device supports on-demand migration of shared allocations, data movement occurs after memory is accessed in a location where it is not currently resident. However, a kernel can stall while waiting for the data movement to complete. The next statement it executes may even cause more data movement to occur and introduce additional latency to the kernel execution.

SYCL gives us a way to modify the performance of the automatic migration mechanisms. It does this by defining two functions: prefetch and mem\_advise. Figure 6-8 shows a simple utilization of each. These functions let us give hints to the runtime about how kernels will access data so that the runtime can choose to start moving data before a kernel tries to access it. Note that this example uses the queue shortcut methods that directly invoke parallel\_for on the queue object instead of inside a lambda passed to the submit method (a command group).

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;

// Appropriate values depend on your HW
constexpr int BLOCK_SIZE = 42;
constexpr int NUM_BLOCKS = 2500;
constexpr int N = NUM_BLOCKS * BLOCK_SIZE;

int main() {
    queue q;
    int *data = malloc_shared<int>(N, q);
    int *read_only_data = malloc_shared<int>(BLOCK_SIZE, q);

    for (int i = 0; i < N; i++) {
        data[i] = -i;
    }

    // Never updated after initialization
    for (int i = 0; i < BLOCK_SIZE; i++) {
        read_only_data[i] = i;
    }

    // Mark this data as "read only" so the runtime can copy
    // it to the device instead of migrating it from the host.
    // Real values will be documented by your backend.
    int HW_SPECIFIC_ADVICE_RO = 0;
    q.mem_advise(read_only_data, BLOCK_SIZE,
                    HW_SPECIFIC_ADVICE_RO);
    event e = q.prefetch(data, BLOCK_SIZE * sizeof(int));

    for (int b = 0; b < NUM_BLOCKS; b++) {
        q.parallel_for(range{BLOCK_SIZE}, e, [=](id<1> i) {
            data[b * BLOCK_SIZE + i] += read_only_data[i];
        });
        if ((b + 1) < NUM_BLOCKS) {
            // Prefetch next block
            e = q.prefetch(data + (b + 1) * BLOCK_SIZE,
                    BLOCK_SIZE * sizeof(int));
        }
    }
    q.wait();

    free(data, q);
    free(read_only_data, q);
    return 0;
}
```

Figure 6-8. Fine-grained control via prefetch and mem\_advise

The simplest way for us to do this is by invoking prefetch. This function is invoked as a member function of the handler or queue class and takes a base pointer and number of bytes. This lets us inform the runtime that certain data is about to be used on a device so that it can eagerly start migrating it. Ideally, we would issue these prefetch hints early enough such that by the time the kernel touches the data, it is already resident on the device, eliminating the latency we previously described.

The other function provided by SYCL is mem\_advise. This function allows us to provide device-specific hints about how memory will be used in kernels. An example of such possible advice that we could specify is that the data will only be read in a kernel, not written. In that case, the system could realize it could copy, or duplicate, the data on the device, so that the host’s version does not need to be updated after the kernel is complete. However, the advice passed to mem\_advise is specific to a particular device, so be sure to check the documentation for hardware before using this function.

## Queries

Finally, not all devices support every feature of USM. We should not assume that all USM features are available if we want our programs to be portable across different devices. USM defines several things that we can query. These queries can be separated into two categories: pointer queries and device capability queries. Figure 6-9 shows a simple utilization of each.

The pointer queries in USM answer two questions. The first question is “What type of USM allocation does this pointer point to?” The get\_ pointer\_type function takes a pointer and SYCL context and returns a result of type usm::alloc, which can have four possible values: host, device, shared, or unknown. The second question is “What device was this USM pointer allocated against?” We can pass a pointer and a context to the function get\_pointer\_device and get back a device object. This is mostly used with device or shared USM allocations since it does not make much sense with host allocations. The SYCL specification states that when used with host allocations, the first device in the context is returned—this is not for any particular reason other than to avoid throwing an exception, which would seem a bit odd for code that may be templated on USM allocation type.

The second type of query provided by USM concerns the capabilities of a device. USM has its own list of device aspects that can be queried by calling has on a device object. These queries can be used to test which types of USM allocations are supported by a device. Additionally, we can query if shared allocations may be concurrently accessed by the host and device. The full list of queries is shown in Figure 6-10. In Chapter 12, we will look at the query mechanism in more detail.

```cpp
#include <sycl/sycl.hpp>
using namespace sycl;
namespace dinfo = info::device;
constexpr int N = 42;

template <typename T>
void foo(T data, id<1> i) {
  data[i] = N;
}

int main() {
  queue q;
  auto dev = q.get_device();
  auto ctxt = q.get_context();
  bool usm_shared = dev.has(aspect::usm_shared_allocations);
  bool usm_device = dev.has(aspect::usm_device_allocations);
  bool use_USM = usm_shared || usm_device;

  if (use_USM) {
    int *data;
    if (usm_shared) {
      data = malloc_shared<int>(N, q);
    } else /* use device allocations */ {
      data = malloc_device<int>(N, q);
    }
    std::cout << "Using USM with "
                  << ((get_pointer_type(data, ctxt) ==
                   usm::alloc::shared)
                   ? "shared"
                   : "device")
                  << " allocations on "
                  << get_pointer_device(data, ctxt)
                   .get_info<dinfo::name>()
                  << "\n";
    q.parallel_for(N, [=](id<1> i) { foo(data, i); });
    q.wait();
    free(data, q);
} else /* use buffers */ {
    buffer<int, 1> data{range{N}};
    q.submit([&](handler &h) {
      accessor a(data, h);
      h.parallel_for(N, [=](id<1> i) { foo(a, i); });
    });
    q.wait();
  }
  return 0;
}
```

Figure 6-9. Queries on USM pointers and devices

<table><tr><td>Aspect</td><td>Description</td></tr><tr><td>aspect::usm_device_allocations</td><td>This device supports device allocations</td></tr><tr><td>aspect::usm_host_allocations</td><td>This device supports host allocations</td></tr><tr><td>aspect::usm_atomic_host_allocations</td><td>This device supports host allocations that may be modified atomically by the device</td></tr><tr><td>aspect::shared_allocations</td><td>This device supports shared allocations</td></tr><tr><td>aspect::atomic_shared_allocations</td><td>This device supports shared allocations and the host and device may concurrently access and atomically modify shared allocations</td></tr><tr><td>aspect::usm_system_allocations</td><td>This device supports using allocations made with the system allocator on the device</td></tr></table>

Figure 6-10. USM device aspects

## One More Thing

There is one more form of USM that we haven’t covered. The forms of USM we have described in this chapter all require the use of special allocation functions. While not a huge burden, this represents a change from traditional C++ code that uses the system allocator in the form of malloc or the new operator. While some devices today, such as CPUs, may not need this requirement, most accelerator devices still need it. Thus, we have described how to use the USM allocation functions in the name of greater portability. However, we believe that we will soon see more accelerator designs that support use of the system allocator. Such devices will greatly simplify programs by freeing the programmer from worrying about allocating the right type of USM memory or copying the correct data at the appropriate time. In some sense, one can view eventual system allocator support as the final evolution of USM—it would provide the benefits of shared USM allocations without requiring the use of special allocation functions.

## Summary

In this chapter, we’ve described Unified Shared Memory, a pointer-based strategy for data management. We covered the three types of allocations that USM defines. We discussed all the different ways that we can allocate and deallocate memory with USM and how data movement can be either explicitly controlled by us (the programmers) for device allocations or implicitly controlled by the system for host or shared allocations. Finally, we discussed how to query the different USM capabilities that a device supports and how to query information about USM pointers in a program.

Since we have not discussed synchronization in this book in detail yet, there is more on USM in later chapters when we discuss scheduling, communications, and synchronization. Specifically, we cover these additional considerations for USM in Chapters 8, 9, and 19.

In the next chapter, we will cover the second strategy for data management: buffers.

![](images/65d8d0af5f8725a56b7a2d81fda19edb8b184e508e2d6096ccd1bfb2ba64ce1f.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Buffers

In this chapter, we will learn about the buffer abstraction. We learned about Unified Shared Memory (USM), the pointer-based strategy for data management, in the previous chapter. USM forces us to think about where memory lives and what should be accessible where. The buffer abstraction is a higher-level model that hides this from the programmer. Buffers simply represent data, and it becomes the job of the runtime to manage how the data is stored and moved in memory.

This chapter presents an alternative approach to managing our data. The choice between buffers and USM often comes down to personal preference and the style of existing code, and applications are free to mix and match the two styles in representation of different data within the application.

USM simply exposes different abstractions for memory. USM has pointers, and buffers are a higher-level abstraction. The abstraction level of buffers allows the data contained within to be used on any device within the application, where the runtime manages whatever is needed to make that data available. The pointer-based model of USM is probably a better fit for applications that use pointer-based data structures such as linked lists, trees, or others. Buffers can also be trickier to retrofit into existing codes that already use pointers. However, buffers are guaranteed to work on every device in the system, while some devices may not support specific (or any) modes of USM. Choices are good, so let’s dive into buffers.

We will look more closely at how buffers are created and used. A discussion of buffers would not be complete without also discussing the accessor. While buffers abstract how we represent and store data in a program, we do not directly access the data using the buffer. Instead, we use accessor objects that inform the runtime how we intend to use the data we are accessing, and accessors are tightly coupled to the powerful data dependence mechanisms within task graphs. After we cover all the things we can do with buffers, we will also explore how to create and use accessors in our programs.

## Buffers

A buffer is a high-level abstraction for data. Buffers are not necessarily tied to a single location or virtual memory address. Indeed, the runtime is free to use many different locations in memory (even across different devices) to represent a buffer, but the runtime must be sure to always give us a consistent view of the data. A buffer is accessible on the host and on any device.

template <typename T, int Dimensions, AllocatorT allocator> class buffer;

## Figure 7-1. Buffer class definition

The buffer class is a template class with three template arguments, as shown in Figure 7-1. The first template argument is the type of the object that the buffer will contain. This type must be device copyable, which extends the notion of trivially copyable as defined by C++. Types that are trivially copyable are safe to copy byte by byte without using any special copy or move constructors. Device copyable types extend this notion recursively to certain C++ types like std::pair or std::tuple. The next template argument is an integer describing the dimensionality of the buffer. The final template argument is optional, and the default

value is usually what is used. This argument specifies a C++-style allocator class that is used to perform any memory allocations on the host that are needed for the buffer. First, we will examine the many ways that buffer objects can be created.

## Buffer Creation

In the following figures, we show several ways in which buffer objects can be created. Let’s walk through the example and look at each instance.

```cpp
// Create a buffer of 2x5 ints using the default allocator
buffer<int, 2, buffer_allocator<int>> b1{range<2>{2, 5}};
// Create a buffer of 2x5 ints using the default allocator
// and CTAD for range
buffer<int, 2> b2{range{2, 5}};
// Create a buffer of 20 floats using a
// default-constructed std::allocator
buffer<float, 1, std::allocator<float>> b3{range{20}};
// Create a buffer of 20 floats using a passed-in
// allocator
std::allocator<float> myFloatAlloc;
buffer<float, 1, std::allocator<float>> b4{range(20),
myFloatAlloc};
```  
Figure 7-2. Creating buffers, Part 1

The first buffer we create in Figure 7-2, b1, is a two-dimensional buffer of ten integers. We explicitly pass all template arguments, even explicitly passing the default value of buffer\_allocator<T> as the allocator type. Since buffer\_allocator is also a templated type, we must explicitly specialize it just as we do the buffer by specifying buffer\_allocator<int>. However, using modern C++, we can express this much more compactly. Buffer b2 is also a two-dimensional buffer of ten integers using the default allocator. Here we make use of C++17’s class template argument deduction (CTAD) to automatically infer template arguments. CTAD is an all-or-none tool—it must either infer every template argument for a class or infer none of them. In this case, we use the fact that we are initializing b2 with a range that takes two arguments to infer that it is a two-dimensional range. The allocator template argument has a default value, so we do not need to explicitly list it when creating the buffer.

With buffer b3, we create a buffer of 20 floats and use a defaultconstructed std::allocator to allocate any necessary memory on the host. When using a custom allocator type with a buffer, we often want to pass an actual allocator object to the buffer to use instead of the defaultconstructed one. Buffer b4 shows how to do this, taking the allocator object after the range in the call to its constructor.

For the first four buffers in our example, we let the buffer allocate any memory it needs and we do not initialize that data with any values at the time of their creation. It is a common pattern to use buffers to effectively wrap existing C++ allocations, which may already have been initialized with data. We can do this by passing a source of initial values to the buffer constructor. Doing so allows us to do several things, which we will see with the next example.

```cpp
// Create a buffer of 4 doubles and initialize it from a
// host pointer
double myDoubles[4] = {1.1, 2.2, 3.3, 4.4};
buffer b5{myDoubles, range{4}};

// Create a buffer of 5 doubles and initialize it from a
// host pointer to const double
const double myConstDbls[5] = {1.0, 2.0, 3.0, 4.0, 5.0};
buffer b6{myConstDbls, range{5}};

// Create a buffer from a shared pointer to int
auto sharedPtr = std::make_shared<int>(42);
buffer b7{sharedPtr, range{1}};
```  
Figure 7-3. Creating buffers, Part 2

In Figure 7-3, buffer b5 creates a one-dimensional buffer of four doubles. We pass the host pointer to the C array myDoubles to the buffer constructor in addition to the range that specifies the size of the buffer. Here we can make full use of CTAD to infer all the template arguments of our buffer. The host pointer we pass points to doubles, which gives us the data type of our buffer. The number of dimensions is automatically inferred from the one-dimensional range, which itself is inferred because it is created with only one number. Finally, the default allocator is used, so we do not have to specify that.

Passing a host pointer has a few ramifications of which we should be aware. By passing a pointer to host memory, we are promising the runtime that we will not try to access the host memory during the lifetime of the buffer. This is not (and cannot be) enforced by a SYCL implementation— it is our responsibility to ensure that we do not break this contract. One reason that we should not try to access this memory while the buffer is alive is that the buffer may choose to use different memory on the host to represent the buffer content, often for optimization reasons. If it does so, the values will be copied into this new memory from the host pointer. If subsequent kernels modify the buffer, the original host pointer will not reflect the updated values until certain specified synchronization points. We will talk more about when data gets written back to a host pointer later in this chapter.

Buffer b6 is very similar to buffer b5 with one major difference. This time, we are initializing the buffer with a pointer to const double. This means that we can only read values through the host pointer and not write them. However, the type for our buffer in this example is still double, not const double since the deduction guides do not take const-ness into consideration. This means that the buffer may be written to by a kernel, but we must use a different mechanism to update the host after the buffer has outlived its use (covered later in this chapter).

Buffers can also be initialized using C++ shared pointer objects. This is useful if our application already uses shared pointers, as this method of initialization will properly count the reference and ensure that the memory is not deallocated. Buffer b7 creates a buffer containing a single integer and initializes it using a shared pointer.

```cpp
// Create a buffer of ints from an input iterator
std::vector<int> myVec;
buffer b8{myVec.begin(), myVec.end()};
buffer b9{myVec};

// Create a buffer of 2x5 ints and 2 non-overlapping
// sub-buffers of 5 ints.
buffer<int, 2> b10{range{2, 5}};
buffer b11{b10, id{0, 0}, range{1, 5}};
buffer b12{b10, id{1, 0}, range{1, 5}};
```

## Figure 7-4. Creating buffers, Part 3

Containers are commonly used in modern C++ applications, with examples including std::array, std::vector, std::list, or std::map. We can initialize one-dimensional buffers using containers in two different ways. The first way, as shown in Figure 7-4 by buffer b8, uses input iterators. Instead of a host pointer, we pass two iterators to the buffer constructor, one representing the beginning of the data and another representing the end. The size of the buffer is computed as the number of elements returned by incrementing the start iterator until it equals the end iterator. This is useful for any data type that implements the C++ InputIterator interface. If the container object that provides the initial values for a buffer is also contiguous, then we can use an even simpler form to create the buffer. Buffer b9 creates a buffer from a vector simply by passing the vector to the constructor. The size of the buffer is determined by the size of the container being used to initialize it, and the type for the buffer data comes from the type of the container data. Creating buffers using this approach is common and recommended from containers such as std::vector and std::array.

The final example of buffer creation illustrates another feature of the buffer class. It is possible to create a sub-buffer, which is a view of a buffer from another buffer. A sub-buffer requires three things: a reference to a parent buffer, a base index, and the range of the sub-buffer. A subbuffer cannot be created from a sub-buffer. Multiple sub-buffers can be created from the same buffer, and they are free to overlap. Buffer b10 is created exactly like buffer b2, a two-dimensional buffer of integers with five integers per row. Next, we create two sub-buffers from buffer b10, sub-buffers b11 and b12. Sub-buffer b11 starts at index (0,0) and contains every element in the first row. Similarly, sub-buffer b12 starts at index (1,0) and contains every element in the second row. This yields two disjoint sub-buffers. Since the sub-buffers do not overlap, different kernels could operate on the different sub-buffers concurrently, but we will talk more about scheduling execution graphs and dependences in the next chapter.

```cpp
CHAPTER 7 BUFFERS

queue q;
int my_ints[42];

// Create a buffer of 42 ints
buffer<int> b{range(42));

// Create a buffer of 42 ints, initialize with a host
// pointer, and add the use_host_pointer property
buffer b1{my_ints,
        range(42),
        {property::buffer::use_host_ptr{}}}

// Create a buffer of 42 ints, initialize with a host
// pointer, and add the use_mutex property
std::mutex myMutex;
buffer b2{my_ints,
        range(42),
        {property::buffer::use_mutex{myMutex}}};
// Retrieve a pointer to the mutex used by this buffer
auto mutexPtr =
    b2.get_property<property::buffer::use_mutex>()
        .get_mutex_ptr();
// Lock the mutex until we exit scope
std::lock_guard<std::mutex> guard{*mutexPtr};

// Create a context-bound buffer of 42 ints, initialized
// from a host pointer
buffer b3{
    my_ints,
    range(42),
    {property::buffer::context_bound{q.get_context()}}};
```

## Figure 7-5. Buffer properties

## Buffer Properties

Buffers can also be created with special properties that alter their behavior. In Figure 7-5, we will walk through an example of the three different optional buffer properties and discuss how they might be used. Note that these properties are relatively uncommon in most codes.

## use\_host\_ptr

The first property that may be optionally specified during buffer creation is use\_host\_ptr. When present, this property requires the buffer to not allocate any memory on the host, and any allocator passed or specified on buffer construction is effectively ignored. Instead, the buffer must use the memory pointed to by a host pointer that is passed to the constructor. Note that this does not require the device to use the same memory to hold the buffer’s data. A device is free to cache the contents of a buffer in its attached memory. Also note that this property may only be used when a host pointer is passed to the constructor. This option can be useful when the program wants full control over all host memory allocations—for example, it allows programmers to try to minimize the memory footprint of an application.

In our example in Figure 7-5, we create a buffer b as we saw in our previous examples. We next create buffer b1 and initialize it with a pointer to myInts. We also pass the property use\_host\_ptr, which means that buffer b1 will only use the memory pointed to by myInts and not allocate any additional temporary storage on the host.

## use\_mutex

The next property, use\_mutex, concerns fine-grained sharing of memory between buffers and host code. Buffer b2 is created using this property. The property takes a reference to a mutex object that can later be queried from the buffer as we see in the example. This property also requires a host pointer be passed to the constructor, and it lets the runtime determine when it is safe to access updated values in host code through the provided host pointer. We cannot lock the mutex until the runtime guarantees that the host pointer sees the latest value of the buffer. While this could be combined with the use\_host\_ptr property, it is not required. use\_mutex is a mechanism that allows host code to access data within a buffer while

the buffer is still alive and without using the host accessor mechanism (described later). In general, the host accessor mechanism should be preferred unless we have a specific reason to use a mutex, particularly because there are no guarantees on how long it will take before the mutex will be successfully locked and the data ready for use by host code.

## context\_bound

The final property is shown in the creation of buffer b3 in our example. Here, our buffer of 42 integers is created with the context\_bound property. The property takes a reference to a context object. Normally, a buffer is free to be used on any device or context. However, if this property is used, it locks the buffer to the specified context. Attempting to use the buffer on another context will result in a runtime error. This could be useful for debugging programs by identifying cases where a kernel might be submitted to the wrong queue, for instance. In practice, we do not expect to see this property used in many programs, and the ability for buffers to be accessed on any device in any context is one of the most powerful properties of the buffer abstraction (which this property undoes).

## What Can We Do with a Buffer?

Many things can be done with buffer objects. We can query characteristics of a buffer, determine if and where any data is written back to host memory after the buffer is destroyed, or reinterpret a buffer as one with different characteristics. One thing that cannot be done, however, is to directly access the data that a buffer represents. Instead, we must create accessor objects to access the data, and we will learn all about this later in the chapter.

Examples of things that can be queried about a buffer include its range, the total number of data elements it represents, and the number of bytes required to store its elements. We can also query which allocator object is being used by the buffer and whether the buffer is a sub-buffer or not.

Updating host memory when a buffer is destroyed is an important aspect to consider when using buffers. Depending on how a buffer is created, host memory may or may not be updated with the results of a computation after buffer destruction. If a buffer is created and initialized from a host pointer to non-const data, that same pointer is updated with the latest data when the buffer is destroyed. However, there is also a way to update host memory regardless of how a buffer was created. The set\_final\_data method is a template method of buffer that can accept either a raw pointer, a C++ OutputIterator, or a std::weak\_ptr. When the buffer is destroyed, data contained by the buffer will be written to the host using the supplied location. Note that if the buffer was created and initialized from a host pointer to non-const data, it’s as if set\_final\_data was called with that pointer. Technically, a raw pointer is a special case of an OutputIterator. If the parameter passed to set\_final\_data is a std::weak\_ptr, the data is not written to the host if the pointer has expired or has already been deleted. Whether or not writeback occurs can also be controlled by the set\_write\_back method.

## Accessors

Data represented by a buffer cannot be directly accessed through the buffer object. Instead, we must create accessor objects that allow us to safely access a buffer’s data. Accessors inform the runtime where and how we want to access data, allowing the runtime to ensure that the right data is in the right place at the right time. This is a very powerful concept, especially when combined with the task graph that schedules kernels for execution based in part on data dependences.

Accessor objects are instantiated from the templated accessor class. This class has five template parameters. The first parameter is the type of the data being accessed. This should be the same as the type of data being stored by the corresponding buffer. Similarly, the second parameter describes the dimensionality of the data and buffer and defaults to a value of one.

<table><tr><td>Mode</td><td>Description</td></tr><tr><td>read</td><td>Read-only access</td></tr><tr><td>write</td><td>Write-only access preserving previous contents</td></tr><tr><td>read_write</td><td>Read and write access</td></tr></table>

## Figure 7-6. Access modes

The next three template parameters are unique to accessors. The first of these is the access mode. The access mode describes how we intend to use an accessor in a program. The possible modes are listed in Figure 7-6. We will learn how these modes are used to order the execution of kernels and perform data movement in Chapter 8. The access mode parameter does have a default value if none is specified or automatically inferred. If we do not specify otherwise, accessors will default to read\_write access mode for non-const data types and read for const data types. These defaults are always correct but providing more accurate information may improve a runtime’s ability to perform optimizations. When starting application development, it is safe and concise to simply not specify an access mode, and we can then refine the access modes based on profiling of performance-critical regions of the application.

<table><tr><td>Target</td><td>Description</td></tr><tr><td>device</td><td>Access a buffer via device global memory</td></tr><tr><td>host_task</td><td>Access a buffer from a host task</td></tr></table>

Figure 7-7. Access targets

The next template parameter is the access target. Buffers are an abstraction of data and do not describe where and how data is stored. The access target describes where we are accessing data. The two possible access targets are listed in Figure 7-7.

When using C++ with SYCL, there are only two targets: device and host\_task. The default template value is device, and this means that we intend to access a buffer’s data on a device. This is reasonable as accessors are most commonly used in operations on a device such as kernels or data transfers. The other access target is host\_task, which is used when a host task needs to access a buffer’s data.

Devices may have different types of memories available. In particular, many devices have some sort of fast local memory that is shared across multiple work-items in a work-group. Prior versions of SYCL had special access targets for local memory, but SYCL 2020 handles it in a different way. We will learn how to use work-group local memory in Chapter 9. Prior versions of SYCL also had a special access target for the host (outside of host tasks, which are new to SYCL 2020). This has been replaced with the new host\_accessor class, which provides access to a buffer’s data in host code. However, the access will remain valid for the lifetime of the host\_ accessor. Given that a buffer is locked to the host while a host\_accessor is valid, one should take special care to limit the scope of host\_accessor objects.

The final template parameter governs whether an accessor is a placeholder accessor or not. This is not a parameter that a programmer is likely to ever directly set and is usually deduced by which constructor call is used to create the accessor. A placeholder accessor is one that is declared outside of a command group but meant to be used to access data on a device inside a kernel. We will see what differentiates a placeholder accessor from one that is not once we look at examples of accessor creation.

While accessors can be extracted from a buffer object using its get\_access method, it’s simpler to directly create (construct) them. This is the style we will use in upcoming examples since it is very simple to understand and is compact.

## Accessor Creation

Figure 7-8 shows an example program with everything that we need to get started with accessors. In this example, we have three buffers, A, B, and C. The first parallel task we submit to the queue creates accessors to each buffer and defines a kernel that uses these accessors to initialize the buffers with some values. Each accessor is constructed with a reference to the buffer it will access as well as the handler object defined by the command group we’re submitting to the queue. This effectively binds the accessor to the kernel we’re submitting as part of the command group. Regular accessors are device accessors since they, by default, target global buffers stored in device memory. This is the most common use case.

```cpp
#include <cassert>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;
    // Create 3 buffers of 42 ints
    buffer<int> a_buf{range{N}};
    buffer<int> b_buf{range{N}};
    buffer<int> c_buf{range{N}};
    accessor pc{c_buf};

    q.submit([&](handler &h) {
        accessor a{a_buf, h};
        accessor b{b_buf, h};
        accessor c{c_buf, h};
        h.parallel_for(N, [=](id<1> i) {
            a[i] = 1;
            b[i] = 40;
            c[i] = 0;
        });
    });
    q.submit([&](handler &h) {
        accessor a{a_buf, h};
        accessor b{b_buf, h};
        accessor c{c_buf, h};
        h.parallel_for(N,
                                    [=](id<1> i) { c[i] += a[i] + b[i]; });
    });
    q.submit([&](handler &h) {
        h.require(pc);
        h.parallel_for(N, [=](id<1> i) { pc[i]++;
    });

    host_accessor result{c_buf};
    for (int i = 0; i < N; i++) {
        assert(result[i] == N);
    }
    return 0;
}
```

## Figure 7-8. Simple accessor creation

The second task we submit also defines three accessors to the buffers. We then use those accessors in the second kernel to add the elements of buffers A and B into buffer C. Since this second task operates on the same data as the first one, the runtime will execute this task after the first one is complete. We will learn about this in detail in the next chapter.

The third task shows how we can use a placeholder accessor. The accessor pC is declared at the beginning of the example in Figure 7-8 after we create our buffers. Note that the constructor is not passed a handler object since we don’t have one to pass. This lets us create a reusable accessor object ahead of time. However, in order to use this accessor inside a kernel, we need to bind it to a command group during submission. We do this using the handler object’s require method. Once we have bound our placeholder accessor to a command group, we can then use it inside a kernel as we would any other accessor.

Finally, we create a host\_accessor object in order to read the results of our computations back on the host. Note that this is a different type than we used inside our kernels. Note that the host accessor result in this example also does not take a handler object since we once again do not have one to pass. The special type for host accessors also lets us disambiguate them from placeholders. An important aspect of host accessors is that the constructor only completes when the data is available for use on the host, which means that construction of a host accessor can appear to take a long time. The constructor must wait for any kernels to finish executing that produce the data to be copied as well as for the copy itself to finish. Once the host accessor construction is complete, it is safe to use the data that it accesses directly on the host, and we are guaranteed that the latest version of the data is available to us on the host.

While this example is perfectly correct, we don’t say anything about how we intend to use our accessors when we create them. Instead, we use the default access mode, which is read\_write, for the non-const int data in our buffers. This is potentially overconservative and may

create unnecessary dependences between operations or superfluous data movement. A runtime may be able to do a better job if it has more information about how we plan to use the accessors we create. However, before we go through an example where we do this, we should first introduce one more tool—the deduction tag.

Deduction tags are a compact way to express the desired combination of access mode and target for an accessor. Deduction tags, when used, are passed as a parameter to an accessor’s constructor. The possible tags are shown in Figure 7-9. When an accessor is constructed with a tag parameter, C++ CTAD can then properly deduce the desired access mode and target, providing an easy way to override the default values for those template parameters. We could also manually specify the desired template parameters, but tags provide a simpler, more compact way to get the same result without spelling out fully templated accessors.

<table><tr><td>Tag value</td><td>access_mode::</td><td>target::</td></tr><tr><td>read_only</td><td>read</td><td>device</td></tr><tr><td>read_write</td><td>read_write</td><td>device</td></tr><tr><td>write_only</td><td>write</td><td>device</td></tr><tr><td>read_only_host_task</td><td>read</td><td>host_task</td></tr><tr><td>read_write_host_task</td><td>read_write</td><td>host_task</td></tr><tr><td>write_only_host_task</td><td>write</td><td>host_task</td></tr></table>

Figure 7-9. Deduction tags

Let’s take our previous example and rewrite it to add deduction tags. This new and improved example is shown in Figure 7-10.

```cpp
CHAPTER 7 BUFFERS

#include <cassert>
#include <sycl/sycl.hpp>
using namespace sycl;
constexpr int N = 42;

int main() {
    queue q;

    // Create 3 buffers of 42 ints
    buffer<int> buf_a{range{N}};
    buffer<int> buf_b{range{N}};
    buffer<int> buf_c{range{N}};

    accessor pc{buf_c};

    q.submit([&](handler &h) {
        accessor a{buf_a, h, write_only, no_init};
        accessor b{buf_b, h, write_only, no_init};
        accessor c{buf_c, h, write_only, no_init};
        h.parallel_for(N, [=](id<1> i) {
            a[i] = 1;
            b[i] = 40;
            c[i] = 0;
        });
    });
    q.submit([&](handler &h) {
        accessor a{buf_a, h, read_only};
        accessor b{buf_b, h, read_only};
        accessor c{buf_c, h, read_write};
        h.parallel_for(N,
                                    [=](id<1> i) { c[i] += a[i] + b[i]; });
    });
    q.submit([&](handler &h) {
        h.require(pc);
        h.parallel_for(N, [=](id<1> i) { pc[i]++;
    });

    host_accessor result{buf_c, read_only};

    for (int i = 0; i < N; i++) {
        assert(result[i] == N);
    }
    return 0;
}
```

Figure 7-10. Accessor creation with specified usage

We begin by declaring our buffers as we did in Figure 7-8. We also create our placeholder accessor that we’ll use later. Let’s now look at the first task we submit to the queue. Previously, we created our accessors by passing a reference to a buffer and the handler object for the command group. Now, we add two extra parameters to our constructor calls. The first new parameter is a deduction tag. Since this kernel is writing the initial values for our buffers, we use the write\_only deduction tag. This lets the runtime know that this kernel is producing new data and will not read from the buffer.

The second new parameter is an optional accessor property, similar to the optional properties for buffers that we saw earlier in the chapter. The property we pass, no\_init, lets the runtime know that the previous contents of the buffer can be discarded. This is useful because it can let the runtime eliminate unnecessary data movement. In this example, since the first task is writing the initial values for our buffers, it’s unnecessary for the runtime to copy the uninitialized host memory to the device before the kernel executes. The no\_init property is useful for this example, but it should not be used for read–modify–write cases or kernels where only some values in a buffer may be updated.

The second task we submit to our queue is identical to before, but now we add deduction tags to our accessors. Here, we add the tags read\_only to accessors aA and aB to let the runtime know that we will only read the values of buffers A and B through these accessors. The third accessor, aC, gets the read\_write deduction tag since we accumulate the sum of the elements of A and B into C. We explicitly use the tag in the example to be consistent, but this is unnecessary since the default access mode is read\_write.

The default usage is retained in the third task where we use our placeholder accessor. This remains unchanged from the simplified example we saw in Figure 7-8. Our final accessor, the host accessor result, now receives a deduction tag when we create it. Since we only read the final values on the host, we pass the read\_only tag to the constructor. If we rewrote the program in such a way that the host accessor was destroyed, launching another kernel that operated on buffer C would not require it to be written back to the device since the read\_only tag lets the runtime know that it will not be modified by the host.

## What Can We Do with an Accessor?

Many things can be done with an accessor object. However, the most important thing we can do is spelled out in the accessor’s name—access data. This is usually done through one of the accessor’s [] operators. We use the [] operator in our examples in Figures 7-8 and 7-10. This operator takes either an id object that can properly index multidimensional data or a single size\_t. The second case can be used when an accessor has more than one dimension. In that case, it returns an object that is then meant to be indexed again with [] until we arrive at a scalar value, and this would be of the form a[i][j] in a two-dimensional case. Remember that the ordering of accessor dimensions follows the convention of C++ where the rightmost dimension is the unit-stride dimension (iterates “fastest”).

An accessor can also return a pointer to the underlying data. This pointer can be accessed directly following normal C++ rules. Note that there can be additional complexity involved with respect to the address space of this pointer.

Many things can also be queried from an accessor object. Examples include the number of elements accessible through the accessor, the size in bytes of the region of the buffer it covers, or the range of data accessible.

Accessors provide a similar interface to C++ containers and may be used in many situations where containers may be passed. The container interface supported by accessors includes the data method, which is equivalent to get\_pointer, and several flavors of forward and backward iterators.

## Summary

In this chapter, we have learned about buffers and accessors. Buffers are an abstraction of data that hides the underlying details of memory management from the programmer. They do this in order to provide a simpler, higher-level abstraction. We went through several examples that showed us the different ways to construct buffers as well as the different optional properties that can be specified to alter their behavior. We learned how to initialize a buffer with data from host memory as well as how to write data back to host memory when we are done with a buffer.

Since we cannot access buffers directly, we learned how to access the data in a buffer by using accessor objects. We learned the difference between device accessors and host accessors. We discussed the different access modes and targets and how they inform the runtime how and where an accessor will be used by the program. We showed the simplest way to use accessors using the default access modes and targets, and we learned how to distinguish between a placeholder accessor and one that is not. We then saw how to further optimize the example program by giving the runtime more information about our accessor usage by adding deduction tags to our accessor declarations. Finally, we covered many of the different ways that accessors can be used in a program.

In the next chapter, we will learn in greater detail how the runtime can use the information we give it through accessors to schedule the execution of different kernels. We will also see how this information informs the runtime about when and how the data in buffers needs to be copied between the host and a device. We will learn how we can explicitly control data movement involving buffers—and USM allocations too.

![](images/a0be8fdb8b600de904d36c20e21c705fedefa87101b252b4f9a77cd47e91ba09.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
