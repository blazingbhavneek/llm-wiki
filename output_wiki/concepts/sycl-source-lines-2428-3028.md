# sycl Source Lines 2428-3028

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L2428-L3028

Citation: [sycl:L2428-L3028]

````text
# Expressing Parallelism

We already know how to place code (Chapter 2) and data (Chapter 3) on a device—all we must do now is engage in the art of deciding what to do with it. To that end, we now shift to fill in a few things that we have conveniently left out or glossed over so far. This chapter marks the transition from simple teaching examples toward real-world parallel code and expands upon details of the code samples we have casually shown in prior chapters.

Writing our first program in a new parallel language may seem like a daunting task, especially if we are new to parallel programming. Language specifications are not written for application developers and often assume some familiarity with terminology; they do not contain answers to questions like these:

• Why is there more than one way to express parallelism?

• Which method of expressing parallelism should I use?

• How much do I really need to know about the execution model?

This chapter seeks to address these questions and more. We introduce the concept of a data-parallel kernel, discuss the strengths and weaknesses of the different kernel forms using working code examples, and highlight the most important aspects of the kernel execution model.

## Parallelism Within Kernels

Parallel kernels have emerged in recent years as a powerful means of expressing data parallelism. The primary design goals of a kernelbased approach are portability across a wide range of devices and high programmer productivity. As such, kernels are typically not hard-coded to work with a specific number or configuration of hardware resources (e.g., cores, hardware threads, SIMD [single instruction, multiple data] instructions). Instead, kernels describe parallelism in terms of abstract concepts that an implementation (i.e., the combination of compiler and runtime) can then map to the hardware parallelism available on a specific target device. Although this mapping is implementation-defined, we can (and should) trust implementations to select a mapping that is sensible and capable of effectively exploiting hardware parallelism.

Exposing a great deal of parallelism in a hardware-agnostic way ensures that applications can scale up (or down) to fit the capabilities of different platforms, but…

Guaranteeing functional portability is not the same as guaranteeing high performance!

There is a significant amount of diversity in the devices supported, and we must remember that different architectures are designed and optimized for different use cases. Whenever we hope to achieve the highest levels of performance on a specific device, we should always expect that some additional manual optimization work will be required— regardless of the programming language we are using! Examples of such device-specific optimizations include blocking for a particular cache size, choosing a work grain size that amortizes scheduling overheads, making use of specialized instructions or hardware units, and, most importantly, choosing an appropriate algorithm. Some of these examples will be revisited in Chapters 15, 16, and 17.

Striking the right balance between performance, portability, and productivity during application development is a challenge that we must all face—and a challenge that this book cannot address in its entirety. However, we hope to show that C++ with SYCL provides all the tools required to maintain both generic portable code and optimized targetspecific code using a single high-level programming language. The rest is left as an exercise to the reader!

## Loops vs. Kernels

An iterative loop is an inherently serial construct: each iteration of the loop is executed sequentially (i.e., in order). An optimizing compiler may be able to determine that some or all iterations of a loop can execute in parallel, but it must be conservative—if the compiler is not smart enough or does not have enough information to prove that parallel execution is always safe, it must preserve the loop’s sequential semantics for correctness.

```txt
for (int i = 0; i < N; ++i) {
    c[i] = a[i] + b[i];
}
```

## Figure 4-1. Expressing a vector addition as a serial loop

Consider the loop in Figure 4-1, which describes a simple vector addition. Even in a simple case like this, proving that the loop can be executed in parallel is not trivial: parallel execution is only safe if c does not overlap a or b, which in the general case cannot be proven without a runtime check! In order to address situations like this, languages have added features enabling us to provide compilers with extra information that may simplify analysis (e.g., asserting that pointers do not overlap with restrict) or to override all analysis altogether (e.g., declaring that all iterations of a loop are independent or defining exactly how the loop should be scheduled to parallel resources).

The exact meaning of a parallel loop is somewhat ambiguous—due to overloading of the term by different parallel programming languages and runtimes—but many common parallel loop constructs represent compiler transformations applied to sequential loops. Such programming models enable us to write sequential loops and only later provide information about how different iterations can be executed safely in parallel. These models are very powerful, integrate well with other state-of-the-art compiler optimizations, and greatly simplify parallel programming, but do not always encourage us to think about parallelism at an early stage of development.

