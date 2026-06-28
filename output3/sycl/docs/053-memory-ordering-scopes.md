
## Figure 19-6. Avoiding a data race using a barrier

Although using a barrier to implement this pattern is possible, it is not typically encouraged—it forces the work-items in a group to execute sequentially and in a specific order, which may lead to long periods of inactivity in the presence of load imbalance. It may also introduce more synchronization than is strictly necessary—if the different work-items happen to use different values of i, they will still be forced to synchronize at the barrier.

Barrier synchronization is a useful tool for ensuring that all work-items in a work-group or sub-group complete some stage of a kernel before proceeding to the next stage, but is too heavy-handed for fine-grained (and potentially data-dependent) synchronization. For more general synchronization patterns, we must look to atomic operations.

## Atomic Operations

Atomic operations enable concurrent access to a memory location without introducing a data race. When multiple atomic operations access the same memory, they are guaranteed not to overlap. Note that this guarantee does not apply if only some of the accesses use atomics and that it is our responsibility as programmers to ensure that we do not concurrently access the same data using operations with different atomicity guarantees.

Mixing atomic and non-atomic operations on the same memory location(s) at the same time results in undefined behavior!

If our simple addition is expressed using atomic operations, the result may look like Figure 19-8—each update is now an indivisible chunk of work, and our application will always produce the correct result. The corresponding code is shown in Figure 19-7—we will revisit the atomic\_ ref class and the meaning of its template arguments later in the chapter.

```cpp
int* data = malloc_shared<int>(N, q);
std::fill(data, data + N, 0);

q.parallel_for(N, [=](id<1> i) {
    int j = i % M;
    atomic_ref<int, memory_order::relaxed,
            memory_scope::system,
            access::address_space::global_space>
        atomic_data(data[j]);
    atomic_data += 1;
}).wait();

for (int i = 0; i < N; ++i) {
    std::cout << "data [" << i << "] = " << data[i] << "\n";
}
```  
Figure 19-7. Avoiding a data race using atomic operations

![](images/11bcb19a11df00a214cd4fee7218921a6ffe2f2d8fcbbb42aa278af3d9f83d15.jpg)  
Figure 19-8. An interleaving of data[i] += x executed concurrently with atomic operations

However, it is important to note that this is still only one possible execution order. Using atomic operations guarantees that the two updates do not overlap (if both threads use the same value of i), but there is still no guarantee as to which of the two threads will execute first. Even more importantly, there are no guarantees about how these atomic operations are ordered with respect to any non-atomic operations in different threads.

## Memory Ordering

Even within a sequential application, optimizing compilers and the hardware are free to reorder operations if they do not change the observable behavior of an application. In other words, the application must behave as if it ran exactly as it was written by the programmer.

Unfortunately, this as-if guarantee is not strong enough to help us reason about the execution of parallel programs. We now have two sources of reordering to worry about: the compiler and hardware may reorder the execution of statements within each sequential thread, and the threads themselves may be executed in any (possibly interleaved) order. To design and implement safe communication protocols between threads, we need to be able to constrain this reordering. By providing the compiler with information about our desired memory order, we can prevent reordering optimizations that are incompatible with the intended behavior of our applications.

Three commonly available memory orderings are:

1. A relaxed memory ordering

2. An acquire-release or release-acquire memory ordering

## 3. A sequentially consistent memory ordering

Under a relaxed memory ordering, memory operations can be reordered without any restrictions. The most common usage of a relaxed memory model is incrementing shared variables (e.g., a single counter, an array of values during a histogram computation).

Under an acquire-release memory ordering, one thread releasing an atomic variable and another thread acquiring the same atomic variable acts as a synchronization point between those two threads and guarantees that any prior writes to memory issued by the releasing thread are visible to the acquiring thread. Informally, we can think of atomic operations releasing side effects from other memory operations to other threads or acquiring the side effects of memory operations on other threads. Such a memory model is required if we want to communicate values between pairs of threads via memory, which may be more common than we would think. When a program acquires a lock, it typically goes on to perform some additional calculations and modify some memory before eventually releasing the lock—only the lock variable is ever updated atomically, but we expect memory updates guarded by the lock to be protected from data races. This behavior relies on an acquire-release memory ordering for correctness, and attempting to use a relaxed memory ordering to implement a lock will not work.

