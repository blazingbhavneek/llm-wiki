## Understanding Explicit ND-Range Parallel Kernels

The execution range of an ND-range kernel is divided into work-groups, sub-groups, and work-items. The ND-range represents the total execution range, which is divided into work-groups of uniform size (i.e., the workgroup size must divide the ND-range size exactly in each dimension). Each work-group can be further divided by the implementation into sub-groups. Understanding the execution model defined for work-items and each type of group is an important part of writing correct and portable programs.

Figure 4-12 shows an example of an ND-range of size (8, 8, 8) divided into 8 work-groups of size (4, 4, 4). Each work-group contains 16 onedimensional sub-groups of 4 work-items. Pay careful attention to the

numbering of the dimensions: sub-groups are always one-dimensional, and so dimension 2 of the ND-range and work-group becomes dimension 0 of the sub-group.

![](images/76b5a0a803352008c821c3c0e1fce8989d83c979474810b6d29f6414c9ad8c01.jpg)  
Figure 4-12. Three-dimensional ND-range divided into work-groups, sub-groups, and work-items

The exact mapping from each type of group to hardware resources is implementation-defined, and it is this flexibility that enables programs to execute on a wide variety of hardware. For example, work-items could be executed completely sequentially, executed in parallel by hardware threads and/or SIMD instructions, or even executed by a hardware pipeline specifically configured for a kernel.

In this chapter, we are focused only on the semantic guarantees of the ND-range execution model in terms of a generic target platform, and we will not cover its mapping to any one platform. See Chapters 15, 16, and 17 for details of the hardware mapping and performance recommendations for GPUs, CPUs, and FPGAs, respectively.

## Work-Items

Work-items represent the individual instances of a kernel function. In the absence of other groupings, work-items can be executed in any order and cannot communicate or synchronize with each other except by way of atomic memory operations to global memory (see Chapter 19).

## Work-Groups

The work-items in an ND-range are organized into work-groups. Workgroups can execute in any order, and work-items in different work-groups cannot communicate with each other except by way of atomic memory operations to global memory (see Chapter 19). However, the work-items within a work-group have some scheduling guarantees when certain constructs are used, and this locality provides some additional capabilities:

1. Work-items in a work-group have access to workgroup local memory, which may be mapped to a dedicated fast memory on some devices (see Chapter 9).

2. Work-items in a work-group can synchronize using work-group barriers and guarantee memory consistency using work-group memory fences (see Chapter 9).

3. Work-items in a work-group have access to group functions, providing implementations of common communication routines (see Chapter 9) and group algorithms, providing implementations of common parallel patterns such as reductions and scans (see Chapter 14).

The number of work-items in a work-group is typically configured for each kernel at runtime, as the best grouping will depend upon both the amount of parallelism available (i.e., the size of the ND-range) and properties of the target device. We can determine the maximum number of work-items per work-group supported by a specific device using the query functions of the device class (see Chapter 12), and it is our responsibility to ensure that the work-group size requested for each kernel is valid.

There are some subtleties in the work-group execution model that are worth emphasizing.

First, although the work-items in a work-group are scheduled to a single compute unit, there need not be any relationship between the number of work-groups and the number of compute units. In fact, the number of work-groups in an ND-range can be many times larger than the number of work-groups that a given device can execute simultaneously! We may be tempted to try and write kernels that synchronize across work-groups by relying on very clever device-specific scheduling, but we strongly recommend against doing this—such kernels may appear to work today, but they are not guaranteed to work with future implementations and are highly likely to break when moved to a different device.

Second, although the work-items in a work-group are scheduled such that they can cooperate with one another, they are not required to provide any specific forward progress guarantees—executing the workitems within a work-group sequentially between barriers and collectives is a valid implementation. Communication and synchronization between work-items in the same work-group is only guaranteed to be safe when performed using the barrier and collective functions provided, and handcoded synchronization routines may deadlock.

# THINKING IN WORK-GROUPS

Work-groups are similar in many respects to the concept of a task in other programming models (e.g., Threading Building Blocks): tasks can execute in any order (controlled by a scheduler); it’s possible (and even desirable) to oversubscribe a machine with tasks; and it’s often not a good idea to try and implement a barrier across a group of tasks (as it may be very expensive or incompatible with the scheduler). If we’re already familiar with a task-based programming model, we may find it useful to think of work-groups as though they are data-parallel tasks.