A parallel kernel is not a loop and does not have iterations. Rather, a kernel describes a single operation, which can be instantiated many times and applied to different input data; when a kernel is launched in parallel, multiple instances of that operation may be executed simultaneously.

```txt
launch N kernel instances {
    int id =
        get_instance_id();  // unique identifier in [0, N)
    c[id] = a[id] + b[id];
}
```

## Figure 4-2. Loop rewritten (in pseudocode) as a parallel kernel

Figure 4-2 shows our simple loop example rewritten as a kernel using pseudocode. The opportunity for parallelism in this kernel is clear and explicit: the kernel can be executed in parallel by any number of instances, and each instance independently applies to a separate piece of data. By writing this operation as a kernel, we are asserting that it is safe to run in parallel (and that it ideally should be run in parallel).

In short, kernel-based programming is not a way to retrofit parallelism into existing sequential codes, but a methodology for writing explicitly parallel applications.

The sooner that we can shift our thinking from parallel loops to kernels, the easier it will be to write effective parallel programs using C++ with SYCL.

## Multidimensional Kernels

The parallel constructs of many other languages are one-dimensional, mapping work directly to a corresponding one-dimensional hardware resource (e.g., number of hardware threads). Parallel kernels in SYCL are a higher-level concept than this, and their dimensionality is more reflective of the problems that our codes are typically trying to solve (in a one-, two-, or three-dimensional space).

However, we must remember that the multidimensional indexing provided by parallel kernels is a programmer convenience that may be implemented on top of an underlying one-dimensional space. Understanding how this mapping behaves can be an important part of certain optimizations (e.g., tuning memory access patterns).

One important consideration is which dimension is contiguous or unitstride (i.e., which locations in the multidimensional space are next to each other in a one-dimensional mapping). All multidimensional quantities related to parallelism in SYCL use the same convention: dimensions are numbered from 0 to N-1, where dimension N-1 corresponds to the contiguous dimension. Wherever a multidimensional quantity is written as a list (e.g., in constructors) or a class supports multiple subscript operators, this numbering applies left to right (starting with dimension 0 on the left). This convention is consistent with the behavior of multidimensional arrays in standard C++.

An example of mapping a two-dimensional space to a linear index using the SYCL convention is shown in Figure 4-3. We are of course free to break from this convention and adopt our own methods of linearizing indices, but must do so carefully—breaking from the SYCL convention may have a negative performance impact on devices that benefit from strideone accesses.

<table><tr><td rowspan="2">dimension 0 (non-contiguous)</td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td><td>13</td><td>14</td><td>15</td></tr></table>

Figure 4-3. Two-dimensional range of size (2, 8) mapped to linear indices

If an application requires more than three dimensions, we must take responsibility for mapping between multidimensional and linear indices manually, using modulo arithmetic or other techniques.

## Overview of Language Features

Once we have decided to write a parallel kernel, we must decide what type of kernel we want to launch and how to represent it in our program. There are a multitude of ways to express parallel kernels, and we need to familiarize ourselves with each of these options if we want to master the language.

## Separating Kernels from Host Code

We have several alternative ways to separate host and device code, which we can mix and match within an application: C++ lambda expressions or function objects, kernels defined via an interoperability interface

(e.g., OpenCL C source strings), or binaries. Some of these options were already covered in Chapter 2, and the others will be covered in detail in Chapters 10 and 20.

The fundamental concepts of expressing parallelism are shared by all these options. For consistency and brevity, all the code examples in this chapter express kernels using C++ lambda expressions.

## LAMBDA EXPRESSIONS NOT CONSIDERED HARMFUL

There is no need to fully understand everything that the C++ specification says about lambda expressions in order to get started with SYCL—all we need to know is that the body of the lambda expression represents the kernel and that variables captured (by value) will be passed to the kernel as arguments.

There is no performance impact arising from the use of lambda expressions instead of more verbose mechanisms for defining kernels. A C++ compiler with SYCL support always understands when a lambda expression represents the body of a parallel kernel and can optimize for parallel execution accordingly.

For a refresher on C++ lambda expressions, with notes about their use in SYCL, see Chapter 1. For more specific details on using lambda expressions to define kernels, see Chapter 10.

