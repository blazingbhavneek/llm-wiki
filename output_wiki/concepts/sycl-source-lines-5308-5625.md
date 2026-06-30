# sycl Source Lines 5308-5625

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L5308-L5625

Citation: [sycl:L5308-L5625]

````text
# Vectors and Math Arrays

Vectors are collections of data. Vectors can be useful because parallelism in our computers comes from collections of computer hardware, and data is often processed in related groupings (e.g., the color channels in an RGB pixel). The concept is so important that we spend a chapter discussing the different SYCL vector types and how to utilize them. Note that we will not dive into vectorization of scalar operations in this chapter since that varies based on device type and implementations. Vectorization of scalar operations is covered in Chapter 16.

This chapter seeks to address the following questions:

• What are vector types?

• What is the difference between the SYCL math array (marray) and vector (vec) types?

• When and how should I use marray and vec?

We discuss marray and vec using working code examples and highlight the most important aspects of exploiting these types.

## The Ambiguity of Vector Types

Vectors are a surprisingly controversial topic when we talk with parallel programming experts. In the authors’ experience, this is because different people define and think about vectors in different ways.

There are two broad ways to think about what this chapter calls vector types:

1. As a convenience type, which groups data that we might want to refer to and operate on as a group, for example, the RGB or YUV color channels of a pixel. We could define a pixel class or struct and define math operators like + on it, but convenience types do this for us out of the box. Convenience types can be found in many shader languages used to program GPUs, so this way of thinking is common among many GPU developers.

2. As a mechanism to describe how code maps to a SIMD (single instruction, multiple data) instruction set in hardware. For example, in some languages and implementations, operations on a float8 could map to an eight-lane SIMD instruction in hardware. SIMD vector types are used in many languages as a high-level alternative to CPU-specific intrinsics, so this way of thinking is already common among many CPU developers.

Although these two interpretations of vector types are very different, they unintentionally became combined and muddled together as SYCL and other languages became applicable to both CPUs and GPUs. The vec class (which existed in SYCL 1.2.1, and still exists in SYCL 2020) is compatible with either interpretation, whereas the marray class (which was introduced in SYCL 2020) is explicitly described as a convenience type unrelated to SIMD vector hardware instructions.

## CHANGES ARE ON THE HORIZON: SIMD TYPES

SY CL 2020 does not yet include a vector type explicitly tied to the second interpretation (SIMD mappings). However, there are already extensions that allow us to write explicit vector code that maps directly to SIMD instructions in the hardware, designed for expert programmers who want to tune code for a specific architecture and take control from the compiler vectorizers. We should also expect another vector type to eventually appear in SY CL to cover the second interpretation, likely aligned with the proposed C++ std::simd templates. This new class would make it very clear when code is written in an explicit vector style, to reduce confusion. Both the existing extensions and a future std::simd-like type in SY CL are niche features that we expect will be used by few developers.

With marray and a dedicated SIMD class, our intent as programmers will be clear from the code that we write. This will be less error prone, less confusing, and may even reduce the number of heated discussions between expert developers when the question arises: “What is a vector?”

## Our Mental Model for SYCL Vector Types

Throughout this book, we talk about how work-items can be grouped together to expose powerful communication and synchronization primitives, such as sub-group barriers and shuffles. For these operations to be efficient on vector hardware, there is an assumption that different workitems in a sub-group combine and map to SIMD instructions. Said another way, multiple work-items are grouped together by the compiler, at which point they can map to SIMD instructions in the hardware. Remember from Chapter 4 that this is a basic premise of SPMD (single program, multiple data) programming models that operate on top of vector hardware, where a single work-item constitutes a lane of what might be a SIMD instruction in hardware, instead of a work-item defining the entire operation that will be a SIMD instruction in the hardware. You can think of the compiler as always vectorizing across work-items when mapping to SIMD instructions in hardware, when programming in a SPMD style.

For developers coming from languages that don’t have vector types, or from GPU shading languages, we can think of SYCL vector types as being local to a work-item, in that if there is an addition of two four-element vectors that addition might take four instructions in the hardware (it would be scalarized from the perspective of the work-item). Each element of the vectors would be added by a different instruction/clock cycle in the hardware. This is consistent with our interpretation of vector types as a convenience—we can add two vectors in a single operation in our source code, as opposed to performing four scalar operations in our source.

For developers coming from a CPU background, we should know that implicit vectorization for SIMD hardware occurs by default in many compilers, independent of vector type usage. The compiler may perform this implicit vectorization across work-items, extract the vector operations from well-formed loops, or honor vector types when mapping to vector instructions—see Chapter 16 for more information.