Under a sequentially consistent memory ordering, the guarantees of acquire-release ordering still hold, but there additionally exists a single global order of all atomic operations. The behavior of this memory ordering is the most intuitive of the three and the closest that we can get to the original as-if guarantee we are used to relying upon when developing sequential applications. With sequential consistency, it becomes significantly easier to reason about communication between groups (rather than pairs) of threads, since all threads must agree on the global ordering of all atomic operations.

Understanding which memory orders are supported by a combination of programming model and device is a necessary part of designing portable parallel applications. Being explicit in describing the memory order required by our applications ensures that they fail predictably (e.g., at compile time) when the behavior we require is unsupported and prevents us from making unsafe assumptions.

## The Memory Model

The chapter so far has introduced the concepts required to understand the memory model. The remainder of the chapter explains the memory model in detail, including

• How to express the memory ordering requirements of our kernels

• How to query the memory orders supported by a specific device

• How the memory model behaves with respect to disjoint address spaces and multiple devices

• How the memory model interacts with barriers, fences, and atomics

• How using atomic operations differs between buffers and USM

The memory model is based on the memory model of C++ but differs in some important ways. These differences reflect our long-term vision that SYCL should help inform the future of C++: the default behaviors and naming of classes are closely aligned with the C++ standard library and are intended to extend C++ functionality rather than to restrict it.

The table in Figure 19-9 summarizes how different memory model concepts are exposed as language features in C++ (C++11, C++14, C++17, C++20) vs. SYCL. The C++14, C++17, and C++20 standards additionally include some clarifications that impact implementations of C++. These clarifications should not affect the application code that we write, so we do not cover them here.

<table><tr><td>Feature</td><td>C++</td><td>SYCL</td></tr><tr><td>Atomic Objects</td><td>std::atomic</td><td>Not available.</td></tr><tr><td>Atomic References</td><td>std::atomic_ref (C++20 onwards)</td><td>sycl::atomic_ref</td></tr><tr><td>Memory Orders</td><td>relaxedconsumeacquirereleaseacq_relseq_cst</td><td>relaxedacquirereleaseacq_relseq_cst</td></tr><tr><td>Memory Scopes</td><td>Not available.Behavior of atomics and fences matches SYCL system scope.</td><td>work_itemsub_groupwork_groupdevicesystem</td></tr><tr><td>Fences</td><td>std::atomic_thread_fence</td><td>sycl::atomic_fence</td></tr><tr><td>Barriers</td><td>std::barrier (C++20 onwards)</td><td>sycl::group_barrier</td></tr><tr><td>Address Spaces</td><td>All memory is in a single (host) address space.</td><td>HostDevice (Global)Device (Local)Device (Private)Shared (USM)</td></tr></table>

Figure 19-9. Comparing C++ and SYCL memory models

## The memory\_order Enumeration Class

The memory model exposes different memory orders through five values of the memory\_order enumeration class (note: C++ “consume” is not part of SYCL), which can be supplied as arguments to fences and atomic operations. Supplying a memory order argument to an operation tells the compiler what memory ordering guarantees are required for all other memory operations (to any address) relative to that operation, as explained in the following:

## • memory\_order::relaxed

Read and write operations can be reordered before or after the operation with no restrictions. There are no ordering guarantees.

## • memory\_order::acquire

Read and write operations appearing after the operation in the program must occur after it (i.e., they cannot be reordered before the operation).

## • memory\_order::release

Read and write operations appearing before the operation in the program must occur before it (i.e., they cannot be reordered after the operation), and preceding write operations are guaranteed to be visible to other work-items which have been synchronized by a corresponding acquire operation (i.e., an atomic operation using the same variable and memory\_order::acquire or a barrier function).

## • memory\_order::acq\_rel

The operation acts as both an acquire and a release. Read and write operations cannot be reordered around the operation, and preceding writes must be made visible as previously described for memory\_ order::release.

## • memory\_order::seq\_cst

The operation acts as an acquire, release, or both depending on whether it is a read, write, or read–modify–write operation, respectively. All operations with this memory order are observed in a sequentially consistent order.

There are several restrictions on which memory orders are supported by each operation. The table in Figure 19-10 summarizes which combinations are valid.

<table><tr><td rowspan="2">Functions</td><td colspan="5">Supported memory_order Values</td></tr><tr><td>relaxed</td><td>acquire</td><td>release</td><td>acq_rel</td><td>seq_cst</td></tr><tr><td>load</td><td>✓</td><td>✓</td><td>✗</td><td>✗</td><td>✓</td></tr><tr><td>store</td><td>✓</td><td>✗</td><td>✓</td><td>✗</td><td>✓</td></tr><tr><td>exchange compare_exchange_* fetch_*</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>fence</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr></table>

