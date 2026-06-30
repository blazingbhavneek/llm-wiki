# sycl Source Lines 4656-5307

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L4656-L5307

Citation: [sycl:L4656-L5307]

````text
## Work-Group Barriers and Local Memory in ND-Range Kernels

This section describes how work-group barriers and local memory are expressed in ND-range kernels. For ND-range kernels, the representation is explicit: a kernel declares and operates on a local accessor representing an allocation in the local address space and calls a barrier function to synchronize the work-items in a work-group.

## Local Accessors

To declare local memory for use in an ND-range kernel, use a local accessor. Like other accessor objects, a local accessor is constructed within a command group handler, but unlike the accessor objects discussed in Chapters 3 and 7, a local accessor is not created from a buffer object. Instead, a local accessor is created by specifying a type and a range describing the number of elements of that type. Like other accessors, local accessors may be one-dimensional, two-dimensional, or threedimensional. Figure 9-7 demonstrates how to declare local accessors and use them in a kernel.

## Chapter 9 Communication and Synchronization

```txt
/ This is a typical global accessor.
accessor dataAcc{dataBuf, h};

// This is a 1D local accessor consisting of 16 ints:
auto localIntAcc = local_accessor<int, 1>(16, h);

// This is a 2D local accessor consisting of 4 x 4
// floats:
auto localFloatAcc =
    local_accessor<float, 2>({4, 4}, h);

h.parallel_for(
    nd_range<1>{{size}, {16}}, [=](nd_item<1> item) {
        auto index = item.get_global_id();
        auto local_index = item.get_local_id();

        // Within a kernel, a local accessor may be read
        // from and written to like any other accessor.
        localIntAcc[local_index] = dataAcc[index] + 1;
        dataAcc[index] = localIntAcc[local_index];
    });
```

## Figure 9-7. Declaring and using local accessors

Remember that local memory is uninitialized when each work-group begins and does not persist after each work-group completes. This means that a local accessor must always be read\_write, since otherwise a kernel would have no way to assign the contents of local memory or view the results of an assignment. Local accessors may optionally be atomic though, in which case accesses to local memory via the accessor are performed atomically. Atomic accesses are discussed in more detail in Chapter 19.

## Synchronization Functions

To synchronize the work-items in an ND-range kernel work-group, call the group\_barrier function with a group representing the work-group. Because the group representing the work-group may only be queried from an nd\_item and cannot be queried from an item, work-group barriers are only available to ND-range kernels and are not available to basic dataparallel kernels.

The group\_barrier function accepts one additional optional argument to describe the scope of any memory consistency operations that are performed by the barrier. When no additional arguments are passed to the group\_barrier function, the barrier function will determine the default scope based on the passed-in group. The default scope is usually correct and therefore an explicit scope is rarely required, but the memory scope can be broadened if necessary for some algorithms.

Please note that the explicit scope only affects the memory operations that are performed by the barrier, and that the set of work-items that synchronize execution at the barrier is determined entirely by the group object passed to the barrier. We cannot synchronize more or fewer workitems by passing a different memory scope to the barrier, but we can synchronize a different set of work-items by passing a different group object to the barrier.

## A Full ND-Range Kernel Example

Now that we know how to declare a local memory accessor and synchronize accesses to it using a barrier function, we can implement an ND-range kernel version of matrix multiplication that coordinates communication among work-items in the work-group to reduce traffic to global memory. The complete example is shown in Figure 9-8.

```lisp
CHAPTER 9 COMMUNICATION AND SYNCHRONIZATION

// Traditional accessors, representing matrices in
// global memory:
accessor matrixA{bufA, h};
accessor matrixB{bufB, h};
accessor matrixC{bufC, h};

// Local accessor, for one matrix tile:
constexpr int tile_size = 16;

// Template type T is the type of data stored in the matrix
auto tileA = local_accessor<T, 1>(tile_size, h);

h.parallel_for(
    nd_range<2>{{M, N}, {1, tile_size}},
    [=](nd_item<2> item) {
        // Indices in the global index space:
        int m = item.get_global_id()[0];
        int n = item.get_global_id()[1];

        // Index in the local index space:
        int i = item.get_local_id()[1];

        T sum = 0;
        for (int kk = 0; kk < K; kk += tile_size) {
            // Load the matrix tile from matrix A, and
            // synchronize to ensure all work-items have a
            // consistent view of the matrix tile in local
            // memory.
            tileA[i] = matrixA[m][kk + i];
            group_barrier(item.get_group());

            // Perform computation using the local memory
            // tile, and matrix B in global memory.
            for (int k = 0; k < tile_size; k++) {
                sum += tileA[k] * matrixB[kk + k][n];
            }

            // After computation, synchronize again, to
            // ensure all reads from the local memory tile
            // are complete.
            group_barrier(item.get_group());
        }

        // Write the final result to global memory.
        matrixC[m][n] = sum;
    });
```

