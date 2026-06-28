
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