The rest of this chapter focuses on teaching vectors using the convenience interpretation of vector types (for both marray and vec), and that is the one that we should keep in our minds when programming in SYCL.

## OTHER IMPLEMENTATIONS POSSIBLE!

Different compilers and implementations of SY CL can in theory make different decisions on how vector data types in code map to SIMD vector hardware instructions. We should read a vendor’s documentation and optimization guides to understand how to write code that will map to efficient SIMD instructions, though the thinking and programming patterns that are described in this chapter are applicable to most (ideally all) SY CL implementations.

## Math Array (marray)

The SYCL math array type (marray), see Figure 11-1, is a new addition in SYCL 2020 which has been defined to disambiguate different interpretations of how vector types should behave. marray explicitly represents the first interpretation of vector types introduced in the previous section of this chapter—a convenience type unrelated to vector hardware instructions. By removing “vector” from the name and by including “array” instead, it becomes easier to remember and reason about how the type will be logically implemented on hardware.

<table><tr><td>Type Alias</td><td>marray Equivalent</td></tr><tr><td>mcharN</td><td>marray</td></tr><tr><td>mucharN</td><td>marray</td></tr><tr><td>mshortN</td><td>marray</td></tr><tr><td>mushortN</td><td>marray</td></tr><tr><td>mintN</td><td>marray</td></tr><tr><td>muintN</td><td>marray</td></tr><tr><td>mlongN</td><td>marray</td></tr><tr><td>mulongN</td><td>marray</td></tr><tr><td>mhalfN</td><td>marray</td></tr><tr><td>mfloatN</td><td>marray</td></tr><tr><td>mdoubleN</td><td>marray</td></tr><tr><td>mboolN</td><td>marray</td></tr></table>

Figure 11-1. Type aliases for math arrays

The marray class is templated on its element type and number of elements. The number of elements parameter, NumElements, is a positive integer—when NumElements is 1, an marray is implicitly convertible to an equivalent scalar type. The element type parameter, DataT, must be a numeric type as defined by C++.

Marray is an array container, like std::array, with additional support for mathematical operators (e.g., +, +=) and SYCL mathematical functions (e.g., sin, cos) on arrays. It is designed to provide efficient and optimized array operations for parallel computation on SYCL devices.

For convenience, SYCL provides type aliases for math arrays. For these type aliases, the number of elements N must be 2, 3, 4, 8, or 16.

Figure 11-2 shows a simple example how to apply the cos function to every element in an marray consisting of four floats. This example highlights the convenience of using marray to express operations that apply to all elements of a collection of data assigned to each work-item.

```txt
queue q;
marray<float, 4> input{1.0004f, 1e-4f, 1.4f, 14.0f};
marray<float, 4> res[M];
for (int i = 0; i < M; i++)
    res[i] = {-(i + 1), -(i + 1), -(i + 1), -(i + 1)};
{
    buffer in_buf(&input, range{1});
    buffer re_buf(res, range{M});

    q.submit([&](handler &cgh) {
        accessor re_acc{re_buf, cgh, read_write};
        accessor in_acc{in_buf, cgh, read_only};

        cgh.parallel_for(range<1>(M), [=](id<1> idx) {
            int i = idx[0];
            re_acc[i] = cos(in_acc[0]);
        });
    });
}
```

## Figure 11-2. A simple example using marray

By executing this kernel over a large range of data M, we can achieve good parallelism on many different types of devices, including those that are much wider than the four elements of the marray, without prescribing how our code maps to a SIMD instruction set operating on vector types.

## Vector (vec)

The SYCL vector type (vec) existed in SYCL 1.2.1 and is still included in SYCL 2020. As mentioned previously, vec is compatible with either interpretation of a vector type. In practice, vec is typically interpreted as a convenience type, and our recommendation is therefore to use marray instead to improve code readability and reduce ambiguity. However, there are three exceptions to this recommendation, which we will cover in this section: vector loads and stores, interoperability with backend-native vector types, and operations known as “swizzles”.

Like marray, the vec class is templated on its number of elements and element type. However, unlike marray, the NumElements parameter must be either 1, 2, 3, 4, 8, or 16, and any other value will produce a compilation failure. This is a good example of the confusion around vector types impacting vec’s design: limiting the size of a vector to small powers of 2 makes sense for SIMD instruction sets but appears arbitrary from the perspective of a programmer looking for a convenience type. The element type parameter, DataT, can be any of the basic scalar types supported in device code.