## Different Forms of Parallel Kernels

There are three different kernel forms in SYCL, supporting different execution models and syntax. It is possible to write portable kernels using any of the kernel forms, and kernels written in any form can be tuned to achieve high performance on a wide variety of device types. However,

there will be times when we may want to use a specific form to make a specific parallel algorithm easier to express or to make use of an otherwise inaccessible language feature.

The first form is used for basic data-parallel kernels and offers the gentlest introduction to writing kernels. With basic kernels, we sacrifice control over low-level features like scheduling to make the expression of the kernel as simple as possible. How the individual kernel instances are mapped to hardware resources is controlled entirely by the implementation, and so as basic kernels grow in complexity, it becomes harder and harder to reason about their performance.

The second form extends basic kernels to provide access to low-level performance-tuning features. This second form is known as ND-range (N-dimensional range) data parallel for historical reasons, and the most important thing to remember is that it enables certain kernel instances to be grouped together, allowing us to exert some control over data locality and the mapping between individual kernel instances and the hardware resources that will be used to execute them.

The third form offers an experimental alternative syntax for expressing ND-range kernels using syntax similar to nested parallel loops. This third form is referred to as hierarchical data parallel, referring to the hierarchy of the nested constructs that appear in user source code. Compiler support for this syntax is still immature, and many SYCL implementations do not implement hierarchical data-parallel kernels as efficiently as the other two forms. The syntax is also incomplete, in the sense that there are many performance-enabling features of SYCL that are incompatible with or inaccessible from hierarchical kernels. Hierarchical parallelism in SYCL is in the process of being updated, and the SYCL specification includes a note recommending that new codes refrain from using hierarchical parallelism until the feature is ready; in keeping with the spirit of this note, the remainder of this book teaches only basic and ND-range parallelism.

We will revisit how to choose between the different kernel forms again at the end of this chapter once we have discussed their features in more detail.

## Basic Data-Parallel Kernels

The most basic form of parallel kernel is appropriate for operations that are embarrassingly parallel (i.e., operations that can be applied to every piece of data completely independently and in any order). By using this form, we give an implementation complete control over the scheduling of work. It is thus an example of a descriptive programming construct—we describe that the operation is embarrassingly parallel, and all scheduling decisions are made by the implementation.

Basic data-parallel kernels are written in a single program, multiple data (SPMD) style—a single “program” (the kernel) is applied to multiple pieces of data. Note that this programming model still permits each instance of the kernel to take different paths through the code, because of data-dependent branches.

One of the greatest strengths of a SPMD programming model is that it allows the same “program” to be mapped to multiple levels and types of parallelism, without any explicit direction from us. Instances of the same program could be pipelined, packed together and executed with SIMD instructions, distributed across multiple hardware threads, or a mix of all three.

## Understanding Basic Data-Parallel Kernels

The execution space of a basic parallel kernel is referred to as its execution range, and each instance of the kernel is referred to as an item. This is represented diagrammatically in Figure 4-4.

![](images/a7d5c4ad52881b094b413465bb355b3ee88ecd91a6ac46fe6212e1988ca81e4c.jpg)  
Figure 4-4. Execution space of a basic parallel kernel, shown for a 2D range of 64 items

The execution model of basic data-parallel kernels is very simple: it allows for completely parallel execution but does not guarantee or require it. Items can be executed in any order, including sequentially on a single hardware thread (i.e., without any parallelism)! Kernels that assume that all items will be executed in parallel (e.g., by attempting to synchronize items) could therefore very easily cause programs to hang on some devices.

However, to guarantee correctness, we must always write our kernels under the assumption that they could be executed in parallel. For example, it is our responsibility to ensure that concurrent accesses to memory are appropriately guarded by atomic memory operations (see Chapter 19) to prevent race conditions.

## Writing Basic Data-Parallel Kernels

Basic data-parallel kernels are expressed using the parallel\_for function. Figure 4-5 shows how to use this function to express a vector addition, which is our take on “Hello, world!” for parallel accelerator programming.

```javascript
h.parallel_for(range{N}, [=](id<1> idx) {
    c[idx] = a[idx] + b[idx];
});
```

## Figure 4-5. Expressing a vector addition kernel with parallel\_for