## Sub-Groups

On many modern hardware platforms, subsets of the work-items in a work-group known as sub-groups are executed with additional scheduling guarantees. For example, the work-items in a sub-group could be executed simultaneously as a result of compiler vectorization, and/or the sub-groups themselves could be executed with strong forward progress guarantees because they are mapped to independent hardware threads.

When working with a single platform, it is tempting to bake assumptions about these execution models into our codes, but this makes them inherently unsafe and non-portable—they may break when moving between different compilers or even when moving between different generations of hardware from the same vendor!

Defining sub-groups as a core part of the language gives us a safe alternative to making assumptions that may later prove to be devicespecific. Leveraging sub-group functionality also allows us to reason about the execution of work-items at a low level (i.e., close to hardware) and is key to achieving very high levels of performance across many platforms.

## Chapter 4 Expressing Parallelism

As with work-groups, the work-items within a sub-group can synchronize, guarantee memory consistency, or execute common parallel patterns via group functions and group algorithms. However, there is no equivalent of work-group local memory for sub-groups (i.e., there is no sub-group local memory). Instead, the work-items in a sub-group can exchange data directly—without explicit memory operations—using a subset of the group algorithms colloquially known as “shuffle” operations (Chapter 9).

## WHY “SHUFFLE”?

The “shuffle” operations in languages like OpenCL, CUDA, and SPIR -V all include “shuffle” in their name (e.g., sub\_group\_shuffle, \_\_shfl, and OpGroupNonUniformShuffle). SYCL adopts a different naming convention to avoid confusion with the std::shuffle function defined in C++ (which randomly reorders the contents of a range).

Some aspects of sub-groups are implementation-defined and outside of our control. However, a sub-group has a fixed (one-dimensional) size for a given combination of device, kernel, and ND-range, and we can query this size using the query functions of the kernel class (see Chapters 10 and 12). By default, the number of work-items per sub-group is also chosen by the implementation—we can override this behavior by requesting a particular sub-group size at compile time but must ensure that the subgroup size we request is compatible with the device.

Like work-groups, the work-items in a sub-group are not required to provide any specific forward progress guarantees—an implementation is free to execute each work-item in a sub-group sequentially and only switch between work-items when a sub-group collective function is encountered. However, on some devices, all sub-groups within a work-group are guaranteed to execute (make progress) eventually, which is a cornerstone of several producer–consumer patterns. This is currently implementationdefined behavior, and so we cannot rely on sub-groups to make progress if we want our kernels to remain portable. We expect a future version of SYCL to provide device queries describing the progress guarantees of sub-groups.

When writing kernels for a specific device, the mapping of workitems to sub-groups is known, and our codes can often take advantage of properties of this mapping to improve performance. However, a common mistake is to assume that because our code works on one device, it will work on all devices. Figures 4-13 and 4-14 show just two of the possibilities when mapping work-items in a multidimensional kernel with a range of {4, 4} to sub-groups, for a maximum sub-group size of 8. The mapping in Figure 4-13 produces two sub-groups of eight work-items, while the mapping in Figure 4-14 produces four sub-groups of four work-items!

![](images/deb593e3e38ffcc24f8138d00e174f2d1eacf6811ec4191e7f84826ac5a4efac.jpg)  
Figure 4-13. One possible sub-group mapping, where the sub-group size is permitted to be larger than the extent of the highest-numbered (contiguous) dimension of the work-group, and so the sub-group appears to “wrap around”

![](images/112e7cd4f2254cbcbd915ffc4a74b84027b11ab39ce65cbfe12ecc9256ebfc1f.jpg)  
Figure 4-14. Another possible sub-group mapping, where the subgroup size is not permitted to be larger than the extent of the highestnumbered (contiguous) dimension of the work-group

SYCL does not currently provide a way to query how work-items are mapped to sub-groups nor a mechanism to request a specific mapping. The best ways to write portable code using sub-groups are using onedimensional work-groups or using multidimensional work-groups where the highest-numbered dimension is divisible by the kernel’s required subgroup size.

## THINKING IN SUB-GROUPS

If we are coming from a programming model that requires us to think about explicit vectorization, it may be useful to think of each sub-group as a set of work-items packed into a SIM D register, where each work-item in the subgroup corresponds to a SIM D lane. When multiple sub-groups are in flight simultaneously and a device guarantees they will make forward progress, this mental model extends to treating each sub-group as though it were a separate stream of vector instructions executing in parallel.