Also, like marray, vec exposes shorthand type aliases for 2, 3, 4, 8, and 16 elements. Whereas marray aliases are prefixed with an “m”, vec aliases are not, for example, uint4 is an alias to vec<uint32\_t, 4> and float16 is an alias to vec<float, 16>. It is important we pay close attention to the presence or absence of this “m” when working with vector types, to ensure we know which class we are dealing with.

## Loads and Stores

The vec class provides member functions for loading and storing the elements of a vector. These operations act on contiguous memory locations storing objects of the same type as the channels of the vector.

The load and store functions are shown in Figure 11-3. The load member function reads values of type DataT from memory at the address of the multi\_ptr, offset by NumElements \* offset elements of DataT, and writes those values to the channels of the vec. The store member function reads the channels of a vec and writes those values to memory at the address of the multi\_ptr, offset by NumElements \* offset elements of DataT.

Note that the parameter is a multi\_ptr, rather than an accessor or raw pointer. The data type of the multi\_ptr is DataT, that is, the data type of the components of the vec class specialization. This requires that the pointer passed to either load or store must match the component type of the vec instance itself.

```cpp
template <access::address_space AddressSpace, access::decorated IsDecorated>
  void load(size_t offset, multi_ptr<DataT, AddressSpace, IsDecorated> ptr);

template <access::address_space addressSpace, access::decorated IsDecorated>
  void store(size_t offset, multi_ptr<DataT, AddressSpace, IsDecorated> ptr) const;
```

## Figure 11-3. vec load and store functions

A simple example of using the load and store functions is shown in Figure 11-4.

```cpp
std::array<float, size> fpData;
for (int i = 0; i < size; i++) {
    fpData[i] = 8.0f;
}

buffer fpBuf(fpData);

queue q;
q.submit([&](handler& h) {
    accessor acc{fpBuf, h};

    h.parallel_for(workers, [=](id<1> idx) {
        float16 inpf16;
        inpf16.load(idx, acc.get_multi_ptr<access::decorated::no>());
        float16 result = inpf16 * 2.0f;
        result.store(idx, acc.get_multi_ptr<access::decorated::no>());
    });
});
```

## Figure 11-4. Use of load and store member functions

The SYCL vector load and store functions provide abstractions for expressing vector operations, but the underlying hardware architecture and compiler optimizations will determine any actual performance benefits. We recommend analyzing performance using profiling tools and experimenting with different strategies to find the best utilization of vector load and store operations for specific use cases.

Even though we should not expect vector load and store operations to map to SIMD instructions, using vector load and store functions can still help to improve memory bandwidth utilization. Operating on vector types effectively is a hint to the compiler that each work-item is accessing a contiguous block of memory, and certain devices may be able to leverage this information to load or store multiple elements at once, thereby improving efficiency.

## Interoperability with Backend-Native Vector Types

The SYCL vec class template may also provide interoperability with a backend’s native vector type (if one exists). The backend-native vector type is defined by the member type vector\_t and is available only in device code. The vec class can be constructed from an instance of vector\_t and can be implicitly converted to an instance of vector\_t.

Most of us will never need to use vector\_t, as its use cases are very limited; it exists only to allow interoperability with backend-native functions called from within a kernel function (e.g., calling a function written in OpenCL C from within a SYCL kernel).

## Swizzle Operations

In graphics applications, swizzling means rearranging the data elements of a vector. For example, if a vector a contains the elements {1, 2, 3, 4}, and knowing that the components of a four-element vector can be referred to as {x, y, z, w}, we could write b = a.wxyz(), and the values in the vector b would be {4, 1, 2, 3}. This syntax is common in applications for code compactness and where there is efficient hardware for such operations.

The vec class allows swizzles to be performed in one of two ways, as shown in Figure 11-5.

```c
template <int... swizzleindexes>
__swizzled_vec__ swizzle() const;
__swizzled_vec__ XYZW_ACCESS() const;
__swizzled_vec__ RGBA_ACCESS() const;
__swizzled_vec__ INDEX_ACCESS() const;

#ifdef SYCL_SIMPLE_SWIZZLES
// Available only when numElements <= 4
// XYZW_SWIZZLE is all permutations with repetition of:
// x, y, z, w, subject to numElements
__swizzled_vec__ XYZW_SWIZZLE() const;

// Available only when numElements == 4
// RGBA_SWIZZLE is all permutations with repetition of: r,
// g, b, a.
__swizzled_vec__ RGBA_SWIZZLE() const;
#endif
```  
Figure 11-5. vec swizzle member functions

