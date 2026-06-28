
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