The function only takes two arguments: the first is a range (or integer) specifying the number of items to launch in each dimension, and the second is a kernel function to be executed for each index in the range. There are several different classes that can be accepted as arguments to a kernel function, and which should be used depends on which class exposes the functionality required—we’ll revisit this later.

Figure 4-6 shows a very similar use of this function to express a matrix addition, which is (mathematically) identical to vector addition except with two-dimensional data. This is reflected by the kernel—the only difference between the two code snippets is the dimensionality of the range and id classes used! It is possible to write the code this way because a SYCL accessor can be indexed by a multidimensional id. As strange as it looks, this can be very powerful, enabling us to write generic kernels templated on the dimensionality of our data.

```javascript
h.parallel_for(range{N, M}, [=](id<2> idx) {
    c[idx] = a[idx] + b[idx];
});
```

## Figure 4-6. Expressing a matrix addition kernel with parallel\_for

It is more common in C/C++ to use multiple indices and multiple subscript operators to index multidimensional data structures, and this explicit indexing is also supported by accessors. Using multiple indices in this way can improve readability when a kernel operates on data of different dimensionalities simultaneously or when the memory access patterns of a kernel are more complicated than can be described by using an item’s id directly.

For example, the matrix multiplication kernel in Figure 4-7 must extract the two individual components of the index in order to be able to describe the dot product between rows and columns of the two matrices. In the authors’ opinion, consistently using multiple subscript operators (e.g., [j][k]) is more readable than mixing multiple indexing modes and constructing two-dimensional id objects (e.g., id(j,k)), but this is simply a matter of personal preference.

The examples in the remainder of this chapter all use multiple subscript operators, to ensure that there is no ambiguity in the dimensionality of the buffers being accessed.

```javascript
h.parallel_for(range{N, N}, [=](id<2> idx) {
    int j = idx[0];
    int i = idx[1];
    for (int k = 0; k < N; ++k) {
        c[j][i] +=
            a[j][k] * b[k][i];   // or c[idx] += a[id(j,k)]
                                        // * b[id(k,i)];
    }
});
```

Figure 4-7. Expressing a naïve matrix multiplication kernel for square matrices, with parallel\_for

![](images/8913704a9ff905cb24d5dcf623affa601163d49a2c205fb867368040fa5c6330.jpg)  
Figure 4-8. Mapping matrix multiplication work to items in the execution range

The diagram in Figure 4-8 shows how the work in our matrix multiplication kernel is mapped to individual items. Note that the number of items is derived from the size of the output range and that the same input values may be read by multiple items: each item computes a single value of the C matrix, by iterating sequentially over a (contiguous) row of the A matrix and a (noncontiguous) column of the B matrix.

## Details of Basic Data-Parallel Kernels

The functionality of basic data-parallel kernels is exposed via three C++ classes: range, id, and item. We have already seen the range and id classes a few times in previous chapters, but we revisit them here with a different focus.

## The range Class

A range represents a one-, two-, or three-dimensional range. The dimensionality of a range is a template argument and must therefore be known at compile time, but its size in each dimension is dynamic and is passed to the constructor at runtime. Instances of the range class are used to describe both the execution ranges of parallel constructs and the sizes of buffers.

A simplified definition of the range class, showing the constructors and various methods for querying its extent, is shown in Figure 4-9.

```cpp
template <int Dimensions = 1>
class range {
  public:
    // Construct a range with one, two or three dimensions
    range(size_t dim0);
    range(size_t dim0, size_t dim1);
    range(size_t dim0, size_t dim1, size_t dim2);

    // Return the size of the range in a specific dimension
    size_t get(int dimension) const;
    size_t &operator[](int dimension);
    size_t operator[](int dimension) const;

    // Return the product of the size of each dimension
    size_t size() const;

    // Arithmetic operations on ranges are also supported
};
```  
Figure 4-9. Simplified definition of the range class

## The id Class

An id represents an index into a one-, two-, or three-dimensional range. The definition of id is similar in many respects to range: its dimensionality must also be known at compile time, and it may be used to index an individual instance of a kernel in a parallel construct or an offset into a buffer.

As shown by the simplified definition of the id class in Figure 4-10, an id is conceptually nothing more than a container of one, two, or three integers. The operations available to us are also very simple: we can query the component of an index in each dimension, and we can perform simple arithmetic to compute new indices.