## Writing Explicit ND-Range Data-Parallel Kernels

```txt
range global{N, N};
range local{B, B};
h.parallel_for(nd_range{global, local},
            [=](nd_item<2> it) {
                int j = it.get_global_id(0);
                int i = it.get_global_id(1);

                for (int k = 0; k < N; ++k) {
                    c[j][i] += a[j][k] * b[k][i];
                }
            });
```

## Figure 4-15. Expressing a naïve matrix multiplication kernel with ND-range parallel\_for

Figure 4-15 reimplements the matrix multiplication kernel that we saw previously using the ND-range parallel kernel syntax, and the diagram in Figure 4-16 shows how the work in this kernel is mapped to the work-items in each work-group. Grouping our work-items in this way ensures locality of access and hopefully improves cache hit rates: for example, the workgroup in Figure 4-16 has a local range of (4, 4) and contains 16 work-items, but only accesses four times as much data as a single work-item—in other words, each value we load from memory can be reused four times.

![](images/eaadf88bc25a230a8c687d40ce20a4948de3fcbc41ee38f52fdc43b8c3a6a727.jpg)  
Figure 4-16. Mapping matrix multiplication to work-groups and work-items

So far, our matrix multiplication example has relied on a hardware cache to optimize repeated accesses to the A and B matrices from workitems in the same work-group. Such hardware caches are commonplace on traditional CPU architectures and are becoming increasingly common on GPU architectures, but several architectures have explicitly managed “scratchpad” memories that can deliver higher performance (e.g., via lower latency). ND-range kernels can use local accessors to describe allocations that should be placed in work-group local memory, and an implementation is then free to map these allocations to special memory (where it exists). Usage of this work-group local memory will be covered in Chapter 9.

## Details of Explicit ND-Range Data-Parallel Kernels

ND-range data-parallel kernels use different classes compared to basic data-parallel kernels: range is replaced by nd\_range, and item is replaced by nd\_item. There are also two new classes, representing the different types of groups to which a work-item may belong: functionality tied to work-groups is encapsulated in the group class, and functionality tied to sub-groups is encapsulated in the sub\_group class.

## The nd\_range Class

An nd\_range represents a grouped execution range using two instances of the range class: one denoting the global execution range and another denoting the local execution range of each work-group. A simplified definition of the nd\_range class is given in Figure 4-17.

It may be a little surprising that the nd\_range class does not mention sub-groups at all: the sub-group range is not specified during construction and cannot be queried. There are two reasons for this omission. First, subgroups are a low-level implementation detail that can be ignored for many kernels. Second, there are several devices supporting exactly one valid sub-group size and specifying this size everywhere would be unnecessarily verbose. All functionality related to sub-groups is encapsulated in a dedicated class that will be discussed shortly.

```cpp
template <int Dimensions = 1>
class nd_range {
  public:
    // Construct an nd_range from global and work-group local
    // ranges
    nd_range(range<Dimensions> global,
           range<Dimensions> local);

    // Return the global and work-group local ranges
    range<Dimensions> get_global_range() const;
    range<Dimensions> get_local_range() const;

    // Return the number of work-groups in the global range
    range<Dimensions> get_group_range() const;
};
```  
Figure 4-17. Simplified definition of the nd\_range class

## The nd\_item Class

An nd\_item is the ND-range form of an item, again encapsulating the execution range of the kernel and the item’s index within that range. Where nd\_item differs from item is in how its position in the range is queried and represented, as shown by the simplified class definition in Figure 4-18. For example, we can query the item’s index in the (global) ND-range using the get\_global\_id() function or the item’s index in its (local) parent workgroup using the get\_local\_id() function.

The nd\_item class also provides functions for obtaining handles to classes describing the group and sub-group that an item belongs to. These classes provide an alternative interface for querying an item’s index in an ND-range.

## Chapter 4 Expressing Parallelism

