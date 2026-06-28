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
