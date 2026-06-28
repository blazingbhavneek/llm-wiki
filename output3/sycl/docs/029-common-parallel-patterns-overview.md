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