The swizzle member function template allows us to perform swizzle operations by calling the template member function swizzle. This member function takes a variadic number of integer template arguments, where each argument represents the swizzle index for the corresponding element in the vector. The swizzle indices must be integers between 0 and NumElements-1, where NumElements represents the number of elements in the original SYCL vector (e.g., vec.swizzle<2, 1, 0, 3>() for a vector of four elements). The return type of the swizzle member function is always an instance of \_\_swizzled\_vec\_\_, which is an implementation-defined temporary class representing the swizzled vector. Note that the swizzle operation is not performed immediately when calling swizzle. Instead, the swizzle operation is performed when the returned \_\_swizzled\_vec\_ instance is used within an expression.

The set of simple swizzle member functions, described in the SYCL specification as XYZW\_SWIZZLE and RGBA\_SWIZZLE, are provided as an alternative way to perform swizzle operations. These member functions are only available for vectors with up to four elements, and only if the SYCL\_SIMPLE\_SWIZZLES macro is defined before any SYCL header files.

The simple swizzle member functions allow us to refer to the elements of a vector using the names {x, y, z, w} or {r, g, b, a} and to perform swizzle operations by calling member functions using these element names directly.

For example, simple swizzles enable the XYZW swizzle syntax a.wxyz() used previously. The same operation can be performed equivalently using RGBA swizzles by writing a.argb(). Using simple swizzles can produce more compact code and code that is a closer match to other languages, especially graphics shading languages. Simple swizzles can also better express programmer intent when a vector contains XYZW position data or RGBA color data. The return type of the simple swizzle member functions is also \_\_swizzled\_vec\_\_. Like the swizzle member function template, the actual swizzle operation is performed when the returned \_\_swizzled\_vec\_\_ instance is used within an expression.

```cpp
constexpr int size = 16;

std::array<float4, size> input;
for (int i = 0; i < size; i++) {
    input[i] = float4(8.0f, 6.0f, 2.0f, i);
}

buffer b(input);

queue q;
q.submit([&](handler& h) {
    accessor a{b, h};

    // We can access the individual elements of a vector
    // using the functions x(), y(), z(), w() and so on.
    //
    // "Swizzles" can be used by calling a vector member
    // equivalent to the swizzle order that we need, for
    // example zyx() or any combination of the elements.
    // The swizzle need not be the same size as the
    // original vector.
    h.parallel_for(size, [=](id<1> idx) {
        auto e = a[idx];
        float w = e.w();
        float4 sw = e.xyzw();
        sw = e.xyzw() * sw.wzyx();
        sw = sw + w;
        a[idx] = sw.xyzw();
    });
});
```

## Figure 11-6. Example of using the \_\_swizzled\_vec\_\_ class

Figure 11-6 demonstrates the usage of simple swizzles and the swizzled\_vec\_\_ class. Although the \_\_swizzled\_vec\_\_ does not appear directly in our code, it is used within expressions such as b.xyzw() \* sw.wzyx(): the return type of b.xyzw() and sw.wzyx() is instances of \_swizzled\_vec\_\_, and the multiplication is not evaluated until the result is assigned back to the float4 variable sw.

## How Vector Types Execute

As described throughout this chapter, there are two different interpretations of vector types and how they might map to hardware. Until this point, we have deliberately only discussed these mappings at a high level. In this section, we will take a deeper look into exactly how different interpretations of the vector types may map to low-level hardware features such as SIMD registers, demonstrating that both interpretations can make efficient use of vector hardware.

## Vectors as Convenience Types

There are three primary points that we’d like to make around how vectors map from convenience types (e.g., marray and usually vec) to hardware implementations:

1. To leverage the portability and expressiveness of the SPMD programming model, we should think of multiple work-items being combined to create vector hardware instructions. More specifically, we should not think of vector hardware instructions being created from a single work-item in isolation.

2. As a consequence of (1), we should think of operations (e.g., addition) on a vector as executing per-channel or per-element in time, from the perspective of one work-item. Using vectors in our source code is usually unrelated to taking advantage of underlying vector hardware instructions.

3. Compilers are required to obey the memory layout requirements of vectors and math arrays if we write code in certain ways, such as by passing the address of a vector to a function, which can cause surprising performance impacts. Understanding this can make it easier to write code which compilers can aggressively optimize.

We will start by further describing the first two points, because a clear mental model can make it much easier to write code.