Figure 19-10. Supporting atomic operations with memory\_order

Load operations do not write values to memory and are therefore incompatible with release semantics. Similarly, store operations do not read values from memory and are therefore incompatible with acquire semantics. The remaining read–modify–write atomic operations and fences are compatible with all memory orderings.

## MEMORY ORDER IN C++

The C++ memory model additionally includes memory\_order::consume, with similar behavior to memory\_order::acquire. However, C++17 discourages its use, noting that its definition is being revised. Its inclusion in SYCL has therefore been left to consider for a future specification.

## The memory\_scope Enumeration Class

The C++ memory model assumes that applications execute on a single device with a single address space. Neither of these assumptions holds for SYCL applications: various parts of the application execute on different

devices (i.e., a host and one or more accelerator devices); each device has multiple address spaces (i.e., private, local, and global); and the global address space of each device may or may not be disjoint (depending on USM support).

To address this, SYCL extends the C++ notion of memory order to include the scope of an atomic operation, denoting the minimum set of work-items to which a given memory ordering constraint applies. The set of scopes are defined by way of a memory\_scope enumeration class:

## • memory\_scope::work\_item

The memory ordering constraint applies only to the calling work-item. This scope is only useful for image operations, as all other operations within a work-item are already guaranteed to execute in program order.

## • memory\_scope::sub\_group, memory\_scope::work\_group

The memory ordering constraint applies only to work-items in the same sub-group or work-group as the calling work-item.

## • memory\_scope::device

The memory ordering constraint applies only to work-items executing on the same device as the calling work-item.

## • memory\_scope::system

The memory ordering constraint applies to all workitems in the system.

Barring restrictions imposed by the capabilities of a device, all memory scopes are valid arguments to all atomic and fence operations. However, a scope argument may be automatically demoted to a narrower scope in one of three situations:

1. If an atomic operation updates a value in workgroup local memory, any scope broader than memory\_scope::work\_group is narrowed (because local memory is only visible to work-items in the same work-group).

2. If a device does not support USM, specifying memory\_scope::system is always equivalent to memory\_scope::device (because buffers cannot be accessed concurrently by multiple devices).

3. If an atomic operation uses memory\_order::relaxed, there are no ordering guarantees, and the memory scope argument is effectively ignored.

## Querying Device Capabilities

To ensure compatibility with devices supported by previous versions of SYCL and to maximize portability, SYCL supports OpenCL 1.2 devices and other hardware that may not be capable of supporting the full C++ memory model (e.g., certain classes of embedded devices). SYCL provides device queries to help us reason about the memory order(s) and memory scope(s) supported by the devices available in a system:

• atomic\_memory\_order\_capabilities

Return a list of all memory orderings supported by atomic operations on a specific device. All devices are required to support at least memory\_order::relaxed.

## • atomic\_fence\_order\_capabilities

Return a list of all memory orderings supported

by fence operations on a specific device.

All devices are required to support at least

memory\_order::relaxed, memory\_order::acquire,

memory\_order::release, and memory\_order::acq\_rel.

Note that the minimum requirement for fences is

stronger than the minimum requirement for atomic

operations, since such fences are essential for

reasoning about memory order in the presence of

• atomic\_memory\_scope\_capabilities

atomic\_fence\_scope\_capabilities

Return a list of all memory scopes supported by

atomic and fence operations on a specific device.

All devices are required to support at least

memory\_order::work\_group.

It may be difficult at first to remember which memory orders and scopes are supported for which combinations of function and device capability. In practice, we can avoid much of this complexity by following one of the two development approaches outlined in the following:

## 1. Develop applications with sequential consistency and system fences.

Only consider adopting less strict memory orders

during performance tuning.

## 2. Develop applications with relaxed consistency and work-group fences.

Only consider adopting more strict memory orders and broader memory scopes where required for correctness.

The first approach ensures that the semantics of all atomic operations and fences match the default behavior of C++. This is the simplest and least error-prone option but has the worst performance and portability characteristics.

The second approach is more aligned with the default behavior of previous versions of SYCL and languages like OpenCL. Although more complicated—since it requires that we become more familiar with the different memory orders and scopes—it ensures that the majority of the SYCL code we write will work on any device without performance penalties.

## Barriers and Fences