## Figure 9-8. Expressing a tiled matrix multiplication kernel with an ND-range parallel\_for and work-group local memory

The main loop in this kernel can be thought of as two distinct phases: in the first phase, the work-items in the work-group collaborate to load shared data from the A matrix into work-group local memory; and in the second, the work-items perform their own computations using the shared data. To ensure that all work-items have completed the first phase before moving onto the second phase, the two phases are separated by a call to group\_barrier to synchronize all work-items in the work-group and to provide a memory fence. This pattern is a common one, and the use of work-group local memory in a kernel almost always necessitates the use of work-group barriers.

Note that there must also be a call to group\_barrier to synchronize execution between the computation phase for the current tile and the loading phase for the next matrix tile. Without this synchronization operation, part of the current matrix tile may be overwritten by one workitem in the work-group before another work-item is finished computing with it. In general, any time that one work-item is reading or writing data in local memory that was read or written by another work-item, synchronization is required. In Figure 9-8, the synchronization is done at the end of the loop, but it would be equally correct to synchronize at the beginning of each loop iteration instead.

## Sub-Groups

So far in this chapter, work-items have communicated with other workitems in the work-group by exchanging data through work-group local memory and by synchronizing using the group\_barrier function on a work-group.

In Chapter 4, we discussed another grouping of work-items. A subgroup is an implementation-defined subset of work-items in a work-group that execute together on the same hardware resources or with additional scheduling guarantees. Because the implementation decides how to group work-items into sub-groups, the work-items in a sub-group may be able to communicate or synchronize more efficiently than the work-items in an arbitrary work-group.

This section describes the building blocks for communication among work-items in a sub-group. Sub-groups also require a notion of workitem grouping, so sub-groups also require ND-range kernels and are not included in the execution model for basic data-parallel kernels.

## Synchronization via Sub-Group Barriers

Just like how the work-items in a work-group may synchronize using a work-group barrier, the work-items in a sub-group may synchronize using a sub-group barrier. To perform a sub-group barrier, call the same group\_ barrier function, but pass a group object representing the sub-group rather than the work-group, as shown in Figure 9-9. Like for work-group objects, a group object representing the sub-group can be queried from the nd\_item class for ND-range kernels but cannot be queried from a basic data-parallel item.

```txt
h.parallel_for(
    nd_range{{size}, {16}}, [=](nd_item<1> item) {
        auto sg = item.get_sub_group();
        group_barrier(sg);
        // ...
        auto index = item.get_global_id();
        data_acc[index] = data_acc[index] + 1;
    });
```

## Figure 9-9. Querying and using the sub\_group class

Also like the work-group barrier, the sub-group barrier may accept optional arguments to broaden the scope of any memory operations associated with the sub-group barrier, but this is uncommon and in most cases we can simply use the default memory scope.

## Exchanging Data Within a Sub-Group

Unlike work-groups, sub-groups do not have a dedicated memory space for exchanging data. Instead, work-items in the sub-group may exchange data through work-group local memory, through global memory, or more commonly by using sub-group collective functions.

As described previously, a collective function is a function that describes an operation performed by a group of work-items, not an individual work-item. Because a barrier synchronization function is an operation performed by a group of work-items, it is one example of a collective function.

Other collective functions express common communication patterns. We will describe the semantics for many collective functions in detail later in this chapter, but for now, we focus on the group\_broadcast collective function that we will use to implement matrix multiplication using sub-groups.

The group\_broadcast collective function takes a value from one work-item in the group and communicates it to all other work-items in the group. An example is shown in Figure 9-10. Notice that the semantics of the broadcast function require that the local\_id identifying the value in the group to communicate must be the same for all work-items in the group, ensuring that the result of the broadcast function is also the same for all work-items in the group.

![](images/7c5eb0d317908cee562b7c778c1f695b71c1c1350c37c986a14a96274073e272.jpg)  
Figure 9-10. Processing by the broadcast function

If we look at the innermost loop of our local memory matrix multiplication kernel, shown in Figure 9-11, we can see that the access to the matrix tile is a broadcast operation, since each work-item in the group reads the same value out of the matrix tile.