Although we can construct an id to represent an arbitrary index, to obtain the id associated with a specific kernel instance, we must accept it (or an item containing it) as an argument to a kernel function. This id (or values returned by its member functions) must be forwarded to any function in which we want to query the index—there are not currently any free functions for querying the index at arbitrary points in a program, but this may be simplified in a future version of SYCL.

Each instance of a kernel accepting an id knows only the index in the range that it has been assigned to compute and knows nothing about the range itself. If we want our kernel instances to know about their own index and the range, we need to use the item class instead.

```cpp
template <int Dimensions = 1>
class id {
  public:
    // Construct an id with one, two or three dimensions
    id(size_t dim0);
    id(size_t dim0, size_t dim1);
    id(size_t dim0, size_t dim1, size_t dim2);

    // Return the component of the id in a specific dimension
    size_t get(int dimension) const;
    size_t &operator[](int dimension);
    size_t operator[](int dimension) const;

    // Arithmetic operations on ids are also supported
};
```  
Figure 4-10. Simplified definition of the id class

## The item Class

An item represents an individual instance of a kernel function, encapsulating both the execution range of the kernel and the instance’s index within that range (using a range and an id, respectively). Like range and id, its dimensionality must be known at compile time.

A simplified definition of the item class is given in Figure 4-11. The main difference between item and id is that item exposes additional functions to query properties of the execution range (e.g., its size) and a convenience function to compute a linearized index. As with id, the only way to obtain the item associated with a specific kernel instance is to accept it as an argument to a kernel function.

```cpp
template <int Dimensions = 1, bool WithOffset = true>
class item {
    public:
        // Return the index of this item in the kernel's execution
        // range
        id<Dimensions> get_id() const;
        size_t get_id(int dimension) const;
        size_t operator[](int dimension) const;

        // Return the execution range of the kernel executed by
        // this item
        range<Dimensions> get_range() const;
        size_t get_range(int dimension) const;

        // Return the offset of this item (if WithOffset == true)
        id<Dimensions> get_offset() const;

        // Return the linear index of this item
        // e.g. id(0) * range(1) * range(2) + id(1) * range(2) +
        // id(2)
        size_t get_linear_id() const;
};
```  
Figure 4-11. Simplified definition of the item class

## Explicit ND-Range Kernels

The second form of parallel kernel replaces the flat execution range of basic data-parallel kernels with an execution range where items belong to groups. This form is most appropriate for cases where we would like to express some notion of locality within our kernels. Different behaviors are defined and guaranteed for different types of groups, giving us more insight into and/or control over how work is mapped to specific hardware platforms.

These explicit ND-range kernels are thus an example of a more prescriptive parallel construct—we prescribe a mapping of work to each type of group, and the implementation must obey that mapping. However, it is not completely prescriptive, as the groups themselves may execute in any order and an implementation retains some freedom over how each type of group is mapped to hardware resources. This combination of prescriptive and descriptive programming enables us to design and tune our kernels for locality without destroying their portability.

Like basic data-parallel kernels, ND-range kernels are written in a SPMD style where all work-items execute the same kernel “program” applied to multiple pieces of data. The key difference is that each program instance can query its position within the groups that contain it and can access additional functionality specific to each type of group (see Chapter 9).

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

Most of the code examples so far have assumed that each instance of a kernel function corresponds to a single operation on a single piece of data. This is a straightforward way to write kernels, but such a one-to-one mapping is not dictated by SYCL or any of the kernel forms—we always have complete control over the assignment of data (and computation) to individual work-items and making this assignment parameterizable can be a good way to improve performance portability.

## One-to-One Mapping

When we write kernels such that there is a one-to-one mapping of work to work-items, those kernels must always be launched with a range or nd\_range with a size exactly matching the amount of work that needs to be done. This is the most obvious way to write kernels, and in many cases, it works very well—we can trust an implementation to map work-items to hardware efficiently.

However, when tuning for performance on a specific combination of system and implementation, it may be necessary to pay closer attention to low-level scheduling behaviors. The scheduling of work-groups to compute resources is implementation-defined and could potentially be dynamic (i.e., when a compute resource completes one work-group, the next work-group it executes may come from a shared queue). The impact of dynamic scheduling on performance is not fixed, and its significance depends upon factors including the execution time of each instance of the kernel function and whether the scheduling is implemented in software (e.g., on a CPU) or hardware (e.g., on a GPU).

