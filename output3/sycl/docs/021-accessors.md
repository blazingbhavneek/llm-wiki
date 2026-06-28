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