```lisp
h.parallel_for(
    nd_range<2>{{M, N}, {1, tile_size}},
    [=](nd_item<2> item) {
        // Indices in the global index space:
        int m = item.get_global_id()[0];
        int n = item.get_global_id()[1];

        // Index in the local index space:
        int i = item.get_local_id()[1];

        // Template type T is the type of data stored in
        // the matrix
        T sum = 0;
        for (int kk = 0; kk < K; kk += tile_size) {
            // Load the matrix tile from matrix A, and
            // synchronize to ensure all work-items have a
            // consistent view of the matrix tile in local
            // memory.
            tileA[i] = matrixA[m][kk + i];
            group_barrier(item.get_group());

            // Perform computation using the local memory
            // tile, and matrix B in global memory.
            for (int k = 0; k < tile_size; k++) {
                // Because the value of k is the same for
                // all work-items in the group, these reads
                // from tileA are broadcast operations.
                sum += tileA[k] * matrixB[kk + k][n];
            }

            // After computation, synchronize again, to
            // ensure all reads from the local memory tile
            // are complete.
            group_barrier(item.get_group());
        }

        // Write the final result to global memory.
        matrixC[m][n] = sum;
    });
```

## Figure 9-11. Matrix multiplication kernel includes a broadcast operation

We will use the group\_broadcast function with a sub-group object to implement a matrix multiplication kernel that does not require workgroup local memory or barriers. On many devices, sub-group broadcasts are faster than work-group broadcasts using work-group local memory and barriers.

## A Full Sub-Group ND-Range Kernel Example

Figure 9-12 is a complete example that implements matrix multiplication using sub-groups. Notice that this kernel requires no work-group local memory or explicit synchronization and instead uses a sub-group broadcast collective function to communicate the contents of the matrix tile among the work-items in the sub-group.

```lisp
// Note: This example assumes that the sub-group size
// is greater than or equal to the tile size!
constexpr int tile_size = 4;
h.parallel_for(
    nd_range<2>{{M, N}, {1, tile_size}},
    [=](nd_item<2> item) {
        auto sg = item.get_sub_group();

        // Indices in the global index space:
        int m = item.get_global_id()[0];
        int n = item.get_global_id()[1];

        // Index in the local index space:
        int i = item.get_local_id()[1];

        // Template type T is the type of data stored
        // in the matrix
        T sum = 0;
        for (int kk = 0; kk < K; kk += tile_size) {
            // Load the matrix tile from matrix A.
            T tileA = matrixA[m][kk + i];

            // Perform computation by broadcasting from
            // the matrix tile and loading from matrix B
            // in global memory. The loop variable k
            // describes which work-item in the sub-group
            // to broadcast data from.
            for (int k = 0; k < tile_size; k++) {
                sum += group_broadcast(sg, tileA, k) *
                    matrixB[kk + k][n];
            }
        }

        // Write the final result to global memory.
        matrixC[m][n] = sum;
    });
```

## Figure 9-12. Tiled matrix multiplication kernel expressed with NDrange parallel\_for and sub-group collective functions

## Group Functions and Group Algorithms

In the “Sub-Groups” section of this chapter, we described collective functions and how collective functions express common communication patterns. We specifically discussed the broadcast collective function, which is used to communicate a value from one work-item in a group to the other work-items in the group. This section describes additional collective functions.

Although the collective functions described in this section can be implemented directly in our programs using features such as atomics, work-group local memory, and barriers, many devices include dedicated hardware to accelerate collective functions. Even when a device does not include specialized hardware, vendor-provided implementations of collective functions are likely tuned for the device they are running on, so calling a built-in collective function will usually perform better than a general-purpose implementation that we might write.

Use collective functions for common communication patterns to simplify code and increase performance!

## Broadcast

The group\_broadcast function enables one work-item in a group to share the value of a variable with all other work-items in the group. A diagram showing how the broadcast function works can be found in Figure 9-10. The group\_broadcast function is supported for both work-groups and sub-groups.

## Votes

The any\_of\_group, all\_of\_group, and none\_of\_group functions (henceforth referred to as “vote” functions) enable work-items to compare the result of a Boolean condition across their group: any\_of\_group returns true if the condition is true for at least one work-item in the group, all\_of\_ group returns true if the condition is true for all work-items in the group, and none\_of\_group returns true if the condition is false for all of the workitems in the group. A comparison of these two functions for an example input is shown in Figure 9-13.

![](images/38195e783784cc44261892fa8c9a8f4d1a8789d2c48b24f4393aede7ecffc958.jpg)  
Figure 9-13. Comparison of the any\_of\_group, all\_of\_group, and none\_of\_group functions

SYCL 2020 also supports another variant of these functions where the work-items in a group cooperate to evaluate a range of data like the standard C++ all\_of, any\_of, and none\_of algorithms. These functions are named joint\_any\_of, joint\_all\_of, and joint\_none\_of to differentiate from the variants where each work-item in the group holds the data to compare directly.

The vote functions are useful for some iterative algorithms to determine when a solution has converged for all work-items in the group, for example. The vote functions are supported for work-groups and sub-groups.

## Shuffles

