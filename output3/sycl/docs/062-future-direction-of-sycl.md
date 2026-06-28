
• Getting Started Guide for the DPC++ Compatibility Tool (tinyurl.com/startDPCpp)

![](images/2f9728d753ff200163fe6b25f46323dce7378e461458a77fe2dce907b64309b9.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Future Direction of SYCL

Take a moment now to feel the peace and calm of knowing that we have covered programming using C++ with SYCL. All the pieces have fallen into place.

We’ve endeavored to ensure that the code samples in previous chapters use standard SYCL 2020 functionality and execute on a wide range of hardware, and the few places we used extensions (e.g., interoperability and FPGA-specific extensions), we call it out. However, the future-looking code shown in this epilogue does not compile with any compiler as of mid-2023.

In this epilogue, we speculate on the future. Our crystal ball can be a bit difficult to read—this epilogue comes without any warranty. Some of the predictions we made in the first edition of this book came true, but others did not.

This epilogue provides a sneak peek of upcoming SYCL features and DPC++ extensions that we are very excited about. We offer no guarantees that the code samples printed in this epilogue compile: some may already be compatible with a compiler released after the book, while others may compile only after some massaging of syntax. Some features may be released as extensions or incorporated into future versions of SYCL, while others may remain experimental features indefinitely. The code samples in the GitHub repository associated with this book may be updated to use new syntax as it evolves. Likewise, we will have an erratum for the

book, which may get additions made from time to time. We recommend checking for updates in these two places (code repository and book errata—links can be found early in Chapter 1).

## Closer Alignment with C++11, C++14, and C++17

Maintaining close alignment between SYCL and C++ has two advantages. First, it enables SYCL to leverage the newest and greatest features of C++ to improve developer productivity. Second, it increases the chances of heterogeneous programming features introduced in SYCL successfully influencing the future direction of C++.

SYCL 1.2.1 was based on C++11, and many of the biggest improvements to the interfaces of SYCL 2020 are only possible because of language features introduced in C++14 (e.g., generic lambdas) and C++17 (e.g., class template argument deduction—CTAD). We expect SYCL and C++ to grow closer over time, and there are several exciting efforts already underway.

The C++ Standard Template Library (STL) contains several algorithms which correspond to the parallel patterns discussed in Chapter 17. The algorithms in the STL typically apply to sequences specified by pairs of iterators and—starting with C++17—support an execution policy argument denoting whether they should be executed sequentially or in parallel. The standard allows for implementations to define their own execution policies, too, and the oneAPI DPC++ Library (oneDPL) covered in Chapter 18 leverages such a custom execution policy to enable algorithms to execute on SYCL devices. The result is a high-productivity approach to programming heterogeneous devices—if an application can be expressed solely using functionality of the STL algorithms, oneDPL makes it possible to make use of the accelerators in our systems without writing a single line of SYCL kernel code! There are still open questions about how the STL algorithms should interact with certain SYCL concepts (e.g., buffers), and how to ensure that all the standard library classes we might want (e.g., std::complex, std::atomic) are available in device code, but oneDPL is the first step on a long path toward unifying our host and device code.

## Adopting Features from C++20, C++23 and Beyond

The SYCL specification deliberately trails behind C++ to ensure that the features it uses have broad compiler support. However, SYCL committee members—many of whom are also involved in ISO C++ committees—are keeping a close eye on how future versions of C++ are developing.

Adopting C++ or SYCL features we discuss here that are not finalized yet into a specification could be a mistake—features may change significantly before making it into a standard. Nevertheless, there are a number of features under discussion that may change the way that future SYCL programs look and behave which are worth discussing.

Some of the features in SYCL 2020 were informed by C++20 (e.g., std::atomic\_ref) and others were pre-adopted into the sycl:: namespace (e.g., std::bit\_cast, std::span). As we move toward the next official release of SYCL, we expect to align with C++20 more closely and incorporate the most useful parts of it. For example, C++20 introduced some additional thread synchronization routines in the form of std::latch and std::barrier; we already explored in Chapter 19 how similar interfaces could be used to define device-wide barriers, and it may make sense to reexamine sub-group and work-group barriers in the context of the new C++20 syntax as well.

One of the most exciting features in C++23 is mdspan, a non-owning view of data that provides both multidimensional array syntax for pointers and an AccessorPolicy as an extension point for controlling access to the underlying data. These semantics are very similar to those of SYCL

accessors, and mdspan would enable accessor-like syntax to be used for both buffers and USM allocations, as shown in Figure EP-1.

```cpp
queue q;
constexpr int N = 4;
constexpr int M = 2;
int* data = malloc_shared<int>(N * M, q);

stackx::mdspan<int, N, M> view{data};
q.parallel_for(range<2>{N, M}, [=](id<2> idx) {
    int i = idx[0];
    int j = idx[1];
    view(i, j) = i * M + j;
}).wait();
```

Figure EP-1. Attaching accessor-like indexing to a USM pointer using mdspan

Hopefully it is only a matter of time until SYCL officially supports mdspan. In the meantime, we recommend that interested readers experiment with the open source production-quality reference implementation available as part of the Kokkos project.

## Mixing SPMD and SIMD Programming

Another exciting, proposed feature for C++ is the std::simd class template, which seeks to provide a portable interface for explicit vector parallelism in C++. Adopting this interface would provide a clear distinction between the two different uses of vector types described in Chapter 11: uses of vector types for programmer convenience and uses of vector types by ninja programmers for low-level performance tuning. The presence of support for both SPMD and SIMD programming styles within the same language also raises some interesting questions: how should we declare which style a kernel uses, and should we be able to mix and match styles within the same kernel?

We have started to explore potential answers to this question in the form of a DPC++ extension (sycl\_ext\_oneapi\_invoke\_simd), which provides a new invoke\_simd function (modelled on std::invoke) that allows developers to call explicitly vectorized (SIMD) code from within an SPMD kernel. The call to invoke\_simd acts as a clear boundary between the two execution models implied by the two programming styles and defines how data should flow between them. The code in Figure EP-2 shows a very simple example of invoke\_simd’s usage, calling out to a function that expects to receive a combination of scalar and vector (simd) arguments.

```cpp
// Function expects one vector argument (x) and one scalar
// argument (n)
simd<float, 8> scale(simd<float, 8> x, float n) {
  return x * n;
}

q.parallel_for(..., sycl::nd_item<1> it)
    [[sycl::reqd_sub_group_size(8)]] {
  // In SPMD code, each work-item has its own x and n
  // variables
  float x = ...;
  float n = ...;

  // Invoke SIMD function (scale) using work-items in the
  // sub-group x values from each work-item are combined
  // into a simd<float, 8>
  // The value of n is defined to be the
  // same (uniform) across all work-items
  // Returned simd<float, 8> is unpacked
  sycl::sub_group sg = it.get_sub_group();
  float y = invoke_simd(sg, scale, x, uniform(n));
});
```

## Figure EP-2. A simple example of invoking a SIMD function from a SPMD kernel

The approach taken by invoke\_simd has several advantages. First, there can be no nasty surprises— functions with a different execution model are invoked explicitly, and the user is responsible for describing how to marshal data back and forth. Second, the mechanism allows

for fine-grained specialization—it is possible to write just a few lines of explicitly vectorized code (e.g., for performance tuning) without having to throw away the rest of our SPMD code. Finally, it is straightforward to extend—invoke\_simd itself can be extended to support new groups or new argument mappings via simple overloading, and similar invoke\_\* functions could be introduced to handle interoperability with different contexts (e.g., code written in a language that isn’t SYCL).

## Address Spaces

The introduction of generic address space support in SYCL 2020 has the potential to greatly simplify many codes, by allowing us to use regular C++ pointers without worrying about what kind of memory is being used. Many modern architectures provide hardware support for the generic address space, and so we can expect code using regular C++ pointers to work across a wide variety of machines and with minimal performance overhead.

However, there are some (older, or more special purpose) architectures on which generic address space support is a more complicated story. Some hardware may use different instructions to access different kinds of memory, requiring compilers to identify a concrete address space at compile time (i.e., to generate the correct instructions). There may also be SYCL backends incapable of representing a generic address space (e.g., OpenCL 1.2). SYCL 2020 makes allowances for such hardware and backends via a set of inference rules for deducing address spaces.

The address space deduction rules were inherited from SYCL 1.2.1, and the SYCL 2020 specification includes a note that the rules will be revisited in a future version of SYCL. Although it is unclear at the time of writing exactly how these rules will change, SYCL’s long-term thinking is clear: in most cases, we should not be concerned with address space management and should trust the compiler and hardware to do the right thing.

## Specialization Mechanism

There are plans to introduce compile-time queries enabling kernels to be specialized based on properties (aspects) of the targeted device (e.g., the device type, support for a specific extension, the size of work-group local memory, the sub-group size selected by the compiler). Such queries require a new kind of constant expression not currently present in C++— they are not necessarily constexpr when the host code is compiled but become constexpr when the target device becomes known.

The exact mechanism used to expose this “device-constant expression” concept is still being designed. We expect it to build on the specialization constants feature introduced in SYCL 2020 and to look and behave similarly to the code shown in Figure EP-3.

```cpp
h.parallel_for(range{1}, [=](id<1> idx) {
  if_device_has<aspect::cpu>([&]() {
    /* Code specialized for CPUs */
    out << "On a CPU!" << endl;
  }).else_if_device_has<aspect::gpu>([&]() {
    /* Code specialized for GPUs */
    out << "On a GPU!" << endl;
  });
});
```

Figure EP-3. Specializing kernel code based on device aspects at kernel compile time

## Compile-Time Properties

SYCL allows the behavior of certain classes (e.g., buffers, accessors) to be modified by passing a property list into the constructor. These properties are already very powerful, but their power is limited by the fact that the properties passed to a constructor are not known until runtime. Allowing for certain properties to be declared at compile time has the potential to significantly improve performance, by reducing the number of runtime checks and by enabling compilers to aggressively specialize both host and device code in the presence of specific properties.

The DPC++ compiler supports an experimental extension for compiletime properties (sycl\_ext\_oneapi\_properties), and it already enables a wide variety of other extensions:

Pointers annotated with information extending beyond just address spaces, which could inform the future of sycl::multi\_ptr (sycl\_ext\_oneapi\_annotated\_ptr)

Kernel configuration controls, which could replace C++ attributes and increase the capabilities of libraryonly SYCL implementations (sycl\_ext\_oneapi\_kernel\_ properties)

Descriptions of desired memory behavior and access controls (sycl\_ext\_oneapi\_device\_global, sycl\_ext\_ oneapi\_prefetch)

Our early experience with compile-time properties has been very positive, and we’re finding more and more potential use cases for them all the time. Given their wide applicability, we are keen to see some version of compile-time properties adopted in a future SYCL specification.

## Summary

There is already a lot of excitement around SYCL, and this is just the beginning! We (as a community) have a long path ahead of us, and it will take significant continued effort to distill the best practices for heterogeneous programming and to design new language features that strike the desired balance between performance, portability, and productivity.

We need your help! If your favorite feature of C++ (or any other programming language) is missing from SYCL, please reach out to us. Together, we can shape the future direction of SYCL and C++.

## For More Information

• Khronos SYCL Registry, www.khronos.org/ registry/SYCL

• H. Carter Edwards et al., “mdspan: A Non-Owning Multidimensional Array Reference,” wg21.link/p0009

• D. Hollman et al., “Production-Quality mdspan Implementation,” github.com/kokkos/mdspan

• Intel DPC++ Compiler Extensions, tinyurl.com/ syclextend