As described in Chapters 4 and 9, a work-item is the leaf node of the parallelism hierarchy and represents an individual instance of a kernel function. Work-items can be executed in any order and cannot communicate or synchronize with each other except through atomic memory operations to local or global memory, or through group collective functions (e.g., select\_from\_group, group\_barrier).

Instances of convenience types are local to a single work-item and can therefore be thought of as equivalent to a private array of NumElements per work-item. For example, the storage of a float4 y4 declaration can be considered equivalent to float y4[4]. Consider the example shown in Figure 11-7.

```txt
h.parallel_for(8, [=](id<1> i) {
  float x = a[i];
  float4 y4 = b[i];
  a[i] = x + sycl::length(y4);
});
```

## Figure 11-7. Vector execution example

For the scalar variable x, the result of kernel execution with multiple work-items on hardware that has SIMD instructions (e.g., CPUs, GPUs) might use a vector register and SIMD instructions, but the vectorization is across work-items and unrelated to any vector type in our code. Each work-item, with its own scalar x, could form a different lane in an implicit

SIMD hardware instruction that the compiler generates, as shown in Figure 11-8. The scalar data in a work-item can be thought of as being implicitly vectorized (combined into SIMD hardware instructions) across work-items that happen to execute at the same time, in some implementations and on some hardware, but the work-item code that we write does not encode this in any way—this is the core of the SPMD style of programming.

<table><tr><td>Work-item ID</td><td>w0</td><td>w1</td><td>w2</td><td>w3</td><td>w4</td><td>w5</td><td>w6</td><td>w7</td></tr><tr><td>SIMD hardware instruction lanes</td><td>x [w0]</td><td>x [w1]</td><td>x [w2]</td><td>x [w3]</td><td>x [w4]</td><td>x [w5]</td><td>x [w6]</td><td>x [w7]</td></tr></table>

Figure 11-8. Possible expansion from scalar variable x to eight-wide hardware vector instruction

Exposing potential parallelism in a hardware-agnostic way ensures that our applications can scale up (or down) to fit the capabilities of different platforms, including those with vector hardware instructions. Striking the right balance between work-item and other forms of parallelism during application development is a challenge that we must all engage with, and is covered in more detail in Chapters 15, 16, and 17.

With the implicit vector expansion from scalar variable x to a vector hardware instruction by the compiler as shown in Figure 11-8, the compiler creates a SIMD operation in hardware from a scalar operation that occurs in multiple work-items.

Returning to the code example in Figure 11-7, for the vector variable y4, the result of kernel execution for multiple work-items (e.g., eight work-items) does not process the four-element vector by using vector operations in hardware. Instead, each work-item independently sees its own vector (float4 in this case), and the operations on elements of that vector may occur across multiple clock cycles/instructions. This is shown in Figure 11-9. We can think of the vectors as having been scalarized by the compiler from the perspective of a work-item.

<table><tr><td>Scalarized ops</td><td>Exec cycle</td><td colspan="8">Work-item ID</td></tr><tr><td></td><td></td><td>w0</td><td>w1</td><td>w2</td><td>w3</td><td>w4</td><td>w5</td><td>w6</td><td>w7</td></tr><tr><td>y4.x</td><td>N</td><td>y4[w0].x</td><td>y4[w1].x</td><td>y4[w2].x</td><td>y4[w3].x</td><td>y4[w4].x</td><td>y4[w5].x</td><td>y4[w6].x</td><td>y4[w7].x</td></tr><tr><td>y4.y</td><td>N+1</td><td>y4[w0].y</td><td>y4[w1].y</td><td>y4[w2].y</td><td>y4[w3].y</td><td>y4[w4].y</td><td>y4[w5].y</td><td>y4[w6].y</td><td>y4[w7].y</td></tr><tr><td>y4.z</td><td>N+2</td><td>y4[w0].z</td><td>y4[w1].z</td><td>y4[w2].z</td><td>y4[w3].z</td><td>y4[w4].z</td><td>y4[w5].z</td><td>y4[w6].z</td><td>y4[w7].z</td></tr><tr><td>y4.w</td><td>N+3</td><td>y4[w0].w</td><td>y4[w1].w</td><td>y4[w2].w</td><td>y4[w3].w</td><td>y4[w4].w</td><td>y4[w5].w</td><td>y4[w6].w</td><td>y4[w7].w</td></tr></table>

Figure 11-9. Vector hardware instructions access strided memory locations across SIMD lanes

Figure 11-9 also demonstrates the third key point for this section, that the convenience interpretation of vectors can have memory access implications that are important to understand. In the preceding code example, each work-item sees the original (consecutive) data layout of y4, which provides an intuitive model to reason about and tune.