```lisp
template <int Dimensions = 1>
class nd_item {
  public:
    // Return the index of this item in the kernel's execution
    // range
    id<Dimensions> get_global_id() const;
    size_t get_global_id(int dimension) const;
    size_t get_global_linear_id() const;

    // Return the execution range of the kernel executed by
    // this item
    range<Dimensions> get_global_range() const;
    size_t get_global_range(int dimension) const;

    // Return the index of this item within its parent
    // work-group
    id<Dimensions> get_local_id() const;
    size_t get_local_id(int dimension) const;
    size_t get_local_linear_id() const;

    // Return the execution range of this item's parent
    // work-group
    range<Dimensions> get_local_range() const;
    size_t get_local_range(int dimension) const;

    // Return a handle to the work-group
    // or sub-group containing this item
    group<Dimensions> get_group() const;
    sub_group get_sub_group() const;
};
```  
Figure 4-18. Simplified definition of the nd\_item class

## The group Class

The group class encapsulates all functionality related to work-groups, and a simplified definition is shown in Figure 4-19.

```cpp
template <int Dimensions = 1>
class group {
  public:
    // Return the index of this group in the kernel's
    // execution range
    id<Dimensions> get_id() const;
    size_t get_id(int dimension) const;
    size_t get_linear_id() const;

    // Return the number of groups in the kernel's execution
    // range
    range<Dimensions> get_group_range() const;
    size_t get_group_range(int dimension) const;

    // Return the number of work-items in this group
    range<Dimensions> get_local_range() const;
    size_t get_local_range(int dimension) const;
};
```  
Figure 4-19. Simplified definition of the group class

Many of the functions that the group class provides each have equivalent functions in the nd\_item class: for example, calling group. get\_group\_id() is equivalent to calling item.get\_group\_id(), and calling group.get\_local\_range() is equivalent to calling item.get\_local\_ range(). If we are not using any group functions or algorithms, should we still use the group class? Wouldn’t it be simpler to use the functions in nd\_item directly, instead of creating an intermediate group object? There is a trade-off here: using group requires us to write slightly more code, but that code may be easier to read. For example, consider the code snippet in Figure 4-20: it is clear that body expects to be called by all work-items in the group, and it is clear that the range returned by get\_local\_range() in the body of the parallel\_for is the range of the group. The same code could very easily be written using only nd\_item, but it would likely be harder for readers to follow.

## Chapter 4 Expressing Parallelism

```txt
void body(group& g);

h.parallel_for(nd_range{global, local}, [=](nd_item<1> it) {
  group<1> g = it.get_group();
  range<1> r = g.get_local_range();
  ...
  body(g);
});
```

## Figure 4-20. Using the group class to improve readability

Another powerful option enabled by the group class is the ability to write generic group functions that accept any type of group via a template argument. Although SYCL does not (yet) define an official Group “concept” (in the C++20 sense), the group and sub\_group classes expose a common interface, allowing templated SYCL functions to be constrained using traits like sycl::is\_group\_v. Today, the primary advantages of this generic form of coding are the ability to support work-groups with an arbitrary number of dimensions, and the ability to allow the caller of a function to decide whether the function should divide work across the work-items in a work-group or the work-items in a sub-group. However, the SYCL group interface has been designed to be extensible, and we expect a larger number of classes representing different groupings of work-items to appear in future versions of SYCL.

## The sub\_group Class

The sub\_group class encapsulates all functionality related to subgroups, and a simplified definition is shown in Figure 4-21. Unlike with work-groups, the sub\_group class is the only way to access sub-group functionality; none of its functions are duplicated in nd\_item.

```cpp
class sub_group {
  public:
    // Return the index of the sub-group
    id<1> get_group_id() const;

    // Return the number of sub-groups in this item's parent
    // work-group
    range<1> get_group_range() const;

    // Return the index of the work-item in this sub-group
    id<1> get_local_id() const;

    // Return the number of work-items in this sub-group
    range<1> get_local_range() const;

    // Return the maximum number of work-items in any
    // sub-group in this item's parent work-group
    range<1> get_max_local_range() const;
};
```

## Figure 4-21. Simplified definition of the sub\_group class

Note that there are separate functions for querying the number of work-items in the current sub-group and the maximum number of workitems in any sub-group within the work-group. Whether and how these differ depends on exactly how sub-groups are implemented for a specific device, but the intent is to reflect any differences between the sub-group size targeted by the compiler and the runtime sub-group size. For example, very small work-groups may contain fewer work-items than the compiletime sub-group size, or sub-groups of different sizes may be used to handle work-groups and dimensions that are not divisible by the sub-group size.

## Mapping Computation to Work-Items