## Many-to-One Mapping

The alternative is to write kernels with a many-to-one mapping of work to work-items. The meaning of the range changes subtly in this case: the range no longer describes the amount of work to be done, but rather the number of workers to use. By changing the number of workers and the amount of work assigned to each worker, we can fine-tune work distribution to maximize performance.

Writing a kernel of this form requires two changes:

1. The kernel must accept a parameter describing the total amount of work.

2. The kernel must contain a loop assigning work to work-items.

A simple example of such a kernel is given in Figure 4-22. Note that the loop inside the kernel has a slightly unusual form—the starting index is the work-item’s index in the global range, and the stride is the total number of work-items. This round-robin scheduling of data to work-items ensures that all N iterations of the loop will be executed by a work-item, but also that linear work-items access contiguous memory locations (to improve cache locality and vectorization behavior). Work can be similarly distributed across groups or the work-items in individual groups to further improve locality.

```txt
size_t N = ...;  // amount of work
size_t W = ...;  // number of workers
h.parallel_for(range{W}, [=](item<1> it) {
    for (int i = it.get_id()[0]; i < N;
        i += it.get_range()[0]) {
        output[i] = function(input[i]);
    }
});
```

## Figure 4-22. Kernel with separate data and execution ranges

These work distribution patterns are common, and we expect that future versions of SYCL will introduce syntactic sugar to simplify the expression of work distribution in ND-range kernels.

## Choosing a Kernel Form

Choosing between the different kernel forms is largely a matter of personal preference and heavily influenced by prior experience with other parallel programming models and languages.

The other main reason to choose a specific kernel form is that it is the only form to expose certain functionality required by a kernel. Unfortunately, it can be difficult to identify which functionality will be required before development begins—especially while we are still unfamiliar with the different kernel forms and their interaction with various classes.

We have constructed two guides based on our own experience to help us navigate this complex space. These guides should be considered initial suggestions and are definitely not intended to replace our own experimentation—the best way to choose between the different kernel forms will always be to spend some time writing in each of them, in order to learn which form is the best fit for our application and development style.

The first guide is the flowchart in Figure 4-23, which selects a kernel form based on

1. Whether we have previous experience with parallel programming

2. Whether we are writing a new code from scratch or are porting an existing parallel program written in a different language

3. Whether our kernel is embarrassingly parallel or reuses data between different instances of the kernel function

4. Whether we are writing a new kernel in SYCL to maximize performance, to improve the portability of our code, or because it provides a more productive means of expressing parallelism than lower-level languages

![](images/e4825e67893dda20e28e6c7b749d54deea12cf80627011e3a01eda5c4d54b8b6.jpg)  
Figure 4-23. Helping choose the right form for our kernel

The second guide is the set of features exposed to each of the kernel forms. Work-groups, sub-groups, group barriers, group-local memory, group functions (e.g., broadcast), and group algorithms (e.g., scan, reduce) are only available to ND-range kernels, and so we should prefer NDrange kernels in situations where we are interested in expressing complex algorithms or fine-tuning for performance.

The features available to each kernel form should be expected to change as the language evolves, but we expect the basic trend to remain the same: basic data-parallel kernels will not expose locality-aware features and explicit ND-range kernels will expose all performanceenabling features.

## Summary

This chapter introduced the basics of expressing parallelism in C++ with SYCL and discussed the strengths and weaknesses of each approach to writing data-parallel kernels.

SYCL provides support for many forms of parallelism, and we hope that we have provided enough information to prepare readers to dive in and start coding!

We have only scratched the surface, and a deeper dive into many of the concepts and classes introduced in this chapter is forthcoming: the usage of local memory, barriers, and communication routines are covered in Chapter 9; different ways of defining kernels besides using lambda expressions are discussed in Chapters 10 and 20; detailed mappings of the ND-range execution model to specific hardware are explored in Chapters 15, 16, and 17; and best practices for expressing common parallel patterns using SYCL are presented in Chapter 14.

![](images/00c7b1b8bc34ab706d2dfb265806f5c36c44b98613754a2233e758de2cb4654a.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