From a performance perspective, the downside of this work-itemcentric vector data layout is that if a compiler vectorizes across work-items to create vector hardware instructions, the lanes of the vector hardware instruction do not access consecutive memory locations. Depending on the vector data size and the capabilities of a specific device; a compiler may need to generate, gather, or scatter memory instructions; as shown in Figure 11-10. This is required because the vectors are contiguous in memory, and neighboring work-items are operating on different vectors in parallel. See Chapters 15 and 16 for more discussion of how vector types may impact execution on specific devices, and be sure to check vendor documentation, compiler optimization reports, and use runtime profiling to understand the efficiency of specific scenarios.

```txt
q.submit([&](sycl::handler &h) { // assume sub group size is 8
// ...
h.parallel_for(range<1>(8), [=](id<1> i) {
    // ...
    float4 y4 = b[i];  // i=0, 1, 2, ...
    // ...
    float x = dowork(&y4);  // the "dowork" expects y4,
                               // i.e., vec_y[8][4] layout
});
```

## Figure 11-10. Vector code example with address escaping

When the compiler can prove that the address of y4 does not escape from the current kernel work-item, or if all callee functions are inlined, then the compiler may perform aggressive optimizations that may improve performance. For example, the compiler can legally transpose the storage of y4 if it is not observable, enabling consecutive memory accesses that avoid the need for gather or scatter instructions. Compiler optimization reports can provide information how our source code has been transformed into vector hardware instructions and can provide hints on how to tweak our code for increased performance.

As a general guideline, we should use convenience vectors (e.g., marray) whenever they make logical sense, because code using these types is much easier to write and maintain. Only when we see performance hotspots in our application should we investigate whether a source code vector operation has been lowered into suboptimal hardware implementation.

## Vectors as SIMD Types

Although we have emphasized in this chapter that marray and vec are not SIMD types, for completeness we include here a brief discussion of how SIMD types may map to vector hardware. This discussion is not coupled to vectors within our SYCL source code but provides background that will be useful as we progress to the later chapters of this book that describe specific device types (GPU, CPU, FPGA), and may help to prepare us for the possible introduction of SIMD types in future versions of SYCL.

SYCL devices may contain SIMD instruction hardware that operates on multiple data values contained in one vector register or a register file. On devices that provide SIMD hardware, we can consider a vector addition operation, for example, on an eight-element vector, as shown in Figure 11-11.

![](images/ae5d82ca4c9cbcc4c5f3dfe584b127caf22c353160f17abe145eedae7a8d0812.jpg)  
Figure 11-11. SIMD addition with eight-way data parallelism

The vector addition in this example could execute in a single instruction using vector hardware, adding the vector registers vec\_x and vec\_y in parallel with that SIMD instruction.

This mapping of SIMD types to vector hardware is very straightforward and predictable, and likely to be performed the same way by any compiler. These properties make SIMD types very attractive for low-level performance tuning on SIMD hardware but come with a cost—the code is less portable and becomes sensitive to details of the specific architecture. The SPMD programming model evolved to combat these costs.

That developers expect SIMD types to have predictable hardware mapping properties is precisely why it is critical to cleanly separate the two interpretations of vectors via two distinct language features: if a developer uses a convenience type expecting it to behave as a SIMD type, they will likely be working against compiler optimizations and will likely see lower performance than hoped or expected.

## Summary

There are multiple interpretations of the term vector within programming languages, and understanding the interpretation that a particular language or compiler has been built around is important when writing performant and scalable code. SYCL has been built around the idea that vector types in source code are convenience types local to a work-item and that implicit vectorization by the compiler across work-items map to SIMD instructions in the hardware. When we (in very rare cases) want to write code which maps directly to vector hardware explicitly, we should look to vendor documentation and in some cases to extensions to SYCL. Most applications should be written assuming that kernels will be vectorized across work-items—doing so leverages the powerful abstraction of SPMD, which provides an easy-to-reason-about programming model, and that provides scalable performance across devices and architectures.

This chapter described the marray interface, which offers convenience out of the box when we have groupings of similarly typed data that we want to operate on (e.g., a pixel with multiple color channels). In addition, we discussed the legacy vec class, which may be convenient for expressing certain patterns (with swizzles) or optimizations (with loads/stores and backend interoperability).

![](images/008dcb4b653d74cccfacba5fd8163609dacc0c96f5c054c1b511e9c4872c4ffd.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
