# sycl Source Lines 6675-7051

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L6675-L7051

Citation: [sycl:L6675-L7051]

````text
## Chapter 13 Practical Tips

One final detail to mention is that host accessors sometime cause an opposite bug in applications, because they also have a lifetime. While a host\_accessor to a buffer is alive, the runtime will not allow that buffer to be used by any devices! The runtime does not analyze our host programs to determine when they might access a host accessor, so the only way for it to know that the host program has finished accessing a buffer is for the host\_accessor destructor to run. As shown in Figure 13-13, this can cause applications to appear to hang if our host program is waiting for some kernels to run (e.g., queue::wait() or acquiring another host accessor) and if the SYCL runtime is waiting for our earlier host accessor(s) to be destroyed before it can run kernels that use a buffer.

When using host accessors, be sure that they are destroyed when no longer needed to unlock use of the buffer by kernels or other host accessors.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create buffers using host allocations (vector in this
// case)
buffer<int> in_buf{N}, out_buf{N};

// Use host accessors to initialize the data
host_accessor in_acc{in_buf}, out_acc{out_buf};
for (int i = 0; i < N; i++) {
    in_acc[i] = i;
    out_acc[i] = 0;
}

// BUG: Host accessors in_acc and out_acc are still alive!
// Later q submits will never start on a device, because
// the runtime doesn't know that we've finished accessing
// the buffers via the host accessors. The device kernels
// can't launch until the host finishes updating the
// buffers, since the host gained access first (before the
// queue submissions). This program will appear to hang!
// Use a debugger in that case.

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

std::cout << "This program will deadlock here!!! Our "
              "host_accessors used\n"
        << " for data initialization are still in "
              "scope, so the runtime won't\n"
        << " allow our kernel to start executing on "
              "the device (the host could\n"
        << " still be initializing the data that is "
              "used by the kernel). The next line\n"
        << " of code is acquiring a host accessor for "
              "the output, which will wait for\n"
        << " the kernel to run first. Since in_acc "
              "and out_acc have not been\n"
        << " destructed, the kernel is not safe for "
              "the runtime to run, and we deadlock.\n";

// Check that all outputs match expected value
// Use host accessor! Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
    std::cout << "A[" << i << "]=" << A[i] << "\n";
```

## Figure 13-13. Deadlock (bug—it hangs!) from improper use of host\_ accessors

## Multiple Translation Units

When we want to call functions inside a kernel that are defined in a different translation unit, those functions need to be labeled with SYCL\_EXTERNAL. Without this decoration, the compiler will only compile a function for use outside of device code (making it illegal to call that external function from within device code).

There are a few restrictions on SYCL\_EXTERNAL functions that do not apply if we define the function within the same translation unit:

• SYCL\_EXTERNAL can only be used on functions.

• SYCL\_EXTERNAL functions cannot use raw pointers as parameter or return types. Explicit pointer classes must be used instead.

• SYCL\_EXTERNAL functions cannot call a parallel\_ for\_work\_item method.

• SYCL\_EXTERNAL functions cannot be called from within a parallel\_for\_work\_group scope.

If we try to compile a kernel that is calling a function that is not inside the same translation unit and is not declared with SYCL\_EXTERNAL, then we can expect a compile error similar to

error: SYCL kernel cannot call an undefined function without SYCL\_EXTERNAL attribute

If the function itself is compiled without a SYCL\_EXTERNAL attribute, we can expect to see either a link or runtime failure such as

terminate called after throwing an instance of '...compile\_ program\_error'...

error: undefined reference to ...

SYCL does not require compilers to support SYCL\_EXTERNAL; it is an optional feature in general. DPC++ supports SYCL\_EXTERNAL.

## Performance Implication of Multiple Translation Units

An implication of the compilation model (see earlier in this chapter) is that if we scatter our device code into multiple translation units, that may trigger more invocations of just-in-time compilation than if our device code is colocated. This is highly implementation-dependent and is subject to changes over time as implementations mature.

Such effects on performance are minor enough to ignore through most of our development work, but when we get to fine-tuning to maximize code performance, there are two things we can consider to mitigate these effects: (1) group device code together in the same translation unit, and (2) use ahead-of-time compilation to avoid just-in-time compilation effects entirely. Since both of these require some effort on our part, we only do this when we have finished our development and are trying to squeeze every ounce of performance out of our application. When we do resort to this detailed tuning, it is worth testing changes to observe their effect on the exact SYCL implementation that we are using.

## When Anonymous Lambdas Need Names

SYCL allows for assigning names to lambdas in case tools need it and for debugging purposes (e.g., to enable displays in terms of user-defined names). Naming lambdas is optional per the SYCL 2020 specification. Throughout most of this book, anonymous lambdas are used for kernels because names are not needed when using C++ with SYCL (except for passing of compile options as described with lambda naming discussion in Chapter 10).

When we have an advanced need to mix SYCL tools from multiple vendors in a codebase, the tooling may require that we name lambdas. This is done by adding a <class uniquename> to the SYCL action construct in which the lambda is used (e.g., parallel\_for). This naming allows tools from multiple vendors to interact in a defined way within a single compilation and can also help by displaying kernel names that we define within debug tools and layers.

We also need to name kernels if we want to use kernel queries. The SYCL standards committee was unable to find a solution to requiring this in the SYCL 2020 standard. For instance, querying a kernel’s preferred\_work\_group\_size\_multiple requires us to call the get\_info() member function of the kernel class, which requires an instance of the kernel class, which ultimately requires that we know the name (and kernel\_id) of the kernel in order to extract a handle to it from the relevant kernel\_bundle.

## Summary

Popular culture today often refers to tips as life hacks. Unfortunately, programming culture often assigns a negative connotation to hack, so the authors refrained from naming this chapter “SYCL Hacks.” Undoubtedly, this chapter has just touched the surface of what practical tips can be given for using C++ with SYCL. More tips can be shared by all of us as we learn together how to make the most out of C++ with SYCL.

![](images/5886d8b65391ce71bb7c94aa095bc22c514037b2f6a34fdce4623ad8a3fd3c49.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Common Parallel Patterns

When we are at our best as programmers, we recognize patterns in our work and apply techniques that are time-tested to be the best solution. Parallel programming is no different, and it would be a serious mistake not to study the patterns that have proven to be useful in this space. Consider the MapReduce frameworks adopted for Big Data applications; their success stems largely from being based on two simple yet effective parallel patterns—map and reduce.

There are a number of common patterns in parallel programming that crop up time and again, independent of the programming language that we’re using. These patterns are versatile and can be employed at any level of parallelism (e.g., sub-groups, work-groups, full devices) and on any device (e.g., CPUs, GPUs, FPGAs). However, certain properties of the patterns (such as their scalability) may affect their suitability for different devices. In some cases, adapting an application to a new device may simply require choosing appropriate parameters or fine-tuning an implementation of a pattern; in others, we may be able to improve performance by selecting a different pattern entirely.

Developing an understanding of how, when, and where to use these common parallel patterns is a key part of improving our proficiency in SYCL (and parallel programming in general). For those with existing

parallel programming experience, seeing how these patterns are expressed in SYCL can be a quick way to spin up and gain familiarity with the capabilities of the language.

This chapter aims to provide answers to the following questions:

• What are some common patterns that we should understand?

• How do the patterns relate to the capabilities of different devices?

• Which patterns are already provided as SYCL functions and libraries?

• How would the patterns be implemented using direct programming?

## Understanding the Patterns

The patterns discussed here are a subset of the parallel patterns described in the book Structured Parallel Programming by McCool et al. We do not cover the patterns related to types of parallelism (e.g., fork-join, branchand-bound) but focus on some of the algorithmic patterns most useful for writing data-parallel kernels.

We wholeheartedly believe that understanding this subset of parallel patterns is critical to becoming an effective SYCL programmer. The table in Figure 14-1 presents a high-level overview of the different patterns, including their primary use cases, their key attributes, and how their attributes impact their affinity for different hardware devices.

<table><tr><td>Pattern</td><td>Useful For</td><td>Key Attributes</td><td>Device Affinity</td></tr><tr><td>Map</td><td>Simple parallel kernels</td><td>No data dependences and high scalability</td><td>All</td></tr><tr><td>Stencil</td><td>Structured data dependences</td><td>Data dependences and data re-use</td><td>Depends on stencil size</td></tr><tr><td>Reduction</td><td>Combining partial results</td><td>Data dependences</td><td>All</td></tr><tr><td>Scan Pack/Unpack</td><td>Filtering and restructuring data</td><td>Limited scalability</td><td>Depends on problem size</td></tr></table>

Figure 14-1. Parallel patterns and their affinity for different device types

## Map

The map pattern is the simplest parallel pattern of all and will be immediately familiar to readers with experience in functional programming languages. As shown in Figure 14-2, each input element of a range is independently mapped to an output by applying some function. Many data-parallel operations can be expressed as instances of the map pattern (e.g., vector addition).

![](images/60b54d3b18c220f3d0c901b5a79710778096046f1b1aae6a04032898f6f419cb.jpg)  
Figure 14-2. Map pattern

## Chapter 14 Common Parallel Patterns

Since every application of the function is completely independent, expressions of map are often very simple, relying on the compiler and/ or runtime to do most of the hard work. We should expect kernels written to the map pattern to be suitable for any device and for the performance of those kernels to scale very well with the amount of available hardware parallelism.

However, we should think carefully before deciding to rewrite entire applications as a series of map kernels! Such a development approach is highly productive and guarantees that an application will be portable to a wide variety of device types but encourages us to ignore optimizations that may significantly improve performance (e.g., improving data reuse, fusing kernels).

## Stencil

The stencil pattern is closely related to the map pattern. As shown in Figure 14-3, a function is applied to an input and a set of neighboring inputs described by a stencil to produce a single output. Stencil patterns appear frequently in many domains, including scientific/engineering applications (e.g., finite difference codes) and computer vision/machine learning applications (e.g., image convolutions).

![](images/bac9ec8f5f9bbfeed98044d6eb67b7f6f14df51e1685da4637ae7bb38ddba9b5.jpg)  
Figure 14-3. Stencil pattern

When the stencil pattern is executed out-of-place (i.e., writing the outputs to a separate storage location), the function can be applied to every input independently. Scheduling stencils in the real world is often more complicated than this: computing neighboring outputs requires the same data, and loading that data from memory multiple times will degrade performance; and we may wish to apply the stencil in-place (i.e., overwriting the original input values) in order to decrease an application’s memory footprint.

The suitability of a stencil kernel for different devices is therefore highly dependent on properties of the stencil and the input problem. Generally speaking,

• Small stencils can benefit from the scratchpad storage of GPUs.

• Large stencils can benefit from the (comparatively) large caches of CPUs.

• Small stencils operating on small inputs can achieve significant performance gains via implementation as systolic arrays on FPGAs.

Since stencils are easy to describe but complex to implement efficiently, many stencil applications make use of a domain-specific language (DSL). There are already several embedded DSLs leveraging the template meta-programming capabilities of C++ to generate highperformance stencil kernels at compile time.

## Reduction

A reduction is a common parallel pattern which combines partial results using an operator that is typically associative and commutative (e.g., addition). The most ubiquitous examples of reductions are computing a sum (e.g., while computing a dot product) or computing the minimum/ maximum value (e.g., using maximum velocity to set time-step size).

Figure 14-4 shows the reduction pattern implemented by way of a tree reduction, which is a popular implementation requiring log (N) combination operations for a range of N input elements. Although tree reductions are common, other implementations are possible—in general, we should not assume that a reduction combines values in a specific order.

![](images/b93ca2a3adbe627ac5422a05826823afdb115dddc41d282446faff36efcd39f6.jpg)  
Figure 14-4. Reduction pattern

Kernels are rarely embarrassingly parallel in real life, and even when they are, they are often paired with reductions (as in MapReduce frameworks) to summarize their results. This makes reductions one of the most important parallel patterns to understand and one that we must be able to execute efficiently on any device.

Tuning a reduction for different devices is a delicate balancing act between the time spent computing partial results and the time spent combining them; using too little parallelism increases computation time, whereas using too much parallelism increases combination time.

It may be tempting to improve overall system utilization by using different devices to perform the computation and combination steps, but such tuning efforts must pay careful attention to the cost of moving data between devices. In practice, we find that performing reductions directly on data as it is produced and on the same device is often the best approach. Using multiple devices to improve the performance of reduction patterns therefore relies not on task parallelism but on another level of data parallelism (i.e., each device performs a reduction on part of the input data).

## Scan

The scan pattern computes a generalized prefix sum using a binary associative operator, and each element of the output represents a partial result. A scan is said to be inclusive if the partial sum for element i is the sum of all elements in the range [0, i] (i.e., the sum including i). A scan is said to be exclusive if the partial sum for element i is the sum of all elements in the range [0, i) (i.e., the sum excluding i).

At first glance, a scan appears to be an inherently serial operation—the value of each output depends on the value of the previous output! While it is true that scan has less opportunities for parallelism than other patterns (and may therefore be less scalable), Figure 14-5 shows that it is possible to implement a parallel scan using multiple sweeps over the same data.

![](images/36299cbb58db138e18b4a9b3c739e7e223583b83540938a52c897bfd69fa3d5e.jpg)  
Figure 14-5. Scan pattern

Because the opportunities for parallelism within a scan operation are limited, the best device on which to execute a scan is highly dependent on problem size: smaller problems are a better fit for a CPU, since only larger problems will contain enough data parallelism to saturate a GPU. Problem size is less of a concern for FPGAs and other spatial architectures since scans naturally lend themselves to pipeline parallelism. As in the case of a reduction, it is usually a good idea to execute the scan operation on the same device that produced the data—considering where and how scan operations fit into an application during optimization will typically produce better results than focusing on optimizing the scan operations in isolation.

## Pack and Unpack

The pack and unpack patterns are closely related to scans and are often implemented on top of scan functionality. We cover them separately here because they enable performant implementations of common operations (e.g., appending to a list) that may not have an obvious connection to prefix sums.

## Pack

The pack pattern, shown in Figure 14-6, discards elements of an input range based on a Boolean condition, packing the elements that are not discarded into contiguous locations of the output range. This Boolean condition could be a precomputed mask or could be computed online by applying some function to each input element.

![](images/b52c04ee4825372878907fef4742e16dec89a3bd86c3070404ff22f6dc5c4dd6.jpg)  
Figure 14-6. Pack pattern

Like with scan, there is an inherently serial nature to the pack operation. Given an input element to pack/copy, computing its location in the output range requires information about how many prior elements were also packed/copied into the output. This information is equivalent to an exclusive scan over the Boolean condition driving the pack.

## Unpack

As shown in Figure 14-7 (and as its name suggests), the unpack pattern is the opposite of the pack pattern. Contiguous elements of an input range are unpacked into noncontiguous elements of an output range, leaving other elements untouched. The most obvious use case for this pattern is to unpack data that was previously packed, but it can also be used to fill in “gaps” in data resulting from some previous computation.

![](images/e6dfb410ef60517d9c523fada697faaa38d9305188a5a9f731ae958437726e34.jpg)  
Figure 14-7. Unpack pattern

## Using Built-In Functions and Libraries

Many of these patterns can be expressed directly using builtin functionality of SYCL or vendor-provided libraries written in SYCL. Leveraging these functions and libraries is the best way to balance performance, portability, and productivity in real large-scale software engineering projects.

## The SYCL Reduction Library

Rather than require that each of us maintain our own library of portable and highly performant reduction kernels, SYCL provides a convenient abstraction for describing variables with reduction semantics. This abstraction simplifies the expression of reduction kernels and makes the fact that a reduction is being performed explicit, allowing implementations to select between different reduction algorithms for different combinations of device, data type, and reduction operation.

The kernel in Figure 14-8 shows an example of using the reduction library. Note that the kernel body doesn’t contain any reference to reductions—all we must specify is that the kernel contains a reduction which combines instances of the sum variable using the plus functor. This provides enough information for an implementation to automatically generate an optimized reduction sequence.

```javascript
h.parallel_for(
    range<1>{N}, reduction(sum, plus<>()),
    [=](id<1> i, auto& sum) { sum += data[i]; });
```

Figure 14-8. Reduction expressed as a data-parallel kernel using the reduction library

The result of a reduction is not guaranteed to be written back to the original variable until the kernel has completed. Apart from this restriction, accessing the result of a reduction behaves identically to accessing any other variable in SYCL: accessing a reduction result stored in a buffer requires the creation of an appropriate device or host accessor, and accessing a reduction result stored in a USM allocation may require explicit synchronization and/or memory movement.

One important way in which the SYCL reduction library differs from reduction abstractions found in other languages is that it restricts our access to the reduction variable during kernel execution—we cannot inspect the intermediate values of a reduction variable, and we are forbidden from updating the reduction variable using anything other than the specified combination function. These restrictions prevent us from making mistakes that would be hard to debug (e.g., adding to a reduction variable while trying to compute the maximum) and ensure that reductions can be implemented efficiently on a wide variety of different devices.

## The reduction Class

The reduction class is the interface we use to describe the reductions present in a kernel. The only way to construct a reduction object is to use one of the functions shown in Figure 14-9. Note that there are three families of reduction function (for buffers, USM pointers and spans), each with two overloads (with and without an identity variable).

## Chapter 14 Common Parallel Patterns

```cpp
template <typename BufferT, typename BinaryOperation>
unspecified reduction(BufferT variable, handler& h,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename BufferT, typename BinaryOperation>
unspecified reduction(BufferT variable, handler& h,
                       const BufferT::value_type& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename BinaryOperation>
unspecified reduction(T* variable, BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename BinaryOperation>
unspecified reduction(T* variable, const T& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename Extent,
       typename BinaryOperation>
unspecified reduction(span<T, Extent> variables,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename Extent,
       typename BinaryOperation>
unspecified reduction(span<T, Extent> variables,
                       const T& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});
```

## Figure 14-9. Function prototypes of the reduction function

If a reduction is initialized using a buffer or a USM pointer, the reduction is a scalar reduction, operating on the first object in an array. If a reduction is initialized using a span, the reduction is an array reduction. Each component of an array reduction is independent—we can think of an array reduction operating on an array of size N as equivalent to N scalar reductions with the same data type and operator.

The simplest overloads of the function allow us to specify the reduction variable and the operator used to combine the contributions from each work-item. The second set of overloads allow us to provide an optional identity value associated with the reduction operator—this is an optimization for user-defined reductions, which we will revisit later.

Note that the return type of the reduction function is unspecified, and the reduction class itself is completely implementation-defined. Although this may appear slightly unusual for a C++ class, it permits an implementation to use different classes (or a single class with any number of template arguments) to represent different reduction algorithms. Future versions of SYCL may decide to revisit this design in order to enable us to explicitly request specific reduction algorithms in specific execution contexts (most likely, via the property\_list argument).

## The reducer Class

An instance of the reducer class encapsulates a reduction variable, exposing a limited interface ensuring that we cannot update the reduction variable in any way that an implementation could consider to be unsafe. A simplified definition of the reducer class is shown in Figure 14-10. Like the reduction class, the precise definition of the reducer class is implementation-defined—a reducer’s type will depend on how the reduction is being performed, and it is important to know this at compile time in order to maximize performance. However, the functions and operators that allow us to update the reduction variable are well defined and are guaranteed to be supported by any SYCL implementation.

## Chapter 14 Common Parallel Patterns

```cpp
template <typename T, typename BinaryOperation,
         /* implementation-defined */>
class reducer {
  // Combine partial result with reducer's value
  void combine(const T& partial);
};

// Other operators are available for standard binary
// operations
template <typename T>
auto& operator+=(reducer<T, plus::<T>>&, const T&);
```

## Figure 14-10. Simplified definition of the reducer class

Specifically, every reducer provides a combine() function which combines the partial result (from a single work-item) with the value of the reduction variable. How this combine function behaves is implementation-defined but is not something that we need to worry about when writing a kernel. A reducer is also required to make other operators available depending on the reduction operator; for example, the += operator is defined for plus reductions. These additional operators are provided only as a programmer convenience and to improve readability; where they are available, these operators have identical behavior to calling combine() directly.

When working with array reductions, the reducer provides an additional subscript operator (i.e., operator[]), allowing access to individual elements of the array. Rather than returning a reference directly to an element of the array, this operator returns another reducer object, which exposes the same combine() function and shorthand operators as the reducers associated with a scalar reduction. Figure 14-11 shows a simple example of a kernel using an array reduction to compute a histogram, where the subscript operator is used to access only the histogram bin that is updated by the work-item.

```txt
h.parallel_for(
    range{N},
    reduction(span<int, 16>(histogram, 16), plus<>()),
    [=](id<1> i, auto& histogram) {
        histogram[i % B]++;
    });
```

Figure 14-11. An example kernel using an array reduction to compute a histogram

## User-Defined Reductions

Several common reduction algorithms (e.g., a tree reduction) do not see each work-item directly update a single shared variable, but instead accumulate some partial result in a private variable that will be combined at some point in the future. Such private variables introduce a problem: how should the implementation initialize them? Initializing variables to the first contribution from each work-item has potential performance ramifications, since additional logic is required to detect and handle uninitialized variables. Initializing variables to the identity of the reduction operator instead avoids the performance penalty but is only possible when the identity is known.

SYCL implementations can only automatically determine the correct identity value to use when a reduction is operating on simple arithmetic types and the reduction operator is one of several standard function objects (e.g., plus). For user-defined reductions (i.e., those operating on user-defined types and/or using user-defined function objects), we may be able to improve performance by specifying the identity value directly.

Support for user-defined reductions is limited to trivially copyable types and combination functions with no side effects, but this is enough to enable many real-life use cases. For example, the code in Figure 14-12 demonstrates the usage of a user-defined reduction to compute both the minimum element in a vector and its location.

## Chapter 14 Common Parallel Patterns

```cpp
template <typename T, typename I>
using minloc = minimum<std::pair<T, I>>;

int main() {
  constexpr size_t N = 16;

  queue q;
  float* data = malloc_shared<float>(N, q);
  std::pair<float, int>* res =
    malloc_shared<std::pair<float, int>>(1, q);
  std::generate(data, data + N, std::mt19937{});

  std::pair<float, int> identity = {
    std::numeric_limits<float>::max(),
    std::numeric_limits<int>::min()};
  *res = identity;

  auto red =
    sycl::reduction(res, identity, minloc<float, int>());
  q.submit([&](handler& h) {
    h.parallel_for(
      range<1>{N}, red, [=](id<1> i, auto& res) {
        std::pair<float, int> partial = {data[i], i};
        res.combine(partial);
      });
    }).wait();

  std::cout << "minimum value = " << res->first << " at "
              << res->second << "\n";
  ...
```

Figure 14-12. Using a user-defined reduction to find the location of the minimum value
````