One of the most useful features of sub-groups is the ability to communicate directly between individual work-items without explicit memory operations. In many cases, such as the sub-group matrix multiplication kernel, these shuffle operations enable us to both remove work-group local memory usage from our kernels and avoid unnecessary repeated accesses to global memory. There are several flavors of these shuffle functions available.

The most general of the shuffle functions is called select\_from\_group, and as shown in Figure 9-14, it allows for arbitrary communication between any pair of work-items in the sub-group. This generality may come at a performance cost, however, and we strongly encourage making use of the more specialized shuffle functions wherever possible.

![](images/b646c5a4aa93c4d5bb8d26a6159be8753bd91ea2d6e99b35fb6dffdb9a129692.jpg)  
Figure 9-14. Using a generic select\_from\_group to sort values based on precomputed indices

In Figure 9-14, a generic shuffle is used to sort the values of a subgroup using precomputed permutation indices. Arrows are shown for one work-item in the sub-group, where the result of the shuffle is the value of x for the work-item with local\_id equal to 7.

Note that the sub-group group\_broadcast function can be thought of as a specialized version of the general-purpose select\_from\_group function, where the shuffle index is the same for all work-items in the sub-group. When the shuffle index is known to be the same for all workitems in the sub-group, using group\_broadcast instead of select\_from\_ group provides the compiler additional information and may increase performance on some implementations.

The shift\_group\_right and shift\_group\_left functions effectively shift the contents of a sub-group by a fixed number of elements in a given direction, as shown in Figure 9-15. Note that the values returned to the last five work-items in the sub-group are undefined and are shown as blank in Figure 9-15. Shifting can be useful for parallelizing loops with loopcarried dependences or when implementing common algorithms such as exclusive or inclusive scans.

<table><tr><td>x:</td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td>delta:</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td></tr><tr><td>shift_group_left (group, x, delta):</td><td>5</td><td>6</td><td>7</td><td></td><td></td><td></td><td></td><td></td></tr></table>

Figure 9-15. Using shift\_group\_left to shift x values of a subgroup by five items

The permute\_group\_by\_xor function swaps the values of two work items, specified by the result of an XOR operation applied to the workitem’s sub-group local id and a fixed constant. As shown in Figure 9-16 and Figure 9-17, several common communication patterns can be expressed using an XOR, such as swapping pairs of neighboring values or reversing the sub-group values.

![](images/13446ff1b16788c5a259268e399d787ac06681727c00cea7517bdaf15440e337.jpg)  
Figure 9-16. Swapping neighboring pairs of x using a permute\_ group\_by\_xor

![](images/d272cb951b512fc6db3235a763c7bf144b97f4dd8396046a21f12a585992f6bd.jpg)  
Figure 9-17. Reversing the values of x using a permute\_ group\_by\_xor

## SUB-GROUP OPTIMIZATIONS USING BROADCAST, VOTE, AND COLLECTIVES

The behavior of broadcast, vote, and other collective functions applied to subgroups is identical to when they are applied to work-groups, but they deserve additional attention because they may enable aggressive optimizations in certain compilers. For example, a compiler may be able to reduce register usage for variables that are broadcast to all work-items in a sub-group, or may be able to reason about control flow divergence based on usage of the any\_of\_group and all\_of\_group functions.

Because the shuffle functions are so specialized, they are only available for sub-groups and are not available for work-groups.

## Summary

This chapter discussed how work-items in a group may communicate and cooperate to improve the performance of some types of kernels.

We first discussed how ND-range kernels support grouping work-items into work-groups. We discussed how grouping work-items into workgroups changes the parallel execution model, guaranteeing that the workitems in a work-group are scheduled for execution in a way that enables communication and synchronization.

Next, we discussed how the work-items in a work-group may synchronize using barriers and how barriers are expressed in kernels. We also discussed how communication between work-items in a work-group can be performed via work-group local memory, to simplify kernels and to improve performance, and we discussed how work-group local memory is represented using local accessors.

We discussed how work-groups in ND-range kernels may be further divided into sub-groupings of work-items, where the sub-groups of workitems may support additional communication patterns or scheduling guarantees.

For both work-groups and sub-groups, we discussed how common communication patterns may be expressed and accelerated through the use of collective functions.

The concepts in this chapter are an important foundation for understanding the common parallel patterns described in Chapter 14 and for understanding how to optimize for specific devices in Chapters 15, 16, and 17.

![](images/b4e789da67fb5657768f181a313d4b7e24c87d04a90ee5e78540d3013f45586a.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Defining Kernels

Thus far in this book, our code examples have represented kernels using C++ lambda expressions. Lambda expressions are a concise and convenient way to represent a kernel right where it is used, but they are not the only way to represent a kernel in SYCL. In this chapter, we will explore various ways to define kernels in detail, helping us to choose a kernel form that is most natural for our C++ coding needs.

This chapter explains and compares three ways to represent a kernel:

• Lambda expressions.

• Named function objects (functors).

• Via interoperability with kernels created via other languages or APIs. This topic is covered briefly in this chapter, and in more detail in Chapter 20.

This chapter closes with a discussion of how to explicitly manipulate kernels in a kernel bundle to query kernel properties and to control when and how kernels are compiled.

## Why Three Ways to Represent a Kernel?

Before we dive into the details, let’s start with a summary of why there are three ways to define a kernel and the advantages and disadvantages of each method. A useful summary is given in Figure 10-1.

Bear in mind that a kernel is used to express a unit of computation and that many instances of a kernel will usually execute in parallel on an accelerator. SYCL supports multiple ways to express a kernel to integrate naturally and seamlessly into codebases with different coding styles, while also executing efficiently on a wide diversity of accelerator types.

<table><tr><td>Kernel Representation</td><td>Description</td></tr><tr><td>Lambda Expression</td><td>Pros:• Lambda expressions are a concise way to represent a kernel right where it is used.• Lambda expressions are a familiar way to represent kernel-like operations in modern C++ codebases.• Lambda capture rules automatically pass data to kernels.Cons:• Kernels represented as lambda expressions cannot be templated, and do not assemble as a library (like regular functions) without extra work.• The lambda syntax may be unfamiliar to some C++ codebases.</td></tr><tr><td>Named Function Object (Functor)</td><td>Pros:• Functors can be templated, reused, and shipped as a part of a library, just like any other C++ class.• Functors provide more control over the data that gets passed into a kernel.Cons:• Kernels represented as functors require more code than kernels represented as lambda expressions.• Kernel arguments must be explicitly passed to functors and are not captured automatically.</td></tr><tr><td>Interoperability with Other Languages or APIs</td><td>Pros:• Enables re-use of previously written kernels or libraries.• Enables large application codebases to incrementally add support for SYCL.• Kernel languages from other APIs may support features that have not been added or are difficult to express with SYCL.Cons:• Interoperability is an optional feature that may not be supported by all SYCL implementations or by all SYCL devices in an implementation.• Kernels written in other APIs are not compiled by the SYCL device compiler, which may limit compile-time syntax checking, type checking for kernel arguments, and optimization opportunities.• Kernels written in other APIs may not support the latest C++ features.</td></tr></table>

Figure 10-1. Three ways to represent a kernel

## Kernels as Lambda Expressions

C++ lambda expressions, also referred to as anonymous function objects, unnamed function objects, closures, or simply lambdas, are a convenient way to express a kernel right where it is used. This section describes how to represent a kernel as a C++ lambda expression. This expands on the introductory refresher on C++ lambda expressions, in Chapter 1, which included some basic coding samples with output.

C++ lambda expressions are very powerful and have an expressive syntax, but only a specific subset of the full C++ lambda expression syntax is required (and supported) when expressing a kernel in SYCL.

```rust
h.parallel_for(
    size,
    // This is the start of a kernel lambda expression:
    [=](id<1> i) { data_acc[i] = data_acc[i] + 1; }
    // This is the end of the kernel lambda expression.
);
```  
Figure 10-2. Simple kernel defined using a lambda expression

## Elements of a Kernel Lambda Expression

Figure 10-2 shows a simple kernel written as a typical lambda expression—the code examples so far in this book have used this syntax.

The illustration in Figure 10-3 shows elements of a lambda expression that may be used with kernels, but many of these elements are not typical. In most cases, the lambda defaults are sufficient, so a typical kernel lambda expression looks more like the lambda expression in Figure 10-2 than the more complicated lambda expression in Figure 10-3.

```cpp
q.submit([&](handler& h) {
  accessor data_acc{data_buf, h};
  h.parallel_for(
    nd_range{{size}, {8}},
    1     2     4     5
    [=](id<1> i) noexcept [[sycl::reqd_work_group_size(8)]] ->void {
      data_acc[i] = data_acc[i] + 1;
    });
});
```

Figure 10-3. More elements of a kernel lambda expression, including optional elements

1. The first part of a lambda expression describes the lambda captures. Capturing a variable from a surrounding scope enables it to be used within the lambda expression, without explicitly passing it to the lambda expression as a parameter.

C++ lambda expressions support capturing a variable by copying it or by creating a reference to it, but for kernel lambda expressions, variables may only be captured by copy. General practice is to simply use the default capture mode [=], which implicitly captures all variables by value, although it is possible to explicitly name each captured variable in a comma-separated capture-list as well. Any variable used within a kernel that is not captured by value will cause a compile-time error. Note that global variables are not captured by a lambda expression, as per the C++ standard.

2. The second part of a lambda expression describes parameters that are passed to the lambda expression, just like parameters that are passed to named functions.

For kernel lambda expressions, the parameter depends on how the kernel was invoked and identifies the index of the work-item in the parallel execution space. Please refer to Chapter 4 for more details about the various parallel execution spaces and how to identify the index of a work-item in each execution space.

3. The last part of the lambda expression defines the function body. For a kernel lambda expression, the function body describes the operations that should be performed at each index in the parallel execution space.

There are other parts of a lambda expression, but they are either optional, infrequently used, or unsupported by SYCL 2020:

4. No specifiers (such as mutable) are defined by SYCL 2020, so none are shown in the example code.

5. The exception specification is supported, but must be noexcept if provided, since exceptions are not supported for kernels.

6. Lambda attributes are supported and may be used to control how the kernel is compiled. For example, the reqd\_work\_group\_size attribute can be used to require a specific work-group size for a kernel, and the device\_has attribute can be used to require specific device aspects for a kernel. Chapter 12 contains more information on kernel specialization using attributes and aspects.

7. The return type may be specified but must be void if provided, since non-void return types are not supported for kernels.

## LAMBDA CAPTURES: IMPLICIT OR EXPLICIT?

Some C++ style guides recommend against implicit (or default) captures for lambda expressions due to possible dangling pointer issues, especially when lambda expressions cross scope boundaries. The same issues may occur when lambdas are used to represent kernels, since kernel lambdas execute asynchronously on the device, separately from host code.

Because implicit captures are useful and concise, it is common practice for SYCL kernels and a convention we use in this book, but it is ultimately our decision whether to prefer the brevity of implicit captures or the clarity of explicit captures.

## Identifying Kernel Lambda Expressions

There is one more element that must be provided in some cases when a kernel is written as a lambda expression: because lambda expressions are anonymous, at times SYCL requires an explicit kernel name template parameter to uniquely identify a kernel written as a lambda expression.

```txt
// In this example, "class Add" names the kernel
// lambda expression.
h.parallel_for<class Add>(size, [=](id<1> i) {
  data_acc[i] = data_acc[i] + 1;
});
```

Figure 10-4. Identifying kernel lambda expressions

Naming a kernel lambda expression is a way for a host code compiler to identify which kernel to invoke when the kernel was compiled by a separate device code compiler. Naming a kernel lambda also enables runtime introspection of a compiled kernel or building a kernel by name, as shown in Figure 10-9.

To support more concise code when the kernel name template parameter is not required, the kernel name template parameter is optional for most SYCL 2020 compilers. When no kernel name template parameter is required, our code can be more compact, as shown in Figure 10-5.

```javascript
h.parallel_for(size, [=](id<1> i) {
  data_acc[i] = data_acc[i] + 1;
});
```

## Figure 10-5. Using unnamed kernel lambda expressions

Because the kernel name template parameter for lambda expressions is not required in most cases, we can usually start with an unnamed lambda and only add a kernel name in specific cases when the kernel name template parameter is required.

When the kernel name template parameter is not required, using unnamed kernel lambdas is preferred to reduce verbosity.

## Kernels as Named Function Objects

Named function objects, also known as functors, are an established pattern in C++ that allows operating on an arbitrary collection of data while maintaining a well-defined interface. When used to represent a kernel, the member variables of a named function object define the state that the kernel may operate on, and the overloaded function call operator() is invoked for each work-item in the parallel execution space.

Named function objects require more code than lambda expressions to express a kernel, but the extra verbosity provides more control and additional capabilities. It may be easier to analyze and optimize kernels expressed as named function objects, for example, since any buffers and data values used by the kernel must be explicitly passed to the kernel, rather than captured automatically by a lambda expression.

Kernels expressed as named function objects may also be easier to debug, easier to reuse, and they may be shipped as part of a separate header file or library.

Finally, because named function objects are just like any other C++ class, kernels expressed as named function objects may be templated. C++20 added templated lambda expressions, but templated lambda expressions are not supported for kernels in SYCL 2020, which is based on C++17.

## Elements of a Kernel Named Function Object

The code in Figure 10-6 demonstrates typical usage of a kernel represented as a named function object. In this example, the parameters to the kernel are passed to the class constructor, and the kernel itself is in the overloaded function call operator().

```cpp
class Add {
public:
    Add(accessor<int> acc) : data_acc(acc) {}
    void operator()(id<1> i) const {
        data_acc[i] = data_acc[i] + 1;
    }

private:
    accessor<int> data_acc;
};

int main() {
    constexpr size_t size = 16;
    std::array<int, size> data;

    for (int i = 0; i < size; i++) {
        data[i] = i;
    }

    {
        buffer data_buf{data};

        queue q;
        std::cout
            << "Running on device: "
            << q.get_device().get_info<info::device::name>()
            << "\n";

        q.submit([&](handler& h) {
            accessor data_acc{data_buf, h};
            h.parallel_for(size, Add(data_acc));
        });
    }
    // ...
```

## Figure 10-6. Kernel as a named function object

When a kernel is expressed as a named function object, the named function object type must follow SYCL 2020 rules to be device copyable. Informally, this means that the named function objects may be safely copied byte by byte, enabling the member variables of the named function object to be passed to and accessed by kernel code executing on a device. Any C++ type that is trivially copyable is implicitly device copyable.

The argument to the overloaded function call operator() depends on how the kernel is launched, just like for kernels expressed as lambda expressions.

The code in Figure 10-7 shows how to use optional kernel attributes, like the reqd\_work\_group\_size attribute, on kernels defined as named function objects. There are two valid positions for the optional kernel attribute when a kernel is defined as a named function object. This is different than a kernel written as a lambda expression, where only one position for the optional kernel attribute is valid.

```cpp
class AddWithAttribute {
  public:
    AddWithAttribute(accessor<int> acc) : data_acc(acc) {}
    [[sycl::reqd_work_group_size(8)]] void operator()( id<1> i) const {
      data_acc[i] = data_acc[i] + 1;
    }

    private:
      accessor<int> data_acc;
};

class MulWithAttribute {
  public:
    MulWithAttribute(accessor<int> acc) : data_acc(acc) {}
    void operator()
      [[sycl::reqd_work_group_size(8)]] (id<1> i) const {
      data_acc[i] = data_acc[i] * 2;
    }

    private:
      accessor<int> data_acc;
};
```

## Figure 10-7. Using optional attributes with a named function object

Because all function objects are named, the host code compiler can use the function object type to identify the kernel code produced by the device code compiler even if the function object is templated. No additional kernel name template parameter is needed to name a kernel function object.

## Kernels in Kernel Bundles

One final topic we should be aware of related to SYCL kernels concerns SYCL kernel objects and SYCL kernel bundles. Knowledge of kernel objects and kernel bundles is not required for typical application development but is useful in some cases to tune application performance. Knowledge of kernel objects and kernel bundles can also help to understand how kernels are organized and managed by a SYCL implementation.

A SYCL kernel bundle is a container for SYCL kernels or SYCL functions used by an application. The number of kernel bundles in an application depends on the specific SYCL compiler. Some applications may have just one kernel bundle, even if they have multiple kernels, while other applications may have more than one kernel bundle, even if they just have a few kernels.

A SYCL kernel bundle and the kernels or functions it contains can be in one of three states:

An input state: Kernel bundles in this state are typically in some sort of intermediate representation and must be just-in-time (JIT) compiled before they can execute on a device.

An object state: Kernel bundles in this state are usually compiled but not linked, like object files created by host application compilers.

An executable state: Kernel bundles in this state are fully compiled to device code and are ready to be executed on the device. Kernel bundles that are aheadof-time (AOT) compiled when the host application is compiled will initially be in this state.

While not required by the specification, many SYCL compilers compile kernels to an intermediate representation initially, for portability to the largest number of SYCL devices. This means that usually the application kernel bundles are in the input state initially. Then, many SYCL runtime libraries compile the kernel bundles from the input state to the executable state “lazily,” on an as-needed basis.

This is usually a good policy because it enables fast application startup and does not compile kernels unnecessarily if they are never executed. The disadvantage of this policy, though, is that the first use of a kernel takes longer than subsequent uses, since it includes both the time needed to compile the kernel and the usual time needed to submit and execute the kernel. For complex kernels, the time to compile the kernel can be significant, making it desirable to shift compilation to a different point during application execution, such as when the application is loading, or to a separate background thread.

To provide more control over when and how a kernel is compiled, we can explicitly request a kernel bundle to be compiled before submitting a kernel to a queue. The precompiled kernel bundle can be used when the kernel is submitted to a queue for execution. Figure 10-8 shows how to compile all the kernels used by an application before any of the kernels are submitted to a queue, and how to use the precompiled kernel bundle.

```cpp
auto kb = get_kernel_bundle<bundle_state::executable>(
    q.get_context());

std::cout
    << "All kernel compilation should be done now.\n";

q.submit([&](handler& h) {
  // Use the pre-compiled kernel from the kernel bundle.
  h.use_kernel_bundle(kb);

  accessor data_acc{data_buf, h};
  h.parallel_for(range{size}, [=](id<1> i) {
    data_acc[i] = data_acc[i] + 1;
  });
});
```

## Figure 10-8. Compiling kernels explicitly using kernel bundles

This example requests a kernel bundle in an executable state for all the devices in the SYCL context associated with the SYCL queue, which will cause any kernels in the application to be just-in-time compiled if they are not already in the executable state. In this specific example, the kernel is very short and should not take long to compile, but if there were many kernels, or if they were more complicated, this step could take a significant amount of time. Of course, if all kernels were ahead-of-time compiled, or if all kernels had already been just-in-time compiled, this operation would effectively be free because all kernels would already be in the executable state.

If we want even more control over when and how our kernels are compiled, we can request a kernel bundle for a specific device, or even specific kernels in our program. This allows us to selectively compile some of the kernels in our program immediately, while leaving other kernels to be compiled later or on an as-needed basis. Figure 10-9 shows how to compile only the kernel identified by the class Add kernel name and only for the SYCL device associated with the SYCL queue, rather than all kernels in the program and all devices in the SYCL context.

```cpp
CHAPTER 10   DEFINING KERNELS

auto kid = get_kernel_id<class Add>();
auto kb = get_kernel_bundle<bundle_state::executable>(
    q.get_context(), {q.get_device()}, {kid});

std::cout << "Kernel compilation should be done now.\n";

q.submit([&](handler& h) {
    // Use the pre-compiled kernel from the kernel bundle.
    h.use_kernel_bundle(kb);

    accessor data_acc{data_buf, h};
    h.parallel_for<class Add>(range{size}, [=](id<1> i) {
        data_acc[i] = data_acc[i] + 1;
    });
});
```

Figure 10-9. Compiling kernels explicitly and selectively using kernel bundles

This is a rare case where we needed to name our kernel lambda expression; otherwise, we would have no way to identify the kernel to compile.

Use kernel bundles to compile kernels predictably in an application!

Kernels in kernel bundles can also be used to query information about a compiled kernel, say to determine the maximum work-group size for a kernel for a specific device. In some cases, these types of kernel queries may be needed to choose valid values to use for a kernel and a specific device. In other cases, kernel queries can provide hints, allowing our application to dynamically adapt and choose optimal values for a kernel and a specific device.

The basic mechanism to identify a kernel, get a kernel object from a compiled kernel bundle, and use the kernel object to perform devicespecific queries is shown in Figure 10-10. A more complete list of available kernel queries is described in Chapter 12.

```txt
auto kid = get_kernel_id<class Add>();
auto kb = get_kernel_bundle<bundle_state::executable>(
    q.get_context(), {q.get_device()}, {kid});
auto kernel = kb.get_kernel(kid);

std::cout
    << "The maximum work-group size for the kernel and "
        "this device is: "
    << kernel.get_info<info::kernel_device_specific::
        work_group_size>(
        q.get_device())
    << "\n";

std::cout
    << "The preferred work-group size multiple for the "
        "kernel and this device is: "
    << kernel.get_info<
        info::kernel_device_specific::
            preferred_work_group_size_multiple>(
        q.get_device())
    << "\n";

Example Output:
Running on device: NVIDIA GeForce RTX 3060
The maximum work-group size for the kernel and this device is: 1024
The preferred work-group size multiple for the kernel and this device is: 32

Example Output:
Running on device: Intel(R) Data Center GPU Max 1100
The maximum work-group size for the kernel and this device is: 1024
The preferred work-group size multiple for the kernel and this device is: 16

Example Output:
Running on device: Intel(R) UHD Graphics 770
The maximum work-group size for the kernel and this device is: 512
The preferred work-group size multiple for the kernel and this device is: 64
```  
Figure 10-10. Querying kernels in kernel bundles

This is another rare case where we need to name our kernel lambda expression; otherwise, we would have no way to identify the kernel to query.

## Interoperability with Other APIs

When a SYCL implementation is built on top of another API, the implementation may be able to interoperate with kernels defined using mechanisms of the underlying API. This allows an application to integrate SYCL easily and incrementally into existing codebases that are already using the underlying API. This topic is covered in detail in Chapter 20. For the purposes of this chapter, we can simply recognize that interoperability with kernels or kernel bundles created via other source languages or APIs provides a third way to represent a kernel.

## Summary

In this chapter, we explored different ways to define kernels. We described how to seamlessly integrate SYCL into existing C++ codebases by representing kernels as C++ lambda expressions or named function objects. For new codebases, we also discussed the pros and cons of the different kernel representations to help choose the best way to define kernels based on the needs of our application or library.

We described how kernels are typically compiled in a SYCL application and how to directly manipulate kernels in kernel bundles to control the compilation process. Even though this level of control will not be required for most applications, it is a useful technique to be aware of when we are tuning our applications.

![](images/da90e0e564b99993d81905fb64b761f7d123f784599183e6191185eaac3a5f48.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
